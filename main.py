import getData
import evaluation
import matrix

reviews = getData.getReviews()
print 'Got data'
train_reviews = reviews[1]
test_reviews = reviews[0]

# TODO compute similarities matrix
matrix = matrix.Matrix(100000, 10000)


evaluation.evaluate(matrix, train_reviews, test_reviews)
