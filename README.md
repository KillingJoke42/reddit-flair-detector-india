# reddit-flair-detector-india
Flair Detector For the r/India Subreddit. Consists of Django App that can also recieve automated POST requests to get flairs for subreddit posts as long as a valid reddit url from r/india is provided

For information about the repository look at Manual+EDA.ipynb for more info<br>

To launch the app locally, clone the git repository. Refer to the requirements.txt to make sure you have all the dependancies <br>
cd to the cloned directory and run "python3 manage.py runserver"<br>

To access the heroku portal go to : "https://reddit-flair-detector-india.herokuapp.com/"<br>

To start automatic testing, send a POST request to 'automated_testing/' endpoint and receive a json of the predicted flairs.
