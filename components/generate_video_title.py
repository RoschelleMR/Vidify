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

    prompt = f"Generate a catchy and relevant title for a YouTube video based on this transcript:\n\n{transcript}\n\nTitle:"
    
    response = client.chat.completions.create(
        model="gpt-4o",  # You can choose a different model if needed
        messages=[
            {"role": "system", "content": "You are a YouTube video creator. Generate a catchy and relevant title for a video based on the following transcript:"},
            {"role": "user", "content": transcript}
        ],
        max_tokens=20,  # Keep it short for a title
        temperature=0.7,
        n=1
    )
    
    title = response.choices[0].message.content
    return title

# # Example usage
# transcript = "This video is about a person who caught their spouse messaging others online and how they handled the situation."
# title = generate_video_title(transcript)
# print(f"Generated Title: {title}")