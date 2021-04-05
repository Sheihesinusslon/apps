# Hello World!

This is an implementation of a Telegram Bot, designed for a
registration of students for a Speaking club event, that is held at
my current work place, Wake Up English school.
  
### Version 1.0
The bot can sign up and sign out a user for the event.  
```Python + Telebot used```
  
  
### Version 2.0
Massive update:
- the bot now works asynchronously
- implemented a subscription for users (SQL db). Now users can subscribe for
updates about the event and get notifications from the bot with a suggestion to sign up for the event
- the bot parses the last post about the event from a VK group (using VK api) and sends it to users
- if maximum event capacity is reached, the bot suggests to a new user to add them in a waiting list.
If some users refuse to join and sign out, the bot sends a suggestion to join to a first user in a waiting list
- if minimal event capacity hasn't been reached on the event day, the bot sends a message to an event manager with an option to
cancel the event. If the manager approves, the bot sends notifications to all signed up users about an event cancellation
- the bot sends info to the event manager about the number of participants every 6 hours and clears all lists the next day after the event  
```Python + aiogram, asyncio, aioschedule, sqlite3, VK api used```  
  
<img src="https://user-images.githubusercontent.com/75010755/113416761-a40e2780-93ca-11eb-8b43-b04693928fa2.jpg" width="240" height="420"> <img src="https://user-images.githubusercontent.com/75010755/113416759-a2dcfa80-93ca-11eb-8cdc-1922c358b3aa.jpg" width="240" height="420"> <img src="https://user-images.githubusercontent.com/75010755/113416739-9ce71980-93ca-11eb-878f-d18936a4e728.jpg" width="240" height="420">   
  
<img src="https://user-images.githubusercontent.com/75010755/113416757-a2446400-93ca-11eb-89d2-2b7c45809af9.jpg" width="240" height="420"> <img src="https://user-images.githubusercontent.com/75010755/113417344-dd936280-93cb-11eb-8a51-e1f3bfc17d16.jpg" width="240" height="420"> <img src="https://user-images.githubusercontent.com/75010755/113416760-a3759100-93ca-11eb-8fd8-028d66184256.jpg" width="240" height="420">
