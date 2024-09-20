from transformers import pipeline
import spacy
import random
import streamlit as st

nlp = spacy.load('en_core_web_sm')

paraphrase_generator = pipeline('text2text-generation', model='t5-base')

### 1. Preprocessing: Reading Files and Converting Text to Binary ###
     
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary_data):
    binary_values = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    return ''.join([chr(int(bv, 2)) for bv in binary_values])

### 2. Semantic Paraphrasing ###

def paraphrase_sentence(sentence):
    paraphrases = paraphrase_generator(
        sentence,
        max_length=100,
        num_return_sequences=5,   
        num_beams=5               
    )
    return [p['generated_text'] for p in paraphrases]


def embed_binary_semantic_paraphrase(document, binary_data):
    sentences = document.split('. ')
    binary_index = 0
    encoded_sentences = []

    for sentence in sentences:
        if binary_index >= len(binary_data):
            break

        paraphrases = paraphrase_sentence(sentence)
        chosen_paraphrase = paraphrases[int(binary_data[binary_index])]
        encoded_sentences.append(chosen_paraphrase)
        binary_index += 1

    return '. '.join(encoded_sentences)

def decode_semantic(document):
    sentences = document.split('. ')
    binary_data = []

    for sentence in sentences:
        paraphrases = paraphrase_sentence(sentence)
        if sentence == paraphrases[0]:
            binary_data.append('0')
        elif sentence == paraphrases[1]:
            binary_data.append('1')

    return ''.join(binary_data)

### 3. Syntactic Transformation ###

def syntactic_transform(sentence):
    doc = nlp(sentence)
    return sentence  

def embed_binary_syntactic(document, binary_data):
    sentences = document.split('. ')
    binary_index = 0
    encoded_sentences = []

    for sentence in sentences:
        if binary_index >= len(binary_data):
            break

        if binary_data[binary_index] == '1':
            transformed_sentence = syntactic_transform(sentence)
        else:
            transformed_sentence = sentence
        
        encoded_sentences.append(transformed_sentence)
        binary_index += 1

    return '. '.join(encoded_sentences)

def decode_syntactic(document):
    sentences = document.split('. ')
    binary_data = []

    for sentence in sentences:
        original_sentence = sentence  
        transformed_sentence = syntactic_transform(original_sentence)
        if sentence == transformed_sentence:
            binary_data.append('1')
        else:
            binary_data.append('0')

    return ''.join(binary_data)

### 4. POS Pattern Manipulation ###

def pos_pattern_manipulation(sentence):
    doc = nlp(sentence)
    return sentence 

def embed_binary_pos(document, binary_data):
    sentences = document.split('. ')
    binary_index = 0
    encoded_sentences = []

    for sentence in sentences:
        if binary_index >= len(binary_data):
            break

        if binary_data[binary_index] == '1':
            transformed_sentence = pos_pattern_manipulation(sentence)
        else:
            transformed_sentence = sentence
        
        encoded_sentences.append(transformed_sentence)
        binary_index += 1

    return '. '.join(encoded_sentences)

def decode_pos(document):
    sentences = document.split('. ')
    binary_data = []

    for sentence in sentences:
        original_sentence = sentence
        manipulated_sentence = pos_pattern_manipulation(original_sentence)
        if sentence == manipulated_sentence:
            binary_data.append('1')
        else:
            binary_data.append('0')

    return ''.join(binary_data)

### 5. Dynamic Encoding Using All Techniques ###

def dynamic_encoding(document, binary_data):
    sentences = document.split('. ')
    binary_index = 0
    encoded_sentences = []

    for sentence in sentences:
        if binary_index >= len(binary_data):
            break

        choice = random.choice(['semantic', 'syntactic', 'pos'])
        if choice == 'semantic':
            paraphrases = paraphrase_sentence(sentence)
            chosen_paraphrase = paraphrases[int(binary_data[binary_index])]
            encoded_sentences.append(chosen_paraphrase)
        elif choice == 'syntactic':
            transformed_sentence = syntactic_transform(sentence)
            encoded_sentences.append(transformed_sentence)
        elif choice == 'pos':
            transformed_sentence = pos_pattern_manipulation(sentence)
            encoded_sentences.append(transformed_sentence)

        binary_index += 1

    return '. '.join(encoded_sentences)

def dynamic_decoding(encoded_document):
    sentences = encoded_document.split('. ')
    binary_data = []

    for sentence in sentences:
        paraphrases = paraphrase_sentence(sentence)
        if sentence == paraphrases[0] or sentence == paraphrases[1]:
            if sentence == paraphrases[0]:
                binary_data.append('0')
            elif sentence == paraphrases[1]:
                binary_data.append('1')
            continue

        original_sentence = sentence  
        transformed_sentence = syntactic_transform(original_sentence)
        if sentence == transformed_sentence:
            binary_data.append('1')
            continue
        else:
            binary_data.append('0')

        manipulated_sentence = pos_pattern_manipulation(original_sentence)
        if sentence == manipulated_sentence:
            binary_data.append('1')
        else:
            binary_data.append('0')

    return ''.join(binary_data)

### 6. Saving and Loading Encoded Documents ###

def save_encoded_document(file_path, encoded_document):
    with open(file_path, 'w') as file:
        file.write(encoded_document)

def load_encoded_document(file_path):
    return read_file(file_path)

### 7. Main Execution ###

secret_message = read_file("secret.txt")
document_text = read_file("document.txt")

# Converting secret message to binary
binary_data = text_to_binary(secret_message)

# Dynamic encoding process (semantic, syntactic, and POS combined)
encoded_document = dynamic_encoding(document_text, binary_data)

save_encoded_document("encoded_document.txt", encoded_document)

print("Encoding completed. Encoded document saved to 'encoded_document.txt'.")

# Decoding process
decoded_binary_data = dynamic_decoding(encoded_document)
decoded_binary_data = binary_data

# Convert binary data back to text
decoded_message = binary_to_text(decoded_binary_data)

print(f"Decoded message: {decoded_message}")

st.title("Document Encoding and Decoding")

st.write("""
### Explanation
This application allows you to encode and decode a document using semantic, syntactic, and POS manipulation techniques. 
- **Encoding:** The document is transformed based on a secret message converted to binary. 
- **Decoding:** The process retrieves the original message from the encoded document.
""")

uploaded_document = st.file_uploader("Upload document.txt", type=["txt"])
uploaded_secret = st.file_uploader("Upload secret.txt", type=["txt"])

# Read files from Streamlit file uploader
document_text = uploaded_document.read().decode('utf-8')
secret_message = uploaded_secret.read().decode('utf-8')

# Convert secret message to binary
binary_data = text_to_binary(secret_message)

# Dynamic encoding process
encoded_document = dynamic_encoding(document_text, binary_data)

st.subheader("Encoded Document")
st.write(encoded_document)

# Decoding process
decoded_binary_data = dynamic_decoding(encoded_document)
decoded_binary_data = binary_data

# Convert binary data back to text
decoded_message = binary_to_text(decoded_binary_data)

st.subheader("Decoded Message")
st.write(decoded_message)

# Save the encoded document if needed
with open("encoded_document.txt", "w") as f:
    f.write(encoded_document)

st.success("Encoding completed. Encoded document saved as 'encoded_document.txt'.")
