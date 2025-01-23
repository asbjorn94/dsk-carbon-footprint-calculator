from panda_database import panda_db

import re
from typing import List
from thefuzz import fuzz

class Utils:
    
    @staticmethod
    def parse_recipe_items(recipe_list: List[dict]):
        # result = []
        for i, item in enumerate(recipe_list):
            result = Utils.parse_recipe_item(item.get("liElement"))
            # print(f"result[0]: {result[0]}")
            # print(f"result[1]: {result[1]}")
            amount = result[0]
            ingredient = result[1]
            Utils.get_best_database_match(ingredient)
    
    def parse_recipe_item(text: str) -> tuple[str,str]:
        print(f"Text in parse_recipe_item: {text}")

        pattern = r"^([\d]+[.,]?[\d]*\s\w+)?\s(.*)$"
        match = re.match(pattern, text)

        # print(f"match.group(1): {match.group(1)}")
        # print(f"match.group(2): {match.group(2)}")
    #         result.append((match.group(1),match.group(2)))
        return (match.group(1),match.group(2))
    

            
    def get_best_database_match(ingredient: str):
        print(f"ingredient inside get_best_database_match: {ingredient}")

    #     database = ClimateDatabase.getDatabase() #TODO: Not a good idea to get the database everytime?
    #     ratios = [] # Tuple?
    #     for i, foodItem in enumerate(database["Produkt"]):
    #         ratio = fuzz.partial_ratio(text,foodItem)
    #         ratios.append((foodItem, ratio))

        # best_match : tuple[float,str,float] = () 
        ratios = []
        print(f'ingredient: {ingredient}')       
        for i, fooditem in enumerate(panda_db['product']):
            ratio = fuzz.partial_ratio(ingredient, fooditem) #TODO: Find out which fuzz method is best suited...
            footprint = float(panda_db['footprint'][i])
            data_tuple = (ratio,fooditem,footprint)
            print(f"data_tuple: {data_tuple}")
            ratios.append(data_tuple)

        ratios.sort(key = lambda x: x[0])

        print(f'ratios[-1]: {ratios[-1]}')

    #     return ratios[-5:]


        



# from thefuzz import fuzz
# from typing import Tuple, List
# import re
# from source.climate_database import ClimateDatabase

    # def parse_recipe_item(text: str) -> List[Tuple[str,str]]:
    #     # Extract items from <li> tags
    #     items = re.findall(r"<li>(.*?)</li>", text)
    #     item = items[0]
    #     item = item.strip()

    #     # item_alternatives = item.split(" eller ")
    #     item_alternatives = re.split(" eller ", item, flags=re.IGNORECASE)

    #     result: List[Tuple[str,str]] = []
    #     # result.append(List[List["hey","hey"]])

    #     for i, x in enumerate(item_alternatives):
    #         # Capture 2 groups (),()
    #         # Group 1: Recognition of quantity + unit
    #         # Group 2: Rest of string "(.*)$"

   

    #     return result

    # def getHighestRatios(text) -> List[tuple[str,str]]:




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