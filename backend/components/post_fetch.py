import praw
import re
import os
from dotenv import load_dotenv

from .text_cleaner import clean_text

load_dotenv()

def fetch_subreddit_posts(subreddit_name, limit, post_type):
    
    """
    Fetches the latest posts from a subreddit.

    Returns:
        dict: A dictionary of post IDs and their cleaned text.
        
    """
    
    print('fetching posts', subreddit_name, limit, post_type)
   
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
    )

    subreddit = reddit.subreddit(subreddit_name)
    
    if post_type == 'hot':
        posts = subreddit.hot(limit=limit)
    elif post_type == 'new':
        posts = subreddit.new(limit=limit)
    elif post_type == 'top':
        posts = subreddit.top(limit=limit)
    
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
    print('fetched posts: ', posts_dict)
    return posts_dict
