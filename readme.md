# UpdateCheckerBot
This program has been written to serve as a way to automatically check if a ARMA 3 steam workshop item has been updated
## How to setup
1. Clone the repository
2. Create a config folder on the same level as bot.py
3. Create a preset folder inside of config with your desired presets(these can be made in the arma 3 launcher)
4. Create a secrets.json inside of config in here you will need the following data
    1. token: your discord bot token
    2. databaseURL: your database url. This program has been written for firebase
    3. steamAPIKey: your steam web api key
5. Create a updateCheckerToken, this token has your firebase database key inside