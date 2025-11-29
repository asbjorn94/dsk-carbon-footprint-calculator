from .databases import synonym_table, conversion_table, get_dsk_item_by_id
from .objects import DSKItem, IngredientItem
from .errors import UnitNotRecognizedError, IngredientNotFoundError,QuantityNotStatedError
import re
from typing import List
from thefuzz import fuzz
from .ingredient_parser import fetch_from_api
from .product_mapper import get_best_match

class Utils:
    
    @staticmethod
    def parse_recipe_items(recipe_list: List[dict],method='fuzzy') -> dict[str,list]:
        response = {
            "recipeitemFootprintCalculated" : [],
            "unitsNotRecognized" : [],
            "quantityNotStated" : [],
            "foodProductsNotFound" : []
        }

        if method == 'fuzzy':
            return parse_recipe_items_fuzzy(response, recipe_list)
        elif method == 'semantic':
            return parse_recipe_items_semantic(response, recipe_list)


def generate_response_item(response, #TODO The generation of JSON response needs to be simplified...
                           type, 
                           ingredient=None, 
                           food_product=None, 
                           error_mesage=None, 
                           food_product_footprint=None, 
                           recipe_item_footprint=None):
    response[type].append({
        "ingredient": ingredient,
        "foodProduct": food_product,
        "errorMessage": error_mesage,
        "foodProductFootprint": food_product_footprint,
        "recipeitemFootprint": recipe_item_footprint
    })


def parse_recipe_items_semantic(response, recipe_list: List[dict]) -> dict[str,list]:
    recipe_list = [item.get("liElement") for i, item in enumerate(recipe_list)]
    parsed_recipe_list = fetch_from_api(recipe_list)
    for ingredient in parsed_recipe_list:
        best_match : DSKItem = get_best_match(ingredient['name'])
        if ingredient['quantity'] is None:
            generate_response_item(
                response=response, 
                type='quantityNotStated',
                food_product=best_match.product,
                error_mesage=f'Ingen mængdeangivelse kunne detekteres for den givne ingrediens',
                food_product_footprint=best_match.footprint
            )
        elif best_match is None:
            generate_response_item(
                response=response, 
                type='foodProductsNotFound',
                ingredient=ingredient['name'],
                error_mesage=f'Ingrediensen, "{ingredient["name"]}", kunne ikke findes i databasen.'
            )
        else:
            try:
                recipe_item_footprint = best_match.footprint * compute_kilograms_from_unit(best_match.id,ingredient['quantity'],ingredient['unit'])
                generate_response_item(
                    response=response, 
                    type='recipeitemFootprintCalculated',
                    food_product=best_match.product,
                    recipe_item_footprint=recipe_item_footprint
                )
            except UnitNotRecognizedError as e:
                print(e) 
                generate_response_item(
                    response=response, 
                    type='unitsNotRecognized',
                    food_product=best_match.product,
                    error_mesage=f'Måleenheden kunne ikke genkendes.',
                    food_product_footprint=best_match.footprint
                )
    return response
        

def parse_recipe_items_fuzzy(response, recipe_list: List[dict]) -> dict[str,list]:        

    for i, item in enumerate(recipe_list):
        try:
            ingredient_item = parse_recipe_item(item.get("liElement"))
            best_match = get_best_database_match(ingredient_item.name)
            if ingredient_item.quantity is None and ingredient_item.unit is None:
                raise QuantityNotStatedError("The quantity for the ingredient has not been stated. Alternatively, the software might not have been able to recognize the quanity stated, if any.")
            amount_in_kg = compute_kilograms_from_unit(best_match.id, ingredient_item.quantity, ingredient_item.unit)
            recipeitem_footprint = amount_in_kg * best_match.footprint
            recipeitem_footprint = round(recipeitem_footprint,3)
        
        except IngredientNotFoundError as e:     
            print(e.error_msg)
            generate_response_item(
                response=response, 
                type='foodProductsNotFound',
                ingredient=e.ingredient,
                error_mesage=f'Ingrediensen, "{e.ingredient}", kunne ikke findes i databasen.'
            )
        except UnitNotRecognizedError as e:
            print(e)  
            generate_response_item(
                response=response, 
                type='unitsNotRecognized',
                food_product=best_match.product,
                error_mesage=f'Måleenheden, "{ingredient_item.unit}", kunne ikke genkendes.',
                food_product_footprint=best_match.footprint
            )
        except QuantityNotStatedError as e:
            print(e)
            generate_response_item(
                response=response, 
                type='quantityNotStated',
                food_product=best_match.product,
                error_mesage=f'Ingen mængdeangivelse kunne detekteres for den givne ingrediens',
                food_product_footprint=best_match.footprint
            )
        else:
            generate_response_item(
                response=response, 
                type='recipeitemFootprintCalculated',
                food_product=best_match.product,
                recipe_item_footprint=recipeitem_footprint
            )
    return response     


def parse_recipe_item(text: str) -> IngredientItem:
    amount_pattern = "([\d]+[.,]?[\d]*\s\w+)"
    ingredient_pattern = "(.*)"
    pattern = r"^" + amount_pattern + "?\s?" + ingredient_pattern + "$"
    match = re.match(pattern, text)
    ingredient_name = match.group(2)
    amount = match.group(1)

    if amount is not None:
        (quantity, unit) = split_into_quantity_and_unit(amount)
    else:
        quantity = unit = None

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
            raise UnitNotRecognizedError(f"The unit, \"{unit}\" , used for the ingredient is not recognized") 


def get_conversion_factor(ingredient_id : int, unit : str) -> float:
    return conversion_table.loc[conversion_table['product_id'].eq(ingredient_id) & conversion_table['unit'].eq(unit)]['kg_conversion_factor'].item()


def split_into_quantity_and_unit(amount : str) -> tuple[float,str]:
    pattern = r"^(\d*\.?\d*) (.*)$"
    match = re.match(pattern, amount)
    quantity = float(match.group(1))
    unit = match.group(2)
    return (quantity,unit)