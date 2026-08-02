import re
import pdfplumber

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    stop_words = {
        "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
        "had", "has", "have", "he", "her", "here", "hers", "him", "his", "i",
        "in", "into", "is", "it", "its", "me", "my", "of", "on", "or", "our",
        "ours", "she", "that", "the", "their", "them", "there", "these", "they",
        "this", "those", "to", "was", "were", "what", "when", "where", "which",
        "who", "whom", "why", "will", "with", "you", "your", "yours", "can",
        "could", "should", "would", "do", "does", "did", "not", "no", "so",
        "such", "very", "than", "then", "too", "also", "all", "any", "both",
        "each", "few", "more", "most", "some", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine", "ten"
    }

# --------------------------------------------------
# Extract Text
# --------------------------------------------------

def extract_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    text = ""
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
    text = str(text or "").lower()

    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"\+?\d[\d\s\-\(\)]{8,}\d", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    words = []
    for word in text.split():
        if word not in stop_words:
            words.append(stemmer.stem(word))

    return " ".join(words)

# --------------------------------------------------
# Skill Extraction
# --------------------------------------------------

SKILLS = [
    "python", "java", "c++", "sql", "excel",
    "machine learning", "deep learning",
    "tensorflow", "keras", "pytorch",
    "react", "node", "django", "flask",
    "html", "css", "javascript",
    "mongodb", "mysql", "postgresql",
    "power bi", "tableau", "aws", "azure",
    "git", "docker", "linux"
]

def extract_skills(text):
    text = str(text or "").lower()
    found = []

    for skill in SKILLS:
        if skill.lower() in text:
            found.append(skill)

    return sorted(set(found))