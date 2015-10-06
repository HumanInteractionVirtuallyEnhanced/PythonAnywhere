from flask import render_template, flash, redirect, session, url_for, request, g, Flask, jsonify, Response
from flask.ext.login import login_user, logout_user, current_user, login_required, LoginManager
from app import app, db, lm#, oid
from models import User, ROLE_USER, ROLE_ADMIN, ROLE_PROF, Comment, Notification, Hashtag, Message, DirectMessage
#import functions
#from forms import LoginForm, SearchForm, fakeUserForm, createEventForm, submitCommentForm, submitReplyForm, professorLoginForm, emailForm
from random import randint
from datetime import datetime, timedelta
from sqlalchemy import desc
#import pyimgur #Client ID = bec1dce8d56fe94|| Client secret:3e457c44ecb7ab75cc9a83697cc71920ea273043
from werkzeug import secure_filename
from time import strptime, strftime
from flask.ext.mail import Mail, Message
import re
import random
import requests
import json
import urllib2

from geopy.geocoders import GoogleV3
geolocator = GoogleV3()

from config import ADMINS

login_manager = LoginManager()
login_manager.login_view = "index"

#timeChanger = timedelta(hours=(4), minutes=30)
timeChanger = timedelta(hours=5, minutes=0)#This is the correct time for people in new haven
#timeChanger = timedelta(hours=(5 + 59), minutes=0)
da_time= datetime.now() - timeChanger

# from flask.ext.social import Social
# # from flask.ext.security import Security, SQLAlchemyUserDatastore, \
# #     UserMixin, RoleMixin, login_required
# from flask.ext.social.datastore import SQLAlchemyConnectionDatastore

from flask_oauth import OAuth
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='613995812038257',
    consumer_secret='05e778848e1187897b834fba967cc0c9',
    request_token_params={'scope': 'email'}
)
# facebook = OAuth2Service(name='facebook',
#                          authorize_url='https://www.facebook.com/dialog/oauth',
#                          access_token_url=graph_url + 'oauth/access_token',
#                          client_id='613995812038257',
#                          client_secret='05e778848e1187897b834fba967cc0c9',
#                          base_url=graph_url)




# f = FacebookAPI(client_id='613995812038257',
#                 client_secret='05e778848e1187897b834fba967cc0c9',
#                 redirect_uri='http://groopie.pythonanywhere.com/login/')


import os
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'groopieco@gmail.com'#os.environ.get('groopieco@gmail.com')
MAIL_PASSWORD = '12RedFoxes'#os.environ.get('12RedFoxes')



# #https://graph.facebook.com/<user alias>/picture - gives you access to a small thumbnail of the user's facebook profile picture. The <user alias> is the person's facebook ID which is found using the method below.
#https://graph.facebook.com/10205478054374438/picture
# #import datetime


# UPLOAD_FOLDER = 'static/img/saved'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



#from app import app
# @app.route('/')
# @app.route('/index')
# def index():
#     return "Hello World!"

mail = Mail(app)






@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
    #return "OHFSOIDJFOISDJFIOJ"
    # comString = Comment.query.order_by(desc(Comment.atTime)).first().latLon
    # address = geolocator.reverse(comString)
    # simpleAdress = str(address[0][0])
    # retStr = simpleAdress.split(',')[1]
    # #return jsonify(results = address)
    # for a in address:
    #     retStr += str(a)
    #     retStr += "<br>"
    # return retStr

@app.route('/leaderboard')
def leaderboard():
    #return "KOOLAID"
    #us = models.User.qu
    #return render_template("leaderboard.html")
    #users = sorted(User.query.all(), key=lambda User:User.followers.count(), reverse=True)[:2]
    # retStr = ""
    # for u in us:
    #     retStr += u.nickname
    #     retStr += "<br>"
    #     retStr += "Followers:"
    #     retStr += str(u.followers.count())
    #     retStr += "<br><br>"
    return render_template("leaderboard.html")
    #return retStr

@app.route('/get_leaders', methods = ["GET", "POST"])
def get_leaders():
    users = sorted(User.query.all(), key=lambda User:User.followers.count(), reverse=True)[:20]
    return render_template('allLeaders.html', users = users)

    #return render_template("index.html")
# 	user = g.user
# 	if user.is_authenticated() is True and user.role is not 1:
# 	        return redirect(url_for('home', focus = 'user'))
# # 	return redirect(url_for('userYou', nickname = user.nickname, on_course = 777, on_note = 10101, reply_to = 121212))
# 	return render_template("index.html",
# 		title = 'Home',
# 		user = user)


@app.route('/apply')
def apply():
    #msg = Message("test", sender = 'groopieco@gmail.com', recipients=['groopieco@gmail.com'])
    #mail.send(msg)
    return render_template('apply.html')

@app.route('/apply_send', methods = ["GET", "POST"])
def apply_send():
    fullMessage = str(request.form['sent_message'])
    userEmail = str(request.form['user_email'])
    msg = Message('Groopie Application', sender='groopieco@gmail.com', recipients=['groopieco@gmail.com','rijul.gupta@yale.edu', 'james.park.jp858@yale.edu'])
    msg.body = fullMessage
    mail.send(msg)
    return "done"


@app.route('/report_comment', methods = ["GET", "POST"])
def report_comment():
    comment_id = int(request.form['comment_id'])
    reporting_user = g.user
    comment = Comment.query.filter_by(id = comment_id).first()
    body = comment.body
    reported_user = comment.author.nickname
    user_email = comment.author.email
    send_string = "Reported User:"
    send_string += str(reported_user)
    send_string += "<br><br>"
    send_string += "Comment:"
    send_string += str(body)
    send_string += "<br><br>"
    send_string += "Email:"
    send_string += str(user_email)
    send_string += "<br><br><br><br>"
    send_string += "Reporting User:"
    send_string += str(reporting_user.nickname)
    send_string += "<br><br>"
    send_string += "Email:"
    send_string += str(reporting_user.email)
    send_string += "<br><br><br><br>"
    send_string += "Period ID:"
    send_string += str(comment.period_id)
    send_string += "<br><br>"
    msg = Message('Reporting Comment', sender='groopieco@gmail.com', recipients=['groopieco@gmail.com'])
    msg.html = send_string
    mail.send(msg)
    returnString = "The comment by " + str(reported_user) + " has been reported for abuse!"
    return returnString

# @app.errorhandler(500)
# def page_not_found(e):
#     #user = g.user
#     return render_template("HELLO WORLD!")


# @app.errorhandler(400)
# def page_not_found_bad_proxy(e):
#     #user = g.user
#     return render_template("HELLO WORLD!")

# @app.errorhandler(404)
# def page_not_found_404(e):
#     #user = g.user
#     return "NO"

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


# @app.before_request
# def before_request():
#     g.user = current_user
#     if g.user.is_authenticated():
#     	g.user.last_seen = datetime.utcnow()
#     	g.search_form = SearchForm()





@app.route('/logout')
def logout():
    logout_user()
    session.clear()
	#session['oauth_token'] = ""
	#return redirect(url_for('https://www.facebook.com/logout.php?next=google.com&access_token='+session.get('oauth_token').value))
    return redirect(url_for('index'))





@app.route('/login', methods = ["GET", "POST"])
def login():
# 	if g.user is not None and g.user.is_authenticated():
# 		return redirect(url_for('index'))

    r = requests.get('https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id=613995812038257&client_secret=05e778848e1187897b834fba967cc0c9')
    access_token = r.text.split('=')[1]
    userID = str(10205478054374438)
    reqString = "https://graph.facebook.com/"+userID+"?fields=name&access_token=" + str(access_token)
    reqString = "https://graph.facebook.com/"+userID+"?fields=email&access_token=" + str(access_token)
    #return reqString
    got = requests.get(reqString)
    retString = "none"
    return got.json()["email"]
    #return access_token
    #facebook.authorize(callback=url_for('facebook_authorized', next=request.args.get('next') or request.referrer or None, _external=True))
    #return facebook_authorized()
	#return facebook.authorize(callback=url_for('facebook_authorized', next=request.args.get('next') or request.referrer or None, _external=True))


# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)


# @app.route('/login/authorized')
# @facebook.authorized_handler
# def facebook_authorized(resp):
# #def facebook_authorized():
#     #return redirect(url_for('index'))
#     return "testical"
#     if resp is None:
#       return 'Access denied: reason=%s error=%s' % (
#             request.args['error_reason'],
#             request.args['error_description']
#         )
#     return "hello"
#     session['oauth_token'] = (resp['access_token'], '')
#     me = facebook.get('/me')
#     return str("hello")
#     #return requests.get('https://graph.facebook.com/10205478054374438?fields=username')
#     #return jsonify(results = response)
#     #return jsonify(results = me.data['name'])
#     #user = User.query.filter_by(email = me.data['email']).first()
#     user = User.query.filter_by(fb_id = me.data['id']).first()
#     if user is None:
#     	u = User(nickname = me.data['name'], email = me.data['email'], role = ROLE_USER, fb_id = me.data['id'])
#     	db.session.add(u)
#     	db.session.commit()
#     	return redirect(url_for('validate'))
#     user.nickname = me.data['name']
#     user.fb_id = int(me.data['id'])
#     login_user(user, remember = True)
#     db.session.commit()
#     #return redirect(request.args.get('next'))
#     #return redirect(url_for('event', eventID = 1761))
#     return "done"
#     #return redirect(url_for('index'))
#     #return redirect(url_for('validate'))
#     #return redirect(url_for('home', focus = "user"))
# #     return 'Logged in as id=%s name=%s redirect=%s || email=%s' % \
# #         (me.data['id'], me.data['name'], request.args.get('next'), me.data['email'])

# @facebook.tokengetter
# def get_facebook_oauth_token():
#     return session.get('oauth_token')



@app.route('/validate', methods = ["GET", "POST"])
@login_required
def validate():
    user = g.user
    eForm = emailForm(prefix = "eForm")
    if eForm.validate_on_submit():
        user.email = eForm.email.data
        db.session.commit()
        return redirect(url_for('home', focus = "user"))
    else:
        flash("I'm sorry, we didn't quite get that...")
    return render_template('validate.html', user = user, eForm = eForm)


# @app.route('/professorLogin', methods = ['GET', 'POST'])
# def professorLogin():
#     form = professorLoginForm(prefix = "pForm")
#     eForm = emailForm(prefix = "eForm")
#     validCredentials = [#fake array of user - this will be many-to-many
# 		{
# 			'loginName': 'Ronald R Coifman',
# 			'password': 'CKT104'
# 		},
# 		{
# 			'loginName': 'Surjit K Chandhoke',
# 			'password': 'CKT304'
# 		},
# 		{
# 			'loginName': 'Weimin Zhong',
# 			'password': 'CKT404'
# 		},
# 		{
# 			'loginName': 'John Bargh',
# 			'password': 'CKT504'
# 		},
# 		{
# 			'loginName': 'Joshua Knobe',
# 			'password': 'CKT604'
# 		},
# 		{
# 			'loginName': 'Bryan A Ford',
# 			'password': 'CKT205'
# 		},
# 		{
# 			'loginName': 'James Aspnes',
# 			'password': 'CKT206'
# 		},
# 		{
# 			'loginName': 'Jane Levin',
# 			'password': 'CKT207'
# 		},
# 		{
# 			'loginName': 'Hilary Fink',
# 			'password': 'CKT208'
# 		},
# 		{
# 			'loginName': 'Virginia Jewiss',
# 			'password': 'CKT209'
# 		},
# 		{
# 			'loginName': 'Anthony Kronman',
# 			'password': 'CKT210'
# 		},
# 		{
# 			'loginName': 'Christopher Semk',
# 			'password': 'CKT211'
# 		},
# 		{
# 			'loginName': 'Katerina Simons',
# 			'password': 'CKT212'
# 		},
# 		{
# 			'loginName': 'Pinelopi Goldberg',
# 			'password': 'CKT214'
# 		},
# 		{
# 			'loginName': 'Aleh Tsyvinski',
# 			'password': 'CKT215'
# 		},
# 		{
# 			'loginName': 'William D Nordhaus',
# 			'password': 'CKT216'
# 		},
# 		{
# 			'loginName': 'Jose-Antonio Espin-Sanchez',
# 			'password': 'CKT217'
# 		},
# 		{
# 			'loginName': 'Joel Silverman',
# 			'password': 'CKT218'
# 		},
# 		{
# 			'loginName': 'Briallen E Hopper',
# 			'password': 'CKT219'
# 		},
# 		{
# 			'loginName': 'Barbara L Stuart',
# 			'password': 'CKT230'
# 		},
# 		{
# 			'loginName': 'John B Starr',
# 			'password': 'CKT232'
# 		},
# 		{
# 			'loginName': 'Paul Freedman',
# 			'password': 'CKT234'
# 		},
# 		{
# 			'loginName': 'John Wargo',
# 			'password': 'CKT236'
# 		},
# 		{
# 			'loginName': 'Anders Winroth',
# 			'password': 'CKT432'
# 		},
# 		{
# 			'loginName': 'Nicholas A Christakis',
# 			'password': 'CKT238'
# 		},
# 		{
# 			'loginName': 'Tim J Barringer',
# 			'password': 'CKT242'
# 		},
# 		{
# 			'loginName': 'Marketa Havlickova',
# 			'password': 'CKT244'
# 		},
# 		{
# 			'loginName': 'Robert J Bazell',
# 			'password': 'CKT246'
# 		},
# 		{
# 			'loginName': 'Francis Robinson',
# 			'password': 'CKT248'
# 		},
# 		{
# 			'loginName': 'Sarah M Demers Konezny',
# 			'password': 'CKT250'
# 		},
# 		{
# 			'loginName': 'C. Megan Urry',
# 			'password': 'CKT252'
# 		},
# 		{
# 			'loginName': 'Nuno P Monteiro',
# 			'password': 'CKT254'
# 		},
# 		{
# 			'loginName': 'Stephen Latham',
# 			'password': 'CKT256'
# 		},
# 		{
# 			'loginName': 'Laurie Santos',
# 			'password': 'CKT258'
# 		},
# 		{
# 			'loginName': 'Joseph T Chang',
# 			'password': 'CKT260'
# 		},
# 		{
# 			'loginName': 'Shikha Gupta',
# 			'password': 'BTU263'
# 		}]
# 	#Ronald R Coifman||Surjit K Chandhoke|| Weimin Zhong||John Bargh||Joshua Knobe||
# 	#Bryan A Ford||James Aspnes||Jane Levin||Hilary Fink||Virginia Jewiss||Anthony Kronman
# 	#||Christopher Semk||Katerina Simons||Pinelopi Goldberg||Aleh Tsyvinski
# 	#William D Nordhaus||Jose-Antonio Espin-Sanchez||Joel Silverman||Briallen E Hopper
# 	#Barbara L Stuart||John B Starr||Paul Freedman||John Wargo||Anders Winroth
# 	#Nicholas A Christakis||Tim J Barringer||Marketa Havlickova||Robert J Bazell||Francis Robinson
# 	#Sarah M Demers Konezny||C. Megan Urry||Nuno P Monteiro||Stephen Latham||Laurie Santos||Joseph T Chang
#     if g.user.is_anonymous() == False:
#         if g.user.role is not 1 and g.user.is_authenticated() is True:
# 	        return redirect(url_for('index'))
#     if eForm.validate_on_submit():
# 	    msg = Message('Professor Secret Key Request', sender='groopieco@gmail.com', recipients=['groopieco@gmail.com'])
# 	    msg.body = str(eForm.email.data)
# 	    mail.send(msg)
#     if form.validate_on_submit():
#         for vot in validCredentials:
#             vName = str(vot['loginName'])
#             vPass = str(vot['password'])
#             givenEmail = str(form.email.data)
#             if str(form.name.data) == vName and str(form.secretKey.data) == vPass:
#                 for u in User.query.all():
#                     if vName == u.nickname and u.role == ROLE_PROF:
#                         user = u
#                         u.email = givenEmail
#                         u.role = ROLE_PROF
#                         login_user(user, remember = True)
#                         return redirect(url_for('index'))
#                 crazy = User(nickname = vName, email = givenEmail, role = ROLE_PROF, karma = 100)
#                 db.session.add(crazy)
#                 db.session.commit()
#                 login_user(crazy, remember = True)
#                 return redirect(url_for('professorChoose', user_id = crazy.id))
#             else:
#                 holder = "nil"
#                 #flash("Sorry, those credentials aren't recognized")
#     return render_template('professor_login.html', validCredentials = validCredentials, form = form, eForm = eForm)


