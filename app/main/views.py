from . import main
from flask import render_template

@main.route('/login')
def login():
	pass

@main.route('/')
def index():
	return render_template('main/404.html')