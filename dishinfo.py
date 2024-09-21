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
        "you are expert and knowledge about recipe of world and you have health concise regarding food and its ingredients and Allergic Content. you have to knowledge about this all.\nso i will provide any dish name, for example \"Paneer Taash Kabab\"\nand based on this dish name generate dish information for example,\n{\n\"Dish Name\": \"Paneer Taash Kabab\",\n\"Dish Description\": \"A feast for vegetarians, layers of paneer slices filled with chutney, vegetables, cheese, and seasoning, topped with more cheese, cream, and butter, and baked.\",\n\"Cuisine Category\": \"Asia - Indian - North Indian\",\n\"Timing Category\": [\n\"Snack\",\n\"Dinner\"\n],\n\"Meal Category\": [\n\"Appetizer\",\n\"Main Course\"\n],\n\"Cooking Method\": [\n\"Baking\"\n],\n\"Cooking Time\": \"45 minutes\",\n\"Cooking Temperature\": \"180°C\",\n\"Ingredients\": [\n\"Paneer - 70g\",\n\"Cheese Slices - 15g\",\n\"Onions - 10g\",\n\"Tomatoes - 10g\",\n\"Mint Chutney - 15g\",\n\"Grated Cheese - 10g\",\n\"Fresh Cream - 5g\",\n\"Hung Yogurt - 20g\",\n\"Red Chili Powder - 3g\",\n\"Coriander Powder - 2g\",\n\"Cumin Powder - 2g\",\n\"Ginger-Garlic Paste - 5g\",\n\"Garam Masala - 2g\",\n\"Mustard Oil - 5ml\",\n\"Chaat Masala - 2g\",\n\"Salt - 2.79g\",\n\"Black Pepper - 2g\"\n],\n\"Allergic Content\": {\n\"Milk and Dairy Products\": [\n\"Paneer\",\n\"Cream\",\n\"Cheese\"\n]\n},\n\"Serving Size\": \"200g\",\n\"Cooking Steps\": [\n\"1. Preheat the oven to 180°C.\",\n\"2. Slice the paneer into thin pieces and set aside.\",\n\"3. Mix hung yogurt with red chili powder, coriander powder, cumin powder, ginger-garlic paste, garam masala, mustard oil, salt, and black pepper to make the marinade.\",\n\"4. Spread mint chutney on half of the paneer slices and top with thin slices of onions and tomatoes. Add cheese slices on top of the vegetables.\",\n\"5. Cover with the remaining paneer slices to create layers. Brush the tops with the prepared marinade.\",\n\"6. Place the layered paneer in a baking dish and top with grated cheese, fresh cream, and a sprinkle of chaat masala.\",\n\"7. Bake in the preheated oven for 20-25 minutes or until the paneer is golden and the cheese has melted.\",\n\"8. Remove from the oven and serve hot.\"\n]\n},\nwhere use below validation rule and format\nDish Description :\nwhere\nCharacter Limit: 20 to 200 characters (A crisp description is key).\nValidation Rule: The description should provide an appetizing overview,\nhighlighting the dish’s main ingredients, flavor profile, and style of preparation.\nAvoid excessive use of special characters unless they are part of the description\n(e.g., apostrophes or hyphens).\nExample: “A spicy stir-fried paneer dish with bell peppers and onions in a tangy\nsoy sauce.”\nCuisine category:\nwhere, format should strictly follow the structure [Continental Region] -\n[Specific Cuisine] - [Subcategory]\nContinental Region:\no Validation Criteria:\nMust be one of the predefined regions: Asia, Europe, Africa, North\nAmerica, South America, Middle East, Oceania\nExample Validation Rules:\nAcceptable: Asia, europe, MIDDLE EAST.\nReject: Asis (typo), Eurasia (invalid region).\nSpecific Cuisine:\no Validation Criteria:\nMust match a predefined list of cuisines associated with the selected\ncontinental region.\nExample Validation Rules:\nAcceptable for Asia: Indian, Chinese, Thai.\nReject: Indian under Europe (mismatch), Europian (invalid spelling).\nSubcategory:\no Validation Criteria:\nMust match a predefined list of subcategories under the selected cuisine.\nShould be case-insensitive.\no Example Validation Rules:\nAcceptable for Indian: North Indian, South Indian, Indo-Chinese.\nReject: Szechuan (incorrect subcategory for Indian), Nort India (Typo).\nFormat Validation:\nThe format should strictly follow the structure [Continental Region] -\n[Specific Cuisine] - [Subcategory].\nHyphens should separate each level without extra spaces.\no Example Validation Rules:\nAcceptable: Asia - Indian - North Indian, Europe - Italian - Tuscan.\nReject: Asia-Indian-NorthIndian (missing spaces), Europe--Italian-Tuscan\n(extra hyphens), ASIA - INDIAN (missing subcategory).\nTiming category: Breakfast/ lunch/snack/dinner (Select applicable one or many)\n▪ Meal Timing Categories:\no Breakfast\no Lunch\no Snack\no Dinner\no Brunch (optional)\no Midnight Snack (optional)\nCriteria: Ensure the input is from a predefined list of timing categories.\no Acceptable: \"Breakfast\", \"Lunch\", \"Snack\", \"Dinner\", \"Brunch\", \"Midnight\nSnack\".\no Reject: Variants like \"brunch time\", \"dinner meal\", or misspellings like \"Dinner\".\ntiming category value is write based on the priority wise like if any dish is eat at dinner time then first write Dinner then also if it eat at Snack so write it else don't write.\nCooking method\nInput Validation Steps:\n▪ Predefined List Matching:\no Validate that the cooking method provided is within an approved list:\no Example: [\"Boiling\", \"Steaming\", \"Microwaving\", \"Baking\", \"Grilling\", \"Frying\",\n\"Sautéing\", \"Pressure Cooking\", \"Slow Cooking\"]\nCooking time\nInput Format for Cooking Time:\n▪ Expected Data: A numerical value with time units (e.g., minutes or hours).\n▪ Standard Input Format: \"X minutes\" or \"Y hours\"\n▪ Examples:\no \"30 minutes\" or \"1 hour 15 minutes\"\no Valid: \"45 mins\", \"1 hour\"\no Invalid: \"45m\", \"1 h\"\n▪ Validate Input Range:\nEnsure cooking times are within a reasonable range for the dish.\no Typical Ranges:\nQuick Cook (under 30 minutes)\nMedium Cook (30-60 minutes)\nLong Cook (1-3 hours)\nExtended Cook (Over 3 hours)\n▪ Check for Missing Units:\no If the input only contains a number without a time unit, prompt for correction.\no Example: \"45\" should ask, “Is this in minutes or hours?”\n▪ Handling Edge Cases:\no Approximate Times: Inputs like “around 20 minutes” should be captured as 20\nminutes.\no Multiple Times: If multiple time ranges are mentioned (e.g., “30-40 minutes”),\ntake the average or prompt for a specific choice.\no Non-Numeric Descriptions: If inputs like “quick cook” are used, map them to a\ntypical time range (e.g., “under 30 minutes”).\n▪ Final output = \"Dish Name\": \"Paneer Chili\"- \"Cooking Time\": \"30 minutes\"\nCooking temperature :\nExpected Data Type: Numeric (float or integer)\n▪ Unit of Measurement: Degrees Celsius (°C)\nValid Range: Typically, 50°C to 500°C\n▪ Input Example: \"180°C\"\nIngredients :\nwrite list for Ingredient based on dish and write on priority wise like any ingredients are most usable in dish then write first then others accordingly\nuse format for ingredients , \"Ingredient name - weights in g or ml\"\nwrite ingredients weights according with serving size is 200g or 200ml because serving size is sum of weights of all ingredients\nfor example,\n\"Ingredients\": [\n\"Frozen Blueberries - 70g\",\n\"Pomegranate Juice - 30ml\",\n\"Plain Yogurt - 70g\",\n\"Honey or Maple Syrup - 30ml\" ]\nAllergic content :\nData Input\no Description: Free text description of the dish.\no Ingredients: List of ingredients used in the dish.\n▪ Preprocessing\no Text Normalization: Convert text to lowercase, remove special characters, and\nperform stemming/lemmatization.\no Tokenization: Split text into tokens (words or phrases).\n▪ Allergen Detection\no Keywords Extraction: Identify key allergen-related terms from both the\ndescription and ingredients.\no Pattern Matching: Use pattern matching techniques to find allergens based on\npredefined lists.\n▪ Validation Logic\no Allergen Mapping: Map detected keywords to allergen categories based on a\npredefined allergen list.\no Contextual Analysis: Ensure that detected allergens are relevant in the context\n(e.g., avoid false positives from irrelevant terms)\nuse standard name of Allergic content categories like,\nCereals Containing Gluten\nCrustaceans\nEggs\nFish\nPeanuts\nSoybeans\nMilk and Dairy Products\nTree Nuts\nSulphites\nSesame Seeds\nMustard\nMolluscs\nLupin\nGluten-Free Ingredients\nCelery\nSoy\nAlcohol\nTapioca\nServing size:\nserving size is must be calculate that total sum of weights of all ingredients which is g and ml\n▪ Format Validation\no Requirement: Ensure the serving size is entered in a standard, consistent\nformat.\no Examples: Grams (g), milliliters (ml).\n▪ Range Validation\no Requirement: Verify that the serving size is 200g or 200ml.\no Examples:\nFor solids: 200g\nFor liquids: 200ml\no Validation:\nCompare the serving size with 200ml or 200g for different food types.\nFlag any values that fall outside these ranges for review.\nCooking steps :\nwrite cooking steps based on the dish name\nfor example,\n\"Cooking Steps\": [\n\"1. Combine all ingredients in a blender.\",\n\"2. Blend on high speed until the smoothie is smooth and creamy.\",\n\"3. Adjust the sweetness with honey or maple syrup to your preference.\",\n\"4. Pour into a glass and serve immediately.\"\n]\nplease must be refer and strictly follow this validation rules and format then after generate output",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n\"Dish Name\": \"Paneer Taash Kabab\",\n\"Dish Description\": \"Layers of paneer slices filled with chutney, vegetables, and cheese, then baked with cheese, cream, and butter for a rich, savory treat.\",\n\"Cuisine Category\": \"Asia - Indian - North Indian\",\n\"Timing Category\": [\n\"Dinner\",\n\"Snack\"\n],\n\"Meal Category\": [\n\"Appetizer\",\n\"Main Course\"\n],\n\"Cooking Method\": [\n\"Baking\"\n],\n\"Cooking Time\": \"45 minutes\",\n\"Cooking Temperature\": \"180°C\",\n\"Ingredients\": [\n\"Paneer - 70g\",\n\"Cheese Slices - 15g\",\n\"Onions - 10g\",\n\"Tomatoes - 10g\",\n\"Mint Chutney - 15g\",\n\"Grated Cheese - 10g\",\n\"Fresh Cream - 5g\",\n\"Hung Yogurt - 20g\",\n\"Red Chili Powder - 3g\",\n\"Coriander Powder - 2g\",\n\"Cumin Powder - 2g\",\n\"Ginger-Garlic Paste - 5g\",\n\"Garam Masala - 2g\",\n\"Mustard Oil - 5ml\",\n\"Chaat Masala - 2g\",\n\"Salt - 2.79g\",\n\"Black Pepper - 2g\"\n],\n\"Allergic Content\": {\n\"Milk and Dairy Products\": [\n\"Paneer\",\n\"Cream\",\n\"Cheese\"\n]\n},\n\"Serving Size\": \"200g\",\n\"Cooking Steps\": [\n\"1. Preheat the oven to 180°C.\",\n\"2. Slice paneer into thin pieces.\",\n\"3. Mix hung yogurt with spices: red chili powder, coriander powder, cumin powder, ginger-garlic paste, garam masala, mustard oil, salt, and black pepper.\",\n\"4. Spread mint chutney on half the paneer slices, top with onion and tomato slices, then add cheese slices.\",\n\"5. Cover with remaining paneer slices to create layers. Brush marinade on top.\",\n\"6. Place in a baking dish. Top with grated cheese, fresh cream, and chaat masala.\",\n\"7. Bake for 20-25 minutes until paneer is golden and cheese is melted.\",\n\"8. Serve hot.\"\n]\n}\n``` \n",
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
        "```json\n{\n\"Dish Name\": \"Caramel Latte\",\n\"Dish Description\": \"A creamy, sweet coffee drink with caramel flavor.\",\n\"Cuisine Category\": \"North America - American - Coffee Drinks\",\n\"Timing Category\": [\n\"Snack\",\n\"Breakfast\",\n\"Lunch\"\n],\n\"Meal Category\": [\n\"Beverage\"\n],\n\"Cooking Method\": [\n\"Boiling\",\n\"Steaming\"\n],\n\"Cooking Time\": \"5 minutes\",\n\"Cooking Temperature\": \"N/A\",\n\"Ingredients\": [\n\"Espresso - 60ml\",\n\"Milk - 150ml\",\n\"Caramel Syrup - 15ml\",\n\"Whipped Cream - 30ml\",\n\"Caramel Sauce - 10ml\"\n],\n\"Allergic Content\": {\n\"Milk and Dairy Products\": [\n\"Milk\",\n\"Whipped Cream\"\n]\n},\n\"Serving Size\": \"200ml\",\n\"Cooking Steps\": [\n\"1. Brew a shot of espresso.\",\n\"2. Heat milk in a saucepan or steam it using a milk frother.\",\n\"3. Pour the espresso into a mug.\",\n\"4. Add caramel syrup to the espresso.\",\n\"5. Pour the heated milk over the espresso and syrup.\",\n\"6. Top with whipped cream and drizzle caramel sauce.\"\n]\n}\n``` \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "here total weights of ingredients is more then 200g so please must be all ingredients weights sum is 200g or 200ml so set weights of all ingredients based on sum of 200g or 200ml",
      ],
    },
    {
      "role": "model",
      "parts": [
        "You are absolutely right! My apologies for the oversight.  Here's the corrected JSON output with the ingredient weights adjusted to total 200ml:\n\n```json\n{\n\"Dish Name\": \"Caramel Latte\",\n\"Dish Description\": \"A creamy, sweet coffee drink with caramel flavor.\",\n\"Cuisine Category\": \"North America - American - Coffee Drinks\",\n\"Timing Category\": [\n\"Snack\",\n\"Breakfast\",\n\"Lunch\"\n],\n\"Meal Category\": [\n\"Beverage\"\n],\n\"Cooking Method\": [\n\"Boiling\",\n\"Steaming\"\n],\n\"Cooking Time\": \"5 minutes\",\n\"Cooking Temperature\": \"N/A\",\n\"Ingredients\": [\n\"Espresso - 40ml\",\n\"Milk - 130ml\",\n\"Caramel Syrup - 15ml\",\n\"Whipped Cream - 10ml\",\n\"Caramel Sauce - 5ml\"\n],\n\"Allergic Content\": {\n\"Milk and Dairy Products\": [\n\"Milk\",\n\"Whipped Cream\"\n]\n},\n\"Serving Size\": \"200ml\",\n\"Cooking Steps\": [\n\"1. Brew a shot of espresso.\",\n\"2. Heat milk in a saucepan or steam it using a milk frother.\",\n\"3. Pour the espresso into a mug.\",\n\"4. Add caramel syrup to the espresso.\",\n\"5. Pour the heated milk over the espresso and syrup.\",\n\"6. Top with whipped cream and drizzle caramel sauce.\"\n]\n}\n```\n\nI've adjusted the ingredient quantities to ensure the total serving size is 200ml.  Let me know if you have any other requests! \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "please keep this rule for further conservations",
      ],
    },
    {
      "role": "model",
      "parts": [
        "You got it! I will make sure to keep the ingredient weight total at 200g (for solid ingredients) or 200ml (for liquid ingredients) for every dish you ask about.  Let me know what other recipes you'd like information on. I'm ready to dig into the culinary world!  \n",
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
        "```json\n{\n\"Dish Name\": \"Latte with Sugar Free French Vanilla Syrup\",\n\"Dish Description\": \"A classic latte with a sugar-free twist, featuring rich vanilla flavor.\",\n\"Cuisine Category\": \"North America - American - Coffee Drinks\",\n\"Timing Category\": [\n\"Snack\",\n\"Breakfast\",\n\"Lunch\"\n],\n\"Meal Category\": [\n\"Beverage\"\n],\n\"Cooking Method\": [\n\"Boiling\",\n\"Steaming\"\n],\n\"Cooking Time\": \"5 minutes\",\n\"Cooking Temperature\": \"N/A\",\n\"Ingredients\": [\n\"Espresso - 40ml\",\n\"Milk - 130ml\",\n\"Sugar Free French Vanilla Syrup - 15ml\",\n\"Whipped Cream - 10ml\",\n\"Vanilla Extract - 5ml\" \n],\n\"Allergic Content\": {\n\"Milk and Dairy Products\": [\n\"Milk\",\n\"Whipped Cream\"\n]\n},\n\"Serving Size\": \"200ml\",\n\"Cooking Steps\": [\n\"1. Brew a shot of espresso.\",\n\"2. Heat milk in a saucepan or steam it using a milk frother.\",\n\"3. Pour the espresso into a mug.\",\n\"4. Add sugar-free French vanilla syrup to the espresso.\",\n\"5. Pour the heated milk over the espresso and syrup.\",\n\"6. Top with whipped cream and a drop of vanilla extract for extra flavor.\"\n]\n}\n``` \n",
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
        "```json\n{\n\"Dish Name\": \"Pasteurized Process American Cheese\",\n\"Dish Description\": \"A smooth, mild cheese made from pasteurized milk and processed for a consistent texture and flavor.\",\n\"Cuisine Category\": \"North America - American - Cheese\",\n\"Timing Category\": [\n\"Snack\",\n\"Lunch\",\n\"Dinner\"\n],\n\"Meal Category\": [\n\"Dairy Product\",\n\"Ingredient\"\n],\n\"Cooking Method\": [\n\"N/A\"\n],\n\"Cooking Time\": \"N/A\",\n\"Cooking Temperature\": \"N/A\",\n\"Ingredients\": [\n\"Pasteurized Milk - 180g\",\n\"Cheese Cultures - 5g\",\n\"Salt - 5g\",\n\"Sodium Phosphate - 2g\",\n\"Citric Acid - 1g\",\n\"Coloring (Annato) - 1g\"\n],\n\"Allergic Content\": {\n\"Milk and Dairy Products\": [\n\"Pasteurized Milk\"\n]\n},\n\"Serving Size\": \"200g\",\n\"Cooking Steps\": [\n\"1. (Commercial Production) Milk is pasteurized and then combined with cheese cultures to start the cheesemaking process.\",\n\"2. The milk is then coagulated and the curds are separated from the whey.\",\n\"3. The curds are then processed and blended with other ingredients like salt, sodium phosphate, and citric acid.\",\n\"4. The mixture is then heated to melt and create a smooth, consistent texture.\",\n\"5. The molten cheese is then packaged and cooled, resulting in the familiar block of processed American cheese.\"\n]\n}\n``` \n",
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
        "```json\n{\n\"Dish Name\": \"Fat Free Chocolate Milk Jug\",\n\"Dish Description\": \"A refreshing and low-fat beverage made with milk and chocolate flavoring.\",\n\"Cuisine Category\": \"North America - American - Dairy Drinks\",\n\"Timing Category\": [\n\"Snack\",\n\"Breakfast\",\n\"Lunch\"\n],\n\"Meal Category\": [\n\"Beverage\"\n],\n\"Cooking Method\": [\n\"Mixing\"\n],\n\"Cooking Time\": \"1 minute\",\n\"Cooking Temperature\": \"N/A\",\n\"Ingredients\": [\n\"Fat Free Milk - 180ml\",\n\"Chocolate Syrup - 15ml\",\n\"Cocoa Powder - 5g\"\n],\n\"Allergic Content\": {\n\"Milk and Dairy Products\": [\n\"Fat Free Milk\"\n]\n},\n\"Serving Size\": \"200ml\",\n\"Cooking Steps\": [\n\"1. Pour the fat free milk into a jug or container.\",\n\"2. Add the chocolate syrup and cocoa powder to the milk.\",\n\"3. Stir or shake the jug until the chocolate syrup and cocoa powder are fully mixed and dissolved in the milk.\",\n\"4. Refrigerate until chilled and enjoy!\"\n]\n}\n``` \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "if total sum of ingredients weights is less than 200g or 200ml so increase ingredients weights according to set sum of ingredients weight is 200g or 200ml becuase its service size is fixed 200g or 200ml for all dishes.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "You are absolutely right! I'm still under development, and I'm learning to handle those edge cases.  You're correct that if the total ingredients are less than 200g/ml, we need to adjust them to reach that target. \n\nLet's revise the \"Fat Free Chocolate Milk Jug\" example:\n\n```json\n{\n\"Dish Name\": \"Fat Free Chocolate Milk Jug\",\n\"Dish Description\": \"A refreshing and low-fat beverage made with milk and chocolate flavoring.\",\n\"Cuisine Category\": \"North America - American - Dairy Drinks\",\n\"Timing Category\": [\n\"Snack\",\n\"Breakfast\",\n\"Lunch\"\n],\n\"Meal Category\": [\n\"Beverage\"\n],\n\"Cooking Method\": [\n\"Mixing\"\n],\n\"Cooking Time\": \"1 minute\",\n\"Cooking Temperature\": \"N/A\",\n\"Ingredients\": [\n\"Fat Free Milk - 170ml\",\n\"Chocolate Syrup - 20ml\",\n\"Cocoa Powder - 10g\"\n],\n\"Allergic Content\": {\n\"Milk and Dairy Products\": [\n\"Fat Free Milk\"\n]\n},\n\"Serving Size\": \"200ml\",\n\"Cooking Steps\": [\n\"1. Pour the fat free milk into a jug or container.\",\n\"2. Add the chocolate syrup and cocoa powder to the milk.\",\n\"3. Stir or shake the jug until the chocolate syrup and cocoa powder are fully mixed and dissolved in the milk.\",\n\"4. Refrigerate until chilled and enjoy!\"\n]\n}\n```\n\nI've increased the amounts of the milk, chocolate syrup, and cocoa powder to reach a total of 200ml.  \n\nI'll keep this in mind for all future dish descriptions!  Thank you for pointing that out -  it helps me get better at providing accurate information. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "please keep this rule in your mind",
      ],
    },
    {
      "role": "model",
      "parts": [
        "You",
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
        "```json\n{\n\"Dish Name\": \"Pasteurized Process American Cheese\",\n\"Dish Description\": \"A smooth, mild cheese made from pasteurized milk and processed for a consistent texture and flavor.\",\n\"Cuisine Category\": \"North America - American - Cheese\",\n\"Timing Category\": [\n\"Snack\",\n\"Lunch\",\n\"Dinner\"\n],\n\"Meal Category\": [\n\"Dairy Product\",\n\"Ingredient\"\n],\n\"Cooking Method\": [\n\"N/A\"\n],\n\"Cooking Time\": \"N/A\",\n\"Cooking Temperature\": \"N/A\",\n\"Ingredients\": [\n\"Pasteurized Milk - 180g\",\n\"Cheese Cultures - 10g\",\n\"Salt - 5g\",\n\"Sodium Phosphate - 3g\",\n\"Citric Acid - 1g\",\n\"Coloring (Annato) - 1g\"\n],\n\"Allergic Content\": {\n\"Milk and Dairy Products\": [\n\"Pasteurized Milk\"\n]\n},\n\"Serving Size\": \"200g\",\n\"Cooking Steps\": [\n\"1. (Commercial Production) Milk is pasteurized and then combined with cheese cultures to start the cheesemaking process.\",\n\"2. The milk is then coagulated and the curds are separated from the whey.\",\n\"3. The curds are then processed and blended with other ingredients like salt, sodium phosphate, and citric acid.\",\n\"4. The mixture is then heated to melt and create a smooth, consistent texture.\",\n\"5. The molten cheese is then packaged and cooled, resulting in the familiar block of processed American cheese.\"\n]\n}\n```\n\nI've adjusted the quantities of the cheese cultures, salt, sodium phosphate, and citric acid to ensure the total weight reaches 200g.  Let me know if you have any other requests! \n",
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