@app.route('/professorChoose/<user_id>', methods = ["GET", "POST"])
def professorChoose(user_id):
    fakeProfs = [
        {
			'fname': 'Alex Graham Bell',
			'fb_id': '103752899662780',
			'desc': 'An eminent Scottish-born scientist, inventor, engineer and innovator who is credited with inventing the first practical telephone'
		},
		{
			'fname': 'Richard Dawkins',
			'fb_id': '1376933789198289',
			'desc': 'An English ethologist, evolutionary biologist, and writer'
		},
		{
			'fname': 'Plato',
			'fb_id': '1423804244536441',
			'desc': 'A philosopher, as well as mathematician, in Classical Greece. He is considered an essential figure in the development of philosophy, especially the Western tradition.'
		},
		{
			'fname': 'Carl Sagan',
			'fb_id': '105499302815949',
			'desc': 'An American astronomer, cosmologist, astrophysicist, astrobiologist, author, science popularizer, and science communicator in astronomy and other natural sciences'
		},
		{
			'fname': 'Marie Curie',
			'fb_id': '103157713058424',
			'desc': 'A Polish and naturalized-French physicist and chemist who conducted pioneering research on radioactivity.'
		},
		{
			'fname': 'Isaac Newton',
			'fb_id': '108076819220176',
			'desc': 'An English physicist and mathematician who is widely recognised as one of the most influential scientists of all time and as a key figure in the scientific revolution.'
		},
		{
			'fname': 'Jane Goodall',
			'fb_id': '103860159652734',
			'desc': 'An English primatologist, ethologist, anthropologist, and UN Messenger of Peace'
		},
		{
			'fname': 'Susan B. Anthony',
			'fb_id': '103124393061163',
			'desc': "An American social reformer who played a pivotal role in the women's suffrage movement."
		},
		{
			'fname': 'Leonardo Da Vinci',
			'fb_id': '105978536100775',
			'desc': 'An Italian painter, sculptor, architect, musician, mathematician, engineer, inventor, anatomist, geologist, cartographer, botanist, and writer.'
		},
		{
			'fname': 'Albert Einstein',
			'fb_id': '12534674842',
			'desc': 'A German-born theoretical physicist and philosopher of science. He developed the general theory of relativity, one of the two pillars of modern physics.'
		},
		{
			'fname': 'Nikola Tesla',
			'fb_id': '112449748772539',
			'desc': 'A Serbian American inventor, electrical engineer, mechanical engineer, and futurist best known for his contributions to the design of the modern alternating current electricity supply system.'
		},
		{
			'fname': 'Immanuel Kant',
			'fb_id': '107408079288738',
			'desc': 'A German philosopher who is widely considered to be a central figure of modern philosophy. He argued that fundamental concepts structure human experience, and that reason is the source of morality.'
		},
		{
			'fname': 'Michael Faraday',
			'fb_id': '108002352561518',
			'desc': 'An English scientist who contributed to the fields of electromagnetism and electrochemistry. His main discoveries include those of electromagnetic induction, diamagnetism and electrolysis.'
		},
		{
			'fname': 'Hildegard of Bingen',
			'fb_id': '112741235406960',
			'desc': 'Also known as Saint Hildegard and Sibyl of the Rhine, was a German writer, composer, philosopher, Christian mystic, Benedictine abbess, visionary, and polymath.'
		},
		{
			'fname': 'Mary Wollstonecraft',
			'fb_id': '112291185450706',
			'desc': "An eighteenth-century English writer, philosopher, and advocate of women's rights."
		},
		{
			'fname': 'Jane Austen',
			'fb_id': '344695912224001',
			'desc': 'An English novelist whose works of romantic fiction, set among the landed gentry, earned her a place as one of the most widely read writers in English literature.'
		},
		{
			'fname': 'Eleanor Roosevelt',
			'fb_id': '103109173062350',
			'desc': "An American politician, diplomat, and activist. She was the longest-serving First Lady of the United States, holding the post from March 1933 to April 1945 during her husband President Franklin D. Roosevelt's four terms in office."
		}]
    user = User.query.filter_by(id = user_id).first()
    return render_template('professor_choose.html', fakeProfs = fakeProfs, user = user)

@app.route('/profBecome/<fakeID>/<userID>' , methods = ['GET', 'POST'])
def profBecome(fakeID, userID):
    fakeProfs = [
        {
			'fname': 'Alex Graham Bell',
			'fb_id': '103752899662780',
			'desc': 'An eminent Scottish-born scientist, inventor, engineer and innovator who is credited with inventing the first practical telephone'
		},
		{
			'fname': 'Richard Dawkins',
			'fb_id': '1376933789198289',
			'desc': 'An English ethologist, evolutionary biologist, and writer'
		},
		{
			'fname': 'Plato',
			'fb_id': '1423804244536441',
			'desc': 'A philosopher, as well as mathematician, in Classical Greece. He is considered an essential figure in the development of philosophy, especially the Western tradition.'
		},
		{
			'fname': 'Carl Sagan',
			'fb_id': '105499302815949',
			'desc': 'An American astronomer, cosmologist, astrophysicist, astrobiologist, author, science popularizer, and science communicator in astronomy and other natural sciences'
		},
		{
			'fname': 'Marie Curie',
			'fb_id': '103157713058424',
			'desc': 'A Polish and naturalized-French physicist and chemist who conducted pioneering research on radioactivity.'
		},
		{
			'fname': 'Isaac Newton',
			'fb_id': '108076819220176',
			'desc': 'An English physicist and mathematician who is widely recognised as one of the most influential scientists of all time and as a key figure in the scientific revolution.'
		},
		{
			'fname': 'Jane Goodall',
			'fb_id': '103860159652734',
			'desc': 'An English primatologist, ethologist, anthropologist, and UN Messenger of Peace'
		},
		{
			'fname': 'Susan B. Anthony',
			'fb_id': '103124393061163',
			'desc': "An American social reformer who played a pivotal role in the women's suffrage movement."
		},
		{
			'fname': 'Leonardo Da Vinci',
			'fb_id': '105978536100775',
			'desc': 'An Italian painter, sculptor, architect, musician, mathematician, engineer, inventor, anatomist, geologist, cartographer, botanist, and writer.'
		},
		{
			'fname': 'Albert Einstein',
			'fb_id': '12534674842',
			'desc': 'A German-born theoretical physicist and philosopher of science. He developed the general theory of relativity, one of the two pillars of modern physics.'
		},
		{
			'fname': 'Nikola Tesla',
			'fb_id': '112449748772539',
			'desc': 'A Serbian American inventor, electrical engineer, mechanical engineer, and futurist best known for his contributions to the design of the modern alternating current electricity supply system.'
		},
		{
			'fname': 'Immanuel Kant',
			'fb_id': '107408079288738',
			'desc': 'A German philosopher who is widely considered to be a central figure of modern philosophy. He argued that fundamental concepts structure human experience, and that reason is the source of morality.'
		},
		{
			'fname': 'Michael Faraday',
			'fb_id': '108002352561518',
			'desc': 'An English scientist who contributed to the fields of electromagnetism and electrochemistry. His main discoveries include those of electromagnetic induction, diamagnetism and electrolysis.'
		},
		{
			'fname': 'Hildegard of Bingen',
			'fb_id': '112741235406960',
			'desc': 'Also known as Saint Hildegard and Sibyl of the Rhine, was a German writer, composer, philosopher, Christian mystic, Benedictine abbess, visionary, and polymath.'
		},
		{
			'fname': 'Mary Wollstonecraft',
			'fb_id': '112291185450706',
			'desc': "An eighteenth-century English writer, philosopher, and advocate of women's rights."
		},
		{
			'fname': 'Jane Austen',
			'fb_id': '344695912224001',
			'desc': 'An English novelist whose works of romantic fiction, set among the landed gentry, earned her a place as one of the most widely read writers in English literature.'
		},
		{
			'fname': 'Eleanor Roosevelt',
			'fb_id': '103109173062350',
			'desc': "An American politician, diplomat, and activist. She was the longest-serving First Lady of the United States, holding the post from March 1933 to April 1945 during her husband President Franklin D. Roosevelt's four terms in office."
		}]
    #flash(fakeProfs[0]['fname'])
    #flash('gorram!')
    fakeID = int(fakeID)
    user = User.query.filter_by(id = userID).first()
    #user.nickname = fakeProfs[fakeID]['fname']
    user.fb_id = int(fakeProfs[fakeID]['fb_id'])
    db.session.commit()
    return redirect(url_for('index'))

# @app.route('/hack', methods = ['GET', 'POST'])
# def hack():
#     #return "FUCK"
#     users = User.query.all()
# 	#return redirect(url_for('index'))
#     userForm = fakeUserForm()
#     if userForm.validate_on_submit():
# 		#user = User(nickname = unicode(userForm.nickname.data), email = unicode(userForm.email.data), role = ROLE_USER, karma = 100)
# 		user = User(nickname = "f_n", email = "F_e", role = ROLE_USER, karma = 100)
# 		session['remember_me'] = userForm.remember_me.data
# 		db.session.add(user)
# 		db.session.commit()
# 		remember_me = session['remember_me']
# 		session.pop('remember_me', None)
# 		login_user(user, remember = remember_me)
# 		return redirect(url_for('index'))
#     return render_template('hack.html',
# 	users = users,
# 	userForm = userForm)





@app.route('/become/<UserId>')
def become(UserId):
	user = User.query.filter_by(id = UserId).first()
	login_user(user, remember = True)
	return redirect(url_for('index'))

@app.route('/deleteUser/<UserId>')
def deleteUser(UserId):
    user = User.query.filter_by(id = UserId).first()
    if user is not g.user:
        for c in user.comments:
            db.session.delete(c)
        db.session.commit()
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('hack'))




















# @app.route('/home/<focus>', methods = ["GET", "POST"])
# @login_required
# def home(focus):
# 	focus = str(focus)
# 	if focus  == "nil":
# 		return redirect(url_for("home", focus = "user"))
# 	user = g.user
# 	users = User.query.all()
# 	fav_users = user.followed.all()
# 	#flash(da_time.strftime('Day:%d**Month:%m**Year:%y--Second:%S**Minute:%M**Hour:%H'))
# 	return render_template("home.html",
# 	user = user,
# 	nowTime = da_time,
# 	users = users,
# 	fav_users = fav_users,
# 	send_time_string = send_time_string
# 	)

@app.route('/get_home_groops', methods = ["GET", "POST"])
def get_home_groops():
    return render_template('home_groops.html', nowTime = da_time)

@app.route('/get_home_comments', methods = ["GET", "POST"])
def get_home_comments():
	return render_template('home_comments.html')


@app.route('/get_home_contact', methods = ["GET", "POST"])
def get_home_contact():
    user = g.user
    return render_template('home_content.html', user = user)


@app.route('/get_home_ebook', methods = ["GET", "POST"])
def get_home_ebook():
    user = g.user
    return render_template('home_ebook.html', user = user)

@app.route('/get_home_store', methods = ["GET", "POST"])
def get_home_store():
    return render_template('home_store.html')

@app.route('/get_person_available_karma', methods = ["GET", "POST"])
def get_person_available_karma():
    #var = int(g.user.get_total_likes - g.user.spent_karma)
    return "GOt it"

@app.route('/purchase_item', methods = ["GET", "POST"])
def purchase_item():
    itemTitle = str(request.form['item_title'])
    itemCost = int(request.form['item_cost'])
    fullMessage = itemTitle + "<br><br>" + g.user.nickname + "<br><br><br>" + g.user.email
    msg = Message('Groopie Store Request', sender='groopieco@gmail.com', recipients=['groopieco@gmail.com', 'rijul.gupta@yale.edu', 'james.park.jp858@yale.edu'])
    msg.body = fullMessage
    mail.send(msg)
    g.user.spent_karma += itemCost
    db.session.commit()
    return "Thank you, we have recieved your request. You will get an email soon!"













@app.route('/send_comment', methods = ["GET", "POST"])
def send_comment():
    fullMessage = str(request.form['sent_message'])
    userEmail = str(request.form['user_email'])
    msg = Message('Groopie Ebook Request', sender='groopieco@gmail.com', recipients=['groopieco@gmail.com', 'rijul.gupta@yale.edu', 'james.park.jp858@yale.edu'])
    msg.body = fullMessage
    mail.send(msg)


# @app.route('/upvoteComment/<commentId>')
# @login_required
# def upvoteComment(commentId):
# 	user = g.user
# 	comment = Comment.query.filter_by(id = commentId).first()
# 	comment.did_like(user)
# 	return redirect(request.referrer)
# 	#return redirect(url_for('event', eventID = comment.get_eventID()))
# 	if comment.has_upboat(user) == 0:
# 		flash("You Upvoted")
# 	else:
# 		flash("You have already upvoted this comment")

# @app.route('/downvoteComment/<commentId>')
# @login_required
# def downvoteComment(commentId):
# 	user = g.user
# 	comment = Comment.query.filter_by(id = commentId).first()
# 	comment.did_unlike(user)
# 	return redirect(request.referrer)
# 	#return redirect(url_for('event', eventID = comment.get_eventID()))
# 	if comment.has_upboat(user) != 0:
# 		flash("You Unliked this comment")
# 	else:
# 		flash("You have already upvoted this comment")







#####AJAX#####
# def allowed_file(filename):
#     return '.' in filename and \
#           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS




@app.route('/followUser', methods = ["GET", "POST"])
def followUser():
	checker = int(request.form['id_send'])
	var = jsonify({
	'text': '<h2> You are now following this event - {.?.{user.nickname}.?.}</h2>'
	})
	user = g.user
	fUser = User.query.filter_by(id = checker).first()
	user.follow(fUser)
	db.session.commit()
	#flash(event.title)
	return "done"

@app.route('/unfollowUser', methods = ["GET", "POST"])
def unfollowUser():
	checker = int(request.form['id_send'])
	var = jsonify({
	'text': '<h2> You are now following this event - {.?.{user.nickname}.?.}</h2>'
	})
	user = g.user
	fUser = User.query.filter_by(id = checker).first()
	user.unfollow(fUser)
	db.session.commit()
	#flash(event.title)
	return "done"























@app.route('/get_user_comments', methods = ["GET", "POST"])
def get_user_comments():
	uVar = int(request.form['id_send'])
	commingFrom = str(request.form['from'])
	user = User.query.filter_by(id = uVar).first()
	num_comments = int(request.form['num'])
	num_c_top = 10
	total_comments_length = len(user.get_top_comments())
	if total_comments_length < (num_comments+num_c_top):
		num_c_top = (num_comments + num_c_top) - total_comments_length
	retStr = "</br>"
	#return str
	checker = 0
	#[5:] this cuts out the top 5 comments
	#[:5] this gives the top 5 out of the remaining list
	for c in user.get_top_comments()[num_comments:][:(num_c_top)]:
		retStr += render_template('comment_preview_small.html' , c = c)
		checker = 1
	if checker == 0:
		retStr = "No comments yet.."
	else:
		if num_c_top != total_comments_length:
			if commingFrom == "user_display":
				wtfstring1 = "'comments'"
				wtfstring2 = "'"+str(uVar)+"'"
				retStr += '<div id="load_more_c_2_'+str(num_comments+ num_c_top)+'" ><h2  onclick="javascript:user_display('+wtfstring1+','+wtfstring2+','+str(num_comments + num_c_top)+')"> Load More </h2></div>'
				#retStr += '<div id="load_more_c_'+str(num_comments+ num_c_top)+'" ><h2  onclick="javascript:user_display("comments","'+str(uVar)+'",'+str(num_comments + num_c_top)+')"> Load More </h2></div>'
			else:
				retStr += '<div id="load_more_c_'+str(num_comments+ num_c_top)+'" ><h2  onclick="javascript:'+commingFrom+'('+str(num_comments + num_c_top)+')"> Load More </h2></div>'
		else:
			retStr += '<div id="load_more_c_'+str(num_comments+ num_c_top)+'" ><h2  onclick=""> No More </h2></div>'
	return retStr


@app.route('/get_friends_comments', methods = ["GET", "POST"])
def get_friends_comments():
	user = g.user
	str = "</br>"
	checker = 0
	for c in user.get_friends_comments():
		str += render_template('comment_preview_small.html' , c = c)
		checker = 1
	if checker == 0:
		str = "No comments yet.."
	return str








# @app.route('/get_top_comments2', methods=["GET", "POST"])
# def get_top_comments2():
#     period_id = int(request.form['on_period'])
#     on_period = Period.query.filter_by(id = period_id).first()
#     first_level_coms = on_period.children_comments.filter_by(depth = 1).all()
#     first_level_coms = sorted(first_level_coms, key=lambda Comment:Comment.get_likes(), reverse=True)
#     retStr = ""
#     for c in first_level_coms:
#         retStr += give_comment_template(c)
#     return retStr

# def give_comment_template(c):
#     retS = render_template('commentPreview.html', c = c)
#     retS += "<div id='comment_"+str(c.id)+"_children_holder' style='max-height:10000px; overflow:visible;'>"
#     for k in c.reply_comments:
#         retS += give_comment_template(k)
#     retS += "</div>"
#     return retS




# @app.route('/get_comments_by_round', methods = ["GET", "POST"])
# def get_comments_by_round():
#     period_id = int(request.form['on_period'])
#     round_int = int(request.form['send_round'])
#     period = Period.query.filter_by(id = period_id).first()
#     sent_comments = period.get_comments()
#     retString = ""
#     num_c_top = 5
#     total_comments_length = len(sent_comments)
#     num_comments = total_comments_length - num_c_top*round_int
#     if num_comments <= -1*num_c_top:
#         retString = "<h3 style='' id='get_comments_by_round_more_button' onclick=''>No More Comments...</h3>"
#     else:
#         if num_comments < 0:
#             num_comments = 0
#         retString += "<h3 style='' id='get_comments_by_round_more_button' onclick='javascript:get_comments_by_round("+str(round_int + 1)+");'>Load More Comments</h3>"
#     final_comments = sent_comments[num_comments:][:(num_c_top)]
#     #if total_comments_length < (num_comments+num_c_top):
#     #    num_c_top = (num_comments + num_c_top) - total_comments_length
# 	#[5:] this cuts out the top 5 comments
# 	#[:5] this gives the top 5 out of the remaining list
# 	#for c in sent_comments[num_comments:][:(num_c_top)]:
#     for c in final_comments:
#         retString += give_comment_template(c)
#     if round_int == 1:
#         retString+= "*&&*"
#         retString+= str(period.children_comments.order_by('-id').first().id)
#     return retString

# @app.route('/update_comments', methods=["GET", "POST"])
# def update_comments():
#  	period_id = int(request.form['period_id'])
#  	on_period = Period.query.filter_by(id = period_id).first()
#  	sent_comms = Comment.query.filter_by(period_id = on_period.id).all()
#  	user = g.user
#  	submitForm = submitCommentForm()
# 	return render_template('comments_new.html', on_period = on_period, user = user, form = submitForm)

# @app.route('/get_new_comments', methods = ["GET", "POST"])
# def get_new_comments():
# 	timeString = str(request.form['da_time'])#1:DD**2:MM**3:YY--4:ss**5:mm**6:hh
# 	newTime = datetime.strptime(timeString, "1:%d**2:%m**3:%y--4:%S**5:%M**6:%H") - timedelta(seconds=2)
# 	retStr = ""
# 	pNum = int(request.form['on_period'])
# 	newComs = Comment.query.filter(Comment.atTime > newTime).filter(Comment.depth == 1).filter_by(period_id = pNum).all()
# 	newReps = Comment.query.filter(Comment.atTime > newTime).filter(Comment.depth > 1).filter_by(period_id = pNum).all()
# 	for r in newReps:
# 		if r.user_id is not g.user.id:
# 			retStr += str(r.id)
# 			retStr += "^^&^^" #^^&^^ is the separator key
# 	retStr += "*++*"#'*++*' is the separator key
# 	for c in newComs:
# 		if c.user_id is not g.user.id:
# 		#if 1 == 1:
# 			retStr += render_template('commentPreview.html', c = c, isNew = True)
# 			#retStr += '<div id="comment_'+str(c.id)+'_children_holder" style="">'
# 	return retStr






