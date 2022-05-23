from nltk.sentiment import SentimentIntensityAnalyzer
import csv

sia = SentimentIntensityAnalyzer()

with open("reviews.csv") as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0

    for row in csv_reader:

        if line_count == 0:
            pass
        else:
            print(row[2], " ", sia.polarity_scores(row[3])["compound"])

        line_count += 1
