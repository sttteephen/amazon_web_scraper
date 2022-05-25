# Amazon Review Web Scraper

This is a web scraper built using Python and  Beautiful Soup. It scrapes reviews from an amazon review page, performs sentiment analysis on the review content using the NLTK module and saves the data to a csv file.

## Usage 

Certain optional arguments can be passed to the program: 

-u, --url       should be followed by the url of an Amazon review page which must be given inside inverted commas.

-d, --depth     should be followed by the number of reviews pages to be scraped.

If not passed a url the program will scrape an example page and if not passed a depth it will default to 5 pages.

## Build from Source

The program was built using Python 3.8.5. It can be run with the following command:

```bash
 $ python3 amazon_review.py -u <url> -d <depth>
