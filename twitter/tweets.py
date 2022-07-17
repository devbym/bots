import tweepy
from flask import current_app as app 

def authTwitter(user=False):
    if not user:
        # Auth read-only access
        print("!-- Twitter AppAuth (public)")
        auth = tweepy.AppAuthHandler(app.config['CONSUMER_KEY'],app.config['CONSUMER_SECRET'])
        api = tweepy.API()
    else:
        # Verify credentials and set access token
        auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'],app.config['CONSUMER_SECRET'])        
        auth.set_access_token(app.config['ACCESS_TOKEN'], app.config['ACCESS_TOKEN_SECRET'])
        app.logger.info(f"!-- Succesfully logged in as user: {auth.get_username()}")
        #Invoke API instance
        api = tweepy.API(auth)
        api.get_status
    return api

if app.config['TWITTER'] == True:
    sshintomysoul = authTwitter("sshintomysoul")
else:
    app.logger.info("Twitter disabled, skipping authentication")

def pubTweets(user=sshintomysoul):
    if user == None:
        return False
    elif user == sshintomysoul:
        twapi = user
    else:
        try:
            twapi = authTwitter(user)
        except Exception:
            print(f"Error occured during Twitter auth for user {user}")
            pass
    params = dict(
    trim_user=True,
    tweet_mode='extended',
    count=10,
    )
    public_tweets = twapi.home_timeline(**params)
    #public_tweets = [status._json for status in public_tweets]
    twt = [ dict(
        id = str(x.id),
        author = twapi.get_user(x.author.id).name,
        time = str(x.created_at),
        likes = x.favorite_count,
        retweets = x.retweet_count,
        text = x.full_text,
        #usr = dir(x.author),
        is_quote = x.is_quote_status
        ) for x in public_tweets]
    return twt






