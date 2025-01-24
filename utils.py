from databases import dsk_table, synonym_table, conversion_table

import re
from typing import List
from thefuzz import fuzz

class Utils:
    
    @staticmethod
    def parse_recipe_items(recipe_list: List[dict]) -> list:
        ingredient_footprints = []
        
        for i, item in enumerate(recipe_list):
            (amount,ingredient) = parse_recipe_item(item.get("liElement"))

            (ingredient_id, ingredient_name, ingredient_footprint) = get_best_database_match(ingredient)
            # food_item_name_best_match = best_match[1]
            # food_item_footprint = best_match[2]
            (quantity, unit) = split_into_quantity_and_unit(amount)
            amount_in_kg = compute_kilograms_from_unit(ingredient_id, quantity, unit)
            total_footprint_for_ingredient = calculate_footprint_with_amount(amount_in_kg, ingredient_footprint)
            total_footprint_for_ingredient = round_total_footprint(total_footprint_for_ingredient)

            # print(f"""
            #         For ingredient (incl amount): {result}, \n
            #         the lookup in the database was found to be {best_match[1]}, \n 
            #         and the total footprint was found to be: {total_footprint_for_ingredient}
            #       """)

            ingredient_details = {
                "foodItemName": ingredient_name,
                "totalFootprintForIngredient": total_footprint_for_ingredient   
            }

            ingredient_footprints.append(ingredient_details)

        return ingredient_footprints      


def parse_recipe_item(text: str) -> tuple[str,str]:

    amount_pattern = "([\d]+[.,]?[\d]*\s\w+)"
    ingredient_pattern = "(.*)"
    pattern = r"^" + amount_pattern + "?\s" + ingredient_pattern + "$"
    # pattern = r"^([\d]+[.,]?[\d]*\s\w+)?\s(.*)$"
    match = re.match(pattern, text)

    amount = match.group(1)
    ingredient = match.group(2)

    # (quantity, unit) = split_into_quantity_and_unit(amount)

    return (amount,ingredient)

      
def get_best_database_match(ingredient: str):

    ratios = []  
    # for i, synonym in enumerate(synonym_table['synonym']):
    for i, row in synonym_table.iterrows():
        # id = int(synonym_table['ID'][i])
        # id = synonym_table.iloc[i, synonym_table.columns.get_loc('ID')]
        id = row['ID']
        synonym = row['synonym']
        # print(f"id: {id},\n synonym: {synonym}")

        ratio = fuzz.partial_ratio(ingredient, synonym)
        ratios.append((id,ratio))
        # print(f"(id,ratio): {(id,ratio)}")

    ratios.sort(key = lambda x: x[1])
    # print(f'Highest ratio: {ratios[-1]}')
    (best_ratio_id,x) = ratios[-1]
    # print(f"best_ratio_id: {best_ratio_id}")

    # best_ratio_item = dsk_table.loc[dsk_table['ID'] == best_ratio_id]

    print(f"tuple: {tuple(dsk_table.values[best_ratio_id])}")

    (return_id,return_product,return_footprint) = tuple(dsk_table.values[best_ratio_id])

    # print(f"\nBest match: {return_product}, for given ingredient: {ingredient}\n")

    # for i, fooditem in enumerate(panda_db['product']):
    #     ratio = fuzz.partial_ratio(ingredient, fooditem) #TODO: Find out which fuzz method is best suited...
    #     footprint = float(panda_db['kg_co2e_pr_kg'][i])
    #     data_tuple = (ratio,fooditem,footprint) #TODO make other data structure, e.g. class
    #     ratios.append(data_tuple)
    # ratios.sort(key = lambda x: x[0])

    return (return_id,return_product, return_footprint)
    

def compute_kilograms_from_unit(ingredient_id : int, quantity : float, unit : str) -> float:
    if unit == "kg":
        return quantity
    elif unit == "g":
        return quantity * 0.001
    else: #Unit needs to be translated into kg
        try:
            return (quantity * get_conversion_factor(ingredient_id, unit))
        except:
            raise ValueError("The unit used for the ingredient is not recognized") 


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