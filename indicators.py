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

def extract_sentences(username, input_csv, output_pdf, target_phrase_sections):
    username = username.strip("@")  # Remove "@" symbol from username

    input_csv_path = f"Collection/{username}/{username}_messages.csv"

    output_pdf_path = f"Collection/{username}/{username}__ideologicalindicators_report.pdf"

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

    normal_style.alignment = 0  # Left alignment

    citation_style = ParagraphStyle(name='CitationStyle', parent=normal_style)

    citation_style.leading = 6  # Decrease font size to 6   

    # Add the title to the PDF

    title = Paragraph("Ideological Indicators Report", title_style)

    story = [title, Spacer(1, 12)]
    # Iterate through target phrase sections

    for section_title, target_phrases in target_phrase_sections:

        # Add sub-heading for the section

        section_heading = Paragraph(section_title, subheading_style)

        story.extend((section_heading, Spacer(1, 12)))
        # Create a regex pattern for each target phrase

        target_patterns = [re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE) for phrase in target_phrases]

        # Iterate through messages and extract sentences

        for index, row in df.iterrows():

            message = str(row['Text'])  # Convert to string to handle non-string values

            url = row['Message URL']  # Get the source URL

            sentences = re.split(r'(?<=[.!?])\s+', message)

            for sentence in sentences:

                for pattern in target_patterns:

                    if re.search(pattern, sentence):
                        # Highlight target phrases

                        highlighted_sentence = re.sub(pattern, r'<font color="red">\g<0></font>', sentence)

                        story.extend((Paragraph(highlighted_sentence, normal_style), Spacer(1, 12)))
                        # Add URL end-note citation with size 6 font and bold "Source:"

                        citation = Paragraph(f"<font size='6'><b>Source:</b> <a href='{url}'>{url}</a></font>",
                                             normal_style)

                        story.extend((citation, Spacer(1, 12)))
    # Create the PDF

    doc.build(story)

    print(f"Key phrase extraction report saved to {output_pdf_path}")


