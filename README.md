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

## 31st of March
Changed project such that instead of normalising ratings between 1 and 10, ratings are now expressed as a fraction of listening time and scaled up by 100. My reasoning for this was when given two users who listened to the same song the most, 2 and 50 times respectively, would give a score of 10. 50, however, is substantially more time spent listening to the song than 2, and as such we can be more confident in the second user liking the song, whereas we can't really assume the first user would rate the song 10/10. By making play count proportional to a user's total play count, we are applying weights to ratings.

Another avenue to explore is making ratings proportional to play counts divided by play counts __greater__ than 1. This is because a user __must__ listen to a song at least once to determine whether they like it or not. A play count of 1 also does not necessarily mean a user doesn't like a song, and so it deserves a 1 out of 10. Also worth noting is that by taking this approach, we limit the number of 1s that are used (which is actually a lot), and hopefully boost the ratings for other songs.

## 4th of April
Project back to scaling ratings between 1 and 10. Biggest change is that when normalizing we no bother keeping ratings for song that only have one listen as it's not very useful info. Additionally, using filter\_sparse\_songs.py we prune songs which dont have enough ratings. Fiddled extensively with numbers, and best performance has been achieved using 20,000 users and filtering songs with less than 100 ratings. This results in:

* Factorisation RMSE: 1.268528
* Prediction RMSE: 1.776873

Training Ratio is 0.2
