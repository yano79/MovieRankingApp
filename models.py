from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, URLField
from wtforms.validators import DataRequired, Length


db = SQLAlchemy()

class Movie(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(50))
    year = db.Column(db.Integer)
    description = db.Column(db.String(300), unique=True)
    rating = db.Column(db.String(30), unique=False)
    review = db.Column(db.String(200), unique=False)
    img_url = db.Column(db.String(200))





class Form(FlaskForm):
    new_rating = SelectField(label="Your rating",choices=["⭐" * n for n in range(1,11)], validators=[DataRequired()])
    new_review = StringField(label="Your review", validators=[DataRequired(), Length(max=30)])
    Done = SubmitField(label="Done")


class Entry(FlaskForm):
    title = StringField(label="Title", validators=[DataRequired(), Length(max=50)])
    year = StringField(label="Release date", validators=[DataRequired(),Length(max=4)])
    description = StringField(label="Description", validators=[DataRequired(), Length(max=250)])
    rating = SelectField(label="Your rating",choices=["⭐" * n for n in range(1,11)], validators=[DataRequired()])
    review = StringField(label="Your review", validators=[DataRequired(), Length(max=30)])
    img_url = URLField(label="Image", validators=[DataRequired(), Length(max=300)])
    Done = SubmitField(label="Done")

class Select(FlaskForm):
    Keyword = StringField(label="Title keyword", validators=[DataRequired(), Length(max=50)])
    Search = SubmitField(label="Search")