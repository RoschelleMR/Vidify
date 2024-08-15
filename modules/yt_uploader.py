import os
import sys
import json
from googleapiclient.discovery import build
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload


# Get the absolute path to the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Add the parent directory to sys.path so Python knows where to find your modules
sys.path.append(parent_dir)

from components.youtube_auth import load_credentials



# Configuration
CATEGORY_ID = "22"  # Default category ID for People & Blogs
PRIVACY_STATUS = "private"  # Default privacy status for videos
TAGS = ["AmItheAsshole", "AITA", "Reddit"]  # Default tags for videos

scopes = ["https://www.googleapis.com/auth/youtube"]

# Load credentials and create a YouTube client
credentials = load_credentials()
youtube = build('youtube', 'v3', credentials=credentials)

def upload_video(video_path, title, desc, tags=TAGS, category_id=CATEGORY_ID, privacy_status=PRIVACY_STATUS):
    """
        Uploads a video to YouTube.

        Args:
            video_path (str): Path to the video file.
            title (str): Title of the video.
            description (str): Description of the video.
            tags (list, optional): List of tags for the video.
            category_id (str, optional): YouTube category ID (default is "22" for People & Blogs).
            privacy_status (str, optional): Privacy status of the video (default is "public").
            
    """

    
    request_body = dict(
        snippet = dict(
            title = title,
            description = desc,
            tags = tags,
            categoryId = category_id
        ),
        status = dict(
            privacyStatus = privacy_status
        )
    )
    
    # request_body = json.dumps(request_body)
    # print(request_body)

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    
    request = youtube.videos().insert(
    part=",".join(request_body.keys()),
    body=request_body,
    media_body=media
    )
    
    # request = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media)
    response = None
    
    while response is None:
        status, response = request.next_chunk()
        
        print('This is the RESPONSE ', response, status)
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")
    
    # response = request.execute()
    uploaded_video_id = response.get('id')

    print(f"Video uploaded successfully: https://www.youtube.com/watch?v={uploaded_video_id}")


