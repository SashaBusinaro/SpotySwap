# SpotySwap

##### A light weight Python script to transfer Spotify library tracks from one account to another using the Spotify Web API

## Requirements

```bash
pip install spotipy
```

## Quick Start
**Before running the script**, it is necessary to obtain the API credentials of both Spotify accounts (source and target).
To do this you need to go to Spotify's Developer Dashboard via this [link](https://developer.spotify.com/dashboard/login). 
Once logged in, create a new app and save the Client ID and CLIENT SECRET. 
Then click on EDIT SETTINGS and add `http://localhost:8000` as Redirect URIs and press Save.

**Repeat this procedure with both accounts.**

**Make sure to log out** of your [Spotify account](https://open.spotify.com) from the default browser.

Now enter the credentials obtained in the previous step into the section of the `main.py` file:

    SOURCE_USER_ID = "INSERT HERE"
    SOURCE_USER_SECRET = "INSERT HERE"

    DESTINATION_USER_ID = "INSERT HERE"
    DESTINATION_USER_SECRET = "INSERT HERE"

Save the file `main.py` and run the script with python.

## Run the script
Once you run the script, a browser window will pop up asking you to log in with your Spotify credentials, log in with your source account.  
A confirmation prompt should appear.
A few seconds later a new window should appear asking you to log in again, click on `Not you?` and log in with the target account.

The songs have been transferred to the new account.

Remember that if you want to repeat the process you will have to log out of your [Spotify account](https://open.spotify.com) from the default browser.