from nltk.corpus import stopwords
import re
stopwrds = stopwords.words('english')


def preprocess_text(text:str) -> str:
    text = text.lower()
    text = [t for t in re.findall('\w+',text) if t not in stopwrds ]
    text = [t for t in text if len(t) > 1]
    return " ".join(text)