# @app.route('/get_new_comments_id', methods = ["GET", "POST"])
# def get_new_comments_id():
# 	most_recent_id = "none"
# 	if str(request.form['da_id']) != "none":
# 		most_recent_id = int(request.form['da_id'])
# 	timeString = str(request.form['da_time'])#1:DD**2:MM**3:YY--4:ss**5:mm**6:hh
# 	newTime = datetime.strptime(timeString, "1:%d**2:%m**3:%y--4:%S**5:%M**6:%H")
# 	retStr = ""
# 	pNum = int(request.form['on_period'])
# 	on_p = Period.query.filter_by(id = pNum).first();
# 	checkComs = [] #holds all comments
# 	if on_p.children_comments:
# 			checkComs = on_p.children_comments.order_by(db.asc(Comment.atTime)).all()
# 	#if most_recent_id != "none":
# 	#	checkComs = on_p.children_comments.order_by(db.asc(Comment.atTime)).all()
# 	#elif on_p.children_comments:
# 	#	checkComs = on_p.children_comments.order_by(db.asc(Comment.atTime)).all()
# 	newComs = []#will hold all depth = 1 comments
# 	newReps = []#holds comments of depth > 1
# 	repChecker = 0
# 	idSender = "none"
# 	if checkComs:
# 		if str(most_recent_id) == "none":
# 			repChecker = 1
# 		idSender = str(checkComs[-1].id)
# 		for c in checkComs:
# 			if c.id == most_recent_id:
# 				repChecker = 1
# 			if repChecker == 1 and c.id != most_recent_id:
# 				if c.depth == 1:
# 					newComs.append(c)
# 				if c.depth > 1:
# 					newReps.append(c)
# 	# newComs = Comment.query.filter(Comment.depth == 1).filter_by(period_id = pNum).order_by(Comment.atTime).all()
# # 	newReps = Comment.query.filter(Comment.depth > 1).filter_by(period_id = pNum).order_by(Comment.atTime).all()
# # 	repChecker = 0
# 	for r in newReps:
# 		if str(most_recent_id) == "none":
# 			retStr += str(r.id)
# 			retStr += "^^&^^" #^^&^^ is the separator key
# 		else:
# 			if r.user_id is not g.user.id:
# 				retStr += str(r.id)
# 				retStr += "^^&^^" #^^&^^ is the separator key
# 	retStr += "*++*"#'*++*' is the separator key
# 	for c in newComs:
# 		if str(most_recent_id) == "none":
# 		    retStr += give_comment_template(c)
# 			#retStr += render_template('commentPreview.html', c = c, isNew = True)
# 		else:
# 			if c.user_id is not g.user.id:
# 			#if 1 == 1:
# 			    retStr += give_comment_template(c)
# 				#retStr += render_template('commentPreview.html', c = c, isNew = True)
# 				#retStr += '<div id="comment_'+str(c.id)+'_children_holder" style=""></div>'
# 	retStr +="*++*"
# 	retStr += idSender
# 	return retStr






# @app.route('/get_new_replies', methods = ["GET", "POST"])
# def get_new_replies():
# 	child_id = int(request.form['comment_id'])
# 	child_comment = Comment.query.filter_by(id = child_id).first()
# 	if child_comment.depth == 1:
# 		return ""
# 	else:
# 		parent_id = str(child_comment.parent_id)
# 		retStr = parent_id
# 		retStr += "*++*" #separator key
# 		retStr += give_comment_template(child_comment)
# 		#retStr += render_template('commentPreview.html', c = child_comment, isNew = True)
# 		return retStr


# # @app.route('/get_now_time', methods = ["GET", "POST"])
# # def get_now_time():
# # 	tToS = datetime.now() - timeChanger
# # 	newTimeString = da_time.strftime('Day:%d**Month:%m**Year:%y--Second:%S**Minute:%M**Hour:%H')
# # 	return newTimeString

# @app.route('/get_reply_form', methods=["GET", "POST"])
# def get_reply_form():
#  	reply_id_num = int(request.form['reply_id'])
#  	reply_form = submitReplyForm(prefix="rForm")
# 	return render_template('comment_reply_form.html', reply_form = reply_form, reply_id_num = reply_id_num)


# @app.route('/submit_comment', methods = ["GET", "POST"])
# def submit_comment():
# 	period_id_num = int(request.form['period_id'])
# 	cText = str(request.form['comment_text'])
# 	tttTime = str(request.form['time_sent'])
# 	recTime = datetime.strptime(tttTime, "1:%d**2:%m**3:%y--4:%S**5:%M**6:%H")
# 	period = Period.query.filter_by(id = period_id_num).first()
# 	c = Comment(body = cText, period_id = period.id, user_id = g.user.id, atTime = recTime)
# 	db.session.add(c)
# 	period.children_comments.append(c)
# 	g.user.comments.append(c)
# 	db.session.commit()
# 	retStr = ""
# 	retStr += give_comment_template(c)
# 	#retStr += render_template('commentPreview.html', c = c, isNew = True)
# 	#retStr += '<div id="comment_'+str(c.id)+'_children_holder" style=""></div>'
# 	str2 = "Period:" + str(period.id) + "--Comment:" + cText
# 	return retStr


# @app.route('/submit_comment_reply', methods = ["GET", "POST"])
# def submit_comment_reply():
# 	c_id_num = int(request.form['comment_id'])
# 	rText = str(request.form['reply_text'])
# 	tttTime = str(request.form['time_sent'])
# 	recTime = datetime.strptime(tttTime, "1:%d**2:%m**3:%y--4:%S**5:%M**6:%H")
# 	reply_com = Comment.query.filter_by(id = c_id_num).first()
# 	on_period = Period.query.filter_by(id = reply_com.period_id).first()
# 	c = Comment(body = rText, period_id = reply_com.period_id, user_id = g.user.id, parent_id = reply_com.id, atTime = recTime)
# 	db.session.add(c)
# 	reply_com.reply_comments.append(c)
# 	on_period.children_comments.append(c)
# 	g.user.comments.append(c)
# 	c.set_depth()
# 	db.session.commit()
# 	retStr = give_comment_template(c)
# 	#retStr = render_template('commentPreview.html', c = c)
# 	#retStr +='<div id="comment_'+str(c.id)+'_children_holder" style=""></div>'
# 	return retStr


















# @app.route('/search', methods=['POST'])
# @login_required
# def search():
#     if not g.search_form.validate_on_submit():
#         return redirect(url_for('index'))
#     return redirect(url_for('search_results', query=g.search_form.search.data))



# from config import MAX_SEARCH_RESULTS

# @app.route('/search_results/<query>')
# @login_required
# def search_results(query):
#     results = Event.query.order_by(db.desc(Event.title)).whoosh_search(query, MAX_SEARCH_RESULTS).all()
#     return render_template('search_results.html',
#                           query=query,
#                           results=results,
#                           user = g.user)


# @app.route('/get_search_groops', methods = ["GET", "POST"])
# def get_search_groops():
# 	query = str(request.form['get_query'])
# 	results = Event.query.order_by(db.desc(Event.title)).whoosh_search(query, MAX_SEARCH_RESULTS).all()
# 	#return "GOD FUCKING DAMN IT!"
# 	return render_template('search_groops.html', results = results, user = g.user)

# @app.route('/get_search_users', methods = ["GET", "POST"])
# def get_search_users():
# 	query = str(request.form['get_query'])
# 	results = User.query.order_by(db.desc(User.nickname)).whoosh_search(query, MAX_SEARCH_RESULTS).all()
# 	#return "GOD FUCKING DAMN IT!"
# 	return render_template('search_users.html', results = results, user = g.user)

# @app.route('/get_search_comments', methods = ["GET", "POST"])
# def get_search_comments():
# 	query = str(request.form['get_query'])
# 	results = Comment.query.order_by(db.desc(Comment.atTime)).whoosh_search(query, MAX_SEARCH_RESULTS).all()
# 	#return "GOD FUCKING DAMN IT!"
# 	return render_template('search_comments.html', results = results, user = g.user)



# @login_manager.unauthorized_handler
# def unauthorized_callback():
#     return redirect(url_for('index'))



# function getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2) {
#   var R = 6371; // Radius of the earth in km
#   var dLat = deg2rad(lat2-lat1);  // deg2rad below
#   var dLon = deg2rad(lon2-lon1);
#   var a =
#     Math.sin(dLat/2) * Math.sin(dLat/2) +
#     Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
#     Math.sin(dLon/2) * Math.sin(dLon/2)
#     ;
#   var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
#   var d = R * c; // Distance in km
#   return d;
# }

# function deg2rad(deg) {
#   return deg * (Math.PI/180)
# }
import math

def getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2):
  R = 6371 # Radius of the earth in km
  dLat = deg2rad(lat2-lat1) #deg2rad below
  dLon = deg2rad(lon2-lon1)
  a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  d = R * c * 1000.00 # Distance in m
  return d


def deg2rad(deg):
  return deg * (math.pi/180)


def get_comment_template(c, user):
    if c.author is not None:
        aString = str(c.author.nickname.encode('utf-8'))
        uId = str(c.author.fb_id)
    else:
        aString = "none"
        uId = "none"
    if c.locationAddress is not None:
        locString = c.locationAddress
    else:
        locString = "nil"
    if c.has_liked(user) == True:
        likedString = "yes"
    else:
        likedString = "no"
    if c.imgLink is None:
        imgString = "none"
        testType = "1"
    else:
        imgString = c.imgLink
        testType = "2"
        if imgString == "none":
            testType = "1"
    if c.atTime is None:
        timeString = "none"
        dateString = "none"
    else:
        timeString = c.getAtTime()
        dateString = c.getDate()
    numComString = str(c.reply_comments.count())
        #cString = str(c.body)
    cString = c.body.decode('unicode-escape')
    hString = str(c.get_likes())
    postHashtags = []
    hashtagTitles = []
    comHashs = c.hashtags
    for h in comHashs:
        hashtag = {"body":h.body, "id":str(h.id)}
        postHashtags.append(hashtag)
        hashtagTitles.append(h.body)
    fake_c = {'hearts':hString, 'has_liked':likedString, 'author':aString, 'user_id':uId, 'comments':cString, 'c_id':str(c.id), 'location':locString, 'image':imgString, 'time':timeString, 'date':dateString, 'numComments':numComString, 'type':testType, 'hashtags':postHashtags, 'hashtagTitles':hashtagTitles}
    return fake_c

# def get_fake_post():
#     c = Comment.query.filter_by(id = 201).first()
#     u2 = User.query.filter_by(nickname = "Johnny Apples").first()
#     aString = u2.nickname
#     uId = u2.id
#     if c.has_liked(user) == True:
#         likedString = "yes"
#     else:
#         likedString = "no"
#     if c.imgLink is None:
#         imgString = "none"
#     else:
#         imgString = c.imgLink
#     if c.atTime is None:
#         timeString = "none"
#     else:
#         timeString = c.getAtTime()
#     numComString = str(c.reply_comments.count())
#     fake_c = {'hearts':'0', 'has_liked':likedString, 'author':aString, 'user_id':uId, 'comments':cString, 'c_id':str(c.id), 'location':'Nearby', 'image':imgString, 'time':'now', 'numComments':0}


@app.route("/mobile_user_flagged", methods = ["GET", "POST"])
def mobile_user_flagged():
    c_id = str(request.json['c_id'])
    author = str(request.json['author'])
    author_fbid = str(request.json['fbid'])
    return "done"

@app.route("/mobile_user_delete_comment", methods = ["GET", "POST"])
def mobile_user_delete_comment():
    c_id = str(request.json['c_id'])
    #print("THE FUCKING CID")
    #print(c_id)
    #author = str(request.json['author'])
    author_fbid = str(request.json['fbid'])
    gUser_id = str(request.json['g_fbid'])
    gUser = User.query.filter_by(fb_id = gUser_id).first()
    c = Comment.query.filter_by(id = int(c_id)).first()
    #print(c.body)
    if c.author is gUser:
        db.session.delete(c)
        db.session.commit()
    return jsonify(results = "done")

@app.route('/mobile_user_block', methods = ["GET", "POST"])
def mobile_user_block():
    gUserId = int(request.json['gUser_fbID'])
    gUser = User.query.filter_by(fb_id = gUserId).first()
    inqUserId = int(request.json['iUser_fbID'])
    inqUser = User.query.filter_by(fb_id = inqUserId).first()
    retString = [{'value':'done'}]
    return jsonify(results = retString)

@app.route("/mobile_user_get_connection_status", methods = ["GET", "POST"])
def mobile_user_get_connection_status():
    gid = str(request.json['gfb_id'])
    rid = str(request.json['fb_id'])
    gUser = User.query.filter_by(fb_id = gid).first()
    rUser = User.query.filter_by(fb_id = rid).first()
    status = gUser.get_status(rUser)
    return jsonify(results = status)

@app.route("/mobile_user_request_friend", methods = ["GET", "POST"])
def mobile_user_request_friend():
    gid = str(request.json['gfbid'])
    rid = str(request.json['rfbid'])
    gUser = User.query.filter_by(fb_id = gid).first()
    rUser = User.query.filter_by(fb_id = rid).first()
    gUser.request_friend(rUser)
    create_notification(u1 = rUser, u2 = gUser, c1 = None, r1 = None,  typeN = 5, latLon = None)
    return jsonify(results = "done")

@app.route("/mobile_user_confirm_friend", methods = ["GET", "POST"])
def mobile_user_confirm_friend():
    gid = str(request.json['gfbid'])
    rid = str(request.json['rfbid'])
    gUser = User.query.filter_by(fb_id = gid).first()
    rUser = User.query.filter_by(fb_id = rid).first()
    gUser.add_friend(rUser)
    create_notification(u1 = rUser, u2 = gUser, c1 = None, r1 = None,  typeN = 6, latLon = None)
    return jsonify(results = "done")


@app.route("/test_mobile_ajax", methods = ["GET", "POST"])
def test_mobile_ajax():
    retString = str("blah blah Blah")
    #query = str(request.form['username'])
    query = str(request.json['username'])
    return jsonify(username = retString, test = query)

import threading
import subprocess
import uuid
from flask import abort

background_scripts = {}


@app.route("/recieve_fbfriends_list", methods = ["GET", "POST"])
def recieve_fbfriends_list():
    daUserId = str(request.json['fbid'])
    user = User.query.filter_by(fb_id = daUserId).first()
    if user is None:
        user = mobile_create_user(daUserId)
    daList = str(request.json['ffList'])
    user.fbfriends = daList
    db.session.commit()
    id = str(uuid.uuid4())
    background_scripts[id] = False
    #user = User.query.filter_by(nickname = "Jimmy Park").first()
    #threading.Thread(target=lambda: get_friends_script(id, user)).start()
    print(daList)
    return jsonify(results = "done")

@app.route('/web_create_hashtag', methods = ["GET", "POST"])
def web_create_hashtag():
    return render_template('newHashtag.html')

@app.route('/get_hashtags', methods = ["GET", "POST"])
def get_hashtags():
    print("USER DID GET HASHTAGS")
    hashtags = Hashtag.query.all()
    return render_template('allHashtags.html', hashtags = hashtags)

@app.route('/delete_hashtag', methods = ["GET", "POST"])
def delete_hashtag():
    idnum = int(request.form['hashtagid'])
    h = Hashtag.query.filter_by(id = idnum).first()
    db.session.delete(h)
    db.session.commit()
    return "done"



@app.route('/create_new_hashtag_send', methods = ["GET", "POST"])
def create_new_hashtag_send():
    hashtag = str(request.form['hashtagBody'])
    newH = Hashtag(body = str(hashtag))
    db.session.add(newH)
    db.session.commit()
    return "done"


@app.route('/mobile_user_add_hashtag', methods = ["GET", "POST"])
def mobile_user_add_hashtag():
    hashId = int(request.json['hashId'])
    userId = int(request.json['gfbid'])
    h = Hashtag.query.filter_by(id = hashId).first()
    u = User.query.filter_by(fb_id = userId).first()
    print(u.nickname)
    h.add_user(u)
    db.session.commit()
    retString = [{"done":"yes"}]
    return jsonify(results = retString)

@app.route('/mobile_user_get_hashtags', methods = ["GET", "POST"])
def mobile_user_get_hashtags():
    userId = int(request.json['fb_id'])
    u = User.query.filter_by(fb_id = userId).first()
    u.setRecTime()
    hashtags = u.hashtags
    retString = []
    for h in hashtags:
        hashtag = {"body":h.body, "id":str(h.id)}
        retString.append(hashtag)
    return jsonify(results = retString)

@app.route('/mobile_user_get_mutual_friends', methods = ["GET", "POST"])
def mobile_user_get_mutual_friends():
    guserId = int(request.json['gfb_id'])
    ruserId = int(request.json['fb_id'])
    guser = User.query.filter_by(fb_id = guserId).first()
    ruser = User.query.filter_by(fb_id = ruserId).first()
    return jsonify(results = "22")

@app.route('/mobile_user_submit_dm', methods = ["GET", "POST"])
def mobile_user_submit_dm():
    guserId = int(request.json['gfbid'])
    ruserId = int(request.json['rfbid'])
    message = request.json['message']
    uniCodeBody = message.encode('unicode_escape')
    guser = User.query.filter_by(fb_id = guserId).first()
    guser.setRecTime()
    ruser = User.query.filter_by(fb_id = ruserId).first()
    d = DirectMessage(body = uniCodeBody, user_id = guser.id, receiver_id = ruser.id, atTime = datetime.now())
    #d1 = models.DirectMessage(body = "Test TEST test2", user_id = guser.id, receiver_id = ruser.id, atTime = datetime.now())
    #d = Message(checkit = "IJFIJFIJF")#guser.id)#, reciever_id = ruser.id, atTime = datetime.now())
    db.session.add(d)
    guser.sentMessages.append(d)
    ruser.receivedMessages.append(d)
    db.session.commit()
    create_notification(u1 = ruser, u2 = guser, c1 = None, r1 = None,  typeN = 7, latLon = None)
    #create_notification(u1 = comPar.author, u2 = user, c1 = comPar, r1 = c,  typeN = 3, latLon = None)
    #c = Comment(body = uniCodeBody, user_id = user.id, atTime = datetime.now(), latLon = recieved_latlong, depth = 1, imgLink = imgLink, bodyUni = uniCodeBody)
    return jsonify(results = str(d.id))

