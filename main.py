import getData
import evaluation
import matrix

reviews = getData.getReviews()
train_reviews = reviews[1]
test_reviews = reviews[0]

# TODO compute similarities matrix
matrix = None

evaluation.evaluate(matrix, train_reviews, test_reviews)
