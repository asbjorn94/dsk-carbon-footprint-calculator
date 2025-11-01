from .databases import dsk_table, synonym_table, conversion_table, get_dsk_item_by_id
from .objects import DSKItem, IngredientItem
from .errors import UnitNotRecognizedError, IngredientNotFoundError,QuantityNotStatedError
import re
from typing import List
from thefuzz import fuzz

class Utils:
    
    @staticmethod
    def parse_recipe_items(recipe_list: List[dict]) -> dict[str,list]:
        response = {
            "recipeitemFootprintCalculated" : [],
            "unitsNotRecognized" : [],
            "quantityNotStated" : [],
            "foodProductsNotFound" : []
        }
        
        for i, item in enumerate(recipe_list):
            try:
                ingredient_item = parse_recipe_item(item.get("liElement"))
                best_match = get_best_database_match(ingredient_item.name)
                amount_in_kg = compute_kilograms_from_unit(best_match.id, ingredient_item.quantity, ingredient_item.unit)
                recipeitem_footprint = amount_in_kg * best_match.footprint
                recipeitem_footprint = round(recipeitem_footprint,3)
            
            except IngredientNotFoundError as e:     
                print(e.error_msg)
                response['foodProductsNotFound'].append({
                    "ingredient": e.ingredient, 
                    "errorMessage": f'Ingrediensen, "{e.ingredient}", kunne ikke findes i databasen.'    
                })
            except UnitNotRecognizedError as e:
                print(e)  
                response['unitsNotRecognized'].append({
                    "foodProduct": best_match.product, #TODO: Seems redundant
                    "errorMessage": f'Måleenheden, "{ingredient_item.unit}", kunne ikke genkendes.',
                    "foodProductFootprint": best_match.footprint
                })
            except QuantityNotStatedError as e:
                print(e)
                response['quantityNotStated'].append({
                    "foodProduct": best_match.product, #TODO: Seems redundant - maybe merge into function that is called both when QuantityNotStatedError and UnitNotRecognizedError is raised
                    "errorMessage": f'Ingen mængdeangivelse kunne detekteres for den givne ingrediens',
                    "foodProductFootprint": best_match.footprint
                })
            else:
                response['recipeitemFootprintCalculated'].append({
                    "foodProduct": best_match.product, 
                    "recipeitemFootprint": recipeitem_footprint   
                })
                # print(f"""
                #         For ingredient (incl amount): {result}, \n
                #         the lookup in the database was found to be {best_match[1]}, \n 
                #         and the total footprint was found to be: {total_footprint_for_ingredient}
                #       """)
        return response     


def parse_recipe_item(text: str) -> IngredientItem:
    amount_pattern = "([\d]+[.,]?[\d]*\s\w+)"
    ingredient_pattern = "(.*)"
    pattern = r"^" + amount_pattern + "?\s?" + ingredient_pattern + "$"
    match = re.match(pattern, text)
    ingredient_name = match.group(2)
    amount = match.group(1)

    if amount == None:
        raise QuantityNotStatedError("The quantity for the ingredient has not been stated. Alternatively, the software might not have been able to recognize the quanity stated, if any.")

    (quantity, unit) = split_into_quantity_and_unit(amount)

    ingredient_item = IngredientItem(
        name=ingredient_name,
        unit=unit,
        quantity=quantity
    )

    return ingredient_item


def split_ingredient_string(ingredient : str):
    ingredient = ingredient.replace(",", "").lower()
    return ingredient.split(" ")
      

def get_best_database_match(ingredient: str) -> DSKItem:
    ratios = []  
    ratio_threshold = 60

    for i, row in synonym_table.iterrows():
        id = row['product_id']
        synonym = row['product_name']

        ratio = fuzz.token_set_ratio(ingredient, synonym)

        split_synonym = split_ingredient_string(synonym)
        if len(split_synonym) > 1: #If more than one word
            if split_synonym[0] == ingredient:
                ratio += 100 # If the ingredient is a perfect match on the first word of the synonym, reward it with 100 points
        elif len(split_synonym) == 1 and split_synonym[0] == ingredient:
            #Ingredient string only contains one word and it exactly matches a string in the database when both lowercased
            return get_dsk_item_by_id(id)   

        ratios.append((id,ratio))

    ratios.sort(key = lambda x: x[1])

    print(f"Top 10 ratios: {ratios[-10:]}")

    (best_ratio_id,best_ratio) = ratios[-1]

    if best_ratio < ratio_threshold:
        error_msg = f"The ingredient could not be found. Ratio from fuzzy string matching was below the ratio threshold ({ratio_threshold}"
        raise IngredientNotFoundError(error_msg, ingredient)

    return get_dsk_item_by_id(best_ratio_id)    


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
    return conversion_table.loc[conversion_table['product_id'].eq(ingredient_id) & conversion_table['unit'].eq(unit)]['kg_conversion_factor'].item()


def split_into_quantity_and_unit(amount : str) -> tuple[float,str]:
    pattern = r"^(\d*\.?\d*) (.*)$"
    match = re.match(pattern, amount)
    quantity = float(match.group(1))
    unit = match.group(2)
    return (quantity,unit)