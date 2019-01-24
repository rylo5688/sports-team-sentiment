from keys import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET
try:
    import json
except ImportError:
    import simplejson as json

from firebase import Firebase
from textblob import TextBlob
import tweepy


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

class StreamListener(tweepy.StreamListener):

    def setup(self, filter_by):
        # Initialize Firebase object with our tweet filter
        self.firebase = Firebase(filter_by) # TODO: Do we need to make a new firebase object for each streamlistener... probs not lul

    def get_sentiment(self, text):
        # Returns a sentiment value [-1, 1] for the text
        # TODO: Need to create an sentiment analyzer that understands LoL lingo
        processed_text = TextBlob(text)
        return processed_text.sentiment.polarity


    def on_status(self, status):
        # Callback function for streamed tweets
        #   Update firebase with this tweets information
        #   - If new tweet: Upload the tweet's text, id_str, hashtags, original url, and any counts
        #   - Else: Update the tweet's information: retweet count, favorite count, reply count (can also play around with the replies)
        # Twitter object info: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
        print("\nSTART\n")
        if "RT" in status.text:
            # This is a retweet so it may be shortened.
            # Use the retweeted_status object to get the full tweet.
            tweet_text = status.retweeted_status.text
            polarity = self.get_sentiment(tweet_text)
            self.firebase.push({"tweet_id": status.retweeted_status.id_str, "polarity": polarity})

            print("Original tweet:", status.retweeted_status.text)
            print("Polarity: ")
        else:
            tweet_text = status.text
            polarity = self.get_sentiment(tweet_text)
            self.firebase.push({"tweet_id": status.id_str, "polarity": polarity})

            print("Tweet-text:", status.text)
            print("Retweeted:", status.retweeted)

        print("Entities:", status.entities)
        print("\nEND\n")
        # print("Retweet-count:", status.retweet_count)
        # print("Reply-count:", status.reply_count)
        # print("Favorite-count:", status.favorite_count)



    def on_error(self, status_code):
        if status_code == 420:
            return False

def main():
    filter_by = "NBA"
    stream_listener = StreamListener()
    stream_listener.setup(filter_by)
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener, tweet_mode='extended')
    stream.filter(track=[filter_by, "NFL"], languages=["en"])

main()