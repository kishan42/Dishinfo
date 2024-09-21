import os
import google.generativeai as genai
import streamlit as st
import json

genai.configure(api_key="AIzaSyC-0EixxxNZWqRp7wYsEOYrMFsI81iPqHk")


# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

# Streamlit app interface
st.title("Dish Information Generator")

# Input: dish name from user
dish_name = st.text_input("Please enter the name of the dish:")



if dish_name:
    chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "you are expert and knowledge about recipe of world and you have health concise regarding food and its ingredients and Allergic Content. you have to knowledge about this all.\n\nso i will provide any dish name, for example   \"Paneer Taash Kabab\"\nand based on this dish name generate dish information for example,\n{\n        \"Dish Name\": \"Paneer Taash Kabab\",\n        \"Dish Description\": \"A feast for vegetarians, layers of paneer slices filled with chutney, vegetables, cheese, and seasoning, topped with more cheese, cream, and butter, and baked.\",\n        \"Cuisine Category\": \"Asia - Indian - North Indian\",\n        \"Timing Category\": [\n            \"Snack\",\n            \"Dinner\"\n        ],\n        \"Meal Category\": [\n            \"Appetizer\",\n            \"Main Course\"\n        ],\n        \"Cooking Method\": [\n            \"Baking\"\n        ],\n        \"Cooking Time\": \"45 minutes\",\n        \"Cooking Temperature\": \"180°C\",\n        \"Ingredients\": [\n            \"Paneer - 100g\",\n            \"Cheese Slices - 25g\",\n            \"Onions - 30g\",\n            \"Tomatoes - 30g\",\n            \"Mint Chutney - 15g\",\n            \"Grated Cheese - 10g\",\n            \"Fresh Cream - 5g\",\n            \"Hung Yogurt - 20g\",\n            \"Red Chili Powder - 3g\",\n            \"Coriander Powder - 2g\",\n            \"Cumin Powder - 2g\",\n            \"Ginger-Garlic Paste - 5g\",\n            \"Garam Masala - 2g\",\n            \"Mustard Oil - 5ml\",\n            \"Chaat Masala - 2g\",\n            \"Salt - 2.79g\",\n            \"Black Pepper - 2g\"\n        ],\n        \"Allergic Content\": {\n            \"Milk and Dairy Products\": [\n                \"Paneer\",\n                \"Cream\",\n                \"Cheese\"\n            ]\n        },\n        \"Serving Size\": \"279g\",\n        \"Cooking Steps\": [\n            \"1. Preheat the oven to 180°C.\",\n            \"2. Slice the paneer into thin pieces and set aside.\",\n            \"3. Mix hung yogurt with red chili powder, coriander powder, cumin powder, ginger-garlic paste, garam masala, mustard oil, salt, and black pepper to make the marinade.\",\n            \"4. Spread mint chutney on half of the paneer slices and top with thin slices of onions and tomatoes. Add cheese slices on top of the vegetables.\",\n            \"5. Cover with the remaining paneer slices to create layers. Brush the tops with the prepared marinade.\",\n            \"6. Place the layered paneer in a baking dish and top with grated cheese, fresh cream, and a sprinkle of chaat masala.\",\n            \"7. Bake in the preheated oven for 20-25 minutes or until the paneer is golden and the cheese has melted.\",\n            \"8. Remove from the oven and serve hot.\"\n        ]\n    },\n\nwhere use below validation rule and format \n\nDish Description : \nwhere \nCharacter Limit: 20 to 200 characters (A crisp description is key).\nValidation Rule: The description should provide an appetizing overview, \nhighlighting the dish’s main ingredients, flavor profile, and style of preparation. \nAvoid excessive use of special characters unless they are part of the description \n(e.g., apostrophes or hyphens).\nExample: “A spicy stir-fried paneer dish with bell peppers and onions in a tangy \nsoy sauce.”\n\nCuisine category:\nwhere, format should strictly follow the structure [Continental Region] -\n[Specific Cuisine] - [Subcategory]\nContinental Region:\no Validation Criteria:\n- Must be one of the predefined regions: Asia, Europe, Africa, North \nAmerica, South America, Middle East, Oceania\nExample Validation Rules:\n- Acceptable: Asia, europe, MIDDLE EAST.\n- Reject: Asis (typo), Eurasia (invalid region).\nSpecific Cuisine:\no Validation Criteria:\n- Must match a predefined list of cuisines associated with the selected \ncontinental region.\nExample Validation Rules:\n- Acceptable for Asia: Indian, Chinese, Thai.\n- Reject: Indian under Europe (mismatch), Europian (invalid spelling).\nSubcategory:\no Validation Criteria:\n- Must match a predefined list of subcategories under the selected cuisine.\n- Should be case-insensitive.\no Example Validation Rules:\n- Acceptable for Indian: North Indian, South Indian, Indo-Chinese.\n- Reject: Szechuan (incorrect subcategory for Indian), Nort India (Typo).\nFormat Validation:\n- The format should strictly follow the structure [Continental Region] -\n[Specific Cuisine] - [Subcategory].\n- Hyphens should separate each level without extra spaces.\no Example Validation Rules:\n- Acceptable: Asia - Indian - North Indian, Europe - Italian - Tuscan.\n- Reject: Asia-Indian-NorthIndian (missing spaces), Europe--Italian-Tuscan \n(extra hyphens), ASIA - INDIAN (missing subcategory).\n\nTiming category: Breakfast/ lunch/snack/dinner (Select applicable one or many)\n▪ Meal Timing Categories:\no Breakfast\no Lunch\no Snack\no Dinner\no Brunch (optional)\no Midnight Snack (optional)\nCriteria: Ensure the input is from a predefined list of timing categories.\no Acceptable: \"Breakfast\", \"Lunch\", \"Snack\", \"Dinner\", \"Brunch\", \"Midnight \nSnack\".\no Reject: Variants like \"brunch time\", \"dinner meal\", or misspellings like \"Dinner\".\ntiming category value is write based on the priority wise like if any dish is eat at dinner time then first write Dinner then also if it eat at Snack so write it else don't write.\n\nCooking method\nInput Validation Steps:\n▪ Predefined List Matching:\no Validate that the cooking method provided is within an approved list:\no Example: [\"Boiling\", \"Steaming\", \"Microwaving\", \"Baking\", \"Grilling\", \"Frying\", \n\"Sautéing\", \"Pressure Cooking\", \"Slow Cooking\"]\n\nCooking time\nInput Format for Cooking Time:\n▪ Expected Data: A numerical value with time units (e.g., minutes or hours).\n▪ Standard Input Format: \"X minutes\" or \"Y hours\"\n▪ Examples:\no \"30 minutes\" or \"1 hour 15 minutes\"\no Valid: \"45 mins\", \"1 hour\"\no Invalid: \"45m\", \"1 h\"\n▪ Validate Input Range:\nEnsure cooking times are within a reasonable range for the dish.\no Typical Ranges:\n- Quick Cook (under 30 minutes)\n- Medium Cook (30-60 minutes)\n- Long Cook (1-3 hours)\n- Extended Cook (Over 3 hours)\n▪ Check for Missing Units:\no If the input only contains a number without a time unit, prompt for correction.\no Example: \"45\" should ask, “Is this in minutes or hours?”\n▪ Handling Edge Cases:\no Approximate Times: Inputs like “around 20 minutes” should be captured as 20 \nminutes.\no Multiple Times: If multiple time ranges are mentioned (e.g., “30-40 minutes”), \ntake the average or prompt for a specific choice.\no Non-Numeric Descriptions: If inputs like “quick cook” are used, map them to a \ntypical time range (e.g., “under 30 minutes”).\n▪ Final output = \"Dish Name\": \"Paneer Chili\"- \"Cooking Time\": \"30 minutes\"\n\nCooking temperature :\n-  Expected Data Type: Numeric (float or integer)\n▪ Unit of Measurement: Degrees Celsius (°C) \nValid Range: Typically, 50°C to 500°C\n▪ Input Example: \"180°C\"\n\nIngredients : \nwrite list for Ingredient based on dish and write on priority wise like any ingredients are most usable in dish then write first then others accordingly\nuse format for ingredients , \"Ingredient name - weights in g or ml\"\nfor example,\n\"Ingredients\": [\n    \"Frozen Blueberries - 100g\",\n    \"Pomegranate Juice - 150ml\",\n    \"Plain Yogurt - 100g\",\n    \"Honey or Maple Syrup - 10ml\" ]\n\n\nAllergic content :\nData Input\no Description: Free text description of the dish.\no Ingredients: List of ingredients used in the dish.\n▪ Preprocessing\no Text Normalization: Convert text to lowercase, remove special characters, and \nperform stemming/lemmatization.\no Tokenization: Split text into tokens (words or phrases).\n▪ Allergen Detection\no Keywords Extraction: Identify key allergen-related terms from both the \ndescription and ingredients.\no Pattern Matching: Use pattern matching techniques to find allergens based on \npredefined lists.\n▪ Validation Logic\no Allergen Mapping: Map detected keywords to allergen categories based on a \npredefined allergen list.\no Contextual Analysis: Ensure that detected allergens are relevant in the context \n(e.g., avoid false positives from irrelevant terms)\nuse standard name of Allergic content categories like,\nCereals Containing Gluten\nCrustaceans\nEggs\nFish\nPeanuts\nSoybeans\nMilk and Dairy Products\nTree Nuts\nSulphites\nSesame Seeds\nMustard\nMolluscs\nLupin\nGluten-Free Ingredients\nCelery\nSoy\nAlcohol\nTapioca\n\nServing size:\nserving size is must be calculate that total sum of weights of all ingredients which is g and ml\n▪ Format Validation\no Requirement: Ensure the serving size is entered in a standard, consistent \nformat.\no Examples: Grams (g), milliliters (ml).\n▪ Range Validation\no Requirement: Verify that the serving size falls within typical and expected \nranges.\no Examples:\n- For solids: 30g to 500g\n- For liquids: 50ml to 1000ml\no Validation:\n- Compare the serving size with predefined ranges for different food types.\n- Flag any values that fall outside these ranges for review.\n\nCooking steps :\nwrite cooking steps based on the dish name \nfor example,\n\"Cooking Steps\": [\n    \"1. Combine all ingredients in a blender.\",\n    \"2. Blend on high speed until the smoothie is smooth and creamy.\",\n    \"3. Adjust the sweetness with honey or maple syrup to your preference.\",\n    \"4. Pour into a glass and serve immediately.\"\n  ]\n\nplease must be refer and strictly follow this validation rules and format then after generate output",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"Dish Name\": \"Paneer Taash Kabab\", \"Dish Description\": \"Layered paneer slices filled with chutneys, vegetables, and cheese, baked to golden perfection.\", \"Cuisine Category\": \"Asia - Indian - North Indian\", \"Timing Category\": [\"Dinner\", \"Snack\"], \"Meal Category\": [\"Appetizer\", \"Main Course\"], \"Cooking Method\": [\"Baking\"], \"Cooking Time\": \"45 minutes\", \"Cooking Temperature\": \"180°C\", \"Ingredients\": [\"Paneer - 100g\", \"Cheese Slices - 25g\", \"Onions - 30g\", \"Tomatoes - 30g\", \"Mint Chutney - 15g\", \"Grated Cheese - 10g\", \"Fresh Cream - 5g\", \"Hung Yogurt - 20g\", \"Red Chili Powder - 3g\", \"Coriander Powder - 2g\", \"Cumin Powder - 2g\", \"Ginger-Garlic Paste - 5g\", \"Garam Masala - 2g\", \"Mustard Oil - 5ml\", \"Chaat Masala - 2g\", \"Salt - 2.79g\", \"Black Pepper - 2g\"], \"Allergic Content\": {\"Milk and Dairy Products\": [\"Paneer\", \"Cream\", \"Cheese\"]}, \"Serving Size\": \"279g\", \"Cooking Steps\": [\"1. Preheat the oven to 180°C.\", \"2. Slice the paneer into thin pieces and set aside.\", \"3. Mix hung yogurt with red chili powder, coriander powder, cumin powder, ginger-garlic paste, garam masala, mustard oil, salt, and black pepper to make the marinade.\", \"4. Spread mint chutney on half of the paneer slices and top with thin slices of onions and tomatoes. Add cheese slices on top of the vegetables.\", \"5. Cover with the remaining paneer slices to create layers. Brush the tops with the prepared marinade.\", \"6. Place the layered paneer in a baking dish and top with grated cheese, fresh cream, and a sprinkle of chaat masala.\", \"7. Bake in the preheated oven for 20-25 minutes or until the paneer is golden and the cheese has melted.\", \"8. Remove from the oven and serve hot.\"]}\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Caramel Latte",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"Dish Name\": \"Caramel Latte\", \"Dish Description\": \"A sweet and creamy coffee drink with a caramel drizzle.\", \"Cuisine Category\": \"North America - American - Cafe\", \"Timing Category\": [\"Snack\", \"Breakfast\"], \"Meal Category\": [\"Beverage\"], \"Cooking Method\": [\"Steaming\", \"Heating\"], \"Cooking Time\": \"5 minutes\", \"Cooking Temperature\": \"N/A\", \"Ingredients\": [\"Espresso - 60ml\", \"Milk - 150ml\", \"Caramel Syrup - 20ml\", \"Whipped Cream - 30ml\", \"Caramel Sauce - 10ml\"], \"Allergic Content\": {\"Milk and Dairy Products\": [\"Milk\", \"Whipped Cream\"]}, \"Serving Size\": \"270ml\", \"Cooking Steps\": [\"1. Prepare a shot of espresso.\", \"2. Steam milk until frothy.\", \"3. Pour the espresso into a mug.\", \"4. Add caramel syrup and stir gently.\", \"5. Pour the steamed milk over the espresso and caramel syrup.\", \"6. Top with whipped cream and drizzle with caramel sauce.\"]}\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Latte with Sugar Free French Vanilla Syrup",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"Dish Name\": \"Latte with Sugar Free French Vanilla Syrup\", \"Dish Description\": \"A creamy coffee drink with a hint of vanilla flavor.\", \"Cuisine Category\": \"North America - American - Cafe\", \"Timing Category\": [\"Snack\", \"Breakfast\"], \"Meal Category\": [\"Beverage\"], \"Cooking Method\": [\"Steaming\", \"Heating\"], \"Cooking Time\": \"5 minutes\", \"Cooking Temperature\": \"N/A\", \"Ingredients\": [\"Espresso - 60ml\", \"Milk - 150ml\", \"Sugar Free French Vanilla Syrup - 15ml\", \"Whipped Cream - 30ml\"], \"Allergic Content\": {\"Milk and Dairy Products\": [\"Milk\", \"Whipped Cream\"]}, \"Serving Size\": \"255ml\", \"Cooking Steps\": [\"1. Prepare a shot of espresso.\", \"2. Steam milk until frothy.\", \"3. Pour the espresso into a mug.\", \"4. Add sugar-free French vanilla syrup and stir gently.\", \"5. Pour the steamed milk over the espresso and syrup.\", \"6. Top with whipped cream.\"]}\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "GRILLED CHICKEN FILLET",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"Dish Name\": \"Grilled Chicken Fillet\", \"Dish Description\": \"A simple and flavorful grilled chicken fillet, perfect for a quick and healthy meal.\", \"Cuisine Category\": \"North America - American - Main Dishes\", \"Timing Category\": [\"Lunch\", \"Dinner\"], \"Meal Category\": [\"Main Course\"], \"Cooking Method\": [\"Grilling\"], \"Cooking Time\": \"20 minutes\", \"Cooking Temperature\": \"200°C\", \"Ingredients\": [\"Chicken Fillet - 150g\", \"Olive Oil - 10ml\", \"Salt - 2g\", \"Black Pepper - 1g\", \"Garlic Powder - 1g\", \"Paprika - 1g\"], \"Allergic Content\": {}, \"Serving Size\": \"163g\", \"Cooking Steps\": [\"1. Preheat the grill to medium heat.\", \"2. In a bowl, combine olive oil, salt, black pepper, garlic powder, and paprika.\", \"3. Rub the marinade onto the chicken fillet.\", \"4. Place the chicken fillet on the preheated grill and cook for 10-12 minutes, flipping halfway through, until cooked through and has grill marks.\", \"5. Remove from the grill and let rest for a few minutes before serving.\"]}\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "here Serving size is fix that 200g or 200ml for all dishes then calculate ingredients weights according that serving size because serving size calculate sum of all ingredients weights which is fixed 200g or 200ml , add this rule in your memory and also keep all rules and validation rules which i provided before",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"Dish Name\": \"GRILLED CHICKEN FILLET\", \"Dish Description\": \"A simple and flavorful grilled chicken fillet, perfect for a quick and healthy meal.\", \"Cuisine Category\": \"North America - American - Main Dishes\", \"Timing Category\": [\"Lunch\", \"Dinner\"], \"Meal Category\": [\"Main Course\"], \"Cooking Method\": [\"Grilling\"], \"Cooking Time\": \"20 minutes\", \"Cooking Temperature\": \"200°C\", \"Ingredients\": [\"Chicken Fillet - 150g\", \"Olive Oil - 10ml\", \"Salt - 2g\", \"Black Pepper - 1g\", \"Garlic Powder - 1g\", \"Paprika - 1g\"], \"Allergic Content\": {}, \"Serving Size\": \"200g\", \"Cooking Steps\": [\"1. Preheat the grill to medium heat.\", \"2. In a bowl, combine olive oil, salt, black pepper, garlic powder, and paprika.\", \"3. Rub the marinade onto the chicken fillet.\", \"4. Place the chicken fillet on the preheated grill and cook for 10-12 minutes, flipping halfway through, until cooked through and has grill marks.\", \"5. Remove from the grill and let rest for a few minutes before serving.\"]}\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "here sum ingredients weights is 163g but change Ingredients weights according 200g becuase it is fix value for serving size",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"Dish Name\": \"GRILLED CHICKEN FILLET\", \"Dish Description\": \"A simple and flavorful grilled chicken fillet, perfect for a quick and healthy meal.\", \"Cuisine Category\": \"North America - American - Main Dishes\", \"Timing Category\": [\"Lunch\", \"Dinner\"], \"Meal Category\": [\"Main Course\"], \"Cooking Method\": [\"Grilling\"], \"Cooking Time\": \"20 minutes\", \"Cooking Temperature\": \"200°C\", \"Ingredients\": [\"Chicken Fillet - 150g\", \"Olive Oil - 15ml\", \"Salt - 3g\", \"Black Pepper - 1.5g\", \"Garlic Powder - 1.5g\", \"Paprika - 1.5g\"], \"Allergic Content\": {}, \"Serving Size\": \"200g\", \"Cooking Steps\": [\"1. Preheat the grill to medium heat.\", \"2. In a bowl, combine olive oil, salt, black pepper, garlic powder, and paprika.\", \"3. Rub the marinade onto the chicken fillet.\", \"4. Place the chicken fillet on the preheated grill and cook for 10-12 minutes, flipping halfway through, until cooked through and has grill marks.\", \"5. Remove from the grill and let rest for a few minutes before serving.\"]}\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "PASTEURIZED PROCESS AMERICAN CHEESE",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"Dish Name\": \"PASTEURIZED PROCESS AMERICAN CHEESE\", \"Dish Description\": \"A mild and creamy cheese, perfect for sandwiches, burgers, and grilled cheese.\", \"Cuisine Category\": \"North America - American - Dairy\", \"Timing Category\": [\"Snack\", \"Breakfast\", \"Lunch\", \"Dinner\"], \"Meal Category\": [\"Dairy\"], \"Cooking Method\": [\"N/A\"], \"Cooking Time\": \"N/A\", \"Cooking Temperature\": \"N/A\", \"Ingredients\": [\"Pasteurized Process American Cheese - 200g\"], \"Allergic Content\": {\"Milk and Dairy Products\": [\"Pasteurized Process American Cheese\"]}, \"Serving Size\": \"200g\", \"Cooking Steps\": [\"N/A\"]}\n\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Fat Free Chocolate Milk Jug†",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"Dish Name\": \"Fat Free Chocolate Milk Jug\", \"Dish Description\": \"A refreshing and low-fat chocolate milk drink.\", \"Cuisine Category\": \"North America - American - Dairy\", \"Timing Category\": [\"Snack\", \"Breakfast\", \"Lunch\", \"Dinner\"], \"Meal Category\": [\"Dairy\"], \"Cooking Method\": [\"N/A\"], \"Cooking Time\": \"N/A\", \"Cooking Temperature\": \"N/A\", \"Ingredients\": [\"Fat Free Milk - 180ml\", \"Chocolate Syrup - 20ml\"], \"Allergic Content\": {\"Milk and Dairy Products\": [\"Fat Free Milk\"]}, \"Serving Size\": \"200ml\", \"Cooking Steps\": [\"N/A\"]}\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Vanilla McCafé Shake",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"Dish Name\": \"Vanilla McCafé Shake\", \"Dish Description\": \"A creamy and sweet vanilla milkshake.\", \"Cuisine Category\": \"North America - American - Cafe\", \"Timing Category\": [\"Snack\", \"Dessert\"], \"Meal Category\": [\"Beverage\", \"Dessert\"], \"Cooking Method\": [\"Blending\"], \"Cooking Time\": \"2 minutes\", \"Cooking Temperature\": \"N/A\", \"Ingredients\": [\"Vanilla Ice Cream - 150g\", \"Milk - 50ml\"], \"Allergic Content\": {\"Milk and Dairy Products\": [\"Milk\", \"Vanilla Ice Cream\"]}, \"Serving Size\": \"200ml\", \"Cooking Steps\": [\"1. Combine vanilla ice cream and milk in a blender.\", \"2. Blend on high speed until smooth and creamy.\"]}\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "it is parfectly good generated text , please keep this type of information and rules keep in mind",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Iced Coffee with Sugar Free French Vanilla Syrup",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"Dish Name\": \"Iced Coffee with Sugar Free French Vanilla Syrup\", \"Dish Description\": \"A refreshing coffee drink with a hint of vanilla flavor.\", \"Cuisine Category\": \"North America - American - Cafe\", \"Timing Category\": [\"Snack\", \"Breakfast\"], \"Meal Category\": [\"Beverage\"], \"Cooking Method\": [\"Brewing\", \"Cooling\"], \"Cooking Time\": \"5 minutes\", \"Cooking Temperature\": \"N/A\", \"Ingredients\": [\"Coffee - 60ml\", \"Ice - 100g\", \"Sugar Free French Vanilla Syrup - 15ml\", \"Milk - 25ml\"], \"Allergic Content\": {\"Milk and Dairy Products\": [\"Milk\"]}, \"Serving Size\": \"200ml\", \"Cooking Steps\": [\"1. Brew a cup of coffee.\", \"2. Fill a glass with ice.\", \"3. Pour the coffee over the ice.\", \"4. Add sugar-free French vanilla syrup and stir gently.\", \"5. Add milk and stir again.\"]}\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "BLUEBERRY POMEGRANATE SMOOTHIE BASE",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"Dish Name\": \"Blueberry Pomegranate Smoothie Base\", \"Dish Description\": \"A base for a refreshing and antioxidant-rich smoothie.\", \"Cuisine Category\": \"North America - American - Smoothies\", \"Timing Category\": [\"Breakfast\", \"Snack\"], \"Meal Category\": [\"Beverage\"], \"Cooking Method\": [\"Blending\"], \"Cooking Time\": \"2 minutes\", \"Cooking Temperature\": \"N/A\", \"Ingredients\": [\"Frozen Blueberries - 100g\", \"Pomegranate Juice - 100ml\"], \"Allergic Content\": {}, \"Serving Size\": \"200ml\", \"Cooking Steps\": [\"1. Combine frozen blueberries and pomegranate juice in a blender.\", \"2. Blend on high speed until smooth.\"]}\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "LIGHT CREAM\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"Dish Name\": \"LIGHT CREAM\", \"Dish Description\": \"A lighter version of heavy cream, ideal for whipping and adding a touch of richness to dishes.\", \"Cuisine Category\": \"North America - American - Dairy\", \"Timing Category\": [\"Snack\", \"Breakfast\", \"Lunch\", \"Dinner\"], \"Meal Category\": [\"Dairy\"], \"Cooking Method\": [\"N/A\"], \"Cooking Time\": \"N/A\", \"Cooking Temperature\": \"N/A\", \"Ingredients\": [\"Light Cream - 200ml\"], \"Allergic Content\": {\"Milk and Dairy Products\": [\"Light Cream\"]}, \"Serving Size\": \"200ml\", \"Cooking Steps\": [\"N/A\"]}\n\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "STRAWBERRY SHAKE SYRUP",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"Dish Name\": \"STRAWBERRY SHAKE SYRUP\", \"Dish Description\": \"A sweet and flavorful syrup for making strawberry shakes.\", \"Cuisine Category\": \"North America - American - Syrups\", \"Timing Category\": [\"Snack\"], \"Meal Category\": [\"Syrup\"], \"Cooking Method\": [\"N/A\"], \"Cooking Time\": \"N/A\", \"Cooking Temperature\": \"N/A\", \"Ingredients\": [\"Strawberry Shake Syrup - 200ml\"], \"Allergic Content\": {}, \"Serving Size\": \"200ml\", \"Cooking Steps\": [\"N/A\"]}\n\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Southern Style Crispy Chicken Sandwich",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"Dish Name\": \"Southern Style Crispy Chicken Sandwich\", \"Dish Description\": \"A classic Southern comfort food, featuring a crispy fried chicken breast, pickles, and creamy coleslaw on a toasted bun.\", \"Cuisine Category\": \"North America - American - Southern\", \"Timing Category\": [\"Lunch\", \"Dinner\"], \"Meal Category\": [\"Main Course\"], \"Cooking Method\": [\"Frying\", \"Toasting\"], \"Cooking Time\": \"20 minutes\", \"Cooking Temperature\": \"180°C\", \"Ingredients\": [\"Chicken Breast - 100g\", \"All-Purpose Flour - 20g\", \"Cornstarch - 10g\", \"Salt - 2g\", \"Black Pepper - 1g\", \"Paprika - 1g\", \"Garlic Powder - 1g\", \"Cayenne Pepper - 0.5g\", \"Vegetable Oil - 50ml\", \"Mayonnaise - 20ml\", \"Vinegar - 5ml\", \"Sugar - 5g\", \"Salt - 1g\", \"Black Pepper - 0.5g\", \"Cabbage - 50g\", \"Carrots - 20g\", \"Pickles - 20g\", \"Hamburger Bun - 50g\"], \"Allergic Content\": {}, \"Serving Size\": \"200g\", \"Cooking Steps\": [\"1. In a bowl, whisk together flour, cornstarch, salt, black pepper, paprika, garlic powder, and cayenne pepper.\", \"2. Season the chicken breast with salt and pepper.\", \"3. Dredge the chicken breast in the flour mixture, ensuring it's fully coated.\", \"4. Heat vegetable oil in a skillet over medium-high heat.\", \"5. Carefully place the chicken breast in the hot oil and fry for 5-7 minutes per side, until golden brown and cooked through.\", \"6. While the chicken is frying, prepare the coleslaw by finely shredding cabbage and carrots.\", \"7. In a separate bowl, whisk together mayonnaise, vinegar, sugar, salt, and black pepper.\", \"8. Add the shredded cabbage and carrots to the dressing and toss to combine.\", \"9. Toast the hamburger bun.\", \"10. Place the fried chicken breast on the toasted bun, top with coleslaw and pickles.\"]}\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Bacon Cheddar McChicken",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"Dish Name\": \"Bacon Cheddar McChicken\", \"Dish Description\": \"A classic chicken sandwich with a twist, featuring crispy chicken, bacon, and cheddar cheese.\", \"Cuisine Category\": \"North America - American - Fast Food\", \"Timing Category\": [\"Lunch\", \"Dinner\"], \"Meal Category\": [\"Main Course\"], \"Cooking Method\": [\"Frying\", \"Grilling\", \"Toasting\"], \"Cooking Time\": \"15 minutes\", \"Cooking Temperature\": \"180°C\", \"Ingredients\": [\"Chicken Breast - 80g\", \"Breadcrumbs - 20g\", \"Flour - 10g\", \"Salt - 1g\", \"Black Pepper - 0.5g\", \"Paprika - 0.5g\", \"Garlic Powder - 0.5g\", \"Vegetable Oil - 30ml\", \"Bacon - 20g\", \"Cheddar Cheese - 20g\", \"Hamburger Bun - 50g\", \"Mayonnaise - 10ml\", \"Lettuce - 10g\", \"Tomato - 10g\"], \"Allergic Content\": {\"Milk and Dairy Products\": [\"Cheddar Cheese\"]}, \"Serving Size\": \"200g\", \"Cooking Steps\": [\"1. In a bowl, combine breadcrumbs, flour, salt, black pepper, paprika, and garlic powder.\", \"2. Season the chicken breast with salt and pepper.\", \"3. Dredge the chicken breast in the flour mixture, ensuring it's fully coated.\", \"4. Heat vegetable oil in a skillet over medium-high heat.\", \"5. Carefully place the chicken breast in the hot oil and fry for 5-7 minutes per side, until golden brown and cooked through.\", \"6. While the chicken is frying, cook the bacon in a separate skillet until crispy.\", \"7. Toast the hamburger bun.\", \"8. Spread mayonnaise on the toasted bun.\", \"9. Layer the fried chicken breast, bacon, cheddar cheese, lettuce, and tomato on the bun.\"]}\n\n```",
      ],
    },
  ]
)  
    
    # Send the dish name to the model and receive the response
    response = chat_session.send_message(dish_name)

    try:
        dish_info = json.loads(response.text)
        st.subheader("Generated Dish Information:")
        st.json(dish_info)  # Display the response in JSON format
    except json.JSONDecodeError:
        st.error("Failed to decode the response as JSON.")