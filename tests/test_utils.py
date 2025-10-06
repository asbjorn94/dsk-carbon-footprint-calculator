import pytest
from source import utils

# @pytest.mark.parametrize("input, output", 
#                             [("<li>1 tsk sukker</li>",[('1 tsk', 'sukker')]),
#                             (" <li>0,5 tsk chiliflager (valgfrit)</li>",[('0,5 tsk', 'chiliflager (valgfrit)')])])
# def test__parse_recipe_item(input, output):
#     assert StringHandler.parse_recipe_item(input) == output
#     # result = StringHandler.parse_recipe_item("<li>1 tsk sukker</li>")
#     # self.assertEqual(result, [('1 tsk', 'sukker')])
    
#     # result = StringHandler.parse_recipe_item(" <li>0,5 tsk chiliflager (valgfrit)</li>")
#     # self.assertEqual(result, [('0,5 tsk', 'chiliflager (valgfrit)')])

# #Tests if string-splits on "eller" is conducted correctly
# def test__parse_recipe_item_splitting():
#     result = StringHandler.parse_recipe_item("<li>0,5 dl fløde eller 1 dl sødmælk (valgfrit)</li>")
#     assert result == [('0,5 dl', 'fløde'),('1 dl', 'sødmælk (valgfrit)')]    

#     # result = StringHandler.parse_recipe_item("<li>0,5 dl fløde Eller 1 dl sødmælk (valgfrit)</li>")
#     # self.assertEqual(result, [('0,5 dl', 'fløde'),('1 dl', 'sødmælk (valgfrit)')])  

