from databases import dsk_table, synonym_table, conversion_table

from errors import UnitNotRecognizedError, IngredientNotFoundError,QuantityNotStatedError
import re
from typing import List
from thefuzz import fuzz

ratio_threshold = 60

class Utils:
    
    @staticmethod
    def parse_recipe_items(recipe_list: List[dict]) -> list:
        response = {
            "recipeitemFootprintCalculated" : [],
            "unitsNotRecognized" : [],
            "quantityNotStated" : [],
            "foodProductsNotFound" : []
        }
        
        for i, item in enumerate(recipe_list):
            
            try:
                # (amount, ingredient) = parse_recipe_item(item.get("liElement"))
                (amount, ingredient_id, ingredient, food_product, food_product_footprint) = parse_recipe_item(item.get("liElement"))
                if amount == None:
                    raise QuantityNotStatedError("The quantity for the ingredient has not been stated. Alternatively, the software might not have been able to recognize the quanity stated, if any.")
                
                # (ingredient_id, ingredient_name, ingredient_footprint) = get_best_database_match(ingredient)
                # food_item_name_best_match = best_match[1]
                # food_item_footprint = best_match[2]
                (quantity, unit) = split_into_quantity_and_unit(amount)
                amount_in_kg = compute_kilograms_from_unit(ingredient_id, quantity, unit)
                recipeitem_footprint = calculate_footprint_with_amount(amount_in_kg, food_product_footprint)
                recipeitem_footprint = round_total_footprint(recipeitem_footprint)
            
            except IngredientNotFoundError as e:     
                print(e.error_msg)
                response['foodProductsNotFound'].append({
                    "ingredient": e.ingredient, 
                    "errorMessage": f'Ingrediensen, "{e.ingredient}", kunne ikke findes i databasen.'    
                })
            except UnitNotRecognizedError as e:
                print(e)  
                response['unitsNotRecognized'].append({
                    "foodProduct": food_product, #TODO: Seems redundant
                    "errorMessage": f'Måleenheden, "{unit}", kunne ikke genkendes.',
                    "foodProductFootprint": food_product_footprint
                })
            except QuantityNotStatedError as e:
                print(e)
                response['quantityNotStated'].append({
                    "foodProduct": food_product, #TODO: Seems redundant - maybe merge into function that is called both when QuantityNotStatedError and UnitNotRecognizedError is raised
                    "errorMessage": f'Ingen mængdeangivelse kunne detekteres for den givne ingrediens',
                    "foodProductFootprint": food_product_footprint
                })
            else:
                response['recipeitemFootprintCalculated'].append({
                    "foodProduct": food_product, 
                    "recipeitemFootprint": recipeitem_footprint   
                })
                # print(f"""
                #         For ingredient (incl amount): {result}, \n
                #         the lookup in the database was found to be {best_match[1]}, \n 
                #         and the total footprint was found to be: {total_footprint_for_ingredient}
                #       """)
        return response      


def parse_recipe_item(text: str) -> tuple[int,str,str,str]:

    amount_pattern = "([\d]+[.,]?[\d]*\s\w+)"
    ingredient_pattern = "(.*)"
    pattern = r"^" + amount_pattern + "?\s?" + ingredient_pattern + "$"
    # pattern = r"^([\d]+[.,]?[\d]*\s\w+)?\s(.*)$"
    match = re.match(pattern, text)

    ingredient = match.group(2)
    (ingredient_id, ingredient_name, ingredient_footprint) = get_best_database_match(ingredient)
    amount = match.group(1)

    # (quantity, unit) = split_into_quantity_and_unit(amount)
    return (amount, ingredient_id, ingredient, ingredient_name, ingredient_footprint)
    # return (amount,ingredient)

      
