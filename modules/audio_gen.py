from elevenlabs import play, save
from elevenlabs.client import ElevenLabs
from tqdm import tqdm

client = ElevenLabs(
  api_key="sk_39ebd324a1e8c5683cd5a446e089ef369520d7c054447fe5", 
)

def generate_audio(text):
  
  """
    Generates audio from text. The text is a dictionary of post IDs and their cleaned text.
    
  """
  
  
  for post_id, post_info in tqdm(text.items(), desc="Generating audio"):
    
    post_title = post_info['title']
    post_selftext = post_info['selftext']
    
    # Combine the title and selftext into one string
    
    combined_text = f"{post_title}. {post_selftext}"
        
    # Generate audio from the combined text
    full_audio = client.generate(
        text=combined_text,
        voice='Lowy - soothing, gentle, and warm',
    )
    
    try:
      save(full_audio, f'./audio/{post_id}.mp3')
      print(f"Audio generated and saved for post ID: {post_id}")

    except Exception as e:
      print(f"An error occurred while saving audio for post ID {post_id}: {e}")
  
  return None


