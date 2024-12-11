import re

def clean_text(text):
    #Removes all non-alphanumeric characters from the text.

    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

# Example usage:
text = "Hello! This# is$ a% sample^ text& with* (non-alphanumeric) -characters."
cleaned_text = clean_text(text)
print(cleaned_text)
