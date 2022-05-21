import requests
from bs4 import BeautifulSoup

# request the page and create soup object
def get_page(url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
    }

    captcha_page = True
    while captcha_page:

        html = requests.get(url, headers)

        if html.status_code == 200:
            captcha_page = False
            soup = BeautifulSoup(html.text, "html.parser")
        else:
            print("captcha page")

    return soup


# from soup get list of reviews
def parse_reviews(soup):

    review_cards = soup.find_all("div", class_="a-section review aok-relative")
    print(review_cards)


if __name__ == "__main__":

    soup = get_page(
        "https://www.amazon.co.uk/product-reviews/B095BHVJ3Z/ref=cm_cr_othr_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    )

    # print(soup)

    parse_reviews(soup)
