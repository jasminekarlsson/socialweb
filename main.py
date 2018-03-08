import getData
import evaluation
import matrix

reviews = getData.getReviews()
train_reviews = reviews['trainData']
test_reviews = reviews['testData']

# TODO compute similarities matrix
matrix = None

evaluation.evaluate(matrix, train_reviews, test_reviews)
