import time
import praw
import re
import datetime
from datetime import datetime
import sys

if len(sys.argv) != 3:
	print("incorrect number of arguments, format should be py kotdDataCollection.py [username] [number of posts to check]")
	sys.exit()
if sys.argv[1].isdigit() or not sys.argv[2].isdigit():
	print("incorrect format of arguments, format should be py kotdDataCollection.py [username] [number of posts to check]")
	sys.exit()

#reddit api login
reddit = praw.Reddit(client_id='XDExPtYHaw_Y1A',
					client_secret = 'Nm8PeYUq-zr004RQ3mQcw4pqZ58',
					username = 'Daman159sBotBitch',
					password = 'this is totally the actual password',
					user_agent = 'A random bot for doing stuff and learning bot coding by /u/Daman159')

#subreddits active in
subreddit = reddit.subreddit('kickopenthedoor')

attacksProcessed = []
aliveMonsters = []
deadMonsters = []
maxPosts = int(sys.argv[2])
attackTotal = 0
attackNum = 0
totalDamage = 0
totalGold = 0
totalXP = 0
userTarget = sys.argv[1]
nowDateTime = datetime.fromtimestamp(time.time())
deathDateTime = datetime.fromtimestamp(time.time())
aphTotal = 0.0


def getData(monster):
	global attackTotal
	global totalDamage
	global totalXP
	global totalGold
	global deathDateTime
	global attackNum
	global submission
	global attacksProcessed
	attackNum = 0
	submission = reddit.submission(monster)
	submission.comments.replace_more(limit=None)
	subComments = submission.comments.list()
	deathDateTime = datetime.fromtimestamp(time.time())
	for comment in subComments:
		if comment.author is not None:
			if comment.author.name == 'KickItOpen_Bot' and 'KILL!' in comment.body:
				deathDateTime = datetime.fromtimestamp(comment.created_utc)
			if comment.author.name == userTarget and '!attack' in comment.body:
				comment.replies.replace_more(limit=None)
				replyComments = comment.replies.list()
				for reply in replyComments:
					if reply.author is not None:
						if reply.author.name == 'KickItOpen_Bot' and 'Gold' in reply.body and reply.id not in attacksProcessed:
							commentBody = reply.body
							splitString = commentBody.split('Gold', 1)[1]
							nums = [int(i) for i in splitString.split() if i.isdigit()]
							attackTotal = attackTotal + 1
							attackNum = attackNum + 1
							totalDamage = totalDamage + nums[0]
							totalXP = totalXP + nums[1]
							totalGold = totalGold + nums[2]
							attacksProcessed.append(reply.id)
		
		
for submission in subreddit.new(limit=maxPosts): #finding each submission that is a monster (alive or dead), limit of maxPosts
	try:
		flairtext = submission.link_flair_text
		if flairtext is not None:
			isAlive = re.search('Health: (\d+)', flairtext)
			isDead = re.search('Slain', flairtext)
			if isAlive:
				aliveMonsters.append(submission.id)
			if isDead:
				deadMonsters.append(submission.id)
	except praw.exceptions.APIException as e:
		print(e.message)
		
for monster in aliveMonsters: #for each monster find all attacks by userTarget and collect data
	try:
		getData(monster)
		subPostDateTime = datetime.fromtimestamp(submission.created_utc)
		aphTotal = aphTotal + (attackNum / ((nowDateTime - subPostDateTime).seconds / 60 / 60))
	except praw.exceptions.APIException as e:
		print(e.message)

for monster in deadMonsters: #for each monster find all attacks by userTarget and collect data
	try:
		getData(monster)
		subPostDateTime = datetime.fromtimestamp(submission.created_utc)
		aphTotal = aphTotal + (attackNum / ((deathDateTime - subPostDateTime).seconds / 60 / 60))
	except praw.exceptions.APIException as e:
		print(e.message)
print('TOTALS Monsters Found: %d, Attacks: %d, Damage: %d, XP: %d, Gold: %d' % ((len(aliveMonsters) + len(deadMonsters)), attackTotal, totalDamage, totalXP, totalGold))
print('AVERAGES Attacks/Hour: %f, Damage: %f, XP: %f, Gold: %f' % (aphTotal / (len(aliveMonsters) + len(deadMonsters)), totalDamage / float(attackTotal), totalXP / float(attackTotal), totalGold / float(attackTotal)))