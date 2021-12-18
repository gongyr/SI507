# Fall 2022 SI 507 Final Project

## Introduction
This project aims to build a command line tool, which allows the user to get information about movies based on IMDB ratings and the visualized data for different vairables. Several basic programming techniques are adopted in the project, which includes scaping data and then store the data into a B-tree data structure and using matplotlib and pandas for data visualization, etc.

## Data Sources
The web from IMDB (from page 1 to 50):
<br />
https://www.imdb.com/search/title/?groups=top_1000&view=simple&sort=user_rating,desc

## Data Structure
B-Tree <br />
All fetched data are stored in a tree with nested nodes. 

## Run the Program
### Step 1 (Optional): Make you own csv or download the csv from the repository
(1) Make you own csv:
uncomment make_csv() and delete pass
```
if __name__ == '__main__':
    # make_csv()
    ...
    pass
```
```
$ python3 final_project.py
``` 
(2) Download the csv from the repository:
<br />
top_1000_movies.csv
### Step 2: Install packages
```
pip install -r requirements.txt --user
```  

### Step 3: Run the program
change code snippet below:
<br />
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
```
$ python3 final_project.py
```  