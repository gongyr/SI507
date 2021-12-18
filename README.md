# Fall 2022 SI 507 Final Project

## Introduction
This project aims to build a basic web application, which allows the user to get information about cities in the US and the visualized data for restaurants in different cities. Several basic programming techniques are adopted in the project, which includes accessing data efficiently with caching via scraping and web API, using SQLite for data manipulating, using Unit Test for verification and using Plotly and Flask for data visualization, etc.

## Data Sources
(1) The web from Wikipedia, which is the data source for the table "Cities" in the database. (https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population). 

(2) Yelp Fusion, which is the data source for the table "Restaurants" in the database.
(https://www.yelp.com/developers/documentation/v3/business_search)

## Run the Program
### Step 1(Optional): Make you own csv or download the csv from the repository
(1) Make you own csv:
uncomment make_csv() and delete pass
```
if __name__ == '__main__':
    # make_csv()
    ...
    pass
```
(2) Download the csv from the repository
top_1000_movies.csv
### Step 2: Install packages
```
pip install -r requirements.txt --user
```  

### Step 3: Run the program
change code snippet below:
from 
```
if __name__ == '__main__':
    # make_csv()
    # save_tree_to_json()
    # main()
    pass

```  
to 

```
if __name__ == '__main__':
    # make_csv()
    # save_tree_to_json()
    main()

```  
$ python3 final_project.py
```  
