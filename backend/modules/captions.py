## STEPS -- [Word by Word Captioning]
# ---------------------------------------
# 1. Load model
# 2. Get audio file loaction
# 3. Transcribe audio
# 4. Traverse segments of transcription to get words
# 5. Create an array of each word segment
# 6. Add it to video clip

from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

import whisper_timestamped as whisper
from moviepy.editor import TextClip, VideoFileClip, CompositeVideoClip, AudioFileClip

import moviepy.video.fx.all as vfx

import re



# Remove full stops, commas, exclamations, and question marks from the text.
def clean_text(text):
    
    cleaned_text = re.sub(r'[.,!?]', '', text)
    
    return cleaned_text


# 3.

def gen_transcription(model, audio):

    whisper_model = whisper.load_model(model)
    result = whisper_model.transcribe(audio, word_timestamps=True)

    return result

def get_word_segments(transcription):
    
    segments = transcription['segments']
    words_list = []
    last_segment = False
    
    for index, segment in enumerate(segments): 
        
        if index == len(segments) - 1:
            last_segment = True
        
        words = segment['words']
        
        for index_word, word in enumerate(words):
            
            # remove full stops, commas, exclamations, and question marks from the text.
            word['word'] = clean_text(word['word'])
            
            if index_word == len(words) - 1 and last_segment:
                duration = word['end']
                
            text1 = TextClip(
                txt=word['word'].upper(), 
                fontsize=80, 
                font='Montserrat-Black',
                stroke_width=15,
                stroke_color='black',
                color='white').set_start(word['start']).set_end(word['end']).set_position('center')
            
            text2 = TextClip(
                txt=word['word'].upper(), 
                fontsize=80, 
                font='Montserrat-Black',
                color='white').set_start(word['start']).set_end(word['end']).set_position('center')
            
            
            words_list.append(text1)
            words_list.append(text2)

            
            words_list.append(text1)
            words_list.append(text2)
            
            
    return words_list, duration


def generate_captions(audio):
    
    model = 'base'
    
    transcription = gen_transcription(model, audio)
    clip_words, final_duration = get_word_segments(transcription)
    
    print("Captions generated successfully.")

    return clip_words, final_duration

