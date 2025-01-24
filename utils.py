from databases import dsk_table, synonym_table

import re
from typing import List
from thefuzz import fuzz

class Utils:
    
    @staticmethod
    def parse_recipe_items(recipe_list: List[dict]) -> list:
        ingredient_footprints = []
        
        for i, item in enumerate(recipe_list):
            result = parse_recipe_item(item.get("liElement"))
            amount = result[0]
            ingredient = result[1]

            best_match = get_best_database_match(ingredient)
            food_item_name_best_match = best_match[1]
            food_item_footprint = best_match[2]
            (quantity, unit) = split_into_quantity_and_unit(amount)
            footprint_in_kilograms = compute_kilograms_from_unit(quantity, unit)
            total_footprint_for_ingredient = round_total_footprint(calculate_footprint_with_amount(footprint_in_kilograms, food_item_footprint))

            # print(f"""
            #         For ingredient (incl amount): {result}, \n
            #         the lookup in the database was found to be {best_match[1]}, \n 
            #         and the total footprint was found to be: {total_footprint_for_ingredient}
            #       """)

            ingredient_details = {
                "foodItemName": food_item_name_best_match,
                "totalFootprintForIngredient": total_footprint_for_ingredient   
            }

            ingredient_footprints.append(ingredient_details)

        return ingredient_footprints      


def parse_recipe_item(text: str) -> tuple[str,str]:

    pattern = r"^([\d]+[.,]?[\d]*\s\w+)?\s(.*)$"
    match = re.match(pattern, text)

    return (match.group(1),match.group(2))

      
def get_best_database_match(ingredient: str):

    ratios = []  
    # for i, synonym in enumerate(synonym_table['synonym']):
    for i, row in synonym_table.iterrows():
        # id = int(synonym_table['ID'][i])
        # id = synonym_table.iloc[i, synonym_table.columns.get_loc('ID')]
        id = row['ID']
        synonym = row['synonym']
        print(f"id: {id},\n synonym: {synonym}")

        ratio = fuzz.partial_ratio(ingredient, synonym)
        ratios.append((id,ratio))
        # print(f"(id,ratio): {(id,ratio)}")

    ratios.sort(key = lambda x: x[1])
    print(f'Highest ratio: {ratios[-1]}')
    (best_ratio_id,x) = ratios[-1]
    print(f"best_ratio_id: {best_ratio_id}")

    # best_ratio_item = dsk_table.loc[dsk_table['ID'] == best_ratio_id]

    (return_id,return_product,return_footprint) = tuple(dsk_table.values[best_ratio_id])

    # print(f"""
    #     a: \n{str(a)}\n
    #     b: \n{str((b))}\n
    #     c: \n{str((c))}\n

    # """)



    # for i, fooditem in enumerate(panda_db['product']):
    #     ratio = fuzz.partial_ratio(ingredient, fooditem) #TODO: Find out which fuzz method is best suited...
    #     footprint = float(panda_db['kg_co2e_pr_kg'][i])
    #     data_tuple = (ratio,fooditem,footprint) #TODO make other data structure, e.g. class
    #     ratios.append(data_tuple)
    # ratios.sort(key = lambda x: x[0])


    # print(f"(best_ratio_id,best_ratio_item['product'],best_ratio_item['kg_co2e_pr_kg']): {(best_ratio_id,best_ratio_item['product'],best_ratio_item['kg_co2e_pr_kg'])}")
    # return ratios[-1]
    print(f"(return_id,return_product, return_footprint):\n {(return_id,return_product, return_footprint)}")

    return (return_id,return_product, return_footprint)
    

def compute_kilograms_from_unit(quantity: float, unit : str):
    if unit == "kg":
        return quantity
    elif unit == "g":
        return quantity * 0.001
    else:
        raise ValueError("The unit used for the ingredient is not recogonized")
            
    

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