@app.route('/mobile_user_get_messages', methods = ["GET", "POST"])
def mobile_user_get_messages():
    guserId = int(request.json['gfbid'])
    ruserId = int(request.json['rfbid'])
    guser = User.query.filter_by(fb_id = guserId).first()
    ruser = User.query.filter_by(fb_id = ruserId).first()
    coms = guser.get_messages(ruser)
    coms = sorted(coms, key=lambda DirectMessage:DirectMessage.atTime, reverse=False)
    retString = []
    for c in coms:
        type = "1"
        if c.author.id == guser.id:
            type = "1"
        else:
            type = "2"
        m = {'message':c.body.decode('unicode-escape'), 'type':type, 'id':str(c.id)}
        retString.append(m)
    return jsonify(results = retString)

@app.route('/mobile_user_get_new_messages', methods = ["GET", "POST"])
def mobile_user_get_new_messages():
    guserId = int(request.json['gfbid'])
    ruserId = int(request.json['rfbid'])
    recentId = int(request.json['mostRecentCommentId'])
    guser = User.query.filter_by(fb_id = guserId).first()
    ruser = User.query.filter_by(fb_id = ruserId).first()
    coms = guser.get_messages(ruser)
    #coms = coms.filter_by(id > recentId).all()
    coms = [c for c in coms if c.id > recentId]
    retString = []
    for c in coms:
        type = "1"
        if c.author.id == guser.id:
            type = "1"
        else:
            type = "2"
        m = {'message':c.body, 'type':type, 'id':str(c.id)}
        retString.append(m)
    return jsonify(results = retString)

@app.route('/mobile_user_get_fake_messages', methods = ["GET", "POST"])
def mobile_user_get_fake_messages():
    authorName = "Rijul"
    authorName2 = "Jimmy"
    fakeUser = User.query.filter_by(nickname = "Rijul Gupta").first()
    fakeUser2 = User.query.filter_by(nickname = "Jimmy Park").first()
    authorFBID = str(fakeUser.fb_id)
    authorFBID2 = str(fakeUser2.fb_id)
    messageContent = "ifjifif if ifj ifj ifj if if ijf"
    retString = []
    m1 = {'authorName':authorName, 'authorFBID':authorFBID, 'message':'Hey man, what"s going ?', 'type':'1'}
    m2 = {'authorName':authorName2, 'authorFBID':authorFBID2, 'message':'Not much dude. Cool profile.', 'type':'2'}
    m3 = {'authorName':authorName, 'authorFBID':authorFBID, 'message':'Thanks, yeah, I like yours too. What classes are you taking?', 'type':'1'}
    m4 = {'authorName':authorName2, 'authorFBID':authorFBID2, 'message':'I am taking blah blah blah blah blah. Also, this and that and another thing. I want to make sure this comment is long as hell, just so we can test functionality.', 'type':'2'}
    m5 = {'authorName':authorName, 'authorFBID':authorFBID, 'message':'Hey man, what"s going ?', 'type':'1'}
    m6 = {'authorName':authorName2, 'authorFBID':authorFBID2, 'message':'Not much dude. Cool profile.', 'type':'2'}
    m7 = {'authorName':authorName, 'authorFBID':authorFBID, 'message':'Thanks, yeah, I like yours too. What classes are you taking?', 'type':'1'}
    m8 = {'authorName':authorName2, 'authorFBID':authorFBID2, 'message':'I am taking blah blah blah blah blah. Also, this and that and another thing. I want to make sure this comment is long as hell, just so we can test functionality.', 'type':'2'}
    m9 = {'authorName':authorName, 'authorFBID':authorFBID, 'message':'Hey man, what"s going ?', 'type':'1'}
    m10 = {'authorName':authorName2, 'authorFBID':authorFBID2, 'message':'Not much dude. Cool profile.', 'type':'2'}
    m11 = {'authorName':authorName, 'authorFBID':authorFBID, 'message':'Thanks, yeah, I like yours too. What classes are you taking?', 'type':'1'}
    m12 = {'authorName':authorName2, 'authorFBID':authorFBID2, 'message':'I am taking blah blah blah blah blah. Also, this and that and another thing. I want to make sure this comment is long as hell, just so we can test functionality.', 'type':'2'}
    retString.append(m1)
    retString.append(m2)
    retString.append(m3)
    retString.append(m4)
    retString.append(m5)
    retString.append(m6)
    retString.append(m7)
    retString.append(m8)
    retString.append(m9)
    retString.append(m10)
    retString.append(m11)
    retString.append(m12)
    # for i in range(10):
    #     userInfo = {'authorName':authorName, 'authorFBID':authorFBID,  'message':messageContent}
    #     retString.append(userInfo)
    return jsonify(results = retString)

@app.route('/testticals', methods = ["GET", "POST"])
def testticals():
    return 'done'

@app.route('/mobile_get_hashtags', methods = ["GET", "POST"])
def mobile_get_hashtags():
    retString = []
    for h in Hashtag.query.filter(Hashtag.id != 17).all():
        hashtag = {"body":h.body, "id":str(h.id)}
        retString.append(hashtag)
    return jsonify(results = retString)

@app.route('/mobile_get_hashtags_for_user', methods = ["GET", "POST"])
def mobile_get_hashtags_for_user():
    gUserId = int(request.json['gfbid'])
    gUser = User.query.filter_by(fb_id = gUserId).first()
    if gUser is None:
        gUser = mobile_create_user(gUserId)
    retString = []
    hashes = set(Hashtag.query.all()) - set(gUser.hashtags)
    for h in hashes:
        hashtag = {"body":h.body, "id":str(h.id)}
        retString.append(hashtag)
    return jsonify(results = retString)

@app.route('/mobile_get_people', methods = ["GET", "POST"])
def mobile_get_people():
    gUserId = int(request.json['gfbid'])
    gUser = User.query.filter_by(fb_id = gUserId).first()
    if gUser is None:
        gUser = mobile_create_user(gUserId)
    gUser.setRecTime()
    users = User.query.filter(User.id != gUser.id).all()#[:20]
    users = sorted(users, key=lambda User:User.recTime, reverse=True)[:20]
    retString = []
    hashs = Hashtag.query.all()
    hbs = []
    for h in hashs:
        hbs.append(h.body)
    for u in users:
        uID = str(u.fb_id)
        uName = str(u.nickname.encode('utf-8'))
        uFollow = "yes"
        uStatus = gUser.get_status(u)
        uHashtags = []
        uHashs = u.hashtags
        if uHashs is not None:
            for uh in uHashs:
                uHashtags.append(str(uh.body))
            if uHashs.count() == 0:
                uHashtags.append("#NoHashtags")
        else:
            uHashtags.append("#NoHashtags")
        # h1 = random.choice(hbs)
        # #hbs = hbs.remove(h1)
        # h2 = random.choice(hbs)
        # #hbs = hbs.remove(h2)
        # h3 = random.choice(hbs)
        # h4 = random.choice(hbs)
        # h5 = random.choice(hbs)
        # h6 = random.choice(hbs)
        # #hbs.remove(h3)
        # uHashtags.append(str(h1))
        # uHashtags.append(str(h2))
        # uHashtags.append(str(h3))
        # uHashtags.append(str(h4))
        # uHashtags.append(str(h5))
        # uHashtags.append(str(h6))
        #uHashtags.append("#"+str(u.get_total_likes()))
        #uHashtags.append("#"+str(u.fb_id))
        #uHashtags.append("#"+str(u.email))
        mutualFriends = str(randint(12, 32))
        #if gUser.is_following(u) is True:
       #     uFollow = "yes"
        #else:
        #    uFollow = "no"
        userInfo = {'userID':uID, 'userName':uName, 'userFollow':uFollow, 'hashtags':uHashtags, 'friends':mutualFriends, 'userStatus':uStatus}
        retString.append(userInfo)
    return jsonify(results = retString)

@app.route('/showComs', methods = ["GET", "POST"])
def showComs():
    retString = ""
    allCom = Comment.query.all()
    retString += "BODIES"
    for c in allCom:
        retString += c.body
        retString += "<br><br>"
    retString += "<br><br><br><br>"
    retString += "Locations:"
    totLatFloat = 0.0
    totLonFloat = 0.0
    firstCom = Comment.query.first()
    firstLat = firstCom.latLon.split(',')[0]
    firstLon = firstCom.latLon.split(',')[1]
    for c in allCom:
        if "," in c.latLon:
            lat = c.latLon.split(',')[0]
            lon = c.latLon.split(',')[1]
            totLatFloat += float(lat)
            totLonFloat += float(lon)
            retString += lat
            retString += "<br>"
            retString += lon
            #retString += c.latLon
            retString += "<br><br>"
            retString += str(totLatFloat)
            retString += "<br>"
            retString += str(totLonFloat)
            retString += "<br>"
            distanceFromFirst = getDistanceFromLatLonInKm(float(firstLat), float(firstLon), float(lat), float(lon))
            retString += "Distance from first:"
            retString += str(distanceFromFirst)
            retString +="<br><br>"
    return retString


@app.route('/mobile_get2_top_comments', methods = ["GET", "POST"])
#@login_required
def mobile_get2_top_comments():
    fake_comments = []
    retComs = Comment.query.filter_by(depth = 1).all()#[:100]
    retComs = sorted(retComs, key=lambda Comment:Comment.get_likes(), reverse=True)
    #retComs = filter(retComs, key=lambda Comment:Comment.
    #retComs = filter(lambda x: x., retComs)
    userid = int(request.json['fbid'])
    userLoc = str(request.json['recentLocation'])
    user = User.query.filter_by(fb_id = userid).first()
    user.setRecLoc(userLoc)
    radVal = int(request.json['radiusValue'])
    distanceMeters = 30#the data from apple this is based on is weird. Assume the actual distance is a tenth of this.
    if radVal == 1:
        distanceMeters = 30.0
    if radVal == 2:
        distanceMeters = 250.0
    if radVal == 3:
        distanceMeters = 2500.0
    if userLoc is None:
        userLoc = "41.3078599, -72.930389"
    retComs = filter(lambda x: x.getDistance(userLoc, distanceMeters) == True, retComs)
    #retComs = Comment.query.filter_by(depth = 1).filter(Comment.getDistance(userLoc, distanceMeters)).all()#[:100]
    retComs = retComs[:50]
    if user is None:
        user = mobile_create_user(userid)
    for c in retComs:
        c.createAddressString()
        daCom = get_comment_template(c, user)
        fake_comments.append(daCom)
        # if c.locationAddress is None:
        #     if c.latLon is not None:
        #         address = geolocator.reverse(c.latLon)
	       # if address is not None:
	       #     locString = "@" + str(address[0][0]).split(',')[0]
	       #     c.locationAddress = locString
	       #     db.session.commit()
        # if "," in c.latLon:
        #     uLat = float(userLoc.split(',')[0])
        #     uLon = float(userLoc.split(',')[1])
        #     cLat = float(c.latLon.split(',')[0])
        #     cLon = float(c.latLon.split(',')[1])
        #     dist = getDistanceFromLatLonInKm(float(uLat), float(uLon), float(cLat), float(cLon))
        #     print(dist)
        #     if float(dist) <= distanceMeters:
        #         c.createAddressString()
        #         daCom = get_comment_template(c, user)
        #         fake_comments.append(daCom)
    return jsonify(results = fake_comments)


@login_required
@app.route('/mobile_get2_new_comments', methods = ["GET", "POST"])
def mobile_get2_new_comments():
    fake_comments = []
    retComs = Comment.query.order_by(desc(Comment.atTime)).filter_by(depth = 1)
    userid = int(request.json['fbid'])
    user = User.query.filter_by(fb_id = userid).first()
    userLoc = str(request.json['recentLocation'])
    radVal = int(request.json['radiusValue'])
    distanceMeters = 30.0#the data from apple this is based on is weird. Assume the actual distance is a tenth of this.
    if radVal == 1:
        distanceMeters = 30.0
    if radVal == 2:
        distanceMeters = 250.0
    if radVal == 3:
        distanceMeters = 2500.0
    if user is None:
        user = mobile_create_user(userid)
    if(user.nickname == "Prerna Gupta"):
        userLoc = "41.3078599, -72.930389"
    #if(user.nickname == "Rijul Gupta"):
        #userLoc = "41.3078599, -72.930389"
    #if(user.nickname == "Will Byun"):
    #    userLoc = "41.3078599, -72.930389"
    if userLoc is None:
        userLoc = "41.3078599, -72.930389"
    distanceMeters = 300.0
    retComs = filter(lambda x: x.getDistance(userLoc, distanceMeters) == True, retComs)
    #retComs = Comment.query.order_by(desc(Comment.atTime)).filter_by(depth = 1).filter(Comment.getDistance(userLoc, distanceMeters) == True)[:50]
    retComs = retComs[:50]
    #retComs = Comment.query.filter_by(depth = 1).filter(Comment.getDistance(userLoc, distanceMeters)).all()#[:100]
    for c in retComs:
        c.createAddressString()
        daCom = get_comment_template(c, user)
        fake_comments.append(daCom)
        # if c.locationAddress is None:
        #     if c.latLon is not None:
        #         address = geolocator.reverse(c.latLon)
	       # if address is not None:
	       #     locString = "@" + str(address[0][0]).split(',')[0]
	       #     c.locationAddress = locString
	       #     db.session.commit()
        # if "," in c.latLon:
        #     uLat = float(userLoc.split(',')[0])
        #     uLon = float(userLoc.split(',')[1])
        #     cLat = float(c.latLon.split(',')[0])
        #     cLon = float(c.latLon.split(',')[1])
        #     dist = getDistanceFromLatLonInKm(float(uLat), float(uLon), float(cLat), float(cLon))
        #     print(dist)
        #     if float(dist) <= distanceMeters:
        #         c.createAddressString()
        #         daCom = get_comment_template(c, user)
        #         fake_comments.append(daCom)
    return jsonify(results = fake_comments)
    #return json.dumps(fake_comments, ensure_ascii=False).encode('utf8')
    #return fake_comments


@app.route('/mobile_user_get_comments', methods = ["GET", "POST"])
def mobile_user_get_comments():
    fake_comments = []
    userid = int(request.json['gfbid'])
    user = User.query.filter_by(fb_id = userid).first()
    user.setRecTime()
    userLoc = str(request.json['recentLocation'])
    allc = Comment.query.filter_by(depth = 1).all()
    if userLoc == "none":
        userLoc = "41.3078599, -72.930389"
    if userLoc is None:
        userLoc = "41.3078599, -72.930389"
    if userLoc is "":
        userLoc = "41.3078599, -72.930389"
    #userLoc = "41.3078599, -72.930389"
    allc = filter(lambda x: x.getDistance(userLoc, 500) == True, allc)
    allc = sorted(allc, key=lambda Comment:Comment.getWScore(userLoc), reverse=False)
    allc = allc[:50]
    for c in allc:
        daCom = get_comment_template(c, user)
        fake_comments.append(daCom)
    return jsonify(results = fake_comments)


@app.route('/mobile_get_the_feed', methods = ["GET", "POST"])
def mobile_get_the_feed():
    fake_comments = []
    retComs = Comment.query.order_by(desc(Comment.atTime)).filter_by(depth = 1)
    userid = int(request.json['fbid'])
    user = User.query.filter_by(fb_id = userid).first()
    userLoc = str(request.json['recentLocation'])
    radVal = int(request.json['radiusValue'])
    distanceMeters = 30.0#the data from apple this is based on is weird. Assume the actual distance is a tenth of this.
    if radVal == 1:
        distanceMeters = 30.0
    if radVal == 2:
        distanceMeters = 250.0
    if radVal == 3:
        distanceMeters = 2500.0
    if user is None:
        user = mobile_create_user(userid)
    if(user.nickname == "Prerna Gupta"):
        userLoc = "41.3078599, -72.930389"
    #if(user.nickname == "Rijul Gupta"):
        #userLoc = "41.3078599, -72.930389"
    #if(user.nickname == "Will Byun"):
    #    userLoc = "41.3078599, -72.930389"
    if userLoc is None:
        userLoc = "41.3078599, -72.930389"
    distanceMeters = 300.0
    retComs = filter(lambda x: x.getDistance(userLoc, distanceMeters) == True, retComs)
    #retComs = Comment.query.order_by(desc(Comment.atTime)).filter_by(depth = 1).filter(Comment.getDistance(userLoc, distanceMeters) == True)[:50]
    retComs = retComs[:50]
    #retComs = Comment.query.filter_by(depth = 1).filter(Comment.getDistance(userLoc, distanceMeters)).all()#[:100]
    for c in retComs:
        #c.createAddressString()
        daCom = get_comment_template(c, user)
        fake_comments.append(daCom)
        # if c.locationAddress is None:
        #     if c.latLon is not None:
        #         address = geolocator.reverse(c.latLon)
	       # if address is not None:
	       #     locString = "@" + str(address[0][0]).split(',')[0]
	       #     c.locationAddress = locString
	       #     db.session.commit()
        # if "," in c.latLon:
        #     uLat = float(userLoc.split(',')[0])
        #     uLon = float(userLoc.split(',')[1])
        #     cLat = float(c.latLon.split(',')[0])
        #     cLon = float(c.latLon.split(',')[1])
        #     dist = getDistanceFromLatLonInKm(float(uLat), float(uLon), float(cLat), float(cLon))
        #     print(dist)
        #     if float(dist) <= distanceMeters:
        #         c.createAddressString()
        #         daCom = get_comment_template(c, user)
        #         fake_comments.append(daCom)
    return jsonify(results = fake_comments)
    #return json.dumps(fake_comments, ensure_ascii=False).encode('utf8')
    #return fake_comments

