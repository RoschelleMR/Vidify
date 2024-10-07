import openai

client = openai.OpenAI(
    api_key="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",
    organization="org-riqQmnUrozQlh9m1zCDz9PPx",
    project="proj_6IAz4bd9tr4LVxqHDFV4nrtX"
)



def generate_video_title(transcript):
    """
    Generates a video title based on the transcript using OpenAI's GPT model.
    
    Args:
        transcript (str): The transcript of the video.
    
    Returns:
        str: Generated video title.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",  # You can choose a different model if needed
        messages=[
            {"role": "system", "content": "You are a YouTube video creator. Generate a short catchy and relevant title for a video based on the following transcript"},
            {"role": "user", "content": transcript}
        ],
        max_tokens=256,  # Keep it short for a title
        temperature=1,
        n=1
    )
    
    title = response.choices[0].message.content
    return title

# # Example usage using long reddit post transcript for a 2 minute long video
# transcript = """Am I the asshole for not wanting to attend my sister's wedding? My sister and I have never been close. She has always been the golden child in our family, while I have been the black sheep. She is the one who always gets the attention and praise, while I am the one who is always criticized and ignored. I have always felt like I am not good enough for my family, and my sister's wedding is just another reminder of that. I know that I should be happy for her, but I just can't bring myself to attend the wedding. I don't want to be a part of her special day when I have never felt like a part of the family. Am I the asshole for not wanting to attend my sister's wedding?"""
# title = generate_video_title(transcript)
# print(f"Generated Title: {title}")