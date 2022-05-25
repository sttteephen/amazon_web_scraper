import matplotlib.pyplot as plt
import numpy as np
import csv

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

    # if there is data for that rating append rating to x and average sentiment score to y
    if len(sentiment_dict[rating]) > 0:
        x_values.append(rating)
        y_values.append(sum(sentiment_dict[rating]) / len(sentiment_dict[rating]))


x = np.array(x_values)
y = np.array(y_values)

plt.bar(x, y)
plt.show()
