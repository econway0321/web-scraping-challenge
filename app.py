from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scarpe_mars


app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

@app.route('/')
def index():
	mars=mongo.db.mars.find_one()
	return render_template(index.html,mars=mars)

@app.route('/scrape')
def scrape():
	mars=mongo.db.mars
	mars_dict=scarpe_mars.scrape_all()
	mars.update({},mars_dict,upsert=True)

	return redirect('/')


if __name__ == '__main__':
    app.run()

