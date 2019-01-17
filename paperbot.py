import os
import re
import time
import config
import websocket
import numpy as np
from websocket import *
from websocket._exceptions import WebSocketConnectionClosedException
from datetime import datetime
from collections import Counter
from slackclient import SlackClient
from commands import create_commands
from arxivreader import print_arxiv_paper, all_arxiv_section, get_author_list_arxiv

MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def time_as_int(tm):
    return int(tm[0:2])*60**2+int(tm[3:5])*60+int(tm[6:8])

try:
    np.load('keywords.npy')
except:
    np.save('keywords.npy',np.array([], dtype=str))

try:
    np.load('keywords_authors.npy')
except:
    np.save('keywords_authors.npy',np.array([], dtype=str))

try:
    np.load('prefered_keywords.npy')
except:
    np.save('prefered_keywords.npy',np.array([["","xquatbot",""]], dtype=str))


if "SLACK_BOT_TOKEN" in config.__dict__:
    SLACK_BOT_TOKEN = config.SLACK_BOT_TOKEN
else:
    SLACK_BOT_TOKEN = False
    print("No SLACK_BOT_TOKEN given\n"
          "The bot will not connect to slack")

if "BOT_CHANNEL" in config.__dict__:
    BOT_CHANNEL = config.BOT_CHANNEL
elif "auto_commands" in config.__dict__ and len(config.auto_commands) > 0:
    BOT_CHANNEL = False
    print("No channel for the automated commands given, \n"
          "To use automated commands, add a 'bot_channel' in the config.py")

arxiv_sections = []
if "arxiv_sections" in config.__dict__:
    for section in config.arxiv_sections:
        if section in all_arxiv_section:
            arxiv_sections.append(section)
        else:
            print("arxiv_sections: '" + section + "' not available.")
else:
    print("No default arxiv sections given.\n"
          "Manually indicate the section when calling the bot.")

commands = {'HELP_COMMAND':"help",
            'PAPER_COMMAND':"paper",
            'ADD_KW_COMMAND':"add",
            'REMOVE_KW_COMMAND':"rm",
            'PRINT_KW_COMMAND':"list",
            'ADD_AUTHOR_COMMAND':"add_author",
            'REMOVE_AUTHOR_COMMAND':"rm_author",
            'PRINT_AUTHOR_COMMAND':"authors",
            'ADD_PKW_COMMAND':"add_special",
            'REMOVE_PKW_COMMAND':"rm_special",
            'PRINT_PKW_COMMAND':"special",
            'BUILD_AUTHOR_LIST':"build"}

if "commands" in config.__dict__:
    commands.update(config.commands)
else:
    print("No commands names given.\n"
          "Default values will be used.")

paper_commands = []
if "paper_commands" in config.__dict__:
    paper_commands = config.paper_commands

paper_command_list = create_commands(commands['PAPER_COMMAND'], arxiv_sections, paper_commands)


def read_auto_commands(auto_commands):
    cleaned_commands = []
    for time, days, command in auto_commands:
        try:
            time_ = time_as_int(time)
        except:
            print("auto_command (", time, days, command, "): error time format. (HH:MM:SS)")
            continue

        if days == "weekdays":
            days_ = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        elif days == "weekend":
            days_ = ['Sun', 'Sat']
        elif days == "everyday":
            days_ = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        elif not isinstance(days, (list, tuple)):
            days_ = [days]
        else:
            days_ = days

        known = False
        for key in commands:
            known = known or commands[key] == command
        for paper_command in paper_command_list:
            known = known or paper_command == command
        if not known:
            print("auto_command '" + command + "' not in the list of known commands")
            continue
        cleaned_commands.append((time_, days_, command))
    return cleaned_commands


auto_commands = []
if "auto_commands" in config.__dict__:
    try:
        auto_commands = read_auto_commands(config.auto_commands)
    except:
        print("auto_commands format invalid")