if __name__ == "__main__":
    # Define five different target phrase sections with sub-headings

    target_phrase_sections = [

        ("Racism/Hate Speech", [

            "moslem", "mulatto", "sand nigger", "sandnig", "nigger", "mogger", "negroid", "jew", "kike", "zogbot",
            "chink", "paki", "mudslime", "mudshit", "femoid", "foid", "mongrel",

            "towel 	head", "towelhead", "moslems", "mulattos", "muzzies", "sand niggers", "sandnigs", "shit skin",
            "shitskin", "niggers", "moggers", "negroids", "jews", "kikes", "zogbots",

            "chinks", "pakis", "mudslimes", "mudshits", "femoids", "mongrels", "towel heads", "towelheads", "spics",
            "gooks", "rapefugees", "shitskins", "fag", "fags", "faggot", "faggots",

            "groomer", "groomers", "tranny", "trannys", "jewish", "(((", "Gibsmedat", "Goy", "soyboy", "gibs",
            "soyboys",

        ]),

        ("Indicators - White Identity Motivated Extremism", [

            # List of target phrases for section 2

            "white genocide", "cultural marxism", "cultural marxists", "the great replacement", "white race",
            "demographic replacement", "demographic decline", "anti-Zionist",

            "#WhiteLivesMatter", "white lives matter", "white pride", "ethnostate", "hitler", "Tarrant", "brevik",
            "white nationalist", "ethno-nationalist", "kebab removalist", "remove kebab",

            "remove kebabs", "Aryan", "1488", "14-88", "14/88", "1788", "88/HH", "blood and soil", "RACE WAR NOW",
            "RaHoWa", "Racial Holy War", "FGRN", "GTKRWN", "IOTBW", "jewish question",

            "accelerate", "accelerationist", "sieg heil", "siege pill", "siege pilled", "white power", "goyim",
            "zyklon B", "14 words", "race traitors", "race traitor", "day of the rope",

            "waffen", "iron pill", "iron pilled", "ZOG", "Z.O.G.", "terrorgram", "national socialist",
            "national socialism", "⚡", "//", "Khazarian", "Ashkenazis",

            "tradwife", "tradthot", "cultural jihad", "pro western values", "pro-western values", "western culture",
            "kek", "deus vault", "did nothing wrong", "its okay to be white",

            "it's okay to be white", "it's ok to be white", "white is right", "pro-white activism", "coal burner",
            "race traitor", "race traitors", "6MWNE", "Holocauster", "Holohoax",

            "Clown World", "🤡🌎", "Accelerationist", "James Mason", "Accelerationism",

        ]),

        ("Indicators - Faith Motivated Extremism", [

            # List of target phrases for section 2

            "جهاد", "جهاد", "مرتد", "المرتدين", "الطغاة", "التحالف الصليبي", "جنود الخلافة", "أسود الدولة الإسلامية",
            "في ظل الخلافة", "تقبل الله الله", "المنهجية المؤيدة للفيتيك", "المنهج النبوي", "المتبقية والتوسع",
            "موسوعة الجهاد", "دليل المجاهد", "رفيدة", "الدولة الإسلامية", "الخلافة الإسلاميةروافيض", "استيشادي",
            "باقية من تاتاداد", "التواغيت", "الشريعة",

            "Jihad", "holy war", "apostate", "the apostates", "tyrants", "the crusader coalition",
            "soldiers of the caliphate", "lions of the Islamic State", "in the shadow of the caliphate",

            "may God accept him", "the prophetic methodology", "the prophetic methodology", "Remaining and Expanding",
            "The encyclopedia of Jihad", "The Mujahad’s Handbook", "Rafidha", "Rawafidh",

            "Istishaadi", "Baqiya wa tatamaddad", "al-Tawaghit", "shariyah", "A’maq Agency", "Al-hayat", "al-Emarah",
            "Dabiq",

        ]),

        ("Indicators - Conspiratorial Ideation", [

            "great awakening", "globalist", "globalists", "new world order", "WWG1WGA", "the storm", "chemtrails",
            "freemasons", "freemason", "illuminati", "deep state", "the storm",

            "adrenochrome", "cabal", "rothschilds", "nuremberg", "nuremburg", "crimes against humanity", "great reset",
            "agenda 2030", "agenda 21", "world economic forum", "false flag",

            "Microchipped", "microchips", "pizzagate", "sheeple", "geotus",

        ]),

        ("Indicators - Sovereign Citizen", [

            "sovreign citizen", "sovereign citizen", "free man", "free woman", "flesh and blood", "common law",
            "admiralty law", "non-resident alien", "14th amendment", "legal fiction",

            "notice of understanding and intent", "affidavit of truth", "Birth Certificate Bond",
            "Non-Domiciled Resident", "Natural Law", "Freeman Passport", "Constitutional Sheriff",

            "Nontaxpayer", "Informed Consent", "Commercial Redemption", "Freemen Standby Act", "strawman",
            "man on the land", "non-resident alien", "in admiralty",

            "living soul", "letters of marque", "Settlor", "Quantam Grammar", "Quantum Grammar", "Strawman",
            "Magna Carta", "Maritime Law", "Policy Officer", "Postmaster",

            "Artifical Construct", "Artificial Construct", "Lawful Dissent", "In the Private", "living man",
            "living woman", "Maxim of Law", "Uniform Commercial Code", "Corpus Juris", "Sui Juris",

        ]),

        ("Indicators - Involuntary Celibate", [

            "foid", "femoid", "dog pill", "dog pilled", "red pill", "red pilled", "going ER", "truecel", "incel",
            "chad", "fakecel", "black pilled", "blackpilled", "ragefuel", "rape fuel",

            "ropefuel", "Supreme Gentleman", "Elliot Rodger", "braincels", "genetically inferior", "roasties", "SMV",
            "Sexual Market Value", "have a little fun bEfoRe you go", "red-pilled",

            "cucks", "Manosphere", "incels", "incel", "Mens Rights Activists", "MGTOW", "Men going their own way",
            "alpha male", "beta male", "omega male", "gamma male",

        ]),

        ("Indicators - Dehumanizing Rhetoric", [

            "parasite", "scum", "demon", "demonic", "soulless", "vermin", "parasites", "mongrel", "mongrels", "leeches",
            "leech", "maggot", "maggots", "parasites", "sub-human",

        ]),

    ]

    # Get the target username from the user

    target_username = input("Enter the target username (with @): ")

    # Run the extraction and PDF generation

    extract_sentences(target_username, "input.csv", target_username + "_ideologicalindicators_report.pdf",
                      target_phrase_sections)

# Ask if the user wants to return to the launcher

launcher = input('Do you want to return to the launcher? (y/n)')

if launcher == 'y':
    print('Restarting...')

    exec(open("launcher.py").read())
