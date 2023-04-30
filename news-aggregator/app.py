# Author: Igor Pantaleão
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime 


db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'

db.init_app(app)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thumbnail = db.Column(db.String)
    link = db.Column(db.String)
    publication_date = db.Column(db.String)

    def serialize(self):
        title = self.link.split('/')[-2]
        print(f"Link: {self.link}")   # Debug information
        print(f"Title: {title}") 
        return {
            'id': self.id,
            'thumbnail': self.thumbnail,
            'link': self.link,
            'publication_date': self.publication_date,
            'title': title
        }






with app.app_context():
    db.create_all()
    for news_item in News.query.all():
        print(news_item.serialize())

@app.route('/', methods=['GET'])
def home():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 9, type=int)
    news = News.query.paginate(page=page, per_page=per_page)

    return render_template('base.html', news=news)





if __name__ == "__main__":
    app.run(debug=True)
