---
title: "Automating my Outlook calendars"
date: 2022-12-01T12:00:00Z
draft: false
featured: false
image: "images/cover.jpg"
tags: 
    - python
    - tutorials
    - automations
authors:
    - samuel
---
Making my life easier by creating a simple python script to generate Outlook meetings from an Excel spreadsheet.

<!--more-->

*This is something I've done for myself for work on my own time, hence why some parts are vague/blurred!*

## Backstory
A new project started at work, and we needed to make a schedule between two people.
There is 1 to 5 tasks of 10 min that needs to be scheduled each day.

The scheduling is done on an Excel spreadsheet because it's just easier for now. The spreadsheet looks a bit like this:
![enter image description here.](images/dl_EXCEL_2022_11_18_14-58-09_25dyEwwxSR.png)

This works, but it's a bit outdated and since, for the start of the project, I must be present to monitor some things on pretty much each one I wanted something else than a spreadsheet.
Moreover, the spreadsheet is updated frequently which is a pain if you want to set up events in a calendar

At work, we use outlook, outlook has, of course, calendars and a pretty good add-on system and an API.
The idea would be to parse the Excel file and generate meetings in a separate calendar so that I could get notifications and see easier when the next task is happening.

## Feasibility
First thing is I do is to check if it's even possible:

For Excel, it's pretty simple, python has a very cool module named `openpyxl` which can read XLSX files.

Outlook was a bit different. It has a pretty good add-ons system and an API you can call from windows, but as always with Microsoft, the docs sucks and are hard to find. Fortunately, simply googling `Outlook meeting python` yields multiple stack overflow question about this and have some code samples, cool!

## Let's start coding

First thing I need to say is that this a script that live on my desktop and is not intended to be run automatically nor to be distributed to other people. So code quality went out of the window for this one 😅

### Excel file:
```
>>> import openpyxl
>>> workbook = openpyxl.load_workbook("4BOE9 EEG StudyG1 Schedule Online Shared_Biotrial_15NOV2022_sentABL&LAD.xlsx")
>>> sheet = workbook.active
>>> header = [cell.value for cell in sheet['A1:G1'][0]]
>>> header
['Date', 'Group', 'Visit', 'Time', 'Time Slot', 'Contractor 1', 'Contractor 2']
```
Perfect, I have the header, now let's get the values

```
>>> events = []
>>> row = 2
>>> while True:
...     values = [cell.value for cell in sheet[f'A{row}:G{row}'][0]]
...     values_dict = {}
...     for i in range(len(header)):
...         values_dict[header[i]] = values[i]
...     if values_dict["Date"] == None:
...         break
...     events.append(values_dict)
...     row += 1
...
>>> for e in event: 
...     print(e)
{'Date': datetime.datetime(2022, 11, 2, 0, 0), 'Group': '1', 'Visit': '1', 'Time': datetime.time(7, 15), 'Time Slot': '07:05-08:35', 'Contractor 1': 'x', 'Contractor 2': None}
{'Date': datetime.datetime(2022, 11, 2, 0, 0), 'Group': '1', 'Visit': '1', 'Time': datetime.time(8, 15), 'Time Slot': None, 'Contractor 1': 'x', 'Contractor 2': None}
{'Date': datetime.datetime(2022, 11, 3, 0, 0), 'Group': '1', 'Visit': '2', 'Time': datetime.time(7, 15), 'Time Slot': '07:05-08:35', 'Contractor 1': 'x', 'Contractor 2': None}
{'Date': datetime.datetime(2022, 11, 3, 0, 0), 'Group': '1', 'Visit': '2', 'Time': datetime.time(8, 15), 'Time Slot': None, 'Contractor 1': 'x', 'Contractor 2': None}
{'Date': datetime.datetime(2022, 11, 4, 0, 0), 'Group': '1', 'Visit': '3', 'Time': datetime.time(7, 15), 'Time Slot': '07:05-08:35', 'Contractor 1': 'x', 'Contractor 2': None}
<more lines>
```
Not the best code but it works, I now have a list of events to add to my Outlook calendar. I can check the `'x'` in the contractor values to see which one it is.

### Outlook

I want my meetings to be scheduled 15 min before the task and continue for 15 min after the task.

