# coding=utf-8

from flask import Flask,url_for
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from models import Base, RegisteredUsers, FaceFeatureMap, UserRights
from flask import render_template
import cv2
import numpy as np
from capture import Capture



import argparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
db = SQLAlchemy(app)
db.Model = Base


def args_parse():
	arguments  = argparse.ArgumentParser()
	arguments.add_argument('--ip', help='Specify the IP address for web service', required=False, type=str)
	arguments.add_argument('--port', help='Specify the port for service listen', required=False, type=int)
	arguments.add_argument('--debug', help='Enable Debug Model', required=False, type=bool)
	args = arguments.parse_args()
	return args

@app.route('/')
def hello():
	return 'Hello World!'

@app.route('/login_demo/')
def show_login_demo():
	return render_template('login_auth.html')

@app.route('/login_demo/#scan')
def start_scan_face():
	inst_capture = Capture()
	image = inst_capture.start()


@app.route('/user/add/', methods=['GET', 'POST'])
def add_user():
	return 'Add user page'


@app.route('/user/<int:user_id>/delete/', methods=['DELETE'])
def del_user(user_id):
	return 'user {} has been deleted'.format(str(user_id))

@app.route('/login_success/<int:user_id>/')
def login_success(user_id):
	return "Login Successful. User ID: {}".format(str(user_id))

@app.route('/user/<int:user_id>/edit/', methods=['GET', 'POST'])
def modify_user(user_id):
	return "Modify user: {}".format(str(user_id))

@app.route('/user/<int:user_id>/')
def user_detail(user_id):
	edit_url = url_for('modify_user', user_id=user_id)
	return edit_url



if __name__ == '__main__':
	args = args_parse()
	ip_addr = "127.0.0.1" if args.ip is None else args.ip
	port = 5000 if args.port is None else args.port
	app.run(ip_addr, port, debug=args.debug)



