from utils.Idata import article, sample_data
from utils.counter import count_words
import asyncio
from utils.translate import translate_text


def main():
    for cnt in range(len(sample_data)):
        # translate the spanish titles to english
        sample_data[cnt].eng_title = asyncio.run(translate_text(sample_data[cnt].title))

    # run the counter function to print the words repeated more than twice
    count_words(sample_data=sample_data)


if __name__ == "__main__":
    main()
