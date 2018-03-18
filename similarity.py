import getData

# Scaling factors for the different similarity metrics
a = 1 # DR, average difference in ratings
b = 1 # JS, Jaccard similarity
c = 1 # Fr, frienship between users

def simil(u1, u2, reviews):
    # Define a basic value for the similarity. In this way, we always consider
    # a review in the average
    simil = 1.0
    # Use the average difference in ratings. DR is between 0 and 4, so we normalize
    # it into [0, 1] dividing by 4. Furthermore, DR is a measure for the distance,
    # so we obtain a similarity measure by computing 1 - DR
    simil = simil + a * (1.0 - (dr(u1, u2, reviews) / 4.0))
    # Use the Jaccard similarity
    #simil = simil + b * js(u1, u2, reviews)
    # Use the friendship
    #simil = simil + c * fr(u1, u2)
    return simil

# Average difference in ratings
# The average of the absolute value of the difference in the reviews made by the
# two users to the same businesses
def dr(u1, u2, reviews):
    # Get the reviews of each user
    u1Reviews = {}
    u2Reviews = {}
    for r in reviews:
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
    sumDiff = 0
    n = 0
    for key, review in toIterate.iteritems():
        if key in other:
            # The two users reviewed the same business
            sumDiff = sumDiff + abs(review['stars'] - other[key]['stars'])
            n = n + 1

    if n == 0:
        # We do not have element to state the similarity, thus we assign a neutral
        # similarity
        return 2.0
    return sumDiff / n

# Jaccard similarity
def js(u1, u2, reviews):
    #Get categories for each user
    u1Cat = getData.getCategories(u1,reviews)
    u2Cat = getData.getCategories(u2,reviews)
    
    #Get number of common categories
    comCat = len(list(set(u1Cat).intersection(set(u2Cat))))
    
    #Get number of total categories
    allCat = len(list(set(u1Cat).intersection(set(u2Cat))))
    
    return comCat / allCat

# Friendship between users
def fr(u1, u2):
    return getData.isFriend(u1, u2)
