from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt


def scrape_all():

    page = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(page)

    # Run all scraping functions and store in dictionary.
    data = {
        "title": title,
    }

    # Stop webdriver and return data
    page.quit()
    return data


def news(page):
    url = "https://mars.nasa.gov/news/"
    page.visit(url)

    page.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)

    html = page.html
    news = BeautifulSoup(html, "html.parser")

    try:
        slide_elem = news.select_one("ul.item_list li.slide")
        title = slide_elem.find("div", class_="content_title").get_text()
        news_page = slide_elem.find(
            "div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return title, news_page


def featured_image(page):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    page.visit(url)

    full_img = page.find_by_id("full_image")
    full_img.click()

    page.is_element_present_by_text("more info", wait_time=0.5)
    more_info = page.find_link_by_partial_text("more info")
    more_info.click()

    html = page.html
    img_soup = BeautifulSoup(html, "html.parser")

    img = img_soup.select_one("figure.lede a img")

    try:
        img_url_rel = img.get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f"https://www.jpl.nasa.gov{img_url_rel}"

    return img_url



if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())