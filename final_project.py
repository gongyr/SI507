import csv
import json
import jsonpickle
import logging
import requests
import validators
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import webbrowser
from movie_trees import MovieTrees

log = logging.getLogger("IMDB TOP 1000 Movies")
logging.basicConfig(level=logging.INFO)


def connect_200(page_url):
    '''
    A function to make sure the http connection success
    '''
    try:
        page = requests.get(page_url)
        return page
    except ConnectionError as e:
        log.error(e)

class movie:
    '''
    A class contains movie_title, movie_year, rating, vote, url
    '''
    def __init__(self, movie_title, movie_year, rating, vote, url):
        self.movie_title = movie_title
        self.movie_year = movie_year
        self.rating = rating
        self.vote = vote
        self.url = url
        
    def to_string(self):
        return "title={} year={} rating={}".format(self.movie_title, self.movie_year, self.rating)

    def get_rating_value(self):
        return float(self.rating)

    def get_voting_value(self):
        return int(self.vote)

    def get_word_count_in_title(self):
        return len(self.movie_title.strip().split(" ")) if len(self.movie_title) > 0 else 0



def export_top_1000_list(movie_list):
    '''
    A function write a list to csv file
    '''
    file_name = "top_1000_movies.csv"
    export_file = open(file_name, mode='w', newline='', encoding="utf-8")
    with export_file:
        log.info("exporting : {}".format(file_name))
        export_writer = csv.writer(export_file, delimiter=',')
        export_writer.writerow(["index", "movie_title", "movie_year", "movie_rating", "movie_votes_count", "title_word_count"
                                ,"link_url"])
        index = 1
        if movie_list:
            for movie in movie_list:
                export_writer.writerow([index, movie.movie_title, movie.movie_year, movie.get_rating_value(),movie.get_voting_value(),
                                        movie.get_word_count_in_title(),movie.url])
                index += 1



