import pandas as pd
import spacy
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from collections import Counter
import os


# Function to create the target directory if it doesn't exist
def create_target_directory(target_username):
    target_dir = f'Collection/{target_username}'
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)


# Load the CSV file into a pandas DataFrame based on the target username
target_username = input("Enter the target username: ")
target_username = target_username.strip("@")  # Remove @ symbol if present
csv_file = f'Collection/{target_username}/{target_username}_messages.csv'
if not os.path.exists(csv_file):
    print(f"Error: CSV file not found for {target_username}. Make sure the directory structure is correct.")
    exit()

df = pd.read_csv(csv_file)

# Load the spaCy NER model
nlp = spacy.load('en_core_web_sm')


# Preprocessing function
def preprocess_text(text):
    if isinstance(text, str):
        text = re.sub(r'http\S+', '', text)  # Remove URLs
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove non-alphanumeric characters
        text = re.sub(r'(?<=\w)[^\w\s]+(?=\w)', ' ',
                      text)  # Replace punctuation between alphanumeric characters with spaces
    return text


# Dictionary to store named entities of each category with counts
import contextlib
entity_categories = {
    'PERSON': Counter(),
    'ORG': Counter(),
    'GPE': Counter(),
    'DATE': Counter(),
    # You can add more categories here
}

# Process each text and extract named entities
for index, row in df.iterrows():
    text = row['Text']

    # Check if the text is a string
    if isinstance(text, str):
        preprocessed_text = preprocess_text(text)

        with contextlib.suppress(Exception):
            doc = nlp(preprocessed_text)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            for entity, label in entities:
                if label in entity_categories:
                    entity_categories[label][entity] += 1


# Create and export PDF with sorted entity tags
def export_entities_to_pdf(entity_categories, filename='entity_tags.pdf'):
    doc = SimpleDocTemplate(f'Collection/{target_username}/{filename}', pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Mapping for replacing 'ORG' with 'ORGANISATION' and 'GPE' with 'LOCATION'
    category_mapping = {'ORG': 'ORGANISATION', 'GPE': 'LOCATION'}

    # Sort entities within each category by count in descending order
    for category, entities in entity_categories.items():
        if entities:
            sorted_entities = sorted(entities.items(), key=lambda x: x[1], reverse=True)
            entity_str = ", ".join([f"{entity} (x{count})" for entity, count in sorted_entities])
            category_display = category_mapping.get(category, category)
            story.extend(
                (
                    Paragraph(
                        f"<b>{category_display} Entities:</b> {entity_str}",
                        styles["Normal"],
                    ),
                    Paragraph("<br/><br/>", styles["Normal"]),
                )
            )
    doc.build(story)


# Export entities to PDF
export_entities_to_pdf(entity_categories)
print(f"PDF report created: Collection/{target_username}/entity_tags.pdf")

# Ask if the user wants to return to the launcher
launcher = input('Do you want to return to the launcher? (y/n)')

if launcher == 'y':
    print('Restarting...')
    exec(open("launcher.py").read())
