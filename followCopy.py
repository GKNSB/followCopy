import tweepy
import time
import configparser
from datetime import datetime


config = configparser.RawConfigParser()
config.read("configuration.config")
consumer_key = config.get("Config", "consumer_key")
consumer_secret = config.get("Config", "consumer_secret")
user_to_copy = config.get("Config", "user_to_copy")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
print(auth.get_authorization_url())
pin = input('Please insert the PIN you get from the page above:')
token = auth.get_access_token(verifier = pin)

access_token = token[0]
access_token_secret = token[1]
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)
myid = api.me().id
myname = api.me().screen_name
startingTime = time.time()

print("[{0}] Authenticated as: {1} with id {2}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), myname, myid))
time.sleep(5)

followedUsers = []
with open("alreadyFollowed.txt", "a+") as followedFile:
	followedFile.seek(0)

	for line in followedFile:
		followedUsers.append(line.strip())

	i = 1
	banned = []
	alreadyRequested = []

	for user in tweepy.Cursor(api.friends, screen_name=userToCopy).items():
		if user.id not in followedUsers:
			print('{0} User: {1} - Id: {2} - Protected: {3}'.format(i, user.screen_name, user.id, user.protected))
			i += 1

			mustretry = True
			sleepinc = 0

			while(mustretry):
				try:
					api.create_friendship(user.id)
					followedFile.write("\n{0}".format(str(user.id)))
					mustretry = False

				except tweepy.error.TweepError as err:
					if int(err.args[0][0]['code']) == 106 or int(err.args[0][0]['code']) == 162:
						mustretry = False
						banned.append(user)

					elif int(err.args[0][0]['code']) == 160:
						mustretry = False
						alreadyRequested.append(user)

					else:
						print("    [{0}] {1}... Will retry after {2} minutes.".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), err, 2**sleepinc))
						time.sleep(60*2**sleepinc)
						if sleepinc < 9:
							sleepinc +=1
						else:
							pass

		else:
			pass

print("[{0}] -- Already requested users: -- ".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
for user in alreadyRequested:
	print(user.screen_name)

print("[{0}] -- Banned users: -- ".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
for user in banned:
	print(user.screen_name)

endingTime = time.time()
print("[{0}] Execution took {1} seconds".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), int(endingTime - startingTime)))
