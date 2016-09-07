
IR Approach Classes and Methodology

we imported the business, review and tip into mongodb and indexed the 3 collections on business_id.
Indexing on business_id improves the performance of retreiving the data faster when compared without Indexing.
we extracted the  review and tips, business_name, categories for each business_ID and we were able to extract the data in
15 minutes with index on business_ID whereas without Index it took 6 hours.

Create Training and Test Data :

This class creates two collections training_colleciton and test_collection. For each business_Id we extracted review and
tips, business_name, categories. First 40,000(60%) records are stored in training_collection and remaining records(40%) are stored in 
test_collection

Create Training Categories :
Extracts all the unique categories in the list and creates new files for each category and stores review and tips data.

Create Training Index :
Indexes the category and review + tips from the folder created by create training categories class. Used English analyzer
which removes stop words 

Feature Extractor.

This class extracts the top 10 or 50 features for a particular category based on TF and IDF score and stores the result in 
feature_set collection. Before extraction the features, we cleaned the data based on various filters like words, urls, repeating
character in order to get more precise results

create Test Index
Indexed the business_id, review+tips, categories, names from test_collection.

Assign categories to test data:

This class first computes grouping categories. For two categories if the number of features are 70% same, then the two features
are grouped into one category. This step will increase the recall value.

After grouping category, then based on top hits for the features we passed, we predicted the categories to each business_id and stores
the predicted results in categories_assigned_from_code collection

Evaluation :
we estimated the precision, recall and f1 measure based on number of categories matching with already given category and predicted category.