def get_movie_info(page_url):
    '''
    A function that parse html file to movie class
    '''
    log.info("Processing : " + page_url)
    results = []
    page = connect_200(page_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    data = soup.find_all('div', 'lister-list')
    if data:
        movies = data[0].find_all('div', 'lister-item mode-simple')
        # print(list_item)
        if movies:
            for m in movies:
                title = m.find('div', 'col-title')
                title = title.find('a').getText().strip()
                rating = m.find('div', 'col-imdb-rating').getText().strip()
                year = m.find('span', 'lister-item-year text-muted unbold').getText().strip()
                year = (year.replace('(', '')).replace(')', '')
                year = year[-4:]
                for r in m.find_all('div', 'col-imdb-rating'):
                    vote = r.find_all("strong")[0]['title'].split(" ")[3]
                    vote = vote.replace(',', '')
                url_tag = m.find("a")
                url = ""
                if url_tag:
                    url = "https://www.imdb.com" + url_tag['href']
                info = movie(title, year, rating, vote, url)
                results.append(info)
    return results


def get_top_1000():
    '''
    A function that scrape the IMDB website
    '''
    top_list = []
    main_url = "https://www.imdb.com/search/title/?groups=top_1000&view=simple&sort=user_rating,desc&count=100"
    for i in range(0, 901, 100):
        url = main_url + "&start={}&ref_=adv_nxt".format(i + 1) if i > 0 else main_url
        if validators.url(url):
            info = get_movie_info(url)
            top_list += info
    return top_list


def make_csv():
    """
    A function that can be excuted to produces a csv.
    """
    movie_list = get_top_1000()
    if movie_list:
        export_top_1000_list(movie_list)

def main():
    # The start of range
    while True:
            try:
                print("Hello! We can search movies using rating range number. Please follow the guide to enter two numbers (the start of the range and the end of the range). You can enter exit at any time to end the program.")
                query1 = input('\nEnter a rating start number > 7.6 (the rating range is 7.6 to 9.5): ')
                if query1 == "exit":
                    print("Bye!")
                    break
                elif float(query1) > 9.5 or float(query1) < 7.6:
                    print("This is not in the range of 7.6 to 9.5. Please try again!")
                    continue
                else:
                    query1 = float(query1)
                    break
            except:
                print("This is not a valid number. Please enter a rating number in the range of 7.7-9.5: ")
    if query1 == 'exit':
        return 
    # The end of range
    while True:     
            try:
                query2 = input('Enter a rating end number greater than your rating start number (' + str(query1) + ') and less than or equal to 9.5: ')
                if query2 == "exit":
                    print("Bye!")
                    break
                elif float(query2) > 9.5 or float(query2) < 7.6:
                    print("This is not in the range of 7.6 to 9.5. Please try again!")
                    continue
                else:
                    query2 = float(query2)
                    break
            except:
                print("This is not a valid number. Please enter a rating number in the range of 7.7-9.5: ")
    if query2 == 'exit':
        return 
    # Get query result
    data = MovieTrees(3, "top_1000_movies.csv", "movie_rating")
    movie_range_query  = data.range_query(query1, query2)
    movie_range_query.sort(key=lambda row: row[3], reverse=True)

    movie_df = pd.DataFrame(movie_range_query, columns =['index','movie_title','movie_year','movie_rating','movie_votes_count','title_word_count','link_url']) 
    movie_df[["index", "movie_year", "movie_rating", "movie_votes_count", "title_word_count"]] = movie_df[["index", "movie_year", "movie_rating", "movie_votes_count", "title_word_count"]].apply(pd.to_numeric, errors='coerce')
    print("There are the " + str(len(movie_range_query)) + " movies that from rating " + str(query1) + " to " + str(query2))
    print(movie_df.drop(columns=['index']))

    # Open a link
    while True:
            index_url = input("To see more details please enter the index to open the url: ")
            if index_url == "exit":
                print("Bye!")
                break
            elif index_url.isnumeric() and int(index_url) <= len(movie_df) - 1:
                index_url = int(index_url)
                print("Launching " + movie_df['link_url'][index_url] + '...')
                webbrowser.open(movie_df['link_url'][index_url])
                break              
            else:
                print("There is no URL for the media to open.")
    if index_url == 'exit':
        return

    # Open a chart
    while True:
            print("Here are the chart options: \nLine Chart: \n 1.movie_year vs movie_rating \n 2.movie_year vs movie_votes_count\n 3.movie_year vs title_word_count\n 4.movie_rating vs movie_votes_count\n 5.movie_rating vs title_word_count\n\nHistogram: \n 6.movie_year\n 7.movie_rating\n 8.title_word_count\n 9.movie_votes_count\n")            
            index_chart = input("Choose one chart to display: ")
            if index_chart.isnumeric() and int(index_chart) <= 9:
                index_chart = int(index_chart)
                if index_chart == 1: 
                    show_line_chart(movie_df, 'movie_year', 'movie_rating')
                elif index_chart == 2: 
                    show_line_chart(movie_df, 'movie_year', 'movie_votes_count')
                elif index_chart == 3: 
                    show_line_chart(movie_df, 'movie_year', 'title_word_count')
                elif index_chart == 4:
                    show_line_chart(movie_df, 'movie_rating', 'movie_votes_count')
                elif index_chart == 5:
                    show_line_chart(movie_df, 'movie_rating', 'title_word_count')
                elif index_chart == 6:
                    show_hist_chart(movie_df, 'movie_year')
                elif index_chart == 7:
                    show_hist_chart(movie_df, 'movie_rating')
                elif index_chart == 8:
                    show_hist_chart(movie_df, 'title_word_count')
                else:
                    show_hist_chart(movie_df, 'movie_votes_count')
            elif index_chart == "exit":
                print("Bye!")
                break
            else:
                print("There is no chart to display.")
    if index_chart == 'exit':
        return

def show_line_chart(movie_df,x_value, y_value):
    '''
    A function that draw a line chart
    ----------------------------------
    movie_df: the data
    x_value
    y_value
    '''
    if x_value == 'movie_year':
        ax = movie_df.sort_values(by=x_value).plot.line(x=x_value, y=y_value, rot=0)
    else:
         ax = movie_df.plot.line(x=x_value, y=y_value, rot=0)
    ax.set_title(str(x_value) + ' V.S. ' + str(y_value))
    plt.show() 

def show_hist_chart(movie_df, value):
    '''
    A function that draw a histagram
    ----------------------------------
    movie_df: the data
    value
    '''
    ax = movie_df[value].plot.hist(orientation="vertical", cumulative=True)
    ax.set_title("Histogram for " + str(value))
    plt.show() 

def save_tree_to_json():
    '''
    A function that can convert python object to json
    '''
    data = MovieTrees(3, "top_1000_movies.csv", "movie_rating")
    data_json = jsonpickle.encode(data)
    with open('movies.json', 'w') as fp:
        json.dump(data_json, fp)

if __name__ == '__main__':
    # make_csv()
    # save_tree_to_json()
    # main()
    pass
