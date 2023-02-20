Kolokythas Christos sdi1700052

Akoumianakis Andreas sdi1700002

This program includes four functions that interact with a MySQL database to perform various tasks related to sentiment analysis, updating business zip codes, and selecting top businesses based on their reviews.

The connection() function is a helper function that creates a database connection object for MySQL by using the pymysql library and the configuration settings stored in a separate settings module.

The extract_ngrams() function takes two parameters: a string input and an integer n. It splits the input string by space and extracts all contiguous sequences of n words from the split list of words. It returns a list of these n-grams.

The classify_review() function takes a reviewid parameter as input and retrieves the corresponding review text from the database. It then extracts all 1-, 2-, and 3-grams from the review text and searches for the presence of positive and negative terms (stored in separate tables in the database) in the 1-, 2-, and 3-grams. It assigns a score based on the number of positive and negative terms found and classifies the review as either "good" or "bad". Finally, it returns a list of the business name and review text.

The updatezipcode() function takes a business_id and zipcode as input and updates the zip_code field in the business table for the given business_id. If the business_id is not found in the database, it returns an error message.

The selectTopNbusinesses() function takes a category_id and n as input and retrieves the top n businesses (by number of positive reviews) in the given category. It returns a list of the business names and the number of positive reviews.
