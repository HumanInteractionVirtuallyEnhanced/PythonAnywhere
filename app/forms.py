# import sqlalchemy as sa
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# #from wtforms import TextField, BooleanField, TextAreaField, SelectField, SubmitField, StringField
# #from wtforms.widgets import TextArea
# from flask.ext.wtf import Form
# #from wtforms.validators import DataRequired


# class LoginForm(Form):
#  	openid = TextField('openid', validators = [])
#  	remember_me = BooleanField('remember_me', default = False)








# class professorLoginForm(Form):
#     name = TextField(validators = [DataRequired()])
#     secretKey = TextField(validators = [DataRequired()])
#     email = TextField(validators = [DataRequired()])






# class SearchForm(Form):
#     search = StringField('search', validators=[DataRequired()])



# class emailForm(Form):
#     email = TextField(validators = [DataRequired()])


# class fakeUserForm(Form):
# 	nickname = TextField(validators = [DataRequired()])
# 	email = TextField(validators = [DataRequired()])
# 	remember_me = BooleanField('remember_me', default = False)




# class submitCommentForm(Form):
# 	body = TextField(validators = [DataRequired()])

# class submitReplyForm(Form):
# 	body = TextField(validators = [DataRequired()])
# 	reply_id = StringField(validators = [DataRequired()])


# #################################################################
# #####################ADMIN FORMS#################################

# class createEventForm(Form):
# 	title = TextField(validators = [DataRequired()])
# 	course_number = TextField(validators = [DataRequired()])
# 	description = TextField(validators = [DataRequired()])
# 	professorName = TextField(validators = [DataRequired()])
# 	icon_url = TextField()
# 	start_time = TextField(validators = [DataRequired()])
# 	end_time = TextField(validators = [DataRequired()])
# 	bool_monday = BooleanField('bool_monday', default = False)
# 	bool_tuesday = BooleanField('bool_tuesday', default = False)
# 	bool_wednesday = BooleanField('bool_wednesday', default = False)
# 	bool_thursday = BooleanField('bool_thursday', default = False)
# 	bool_friday = BooleanField('bool_friday', default = False)
# 	bool_saturday = BooleanField('bool_saturday', default = False)
# 	bool_sunday = BooleanField('bool_sunday', default = False)


