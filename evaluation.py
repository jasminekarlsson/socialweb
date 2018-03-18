from statistics import mean
import math
import matplotlib.pyplot as plt
import getData
import similarity

threshold = 1.5
minThreshold = 0.5

def computeAvg(review, allReviews):
    averages = {}
    business_id = review['business_id']
    testUser = review['user_id']
    weightedSum = 0
    totalWeight = 0
    arithSum = 0.0
    numberReviews = 0.0

    for r in allReviews:
        if r['business_id'] == business_id and r['id'] != review['id']:
            otherUser = r['user_id']
            weight = similarity.simil(testUser, otherUser, allReviews, review)
            arithSum = arithSum + float(r['stars'])
            numberReviews = numberReviews + 1
            if weight:
                weightedSum = weightedSum + (weight * r['stars'])
                totalWeight = totalWeight + weight

    averages['arithmeticalAvg'] = arithSum / numberReviews
    averages['weightedAvg'] = weightedSum / totalWeight
    return averages

def plotPie(nUnderThreshold, nAboveThreshold, nBetweenTresholds, title):
    # Data to plot
    labels = '|avg - rate| <= ' + str(minThreshold), '|avg - rate| >= ' + str(threshold), str(minThreshold) + ' < |avg - rate| < ' + str(threshold)
    sizes = [ nUnderThreshold, nAboveThreshold, nBetweenTresholds]
    colors = ['xkcd:green', 'xkcd:tomato', 'xkcd:yellow']
    explode = (0.1, 0, 0)  # explode 1st slice
    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)

    plt.axis('equal')
    plt.title(title)
    plt.show()

def computeRMSE(errors, samples):
    # RMSE (Root Mean Squared Error): sqrt((sum(power(result - prediction))/n)
    powErrors = [ err**2 for err in errors ]
    return math.sqrt(sum(powErrors) / samples)

def computeMAE(errors, samples):
    # MAE (Mean Absolute Error): sum(abs(result - prediction)) / n
    absErrors = map(abs, errors)
    return sum(absErrors) / samples

def evaluate(trainingData, testData):
    allReviews = testData + trainingData

    ARnAboveThreshold = 0
    ARnBetweenTresholds = 0
    ARdiffs = []
    WEnAboveThreshold = 0
    WEnBetweenTresholds = 0
    WEdiffs = []


    print "####################### Start iterating reviews"
    for review in testData:
        # TODO check how they are stored
        stars = review['stars']

        # compute the arithmetical average of the considered business
        print "Computing averages"
        # compute the arithmetical and weighted averages of the considered business
        averages = computeAvg(review, allReviews)
        print "Averages computed"
        review['arithmeticalAvg'] = averages['arithmeticalAvg']
        review['weightedAvg'] = averages['weightedAvg']
        if review['arithmeticalAvg'] == 0 or review['weightedAvg'] == 0:
            raise Exception('One or both the averages is 0')
        print review['arithmeticalAvg']
        print review['weightedAvg']
        print stars
        # compute the difference between the aritmethical average and the review
        review['arithmeticalDiff'] = stars - review['arithmeticalAvg']
        ARdiffs.append(review['arithmeticalDiff'])
        # compute the difference between the weighted average and the review
        review['weightedDiff'] = stars - review['weightedAvg']
        WEdiffs.append(review['weightedDiff'])
        # increase counter of the difference category
        # for the arithmetical setting
        if abs(review['arithmeticalDiff']) >= threshold:
            ARnAboveThreshold = ARnAboveThreshold + 1
        else:
           if abs(review['arithmeticalDiff']) > minThreshold:
               ARnBetweenTresholds =  ARnBetweenTresholds + 1
        # for the weighted setting
        if abs(review['weightedDiff']) >= threshold:
            WEnAboveThreshold = WEnAboveThreshold + 1
        else:
           if abs(review['weightedDiff']) > minThreshold:
               WEnBetweenTresholds = WEnBetweenTresholds + 1

    print "############################### end iterating reviews"

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
