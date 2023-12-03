import os
import re
import pandas as pd
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import PageBreak

# Function to extract sentences containing key phrases

def extract_sentences(username, input_csv, output_pdf, target_phrase_list1, target_phrase_list2, target_phrase_list3):
    username = username.strip("@")  # Remove "@" symbol from username

    input_csv_path = f"Collection/{username}/{username}_messages.csv"
    output_pdf_path = f"Collection/{username}/{username}_threat_assessment.pdf"

    if not os.path.exists(input_csv_path):
        print(f"CSV file not found: {input_csv_path}")
        return

    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv_path, encoding='utf-8')

    # Create a PDF document
    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)

    # Define paragraph styles
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    subheading_style = styles["Heading2"]
    normal_style = styles["Normal"]
    normal_style.leading = 14
    normal_style.alignment = 0
    citation_style = ParagraphStyle(name='CitationStyle', parent=normal_style)
    citation_style.leading = 6

    # Add the title to the PDF
    title = Paragraph("Target Threat Assessment", title_style)
    story = [title, Spacer(1, 12)]

    # Add subheading for possible indicators of capability
    subheading_capability = Paragraph("Possible Indicators of Capability", subheading_style)
    story.extend([subheading_capability, Spacer(1, 12)])

    # Create a regex pattern for each target phrase with proximity search
    target_patterns_capability = [
        re.compile(r'\b(?:' + '|'.join(re.escape(phrase1) for phrase1 in target_phrase_list1) + r')\b.{0,5}\b(?:' + '|'.join(re.escape(phrase2) for phrase2 in target_phrase_list2) + r')\b', re.IGNORECASE)
    ]

    # Iterate through messages and extract sentences for capability
    for index, row in df.iterrows():
        message = str(row['Text'])  # Convert to string to handle non-string values
        url = row['Message URL']  # Get the source URL
        sentences = re.split(r'(?<=[.!?])\s+', message)

        for sentence in sentences:
            for pattern in target_patterns_capability:
                if re.search(pattern, sentence):
                    # Highlight target phrases
                    highlighted_sentence = re.sub(pattern, r'<font color="red">\g<0></font>', sentence)
                    story.extend((Paragraph(highlighted_sentence, normal_style), Spacer(1, 6)))
                    # Add URL end-note citation with size 6 font and bold "Source:"
                    citation = Paragraph(f"<font size='6'><b>Source:</b> <a href='{url}'>{url}</a></font>", citation_style)
                    story.extend((citation, Spacer(1, 12)))

    # Add subheading for possible indicators of violent intent
    subheading_intent = Paragraph("Possible Indicators of Violent Intent", subheading_style)
    story.extend([PageBreak(), subheading_intent, Spacer(1, 12)])

    # Create regex pattern for each target phrase without proximity search
    target_patterns_intent = [re.compile(r'\b(?:' + '|'.join(re.escape(phrase) for phrase in target_phrase_list3) + r')\b', re.IGNORECASE)]

    # Iterate through messages and extract sentences for violent intent
    for index, row in df.iterrows():
        message = str(row['Text'])
        url = row['Message URL']
        sentences = re.split(r'(?<=[.!?])\s+', message)

        for sentence in sentences:
            for pattern in target_patterns_intent:
                if re.search(pattern, sentence):
                    # Highlight target phrases
                    highlighted_sentence = re.sub(pattern, r'<font color="red">\g<0></font>', sentence)
                    story.extend((Paragraph(highlighted_sentence, normal_style), Spacer(1, 6)))
                    # Add URL end-note citation with size 6 font and bold "Source:"
                    citation = Paragraph(f"<font size='6'><b>Source:</b> <a href='{url}'>{url}</a></font>", citation_style)
                    story.extend((citation, Spacer(1, 12)))

    # Create the PDF
    doc.build(story)
    print(f"Key phrase extraction report saved to {output_pdf_path}")