Let's start by declaring a few things (links at the end):
```py
import win32com.client
from datetime import timedelta, datetime
import pytz

OUTLOOK_MEETINGSTATUS_MEETING = 1
OUTLOOK_MEETINGSTATUS_CANCELED = 5
OUTLOOK_MEETINGSTATUS_RECEIVED = 3
OUTLOOK_MEETINGSTATUS_RECEIVEDANDCANCELED = 7
OUTLOOK_MEETINGSTATUS_NONMEETING = 0

OUTLOOK_BUSYSTATUS_BUSY = 2
OUTLOOK_BUSYSTATUS_FREE = 0
OUTLOOK_BUSYSTATUS_OOO = 3
OUTLOOK_BUSYSTATUS_TENATIVE = 1
OUTLOOK_BUSYSTATUS_REMOTE = 4

outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')
calendar_folder = outlook.Folders('<my_work_email_here|').Folders('Calendrier').Folders('Calendar for the events')

start_meeting_x_before = 15
meeting_duration = start_meeting_x_before + 10 + 15
```
Outlook is localized, so `Calendrier` means `Calendars` in English and will differ depending on the language, that was fun to find out 🤡.

As I want to be able to run this script without generating duplicates, the first thing to do is to clear all future events:
```py
for i in range(10):
    for item in calendar_folder.Items:
        if item.MeetingStatus != OUTLOOK_MEETINGSTATUS_NONMEETING:
            continue
        if item.Start < datetime.now().replace(tzinfo=pytz.UTC):
            continue
        item.Delete()
```
Outlook is a bit flaky, so I repeat the process a few times. Basically, I delete the meeting if it's in the future and does not have any participants.

I then make a list of all meeting that might still be there (because I manually added a participant for example) as I don't want to re-schedule it :
```py
already_existing = [item.Start.strftime('%d/%m/%Y %H:%M') for item in calendar_folder.Items]
```

Then it's just a matter of looping throughout the event array, checking that the event is in the future, checking that it doesn't already exist and creating it
```py
for event in events:`
    scheduled_start_time = event["Date"] + timedelta(hours=event["Time"].hour, minutes=event["Time"].minute)
    meeting_start_time = scheduled_start_time - timedelta(minutes=start_meeting_x_before)
    meeting_start_time = meeting_start_time.strftime('%d/%m/%Y %H:%M')
        
    if schedule_start_time < datetime.now():
        continue
            
    if meeting_start_time in already_existing:
        print("Already existing")
        continue
            
    print(meeting_start_time, event)
        
    who = "UNKNOWN"
    if event["Contractor 1"] == "x":
        who = "Alice"
    if event["Contractor 2"] == "x":
        who = "Bob"
        
    meeting = calendar_folder.Items.Add()
    meeting.MeetingStatus = OUTLOOK_MEETINGSTATUS_NONMEETING
    meeting.Start = meeting_start_time
    meeting.Duration = meeting_duration
    meeting.Subject = f"{who} - {event['Group']} {event['Visit']}"
    meeting.ResponseRequested = False
    meeting.BusyStatus = OUTLOOK_BUSYSTATUS_FREE
    meeting.ReminderSet = False
    meeting.Save()
```

As this is a shared calendar, I wanted to avoid annoying other people by deleting all event and re-creating them. So by default, the events don't have a reminder and are having the Non-Event status, meaning that there are not any participants/organizer.
I also didn't want to be marked as "Busy" in teams for each meeting, so by default it marks me as free
I can manually set these settings if there is a task that I need to monitor.
This make a very nice and organized calendar that I don't have to modify manually:
![enter image description here.](images/dl_OUTLOOK_2022_11_18_15-35-26_4JaqJoyvbG.png)

## Resources & Conclusion
Including the time I spent trying to locate a proper documentation for creating the events, I spent maybe two hours on this script. Which isn't that bad considering that it took me 45 min last time I did this manually (which was a week ago)

If you want to do something similar, here are the main things I needed:
- Appointment Item doc: https://learn.microsoft.com/en-gb/office/vba/api/outlook.appointmentitem
- https://stackoverflow.com/questions/38899956/python-win32com-get-outlook-event-appointment-meeting-response-status
- https://rmsol.de/2018/06/17/Emails-and-Appointments-with-Outlook-and-Python/
- `outlook.PickFolder()` To figure out why the `Calendars` folder was not found

All in all, pretty good. 
One amelioration would be to auto create Teams meetings or even auto-detect a change in the meeting and, instead of deleting it, modifying the time.
I might also do something similar to filter my emails with sieve scripts or similar because the outlook filters are rubbish.
