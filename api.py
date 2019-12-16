from app import app, datab
from flask import render_template, Response, request, redirect, url_for, session
from models import Book, Author
import config
import requests
import xmltodict
from xml.etree import ElementTree as ET
import flask_login

@app.route('/button', methods=['GET','POST'])
def button():
	bookname = request.form['bookname']
	r = requests.get('https://www.goodreads.com/search.xml?key='+config.GOODREADS_API_KEY+'&q=+'+ bookname +'%27s+')
	if(r.status_code != 200):
		return '<h1> Error with API </h1>'
	else:
		data_dict = xmltodict.parse(r.content)
		author_name = data_dict['GoodreadsResponse']['search']['results']['work'][0]['best_book']['author']['name']
		author = Author(name=author_name)
		title = data_dict['GoodreadsResponse']['search']['results']['work'][0]['best_book']['title']
		year = data_dict['GoodreadsResponse']['search']['results']['work'][0]['original_publication_year']['#text']
		rating = data_dict['GoodreadsResponse']['search']['results']['work'][0]['average_rating']
		image_url = data_dict['GoodreadsResponse']['search']['results']['work'][0]['best_book']['image_url']
		new_book = Book(title=title, year=year, rating=rating, image_url=image_url, owner=author)
		datab.session.add(new_book)
		new_book.bookworms.append(flask_login.current_user)
		datab.session.commit()
		# return data_dict['GoodreadsResponse']['search']['results']['work'][0]['best_book']['image_url']
		return redirect(url_for('dashboard'))