@app.route('/get_poppin_places', methods = ["GET", "POST"])
def get_poppin_places():
    allc = Comment.query.all()
    return "yes"

@app.route('/mobile_get_clusters', methods = ["GET", "POST"])
def mobile_get_clusters():
    fake_sent = []
    user1 = User.query.filter_by(nickname = "Sophie Swanson").first()
    user1id = str(user1.fb_id)
    user1Name = user1.nickname
    user2 = User.query.filter_by(nickname = "Bonnie Rhee").first()
    user2id = str(user2.fb_id)
    user2Name = user2.nickname
    user3 = User.query.filter_by(nickname = "Jan Zielonka").first()
    user3id = str(user3.fb_id)
    user3Name = user3.nickname
    user4 = User.query.filter_by(nickname = "Zak Kayal").first()
    user4id = str(user4.fb_id)
    user4Name = user4.nickname
    user5 = User.query.filter_by(nickname = "Vicky Tu").first()
    user5id = str(user5.fb_id)
    user5Name = user5.nickname
    user6 = User.query.filter_by(nickname = "Jae Park").first()
    user6id = str(user6.fb_id)
    user6Name = user6.nickname
    user7 = User.query.filter_by(nickname = "Jan Zielonka").first()
    user7id = str(user7.fb_id)
    user7Name = user7.nickname
    user8 = User.query.filter_by(nickname = "Zak Kayal").first()
    user8id = str(user8.fb_id)
    user8Name = user8.nickname
    user9 = User.query.filter_by(nickname = "Vicky Tu").first()
    user9id = str(user9.fb_id)
    user9Name = user9.nickname
    numMorePeople = "5"
    pic1 = "http://s3-media3.fl.yelpcdn.com/bphoto/auCOQEeZMozX432Jalee5Q/ls.jpg"
    pic2 = "http://s3-media3.fl.yelpcdn.com/bphoto/9HvMiwyFB7Mnan8G0-671g/ls.jpg"
    pic3 = "http://s3-media1.fl.yelpcdn.com/bphoto/f7LxetNV1TTGTV1R5EA73A/ls.jpg"
    pic4 = "http://s3-media2.fl.yelpcdn.com/bphoto/2JrqfP9rnLo0Wx0KjxZCEw/ls.jpg"
    pic5 = "http://res.cloudinary.com/hwthvxm3h/image/upload/04_San_Francisco_Zoo_640.jpg.jpg"
    pic6 = "http://sfappeal.com/wp-content/uploads/2012/03/sf.zoo_.lemurs.jpg"
    pic7 = "http://s3-media1.fl.yelpcdn.com/bphoto/oUBTGBARZ7u17Z53HbzKhA/348s.jpg"
    pic8 = "http://www.wheelchairtraveling.com/wp-content/uploads/2010/03/SF_zoo3-200x200.jpg"
    latLon = "37.7874944, -122.39653350000003"
    fakep1 = {
        'type':'3',
        'locationAddress':'Galvanize',
        'user1fb':user1id,
        'user1Name':user1Name,
        'user2fb':user2id,
        'user2Name':user2Name,
        'user3fb':user3id,
        'user3Name':user3Name,
        'numMore':numMorePeople,
        'pic1Link':pic1,
        'pic2Link':pic2,
        'pic3Link':pic3,
        'pic4Link':pic4,
        'location':latLon
        }
    fakep2 = {
        'type':'3',
        'locationAddress':'SF Zoo',
        'user1fb':user4id,
        'user1Name':user4Name,
        'user2fb':user5id,
        'user2Name':user5Name,
        'user3fb':user6id,
        'user3Name':user6Name,
        'numMore':'10',
        'pic1Link':pic5,
        'pic2Link':pic6,
        'pic3Link':pic7,
        'pic4Link':pic8,
        'location':'37.732957, -122.50295499999999'
        }
    fake_sent.append(fakep1)
    fake_sent.append(fakep2)
    return jsonify(results = fake_sent)

import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

@app.route('/test_new_feed', methods = ["GET", "POST"])
def test_new_feed():
    allc = Comment.query.filter_by(depth = 1).all()
    userLoc = "41.3078599, -72.930389"
    allc = filter(lambda x: x.getDistance(userLoc, 500) == True, allc)
    allc = sorted(allc, key=lambda Comment:Comment.getWScore(userLoc), reverse=False)
    string2 = ""
    for c in allc:
        string2 += str(c.getWScore(userLoc))
        string2 += "<br>"
    return string2



@app.route('/test_scan', methods = ["GET", "POST"])
def test_scan():
    centers = [[10, 10], [-10, -10], [10, -10]]
    X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4, random_state=0)
    #X = StandardScaler().fit_transform(X)
    db = DBSCAN(eps=0.3, min_samples=10).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    string2 = "Number of clusters:"
    string2 += str(n_clusters_)
    firC = X[labels == 0]
    xcen1 = 0.0
    ycen1 = 0.0
    for c in firC:
        xcen1 += c[0]
        ycen1 += c[1]
    xcen1 = xcen1/len(firC)
    ycen1 = ycen1/len(firC)
    string2 += "<br>"
    string2 += "<br>"
    string2 += "Center X:"
    string2 += str(xcen1)
    string2 += "<br>"
    string2 += "Center Y:"
    string2 += str(ycen1)
    string2 += "<br>"
    string2 += "<br>"
    string2 += "<br>"
    for c in firC:
        string2 += str(c)
        string2 += "<br>"
    string2 += "<br>"
    string2 += "<br>"
    string2 += "<br>"
    for c in X:
        string2 += str(c)
        string2 += "<br>"
    return string2

@app.route('/test_scan2', methods = ["GET", "POST"])
def test_scan2():
    allC = Comment.query.all()
    X = []
    for c in allC:
        if "," in c.latLon:
            y = []
            lat = c.latLon.split(',')[0]
            lon = c.latLon.split(',')[1]
            y1 = float(lat)
            y2 = float(lon)
            #y += y1
            #y += y2
            y.append(y1)
            y.append(y2)
            X.append(y)
    X = np.array(X)
    db = DBSCAN(eps=0.0001, min_samples=10).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    string2 = "Number of clusters:"
    string2 += str(n_clusters_)
    string2 += "<br>"
    string2 += "<br>"
    string2 += "<br>"
    #GET ALL CLUSTER LOCATIONS
    for n in range(n_clusters_):
        daClus = X[labels == n]
        xcen = 0.0
        ycen = 0.0
        for c in daClus:
            xcen += c[0]
            ycen += c[1]
        xcen = xcen/len(daClus)
        ycen = ycen/len(daClus)
        string2 +="Data for cluster "
        string2 += str(n)
        string2 += ":"
        string2 += "<br>"
        string2 += "X Center:"
        string2 += str(xcen)
        string2 += "<br>"
        string2 += "Y Center:"
        string2 += str(ycen)
        string2 += "<br>"
        string2 += "<br>"
    #print points
    string2 += "<br>"
    string2 += "<br>"
    string2 += "<br>"
    string2 += "<br>"
    for c in X:
        string2 += str(c)
        string2 += "<br>"
    return string2
    return str(X)




@app.route('/mobile_throw_fake_places', methods = ["GET", "POST"])
def mobile_throw_fake_places():
    fake_places = []
    user1 = User.query.filter_by(nickname = "Rijul Gupta").first()
    user1id = str(user1.fb_id)
    user1Name = user1.nickname
    user2 = User.query.filter_by(nickname = "Prerna Gupta").first()
    user2id = str(user2.fb_id)
    user2Name = user2.nickname
    user3 = User.query.filter_by(nickname = "Esha Gupta").first()
    user3id = str(user3.fb_id)
    user3Name = user3.nickname
    numMorePeople = "32"
    pic1 = "http://fc08.deviantart.net/fs70/i/2013/039/8/c/greetings_from_imgur_by_garyckarntzen-d5t3tfh.jpg"
    pic2 = "http://i.imgur.com/O1sCuWo.jpg"
    pic3 = "http://a1.mzstatic.com/us/r30/Purple4/v4/6d/8c/b1/6d8cb1d7-d637-db1a-93f5-98460f4d473e/icon100x100.png"
    pic4 = "http://fc08.deviantart.net/fs70/i/2013/039/8/c/greetings_from_imgur_by_garyckarntzen-d5t3tfh.jpg"
    latLon = "41.3078599, -72.930389"
    fakep1 = {
        'type':'3',
        'locationAddress':'A Cool Place To Be',
        'user1fb':user1id,
        'user1Name':user1Name,
        'user2fb':user2id,
        'user2Name':user2Name,
        'user3fb':user3id,
        'user3Name':user3Name,
        'numMore':numMorePeople,
        'pic1Link':pic1,
        'pic2Link':pic2,
        'pic3Link':pic3,
        'pic4Link':pic4,
        'location':latLon
        }
    fake_places.append(fakep1)
    fake_places.append(fakep1)
    fake_places.append(fakep1)
    fake_places.append(fakep1)
    fake_places.append(fakep1)
    userLoc = "41.3078599, -72.930389"
    retComs = Comment.query.order_by(desc(Comment.atTime)).filter_by(depth = 1)
    retComs = filter(lambda x: x.getDistance(userLoc, 50) == True, retComs)
    #retComs = Comment.query.order_by(desc(Comment.atTime)).filter_by(depth = 1).filter(Comment.getDistance(userLoc, distanceMeters) == True)[:50]
    retComs = retComs[:50]
    #retComs = Comment.query.filter_by(depth = 1).filter(Comment.getDistance(userLoc, distanceMeters)).all()#[:100]
    for c in retComs:
        c.createAddressString()
        daCom = get_comment_template(c, user1)
        fake_places.append(daCom)
    fake_places.append(fakep1)
    fake_places.append(fakep1)
    fake_places.append(fakep1)
    fake_places.append(fakep1)
    fake_places.append(fakep1)
    return jsonify(results = fake_places)

@app.route('/mobile_get_location_comments', methods = ["GET", "POST"])
def mobile_get_location_comments():
    fake_comments = []
    retComs = Comment.query.order_by(desc(Comment.atTime)).filter_by(depth = 1)
    userid = int(request.json['fbid'])
    user = User.query.filter_by(fb_id = userid).first()
    userLoc = str(request.json['recentLocation'])
    distanceMeters = 30.0
    retComs = filter(lambda x: x.getDistance(userLoc, distanceMeters) == True, retComs)
    #retComs = Comment.query.order_by(desc(Comment.atTime)).filter_by(depth = 1).filter(Comment.getDistance(userLoc, distanceMeters) == True)[:50]
    retComs = retComs[:50]
    #retComs = Comment.query.filter_by(depth = 1).filter(Comment.getDistance(userLoc, distanceMeters)).all()#[:100]
    for c in retComs:
        c.createAddressString()
        daCom = get_comment_template(c, user)
        fake_comments.append(daCom)
    return jsonify(results = fake_comments)

@app.route('/mobile_get_user_comments', methods = ["GET", "POST"])
def mobile_get_user_comments():
    gotID = request.json['fbid']
    generalID = request.json['gfbid']
    u = User.query.filter_by(fb_id = int(gotID)).first()
    gu = User.query.filter_by(fb_id = int(generalID)).first()
    #coms = u.comments.filter_by(depth = 1).all()
    coms = u.comments.order_by(desc(Comment.atTime)).filter_by(depth = 1)[:30]
    fake_comments = []
    for c in coms:
        daCom = get_comment_template(c, gu)
        fake_comments.append(daCom)
    return jsonify(results = fake_comments)

@app.route('/mobile_get_following_comments', methods = ["GET", "POST"])
def mobile_get_following_comments():
    #gotID = request.json['fbid']
    generalID = request.json['gfbid']
    #u = User.query.filter_by(fb_id = int(gotID)).first()
    gu = User.query.filter_by(fb_id = int(generalID)).first()
    #coms = u.comments.order_by(desc(Comment.atTime)).filter_by(depth = 1).all()
    holdcoms = []
    fake_comments = []
    userLoc = "41.3078599, -72.930389"
    allc = Comment.query.filter_by(depth = 1).all()
    allc = filter(lambda x: x.getDistance(userLoc, 500) == True, allc)
    allc = sorted(allc, key=lambda Comment:Comment.getWScore(userLoc), reverse=False)
    allc = allc[:50]
    for c in allc:
        daCom = get_comment_template(c, gu)
        fake_comments.append(daCom)
    return jsonify(results = fake_comments)
    # for u in gu.followed:
    #     for c in u.comments.filter_by(depth = 1):
    #         holdcoms.append(c)
    #         #daCom = get_comment_template(c, gu)
    #         #fake_comments.append(daCom)
    # #holdcoms = holdcoms.order_by(desc(Comment.atTime)).filter_by(depth = 1)[:50]
    # holdcoms = sorted(holdcoms, key=lambda Comment:Comment.atTime, reverse=True)[:50]
    # for c in holdcoms:
    #     daCom = get_comment_template(c, gu)
    #     fake_comments.append(daCom)
    # return jsonify(results = fake_comments[:50])


@app.route('/mobile_get_comment_info', methods = ["GET", "POST"])
def mobile_get_comment_info():
    gotID = request.json['c_id']
    c = Comment.query.filter_by(id = int(gotID)).first()
    c_info = [{
        "c_id":str(c.id),
        "body":c.body.decode('unicode-escape'),
        "author":str(c.author.nickname),
        "authorFBID":str(c.author.fb_id),
        "time":str(c.getAtTime()),
        "location":str(c.locationAddress),
        "imgLink":str(c.imgLink)
        }]
    #c_info = [{"what":"the hell"}]
    return jsonify(results = c_info)

@app.route('/mobile_delete_comment', methods = ["GET", "POST"])
def mobile_delete_comment():
    cID = request.json['cID']
    c = Comment.query.filter_by(id = cID).first()
    #Johnny = User.query.filter_by(username = "Johnny Apples").first()
    #c.user_id = Johhny.id
    #c.body = "deleted"
    db.session.delete(c)
    retString = [{"done":"yes"}]
    return jsonify(results = retString)


@app.route('/mobile_submit_this_comment', methods = ["GET", "POST"])
def mobile_submit_this_comment():
    daBod = request.json['cBody']
    daFake = "fake it to make it"
    commentBody = str(daBod.encode('utf-8'))
    #uniCodeBody = unicode(daBod, 'utf-8')
    uniCodeBody = daBod.encode('unicode_escape')
    recieved_fb_id = int(request.json['fb_id'])
    recieved_latlong = str(request.json['latLon'])
    imgLink = str(request.json['imgLink'])
    longHashString = str(request.json['hashids'])
    hashids = longHashString.split()
    user = User.query.filter_by(fb_id = recieved_fb_id).first()
    #fuck == "you"
    if user is None:
        user = mobile_create_user(recieved_fb_id)
    c = Comment(body = uniCodeBody, user_id = user.id, atTime = datetime.now(), latLon = recieved_latlong, depth = 1, imgLink = imgLink, bodyUni = uniCodeBody)
    for h in hashids:
        hashtag = Hashtag.query.filter_by(id = int(h)).first()
        c.add_hashtag(hashtag)
    db.session.add(c)
    user.comments.append(c)
    db.session.commit()
    retStr = [
        {
            "done":commentBody
        }
        ]
    return jsonify(results = retStr)



@app.route('/mobile_reply_to_comment', methods = ["GET", "POST"])
def mobile_reply_to_comment():
    daBod = request.json['rBody']
    parentID = request.json['cID']
    #daFake = "fake it to make it"
    commentBody = str(daBod.encode('utf-8'))
    #uniCodeBody = unicode(daBod, 'utf-8')
    uniCodeBody = daBod.encode('unicode_escape')
    recieved_fb_id = int(request.json['fb_id'])
    recieved_latlong = str(request.json['latLon'])
    comPar = Comment.query.filter_by(id = int(parentID)).first()
    #imgLink = str(request.json['imgLink'])
    user = User.query.filter_by(fb_id = recieved_fb_id).first()
    c = Comment(body = uniCodeBody, user_id = user.id, atTime = datetime.now(), latLon = recieved_latlong, depth = 2, imgLink = "none", bodyUni = uniCodeBody, parent_id = comPar.id)
    db.session.add(c)
    user.comments.append(c)
    comPar.reply_comments.append(c)
    db.session.commit()
    create_notification(u1 = comPar.author, u2 = user, c1 = comPar, r1 = c,  typeN = 3, latLon = None)
    retStr = [
        {
            "done":commentBody
        }
        ]
    return jsonify(results = retStr)





@app.route('/mobile_get_comment_replies', methods = ["GET", "POST"])
def mobile_get_comment_replies():
    parentID = request.json['cID']
    recieved_fb_id = int(request.json['fb_id'])
    user = User.query.filter_by(fb_id = recieved_fb_id).first()
    comPar = Comment.query.filter_by(id = int(parentID)).first()
    repComs = comPar.reply_comments
    fake_comments = []
    for c in repComs:
        daCom = get_comment_template(c, user)
        fake_comments.append(daCom)
    return jsonify(results = fake_comments)

@app.route('/mobile_get_comment_likers', methods = ["GET", "POST"])
def mobile_get_comment_likers():
    #c.user_likers
    parentID = request.json['cID']
    recieved_fb_id = int(request.json['fb_id'])
    user = User.query.filter_by(fb_id = recieved_fb_id).first()
    comPar = Comment.query.filter_by(id = int(parentID)).first()
    userLikers = comPar.user_likers
    fake_comments = []
    for u in userLikers:
        uID = str(u.fb_id)
        uName = str(u.nickname.encode('utf-8'))
        if user.is_following(u) is True:
            uFollow = "yes"
        else:
            uFollow = "no"
        fake_c = {'userID':uID, 'userName':uName, 'userFollow':uFollow}
        fake_comments.append(fake_c)
    return jsonify(results = fake_comments)

