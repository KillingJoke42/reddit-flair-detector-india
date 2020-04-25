# Import Reddit API Wrapper
import praw

# Function to get the title from the URL
def get_title(url):

	# Get the Reddit API Wrapper object: PRAW object
	reddit = praw.Reddit(
							client_id="RImabBQtiUpnDw",
							client_secret="VOhkZ1p8g215x4hY354QEKdUEn0",
							user_agent="python-linux:text_classifier:v0.1a (by u/reddit_scraper_)"
						)

	# Get the submission from the url
	sub_test = praw.models.Submission(reddit, url=url)

	# Return the title that was collected from the URL
	del(reddit)
	return sub_test.title