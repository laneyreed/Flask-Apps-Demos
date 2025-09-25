# Recipe-Sharing-Flask-App: Database Design
## 1. Figure out what data needs to be collected
- Recipe Name
- Recipe Description
- Author
- Recipe Type
- Prep Time
- Cook Time
- Total Time
- Ingredients

## 2. Figure out what data can be used in multiple recipes and put them into different tables and which data is unique to each recipe
- Author
- Recipe Type
- Prep Time
- Cook Time
- Total Time
- Ingredients

### Author
- an author can have many recipies, so we do not need to duplicate the authors
- a recipe can have only one author
    - one-to-many relationship with the recipes table
- could create an authors table then include a foreign key, author_id, column in the recipes table, which links each recipe back to a specific author    
    #### author
    | Column Name             | Data Type     | Constraint  |
    | :---------------------- | :-----------: | ----------: |
    | author_id               | int           | PK          |
    | author_name             | string        | NOT NULL    |
    | author_email            | string        | NOT NULL    |

### Recipe Type
- a recipe type can belong to many recipes, so we do not need to duplicate the recipe types
- a recipe can have only one recipe type
    - one-to-many relationship with the recipes table
- could create a recipe_types table then include a foreign key, recipe_type_id, column in the recipes table, which links each recipe back to a specific recipe_type  
    #### recipe_types
    | Column Name             | Data Type     | Constraint  |
    | :---------------------- | :-----------: | ----------: |
    | recipe_type_id          | int           | PK          |
    | recipe_type_name        | string        | NOT NULL    |

### Cook, Prep and total Time
- store prep and cook times in the recipes table with dedicated columns for each time measurement
- total time will be calculated dynamically from the prep and cook times
    - when a user requests a recipe, your application can compute the total time and display it as needed
    - use an SQL query to compute the total time, saving storage space and ensuring the value is always up to date
    - the recommended approach for most applications

### Ingredients
- ingredients can be used in multiple recipes, so we do not need to duplicate all those values
- a recipe has many ingredients, an ingredient has many recipes
    - many-to-many relationship
- **Example:** 1/4 tsp sea salt
    - **ingredient:** sea salt: could have sea salt in another recipe in our database
    
    - **measurement unit:** tsp: could have different tsp amounts
    - could create three different tables then use and join table to connect it with the recipes

        #### ingredients
        | Column Name             | Data Type     | Constraint          |
        | :---------------------- | :-----------: | ------------------: |
        | ingredient_id           | int           | PK                  |
        | ingredient_name         | string        | UNIQUE, NOT NULL    |

        #### measurement_units
        | Column Name             | Data Type     | Constraint  |
        | :---------------------- | :-----------: | ----------: |
        | measurement_unit_id     | int           | PK          |
        | measurement_unit_name   | string        | NOT NULL    |


- **measurement quantity:** 1/4: can be added to the join table


### Recipe Table
- recipe name and description will be different for each recipe, so we need to store both those values
- separate columns for prep and cook times, stored as integers representing minutes
- includes a foreign key column, author_id, which links each recipe back to a specific author
    - ensures that each recipe record in the Recipes table is tied to one and only one record in the authors table
- includes a foreign key column, recipe_type_id, which links each recipe back to a specific recipe type
    - ensures that each recipe record in the Recipes table is tied to one and only one record in the recipe_types table

        #### recipes
        | Column Name            | Data Type     |       Constraint        |
        | :--------------------- | :-----------: | ----------------------: |
        | recipe_id              | int           | PK                      |
        | recipe_name            | string        | NOT NULL                |
        | description            | string        | NOT NULL                |
        | prep_time_minutes      | int           | NOT NULL                |
        | cook_time_minutes      | int           | NOT NULL                |
        | author_id              | int           | FK ref authors table    |
        | recipe_type_id         | int           | FK ref recipe_type table|



## 3. Connect the joining tables
- The recipe table needs to be connected to the ingredients, measurement_units tables using a join table/associative table

### Recipe Ingredients Joining table
- this breaks the many-to-many relationship into two separate one-to-many relationships and also stores extra information, such as the quantity of each ingredient needed for a specific recipe

    #### recipe_ingredients
    | Column Name             | Data Type     | Constraint  |
    | :---------------------- | :-----------: | ----------: |
    | recipe_id               | int           | FK          |
    | ingredient_id           | int           | FK          |
    | quantity                | string        | NOT NULL    |
    | measurement_unit_id     | int           | FK          |