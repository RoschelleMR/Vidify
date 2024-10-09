import json
import random
import time
from flask import Flask, Response, jsonify, request, session
import requests
from dotenv import load_dotenv
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import os, pathlib
import google
import jwt
from flask_cors import CORS

import moviepy.editor as mpy
import moviepy.video.fx.all as vfx

from moviepy.editor import VideoFileClip, concatenate_videoclips

from video_db import delete_video, get_user_videos, store_video_metadata, upload_video_to_blob
from components.post_fetch import fetch_subreddit_posts
from modules.audio_gen import generate_audio
from modules.captions import generate_captions
from modules.video_gen import generate_video
from modules.yt_uploader import upload_video

from db import upsert_user, get_user




# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Config for CORS
app.config['Access-Control-Allow-Origin'] = '*'
app.config['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
app.config["Access-Control-Allow-Headers"]="Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"

# To allow Http traffic for local dev
app.secret_key = os.getenv('FLASK_SECRET_KEY')
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" 

AUTH_FOLDER = 'auth/'
CLIENT_SECRETS_FILE = os.path.join(AUTH_FOLDER, 'client_secrets.json')
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid']
REDIRECT_URI = 'http://localhost:5000/auth/google/callback'
ALGORITHM = os.getenv("ALGORITHM")
BACKEND_URL=os.getenv("BACKEND_URL")
FRONTEND_URL=os.getenv("FRONTEND_URL")


flow = Flow.from_client_secrets_file(
    client_secrets_file=CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)


# Load all video clips from the directory (helper function)
def load_clips(directory):
    clips = []
    for file_name in os.listdir(directory):
        if file_name.endswith(".mp4"):
            clip = VideoFileClip(os.path.join(directory, file_name))
            clips.append(clip)
    return clips

# Create a background video by concatenating random clips to match the audio length
def create_background_video(clips, audio_length):
    selected_clips = []
    total_duration = 0

    while total_duration < audio_length:
        clip = random.choice(clips)
        selected_clips.append(clip)
        total_duration += clip.duration

    background_video = concatenate_videoclips(selected_clips)
    return background_video


def generate_videos(subreddit_name, post_type, limit=5):
    # Fetch posts from the subreddit
    fetched_posts = fetch_subreddit_posts(subreddit_name=subreddit_name, limit=limit, post_type=post_type)

    # Generate audio from fetched posts
    generate_audio(fetched_posts)

    audio_folder = '../audio'
    background_clips = load_clips('../videos/background')

    generated_videos = []  # Store the details of generated videos

    for audio_file in os.listdir(audio_folder):
        if audio_file.endswith('.mp3'):
            audio_name = audio_file.split('.')[0]
            audio_path = os.path.join(audio_folder, audio_file)

            # Generate captions for each audio
            clip_words, final_duration = generate_captions(audio_path)

            # Create background video
            background_video = create_background_video(background_clips, final_duration)

            # Generate the final video
            video_path = generate_video(background_video, audio_path, audio_name, clip_words, final_duration)
            
            # Store video details
            generated_videos.append({
                "title": audio_name,
                "path": video_path
            })

    return generated_videos

# JWT generation function
def generate_JWT(payload):
    encoded_jwt = jwt.encode(payload, app.secret_key, algorithm=ALGORITHM)
    return encoded_jwt

# Login required decorator to protect routes
def login_required(function):
    
    def wrapper(*args, **kwargs):
        encoded_jwt = request.headers.get("Authorization").split("Bearer ")[1]
        if encoded_jwt is None:
            return abort(401)
        else:
            return function()
    return wrapper


# OAuth2 callback route
@app.route('/auth/google/callback')
def google_callback():

    
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    # Create a session to request Google services
    request_session = requests.session()
    token_request = google.auth.transport.requests.Request(session=request_session)
    
    # Verify the Google ID token
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID,
        clock_skew_in_seconds=15
    )
    session["google_id"] = id_info.get("sub")  # Store Google ID in session

    # Generate JWT
    del id_info['aud']  # Removing 'aud' field to prevent any errors
    
    user_data = {
            "id": id_info.get("sub"),
            "name": id_info.get("name"),
            "email": id_info.get("email"),
            "profile_picture": id_info.get("picture"),
            "googleAccessToken": credentials.token,
            "googleRefreshToken": credentials.refresh_token 
    }
    
    
    # Store user data in Cosmos DB
    upsert_user(user_data)
    
    jwt_token = generate_JWT(id_info)
    
    # Redirect user to the frontend with JWT in the query params
    return redirect(f"{FRONTEND_URL}?jwt={jwt_token}")


