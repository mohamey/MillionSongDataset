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

## 9th of April
Processed nym results such that it outputs a list of artists in order of rank that are unique-ish to the Nym.

## 10th of April
A Refactor is sorely needed, code is messy. Code needs to be split into two segments:
* Data preparation (pre-BLC)

  Currently to prepare data a series of scripts must be run in a particular order. These need to be refactored into a module that is called by a data preparation script in the root of the project. This should take a number of arguments to define exactly what should happen
* Result Processing (Post-BLC) - Done

Information files generated while processing need to be stored better, naming makes no sense at the moment:
* Input data for Data preparation should be in folder Raw_Data
* Data pertaining to users and their mapping to ids, then row numbers should be stored in folder generated/User_Data
* Data pertaining to songs and their mappings to ids should be stored in folder generated/Song_Data
* Data pertaining to Nyms, their users, ratings, and songs should be stored in folder generated/Nym_Data

A Config file used by the whole project should define all paths to input/output files so no more local variables are defined.

Also need to begin work such that artists with a high score and low variance are selected as the Nym's seed artists.

## 11th of April
Refactor finished, code has three entry points:
* data_cleaner.py -- Run when dataset has just been downloaded and needs cleaning
* data_preprocessor.py -- Run to build maps of users to songs, normalize play counts, get ratings, and generate a sparse matrix
* process_results.py -- Run to process P file and build nym ratings, top song ranks, and get popular artists for each nym

To run any of the code, the following files need to be downloaded:

* Data/Dataset/train_triplets.txt - [Available Here](http://labrosa.ee.columbia.edu/millionsong/sites/default/files/challenge/train_triplets.txt.zip)
* Data/Dataset/unique_tracks.txt - [Available Here](https://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/unique_tracks.txt)
* Data/Dataset/sid_mismatches.txt - [Available Here](http://labrosa.ee.columbia.edu/millionsong/sites/default/files/tasteprofile/sid_mismatches.txt)

### Further Work RE: Rating Variance
Code now calculates variance of each users ratings and shows the mean rating for each item. Mean Ratings are pretty bad, mostly less than 2 for each item. This is probably due to an excess of 1s in input data. Not sure if this means if I should re-evaluate data preprocessing. Will probably try evaluating against spotify first

## 13th of April
Bug found!
After users have been assigned to nyms and their songs mean ratings calculated, there are songs with only one user in the Nym who've listened to it. The issue is that sometimes this song is the most listened to song by the user, giving it a rating of 5 and a variance of 0. Current ranking metric gives it a score of 5/5, so it ends up scoring ridiculously high even though only one user has listened to the song.

A possible solution is to only rank songs that a required number of users have listened to, like 25% of users.