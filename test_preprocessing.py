
from modules.text_preprocessing import preprocess_text

sample_text = """
HELLO! I am a Python Developer.
I have experience in Python, SQL, C++ and Machine Learning.
Visit https://example.com for more information.
"""

result = preprocess_text(sample_text)

print("\nORIGINAL TEXT:")
print(sample_text)

print("\nCLEANED TEXT:")
print(result["cleaned_text"])

print("\nTOKENS:")
print(result["tokens"])

print("\nFILTERED TOKENS:")
print(result["filtered_tokens"])

print("\nFINAL PROCESSED TEXT:")
print(result["processed_text"])
