from riotwatcher import LolWatcher, ApiError
import pandas as pd
import time


def findDeaths():

	# golbal variables
	with open('token.txt','r') as f:
		api_key = f.read()
	watcher = LolWatcher(api_key)
	region = 'na1'

	names = {
		"Mister Six" : "Colbs", 
		"Senor Seis" : "Colbs",
		"bigbootysix" : "Colbs",

		"TheCobra451" : "Noah", 
		"bigbootycobra" : "Noah",

		"3LPatrrron" : "Christian", 
		"Twiddleyknobs" : "Christian", 
		"bigbootypatrrron" : "Christian",

		"HammerHanz156" : "Thor",
		"bigbootyhanz" : "Thor", 

		"Jaws311" : "Joe",
		"bigbootypatches" : "Joe"
		}

	# set up empty deaths dict
	deaths_dict = {}
	for name in names.keys():
		deaths_dict[names[name]] = 0

	
	for name in names.keys():

		summoner = watcher.summoner.by_name(region, name)
		all_matches = watcher.match.matchlist_by_account(region, summoner['accountId'])["matches"]

		#gather todays matches:
		matches = []
		today = time.gmtime(time.time() - 28800 )[0:3]

		for cur_match in all_matches:
			game_time = time.gmtime((cur_match['timestamp'] / 1000) - 28800)

			if game_time[0:3] != today:
				break

			else:
				matches.append(cur_match)


		#last_match = matches['matches'][0]
		for cur_match in matches:
			kills, deaths, assists = getMatchData(watcher, cur_match, region, name)

			print(f"{name}: {kills} / {deaths} / {assists}")

			addToDict(deaths_dict, names, name, deaths)

		time.sleep(1)

	print("............................")
	print("Death Totals for today:")
	for name in deaths_dict:
		print(f"{name}: {deaths_dict[name]}")

def getMatchData(watcher, match, region, name):
	kills, deaths, assists = 0, 0, 0

	match_detail = watcher.match.by_id(region, match['gameId'])
	participant_id = 0

	for row in match_detail['participantIdentities']:
		if (row["player"]['summonerName'].lower() == name.lower()):
			participant_id = row['participantId']
			break

	if participant_id == 0:
		print("***someing went wrong...")
		return 0, 0, 0

	for row in match_detail['participants']:
		if row['participantId']  == participant_id:
			kills = row['stats']['kills']
			deaths = row['stats']['deaths']
			assists = row['stats']['assists']
			return kills, deaths, assists

	return kills, deaths, assists

def addToDict(deaths_dict, names, name, deaths):
	if name in names.keys():
		deaths_dict[names[name]] += deaths 
	return

findDeaths()