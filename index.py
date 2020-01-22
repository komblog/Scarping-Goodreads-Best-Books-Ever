from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from tqdm import tqdm
import pandas as pd

#Akses web
my_url = 'https://www.goodreads.com/list/show/1.Best_Books_Ever'
client = uReq(my_url)
page_html = client.read()
client.close()

#html parsing
page_soup = soup(page_html, "html.parser")

#grab list books
table = page_soup.find("table", {"class" : "tableList js-dataTooltip"})
table_row = table.find_all('tr')

number = []
title = []
author = []
rating = []
score = []
vote = []

number_of_books = len(table_row)

for row in tqdm(range(number_of_books)):
    number_object = table_row[row].find_all("td", {"class" : "number"})
    book_object = table_row[row].find_all("span", {"itemprop" : "name"})
    book_avg_rating_list = table_row[row].find_all("span", {"class" : "minirating"})
    book_score_object = table_row[row].find_all("span", {"class" : "smallText uitext"})    
    
    book_number = number_object[0].text
    book_title = book_object[0].text
    book_author = book_object[1].text
    book_avg_rating = book_avg_rating_list[0].text
    book_score = book_score_object[0].find_all('a')
    book_score_a = book_score[0].text.split()[1]
    book_people_voted_a = book_score[1].text.split()[0]
    
    number.append(int(book_number))
    title.append(str(book_title))
    author.append(str(book_author))
    rating.append(str(book_avg_rating))
    score.append(str(book_score_a))
    vote.append(str(book_people_voted_a))

    goodread_data = pd.DataFrame(set(zip(number,title, author, rating, score, vote)))
    goodread_data.columns = ["Number","Title", "Author", "Rating", "Score", "Vote"]
    goodread_data = goodread_data.sort_values(['Number'])

    goodread_data