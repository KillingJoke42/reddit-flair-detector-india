import praw
from matplotlib import pyplot as plt

reddit = praw.Reddit(
						client_id="RImabBQtiUpnDw",
						client_secret="VOhkZ1p8g215x4hY354QEKdUEn0",
						user_agent="python-linux:text_classifier:v0.1a (by u/reddit_scraper_)"
					)
def get_hot_data(limit):

	link_flair_tags = {
					"Politics":0, 
					"Non-Political":0, 
					"AskIndia":0, 
					"Policy/Economy":0, 
					"Business/Finance":0, 
					"Science/Technology":0, 
					"Scheduled":0, 
					"Sports":0, 
					"Food":0,
					"Photography":0,
					"CAA-NRC-NPR":0,
					"Coronavirus":0,
				  }

	for submission in reddit.subreddit('india').hot(limit=limit):
		if submission.link_flair_text:
			try:
					link_flair_tags[submission.link_flair_text] += 1
					flair = submission.link_flair_text
			except KeyError:
				print("New Flair Found: " + submission.link_flair_text + ". Ignoring..........")

	flairs = link_flair_tags.keys()
	values = link_flair_tags.values()

	plt.bar(flairs, values)
	plt.xticks(rotation="vertical")
	plt.tight_layout()
	plt.savefig('polls/static/hot_graph.png')
	return link_flair_tags

def get_new_data(limit):

	link_flair_tags = {
					"Politics":0, 
					"Non-Political":0, 
					"AskIndia":0, 
					"Policy/Economy":0, 
					"Business/Finance":0, 
					"Science/Technology":0, 
					"Scheduled":0, 
					"Sports":0, 
					"Food":0,
					"Photography":0,
					"CAA-NRC-NPR":0,
					"Coronavirus":0,
				  }

	for submission in reddit.subreddit('india').new(limit=limit):
		if submission.link_flair_text:
			try:
				link_flair_tags[submission.link_flair_text] += 1
			except KeyError:
				print("New Flair Found: " + submission.link_flair_text + ". Ignoring..........")

	flairs = link_flair_tags.keys()
	values = link_flair_tags.values()

	plt.bar(flairs, values)
	plt.xticks(rotation="vertical")
	plt.tight_layout()
	plt.savefig('polls/static/new_graph.png')
	return link_flair_tags