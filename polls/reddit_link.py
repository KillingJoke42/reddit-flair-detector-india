import praw

def get_title(url):

	reddit = praw.Reddit(
							client_id="RImabBQtiUpnDw",
							client_secret="VOhkZ1p8g215x4hY354QEKdUEn0",
							user_agent="python-linux:text_classifier:v0.1a (by u/reddit_scraper_)"
						)

	sub_test = praw.models.Submission(reddit, url=url)

	del(reddit)
	return sub_test.title