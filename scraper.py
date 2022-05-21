import requests
from bs4 import BeautifulSoup

# represents an individual review
class AmazonReview:
    def __init__(self, profile, title, stars, review):
        self.profile = profile
        self.title = title
        self.stars = stars
        self.review = review

    def __str__(self):
        return f"Profile: {self.profile}\nTitle: {self.title}\nStars: {self.stars}\nReview: {self.review}"


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

    # repeat request until it doesn't receive captcha page
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

    review_list = []
    review_cards = soup.find_all("div", class_="a-section review aok-relative")
    # print(review_cards)

    for review in review_cards:

        profile = review.find_all("a", class_="a-profile")[0]["href"]

        title = review.find_all(
            "a",
            class_="a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold",
        )[0].text.strip()

        stars = int(review.find_all("i", class_="a-icon-star")[0].parent["title"][0])
        review_str = review.find_all("div", "a-row a-spacing-small review-data")[
            0
        ].text.strip()

        r = AmazonReview(profile, title, stars, review_str)
        review_list.append(r)

    return review_list


if __name__ == "__main__":

    soup = get_page(
        "https://www.amazon.co.uk/product-reviews/B095BHVJ3Z/ref=cm_cr_othr_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    )

    # print(soup)

    reviews = parse_reviews(soup)
    for r in reviews:
        print(r)
        print()
