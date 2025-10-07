from flask import Flask, render_template, request
import pypyodbc as odbc

app = Flask(__name__)

# Database Configuration
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = r'SHANNONHP\MSSQLSERVER01'  # Using raw string to handle backslash
DATABASE_NAME = 'VeganRecipes'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

conn = odbc.connect(connection_string)

# Home route
@app.route("/")
def home():
    return render_template("index.html")


# Start Routes for testing search functionality-----------------------------------
@app.route("/search")
def search_home():
    return render_template("./search-demo/search_home.html")

# Main search route - URL path based
@app.route("/recipes/search/<search_term>")
def search_recipes(search_term):
    if not search_term or search_term.strip() == "":
        return "Please provide a search term", 400
    
    local_cursor = conn.cursor()
    try:
        # Search in both recipe name and description for better results
        search_cursor = local_cursor.execute(
            """SELECT recipe_id, recipe_name, recipe_description 
               FROM recipes 
               WHERE recipe_name LIKE ? OR recipe_description LIKE ?""",  #LIKE means partial match
            #this adds % wildcard to both sides of the search term for partial matches
            # meaning it will match any recipe name or description that contains the search term anywhere within it
            # '%' + search_term + '%' is added twice, once for recipe_name and once for recipe_description
            ['%' + search_term + '%', '%' + search_term + '%']#the parameters for the SQL query being passed in as a list, because there are two placeholders in the query (two ?s)
        )
        search_results = search_cursor.fetchall()# Fetch all matching records
        
        #search_results is a list of tuples, where each tuple represents a row from the database
        #each tuple contains (recipe_id, recipe_name, recipe_description)

        # Convert to list for easier template handling
        results_list = []
        for row in search_results:#for each row in the search results, append to results_list
            results_list.append([row[0], row[1], row[2]])#row[0] is recipe_id, row[1] is recipe_name, row[2] is recipe_description
            
        if not results_list:# IF NO RESULTS FOUND
            return render_template("./search-demo/search_results.html", 
                                 results=[], 
                                 search_term=search_term,
                                 no_results=True)
    except Exception as e:
        return f"Database error occurred: {str(e)}", 500
    finally:
        local_cursor.close()

    return render_template("./search-demo/search_results.html", 
                         results=results_list, 
                         search_term=search_term,
                         no_results=False)

# Alternative search route using query parameters (more conventional)
# why is this more conventional? because it allows for multiple parameters to be passed in the URL
# and it is more flexible for users to share links with specific search terms
# using two different routes for search, only to demonstrate both methods
# and to show how to handle query parameters in Flask
# just use one in projects, the query parameter method is generally preferred for search functionality
@app.route("/query_search_results") # Example: http://localhost:5001/query_search_results?querySearchTerm=pasta
def search_recipes_query():
    # request.args.get retrieves query parameters from the URL, so there is no need to pass anything in the URL path
        # requests.args.get() method's parameters: (key, default=None, type=None)
            # key: the name of the parameter to retrieve from the query string
            # default: the value to return if the parameter is not found (default is None)
            # type: the type to which the parameter should be converted (default is str)

    # the querySearchTerm gets put in the URL by the form
    # the form does this by using the GET method, which appends the form data to the URL as query parameters
    # Get the search term from query parameters
    # 'querySearchTerm' matches the form input name, which is where the search term is entered
    search_term = request.args.get('querySearchTerm', '').strip()

    #if search term is empty string, return no results page
    if not search_term:# IF USER ENTERS A EMPTY STRING, LIKE SPACES
        return render_template("./search-demo/search_results.html", 
                             results=[], # empty results
                             search_term="",# empty search term
                             no_results=True,# no results found
                             #Since this error message is only shown when no search term is entered, it is safe to hardcode it here.
                             #this is why the error message is shown in the search_results.html template
                             error_message="Please enter a search term")
    
    #if search term is present, redirect to the main search function
    return search_recipes(search_term)# IF USER ENTERS A VALID SEARCH TERM

# Recipe detail route (needed for search results links)
@app.route("/recipes/<int:recipe_id>")
def get_recipe_details(recipe_id):
    local_cursor = conn.cursor()
    try:
        recipe_cursor = local_cursor.execute(
            "SELECT recipe_id, recipe_name, recipe_description FROM recipes WHERE recipe_id = ?", [recipe_id]
        )
        recipe = recipe_cursor.fetchone()
        if recipe is None:
            return f"Recipe with ID {recipe_id} not found.", 404
        
        recipe_details = [recipe[0], recipe[1], recipe[2]]
        
    except Exception as e:
        return f"Database error occurred: {str(e)}", 500
    finally:
        local_cursor.close()

    return render_template("./search-demo/recipe_detail.html", recipe=recipe_details)
# End Routes for testing search functionality-----------------------------------





if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Different port to avoid conflicts