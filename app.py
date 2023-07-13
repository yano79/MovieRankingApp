
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from sqlalchemy import URL
from models import Movie, db, Form, Select
import requests

app = Flask(__name__)

# HOST=aws.connect.psdb.cloud
# USERNAME=1eadhxwh6bc4jds0lm42
# PASSWORD=pscale_pw_WOctYSAds3YjK2My8dDlxH92YFai5yhyKZ2K4XsywiL
# DATABASE=yano_db

url_object = URL.create(
    "mysql+pymysql",
    username="ahkvz9jht65spaktby5j",
    password="pscale_pw_M9lz1A2xdkVMk9q90CqxgoR6u4hPsrlBgUiKgMRwfIQ",
    host="aws.connect.psdb.cloud",
    database="yano_db",
    port=3306,
    query={"ssl_ca": "/etc/ssl/cert.pem"}
)

API_KEY = '2edabd3ac514a4ff174adf7c3b213d57'
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"



headers = {
    "accept":
    "application/json",
    "Authorization":
    "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyZWRhYmQzYWM1MTRhNGZmMTc0YWRmN2MzYjIxM2Q1NyIsInN1YiI6IjY0NzY3NzMyODlkOTdmMDBiZWM0OGViOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ViECdHOmEWcgYB3LXIRqsW8DyZRZu5bIM5vl7qXzM_c"
  }





app.config['SQLALCHEMY_DATABASE_URI'] = url_object
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

Bootstrap(app)


new_movie = Movie(
        title="Phone Booth",
        year=2002,
        description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
        rating=7.3,
        review="My favourite character was the caller.",
        img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
    )
db.init_app(app)
# with app.app_context():
#     db.drop_all()
    # db.session.query(Movie).delete()
    # db.create_all()
    # db.session.add(new_movie)
    # db.session.commit()
# movie = db.session.query(Movie).all()




@app.route("/")
def home():
    movie = Movie.query.order_by(Movie.rating.desc()).all()
    # for i in range(len(movie)):
        # movie[i].id = i+1
    return render_template("index.html", movies=movie)

@app.route('/edit', methods=["GET", "POST"])
def edit():
    new_form = Form()
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)

    if new_form.validate_on_submit():
        db.session.query(Movie).where(Movie.id == movie_id).update(values={Movie.rating: new_form.new_rating.data, Movie.review: new_form.new_review.data})
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', form=new_form, movie=movie)

@app.route('/delete')
def delete():
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    title = movie.title
    db.session.query(Movie).filter(Movie.id == movie.id).delete(synchronize_session=False)
    db.session.commit()
    return render_template('delete.html', title=title)


@app.route('/add', methods=["GET", "POST"])
def add():

    # new_entry = Entry()
    # if new_entry.validate_on_submit():
    #     new_add = Movie(
    #         title=new_entry.title.data,
    #         year=new_entry.year.data,
    #         description=new_entry.description.data,
    #         rating=new_entry.rating.data,
    #         review=new_entry.review.data,
    #         img_url=new_entry.img_url.data
    #     )
    new_search = Select()
    if new_search.validate_on_submit():
        query = new_search.Keyword.data
        url = f"https://api.themoviedb.org/3/search/movie?query={query}&include_adult=false&language=en-US&page=1&region=USA%20"
        response = requests.get(url, headers=headers).json()
        return render_template('add.html', response=response, select_form=new_search)
    return render_template('select.html', select_form=new_search)
    #     db.session.add(new_add)
    #     db.session.commit()
    #     return redirect(url_for('home'))
    # return render_template('add.html', add_new=new_entry, select_form=new_search)


@app.route('/select', methods=["GET", "POST"])
def select():
    movie_api_id = request.args.get("id")
    movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
    if movie_api_id:
        response = requests.get(movie_api_url, params={'api_key': API_KEY, 'language': 'en-US'})
        data = response.json()
        new_add = Movie(
                title=data["title"],
                year=data["release_date"].split("-")[0],
                description=data["overview"],
                rating=data["vote_average"],
                review=" ",
                img_url=f"https://image.tmdb.org/t/p/original{data['poster_path']}"
            )
        db.session.add(new_add)
        db.session.commit()
        return redirect(url_for('edit', id=new_add.id))

if __name__ == '__main__':
    app.run(debug=True)