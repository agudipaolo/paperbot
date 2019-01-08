import os
# bot user oauth access token
SLACK_BOT_TOKEN = 'xoxb-012345678901-NNNNNNNNNNNNNNNNNNNNNNNN'
#SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

# Slack token for the channel in which the bot write auto commands
BOT_CHANNEL = 'NNNNNNNNN'

# arxiv section from which paper are taken
arxiv_sections = ['quant-ph', 'cond-mat']
#Choose from:
#   'astro-ph', 'cond-mat', 'gr-qc', 'hep-ex', 'hep-lat', 'hep-ph', 'hep-th',
#   'math-ph', 'nlin', 'nucl-ex', 'nucl-th', 'physics', 'quant-ph',
#   'math', 'CoRR', 'q-bio', 'q-fin', 'stat', 'eess', 'econ'


# custom name of the commands call
# Call with "@BOT_ID command"
commands = {
    "HELP_COMMAND":"help",
    #look for papers
    "PAPER_COMMAND":"paper",
    # add/remove/check keywords
    "ADD_KW_COMMAND":"add",
    "REMOVE_KW_COMMAND":"rm",
    "PRINT_KW_COMMAND":"list",
    # add/remove/check author
    "ADD_AUTHOR_COMMAND":"add_author",
    "REMOVE_AUTHOR_COMMAND":"rm_author",
    "PRINT_AUTHOR_COMMAND":"authors",
    # add/remove/check keywords used for special mention
    "ADD_PKW_COMMAND":"add_special",
    "REMOVE_PKW_COMMAND":"rm_special",
    "PRINT_PKW_COMMAND":"special",
    # Add author who published about a subject in a designed year
    "BUILD_AUTHOR_LIST":"build"}

# list of custom commands:
# tuple (name, dict of options)
# name : one words, minuscule.
# available option:
#    "span": number of days, or 'week', or 'month', default=1
#    "kw": list of keywords to look for,
#          default=kw in the keywords list
#    "authors": list of sections from arxiv
#               default=authors in the authors list
#    "sections": list of sections from arxiv from which to import papers
#                default=sections set in the 'arxiv_sections' variable
paper_commands = [
    ("todays", {}),
    ("weekly", {"span":"week"}),
    ("monthly", {"span":"month"}),
    ("home", {"span":31, "authors":["Me", "You"]}),
    ("ai", {"sections":['physics'], "kw":['machine learning', 'neural netwok'] })
]

# list of command to be called at set time
# tuple of time, days, command
# time format: HH:MM:SS
# days: one of "weekdays", "weekend", "everyday" or a list of specific days from
#       ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
auto_commands = [("08:30:00", "weekdays", "todays"),
                 ("13:30:00", ['Mon', 'Wed', 'Fri'], "home")]
