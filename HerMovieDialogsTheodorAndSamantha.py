import requests
from bs4 import BeautifulSoup
import json, re

# Step 1: Load the web page content
url = 'https://imsdb.com/scripts/Her.html'
response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

preTag = soup.find("pre")
conversationToText = preTag.text
cleaned_text = re.sub(r"<b>\s*(\(MORE\)|\(CONTINUED\)|CONTINUED:)\s*</b>", "", conversationToText)
cleaned_text = re.sub(r"Her\s+pg\.\s+\d+", "", cleaned_text)
cleaned_text = cleaned_text.replace("<b>                         (MORE)</b>", "") \
                   .replace("<b>                                                     (CONTINUED)</b>", "") \
                   .replace("<b>   CONTINUED:</b>", "") \
                    .replace("(CONTINUED)", "")\
    .replace("CONTINUED:", "")\
    .replace("<b>   CONTINUED: (4)</b>", "")\
    .replace("CONTINUED: (3)", "")\
    .replace("CONTINUED: (2)", "")\
    .replace("CONTINUED: (1)", "")\
    .replace("                         "
             "", " ")\
    .replace("               ", " ")

# Düzenli ifadeyle diyalogları bulma
pattern = r"(THEODORE|SAMANTHA)(.*?)(?=\n\s*(THEODORE|SAMANTHA|$))"

# Düzenli ifadeyi kullanarak konuşmaları bulma
matches = re.findall(pattern, cleaned_text, re.DOTALL)

# Konuşmaları işleme ve soru-cevap çiftlerini oluşturma
qa_pairs = []
for i in range(len(matches)-1):
    # Eşleşmeleri kontrol etme ve soru-cevap çiftlerini doldurma
    if matches[i][0] == "THEODORE" and matches[i+1][0] == "SAMANTHA":
        question = matches[i][1].strip()
        answer = matches[i+1][1].strip()
        qa_pairs.append({"question": question, "answer": answer})

# JSON'a dönüştürme
qa_json = json.dumps(qa_pairs, indent=4, ensure_ascii=False)

print(qa_json)