@app.route('/mobile_toggle_comment_vote', methods = ["GET", "POST"])
def mobile_toggle_comment_vote():
    userid = int(request.json['fbid'])
    commentid = int(request.json['comment_id'])
    user = User.query.filter_by(fb_id = userid).first()
    com = Comment.query.filter_by(id = commentid).first()
    if user is None:
        user = mobile_create_user(userid)
    if com.has_liked(user) is True:
        com.did_unlike(user)
        retStr = [{"vote":"no"}]
    else:
        com.did_like(user)
        retStr = [{"vote":"yes"}]
        create_notification(u1 = com.author, u2 = user, c1 = com, r1 = None,  typeN = 1, latLon = None)
    return jsonify(results = retStr)



@app.route('/mobile_user_like_comment', methods = ["GET", "POST"])
def mobile_user_like_comment():
    userid = int(request.json['fbid'])
    commentid = int(request.json['comment_id'])
    user = User.query.filter_by(fb_id = userid).first()
    com = Comment.query.filter_by(id = commentid).first()
    if user is None:
        user = mobile_create_user(userid)
    com.did_like(user)
    create_notification(u1 = com.author, u2 = user, c1 = com, r1 = None,  typeN = 1, latLon = None)
    #com.user_likers.append(user)
    #db.session.commit()
    retStr = [
        {
            "done":com.id
        }
        ]
    return jsonify(results = retStr)

@app.route('/mobile_user_unlike_comment', methods = ["GET", "POST"])
def mobile_user_unlike_comment():
    userid = int(request.json['fbid'])
    commentid = int(request.json['comment_id'])
    user = User.query.filter_by(fb_id = userid).first()
    com = Comment.query.filter_by(id = commentid).first()
    if user is None:
        user = mobile_create_user(userid)
    com.did_unlike(user)
    #com.user_likers.remove(user)
    #db.session.commit()
    retStr = [
        {
            "done":com.id
        }
        ]
    return jsonify(results = retStr)

# @app.route('/mobile_get_user_comments', methods = ["GET", "POST"])
# def mobile_get_user_comments():
#     recieved_fb_id = int(request.json['fb_id'])
#     user = User.query.filter_by(fb_id = recieved_fb_id).first()
#     coms = user.comments.all()
#     fake_comments = []
#     for c in coms:
#         daCom = get_comment_template(c, user)
#         fake_comments.append(daCom)
#     return jsonify(results = fake_comments)


@app.route('/mobile_get_user_info', methods = ["GET", "POST"])
def mobile_get_user_info():
    recieved_fb_id = int(request.json['fb_id'])
    recgfbid = int(request.json['gfb_id'])
    user = User.query.filter_by(fb_id = recieved_fb_id).first()
    guser = User.query.filter_by(fb_id = recgfbid).first()
    if guser is None:
        guser = mobile_create_user(recgfbid)
    isFol = "no"
    if(guser.is_following(user) == True):
        isFol = "yes"
    followersNum = str(user.followers.count())
    followingNum = str(user.followed.count())
    karmaNum = str(user.get_total_likes())
    #allComs = sorted(user.comments.filter_by(depth = 1).all(), key=lambda Comment:Comment.atTime, reverse=False)
    lastLoc = "none"
    lastLatLon = "none"
    lastTime = "none"
    comNum = str(user.comments.filter_by(depth = 1).count())
    uHashtags = []
    hashtag = {"body":"TEST", "id":"22"}
    for h in guser.hashtags:
        hashtag2 = {"body":h.body, "id":str(h.id)}
        uHashtags.append(hashtag2)
    uHashtags.append(hashtag)
    uHashtags.append(hashtag)
    uHashtags.append(hashtag)
    uHashtags.append(hashtag)
    uHashtags.append(hashtag)
    if(user.comments.count() > 0):
        allComs = sorted(user.comments.all(), key=lambda Comment:Comment.atTime, reverse=False)
        newestCom = allComs[-1]
        newestCom.createAddressString()
        lastLatLon = newestCom.latLon
        lastLoc = newestCom.locationAddress
        lastTime = newestCom.getAtTime()
    if lastLoc is None:
        lastLoc = lastLatLon
    retString = [
        {
            "karma":karmaNum,
            "lastLoc":lastLoc,
            "comments":comNum,
            "followers":followersNum,
            "following":followingNum,
            "lastlatlon":lastLatLon,
            "lastTime":lastTime,
            "isFollowing":isFol,
            "hashtags":uHashtags
        }]
    return jsonify(results = retString)

@app.route('/mobile_is_user_following', methods = ["GET", "POST"])
def mobile_is_user_following():
    gUserId = int(request.json['gUser_fbID'])
    gUser = User.query.filter_by(fb_id = gUserId).first()
    inqUserId = int(request.json['iUser_fbID'])
    inqUser = User.query.filter_by(fb_id = inqUserId).first()
    if gUser.is_following(inqUser) is True:
        valString = "yes"
    else:
        valString = "no"
    retString = [{'value':valString}]
    return jsonify(results = retString)

@app.route('/mobile_toggle_user_follow', methods = ["GET", "POST"])
def mobile_toggle_user_follow():
    gUserId = int(request.json['gUser_fbID'])
    gUser = User.query.filter_by(fb_id = gUserId).first()
    inqUserId = int(request.json['iUser_fbID'])
    inqUser = User.query.filter_by(fb_id = inqUserId).first()
    if gUser.is_following(inqUser) is True:
        gUser.unfollow(inqUser)
        db.session.commit()
        valString = "no"
    else:
        gUser.follow(inqUser)
        db.session.commit()
        valString = "yes"
        create_notification(u1 = inqUser, u2 = gUser, c1 = None, r1 = None,  typeN = 4, latLon = None)
    retString = [{'value':valString}]
    return jsonify(results = retString)

@app.route('/mobile_get_user_followers', methods = ["GET", "POST"])
def mobile_get_user_followers():
    gUserId = int(request.json['gUser_fbID'])
    gUser = User.query.filter_by(fb_id = gUserId).first()
    inqUserId = int(request.json['iUser_fbID'])
    inqUser = User.query.filter_by(fb_id = inqUserId).first()
    fake_comments = []
    for u in inqUser.followers:
        uID = str(u.fb_id)
        uName = str(u.nickname.encode('utf-8'))
        if gUser.is_following(u) is True:
            uFollow = "yes"
        else:
            uFollow = "no"
        fake_c = {'userID':uID, 'userName':uName, 'userFollow':uFollow}
        fake_comments.append(fake_c)
    return jsonify(results = fake_comments)


@app.route('/mobile_get_user_following', methods = ["GET", "POST"])
def mobile_get_user_following():
    gUserId = int(request.json['gUser_fbID'])
    gUser = User.query.filter_by(fb_id = gUserId).first()
    inqUserId = int(request.json['iUser_fbID'])
    inqUser = User.query.filter_by(fb_id = inqUserId).first()
    fake_comments = []
    for u in inqUser.followed:
        uID = str(u.fb_id)
        uName = str(u.nickname.encode('utf-8'))
        if gUser.is_following(u) is True:
            uFollow = "yes"
        else:
            uFollow = "no"
        fake_c = {'userID':uID, 'userName':uName, 'userFollow':uFollow}
        fake_comments.append(fake_c)
    return jsonify(results = fake_comments)

# facebook = OAuth2Service(name='facebook',
#                          authorize_url='https://www.facebook.com/dialog/oauth',
#                          access_token_url=graph_url + 'oauth/access_token',
#                          client_id=app.config['FB_CLIENT_ID'],
#                          client_secret=app.config['FB_CLIENT_SECRET'],
#                          base_url=graph_url)





# def get_friends_script(id, user):
#     origWD = os.getcwd()
#     os.chdir('hive')
#     targetString = " " + str(user.fb_id)
#     callString = "./scripttest.py" + " -username" + " rijul.gupta@gmail.com " + "-password" + " Rijul191992 " + "-target" + targetString
#     subprocess.call(callString, shell=True)
#     os.chdir(origWD)
#     background_scripts[id] = True

# def run_script(id):
#     origWD = os.getcwd()
#     os.chdir('hive')
#     subprocess.call("./scripttest.py", shell=True)
#     os.chdir(origWD)
#     background_scripts[id] = True

# @app.route('/testMutualFriends', methods = ["GET", "POST"])
# def testMutualFriends():
#     print("DID TRY 1")
#     user1 = User.query.filter_by(nickname = "Rijul Gupta").first()
#     user2 = User.query.filter_by(nickname = "Jimmy Park").first()
#     u1 = user1.fb_id
#     u2 = user2.fb_id
#     return facebook.authorize(callback=url_for('f_autho', next=request.args.get('next') or request.referrer or None, _external=True))
# #def facebook_authorized():
#     #return redirect(url_for('index'))


# @app.route('/f_autho', methods = ["GET", "POST"])
# @facebook.authorized_handler
# def f_autho(resp):
#     print("DID TRY 2")
#     if resp is None:
#       return 'Access denied: reason=%s error=%s' % (
#             request.args['error_reason'],
#             request.args['error_description']
#         )
#     session['oauth_token'] = (resp['access_token'], '')
#     user1 = User.query.filter_by(nickname = "Rijul Gupta").first()
#     user2 = User.query.filter_by(nickname = "Jimmy Park").first()
#     u1 = user1.fb_id
#     u2 = user2.fb_id
#     gS = '/'+str(u2)+'?fields=context.fields%28mutual_friends%29'
#     #gS = '/me'
#     print(gS)
#     me = facebook.get(gS)
#     print(me.data)
#     final = me.data['context']['mutual_friends']['summary']['total_count']
#     return str(final)#.data['name']

@app.route('/checkchekcer', methods = ["GET", "POST"])
def checkchecker():
    id = str(uuid.uuid4())
    background_scripts[id] = False
    user = User.query.filter_by(nickname = "Rijul Gupta").first()
    #threading.Thread(target=lambda: run_script(id)).start()
    threading.Thread(target=lambda: get_friends_script(id, user)).start()
    #return "start -- <script src='http://ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.js'></script><script>function ajaxCallback(data){if(data.done)window.location.replace('http://YOUR_GENERATED_PAGE_URL');elsewindow.setTimeout(function(){$.getJSON('{{ url_for('is_done') }}',{id:{{id}}},ajaxCallback);alert('try');},3000);}$(document).ready(function(){ajaxCallback({done=false});});</script>"
    return render_template('processing.html', id=id)
    #f = os.path.join(os.path.dirname(__file__), 'testCheck.py')
    # g = open(f)
    # h = execfile(f)
    #h = functions.facebook_login('rijul.gupta@gmail.com', 'Rijul191992')
    #return str(h)
    #r = requests.get('http://facebook.com/profile.php?id100000067665209')
    # starturl = 'http://facebook.com/100000067665209'
    # req = urllib2.Request(starturl)
    # res = urllib2.urlopen(req)
    # finalurl = str(res.geturl())
    # finalName = finalurl.replace('http://facebook.com/','')
    # return str(finalName)



@app.route('/is_done', methods = ["GET", "POST"])
def is_done():
    #id = str(request.json('id'))
    id = str(request.args.get('id', None))
    #return jsonify(done="done")
    if id not in background_scripts:
        abort(404)
    #return "done"
    return jsonify(done=background_scripts[id])

    #return facebook.authorize(callback=url_for('facebook_authorized', next=request.args.get('next') or request.referrer or None, _external=True))
# @app.route('/login')
# def login():
# # 	if g.user is not None and g.user.is_authenticated():
# # 		return redirect(url_for('index'))
# 	return facebook.authorize(callback=url_for('facebook_authorized', next=request.args.get('next') or request.referrer or None, _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
#def facebook_authorized():
    #return redirect(url_for('index'))
    if resp is None:
       return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return me.data['friends']
    #user = User.query.filter_by(email = me.data['email']).first()
    # user = User.query.filter_by(fb_id = me.data['id']).first()
    # if user is None:
    # 	u = User(nickname = me.data['name'], email = me.data['email'], role = ROLE_USER, fb_id = me.data['id'])
    # 	db.session.add(u)
    # 	db.session.commit()
    # 	return redirect(url_for('validate'))
    # user.nickname = me.data['name']
    # user.fb_id = int(me.data['id'])
    # login_user(user, remember = True)
    # db.session.commit()
    # #return redirect(request.args.get('next'))
    # return redirect(url_for('event', eventID = 1761))
    #return redirect(url_for('index'))
    #return redirect(url_for('validate'))
    #return redirect(url_for('home', focus = "user"))
#     return 'Logged in as id=%s name=%s redirect=%s || email=%s' % \
#         (me.data['id'], me.data['name'], request.args.get('next'), me.data['email'])

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

    #http://graph.facebook.com/v2.4/100004025035995/friendlists?access_token=23MVoIyzLtyTHQLXifksC-PrBGY
@app.route("/mobile_create_user", methods = ["GET", "POST"])
def mobile_create_user(fbid):
    r = requests.get('https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id=613995812038257&client_secret=05e778848e1187897b834fba967cc0c9')
    access_token = r.text.split('=')[1]
    userID = str(fbid)
    # if userID == "1100032182":
    #     return "Fuck off Minh"
    reqStringName = "https://graph.facebook.com/"+userID+"?fields=name&access_token=" + str(access_token)
    reqStringEmail = "https://graph.facebook.com/"+userID+"?fields=email&access_token=" + str(access_token)
    #return reqString
    gotName = requests.get(reqStringName)
    gotEmail = requests.get(reqStringEmail)
    userName = gotName.json()["name"]
    numUsers = len(User.query.all()) + 1
    userEmail = "none_" + str(numUsers)
    if "email" in gotEmail.json():
        userEmail = gotEmail.json()["email"]
    user = User.query.filter_by(fb_id = fbid).first()
    if user is None:
        u = User(nickname = userName, fb_id = fbid, role = ROLE_USER, email = userEmail, apsToken = "none")
        db.session.add(u)
        db.session.commit()
    return u



@app.route('/mobile_update_user_token', methods = ["GET", "POST"])
def mobile_update_user_token():
    newToken = request.json['token']
    newToken = newToken.replace(" ", "")
    newToken = newToken.replace("<", "")
    newToken = newToken.replace(">", "")
    newToken = str(newToken)
    gotID = request.json['fbid']
    u = User.query.filter_by(fb_id = int(gotID)).first()
    if u is None:
        u = mobile_create_user(gotID)
    if str(newToken) != "none":
        u.apsToken = newToken
        db.session.commit()
    if u.apsToken == "none":
        retString = [{'done':'no'}]
    else:
        retString = [{'done':'yes'}]
    return jsonify(results = retString)

@app.route('/mobile_get_user_notifications', methods = ["GET", "POST"])
def mobile_get_user_notifications():
    gotID = request.json['fbid']
    generalID = request.json['gfbid']
    u = User.query.filter_by(fb_id = int(gotID)).first()
    gu = User.query.filter_by(fb_id = int(generalID)).first()
    #nots = u.comments.order_by(desc(Comment.atTime)).filter_by(depth = 1).all()
    nots = Notification.query.order_by(desc(Notification.atTime)).filter_by(user1_id = u.id)[:30]
    fake_nots = []
    for n in nots:
        daNot = get_notification_template(n, gu)
        fake_nots.append(daNot)
    return jsonify(results = fake_nots)



def get_notification_template(n, user):
    if n.user1_id is not None:
        #u1Name = str(User.query.filter_by(id = n.user1_id).first().nickname)
        u1Name = str(User.query.filter_by(id = n.user1_id).first().nickname.encode('utf-8'))
    else:
        u1Name = "none"
    if n.user2_id is not None:
        #u2Name = str(User.query.filter_by(id = n.user2_id).first().nickname)
        u2Name = str(User.query.filter_by(id = n.user2_id).first().nickname.encode('utf-8'))
        u2Id = str(n.user2_id)
        u2FBID = str(User.query.filter_by(id = n.user2_id).first().fb_id)
    else:
        u2Name = "none"
        u2FBID = "none"
    if n.comment_id is not None:
        cId = str(n.comment_id)
    else:
        cId = "none"
    if n.reply_id is not None:
        rId = str(n.reply_id)
    else:
        rId = "none"
    if n.typeNum is not None:
        typeN = str(n.typeNum)
    else:
        typeN = "none"
    if n.atTime is not None:
        timeString = n.getAtTime()
    else:
        timeString = "none"
    #numComString = str(c.reply_comments.count())
        #cString = str(c.body)
    #cString = c.body.decode('unicode-escape')
    #hString = str(c.get_likes())
    fake_n = {
        'type':typeN,
        'u1Name':u1Name,
        'u2Name':u2Name,
        'u2Id':u2Id,
        'u2FBID':u2FBID,
        'c_id':cId,
        'r_id':rId,
        'time':timeString
        }
    return fake_n



def create_notification(u1, u2, c1, r1, typeN, latLon):
    if typeN == 1:#like a comment
        n = Notification(user1_id = u1.id, user2_id = u2.id, comment_id = c1.id, typeNum = typeN, atTime =  datetime.now(), latLon = "none")
        db.session.add(n)
        db.session.commit()
        st = u2.nickname
        st += " liked your post."
        try:
            send_push(u1, st)
        except:
            return
    if typeN == 2:#like a reply
        n = Notification(user1_id = u1.id, user2_id = u2.id, comment_id = c1.id, typeNum = typeN, atTime =  datetime.now(), latLon = "none")
        db.session.add(n)
        db.session.commit()
        st = u2.nickname
        st += " liked your reply."
        try:
            send_push(u1, st)
        except:
            return
    if typeN == 3:#reply to comment
        n = Notification(user1_id = u1.id, user2_id = u2.id, comment_id = c1.id, reply_id = r1.id, typeNum = typeN, atTime =  datetime.now(), latLon = "none")
        db.session.add(n)
        db.session.commit()
        st = u2.nickname
        st += " replied to your comment."
        try:
            send_push(u1, st)
        except:
            return
    if typeN == 4:#follow user
        n = Notification(user1_id = u1.id, user2_id = u2.id, typeNum = typeN, atTime =  datetime.now(), latLon = "none")
        db.session.add(n)
        db.session.commit()
        st = u2.nickname
        st += " is now following you."
        try:
            send_push(u1, st)
        except:
            return
    if typeN == 5:#requested connection
        n = Notification(user1_id = u1.id, user2_id = u2.id, typeNum = typeN, atTime =  datetime.now(), latLon = "none")
        db.session.add(n)
        db.session.commit()
        st = u2.nickname
        st += " wants to connect"
        try:
            send_push(u1, st)
        except:
            return
    if typeN == 6:#confirm connection
        n = Notification(user1_id = u1.id, user2_id = u2.id, typeNum = typeN, atTime =  datetime.now(), latLon = "none")
        db.session.add(n)
        db.session.commit()
        st = u2.nickname
        st += " accepted your connection"
        try:
            send_push(u1, st)
        except:
            return
    if typeN == 7:#recieved message
        n = Notification(user1_id = u1.id, user2_id = u2.id, typeNum = typeN, atTime =  datetime.now(), latLon = "none")
        db.session.add(n)
        db.session.commit()
        st = u2.nickname
        st += " sent you a message"
        try:
            send_push(u1, st)
        except:
            return


