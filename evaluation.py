import MySQLdb
from statistics import mean
import math
import matplotlib.pyplot as plt

import getData

def arithmeticalAvg(review, allReviews):
    business_id = review['business_id']
    return statistics.mean([ r['stars']
        for r in allReviews
            if (r['business_id'] == business_id and r['id'] != review['id']) ])

def weightedAvg(review, allReviews, matrix):
    business_id = review['business_id']
    testUser = review['user_id']
    weightedSum = 0
    totalWeight = 0
    for r in allReviews:
        if r['business_id'] == business_id and r['id'] != review['id']:
            otherUser = r['user_id']
            weight = matrix.getWeight(testUser, otherUser)
            # TODO: how to manage null similarities? They should still influence the average
            if weight:
                weightedSum = weightedSum + (weight * r['stars'])
                totalWeight = totalWeight + weight
    return weightedSum / totalWeight

def plotPie(nUnderThreshold, nAboveThreshold, nBetweenTresholds, title):
    # Data to plot
    labels = '|avg - rate| < ' + str(minTreshold), '|avg - rate| >= ' + str(threshold), str(minTreshold) + ' < |avg - rate| < ' + str(threshold)
    sizes = [ nUnderThreshold, nAboveThreshold, nBetweenTresholds]
    colors = ['xkcd:green', 'xkcd:tomato', 'xkcd:yellow']
    explode = (0.1, 0, 0)  # explode 1st slice
    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)

    plt.axis('equal')
    plt.title(title)
    plt.show()

def evaluate(matrix, trainingData, testData):
    allReviews = testData + trainingData

    ARnAboveThreshold = 0
    ARnBetweenTresholds = 0
    ARdiffs = []
    WEnAboveThreshold = 0
    WEnBetweenTresholds = 0
    WEdiffs = []

    for review in testData:
        # TODO check how they are stored
        stars = review['stars']

        # compute the arithmetical average of the considered business
        review['arithmeticalAvg'] = arithmeticalAvg(review, allReviews)
        # compute the weighted average of the considered business
        review['weightedAvg'] = weightedAvg(review, allReviews, matrix)
        # compute the difference between the aritmethical average and the review
        review['arithemticalDiff'] = stars - review['arithmeticalAvg']
        ARdiffs.append(review['arithemticalDiff'])
        # compute the difference between the weighted average and the review
        review['weightedDiff'] = stars - review['weightedAvg']
        WEdiffs.append(review['weightedDiff'])
        # increase counter of the difference category
        # for the arithmetical setting
        if abs(review['arithmeticalDiff']) >= threshold:
            ARnAboveThreshold = ARnAboveThreshold + 1
        else:
           if abs(review['arithmeticalDiff']) > minTreshold:
               ARnBetweenTresholds =  ARnBetweenTresholds + 1
        # for the weighted setting
        if abs(review['weightedDiff']) >= threshold:
            WEnAboveThreshold = WEnAboveThreshold + 1
        else:
           if abs(review['weightedDiff']) > minTreshold:
               WEnBetweenTresholds = WEnBetweenTresholds + 1

    # Compute Errors
    samples = len(testData)
    ARnUnderThreshold = samples - ARnAboveThreshold - ARnBetweenTresholds
    WEnUnderThreshold = samples - WEnAboveThreshold - WEnBetweenTresholds
    ARrmse = computeRMSE(ARdiffs, samples)
    ARmae = computeMAE(ARdiffs, samples)
    WErmse = computeRMSE(WEdiffs, samples)
    WEmae = computeMAE(WEdiffs, samples)
    print '######### ARITHMETICAL #############'
    print 'RMSE:', ARrmse
    print 'MAE:', ARmae
    print '######### WEIGHTED #############'
    print 'RMSE:', WErmse
    print 'MAE:', WEmae

    # Plot pie charts
    plotPie(ARnUnderThreshold, ARnAboveThreshold, ARnBetweenTresholds, 'Arithmetical')
    plotPie(WEnUnderThreshold, WEnAboveThreshold, WEnBetweenTresholds, 'Weighted')