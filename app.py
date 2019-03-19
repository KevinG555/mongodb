import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'my_recipe'
app.config["MONGO_URI"] = 'mongodb://kegrl:Cagla2019!@ds263295.mlab.com:63295/my_recipe'

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_recipes')          
def get_recipes():             
    return render_template("index.html", recipes=mongo.db.recipes.find())
    
@app.route("/sandwiches")
def sandwiches():
    return render_template("sandwiches.html", recipes=mongo.db.recipes.find({"category_name": "Sandwich"})) 

@app.route("/cakes")
def cakes():
    return render_template("cakes.html", recipes=mongo.db.recipes.find({"category_name": "Cake"}))        
        
@app.route("/pastas")
def pastas():
    return render_template("pasta.html", recipes=mongo.db.recipes.find({"category_name": "Pasta"})) 

@app.route("/vegan")
def vegan():
    return render_template("vegan.html", recipes=mongo.db.recipes.find({"category_name": "Vegetarian"}))

@app.route("/add_recipe")
def add_recipe():
    return render_template("addrecipe.html", categories = mongo.db.categories.find())
    
@app.route("/insert_recipe", methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)


