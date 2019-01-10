# paperbot

A Slack bot for personalized, filtered and trackable arXiv output.

## Installation:

- To start, [web sign in](https://slack.com) to your user account corresponding to the Slack workspace where you would like to install paperbot.
- Create a [new Slack App](https://api.slack.com/apps?new_app=1). In the pop-up window, set 'paperbot' as **App Name** and choose your **Development Slack Workspace**. 
- Choose **paperbot** in the [Apps page](https://api.slack.com/apps/), and click on **Bot Users** from the menu at the left below "Features". Now select **Add a Bot User** and choose the bot's **Display name**. Finally click on **Add Bot User** and **Save Changes**.
- In the current window, choose **Install App** from the menu at the left below "Settings". Click on **Install App to Workspace** and **Authorize**. Copy the **Bot User OAuth Access Token** and save it somewhere to use later. 
- Open the web-based [Slack App](https://slack.com) corresponding to your workspace and create a new channel. Invite `paperbot` to this channel as if you were inviting another workspace user to it. If you now click on the address bar of your web browser, you will note that it looks like this: https://yourworkspace.slack.com/messages/CHANNEL_ID/something_else. Copy the **CHANNEL_ID** variable and save it somewhere to use later.
- Install slackclient by executing `pip install slackclient` on a terminal.
- Clone the paperbot GitHub repository to your machine. 
- Do `cd` to the `paperbot` folder in the cloned repository, open `config.py` and change the variables `SLACK_BOT_TOKEN` and `CHANNEL_ID` by the previously saved **Bot User OAuth Access Token** and **CHANNEL_ID**, respectively.
- Done! Execute the bot by doing `python paperbot.py` or, in the background, by doing `nohup python paperbot.py > custom-out.log &`.
- Note that you can also command paperbot by private messages. You will find the app in the 'Apps' menu bellow the 'Direct Messages' menu of your Slack Desktop application.

## Customization:

**Automatic daily posts**

In `config.py`, choose the time of the automatic posts by modifying the variable `auto_commands`. By default, the command "todays" is executed every weekday at 08:30 AM (local time), and the command "home" can be configured to print at some other time. We recommend to delete the example line `("13:30:00", ['Mon', 'Wed', 'Fri'], "home")`.

**Choose the default arXiv sections to monitor**

In `config.py`, change the variable `arxiv_sections=[quant-ph, cond-mat]` to include the arXiv sections you want to monitor. 

**Define your favourite authors to be hightlighted**

`parperbot` stores the names of your favourite authors. If a new arXiv preprint includes one or more of such names, `paperbot` will post it highlighting the message with symbols that you can choose. For instance, executing on Slack the command "@paperbot add_special michel devoret, :tada:, :tada:" stores 'Michel Devoret' as favourite author. Note that `paperbot` performs a case-insensitive search. Next time that a preprint is submitted with him as an author, it will be posted and highlighted with :tada:. 

**Build the keywords and authors list**

`paperbot` stores keywords that are used to identify interesting preprints. The keywords list can be build manually by executing the command "@paperbot add some_keyword" on Slack. This adds some_keyword to your keywords list, which can be printed executing "@paperbot list" on Slack.

`paperbot` also includes an authors list which can be built manually. This is done by executing the command "@paperbot add_author some_author" on Slack. Executing "@paperbot authors" on Slack prints the authors list. 

Importantly, `paperbot` provides a method to generate the author list automatically. This is a **key** step to build a powerful preprint filter. It requires the definition of a few root keywords, such as 'superconducting qubit', 'quantum optics', and 'quantum information'. Executing the command "@paperbot build _2018_ ['superconducting qubit', 'quantum optics', 'quantum information'] threshold" on Slack, `paperbot` searchs day-by-day over all arXiv papers submitted in _2018_, and saves the name of the authors that have at least a _threshold_ number of papers including any of the root keywords in its title or abstract. The result of further executions of the `build` command is always appended to the author list. In particular, running `build` every new year keeps the author list up-to-date.

## Usage:

You can call  using "@paperbot paper" so that it print todays' arxiv
papers. The full call is

@paperbot paper sections=[quant-ph, cond-mat] keywords=[qubit, superconductor]
author=[A. Blais, Michel Devoret] span=1
span is the number of days from today to fetch papers.
You can also set the span as dates: begin=YYYY-MM-DD end=YYYY-MM-DD.

When not specificly given, keywords and authors are taken from internal keywords lists.
You can see and add elements to those lists with: "add","list","add_author","authors".

You can ask the bot to highlight some paper by adding the related keywords
in the prefered keywords list:
"@paperbot add_special me, \:tada:, \:tada:"

In config.py, you can set shortcut for prefered options, change the calls
and set commands to be at set times.

**Help**
Execute "@paperbot help" on Slack to access to more `paperbot` commands and details. 

by [TheSQuaD team](https://www.physique.usherbrooke.ca/blais/index.php?sec=accueil&lan=EN) (Theory of Superconducting Quantum Devices).
