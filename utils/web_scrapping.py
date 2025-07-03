from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import os
import time
from utils.Idata import ArticleObject

"""
1.Visit the website El País, a Spanish news outlet.
    Ensure that the website's text is displayed in Spanish.
"""
driver=webdriver.Chrome()
driver.get("https://elpais.com/us/")
spanish_text = driver.find_element(By.TAG_NAME, "body").text
print("Page Text:\n")
print(spanish_text)

driver.get("https://elpais.com/opinion/")
driver.maximize_window()



BASE_URL = "https://elpais.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
}
IMAGE_FOLDER = "images"

def fetch_opinion_articles():
    url = f"{BASE_URL}/opinion/"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    articles = []
    seen_urls = set()

    article_links = soup.select("article a")
    for a in article_links:
        href = a.get("href")
        title = a.get_text(strip=True)
        if href and title:
            full_url = href if href.startswith("http") else BASE_URL + href
            if full_url not in seen_urls:
                seen_urls.add(full_url)
                articles.append({"title": title, "url": full_url})
        if len(articles) == 5:
            break

    return articles

def fetch_article_content_and_image(article_url):
    resp = requests.get(article_url, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Extract article content
    content_div = soup.find("div", {"data-testid": "article-body"})
    content = ""
    if content_div:
        paragraphs = content_div.find_all("p")
        content = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

    # Extract cover image URL
    image_url = None
    figure = soup.find("figure")
    if figure:
        img = figure.find("img")
        if img and img.has_attr("src"):
            image_url = img["src"]

    # Fallback to Open Graph meta image
    if not image_url:
        meta_img = soup.find("meta", property="og:image")
        if meta_img and meta_img.has_attr("content"):
            image_url = meta_img["content"]

    return content, image_url

def save_image(image_url, folder, filename):
    if not image_url:
        return None
    try:
        os.makedirs(folder, exist_ok=True)
        response = requests.get(image_url, headers=HEADERS)
        response.raise_for_status()
        ext = os.path.splitext(image_url)[1].split("?")[0]
        if ext.lower() not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
            ext = ".jpg"

        filepath = os.path.join(folder, f"{filename}{ext}")
        with open(filepath, "wb") as f:
            f.write(response.content)
        return filepath
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).rstrip()

def run_web_scrapping():
    print("🔍 Fetching first 5 opinion articles from El País...\n")
    articles = fetch_opinion_articles()

    processed_articles = []

    for idx, article in enumerate(articles, 1):
        print(f"\n{'='*80}\n")
        print(f"📰 Artículo {idx} - Título: {article['title']}\n")
        processed_articles.append(ArticleObject(title=article["title"]))

        content = article["url"]
        content, image_url = fetch_article_content_and_image(article["url"])

        if content:
            print(content)
        else:
            print("⚠️ No se pudo obtener el contenido del artículo.")

        if image_url:
            filename = sanitize_filename(article['title'])[:50]
            saved_path = save_image(image_url, IMAGE_FOLDER, filename)
            if saved_path:
                print(f"\n📷 Imagen de portada guardada en: {saved_path}")
            else:
                print("\n⚠️ No se pudo descargar la imagen de portada.")
        else:
            print("\n⚠️ No se encontró imagen de portada.")

        time.sleep(2)  # Be polite with the server
    return processed_articles

