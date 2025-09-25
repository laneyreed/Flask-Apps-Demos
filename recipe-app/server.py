from flask import Flask, render_template
import pypyodbc as odbc
import requests


app = Flask(__name__)

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'SHANNONHP\MSSQLSERVER01'
DATABASE_NAME = 'VeganRecipes'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

conn = odbc.connect(connection_string)

# cursor = conn.cursor()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recipes-categories")
def get_recipe_categories():
    return render_template("category_list.html")

@app.route("/recipes/type/<recipe_type>")
def get_recipes_by_type(recipe_type):
     recipe_type_map = {
         "appetizers": 1,
         "breakfast": 2,
         "soups": 3,
         "salads": 5,
         "sides": 6,
         "entrees": 7,
         "desserts": 10
     }

     recipe_type_id = recipe_type_map.get(recipe_type.lower())
     if recipe_type_id is None:
         return f"Unknown recipe type: {recipe_type}", 404

     local_cursor = conn.cursor()
     try:
         recipes_cursor = local_cursor.execute("SELECT recipe_id, recipe_name, recipe_description FROM recipes WHERE recipe_type_id = ?", [recipe_type_id])
         recipes_list = []
         for row in recipes_cursor:
             recipe_id = row[0]
             recipe_name = row[1]
             recipe_description = row[2]
             recipes_list.append([recipe_id, recipe_name, recipe_description])
     finally:
         local_cursor.close()

     template_path = "recipe_cards_list.html"
     return render_template(template_path, recipes=recipes_list, category_title=recipe_type)


#create a route to display a specific recipe
@app.route("/recipes/<int:recipe_id>")
def get_recipe_details(recipe_id):
    local_cursor = conn.cursor()
    try:
        recipe_cursor = local_cursor.execute(
            "SELECT * FROM recipes WHERE recipe_id = ?", [recipe_id]
        )
        recipe = recipe_cursor.fetchone()
        if recipe is None:
            return f"Recipe with ID {recipe_id} not found.", 404
        recipe_details_list = []
        recipe_id = recipe[0]
        # recipe_details_list.append(recipe_id)
        recipe_name = recipe[1]
        # recipe_details_list.append(recipe_name)
        recipe_description = recipe[2]
        # recipe_details_list.append(recipe_description)
        recipe_prep_time = recipe[3]
        # recipe_details_list.append(recipe_prep_time)
        recipe_cook_time = recipe[4]
        # recipe_details_list.append(recipe_cook_time)
        recipe_author_id = recipe[5]
        # recipe_details_list.append(recipe_author_id)
        recipe_type_id = recipe[6]
        # recipe_details_list.append(recipe_type_id)

        # Use slicing over individual assignments
        #  appending each field individually is a valid approach, it is verbose and prone to error if the number of desired fields changes
        # this single line slicing operation accomplishes the same goal more efficiently and elegantly
        # it is the "Pythonic" way to handle such a task
        recipe_details_list = list(recipe[:7])


        ingredients_cursor = local_cursor.execute(
            """
            SELECT ri.quantity, mu.measurement_unit_name, i.ingredient_name
            FROM recipes AS r
            INNER JOIN recipe_ingredient AS ri ON r.recipe_id = ri.recipe_id
            INNER JOIN measurement_units AS mu ON ri.measurement_unit_id = mu.measurement_unit_id
            INNER JOIN ingredients AS i ON ri.ingredient_id = i.ingredient_id
            WHERE r.recipe_id = ?
            """, [recipe_id]
        )
        recipe_ingredients = ingredients_cursor.fetchall()
        if recipe_ingredients is None:
            return f"Recipe with ID {recipe_id} ingredients not found.", 404

    finally:
        local_cursor.close()
    return render_template("recipe_detail.html", recipe=recipe_details_list, ingredients=recipe_ingredients)



if __name__ == "__main__":
    app.run(debug=True)
