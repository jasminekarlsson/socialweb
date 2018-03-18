import getData

# Scaling factors for the different similarity metrics
a = 0 # DR, average difference in ratings
b = 1 # JS, Jaccard similarity
c = 1 # Fr, frienship between users
d = 1 # sim_distance, similarity distance based on ratings done in hands on session 4

# IMPORTANT: review is the review under test, we cannot use its information to
# infer the similarity measure (as an example, check line 32)
def simil(u1, u2, reviews, reviewUnderTest, friendship):
    # Define a basic value for the similarity. In this way, we always consider
    # a review in the average
    simil = 0.0
    if (a != 0 or d != 0):
        drObj = dr(u1, u2, reviews, reviewUnderTest)
        # Use the average difference in ratings.
        simil = simil + a * drObj['absDiff']
        # use similarity diff of ratings from hands on session 4
        simil = simil + d * drObj['powDiff']
    # Use the Jaccard similarity
    simil = simil + b * js(u1, u2, reviews)
    # Use the friendship
    simil = simil + c * fr(u1, u2,friendship)
    return simil

def dr(u1, u2, reviews, reviewUnderTest):
    # Get the reviews of each user
    u1Reviews = {}
    u2Reviews = {}
    for r in reviews:
        if r['id'] == reviewUnderTest['id']:
            continue
        if r['user_id'] == u1:
            u1Reviews[r['business_id']] = r
        if r['user_id'] == u2:
            u2Reviews[r['business_id']] = r
    # Determine which is the user that reviewed less business, so we can be more
    # efficient in the next loop
    toIterate = {}
    other = {}
    if len(u1Reviews) <= len(u2Reviews):
        toIterate = u1Reviews
        other = u2Reviews
    else:
        toIterate = u2Reviews
        other = u1Reviews

    # Compute the average difference of ratings
    sumDiff = 0.0
    powDiff = 0.0
    n = 0.0
    for key, review in toIterate.iteritems():
        if key in other:
            # The two users reviewed the same business
            diff = float(review['stars']) - float(other[key]['stars'])
            sumDiff = sumDiff + abs(diff)
            powDiff = pow(diff, 2)
            n = n + 1

    dr = {}
    dr['absDiff'] = 0.5
    dr['powDiff'] = 0.5

    if n != 0:
        # DR is between 0 and 4, so we normalize
        # it into [0, 1] dividing by 4. Furthermore, DR is a measure for the distance,
        # so we obtain a similarity measure by computing 1 - DR
        dr['absDiff'] = (1.0 - (sumDiff / (4.0 * n)))
        dr['powDiff'] = 1.0 / (1.0 + powDiff)
    return dr



# Average difference in ratings
# The average of the absolute value of the difference in the reviews made by the
# two users to the same businesses
# def dr(u1, u2, reviews, reviewUnderTest):
#     # Get the reviews of each user
#     u1Reviews = {}
#     u2Reviews = {}
#     for r in reviews:
#         if r['id'] == reviewUnderTest['id']:
#             continue
#         if r['user_id'] == u1:
#             u1Reviews[r['business_id']] = r
#         if r['user_id'] == u2:
#             u2Reviews[r['business_id']] = r
#     # Determine which is the user that reviewed less business, so we can be more
#     # efficient in the next loop
#     toIterate = {}
#     other = {}
#     if len(u1Reviews) <= len(u2Reviews):
#         toIterate = u1Reviews
#         other = u2Reviews
#     else:
#         toIterate = u2Reviews
#         other = u1Reviews
#
#     # Compute the average difference of ratings
#     sumDiff = 0
#     n = 0
#     for key, review in toIterate.iteritems():
#         if key in other:
#             # The two users reviewed the same business
#             sumDiff = sumDiff + abs(review['stars'] - other[key]['stars'])
#             n = n + 1
#
#     if n == 0:
#         # We do not have element to state the similarity, thus we assign a neutral
#         # similarity
#         return 2.0
#     return sumDiff / n


# Jaccard similarity
def js(u1, u2, reviews):
    #Get categories for each user
    u1Cat = getData.getCategories(u1,reviews)
    u2Cat = getData.getCategories(u2,reviews)

    #Get number of common categories
    comCat = len(set(u1Cat).intersection(set(u2Cat)))

    #Get number of total categories
    allCat = len(list(set(u1Cat).union(set(u2Cat))))

    return comCat / allCat

# Friendship between users
def fr(u1, u2):
    return getData.isFriend(u1, u2)
