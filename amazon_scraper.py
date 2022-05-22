from urllib.parse import urlparse
import sys
import csv
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

    def to_list(self):
        return [self.profile, self.title, self.stars, self.review]


# request the page and create soup object from html
def get_page_html(url):

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


# from soup return a list of individual review objects
def parse_reviews(soup):

    review_list = []
    review_cards = soup.find_all("div", class_="a-section review aok-relative")
    # print(len(review_cards))

    # pull data from each review card and use it to create review object
    for review in review_cards:

        """print(review.prettify())
        print()"""

        profile = review.find_all("a", class_="a-profile")[0]["href"]
        # print(profile)

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


# check for a next page button and return href, return empty string if none
def get_next_page_href(soup):

    next_page_href = ""
    nav_buttons = soup.find_all("ul", class_="a-pagination")

    # check nav buttons are present on page
    if len(nav_buttons) > 0:
        next_page_button = nav_buttons[0].find_all("li", class_="a-last")[0]

        if "a-diabled" not in next_page_button.get("class"):
            next_page_href = next_page_button.find_all("a")[0]["href"]
            next_page_href = "https://www.amazon.co.uk" + next_page_href

    print("next page href : ", next_page_href)
    return next_page_href


def check_url(url):

    valid = True
    parsed = urlparse(url)

    if parsed.netloc != "www.amazon.co.uk":
        print("url is not an amazon page")
        valid = False

    elif "/product-reviews/" not in parsed.path:
        print("url is not a product review page")
        valid = False

    return valid


# get product reviews from each page up to page 5
def get_reviews(url):

    all_reviews = []

    if check_url(url):
        next_page = url
        page_count = 1

        # check there is a next page and not past page 5
        while next_page != "" and page_count <= 5:

            soup = get_page_html(next_page)
            print("page ", page_count)
            page_reviews = parse_reviews(soup)
            all_reviews += page_reviews

            next_page = get_next_page_href(soup)
            page_count += 1

            print("next page")
    else:
        print("invalid url")

    return all_reviews


# write the data from a list of reviews to a csv file
def write_reviews(review_list):

    with open("reviews.csv", "w") as review_file:

        writer = csv.writer(review_file)

        header = ["profile", "title", "stars", "review"]
        writer.writerow(header)

        for review in review_list:
            writer.writerow(review.to_list())


if __name__ == "__main__":

    url = ""

    # check for url in arguments, give example if none
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "https://www.amazon.co.uk/Dark-Tower-II-Drawing-Three/product-reviews/B008BJ5FNE/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"

    reviews = get_reviews(url)

    print(len(reviews), "reviews scraped")

    write_reviews(reviews)  # write reviews to csv