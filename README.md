# paperbot
A Slack bot for personalized, filtered and trackable arXiv output.

## Installation:
- Get admin/owner permissions of the Slack workspace where you want to install paperbot. 
- Create a new Slack App [here](https://api.slack.com/apps?new_app=1). In the pop-up window, set 'paperbot' as **App Name** and choose your **Development Slack Workspace**. 
- Choose **paperbot** [here](https://api.slack.com/apps/), and click on **Bot Users** from the menu at the left below "Features". Now select **Add a Bot User** and choose the bot's **Display name**. Finally click on **Add Bot User** and **Save Changes**.
- In the same webpage, now choose **Install App** from the menu at the left below "Settings". Then click on **Install App to Workspace** and **Authorize**. Copy the **Bot User OAuth Access Token** and save it somewhere to use later. 
- Open the web-based [Slack app](https://slack.com) corresponding to your workspace and create a new channel. The name of this channel could be `paperbot` or something else. Click on the new channel and copy the address from the address bar of your web browser. It will look something like this: https://yourworkspace.slack.com/messages/**CHANNEL_ID**/team/TEAM_ID/. Copy the **CHANNEL_ID** variable and save somewhere it to use later.
- Install slackclient by executing `pip install slackclient` on a terminal.
- Now clone the `paperbot` repository on your machine. 
- In the `paperbot` folder, open config.py and change the variables `SLACK_BOT_TOKEN` and `CHANNEL_ID` by your previously saved **Bot User OAuth Access Token** and **CHANNEL_ID**, respectively.
- You're done! Invite paperbot to the recently created Slack channel and execute the bot by doing "python paperbot.py", or in the background by doing "nohup python paperbot.py > custom-out.log &"
- Note that you can also command `paperbot` independently by using private messages.  

## Customization:

**Automatic posts**
In `config.py`, choose the time of the automatic posts by modifying the variable `auto_commands`.

**Choose the default arXiv sections to look at**
In `config.py`, change the variable arxiv_sections=[quant-ph, cond-mat] for the ones you want to monitor.

**Build the authors and keywords list**
Pick few root keywords such as 'superconducting qubits' and 'quantum optics'.

**Hightlight your favourite authors**

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

by [TheSQuaD team](https://www.physique.usherbrooke.ca/blais/index.php?sec=accueil&lan=EN) (Theory of Superconducting Quantum Devices).
