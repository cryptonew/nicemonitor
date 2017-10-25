#import config
from config import *
import json, requests
import datetime
import time
requests.packages.urllib3.disable_warnings()

def sendAlert(message, alert):
		#trigger IFTTT event
		report = {}
		report["value1"] = message
		requests.post("https://maker.ifttt.com/trigger/" + alert + "/with/key/" + iftttKey, data=report)

def getStats():
	#query the nicehash API and check worker's status
	url = 'https://api.nicehash.com/api'

	params = dict(
		method='stats.provider.workers',
		addr=btcAddress,
		algo=24
		)

	resp = requests.get(url=url, params=params)
	stats = json.loads(resp.text)
	return stats

stats = getStats()

if len(stats.get("result").get("workers")) < workers_num:
	print ""
	print "First Check Fails. Workers < " + workers_num
	print stats
	print ""
	time.sleep(45)
	stats = getStats()
	if len(stats.get("result").get("workers")) < workers_num:
		print ""
		print "Second Check Fails. Workers < " + workers_num + " Some workers DOWN"
		print stats
		print ""
		time.sleep(45)
		stats = getStats()
		if len(stats.get("result").get("workers")) < workers_num:
               		sendAlert("Nicehash worker DOWN. Please fix it!","nicehash")
			print ""
    			print "Third Check Fails. Workers < " + workers_num + " Some workers DOWN"
               		print stats
			print ""
			print time.strftime("%Y-%m-%d %H:%M:%S")
			print "--------------------------------------------"
			exit()

for worker in stats["result"]["workers"]:
	if float(worker[1].get("a")) < 800:
		sendAlert("Trouble! Worker " + str(worker[0]) + " Speed = " + str(worker[1].get("a")),"nicehash")
		print str(worker[0]) + "Accepted <800"
		print str(worker[0]) + " Speed = " + str(worker[1].get("a"))
		if str(type(worker[1].get("r"))) == "<type 'float'>":
			sendAlert("Trouble! Worker " + str(worker[0]) + " Rejected Speed = " + str(worker[1].get("r")),"nicehash")
			print str(worker[0]) + "Rejected Speed = " + str(worker[1].get("r"))

	elif str(type(worker[1].get("r"))) == "<type 'float'>":
		sendAlert("Trouble! Worker " + str(worker[0]) + " Rejected Speed = " + str(worker[1].get("r")),"nicehash")
		print str(worker[0]) + "Rejected Speed = " + str(worker[1].get("r"))
	else:
		 print "OK"
		 print str(worker[0]) + " Speed = " + str(worker[1].get("a"))

print ""
print time.strftime("%Y-%m-%d %H:%M:%S")
print "--------------------------------------------"
exit()