import time
from apns import APNs, Frame, Payload
import string
#cert_path = os.path.join(os.path.dirname(__file__), 'TutPushCert.pem')
#key_path = os.path.join(os.path.dirname(__file__), 'TutPushKey.pem')
cert_path = os.path.join(os.path.dirname(__file__), 'aps_production.pem')
key_path = os.path.join(os.path.dirname(__file__), 'prodKey.pem')
#apns = APNs(use_sandbox=True, cert_file=cert_path, key_file=key_path, enhanced=True)

apns = APNs(use_sandbox=False, cert_file=cert_path, key_file=key_path, enhanced=True)


@app.route('/testToken')
def testToken():
    token_hex = "0382800351deca3f2f557fcbe1a78b8bcd5870652025ed61715b888282e50aa7"
    payload = Payload(alert="If this works, we're okay.", sound="default", badge=0)
    apns.gateway_server.send_notification(token_hex, payload)
    return "done"

def send_push(u1, text):
    if u1.apsToken is not None:
        if u1.apsToken is not "none":
            if u1.apsToken is not "None":
                if all(c in string.hexdigits for c in u1.apsToken) == True:
                    token_hex = u1.apsToken
                    #token_hex = "Fat Cats Eat Rats"
                    payload = Payload(alert=text, sound="default", badge=0)
                    apns.gateway_server.send_notification(token_hex, payload)

# 	cText = str(request.form['comment_text'])
# 	tttTime = str(request.form['time_sent'])
# 	recTime = datetime.strptime(tttTime, "1:%d**2:%m**3:%y--4:%S**5:%M**6:%H")
# 	period = Period.query.filter_by(id = period_id_num).first()
# 	c = Comment(body = cText, period_id = period.id, user_id = g.user.id, atTime = recTime)
# 	db.session.add(c)
# 	period.children_comments.append(c)
# 	g.user.comments.append(c)
# 	db.session.commit()
# 	retStr = ""
# 	retStr += give_comment_template(c)
# 	#retStr += render_template('commentPreview.html', c = c, isNew = True)
# 	#retStr += '<div id="comment_'+str(c.id)+'_children_holder" style=""></div>'
# 	str2 = "Period:" + str(period.id) + "--Comment:" + cText
# 	return retStr

# def make_unique_nickname(nickname):
#         if User.query.filter_by(nickname=nickname).first() is None:
#             return nickname
#         version = 2
#         while True:
#             new_nickname = nickname + str(version)
#             if User.query.filter_by(nickname=new_nickname).first() is None:
#                 break
#             version += 1
#         return new_nickname















@app.route('/send_push_1')
def send_push_1():
    #token_hex = "0382800351deca3f2f557fcbe1a78b8bcd5870652025ed61715b888282e50aa7"
    token_hex = "0382800351deca3f2f557fcbe1a78b8bcd5870652025ed61715b888282e50aa7"
    payload = Payload(alert="3 of your friends are a block away.", sound="default", badge=0)
    apns.gateway_server.send_notification(token_hex, payload)
    return "done"

@app.route('/send_push_2')
def send_push_2():
    token_hex = "0382800351deca3f2f557fcbe1a78b8bcd5870652025ed61715b888282e50aa7"
    payload = Payload(alert="Ani replied to your comment.", sound="default", badge=0)
    apns.gateway_server.send_notification(token_hex, payload)
    return "done"

@app.route('/send_push_3')
def send_push_3():
    token_hex = "0382800351deca3f2f557fcbe1a78b8bcd5870652025ed61715b888282e50aa7"
    payload = Payload(alert="Jayce liked your comment.", sound="default", badge=0)
    apns.gateway_server.send_notification(token_hex, payload)
    return "done"


#Jayce alone at Myriad Gardens
@app.route('/mobile_video_feed_1', methods = ["GET", "POST"])
def mobile_video_feed_1():
    fake_sent = []
    user1 = User.query.filter_by(nickname = "Sophie Swanson").first()
    user1id = str(user1.fb_id)
    user1Name = user1.nickname
    user2 = User.query.filter_by(nickname = "Bonnie Rhee").first()
    user2id = str(user2.fb_id)
    user2Name = user2.nickname
    user3 = User.query.filter_by(nickname = "Jan Zielonka").first()
    user3id = str(user3.fb_id)
    user3Name = user3.nickname
    user4 = User.query.filter_by(nickname = "Zak Kayal").first()
    user4id = str(user4.fb_id)
    user4Name = user4.nickname
    user5 = User.query.filter_by(nickname = "Vicky Tu").first()
    user5id = str(user5.fb_id)
    user5Name = user5.nickname
    user6 = User.query.filter_by(nickname = "Jae Park").first()
    user6id = str(user6.fb_id)
    user6Name = user6.nickname
    numMorePeople = "5"
    pic1 = "http://www.keepitlocalok.com/sites/default/files/files/cuppies_feature.jpg"
    pic2 = "http://scontent-b.cdninstagram.com/hphotos-xap1/t51.2885-15/928578_248359218698465_368109086_a.jpg"
    pic3 = "https://v.cdn.vine.co/v/avatars/3650B248-F2A9-4736-8377-6E91129435CB-1119-00000125E1260E55.jpg?versionId=ftiN.XX3P1lOKHfu4th.ua4vuhujGh3E"
    pic4 = "http://cuppiesandjoe.com/assets/components/cliche/cache/1/7/_-300x300-zc.png"
    pic5 = "http://californiaskateparks.com/wp-content/uploads/2012/08/skatepark-projects-box.jpg"
    pic6 = "http://s3-media2.fl.yelpcdn.com/bphoto/0DfbRjqhpzLXGkDWHToztQ/ls.jpg"
    pic7 = "http://cdn1.fast-serve.net/cdn/bullethd/Skateboarding-with-BulletHD_700_600_4ZOHM.jpg"
    pic8 = "http://www.howtobeadad.com/wp-content/uploads/2013/04/charlie-skateboarding.jpg"
    latLon = "35.493494, -97.525318"
    fakep1 = {
        'type':'3',
        'locationAddress':'Cuppies & Joe',
        'user1fb':user1id,
        'user1Name':user1Name,
        'user2fb':user2id,
        'user2Name':user2Name,
        'user3fb':user3id,
        'user3Name':user3Name,
        'numMore':numMorePeople,
        'pic1Link':pic1,
        'pic2Link':pic2,
        'pic3Link':pic3,
        'pic4Link':pic4,
        'location':latLon
        }
    fake_c1 = {
        'hearts':'18',
        'has_liked':'yes',
        'author':'Bella Blakeman',
        'user_id':'320',
        'comments':'These gardens are so gorgeous.',
        'c_id':'20',
        'location':'Myriad Gardens',
        'image':'none',
        'time':'2 minutes ago',
        'numComments':'3',
        'type':'1'}
    fake_c2 = {
        'hearts':'12',
        'has_liked':'no',
        'author':'David Steiner',
        'user_id':'236',
        'comments':'Does anyone here have any allergy medication? Its that time of the year, lol.',
        'c_id':'21',
        'location':'Myriad Gardens',
        'image':'none',
        'time':'2 minutes ago',
        'numComments':'6',
        'type':'1'}
    fake_c3 = {
        'hearts':'28',
        'has_liked':'yes',
        'author':'Sloane Smith',
        'user_id':'206',
        'comments':'What is this guy shooting at? Myriad be cray.',
        'c_id':'21',
        'location':'Myriad Gardens',
        'image':'https://lh3.googleusercontent.com/-IyIa-faQ-HE/UREVdZDOAzI/AAAAAAAAGIg/OvSU6m4w8xw/s250-c-k-no/Courage%2BTo%2BLead%2B',
        'time':'5 minutes ago',
        'numComments':'1',
        'type':'2'}
    fake_c4 = {
        'hearts':'15',
        'has_liked':'no',
        'author':'Forrest Lin',
        'user_id':'312',
        'comments':'Anyone around here down for a walk in the park? ;)',
        'c_id':'22',
        'location':'Myriad Gardnes',
        'image':'none',
        'time':'3 minutes ago',
        'numComments':'4',
        'type':'1'}
    fake_c5 = {
        'hearts':'35',
        'has_liked':'yes',
        'author':'Emily Waligurski',
        'user_id':'182',
        'comments':'Wow. Just, wow.',
        'c_id':'23',
        'location':'Myriad Gardens',
        'image':'https://pbs.twimg.com/media/CFuZXc4UsAAubea.jpg:large',
        'time':'10 minutes ago',
        'numComments':'8',
        'type':'2'}
    fakep2 = {
        'type':'3',
        'locationAddress':'Bricktown Skatepark',
        'user1fb':user4id,
        'user1Name':user4Name,
        'user2fb':user5id,
        'user2Name':user5Name,
        'user3fb':user6id,
        'user3Name':user6Name,
        'numMore':'10',
        'pic1Link':pic5,
        'pic2Link':pic6,
        'pic3Link':pic7,
        'pic4Link':pic8,
        'location':latLon
        }
    fake_sent.append(fakep1)
    fake_sent.append(fake_c1)
    fake_sent.append(fake_c2)
    fake_sent.append(fake_c3)
    fake_sent.append(fake_c4)
    fake_sent.append(fake_c5)
    fake_sent.append(fakep2)
    return jsonify(results = fake_sent)


#Peak View of Cuppies and Joe
@app.route('/mobile_video_feed_2', methods = ["GET", "POST"])
def mobile_video_feed_2():
    fake_sent = []
    pic1 = "http://s3-media3.fl.yelpcdn.com/bphoto/auCOQEeZMozX432Jalee5Q/ls.jpg"
    pic2 = "http://s3-media3.fl.yelpcdn.com/bphoto/9HvMiwyFB7Mnan8G0-671g/ls.jpg"
    pic3 = "http://s3-media1.fl.yelpcdn.com/bphoto/f7LxetNV1TTGTV1R5EA73A/ls.jpg"
    pic4 = "http://s3-media2.fl.yelpcdn.com/bphoto/2JrqfP9rnLo0Wx0KjxZCEw/ls.jpg"
    fake_c1 = {
        'hearts':'8',
        'has_liked':'no',
        'author':'Isabelle Savoie',
        'user_id':'317',
        'comments':'Love hanging out with all these cool people!',
        'c_id':'25',
        'location':'Galvanize',
        'image':pic1,
        'time':'1 minute ago',
        'numComments':'3',
        'type':'2'}
    fake_c2 = {
        'hearts':'38',
        'has_liked':'no',
        'author':'Sabrina Bleich',
        'user_id':'319',
        'comments':'Why is no one working this cafe. I NEED COFFEE! Lol.',
        'c_id':'30',
        'location':'Cuppies and Joe',
        'image':pic2,
        'time':'10 minutes ago',
        'numComments':'6',
        'type':'2'}
    fake_c3 = {
        'hearts':'12',
        'has_liked':'no',
        'author':'Sophie Swanson',
        'user_id':'10152691229087251',
        'comments':"This is the coolest hack-a-thon I've ever been to. Really need to come here more often.",
        'c_id':'31',
        'location':'Cuppies and Joe',
        'image':pic3,
        'time':'2 minutes ago',
        'numComments':'6',
        'type':'2'}
    fake_c4 = {
        'hearts':'15',
        'has_liked':'no',
        'author':'Jan Zielonka',
        'user_id':'10153313145682417',
        'comments':"We are here just hanging out at Galvanize. It's a public event right now, everyone come over!",
        'c_id':'33',
        'location':'Cuppies and Joe',
        'image':'none',
        'time':'1 minute ago',
        'numComments':'0',
        'type':'1'}
    fake_c5 = {
        'hearts':'35',
        'has_liked':'yes',
        'author':'Hannah  Sachs',
        'user_id':'295',
        'comments':'Rooftop chilling with the tastemakers. #siliconvalley #crewlove',
        'c_id':'23',
        'location':'Cuppies and Joe',
        'image':pic4,
        'time':'10 minutes ago',
        'numComments':'8',
        'type':'2'}
    fake_c6 = {
        'hearts':'18',
        'has_liked':'no',
        'author':'Karl Marback',
        'user_id':'304',
        'comments':"Can anyone here help me with making AJAX requests from an iOS device?",
        'c_id':'42',
        'location':'Cuppies and Joe',
        'image':'none',
        'time':'20 minutes ago',
        'numComments':'12',
        'type':'1'}
    #fake_sent.append(fakep1)
    fake_sent.append(fake_c1)
    fake_sent.append(fake_c2)
    fake_sent.append(fake_c3)
    fake_sent.append(fake_c4)
    fake_sent.append(fake_c5)
    fake_sent.append(fake_c6)
    #fake_sent.append(fakep2)
    return jsonify(results = fake_sent)




#Actually at Cuppies and Joe
@app.route('/mobile_video_feed_3', methods = ["GET", "POST"])
def mobile_video_feed_3():
    fake_sent = []
    user1 = User.query.filter_by(nickname = "Ben Ackerman").first()
    user1id = str(user1.fb_id)
    user1Name = user1.nickname
    user2 = User.query.filter_by(nickname = "Ani Sefaj").first()
    user2id = str(user2.fb_id)
    user2Name = user2.nickname
    user3 = User.query.filter_by(nickname = "Julia Lee").first()
    user3id = str(user3.fb_id)
    user3Name = user3.nickname
    numMorePeople = "18"
    pic1 = "http://s3-media1.fl.yelpcdn.com/bphoto/Asqoz0SIoQfn6lyFwyPMZw/ls.jpg"
    pic2 = "https://v.cdn.vine.co/r/avatars/6253459C-B8A4-47BB-B0B7-6C2B915E520F-516-000001DD542C5329c7430da8dc.jpg?versionId=rI4BPHtjJQd76JAqAJ.3JESyKGPiwxbd"
    pic3 = "http://s3.amazonaws.com/foodspotting-ec2/reviews/2737952/thumb_600.jpg?1353121375"
    pic4 = "http://s3-media1.fl.yelpcdn.com/bphoto/iBCFt4RvhoiHksq3MMu8GA/ls.jpg"
    latLon = "35.457748, -97.618143"
    fakep1 = {
        'type':'3',
        'locationAddress':"Sherlock's Pub",
        'user1fb':user1id,
        'user1Name':user1Name,
        'user2fb':user2id,
        'user2Name':user2Name,
        'user3fb':user3id,
        'user3Name':user3Name,
        'numMore':numMorePeople,
        'pic1Link':pic1,
        'pic2Link':pic2,
        'pic3Link':pic3,
        'pic4Link':pic4,
        'location':latLon
        }
    fake_c1 = {
        'hearts':'8',
        'has_liked':'no',
        'author':'Isabelle Savoie',
        'user_id':'317',
        'comments':'Cuppies and Joe, chilling with this girl and getting my caff on. This place is the bomb!',
        'c_id':'25',
        'location':'Cuppies and Joe',
        'image':'https://v.cdn.vine.co/v/avatars/3650B248-F2A9-4736-8377-6E91129435CB-1119-00000125E1260E55.jpg?versionId=ftiN.XX3P1lOKHfu4th.ua4vuhujGh3E',
        'time':'1 minute ago',
        'numComments':'3',
        'type':'2'}
    fake_c2 = {
        'hearts':'38',
        'has_liked':'no',
        'author':'Sabrina Bleich',
        'user_id':'319',
        'comments':'10% off your order if you mention Hive.',
        'c_id':'30',
        'location':'Cuppies and Joe',
        'image':'http://www.keepitlocalok.com/sites/default/files/files/cuppies_feature.jpg',
        'time':'10 minutes ago',
        'numComments':'6',
        'type':'2'}
    fake_c3 = {
        'hearts':'12',
        'has_liked':'no',
        'author':'Sophie Swanson',
        'user_id':'10152691229087251',
        'comments':'OMG, everyone has to get try the chocolate chip cookie. It is literally the best thing I have every eaten.',
        'c_id':'31',
        'location':'Cuppies and Joe',
        'image':'http://scontent-b.cdninstagram.com/hphotos-xap1/t51.2885-15/928578_248359218698465_368109086_a.jpg',
        'time':'2 minutes ago',
        'numComments':'6',
        'type':'2'}
    fake_c4 = {
        'hearts':'15',
        'has_liked':'no',
        'author':'Jan Zielonka',
        'user_id':'10153313145682417',
        'comments':'We are here just hanging out. Everyone come over and grab some cupcakes and coffee!',
        'c_id':'33',
        'location':'Cuppies and Joe',
        'image':'none',
        'time':'1 minute ago',
        'numComments':'0',
        'type':'1'}
    fake_c5 = {
        'hearts':'35',
        'has_liked':'yes',
        'author':'Hannah  Sachs',
        'user_id':'295',
        'comments':'Beatiful coffee art and a delicious cupcake? How could it get better than this? Lol.',
        'c_id':'23',
        'location':'Cuppies and Joe',
        'image':'http://cuppiesandjoe.com/assets/components/cliche/cache/1/7/_-300x300-zc.png',
        'time':'10 minutes ago',
        'numComments':'8',
        'type':'2'}
    fake_c6 = {
        'hearts':'18',
        'has_liked':'no',
        'author':'Karl Marback',
        'user_id':'304',
        'comments':"What's good here?",
        'c_id':'42',
        'location':'Cuppies and Joe',
        'image':'none',
        'time':'20 minutes ago',
        'numComments':'12',
        'type':'1'}
    #fake_sent.append(fakep1)
    fake_sent.append(fake_c1)
    fake_sent.append(fake_c2)
    fake_sent.append(fake_c3)
    fake_sent.append(fake_c4)
    fake_sent.append(fake_c5)
    fake_sent.append(fake_c6)
    #fake_sent.append(fakep2)
    return jsonify(results = fake_sent)

