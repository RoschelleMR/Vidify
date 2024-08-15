from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Example usage:
word = "happy"
polarity = analyze_sentiment(word)
print(f"The sentiment polarity of '{word}' is {polarity}")