def handle_command(commandline, slack):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    command = commandline.split()[0]
    args = " ".join(commandline.split()[1:])

    for paper_command in paper_command_list:
        if command == paper_command:
            readlist, error_msg = paper_command(args)
            if error_msg:
                slack.post(error_msg)
            else:
                for site, arguments in readlist:
                    if site == "arxiv":
                        print_arxiv_paper(slack, *arguments)
            return

    if command == commands['ADD_KW_COMMAND']:
        keywords = list(np.load('keywords.npy'))
        kw = args
        iM = kw.find('xx')
        while (iM != -1):
            kw = kw[:iM] + kw[iM + 2].upper() + kw[iM + 3:]
            iM = kw.find('xx')

        if kw in keywords:
            slack.post('_'+kw+'_ was already part of keywords')
        else:
            keywords.append(kw)
            slack.post('_'+kw+'_ added to keywords')
        np.save('keywords.npy',np.array(keywords, dtype=str))

    elif command == commands['REMOVE_KW_COMMAND']:
        keywords = np.load('keywords.npy')
        # mayus conversion
        kw = args
        iM = kw.find('xx')
        while (iM != -1):
            kw = kw[:iM] + kw[iM + 2].upper() + kw[iM + 3:]
            iM = kw.find('xx')
        keywords = np.delete(keywords, np.where(keywords == kw))
        np.save('keywords.npy', keywords)
        slack.post('_'+kw+'_ removed from keywords')

    elif command == commands['PRINT_KW_COMMAND']:
        response = list(np.load('keywords.npy'))
        slack.post('_keywords_ *list*:')
        string_to_post = '\n'.join(response)
        slack.post(string_to_post)

    elif command == commands['ADD_AUTHOR_COMMAND']:
        keywords = list(np.load('keywords_authors.npy'))
        kw = args
        iM = kw.find('xx')
        while (iM != -1):
            kw = kw[:iM] + kw[iM + 2].upper() + kw[iM + 3:]
            iM = kw.find('xx')

        if kw in keywords:
            slack.post('_'+kw+'_ was already part of keywords')
        else:
            keywords.append(kw)
            slack.post('_'+kw+'_ added to keywords')

        np.save('keywords_authors.npy', np.sort(np.array(keywords, dtype=str)))

    elif command == commands['REMOVE_AUTHOR_COMMAND']:
        keywords = np.load('keywords_authors.npy')
        # mayus conversion
        kw = args
        iM = kw.find('xx')
        while (iM != -1):
            kw = kw[:iM] + kw[iM + 2].upper() + kw[iM + 3:]
            iM = kw.find('xx')
        keywords = np.delete(keywords, np.where(keywords == kw))
        np.save('keywords_authors.npy', keywords)
        slack.post('_'+kw+'_ removed from keywords')

    elif command == commands['PRINT_AUTHOR_COMMAND']:
        response = list(np.load('keywords_authors.npy'))
        slack.post('_author_ *list*:')
        string_to_post = '\n'.join(response)
        slack.post(string_to_post)

    elif command == commands['BUILD_AUTHOR_LIST']:
        authors = np.load('keywords_authors.npy')
        Ninitial = len(authors)
        year, kw, threshold = args.replace("[","]").split("]")
        threshold = int(threshold)
        kw = kw.split(",")
        slack.post("Searching for authors, could take some time.")
        new_authors = get_author_list_arxiv(year, kw, arxiv_sections)
        new_authors = [(key) for key, N in Counter(new_authors).items()
                             if N >= threshold]
        authors = list(authors) + new_authors
        authors = [key for key in Counter(authors)]
        authors = np.sort(np.array(authors, dtype=str))
        Nfinal = len(authors)
        np.save('keywords_authors.npy', authors)
        slack.post("Author who published at least "+ str(threshold) + " in " +
                   str(year) + ": " + ", ".join(new_authors))
        slack.post("Added " + str(Nfinal - Ninitial) + " new author to the list.")

    elif command == commands['ADD_PKW_COMMAND']:
        keywords = np.load('prefered_keywords.npy')
        args = args.split(",")
        if len(args) == 3:
            pass
        elif len(args) == 2:
            args.append(args[1])
        else:
            slack.post('adding prefered keywords: ' + command + ' keyword,  before,  after')
            return

        kw = args[0]
        iM = kw.find('xx')
        while (iM != -1):
            kw = kw[:iM] + kw[iM + 2].upper() + kw[iM + 3:]
            iM = kw.find('xx')

        if kw in keywords[:,1]:
            i = np.where(keywords[:,1] == kw)
            keywords[i,0] = args[1].strip() + " "
            keywords[i,2] = " " + args[2].strip()
            slack.post('updating prefered keywords: _' + kw + '_')
        else:
            keywords = np.append(keywords, [[args[1], kw, args[2]]], axis=0)
            slack.post('_'+kw+'_ added to prefered keywords')
        np.save('prefered_keywords.npy', np.array(keywords, dtype=str))

    elif command == commands['REMOVE_PKW_COMMAND']:
        keywords = np.load('prefered_keywords.npy')
        # mayus conversion
        kw = args.strip()
        iM = kw.find('xx')
        while (iM != -1):
            kw = kw[:iM] + kw[iM + 2].upper() + kw[iM + 3:]
            iM = kw.find('xx')
        keywords = np.delete(keywords, np.where(keywords[:,1] == kw), axis=0)
        np.save('prefered_keywords.npy', keywords)
        slack.post('_'+kw+'_ removed from prefered keywords')

    elif command == commands['PRINT_PKW_COMMAND']:
        prefered_keywords = np.load('prefered_keywords.npy')
        slack.post('_prefered_ _keywords_ *list*:')
        string_to_post = "\n".join([" ".join(kw) for kw in prefered_keywords])
        slack.post(string_to_post)

    elif command == commands['HELP_COMMAND']:
        response = []
        for paper_command in paper_command_list:
            response += [paper_command.help()]
        response += ["For all paper fetching, you can add the following args:",
                     "'sections=[section1, section2]' : arxiv section where to "
                     "look for paper",
                     "'span=N': number of days from todays, "
                     "can be _week_ or _month_ ",
                     "or 'begin=YYYY-MM-DD', 'end=YYYY-MM-DD': span as dates",
                     "kw=[_keyword_, _keyword_]: keyword for the search if"
                     " not using the list",
                     "author=[_author_, _author_]: author for the search if"
                     " not using the list"]
        response += ["*" +
                     commands['ADD_KW_COMMAND'] + "* _keyword_ | *" +
                     commands['REMOVE_KW_COMMAND'] + "* _keyword_ | *" +
                     commands['PRINT_KW_COMMAND'] + "*: "
                     "add _keyword_ to | remove _keyword_ from | "
                     "print keywords list"]
        response += ["*" +
                     commands['ADD_AUTHOR_COMMAND'] + "* _author_ | *" +
                     commands['REMOVE_AUTHOR_COMMAND'] + "* _author_ | *" +
                     commands['PRINT_AUTHOR_COMMAND'] + "*: "
                     "add _author_ to | remove _author_ from | "
                     "print author list"]
        response += ["*" +
                     commands['ADD_PKW_COMMAND'] + "* _keyword_ _highlight_"
                     " _highlight_| *" +
                     commands['REMOVE_PKW_COMMAND'] + "* _keyword_ | *" +
                     commands['PRINT_PKW_COMMAND'] + "*: "
                     "add _keyword_ to | remove _keyword_ from | print"
                     " prefered keywords list"]
        response += ["*" + commands['BUILD_AUTHOR_LIST'] + \
                     "* _year_ [_keyword_, _keyword_] _threshold_: "
                     "search for author who published at least _threshold_"
                     " paper containing one of the _keyword_ in during the"
                     " _year_ and add them to the author list"]
        response += ["For uppercase use 'xx' before the corresponding "
                     "character. Ex: xxdevoret -> Devoret, "
                     "xxdixxcarlo -> DiCarlo."]
        slack.post('_bot_ commands')
        for rep in response:
            slack.post(rep)

    elif command == "test":
        print(args)
        slack.post(args)

    else:
        response = "Not sure what you mean. Please use *" + commands['HELP_COMMAND'] + \
                   "* to see the 'help' menu"
        slack.post(response)


