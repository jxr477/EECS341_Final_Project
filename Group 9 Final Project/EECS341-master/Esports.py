from flask import Flask, render_template, request, jsonify
import psycopg2
import json
from json2html import *

app = Flask(__name__)

def connect_db():
	try:
		sql = psycopg2.connect(user = "mye",
										password="abcd1234",
										host="127.0.0.1",
										port="5432",
										database="eecs341")
		return sql
	except:
		print("Unable connect to the database") 

def getQ(input="select * from player"):
	cursor = connect_db().cursor()
	postgreSQL_select_Query = input

	cursor.execute(postgreSQL_select_Query)
	row_headers =[x[0] for x in cursor.description]
	rv = cursor.fetchall()
	json_data=[]
	for result in rv:
		json_data.append(dict(zip(row_headers, result)))
	return json.dumps(json_data)


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/club', methods=['GET', 'POST'])
def club():
	if request.method == 'POST':
		
		if not request.form.get('gameID2'): 
			
			if not request.form.get('rank'):

				if request.form.get('nationality') == 'All':
					if request.form.get("gameID") == "0":
						query = " SELECT DISTINCT club_name FROM club"
						if getQ(query) == "[]":
							return render_template('search_club.html', output2="1")
						else:
							return render_template('search_club.html', output = json2html.convert(getQ(query)))					
						# return '<h1>{}<h1>'.format(query)
						# return render_template('search_club.html', output = json2html.convert(getQ(query)))
					else:
						query = " SELECT DISTINCT club_name FROM club, game, play WHERE play.game_id = game.game_id  and club.club_id = play.club_id and game.game_id = '{}'".format(request.form.get('gameID'))
						if getQ(query) == "[]":
							return render_template('search_club.html', output2="1")
						else:
							return render_template('search_club.html', output = json2html.convert(getQ(query)))						
						# return '<h1>{}<h1>'.format(query)
						# return render_template('search_club.html', output = json2html.convert(getQ(query)))				
				else:
					if request.form.get("gameID") == "0":
						query = " SELECT DISTINCT club_name FROM club where club.country = '{}'".format(request.form.get('nationality'))
						if getQ(query) == "[]":
							return render_template('search_club.html', output2="1")
						else:
							return render_template('search_club.html', output = json2html.convert(getQ(query)))						
						# return '<h1>{}<h1>'.format(query)
						# return render_template('search_club.html', output = json2html.convert(getQ(query)))
					else:
						query = " SELECT DISTINCT club_name FROM club, game, play WHERE play.game_id = game.game_id  and club.club_id = play.club_id and club.country ='{}'and game.game_id = '{}'".format(request.form.get('gameID'),request.form.get('nationality'))
						if getQ(query) == "[]":
							return render_template('search_club.html', output2="1")
						else:
							return render_template('search_club.html', output = json2html.convert(getQ(query)))						
						# return '<h1>{}<h1>'.format(query)
						# return render_template('search_club.html', output = json2html.convert(getQ(query)))	
			else:
				if request.form.get('nationality') == 'All':
					if request.form.get("gameID") == "0":
						query = " SELECT DISTINCT club_name, club_rank FROM club"
						if getQ(query) == "[]":
							return render_template('search_club.html', output2="1")
						else:
							return render_template('search_club.html', output = json2html.convert(getQ(query)))						# return render_template('search_club.html', output = json2html.convert(getQ(query)))
					else:
						query = " SELECT DISTINCT club_name, club_rank  FROM club, game, play WHERE play.game_id = game.game_id  and club.club_id = play.club_id and game.game_id = '{}'".format(request.form.get('gameID'))
						if getQ(query) == "[]":
							return render_template('search_club.html', output2="1")
						else:
							return render_template('search_club.html', output = json2html.convert(getQ(query)))						# return render_template('search_club.html', output = json2html.convert(getQ(query)))				
				else:
					if request.form.get("gameID") == "0":
						query = " SELECT DISTINCT club_name, club_rank  FROM club and club.country = '{}'".format(request.form.get('nationality'))
						if getQ(query) == "[]":
							return render_template('search_club.html', output2="1")
						else:
							return render_template('search_club.html', output = json2html.convert(getQ(query)))						# return render_template('search_club.html', output = json2html.convert(getQ(query)))
					else:
						query = " SELECT DISTINCT club_name, club_rank  FROM club, game, play WHERE play.game_id = game.game_id  and club.club_id = play.club_id and club.country ='{}'and game.game_id = '{}'".format(request.form.get('gameID'),request.form.get('nationality'))
						if getQ(query) == "[]":
							return render_template('search_club.html', output2="1")
						else:
							return render_template('search_club.html', output = json2html.convert(getQ(query)))						# return render_template('search_club.html', output = json2html.convert(getQ(query)))					
		
		else:
			query = "Select c.club_name from Club c where not exists ((select p.club_id from Participate p where p.club_id = c.club_id) except (select g.game_id from Game_tournament g where g.game_id = '{}'))".format(request.form.get('gameID2'))
			if getQ(query) == "[]":
				return render_template('search_club.html', output2="1")
			else:
				return render_template('search_club.html', output = json2html.convert(getQ(query)))				
		
		if getQ(query) == "[]":
			return render_template('search_club.html', output2="1")
		else:
			return render_template('search_club.html', output = json2html.convert(getQ(query)))
	
	return render_template('search_club.html')

@app.route('/player', methods=['GET', 'POST'])
def player():
	if request.method == 'POST':
		if not request.form.get('age'):
			if  request.form.get('country') != 'all':
				if request.form.get('team') == '':
					query =  "SELECT DISTINCT player_name FROM player, game, play WHERE play.game_id = game.game_id  and player.nationality = '{}'".format(request.form.get('country'))					
				# query =  "SELECT DISTINCT player_name FROM player"		
				else:
					query =  "SELECT DISTINCT player_name FROM player, club, work_for WHERE  player.player_id = work_for.player_id and work_for.club_id = club.club_id and club.club_name = '{}' and player.nationality = '{}'".format(request.form['team'], request.form.get('country'))    
			else:
				if request.form.get('team') == '':
					query =  "SELECT DISTINCT player_name FROM player"
				else:
					query =  "SELECT DISTINCT player_name FROM player, club, work_for WHERE  player.player_id = work_for.player_id and work_for.club_id = club.club_id and club.club_name = '{}'".format(request.form['team'])    
		if request.form.get('age'):
			if  request.form.get('country') != 'all':
				if request.form.get('team') == '':
					query =  "SELECT DISTINCT player_name, player_age FROM player, game, play WHERE play.game_id = game.game_id  and player.nationality = '{}'".format(request.form.get('country'))						
				else:
					query =  "SELECT DISTINCT player_name, player_age FROM player, club, work_for WHERE  player.player_id = work_for.player_id and work_for.club_id = club.club_id and club.club_name = '{}' and player.nationality = '{}'".format(request.form['team'], request.form.get('country'))    
			else:
				if request.form.get('team') == '':
					query =  "SELECT DISTINCT player_name, player_age FROM player"
				else:
					query =  "SELECT DISTINCT player_name, player_age FROM player, club, work_for WHERE  player.player_id = work_for.player_id and work_for.club_id = club.club_id and club.club_name = '{}'".format(request.form['team'])       
		
		if getQ(query) == "[]":
			return render_template('search_player.html', output2="1")
		return render_template('search_player.html', output = json2html.convert(getQ(query)))
		# return '<h1>{},{}<h1>'.format(query,getQ(query))
	return render_template('search_player.html')

if __name__ == '__main__':
	app.run(debug=True)
