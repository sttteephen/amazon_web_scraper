import amazon_scraper
import graph_reviews
import argparse
from urllib.parse import urlparse
import sys

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
    parser.add_argument(
        "-g", "--graph", help="create a graph of results", action="store_true"
    )

    args = parser.parse_args()

    # check options have been given and store their values
    if args.url:
        url = args.url

    if args.depth:
        depth = args.depth

    return (url, depth, args.graph)


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


def run_scraper(url, page_depth):

    if check_url(url):

        # get a list of reviews from the given url up to the given page depth
        reviews = amazon_scraper.get_reviews(url, page_depth)

        amazon_scraper.write_reviews(reviews)  # write reviews to csv

    else:

        print("invalid url")


if __name__ == "__main__":

    url, page_depth, graph = get_script_args()
    run_scraper(url, page_depth)

    if graph:
        graph_reviews.graph()
