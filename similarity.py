import getData

# Scaling factors for the different similarity metrics
a = 1 # DR, average difference in ratings
b = 1 # JS, Jaccard similarity
c = 1 # Fr, frienship between users

def simil(u1, u2, reviews):
    return a * dr(u1, u2)
        + b * js(u1, u2)
#        + c * fr(u1, u2)

# Average difference in ratings ALE
def dr(u1, u2):
    return 1

# Jaccard similarity MARIA
def js(u1, u2):
    return 1

# Friendship between users
def fr(u1, u2):
    return getData.isFriend(u1, u2)