def parse_bot_commands(bot_id, slack_events):
    """
        Parses a list of events coming from the Slack RTM API to
        find bot commands. If a bot command is found, this function
        returns a tuple of command and channel.
        If its not found, then this function returns None, None.
        From the tutorial:
        https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == bot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning)
        in message text and returns the user ID which was mentioned.
        If there is no direct mention, returns None
        From the tutorial:
        https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

class slackChannel:
    def __init__(self, slack_client, channel):
        self.slack_client = slack_client
        self.channel = channel

    def post(self, text):
        self.slack_client.api_call("chat.postMessage", channel=self.channel,
                                   text=text, as_user=True)


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    # instantiate Slack & Twilio clients
    slack_client = SlackClient(SLACK_BOT_TOKEN)

    if slack_client.rtm_connect(auto_reconnect=True):
        print("paperbot connected and running!")
        bot_id = slack_client.api_call("auth.test")["user_id"]
        prev2num = time_as_int(time.strftime("%H-%M-%S"))-1
        # read commands
        while True:
            try:
                command, channel = parse_bot_commands(bot_id,
                                                      slack_client.rtm_read())
                if command and channel:
                    post_destination = slackChannel(slack_client, channel)
                    handle_command(command, post_destination)
                    print(channel)
                now2num  = time_as_int(time.strftime("%H-%M-%S"))
                today_char = datetime.now().strftime('%a')
                for run_time, days, command in auto_commands:
                    if (prev2num-run_time) < 0  and (now2num-run_time) >= 0:
                        if today_char in days and BOT_CHANNEL:
                            handle_command(command, BOT_CHANNEL)
                prev2num = now2num
                time.sleep(READ_WEBSOCKET_DELAY)
            except WebSocketConnectionClosedException:
                print("Lost connection to Slack. Reconnecting...")
                if not slack_client.rtm_connect(auto_reconnect=True):
                    print("Failed to reconnect to Slack")
                    time.sleep(0.5)
                else:
                    print("Reconnected to Slack")
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
