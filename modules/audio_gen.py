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
  
  for post_id, post_text in tqdm(text.items(), desc="Generating audio"):
    
    audio = client.generate(
      text=post_text,
      voice='Will',
    )
    
    try:
      save(audio, f'./audio/{post_id}.mp3')
      print(f"Audio generated and saved for post ID: {post_id}")

    except Exception as e:
      print(f"An error occurred while saving audio for post ID {post_id}: {e}")
  
  return None
