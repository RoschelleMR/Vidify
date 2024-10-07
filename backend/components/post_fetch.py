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
    posts = subreddit.hot(limit=limit)
    
    posts_dict = {}

    for post in posts:
        # Ignore pinned posts
        if post.stickied:
            continue
        
        # dictitonary of post title, and selftext
        
        cleaned_title = clean_text(post.title)
        cleaned_selftext = clean_text(post.selftext)
        
        dict_post = {
            'title': cleaned_title,
            'selftext': cleaned_selftext 
        }
        
        posts_dict[post.id] = dict_post
    
    return posts_dict