#Actually at Cuppies and Joe
@app.route('/mobile_video_feed_8', methods = ["GET", "POST"])
def mobile_video_feed_8():
    fake_sent = []
    user1 = User.query.filter_by(nickname = "Ben Ackerman").first()
    user1id = str(user1.fb_id)
    user1Name = user1.nickname
    user2 = User.query.filter_by(nickname = "Ani Sefaj").first()
    user2id = str(user2.fb_id)
    user2Name = user2.nickname
    user3 = User.query.filter_by(nickname = "Julia Lee").first()
    user3id = str(user3.fb_id)
    user3Name = user3.nickname
    numMorePeople = "18"
    pic1 = "http://s3-media1.fl.yelpcdn.com/bphoto/Asqoz0SIoQfn6lyFwyPMZw/ls.jpg"
    pic2 = "https://v.cdn.vine.co/r/avatars/6253459C-B8A4-47BB-B0B7-6C2B915E520F-516-000001DD542C5329c7430da8dc.jpg?versionId=rI4BPHtjJQd76JAqAJ.3JESyKGPiwxbd"
    pic3 = "http://s3.amazonaws.com/foodspotting-ec2/reviews/2737952/thumb_600.jpg?1353121375"
    pic4 = "http://s3-media1.fl.yelpcdn.com/bphoto/iBCFt4RvhoiHksq3MMu8GA/ls.jpg"
    latLon = "35.457748, -97.618143"
    fakep1 = {
        'type':'3',
        'locationAddress':"Sherlock's Pub",
        'user1fb':user1id,
        'user1Name':user1Name,
        'user2fb':user2id,
        'user2Name':user2Name,
        'user3fb':user3id,
        'user3Name':user3Name,
        'numMore':numMorePeople,
        'pic1Link':pic1,
        'pic2Link':pic2,
        'pic3Link':pic3,
        'pic4Link':pic4,
        'location':latLon
        }
    fake_c1 = {
        'hearts':'8',
        'has_liked':'no',
        'author':'Isabelle Savoie',
        'user_id':'317',
        'comments':'Cuppies and Joe, chilling with this girl and getting my caff on. This place is the bomb!',
        'c_id':'25',
        'location':'Cuppies and Joe',
        'image':'https://v.cdn.vine.co/v/avatars/3650B248-F2A9-4736-8377-6E91129435CB-1119-00000125E1260E55.jpg?versionId=ftiN.XX3P1lOKHfu4th.ua4vuhujGh3E',
        'time':'1 minute ago',
        'numComments':'3',
        'type':'2'}
    fake_c2 = {
        'hearts':'38',
        'has_liked':'no',
        'author':'Sabrina Bleich',
        'user_id':'319',
        'comments':'10% off your order if you mention Hive.',
        'c_id':'30',
        'location':'Cuppies and Joe',
        'image':'http://www.keepitlocalok.com/sites/default/files/files/cuppies_feature.jpg',
        'time':'10 minutes ago',
        'numComments':'6',
        'type':'2'}
    fake_c3 = {
        'hearts':'12',
        'has_liked':'no',
        'author':'Sophie Swanson',
        'user_id':'10152691229087251',
        'comments':'OMG, everyone has to get try the chocolate chip cookie. It is literally the best thing I have every eaten.',
        'c_id':'31',
        'location':'Cuppies and Joe',
        'image':'http://scontent-b.cdninstagram.com/hphotos-xap1/t51.2885-15/928578_248359218698465_368109086_a.jpg',
        'time':'2 minutes ago',
        'numComments':'6',
        'type':'2'}
    fake_c4 = {
        'hearts':'15',
        'has_liked':'no',
        'author':'Jan Zielonka',
        'user_id':'10153313145682417',
        'comments':'We are here just hanging out. Everyone come over and grab some cupcakes and coffee!',
        'c_id':'33',
        'location':'Cuppies and Joe',
        'image':'none',
        'time':'1 minute ago',
        'numComments':'0',
        'type':'1'}
    fake_c5 = {
        'hearts':'35',
        'has_liked':'yes',
        'author':'Hannah  Sachs',
        'user_id':'295',
        'comments':'Beatiful coffee art and a delicious cupcake? How could it get better than this? Lol.',
        'c_id':'23',
        'location':'Cuppies and Joe',
        'image':'http://cuppiesandjoe.com/assets/components/cliche/cache/1/7/_-300x300-zc.png',
        'time':'10 minutes ago',
        'numComments':'8',
        'type':'2'}
    fake_c6 = {
        'hearts':'18',
        'has_liked':'no',
        'author':'Karl Marback',
        'user_id':'304',
        'comments':"What's good here?",
        'c_id':'42',
        'location':'Cuppies and Joe',
        'image':'none',
        'time':'20 minutes ago',
        'numComments':'12',
        'type':'1'}
    fake_sent.append(fakep1)
    fake_sent.append(fake_c1)
    fake_sent.append(fake_c2)
    fake_sent.append(fake_c3)
    fake_sent.append(fake_c4)
    fake_sent.append(fake_c5)
    fake_sent.append(fake_c6)
    #fake_sent.append(fakep2)
    return jsonify(results = fake_sent)


#Skate Park 1    before submitting the comment and refresh
@app.route('/mobile_video_feed_4', methods = ["GET", "POST"])
def mobile_video_feed_4():
    fake_sent = []
    pic5 = "http://californiaskateparks.com/wp-content/uploads/2012/08/skatepark-projects-box.jpg"
    pic6 = "http://s3-media2.fl.yelpcdn.com/bphoto/0DfbRjqhpzLXGkDWHToztQ/ls.jpg"
    pic7 = "http://cdn1.fast-serve.net/cdn/bullethd/Skateboarding-with-BulletHD_700_600_4ZOHM.jpg"
    pic8 = "http://www.howtobeadad.com/wp-content/uploads/2013/04/charlie-skateboarding.jpg"
    fake_c1 = {
        'hearts':'9',
        'has_liked':'yes',
        'author':'Derek Boyer',
        'user_id':'100000009454351',
        'comments':"Can someone teach me how to do an ollie? I'm a total noob, lol.",
        'c_id':'55',
        'location':'Bricktown Skatepark',
        'image':'none',
        'time':'5 minutes ago',
        'numComments':'8',
        'type':'1'}
    fake_c2 = {
        'hearts':'32',
        'has_liked':'yes',
        'author':'Ken Yanagisawa',
        'user_id':'891795569',
        'comments':"This place is so legit. I'm about to go so ham over those steps. #dontbelievemejustwatch",
        'c_id':'30',
        'location':'Bricktown Skatepark',
        'image':pic5,
        'time':'5 minutes ago',
        'numComments':'2',
        'type':'2'}
    fake_c3 = {
        'hearts':'55',
        'has_liked':'no',
        'author':'Sam Frampton',
        'user_id':'620567847',
        'comments':"This guy has no idea what he's doing. Lol.",
        'c_id':'84',
        'location':'Bricktown Skatepark',
        'image':pic6,
        'time':'15 minutes ago',
        'numComments':'22',
        'type':'2'}
    fake_c4 = {
        'hearts':'12',
        'has_liked':'no',
        'author':'Dylan Gans',
        'user_id':'100000016102525',
        'comments':"Skateboards are the perfect mode of transportation for people who have nowhere to be! Lol.",
        'c_id':'83',
        'location':'Bricktown Skatepark',
        'image':'none',
        'time':'30 minute ago',
        'numComments':'0',
        'type':'1'}
    #fake_sent.append(fakep1)
    fake_sent.append(fake_c1)
    fake_sent.append(fake_c2)
    fake_sent.append(fake_c3)
    fake_sent.append(fake_c4)
    #fake_sent.append(fakep2)
    return jsonify(results = fake_sent)





#Skate Park 2    after submitting the comment and refresh
@app.route('/mobile_video_feed_5', methods = ["GET", "POST"])
def mobile_video_feed_5():
    fake_sent = []
    pic5 = "http://californiaskateparks.com/wp-content/uploads/2012/08/skatepark-projects-box.jpg"
    pic6 = "http://s3-media2.fl.yelpcdn.com/bphoto/0DfbRjqhpzLXGkDWHToztQ/ls.jpg"
    pic7 = "http://cdn1.fast-serve.net/cdn/bullethd/Skateboarding-with-BulletHD_700_600_4ZOHM.jpg"
    pic8 = "http://www.howtobeadad.com/wp-content/uploads/2013/04/charlie-skateboarding.jpg"
    fake_c0 = {
        'hearts':'1',
        'has_liked':'yes',
        'author':'Alano McClain',
        'user_id':'100002693072880',
        'comments':"Matt killing it!",
        'c_id':'59',
        'location':'Bricktown Skatepark',
        'image':'http://scontent-b.cdninstagram.com/hphotos-xpa1/t51.2885-15/10522325_1506386589575110_1306335938_a.jpg',
        'time':'5 minutes ago',
        'numComments':'0',
        'type':'2'}
    fake_c1 = {
        'hearts':'9',
        'has_liked':'yes',
        'author':'Derek Boyer',
        'user_id':'100000009454351',
        'comments':"Can someone teach me how to do an ollie? I'm a total noob, lol.",
        'c_id':'55',
        'location':'Bricktown Skatepark',
        'image':'none',
        'time':'5 minutes ago',
        'numComments':'8',
        'type':'1'}
    fake_c2 = {
        'hearts':'32',
        'has_liked':'yes',
        'author':'Ken Yanagisawa',
        'user_id':'891795569',
        'comments':"This place is so legit. I'm about to go so ham over those steps. #dontbelievemejustwatch",
        'c_id':'30',
        'location':'Bricktown Skatepark',
        'image':pic5,
        'time':'5 minutes ago',
        'numComments':'2',
        'type':'2'}
    fake_c3 = {
        'hearts':'55',
        'has_liked':'no',
        'author':'Sam Frampton',
        'user_id':'620567847',
        'comments':"This guy has no idea what he's doing. Lol.",
        'c_id':'84',
        'location':'Bricktown Skatepark',
        'image':pic6,
        'time':'15 minutes ago',
        'numComments':'22',
        'type':'2'}
    fake_c4 = {
        'hearts':'12',
        'has_liked':'no',
        'author':'Dylan Gans',
        'user_id':'100000016102525',
        'comments':"Skateboards are the perfect mode of transportation for people who have nowhere to be! Lol.",
        'c_id':'83',
        'location':'Bricktown Skatepark',
        'image':'none',
        'time':'30 minute ago',
        'numComments':'0',
        'type':'1'}
    #fake_sent.append(fakep1)
    fake_sent.append(fake_c0)
    fake_sent.append(fake_c1)
    fake_sent.append(fake_c2)
    fake_sent.append(fake_c3)
    fake_sent.append(fake_c4)
    #fake_sent.append(fakep2)
    return jsonify(results = fake_sent)


#Sherlocks 1    after submitting the comment and refresh
@app.route('/mobile_video_feed_7', methods = ["GET", "POST"])
def mobile_video_feed_7():
    fake_sent = []
    # user1 = User.query.filter_by(nickname = "Ben Ackerman").first()
    # user1id = str(user1.fb_id)
    # user1Name = user1.nickname
    # user2 = User.query.filter_by(nickname = "Ani Sefaj").first()
    # user2id = str(user2.fb_id)
    # user2Name = user2.nickname
    # user3 = User.query.filter_by(nickname = "Julia Lee").first()
    # user3id = str(user3.fb_id)
    # user3Name = user3.nickname
    pic0 = "https://s-media-cache-ak0.pinimg.com/236x/f1/be/cd/f1becdc586835d7a22a25f43db4a7ceb.jpg"
    pic1 = "http://s3-media1.fl.yelpcdn.com/bphoto/Asqoz0SIoQfn6lyFwyPMZw/ls.jpg"
    pic2 = "https://v.cdn.vine.co/r/avatars/6253459C-B8A4-47BB-B0B7-6C2B915E520F-516-000001DD542C5329c7430da8dc.jpg?versionId=rI4BPHtjJQd76JAqAJ.3JESyKGPiwxbd"
    pic3 = "http://s3.amazonaws.com/foodspotting-ec2/reviews/2737952/thumb_600.jpg?1353121375"
    pic4 = "http://s3-media1.fl.yelpcdn.com/bphoto/iBCFt4RvhoiHksq3MMu8GA/ls.jpg"
    fake_c0 = {
        'hearts':'1',
        'has_liked':'yes',
        'author':'Alano McClain',
        'user_id':'100002693072880',
        'comments':"Oh man, this place is great.",
        'c_id':'59',
        'location':'Sherlocks Pub',
        'image':pic0,
        'time':'5 minutes ago',
        'numComments':'0',
        'type':'2'}
    fake_c1 = {
        'hearts':'9',
        'has_liked':'yes',
        'author':'Ben Ackerman',
        'user_id':'1450121801',
        'comments':"Wow, never been to this place, but it's so cool. I love 'pubs', I feel like I'm in the UK!",
        'c_id':'55',
        'location':'Sherlocks Pub',
        'image':'none',
        'time':'5 minutes ago',
        'numComments':'8',
        'type':'1'}
    fake_c2 = {
        'hearts':'32',
        'has_liked':'yes',
        'author':'Eric Nelson',
        'user_id':'585922386',
        'comments':"Yo, this guy seems like part of the family! Lol.",
        'c_id':'30',
        'location':'Sherlocks Pub',
        'image':pic2,
        'time':'1 minute ago',
        'numComments':'2',
        'type':'2'}
    fake_c3 = {
        'hearts':'55',
        'has_liked':'no',
        'author':'Julia Lee',
        'user_id':'1380270277',
        'comments':"Ricky and Mike battling it out on air hockey. #therecanonlybeone",
        'c_id':'84',
        'location':'Sherlocks Pub',
        'image':pic1,
        'time':'8 minutes ago',
        'numComments':'22',
        'type':'2'}
    fake_c4 = {
        'hearts':'17',
        'has_liked':'no',
        'author':'Ani Sefaj',
        'user_id':'693728810',
        'comments':"How much do you all think I can drink tonight? Probably too much...",
        'c_id':'83',
        'location':'Sherlocks Pub',
        'image':'none',
        'time':'22 minute ago',
        'numComments':'0',
        'type':'1'}
    #fake_sent.append(fakep1)
    fake_sent.append(fake_c0)
    fake_sent.append(fake_c1)
    fake_sent.append(fake_c2)
    fake_sent.append(fake_c3)
    fake_sent.append(fake_c4)
    #fake_sent.append(fakep2)
    return jsonify(results = fake_sent)



#Sherlocks 1    before submitting the comment and refresh
@app.route('/mobile_video_feed_6', methods = ["GET", "POST"])
def mobile_video_feed_6():
    fake_sent = []
    # user1 = User.query.filter_by(nickname = "Ben Ackerman").first()
    # user1id = str(user1.fb_id)
    # user1Name = user1.nickname
    # user2 = User.query.filter_by(nickname = "Ani Sefaj").first()
    # user2id = str(user2.fb_id)
    # user2Name = user2.nickname
    # user3 = User.query.filter_by(nickname = "Julia Lee").first()
    # user3id = str(user3.fb_id)
    # user3Name = user3.nickname
    pic1 = "http://s3-media1.fl.yelpcdn.com/bphoto/Asqoz0SIoQfn6lyFwyPMZw/ls.jpg"
    pic2 = "https://v.cdn.vine.co/r/avatars/6253459C-B8A4-47BB-B0B7-6C2B915E520F-516-000001DD542C5329c7430da8dc.jpg?versionId=rI4BPHtjJQd76JAqAJ.3JESyKGPiwxbd"
    pic3 = "http://s3.amazonaws.com/foodspotting-ec2/reviews/2737952/thumb_600.jpg?1353121375"
    pic4 = "http://s3-media1.fl.yelpcdn.com/bphoto/iBCFt4RvhoiHksq3MMu8GA/ls.jpg"
    fake_c1 = {
        'hearts':'9',
        'has_liked':'yes',
        'author':'Ben Ackerman',
        'user_id':'1450121801',
        'comments':"Wow, never been to this place, but it's so cool. I love 'pubs', I feel like I'm in the UK!",
        'c_id':'55',
        'location':'Sherlocks Pub',
        'image':'none',
        'time':'5 minutes ago',
        'numComments':'8',
        'type':'1'}
    fake_c2 = {
        'hearts':'32',
        'has_liked':'yes',
        'author':'Eric Nelson',
        'user_id':'585922386',
        'comments':"Yo, this guy seems like part of the family! Lol.",
        'c_id':'30',
        'location':'Sherlocks Pub',
        'image':pic2,
        'time':'1 minute ago',
        'numComments':'2',
        'type':'2'}
    fake_c3 = {
        'hearts':'55',
        'has_liked':'no',
        'author':'Julia Lee',
        'user_id':'1380270277',
        'comments':"Ricky and Mike battling it out on air hockey. #therecanonlybeone",
        'c_id':'84',
        'location':'Sherlocks Pub',
        'image':pic1,
        'time':'8 minutes ago',
        'numComments':'22',
        'type':'2'}
    fake_c4 = {
        'hearts':'17',
        'has_liked':'no',
        'author':'Ani Sefaj',
        'user_id':'693728810',
        'comments':"How much do you all think I can drink tonight? Probably too much...",
        'c_id':'83',
        'location':'Sherlocks Pub',
        'image':'none',
        'time':'22 minute ago',
        'numComments':'0',
        'type':'1'}
    #fake_sent.append(fakep1)
    fake_sent.append(fake_c1)
    fake_sent.append(fake_c2)
    fake_sent.append(fake_c3)
    fake_sent.append(fake_c4)
    #fake_sent.append(fakep2)
    return jsonify(results = fake_sent)

