from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, URLField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange


db = SQLAlchemy()

class Movie(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100))
    year = db.Column(db.String(10))
    description = db.Column(db.String(768), unique=True)
    rating = db.Column(db.Float(), unique=False)
    review = db.Column(db.String(100), unique=False)
    img_url = db.Column(db.String(200))





class Form(FlaskForm):
    new_rating = FloatField(label="New rating", validators=[DataRequired(), NumberRange(min=0, max=10)])
    new_review = StringField(label="Your review", validators=[DataRequired(), Length(max=30)])
    Done = SubmitField(label="Done")


class Entry(FlaskForm):
    title = StringField(label="Title", validators=[DataRequired(), Length(max=50)])
    year = StringField(label="Release date", validators=[DataRequired(),Length(max=4)])
    description = StringField(label="Description", validators=[DataRequired(), Length(max=250)])
    rating = FloatField(label="rating", validators=[DataRequired(), NumberRange(min=0, max=10)])
    review = StringField(label="Your review", validators=[DataRequired(), Length(max=30)])
    img_url = URLField(label="Image", validators=[DataRequired(), Length(max=300)])
    Done = SubmitField(label="Done")

class Select(FlaskForm):
    Keyword = StringField(label="Title keyword", validators=[DataRequired(), Length(max=50)])
    Search = SubmitField(label="Search")