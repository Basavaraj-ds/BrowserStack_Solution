from utils.Idata import ArticleObject
from utils.counter import count_words
import asyncio
from utils.translate import translate_text
from utils.web_scrapping import  run_web_scrapping


def main():
    processed_articles = run_web_scrapping()


    for cnt in range(len(processed_articles)):
        # translate the spanish titles to english
        processed_articles[cnt].eng_title = asyncio.run(translate_text(processed_articles[cnt].title))

    print(processed_articles)

    # run the counter function to print the words repeated more than twice
    #count_words(processed_articles)


if __name__ == "__main__":
    main()
