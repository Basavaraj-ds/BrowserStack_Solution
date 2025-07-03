
from typing import List
from utils.Idata import ArticleObject
from collections import Counter


def count_words(sample_data:List[ArticleObject]):

    words = []

    for cnt in range(len(sample_data)):
        words.extend(sample_data[cnt].eng_title.split(" "))

    dict = Counter(words)

    for k,v in dict.items():
        if v>2:
            print(f"{k}:{v}")