def get_best_database_match(ingredient: str):

    ratios = []  
    # for i, synonym in enumerate(synonym_table['synonym']):
    for i, row in synonym_table.iterrows():
        # id = int(synonym_table['ID'][i])
        # id = synonym_table.iloc[i, synonym_table.columns.get_loc('ID')]
        id = row['product_id']
        synonym = row['product_name']
        # print(f"id: {id},\n synonym: {synonym}")

        ratio = fuzz.partial_ratio(ingredient, synonym)

        ratios.append((id,ratio))
        # print(f"(id,ratio): {(id,ratio)}")

    ratios.sort(key = lambda x: x[1])
    # print(f'Highest ratio: {ratios[-1]}')
    (best_ratio_id,best_ratio) = ratios[-1]
    # print(f"best_ratio_id: {best_ratio_id}")

    if ingredient_is_not_found(best_ratio):
        error_msg = f"The ingredient could not be found. Ratio from fuzzy string matching was below the ratio threshold ({ratio_threshold}"
        raise IngredientNotFoundError(error_msg, ingredient)

    # best_ratio_item = dsk_table.loc[dsk_table['ID'] == best_ratio_id]

    return_tuple = dsk_table.loc[dsk_table['id'] == best_ratio_id].values[0]

    print(f"Ratio: {best_ratio}, tuple: {tuple(return_tuple)}")

    (return_id,return_product,return_footprint) = tuple(return_tuple)

    # print(f"\nBest match: {return_product}, for given ingredient: {ingredient}\n")

    # for i, fooditem in enumerate(panda_db['product']):
    #     ratio = fuzz.partial_ratio(ingredient, fooditem) #TODO: Find out which fuzz method is best suited...
    #     footprint = float(panda_db['kg_co2e_pr_kg'][i])
    #     data_tuple = (ratio,fooditem,footprint) #TODO make other data structure, e.g. class
    #     ratios.append(data_tuple)
    # ratios.sort(key = lambda x: x[0])

    return (return_id,return_product, return_footprint)
    
#Should contain logic that determines if ingredient is found or not
def ingredient_is_not_found(best_ratio : int) -> bool:

    return best_ratio < ratio_threshold



def compute_kilograms_from_unit(ingredient_id : int, quantity : float, unit : str) -> float:
    if unit == "kg":
        return quantity
    elif unit == "g":
        return quantity * 0.001
    else: #Unit needs to be translated into kg
        try:
            return (quantity * get_conversion_factor(ingredient_id, unit))
        except Exception as e:
            print(e)
            raise UnitNotRecognizedError("The unit used for the ingredient is not recognized") 


def get_conversion_factor(ingredient_id : int, unit : str) -> float:

    return conversion_table.loc[conversion_table['ID'].eq(ingredient_id) & conversion_table['unit'].eq(unit)]['kg_conversion_factor'].item()


def split_into_quantity_and_unit(amount : str) -> tuple[float,str]:
    pattern = r"^(\d*\.?\d*) (.*)$"
    match = re.match(pattern, amount)
    quantity = float(match.group(1))
    unit = match.group(2)

    return (quantity,unit)



def calculate_footprint_with_amount(amount : float, footprint : float):

    return amount * footprint #Only handles amount = kg as of now


def round_total_footprint(number: float) -> float:
    
    return round(number,3)

    #     # item_alternatives = item.split(" eller ")
    #     item_alternatives = re.split(" eller ", item, flags=re.IGNORECASE)



    # def getBestMatch(text):
       
    #     highestRatios = StringHandler.getHighestRatios(text)

    #     #Look among highest ranked items
    #     words = text.split(" ")

    #     ranked_words: List[tuple[str,int]] = []
    #     for word in words: # sødmælk
    #         for ratio in highestRatios:
    #             dbEntry = ratio[0]
    #             word_rank = StringHandler.word_order_ranking(word, dbEntry) #0 ved sødmælk
    #             if word_rank != None:
    #                 ranked_words.append((dbEntry, word_rank))
    #     # Sort
    #     ranked_words.sort(key = lambda x: x[0])
    #     #Return the match with the lowest rank (i.e., where the overlapping word is closest to the beginning of the sentence)
    #     return ranked_words[0][0]
    
    # def word_order_ranking(input: str, dbEntry: str):
    #     input_low = input.lower()
    #     dbEntry_low = dbEntry.lower()
    #     if input_low in dbEntry_low:
    #         dbEntry_words = dbEntry_low.split(" ")
    #         for i, word in enumerate(dbEntry_words):
    #             for char in word:
    #                 if char in ",.":
    #                     word = word.replace(char,"")
                    
    #             # input_low == input_low.replace(",", "")
    #             if input_low == word:
    #                 return i
    #     else:
    #         return None