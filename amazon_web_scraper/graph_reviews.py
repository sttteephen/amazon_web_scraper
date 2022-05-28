import matplotlib.pyplot as plt
import numpy as np
import csv


def graph():

    # the sentiment score from each individual review will be added to list with it's related star rating
    sentiment_dict = {1: [], 2: [], 3: [], 4: [], 5: []}

    with open("reviews.csv", "r") as reviews_file:

        csv_reader = csv.reader(reviews_file, delimiter=",")
        next(csv_reader, None)

        for row in csv_reader:
            # print(row)

            sentiment_dict[int(row[2])].append(float(row[4]))

    x_values = []
    y_values = []

    # iterate through dictionary in acending rating order
    for rating in sorted(sentiment_dict.keys()):

        # if there is scores for that rating append rating to x and average sentiment score to y
        if len(sentiment_dict[rating]) > 0:
            x_values.append(rating)
            # calculate average sentiment score for given rating
            y_values.append(sum(sentiment_dict[rating]) / len(sentiment_dict[rating]))

    # plot sentiment score graph
    x = np.array(x_values)
    y = np.array(y_values)

    plt.subplot(1, 2, 1)
    plt.barh(x, y)
    plt.ylabel("Star Rating")
    plt.xlabel("Average Sentiment Score")
    plt.title("Ratings Sentiment")

    x_values = []
    y_values = []
    # iterate through dictionary in acending rating order
    for rating in sorted(sentiment_dict.keys()):

        # append rating to x and the amount of ratings to y
        x_values.append(rating)
        y_values.append(len(sentiment_dict[rating]))

    # plot ratings graph
    x = np.array(x_values)
    y = np.array(y_values)

    plt.subplot(1, 2, 2)
    plt.barh(x, y)
    plt.ylabel("Star Rating")
    plt.xlabel("Number of Ratings")
    plt.title("Ratings Data")

    plt.show()


if __name__ == "__main__":

    graph()
