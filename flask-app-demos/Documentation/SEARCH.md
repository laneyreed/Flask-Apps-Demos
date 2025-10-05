# Search 

## Features
- **Database integration**: Same SQL Server connection
- **Error handling**: Input validation and database error catching
- **Search functionality**: Searches both recipe names and descriptions

##### Server Routes
- **Search Home with search Form** 
   -  ```python 
         @app.route("/search")
      ```
- **Alternative Search: Query Parameters(`/search?querySearchTerm=<search_term>`)**
   -  ```python 
         @app.route("/query_search_results")
      ```
- **Main search function: URL Path(`/recipes/search/<term>`)**
   -  ```python 
         @app.route("/recipes/search/<search_term>") 
      ```
- **Recipe View**
   -  ```python 
         @app.route("/recipes/<int:id>") 
      ```


## 🧪 Testing the Search

### Method 1: Use the Search Form
- Go to `http://localhost:5001/search`
- Use the search form on the homepage

### Method 2: Direct URL Access
- `http://localhost:5001/search?querySearchTerm=pasta`
- `http://localhost:5001/recipes/search/soup`

### Method 3: Quick Test Links
- Click the test buttons on the homepage

## 🔍 Search Features Demonstrated

1. **Input Validation**: Empty search term handling
2. **Database Search**: LIKE queries on name and description  
3. **Error Handling**: Database connection and SQL errors
4. **Result Processing**: Converting database rows to lists
5. **Template Integration**: Passing data to HTML templates
6. **Multiple Route Types**: Both URL path and query parameters

## 📊 Database Requirements

- SQL Server with `VeganRecipes` database
- `recipes` table with columns: `recipe_id`, `recipe_name`, `recipe_description`

## 🎨 Styling

Uses Bootstrap CDN for clean, responsive design without local CSS files.

---

**Perfect for**: Learning, testing, debugging, or demonstrating just the search functionality!