# Google OAuth2 login route
@app.route("/auth/google")
def login():
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    session["state"] = state  # Store state in session
    return redirect(authorization_url)

    
# Logout route to clear the session
@app.route("/logout")
def logout():
    session.clear()  # Clear session
    return Response(
        response=json.dumps({"message": "Logged out"}),
        status=202,
        mimetype='application/json'
    )
    
# Protected route that requires login
@app.route("/home", methods=["GET"])
@login_required
def home_page_user():
    
    encoded_jwt = request.headers.get("Authorization").split("Bearer ")[1]
    try:
        decoded_jwt = jwt.decode(encoded_jwt, app.secret_key, algorithms=[ALGORITHM], leeway=15)
        return Response(
            response=json.dumps(decoded_jwt),
            status=200,
            mimetype='application/json'
            
        )
    except jwt.ExpiredSignatureError:
        return Response(
            response=json.dumps({"message": "Token has expired"}),
            status=401,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({"message": "Decoding JWT Failed", "exception": e.args}),
            status=500,
            mimetype='application/json'
        )


@app.route('/generate_videos', methods=['POST'])
def generate_videos_route():
    
    if request.method == 'POST':
        
        data = request.get_json()
        
        print('This is the data', data)
        # Extract subreddit, number of videos, and post type from the request
        subreddit_name = data.get('subreddit')
        post_type = data.get('post_type')
        num_videos = data.get('num_videos')
        user_id = data.get('user_id')
        

        # Call the generate_videos function
        # generated_videos = generate_videos(subreddit_name, post_type, num_videos)
        
        # Sample generated videos for testing
        generated_videos = [{
            "path": "../videos/generated/1fzgp8r.mp4",
            "title": "1fzgp8r"
        },
        {
            "path": "../videos/generated/1euv77y.mp4",
            "title": "1euv77y"
        },
        {
            "path": "../videos/generated/1euxboj.mp4",
            "title": "1euxboj"
        }
        ]
        
        # Iterate through generated videos and upload to Blob Storage + store metadata in CosmosDB
        uploaded_videos = []
        
        for video in generated_videos:
            video_path = video["path"]  # Local path to the generated video
            video_title = video["title"]
            
            # Upload video to Azure Blob
            blob_url = upload_video_to_blob(video_path, user_id, video_title)
            
            if blob_url:
                # Store video metadata in CosmosDB
                store_video_metadata(user_id, blob_url, video_title)
                
                uploaded_videos.append({
                    "title": video_title,
                    "url": blob_url
                })


        # Return response with video details
        return jsonify({
            "status": "success",
            "generated_videos": uploaded_videos
        })
    return abort(405)

@app.route('/my_videos', methods=['GET'])
def get_user_videos_route():
    user_id = request.args.get('user_id')

    # Fetch videos for the user
    videos = get_user_videos(user_id)

    return jsonify({
        "status": "success",
        "videos": videos
    })
    

@app.route('/delete_video/<video_id>', methods=['DELETE'])
def delete_video_route(video_id):
    user_id = request.args.get('user_id')  
    blob_name = request.args.get('blob_name') 

    # The function to delete the video
    success = delete_video(user_id, video_id, blob_name)

    if success:
        return jsonify({"status": "success", "message": "Video deleted successfully"})
    else:
        return jsonify({"status": "error", "message": "Failed to delete video"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)