* Get user profile subset
* Strip untrusted song IDs from triplets
* Check how many triplets removed as a result

# Data Processing
* Raw Train Triplets: 48373586
* Filtered Train Triplets: 45795100
* 5.33% of entries Removed (2578486)

## User Data
__After__ build user track dict, there are 1,019,318 users.
__After__ Normalizing data, there are 978,301 users. (-41,017 / 4%)

## Creating BLC input
With 3000 users, originally outputs 1,576,749 ratings, 85.8% of which are 1. I've put a quota for the number of ones in place, so each user can have a max of 5 '1' ratings. With this quota, number of ratings dropped to 235,585 ( -85% )
