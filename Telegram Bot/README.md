## Hello World!

This is an implementation of Telegram Bot, designed for
registration of students for a Speaking club event, that is held at
my current work place, Wake Up English school.
  
# Version 1.0
Bot can sign up and sign out a user for the event.  
```Python + Telebot used```
  
  
# Version 2.0
Massive update:
- bot now works asynchronously
- implemented subscription for users (SQL db). Now users can subscribe for
updates about the event and get notifications from the bot with a suggestion to subscribe
- bot parses last post about the event from VK group (using VK api) and send it to users
- if maximum event capacity has reached, bot suggests to a user to sign up in a waiting list.
If some user refuses to join and signs out, bot sends suggestion to join to a first user in waiting list
- if minimal event capacity hasn't reached, bot sends message to an event manager with an option to
cancel the event. If manager approves, bot sends notifications to all signed up users about an event cancellation
- bot sends info to the event manager about the number of participants every 6 hours  
- 
```Python + aiogram, asyncio, aioschedule, sqlite3, VK api used```
