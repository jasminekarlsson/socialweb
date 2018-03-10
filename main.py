import getData
# import evaluation
# import matrix
import similar

# reviews = getData.getReviews()
# train_reviews = reviews['trainData']
# test_reviews = reviews['testData']

simArrays = similar.getSimilarity()
user1 = simArrays[0]
user2 = simArrays[1]
similarity = simArrays[2]
# for i in range(0, len(user1)):
#     print "Users: " + user1[i] + " and " + user2[i] + " has similarity " + str(similarity[i])


# TODO compute similarities matrix
matrix = None

# evaluation.evaluate(matrix, train_reviews, test_reviews)
