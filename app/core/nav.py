'''
app/core/nav.py

This file exists to map navigation endpoints to UI state.
'''

NAV_MAP = {
    "main.index": "home",
    "main.about": "about",
    "main.contact": "contact",
    "help.help_index": "help",
    "user.profile": "user",
    "admin.dashboard": "admin",
    "call.call": "call",
    "user.dashboard": "dashboard",
}

# apparently you define constant variables using capslock in python. don't like this coming from c and c++
# delete later