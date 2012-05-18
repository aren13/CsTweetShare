def __init__(self, username, key, secret, token_key, token_secret):  
      
        self.username = username  
        self.api = twitter.Api(  
                             consumer_key=key,   
                             consumer_secret=secret,   
                             access_token_key=token_key,  
                             access_token_secret=token_secret)  
        self.user_cache = dict()  
