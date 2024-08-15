import praw
import re

from .text_cleaner import clean_text


def fetch_subreddit_posts(subreddit_name, limit=5):
    
    """
    Fetches the latest posts from a subreddit.

    Returns:
        dict: A dictionary of post IDs and their cleaned text.
        
    """
   
    reddit = praw.Reddit(
        client_id='MHLfk5UxdRjHbN6OkB5gyQ',
        client_secret='aJt_aBCDHr-Ze6oSiZduHbdRrBLNYA',
        user_agent='vidify by /u/ChristmusLights2001',
    )

    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.new(limit=limit)
    
    posts_dict = {}

    for post in posts:
        # Ignore pinned posts
        if post.stickied:
            continue
        
        text = post.selftext
        cleaned_text = clean_text(text)
        
        posts_dict[post.id] = cleaned_text
    
    return posts_dict

