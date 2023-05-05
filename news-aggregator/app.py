# Author: Igor Pantaleão
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime 


db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/igor/myprojects/flask/news-aggregator/rottentomatoes.db'
app.config['SQLALCHEMY_BINDS'] = {
    'tvshows': 'sqlite:////home/igor/myprojects/flask/news-aggregator/comics.db',
    'tvshows': 'sqlite:////home/igor/myprojects/flask/news-aggregator/tvshows-news.db'
}

db.init_app(app)

class News(db.Model):
    __tablename__='articles'
    id = db.Column(db.Integer, primary_key=True)
    thumbnail = db.Column(db.String)
    link = db.Column(db.String)
    publication_date = db.Column(db.String)
    title = db.Column(db.String)

    def serialize(self):
        
        return {
            'id': self.id,
            'thumbnail': self.thumbnail,
            'link': self.link,
            'publication_date': self.publication_date,
            'title': self.title
        }


class Comics(db.Model):
    __bind_key__ = 'tvshows'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    summary = db.Column(db.String)
    author = db.Column(db.String)
    image = db.Column(db.String)

    def serialize(self):
        
        return {
            'id': self.id,
            'title': self.title,
            'link': self.link,
            'summary': self.summary,
            'author': self.author,
            'image': self.image
        }


class Tvshows(db.Model):
    __bind_key__ = 'tvshows'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    summary = db.Column(db.String)
    author = db.Column(db.String)
    image = db.Column(db.String)

    def serialize(self):
        
        return {
            'id': self.id,
            'title': self.title,
            'link': self.link,
            'summary': self.summary,
            'author': self.author,
            'image': self.image
        }


with app.app_context():
    db.create_all()



@app.route('/movies', methods=['GET'])
def movies():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    news = News.query.paginate(page=page, per_page=per_page)

    return render_template('movies.html', news=news)

@app.route('/comics', methods=['GET'])
def comicsNews():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    comics = Comics.query.paginate(page=page, per_page=per_page)

    return render_template('comics.html', comics=comics)  

@app.route('/tvshows', methods=['GET'])
def tvshowsNews():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    tvshow = Tvshows.query.paginate(page=page, per_page=per_page)

    return render_template('tvshows.html', tvshow=tvshow) 






if __name__ == "__main__":
    app.run(debug=True)
