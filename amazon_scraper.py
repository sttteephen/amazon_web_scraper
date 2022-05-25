from nltk.sentiment import SentimentIntensityAnalyzer
from urllib.parse import urlparse
import sys
import argparse
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


# request the pages html and create the soup to be parsed
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


# from soup return a list of review objects
def parse_reviews(soup):

    review_list = []
    review_divs = soup.find_all("div", class_="a-section review aok-relative")

    # flag indicating if reviews from other countries start on this page
    last_uk_review = False

    # pull data from each review div and use it to create review object
    for review in review_divs:

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

        # check if this is the last uk review
        if (
            # check review.next_sibling.next_sibling exists
            review.next_sibling
            and review.next_sibling.next_sibling
            and review.next_sibling.next_sibling.text
        ):
            # check if it is the start of non uk reviews
            if review.next_sibling.next_sibling.text.strip() == "From other countries":
                # if so stop parsing reviews
                last_uk_review = True
                break

    return (review_list, last_uk_review)


# checks there is an active next page button on page and returns next pages href
def get_next_page_href(soup):

    next_page_href = ""
    nav_buttons = soup.find_all("ul", class_="a-pagination")

    # check nav buttons are present on page
    if len(nav_buttons) > 0:
        next_page_button = nav_buttons[0].find_all("li", class_="a-last")[0]

        # check next button is not disabled
        if "a-disabled" not in next_page_button.get("class"):
            next_page_href = next_page_button.find_all("a")[0]["href"]
            next_page_href = "https://www.amazon.co.uk" + next_page_href

    print("next page href : ", next_page_href)
    return next_page_href


# validate the given url is an amazon product review page
def check_url(url):

    valid = True
    parsed_url = urlparse(url)

    # check url is and amazon page
    if parsed_url.netloc != "www.amazon.co.uk":
        print("url is not an amazon page")
        valid = False

    # check url is a product review page
    elif "/product-reviews/" not in parsed_url.path:
        print("url is not a product review page")
        valid = False

    return valid


# get product reviews from multiple pages up to given page depth
def get_reviews(url, page_depth):

    all_reviews = []
    next_page = url
    page_count = 1

    # check there is a next page and not past max page depth
    while next_page != "" and page_count <= page_depth:

        soup = get_page_html(next_page)
        print("parsing page ", page_count)

        page_reviews, last_uk_review = parse_reviews(soup)
        all_reviews += page_reviews

        if last_uk_review:
            next_page = ""
        else:
            next_page = get_next_page_href(soup)
            page_count += 1

    print(len(all_reviews), " reviews parsed")
    return all_reviews


# write the data from a list of reviews and the reviews sentiment score to a csv file
def write_reviews(review_list):

    sia = SentimentIntensityAnalyzer()

    with open("reviews.csv", "w") as review_file:

        writer = csv.writer(review_file)

        header = ["profile", "title", "stars", "review"]
        writer.writerow(header)

        for review in review_list:
            # get list of data from review object and append sentiment score
            review_data = review.to_list()
            review_score = sia.polarity_scores(review_data[3])["compound"]
            review_data.append(review_score)

            writer.writerow(review_data)


# gets the values for url and page depth to be scraped if arguments have been given at command line
def get_script_args():

    # default values for url and depth
    url = "https://www.amazon.co.uk/Dark-Tower-II-Drawing-Three/product-reviews/B008BJ5FNE/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    depth = 5

    # create valid options
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--url",
        help="url of the amazon review page to be scraped, must be given inside inverted commas",
    )
    parser.add_argument(
        "-d", "--depth", help="the number of pages to be scraped", type=int
    )

    args = parser.parse_args()

    # check options have been given and store their values
    if args.url:
        url = args.url

    if args.depth:
        depth = args.depth

    return (url, depth)


def run():

    url, page_depth = get_script_args()

    if check_url(url):

        # get a list of reviews from the given url up to the given page depth
        reviews = get_reviews(url, page_depth)

        write_reviews(reviews)  # write reviews to csv

    else:

        print("invalid url")


if __name__ == "__main__":

    run()
