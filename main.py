from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resourses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)



class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'temp: {self.title}'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categ = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'temp: {self.categ}'

@app.route('/', methods=['GET'])
def index():
    items = Item.query.order_by(Item.id).all()
    searchRequest = ''
    searchRequest = request.args.get('searchField')
    if searchRequest:
        search = "%{}%".format(searchRequest)
        items = Item.query.filter(Item.title.like(search)).order_by(Item.id).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        try:
            title = request.form['title']
            link = request.form['link']
            text = request.form['text']
            if title and link:
                item = Item(title=title, link=link, text=text)
            db.session.add(item)
            db.session.commit()
            return  redirect('/')
        except:
            return "Error"
    else:
        return render_template('create.html')
    return render_template('create.html')

if __name__ == "__main__":
    app.run(debug=True)