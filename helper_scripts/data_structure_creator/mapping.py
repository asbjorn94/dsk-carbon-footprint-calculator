import json
import os
import pandas as pd
from thefuzz import fuzz
from itertools import islice

#TODO: You must be able to do the below in a prettier way
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))
from source.dsk_item import DSKItem, DSKBaseword

base_dir = os.path.dirname(__file__)

def rank_description(residue_words: list[str], description: str):
    desc_words = description.replace(",","").lower().split(" ")  
    desc_word_threshold = 80
    desc_rank = 0
    for desc_word in desc_words:
        for residue_word in residue_words:
            if fuzz.partial_ratio(desc_word, residue_word) > desc_word_threshold:
                desc_rank += 1
    
    return desc_rank

def get_best_description(residue_words, descriptions) -> DSKItem:
    best_matching_description = {
        'rank': 0,
        'dsk_item': None
    }

    for description in descriptions:
        if description['description'] is not None:
            desc_ratio = rank_description(residue_words, description['description'])
            if desc_ratio > best_matching_description['rank']:
                best_matching_description['rank'] = desc_ratio
                best_matching_description['dsk_item'] = DSKItem(
                    id=description['id'],
                    footprint=description['kg_co2e_pr_kg']
                )

    return best_matching_description['dsk_item']


def get_best_match(ingredient : str) -> list[DSKBaseword]:
    with open(base_dir + "/base_datastructure.json") as json_file:
        basewords : dict = json.load(json_file) # The "database"
        basewords = dict(islice(basewords.items(),4)) #For testing
        # print(basewords)
        
        ing_words = ingredient.replace(",","").lower().split(" ") #Tokenize
        ratio_threshold = 90
        for ing_word in ing_words:
            print(f"ing_word: {ing_word}")
            for baseword, descriptions in basewords.items():
                baseword = baseword.lower()
                print(f"baseword: {baseword}")
                #1. Is the word very similar to the baseword?
                if fuzz.partial_ratio(baseword, ing_word) > ratio_threshold:
                    residue_words = [word for word in ing_words if word != ing_word]
                    dsk_item = get_best_description(residue_words, descriptions)
                    
                    # print(f"desc_words: {residue_words}")
                    print(f"dsk_items: {dsk_item}")

def main():
    get_best_match("Agurk, syltet")    

if __name__ == "__main__":
    main()
        



    
