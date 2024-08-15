from moviepy.editor import TextClip, VideoFileClip, CompositeVideoClip, AudioFileClip

from tqdm import tqdm

def generate_video(background_video, audio_path, audio_name, clip_words, final_duration):
    
    print("Loading background video...")
    original_video = VideoFileClip(background_video)
    print("Background video loaded.")

    print("Loading audio clip...")
    audio_clip = AudioFileClip(audio_path)
    print("Audio clip loaded.")

    print("Compositing video clips...")
    output_video = CompositeVideoClip([original_video] + clip_words)
    print("Video clips composited.")

    print("Trimming video to final duration...")
    final_video = output_video.subclip(0, final_duration)
    print("Video trimmed.")

    print("Setting audio to the final video...")
    final_video = final_video.set_audio(audio_clip)
    print("Audio set.")

    print(f"Generating final video file for {audio_name} ...")
    
    final_video.write_videofile(f'videos/generated/{audio_name}.mp4', codec='libx264', audio_codec="aac")
    
    print("Final video generated successfully.")