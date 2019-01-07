# paperbot
A Slack bot for personalized, filtered and trackable arXiv output.


## Installation:
- Get the tokens from slack (Agustin?)
- Add the token to config.py and set your preference.
- Call paperbot.py, you can have it run in the backgroud by calling:
  "nohup python paperbot.py > custom-out.log &"

## Usage:
You can call the bot using "@paperbot paper" so that it print todays' arxiv
papers. The full call is

@paperbot paper sections=[quant-ph, cond-mat] keywords=[qubit, superconductor]
author=[A. Blais, Agustin] span=1
span is the number of days from today to fetch papers.
You can also set the span as dates: begin=YYYY-MM-DD end=YYYY-MM-DD.

When not specificly given, keywords and authors are taken from internal keywords lists.
You can see and add elements to those lists with: "add","list","add_author","authors".

You can ask the bot to highlight some paper by adding the related keywords
in the prefered keywords list:
"@paperbot add_special me, \:tada:, \:tada:"

In config.py, you can set shortcut for prefered options, change the calls
and set commands to be at set times.

We only tested it on linux.

by TheSQuaD team (Theory of Superconducting Quantum Devices)
