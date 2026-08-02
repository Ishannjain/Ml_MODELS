import re
import pdfplumber

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

stop_words = set(stopwords.words("english"))

# --------------------------------------------------
# Extract Text
# --------------------------------------------------

def extract_text(file):

    if file.name.endswith(".txt"):

        return file.read().decode("utf-8")

    text=""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

    return text

# --------------------------------------------------
# Cleaning
# --------------------------------------------------

def clean_resume(text):

    text=text.lower()

    text=re.sub(r"http\S+"," ",text)

    text=re.sub(r"\S+@\S+"," ",text)

    text=re.sub(r"\+?\d[\d\s\-\(\)]{8,}\d"," ",text)

    text=re.sub(r"<.*?>"," ",text)

    text=re.sub(r"[^a-zA-Z\s]"," ",text)

    text=re.sub(r"\s+"," ",text)

    words=[]

    for word in text.split():

        if word not in stop_words:

            words.append(

                stemmer.stem(word)

            )

    return " ".join(words)

# --------------------------------------------------
# Skill Extraction
# --------------------------------------------------

SKILLS=[

"python","java","c++","sql","excel",

"machine learning","deep learning",

"tensorflow","keras","pytorch",

"react","node","django","flask",

"html","css","javascript",

"mongodb","mysql","postgresql",

"power bi","tableau","aws","azure",

"git","docker","linux"

]

def extract_skills(text):

    text=text.lower()

    found=[]

    for skill in SKILLS:

        if skill.lower() in text:

            found.append(skill)

    return sorted(set(found))