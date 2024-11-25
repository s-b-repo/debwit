import tweepy


def error_handler(func):
    """Decorator to handle and log API errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except tweepy.TweepyException as e:
            raise RuntimeError(f"Twitter API error: {str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {str(e)}") from e

    return wrapper


class TwitterBackend:
    def __init__(self, api_key, api_secret, access_token, access_token_secret):
        """Initialize the Twitter API."""
        self.auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

        # Verify credentials on initialization
        self.verify_credentials()

    @error_handler
    def verify_credentials(self):
        """Check if the credentials are valid."""
        user = self.api.verify_credentials()
        if not user:
            raise RuntimeError("Invalid Twitter API credentials!")
        print(f"Successfully authenticated as @{user.screen_name}")

    @error_handler
    def send_tweet(self, tweet_text):
        """Send a tweet."""
        if not tweet_text.strip():
            raise ValueError("Tweet text cannot be empty!")
        return self.api.update_status(tweet_text)

    @error_handler
    def get_mentions(self, count=10):
        """Fetch mentions timeline."""
        return self.api.mentions_timeline(count=count)

    @error_handler
    def get_direct_messages(self, count=10):
        """Fetch direct messages."""
        return self.api.get_direct_messages(count=count)

    @error_handler
    def update_profile(self, name=None, bio=None):
        """Update Twitter profile information."""
        if not name and not bio:
            raise ValueError("Name and bio cannot both be empty!")
        return self.api.update_profile(name=name, description=bio)

    @error_handler
    def get_user_info(self):
        """Fetch the authenticated user's profile info."""
        user = self.api.verify_credentials()
        return {
            "name": user.name,
            "screen_name": user.screen_name,
            "description": user.description,
            "followers": user.followers_count,
            "following": user.friends_count,
        }
