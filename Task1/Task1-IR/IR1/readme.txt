
(1) Build three collections to the database yelp.
business: from file “yelp_academic_dataset_business.json”
review: from file “yelp_academic_dataset_review.json”
tip: from file “yelp_academic_dataset_tip.json”

mongoimport --db yelp --collection business --file /Users/yangyang/Desktop/IU/534/project/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json

mongoimport --db yelp --collection business --file /Users/yangyang/Desktop/IU/534/project/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json

mongoimport --db yelp --collection business --file /Users/yangyang/Desktop/IU/534/project/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_tip.json

(2) Build indexes for business, review and tip collections to speed up the search process.

db.review.ensureIndex({“business_id”:1})
db.tip.ensureIndex({“business_id”:1})
db.business.ensureIndex({“business_id”:1})
	

(3) Build the collection “test_set”, which includes the business information, reviews and tips for each business_id. Total has 61184 records. Finished in 6 minutes.

retrieveCollections.java
(mongo-java-driver-2.11.1.jar)
 

(4) Build index for “test_set” collection
generateIndex.java
(lucene)

(5) Generate queries for all categories. For each category, simply take it as query.
generateQueries.java --- > queries2.txt
910 categories -- > 910 queries

(6) ground truth file
for each business_id, it already has some categories assigned to it. We will use this as ground truth file.  504073 lines in groundtruth.txt
eg. if business_id1 has category [category2]
business_id1		category1		0 
business_id1		category2		1
……


(7) For each query, search the fields “review” and “tip”, and find the top 10 related business_id.  
two separate result files will be generated. 
reviewFieldScores.txt
tipFieldScores.txt
getScores.java

(8) compare the result from (7) with the ground truth file
evaluation_review_BM25.txt
evaluation_tip_BM25.txt

