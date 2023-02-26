from configparser import InterpolationMissingOptionError
import sqlite3
import pandas as pd
import csv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import sqlite3
import pandas as pd
from Dic_expressions import new_dict

# Create your connection.

# To create a database 
# sqlite3.connect('ingredients.db')


conn = sqlite3.connect('ingredients.db') 
c = conn.cursor()
# c.execute('''DROP TABLE Servings''')
# conn.commit()
# Base tables 
c.execute('''
          CREATE TABLE IF NOT EXISTS Calorie
          ([ItemID] INTEGER PRIMARY KEY, 
          [Item_Name] WORDS,
          [Calories] FLOAT, 
          [Fat_value] FLOAT, 
          [Carbohydrates] FLOAT, 
          [Protein] FLOAT,
          [Sodium] FLOAT,
          [Potassium] FLOAT)
          ''') 
conn.commit()
c.execute('''
          CREATE TABLE IF NOT EXISTS Servings
          ([ItemID] INTEGER PRIMARY KEY,
          [Item_Name] WORDS,
          [bowl] FLOAT,
          [cup] FLOAT,
          [1tablespoon] FLOAT,
          [1teaspoon] FLOAT,
          [small] FLOAT,
          [medium] FLOAT,
          [large] FLOAT)
          ''') 
conn.commit()


nutrients = pd.read_csv('D:\\Learning\\Ml Intern(analysed)\\Calorie Calculator\\Nutrients.csv')
#  # # Write the data to a sqlite db table
nutrients.to_sql('Calorie', conn, if_exists='replace', index=False)
conn.commit() 
conn.close()
# Connect to the .db file
conn = sqlite3.connect('ingredients.db')
# Create a cursor object
cursor = conn.cursor()
cursor.execute('SELECT * FROM Calorie')
rows = cursor.fetchall()
dict_y = {}
# index_coloumn =[]
for row in rows:
    index_column = row[1]
    index_column = index_column.replace(",","")
    values = {'Calories': row[2], 'Fat_value': row[3],'Carobohydrates': row[4],'Protein': row[5],'Sodium':row[6],'Potassium':row[7]}
    dict_y[index_column] = values
# print(dict_y.keys())
cursor.close()
conn.close()


units = list(new_dict.values())
unit_string = str('|'.join(units))


def servings(Ing):
    items = Ing.keys()
    # print(items)
    conn = sqlite3.connect('ingredients.db')
    # Create a cursor object
    cursor = conn.cursor()
    dict_z = {}
    for i in items:
        cursor.execute('SELECT * FROM Servings WHERE Item_Name=?',(i,))
        rows = cursor.fetchall()
        
        # index_coloumn =[]
        for row in rows:
            index_column = row[1]
            index_column = index_column.replace(",","")
            values = {'Bowl': row[2], 'Cup': row[3],'1tablespoon': row[4],'1teaspoon': row[5],'small':row[6],'medium':row[7],'large':row[8]}
            dict_z[index_column] = values
    
    cursor.close()
    conn.close()
    return dict_z


def extract_ingredients(recipe):
    ''' This function uses fuzzy matching to extract the best matched string from a given set of values.
    In this function we match our extracted ingredient from the recipe to a database created and select that key and it's respective 
    items to fetch the nutritional info and save it in the processed_ing to get the result better!!'''
    ingredients = {}
    processed_ingredients = set()
    my_list = []
    for sub_recipe in re.split(',', recipe):
        # print(sub_recipe)
        for match in re.finditer(rf"(\d+(\.\d+)?)( ?({unit_string})?)? ?(.*)", sub_recipe):
            quantity = match.group(1) + match.group(3) if match.group(3) else match.group(1)
            # print(quantity)
            ingredient = match.group(5)
            # print(ingredient)
            ingredient = lemmatizer.lemmatize(ingredient)
            if ingredient not in processed_ingredients:
                best_match = (None, 0)
            for known_ingredient, nutritional_info in dict_y.items():
                
                score = fuzz.token_set_ratio(ingredient, known_ingredient)
                if score > best_match[1]:
                    best_match = (known_ingredient, score)
                    
            if best_match[1] > 50:
                ingredients[best_match[0]] = quantity
                processed_ingredients.add(best_match[0])
                my_list.append(dict_y[best_match[0]])

    return ingredients, my_list
        
    

    