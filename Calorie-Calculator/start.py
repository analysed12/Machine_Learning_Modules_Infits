from nltk.tokenize import RegexpTokenizer
import nltk
# nltk.download('stopwords')
from Dic_expressions import new_dict, unit_conversions,exp_dict
from database import extract_ingredients,servings
from nltk.corpus import stopwords
import re
from testing import recipes_list
from re import match as re_match
import pandas as pd
import ast

# from helper import tokenize,classification
#   Helper functions 

extra_words = stopwords.words('english')
extra_words.append('of')

 
def recipe_cleaning(text:str):
    out = []
    for key,value in exp_dict.items():
        text = text.replace(f"{key}",f"{value}")
    # print(text)
    tokenizer = RegexpTokenizer(r'(\d*\.\d+)|(\d*)|(\d[\/]\d|\d[-]\d)|(\w\.)|([A-Za-z]+)')
    for t in tokenizer.tokenize(text):
        # print(t)
        for item in t:
            if item in extra_words:
                continue
            # To check symbols that cannot be interpreted in the recipe
            if item in exp_dict :
                item = exp_dict[item]
                out.append(item)
                continue
                
            # to check the abbrevations in the recipe 
            if item in new_dict:
                item = new_dict[item]
                out.append(item)
            else:
                out.append(item)
                continue

    newList = list(filter(None, out))
    final_text = ' '.join(newList)
    result = [m.group(1) + m.group(2) if m.group(1) else m.group(2) for m in re.finditer(r"([\d.]+)(\D+)", final_text)]
    recipe = ','.join(result)
    return recipe    

def convert(Ing,serving_values):
    new_dict1 = {}
    # print(len(serving_values))
    for (key, value), (serve_ing,serve) in zip(Ing.items(),serving_values.items()):
        # print(serve_ing)
        # print(serve)
        try:
            value = int(value)
            new_dict1[key] = value
        except Exception as e:
            # print(e)
            matches = re.finditer(r"(\d*\.\d+|\d+)\s*(\w+)", value)
            for match in matches:
                if match:
                    value = float(match.group(1))
                    # print(value)
                    unit = match.group(2)
                    # print(unit)
                    count=0
                    for size, value2 in serve.items():
                        if unit == size and value2!= None:
                            new_dict1[key] = value2
                            count+=1   
                            break
                    if count == 1:
                      continue
                    else:
                        new_dict1[key] = value*unit_conversions.get(unit,1)
                        new_dict1[key] = str(new_dict1[key])+" grams "

                else:
                    new_dict1[key] = value             
    return new_dict1

def calc(my_list,data):   
    calories_sum = 0
    fat_sum = 0
    carbohydrates_sum = 0
    protein_sum =0
    sodium_sum = 0
    potassium_sum =0
    for item,val in zip(my_list, data.values()):
        try:
            val = val.split("grams")
            val = float(val[0])
            calories_sum += item["Calories"]*(val/100)
            fat_sum += float(item["Fat_value"])*(val/100)
            carbohydrates_sum += float(item["Carobohydrates"])*(val/100)
            protein_sum += float(item["Protein"])*(val/100)
            if item["Sodium"]==None:
                item["Sodium"]=0
            if item["Potassium"]==None:
                item["Potassium"]=0
                
            sodium_sum+= float(item["Sodium"])*(val/100)
            potassium_sum+= float(item["Potassium"])*(val/100)
        except:
            val = float(val)
            calories_sum += item["Calories"]*(val/100)
            fat_sum += float(item["Fat_value"])*(val/100)
            carbohydrates_sum += float(item["Carobohydrates"])*(val/100)
            protein_sum += float(item["Protein"])*(val/100)
            if item["Sodium"]==None:
                item["Sodium"]=0
            if item["Potassium"]==None:
                item["Potassium"]=0
            sodium_sum+= float(item["Sodium"])*(val/100)
            potassium_sum+= float(item["Potassium"])*(val/100)

    return calories_sum,fat_sum,carbohydrates_sum,protein_sum,sodium_sum/1000,potassium_sum/1000       

def calculate_accuracy(calculated, actual):
    # total = len(actual)
    correct = 0
    if abs(calculated[0] - actual[0]) < 90 and abs(calculated[1] - actual[1]) < 40 and abs(calculated[2] - actual[2]) < 40 and abs(calculated[3] - actual[3]) < 40:
        correct += 1
            
    accuracy =  correct
    return accuracy*100

     
if __name__ == "__main__":
    df = pd.read_csv("D:\Learning\Ml Intern(analysed)\Calorie Calculator\Harighotra.co.uk_RECIPE_DATA.csv",encoding= 'unicode_escape')
    # print(df["Ingredients"])
    result_acc = []
    for (items),(result_nutrition) in zip(df["Ingredients"],df["Nutritional Information"]):
        result = ast.literal_eval(result_nutrition)
        re_item = ''.join(items)
    # for re_item in recipes_list:
    #     # re_item = recipes_list[]      
        re_item = re_item.lower()
        input = recipe_cleaning(re_item)
        print(input)
        Ingredients, Nutrition_values = extract_ingredients(input)
        # print(Nutrition_values)
        # print(len(Nutrition_values))
        # print(Ingredients)
        # print(len(Ingredients))
        serving_values = servings(Ingredients)
        data = convert(Ingredients,serving_values)
        print((data))
        ans1 = calc(Nutrition_values, data)
        # print(type(ans1))
        print()
        print("################################################################################################################################")
        print("Nutritional Information of the Recipe: ")
        cal = round(ans1[0],2)
        fat_val = round(ans1[1],2)
        carbs = round(ans1[2],2)
        protein = round(ans1[3],2)
        sodium = round(ans1[4],5)
        potassium = round(ans1[5],5)
        # print(f"Calories : {cal} cal")
    #     print(f"Fat_value : {fat_val} g")
    #     print(f"Carbohydrates : {carbs} g")
    #     print(f"Protein : {protein} g")
    #     print(f"Sodium : {sodium} g")
    #     print(f"Potassium : {potassium} g")
    #     print()
        calculated_accuracy = []
        actual_result = []
        calculated_accuracy.append(float(cal))
        calculated_accuracy.append(float(fat_val))
        calculated_accuracy.append(float(carbs))
        calculated_accuracy.append(float(protein))
        actual_result.append(float(result["Calories"]))
        actual_result.append(float(result["Fat"]))
        actual_result.append(float(result["Carbohydrates"]))
        actual_result.append(float(result["Protein"]))
        print(actual_result)
        print(calculated_accuracy)
        result_acc.append(float(calculate_accuracy(calculated_accuracy,actual_result)))
    
        # print(f"Fat_value : {fat_val} g")
        # print(f"Carbohydrates : {carbs} g")
        # print(f"Protein : {protein} g")
        # print(f"Sodium : {sodium} g")
        # print(f"Potassium : {potassium} g")
        print()
        
    print(sum(result_acc)/len(result_acc))   