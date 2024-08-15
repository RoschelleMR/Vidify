import sys
import os

import moviepy.editor as mpy
import moviepy.video.fx.all as vfx

from components.post_fetch import fetch_subreddit_posts
from modules.audio_gen import generate_audio
from modules.captions import generate_captions
from modules.video_gen import generate_video
from modules.yt_uploader import upload_video

import schedule
import time


def generate_batch():
     
    
    subreddit_name = 'AmItheAsshole'
    fetched_posts = fetch_subreddit_posts(subreddit_name, limit=10)
    
    generate_audio(fetched_posts)
    
    audio_folder = './audio'

    # Traverse all the audios in the audio folder
    for audio_file in os.listdir(audio_folder):
        
        if audio_file.endswith('.mp3'):
            
            audio_name = audio_file.split('.')[0]
            audio_path = os.path.join(audio_folder, audio_file)
            
            # Generate captions for each audio
            clip_words, final_duration = generate_captions(audio_path)
            
            generate_video('videos/background/minecraft_1.mp4', audio_path, audio_name, clip_words, final_duration)
            
    print("All videos generated successfully.")



def scheduled_upload(path, video_title, video_desc):
    
    print('Running scheduled upload...')
    
    upload_video(video_path=path, title= video_title, desc= video_desc, tags=['AmItheAsshole', 'AITA', 'Reddit'], privacy_status='private')

def check_and_generate_videos():
    
    main_video_path = './videos/generated'
    
    # Check if there are fewer than 3 videos available
    video_count = len([f for f in os.listdir('./videos/generated') if f.endswith('.mp4')])
    
    # Get list of videos in the directory
    video_files = sorted([f for f in os.listdir('./videos/generated') if f.endswith('.mp4')])
    print(video_files)
    
    if video_count < 3:
        
        print("Not enough videos. Generating more...")
        generate_batch()
        
        video_title = video_files[0].split('.')[0] ## temporary
        video_path = main_video_path + '/' + video_files[0]
        
        scheduled_upload(video_path, video_title, "Example video description")
        
    else:
        
        video_title = video_files[0].split('.')[0]
        video_path = main_video_path + '/' + video_files[0]
        
        
        scheduled_upload(video_path, video_title + ' #shorts', "Example video description")

        

# schedule.every().second.do(check_and_generate_videos)

# Scheduler for three specific times of the day
schedule.every().day.at("9:00").do(check_and_generate_videos)
schedule.every().day.at("15:00").do(check_and_generate_videos)
schedule.every().day.at("21:00").do(check_and_generate_videos)


if __name__ == "__main__":
    
    
    while True:
        schedule.run_pending()
        time.sleep(1)