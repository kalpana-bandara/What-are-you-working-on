# What-are-you-working-on
A simple desktop app which runs in background and shows a popup up every interval (hour, minute) asking to enter "What are you working on ?". You will be able to see all the work logs at the end of the day and manually enter the entries to your time logging app. No more memorizing.

# How to run the app

Note : Python should be installed on your computer -  https://www.python.org/downloads/

1. Clone this repository.
2. Open the app folder and run "pip install -r requirements.txt".
3. Run worker.pyw.
4. The app will open and run in the background (it will shown in system tray icon)

Note : Your work logs will be saved to "work_log" file inside the app folder.

# How to change the popup interval

1. Open worker.pyw with notepad or code editor.
2. Edit line number 18 - INTERVAL_MINUTES = your_prefered_interval_in_minutes and save

# How to change Start time and End time (The popup will trigger starting at the configured start time.)

1. Open worker.pyw with notepad or code editor.
2. Edit line number 16 and 17.

# App Screenshot

![work tracker](https://iili.io/KTEHbSI.png?raw=true "work tracker")


