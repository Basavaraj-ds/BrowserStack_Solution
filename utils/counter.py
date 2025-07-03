
from typing import List
from utils.Idata import ArticleObject
from collections import Counter
import re

def clean_text(Article_Object: ArticleObject):
    text = Article_Object.eng_title
    text = text.lower()
    text = re.sub('[^a-zA-Z0-9 \n\.]', '', text)
    words_list = text.split(" ")
    return words_list

def count_words(ArticleList:List[ArticleObject]):

    words = []

    for cnt in range(len(ArticleList)):
        words.extend(clean_text(ArticleList[cnt]))

    dict = Counter(words)

    for k,v in dict.items():
        if v>0:
            print(f"{k}:{v}")