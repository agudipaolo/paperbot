# paperbot
A Slack bot for personalized, filtered and trackable arXiv output.

## Installation:
- Web sign in to your slack workspace and user [Slack app](https://slack.com).
- Create a new Slack App [here](https://api.slack.com/apps?new_app=1). In the pop-up window, set 'paperbot' as **App Name** and choose your **Development Slack Workspace**. 
- Choose **paperbot** [here](https://api.slack.com/apps/), and click on **Bot Users** from the menu at the left below "Features". Now select **Add a Bot User** and choose the bot's **Display name**. Finally click on **Add Bot User** and **Save Changes**.
- In the same webpage, now choose **Install App** from the menu at the left below "Settings". Then click on **Install App to Workspace** and **Authorize**. Copy the **Bot User OAuth Access Token** and save it somewhere to use later. 
- Open the web-based [Slack app](https://slack.com) corresponding to your workspace and create a new channel. The name of this channel could be `arxivbot` or something else. Now invite `paperbot` to this channel, as if you were inviting a workspace user. Note that the address bar of your web browser looks like this: https://yourworkspace.slack.com/messages/CHANNEL_ID/something_else. Copy the **CHANNEL_ID** variable and save somewhere it to use later.
- Install slackclient by executing `pip install slackclient` on a terminal.
- Now clone the `paperbot` GitHub repository to your machine. 
- In the `paperbot` folder, open `config.py` and change the variables `SLACK_BOT_TOKEN` and `CHANNEL_ID` by your previously saved **Bot User OAuth Access Token** and **CHANNEL_ID**, respectively.
- Done! Execute the bot by doing "python paperbot.py", or in the background by doing "nohup python paperbot.py > custom-out.log &".
- Note that you can also command `paperbot` by private messages. You will find the app in the Apps menu bellow the Direct Messages menu of your Slack Desktop application.

## Customization:

**Automatic daily posts**

In `config.py`, choose the time of the automatic posts by modifying the variable `auto_commands`. By default, the command "todays" is executed every weekday at 08:30 AM (local time), and the command "home" can be configured to print at some other time. We recommend to delete the example line `("13:30:00", ['Mon', 'Wed', 'Fri'], "home")`.

**Choose the default arXiv sections to look at**

In `config.py`, change the variable `arxiv_sections=[quant-ph, cond-mat]` to include the arXiv sections you want to monitor. 

**Define your favourite authors to be hightlighted**

`parperbot` stores the names of your favourite authors. If a new paper includes one or more of such names, the corresponding post message will be highlighted with symbols that you can choose. For instance, executing on Slack the command "@paperbot add_special alexandre blais, :tada:, :tada:" saves Alexandre Blais as favourite author. Next time that a paper is published with him as an author, it will be highlighted with :tada:. 

**Build the keywords and authors list**

`paperbot` also stores keywords that are used to identify interesting papers. The keywords list can be build manually, by executing on Slack the command "@paperbot add some_keyword". This will add some_keyword to the list of all your keywords. To print your stored keywords execute "@paperbot list" on Slack.

An authors list can also be built manually, by executing on Slack the command "@paperbot add_author some_author". To print the stored authors execute "@paperbot authors" on Slack. 

Importantly, `paperbot` provides a method to generate the author list automatically. This is a **key** step to build a powerful paper filter. It requires the definition of a few root keywords, such as 'superconducting qubit', 'quantum optics', and 'quantum information'. Executing on Slack the command "@paperbot build _2018_ ['superconducting qubit', 'quantum optics', 'quantum information'] threshold", `paperbot` will search day-by-day over all arXiv papers submitted in _2018_, and save the name of the authors that have at least a _threshold_ number of papers including any of the root keywords in its title or abstract. The result of further executions of the `build` command, for instance sweeping the _2018_ (year) parameter, is appended to the local author list. In particular, running `build` every new year keeps the author list up-to-date.

Note that `paperbot` performs a case-insensitive search.

## Usage:
You can call the bot using "@paperbot paper" so that it print todays' arxiv
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
