# followCopy
Python script to copy the accounts another Twitter user is following.

Simply edit the config file with the corresponding information and remove the `.sample`. Upon execution the script will provide you with a URL to visit, in order to grant the necessary permissions to your twitter account. The code returned from the page should then be given back to the app as input.

Users already followed will be added to a list in order to be ignored later on in case of re-execution. An idea would be to run the script with a cronjob in order to be in sync with another account.

Requires python3 and Tweepy.

Note: The script will take a long time to finish due to Twitter API rate limitations.