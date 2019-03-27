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

@app.route('/get_suggestion')          
def get_suggestion():             
    return render_template("suggestions.html")   
    
    
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
    
@app.route("/edit_recipe", methods=['GET'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('edit_recipe'))
    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('editrecipe.html', recipe=the_recipe,
                           categories=all_categories)    
    
@app.route('/update_recipe/<the_recipe>', methods=["POST", ])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'),
        'category_name':request.form.get('category_name'),
        'recipe_ingredients': request.form.get('recipe_ingredients'),
        'recipe_direction': request.form.get('recipe_direction'),
        'recipe_preptime':request.form.get('recipe_preptime'),
        'recipe_cook':request.form.get('recipe_cook'),
        'recipe_person':request.form.get('recipe_person'),
        'recipe_image_url':request.form.get('recipe_image_url')
        
        
        
    })
    return redirect(url_for('get_recipes'))
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)


