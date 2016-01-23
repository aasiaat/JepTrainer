from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import sqlite3
import time

conn = sqlite3.connect('Jeopardy.db')
c = conn.cursor()

def tableCreate():
    try:
        c.execute("CREATE TABLE jeopardy(ID INTEGER PRIMARY KEY AUTOINCREMENT, game_ID INT, date TEXT, round INT, category TEXT, category_comment TEXT, money_value text, value INT, clue TEXT, correct_response TEXT, correct_contestants INT)")
    except Exception:
        pass

    try:
        c.execute("CREATE TABLE responses(response_ID INTEGER PRIMARY KEY AUTOINCREMENT, clue_ID INT, response_type INT, response_timestamp TIMESTAMP)")
    except Exception:
        pass

def findNewestGameNumber():
    second_soup = BeautifulSoup(urlopen('http://www.j-archive.com/' ),"html.parser")
    newest_game_number = str(second_soup.find('td', {'class' : 'splash_clue_footer'})).rpartition("=")[2]
    newest_game_number = newest_game_number[:4]
    newest_game_number
    return newest_game_number

def findEndOfDB():
    c.execute("SELECT max(game_ID) FROM jeopardy")
    data = c.fetchone()
    return data[0]

def gameDetails():
    game_date = soup.find("div", {"id" : "game_title"})
    game_date = game_date.getText()
    game_date = game_date.rpartition("day, ")[2]
    game_number = url.rpartition("=")[2]
    return game_date, game_number

def round1():
    categories = []
    cat_comments = []
    answers = []
    values = []
    clue = []

    round1 = soup.find("div", {"id" : "jeopardy_round"})

    #Pull out Category Name and any Category Comments
    for category in round1.findAll('td', {'class' : 'category'}):

        cat_name = category.findAll( 'td', {'class' : 'category_name'})
        cat_comm = category.findAll( 'td', {'class' : 'category_comments'})

        categories.append(cat_name[0].getText())
        cat_comments.append(cat_comm[0].getText())



    for clues in round1.findAll('td', {'class' : 'clue'}):
        clue_value = clues.findAll('td', {'class' : re.compile('clue_value*')})
        clue_text = clues.findAll('td', {'class' : 'clue_text'})

        # print(clue_value)
        # print(clue_text)
        # print(clue_text)
        # print(clue_text[0].getText())
        try:
            values.append(clue_value[0].getText())
            clue.append(clue_text[0].getText())
            answer = BeautifulSoup(clues.find("div", onmouseover=True).get("onmouseover"), "html.parser")
            answer = answer.find("em", class_="correct_response").getText()
            answers.append(answer)
        except IndexError:
            values.append(0)
            clue.append(" ")
            answers.append(" ")


    for i in range(len(values)):

         c.execute("INSERT INTO jeopardy(game_ID, date, round, category, category_comment, money_value, value, clue, correct_response) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (game_id, air_date, 1, categories[i % 6], cat_comments[i % 6], values[i], (int(i/6)*200+200), clue[i], answers[i]))

    conn.commit()
    return

def round2():
    categories = []
    cat_comments = []
    answers = []
    values = []
    questions = []
    clue = []

    round2 = soup.find("div", {"id" : "double_jeopardy_round"})

    #Pull out Category Name and any Category Comments
    for category in round2.findAll('td', {'class' : 'category'}):

        cat_name = category.findAll( 'td', {'class' : 'category_name'})
        cat_comm = category.findAll( 'td', {'class' : 'category_comments'})

        categories.append(cat_name[0].getText())
        cat_comments.append(cat_comm[0].getText())

    for clues in round2.findAll('td', {'class' : 'clue'}):
        clue_value = clues.findAll('td', {'class' : re.compile('clue_value*')})
        clue_text = clues.findAll('td', {'class' : 'clue_text'})

        try:
            values.append(clue_value[0].getText())
            clue.append(clue_text[0].getText())
            answer = BeautifulSoup(clues.find("div", onmouseover=True).get("onmouseover"), "html.parser")
            answer = answer.find("em", class_="correct_response").getText()
            answers.append(answer)
        except IndexError:
            values.append(0)
            clue.append(" ")
            answers.append(" ")


    for i , val in enumerate(values):

         c.execute("INSERT INTO jeopardy(game_ID, date, round, category, category_comment, money_value, value, clue, correct_response) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (game_id, air_date, 2, categories[i % 6], cat_comments[i % 6], values[i], (int(i/6)*200+200), clue[i], answers[i]))
    conn.commit()
    return

def round3():

    categories = []
    cat_comments = []
    answers = []
    values = []
    questions = []
    clue = []

    round3 = soup.find("div", {"id" : "final_jeopardy_round"})

    #Pull out Category Name and any Category Comments
    for category in round3.findAll('td', {'class' : 'category'}):

        cat_name = category.find( 'td', {'class' : 'category_name'})
        cat_name = cat_name.getText()

        cat_comm = category.find( 'td', {'class' : 'category_comments'})
        cat_comm = cat_comm.getText()
        answer = BeautifulSoup(category.find("div", onmouseover=True).get("onmouseover"), "html.parser")
        answer = answer.find("em")
        answer = answer.getText()
        correct_responses = BeautifulSoup(category.find("div", onmouseover=True).get("onmouseover"), "html.parser")

        correct_responses = correct_responses.findAll('td', class_="right")
        num_correct_responses = len(correct_responses)
    for clues in round3.findAll('td', {'class' : 'clue'}):

        clue_text = clues.find('td', {'class' : 'clue_text'})
        clue_text = clue_text.getText()

    #c.execute("CREATE TABLE jeopardy(ID INTEGER PRIMARY KEY AUTOINCREMENT, game_ID INT, date TEXT, round INT, category TEXT, money_value text, value INT, clue TEXT, correct_response TEXT, correct_contestants INT)")


    c.execute("INSERT INTO jeopardy(game_ID, date, round, category, category_comment, clue, correct_response, correct_contestants) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (game_id, air_date, 3, cat_name, cat_comm, clue_text, answer, num_correct_responses))
    conn.commit()
    return


tableCreate()

newest_game = int(findNewestGameNumber())

if findEndOfDB() == None:
    next_game = 1
else:
    next_game = findEndOfDB() + 1

while next_game <= newest_game:
    url = "http://www.j-archive.com/showgame.php?game_id=" + str(next_game)
    soup = BeautifulSoup(urlopen(url),"html.parser")

    air_date, game_id = gameDetails()

    round1()
    round2()
    round3()
    next_game = next_game + 1
    time.sleep(20)