if __name__ == "__main__":
    # Define target phrase lists
    target_phrase_list1 = ["my", "buy", "buying", "get", "getting", "got", "have", "acquire", "acquiring", "obtain", "obtaining", "procure", "procuring",  "wanting", "want to", "want a" "going to", "own", "owning", "license", "a", "with", "certified", "need", "stolen", "steal a", "3d print", "3d-print", "3d printed", "3d-printed", "borrow", "take",]
    target_phrase_list2 = ["gun", "rifle", "pistol", "knife", "shotgun", "revolver", "firearm", "firearms", "SMG", "AR", "sawnoff", "sawn off", "sawn-off", "machine gun", "doublebarrel", "doublebarreled", "double-barrel", "double-barreled", "bolt-action", "bolt-action", "lever-action", "lever action", "pump-action", "semi-automatic",  "semiautomatic", "fully automatic", "ar-15", "ar15", "AK-47", "M4", "M16", "remington", "glock", "sig", "springfield", "ruger", "Smith & Wesson", "S&W", "M&P", "Colt", "Winchester", "benelli", "M&P15", "kel-tec", "KSG", "590", "870", "LE6920", "AR-556", "G19", "85", "taurus", "629", ".85", ".45", ".22", "22", "9mm", "9 mm", ".30", "beretta", ".50", "50cal", "50 cal", "bushmaster", "M1911", "12 gauge", "12gauge", "12ga","geissele", "chamber a round" , "ammo", "ammunition", "caliber", "gauge", "magazine", "buck shot", "buckshot", "armor-piercing", "hollow point", "hollow points","birdshot", "bird shot", "gun range", "rifle club", "shooting pracitice", "shooting range", "firearms training ", "hunting", "duck shooting", "target shooting", "target pracitice", "scope", "silencer", "suppressor", "compensator","stock", "barrel", "muzzle", "bipod", "firing pin", "optics", "crossbow", "compound bow", "pipe bomb", "pipebomb", "pipe-bomb", "pipebombs", "pipe-bombs", "grenade", "grenades", "IED", "improvised explosive device", "ball bearings", "molotov", "nitrate", "TNT", "landmine", "firebomb", "tannerite", "semtex", "fertilizer", "detonater", "detornaters", "nitroglycerin", "ammonium nitrate", "propellant", "thermalite", "thermite", "blasting cap", "det cord", "detcord", "boom stick", "fire bomb", "explosives", "kevlar", "body armour", "stab-proof vest", "stabproof vest",]
    target_phrase_list3 = ["will k*ll", "to k*ll", "will kill", "to kill", "should kill", "fucking kill", "be killed", "get killed", "will murder", "to murder", "should murder", "fucking murder", "be murdered", "get murdered", "will execute", "should execute", "to execute", "fucking execute", "be executed", "get executed", "to sh00t", "should shoot", "will shoot", "to shoot", "fucking shoot", "be shot", "get shot", "should stab", "will stab", "to stab", "fucking stab", "be stabbed", "get stabbed", "to rape", "will rape", "should rape", "get raped", "be raped", "execute them", "hang them", "be hung", "should hang", "fucking head", "fucking neck", "fucking throat", "fucking skull", "be hanged", "be exterminated", "and kill", "you to death", "him to death", "her to death", "them to death", "gut you", "gut him", "gut her", "gut them", "to gut", "rag doll", "ragdoll", "rag dolled", "ragdolled", "behead", "beheaded", "decapitate", "decapitated", "string them up", "string him up", "string her up", "strung up", "curb stomp", "curb stomped", "in the head", "in the neck", "in the throat", "by the neck", "by the throat", "lynch him", "lynch her", "lynch them", "to lynch", "lynched", "cable ties", "cabled tied", "hogtied", "hog tied", "hog tie", "hogtie", "cable tie", "in the face", "be strangled", "strangle her", "strangle him", "strangle them", "will strangle", "strangle you", "punch you", "punch him", "punch her", "gonna shoot ",  "gonna stab ",  "gonna kill",  "gonna murder",  "gonna execute", "gonnahang", "gonna rape", "tar and feather", "double tap", "my fist", "and kill", "and shoot", "and stab", "and hang", "and lynch", "and murder", "and execute", "and rape", "and gut", "to attack", "should attack", "and attack", "fucking attack", "attack him", "attack her", "attack them", "take hostages", "take a hostage", "to exterminate", "should exterminate", "and exterminate", "fucking exterminate", "exterminate him", "exterminate her", "exterminate them", "be exterminated", "to slaughter", "should slaughter", "and slaughter", "fucking slaughter", "slaughter him", "slaughter her", "slaughter them", "be slaughtered", "to die"]

    # Get the target username from the user
    target_username = input("Enter the target username (with @): ")

    # Run the extraction and PDF generation
    extract_sentences(target_username, "input.csv", target_username + "_threat_assessment.pdf", target_phrase_list1, target_phrase_list2, target_phrase_list3)

    # Ask if the user wants to return to the launcher
    launcher = input('Do you want to return to the launcher? (y/n)')
    if launcher == 'y':
        print('Restarting...')
        exec(open("launcher.py").read())
