import re


def replace_shorthand(match):
    """
    Replace Reddit shorthand for age and gender

    Args:
        match (re.Match): The matched object from the regex pattern.

    Returns:
        str: The cleaned text.
    """
    
    age = match.group(1)
    gender = match.group(2).lower()  # Convert to lowercase for uniformity
    if gender == 'f':
        return f"{age} female"
    elif gender == 'm':
        return f"{age} male"
    elif gender == 'nb':
        return f"{age} non-binary"
    return match.group(0)  # Return the original match if it doesn't fit known patterns
    
    


def clean_text(text):
    """
    Cleans the input text by removing special characters, 
    converting age/gender formats, and reducing excessive spaces.

    Args:
    text (str): The raw text to be cleaned.

    Returns:
    str: The cleaned text.
    """
    # Regex pattern to remove special characters except for apostrophes, full stops, commas, and question marks
    pattern = r"[^a-zA-Z0-9\s'.,?!]"
    cleaned_text = re.sub(pattern, '', text)

    # Replace multiple spaces with a single space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    # Replace age/gender formats (e.g., 27F to 27 Female, 27M to 27 Male)
    
    cleaned_text = re.sub(r'(\d+)([FfMm])', replace_shorthand, cleaned_text)
    
    # cleaned_text = re.sub(r'(\d{1,2})(F)', r'\1 Female', cleaned_text)
    # cleaned_text = re.sub(r'(\d{1,2})(M)', r'\1 Male', cleaned_text)

    # Remove excessive spaces
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text)

    return cleaned_text