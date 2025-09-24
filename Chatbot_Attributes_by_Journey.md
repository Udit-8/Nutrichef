# 🤖 Nutrition Chatbot - Required Attributes by Journey

---

## **Journey 1: Recipe Discovery**

### **Data Attributes:**
- **recipe_id** (string) - Unique identifier for each recipe
- **recipe_name** (string) - Name of the recipe
- **recipe_image_url** (string) - URL to recipe image
- **cuisine_type** (string) - e.g., Italian, Mexican, Asian, etc.
- **ingredients** (array) - List of ingredient objects with name, quantity, unit
- **dietary_restrictions** (array) - vegetarian, vegan, gluten-free, dairy-free, etc.
- **prep_time** (integer) - Preparation time in minutes
- **cook_time** (integer) - Cooking time in minutes
- **total_time** (integer) - Total time in minutes
- **difficulty_level** (string) - Easy, Medium, Hard
- **rating** (float) - Average user rating (1-5 stars)
- **rating_count** (integer) - Number of ratings
- **description** (string) - Brief recipe description
- **servings** (integer) - Number of servings the recipe makes
- **occasion_tags** (array) - dinner party, quick lunch, family meal, etc.
- **nutrition_facts** (object) - Calories, protein, carbs, fats, fiber per serving
- **cooking_steps** (array) - Step-by-step cooking instructions
- **equipment_needed** (array) - Required cooking equipment

### **User State Attributes:**
- **discovery_method** (string) - cuisine, ingredients, dietary, time, occasion
- **selected_cuisine** (string) - User's cuisine preference
- **available_ingredients** (array) - Ingredients user has available
- **user_dietary_restrictions** (array) - User's dietary restrictions
- **cooking_time_available** (integer) - Time user has to cook (minutes)
- **selected_occasion** (string) - User's cooking occasion
- **search_results** (array) - Current recipe search results
- **favorites** (array) - User's saved favorite recipes

---

## **Journey 2: Step-by-Step Cooking Guidance**

### **Data Attributes:**
- **recipe_id** (string) - ID of recipe being cooked
- **adjusted_servings** (integer) - Number of servings user wants to make
- **adjusted_ingredients** (array) - Ingredient quantities adjusted for servings
- **cooking_steps** (array) - Detailed step-by-step instructions
- **step_timers** (array) - Timer durations for specific steps
- **equipment_checklist** (array) - Required equipment for the recipe
- **prep_instructions** (array) - Ingredient preparation steps
- **cooking_tips** (array) - Helpful tips for each step
- **visual_cues** (array) - What to look for at each step

### **Session State Attributes:**
- **current_step** (integer) - Current cooking step number
- **total_steps** (integer) - Total number of cooking steps
- **session_status** (string) - prep, cooking, paused, completed
- **active_timers** (array) - Currently running timers with remaining time
- **completed_steps** (array) - Steps user has completed
- **cooking_start_time** (datetime) - When cooking session started
- **hands_free_mode** (boolean) - Voice control enabled/disabled

### **User Interaction Attributes:**
- **voice_commands_enabled** (boolean) - User preference for voice control
- **step_feedback** (string) - User feedback on cooking results
- **recipe_rating** (integer) - User's rating for the recipe (1-5)
- **cooking_notes** (string) - User's personal notes about the recipe

---

## **Journey 3: Calorie-Based Meal Suggestions**

### **Data Attributes:**
- **meal_id** (string) - Unique identifier for meal suggestions
- **meal_name** (string) - Name of the suggested meal
- **meal_image_url** (string) - URL to meal image
- **calories_per_serving** (integer) - Exact calorie count
- **macronutrients** (object) - protein_g, carbs_g, fats_g, fiber_g
- **micronutrients** (object) - vitamins and minerals content
- **preparation_time** (integer) - Time to prepare the meal (minutes)
- **meal_components** (array) - Individual food items in the meal
- **ingredient_substitutions** (array) - Alternative ingredients available

### **User Goal Attributes:**
- **calorie_target** (integer) - User's target calorie amount
- **timeframe** (string) - single_meal, full_day, weekly
- **target_meal_type** (string) - breakfast, lunch, dinner, snack
- **daily_calorie_goal** (integer) - User's daily calorie target
- **macro_ratio_preferences** (object) - protein_%, carbs_%, fats_%
- **calorie_tolerance** (integer) - Acceptable calorie range (+/-)

### **Preference Attributes:**
- **dietary_restrictions** (array) - User's dietary limitations
- **cuisine_preferences** (array) - Preferred cuisine types
- **ingredient_dislikes** (array) - Ingredients user wants to avoid
- **ingredient_allergies** (array) - Ingredients user is allergic to
- **meal_complexity** (string) - simple, moderate, complex

### **Session State Attributes:**
- **generated_meals** (array) - Current meal suggestions
- **selected_meals** (array) - Meals user has chosen
- **customization_history** (array) - Changes user made to suggestions
- **nutritional_summary** (object) - Total calories and macros for selected meals

---

## **Journey 4: Event-Driven Meal Planning**

### **Event Attributes:**
- **event_id** (string) - Unique identifier for the event
- **event_type** (string) - birthday, wedding, office_party, etc.
- **event_name** (string) - Custom name for the event
- **guest_count** (integer) - Number of guests attending
- **event_date** (date) - Date of the event
- **event_start_time** (time) - Event start time
- **event_duration** (integer) - Duration in hours
- **venue_type** (string) - home, restaurant, outdoor, office
- **kitchen_constraints** (array) - Available cooking equipment/space
- **budget_min** (integer) - Minimum budget amount
- **budget_max** (integer) - Maximum budget amount
- **budget_currency** (string) - Currency for budget

### **Menu Attributes:**
- **menu_id** (string) - Unique menu identifier
- **service_style** (string) - buffet, plated, cocktail, family_style
- **menu_categories** (object) - appetizers[], mains[], sides[], desserts[]
- **dietary_accommodations** (array) - Special dietary needs for guests
- **kids_menu_needed** (boolean) - Whether kids menu is required
- **cuisine_style** (array) - Preferred cuisine styles for the event

### **Menu Items Attributes:**
- **dish_id** (string) - Unique dish identifier
- **dish_name** (string) - Name of the dish
- **dish_category** (string) - appetizer, main, side, dessert
- **cost_per_serving** (float) - Cost per guest serving
- **preparation_time** (integer) - Time to prepare the dish
- **quantity_per_guest** (float) - Serving size per guest
- **total_quantity_needed** (float) - Total quantity for all guests
- **dietary_tags** (array) - vegetarian, vegan, gluten_free, etc.

### **Planning Attributes:**
- **preparation_schedule** (array) - Timeline of when to prepare each item
- **shopping_list** (array) - Consolidated ingredient list with quantities
- **total_estimated_cost** (float) - Total cost estimate for the menu
- **preparation_timeline** (object) - Day-by-day preparation schedule
- **serving_timeline** (object) - Order and timing of serving dishes

---

## **Journey 5: Daily and Weekly Meal Planning**

### **Plan Attributes:**
- **meal_plan_id** (string) - Unique meal plan identifier
- **plan_type** (string) - daily, weekly
- **plan_duration** (integer) - Number of days in the plan
- **start_date** (date) - When the meal plan starts
- **end_date** (date) - When the meal plan ends
- **meals_included** (array) - breakfast, lunch, dinner, snacks
- **total_planned_calories** (integer) - Total calories for the plan period

### **Personal Profile Attributes:**
- **daily_calorie_goal** (integer) - User's daily calorie target
- **macro_targets** (object) - protein_g, carbs_g, fats_g targets per day
- **dietary_restrictions** (array) - User's dietary limitations
- **cooking_skill_level** (string) - beginner, intermediate, advanced
- **time_constraints** (object) - available cooking time per meal
- **household_size** (integer) - Number of people to cook for
- **budget_per_day** (float) - Daily food budget
- **preferred_cuisines** (array) - User's favorite cuisine types

### **Daily Plan Attributes:**
- **plan_date** (date) - Specific date for daily plan
- **breakfast** (object) - Meal details for breakfast
- **lunch** (object) - Meal details for lunch  
- **dinner** (object) - Meal details for dinner
- **snacks** (array) - Planned snacks for the day
- **daily_calorie_total** (integer) - Total calories for the day
- **daily_macro_totals** (object) - Total macros for the day
- **prep_time_total** (integer) - Total preparation time for the day

### **Customization Attributes:**
- **meal_swaps** (array) - Record of meals user has swapped
- **ingredient_substitutions** (array) - Ingredients user has substituted
- **leftover_planning** (array) - Planned use of leftovers
- **schedule_changes** (array) - Meals moved between days

---

## **Journey 6: Food and Calorie Tracking**

### **Food Database Attributes:**
- **food_id** (string) - Unique identifier for food item
- **food_name** (string) - Name of the food
- **brand_name** (string) - Brand name (if applicable)
- **barcode** (string) - Product barcode (if applicable)
- **serving_sizes** (array) - Available serving size options
- **calories_per_serving** (integer) - Calories per standard serving
- **macronutrients_per_serving** (object) - protein, carbs, fats, fiber per serving
- **micronutrients_per_serving** (object) - vitamins and minerals per serving
- **food_category** (string) - fruits, vegetables, grains, protein, etc.

### **Food Entry Attributes:**
- **entry_id** (string) - Unique identifier for food log entry
- **food_id** (string) - Reference to food in database
- **entry_date** (date) - Date the food was consumed
- **meal_type** (string) - breakfast, lunch, dinner, snack
- **quantity** (float) - Amount consumed
- **serving_unit** (string) - cups, grams, pieces, etc.
- **calories_consumed** (integer) - Calculated calories for the entry
- **macros_consumed** (object) - Calculated macronutrients consumed
- **entry_method** (string) - search, barcode, manual, recent
- **entry_timestamp** (datetime) - When the entry was logged

### **Daily Tracking Attributes:**
- **tracking_date** (date) - Date being tracked
- **daily_calorie_goal** (integer) - User's calorie target for the day
- **calories_consumed** (integer) - Total calories logged for the day
- **calories_remaining** (integer) - Remaining calories to reach goal
- **macro_goals** (object) - Daily macro targets
- **macros_consumed** (object) - Total macros logged for the day
- **macros_remaining** (object) - Remaining macros to reach goals
- **meal_breakdown** (object) - Calories/macros per meal type

### **Progress Tracking Attributes:**
- **weekly_average_calories** (integer) - Average daily calories over the week
- **weekly_trends** (object) - Trends in calories and macros over time
- **goal_adherence** (float) - Percentage of days meeting calorie goals
- **streak_days** (integer) - Consecutive days meeting goals
- **weight_progress** (array) - Weight tracking data (if user provides)

### **User Preferences Attributes:**
- **frequently_eaten_foods** (array) - Foods user logs often
- **recent_foods** (array) - Recently logged foods for quick access
- **custom_foods** (array) - User-created custom food entries
- **measurement_units** (string) - metric or imperial preference
- **notification_preferences** (object) - Reminder settings

---

## **Journey 7: Grocery Assistance**

### **Grocery List Attributes:**
- **list_id** (string) - Unique identifier for grocery list
- **list_name** (string) - Name of the grocery list
- **creation_date** (datetime) - When list was created
- **last_modified** (datetime) - When list was last updated
- **list_source** (string) - recipes, meal_plan, manual
- **total_estimated_cost** (float) - Estimated total cost of items
- **list_status** (string) - active, completed, archived

### **Grocery Item Attributes:**
- **item_id** (string) - Unique identifier for grocery item
- **item_name** (string) - Name of the ingredient/item
- **quantity** (float) - Amount needed
- **unit** (string) - measurement unit (cups, lbs, pieces, etc.)
- **category** (string) - produce, dairy, meat, pantry, etc.
- **aisle_number** (integer) - Store aisle where item is typically found
- **brand_preference** (string) - Specific brand user prefers
- **estimated_cost** (float) - Estimated cost per item
- **priority** (string) - essential, optional
- **purchase_status** (string) - pending, purchased, unavailable
- **notes** (string) - Additional notes about the item

### **List Management Attributes:**
- **consolidation_rules** (object) - Rules for combining duplicate ingredients
- **unit_conversion_table** (object) - Conversion factors between units
- **store_section_mapping** (object) - Mapping items to store sections
- **substitution_suggestions** (array) - Alternative items for unavailable products
- **store_layout** (object) - User's preferred store layout for optimization

### **Recipe Integration Attributes:**
- **source_recipe_ids** (array) - Recipes that contributed to the list
- **source_meal_plan_id** (string) - Meal plan that generated the list
- **ingredient_scaling** (object) - How quantities were adjusted from recipes
- **recipe_notes** (array) - Special notes from recipes about ingredients

### **Sharing and Export Attributes:**
- **shared_with** (array) - Email addresses list is shared with
- **export_format** (string) - email, text, print, app_integration
- **delivery_app_integration** (object) - Integration with grocery delivery services
- **collaborative_editing** (boolean) - Whether others can edit the list

---

## **Journey 8: Nutritional Food Profile (Macro & Micronutrient Lookup)**

### **Food Profile Attributes:**
- **food_id** (string) - Unique identifier for food item
- **food_name** (string) - Common name of the food
- **scientific_name** (string) - Scientific name (if applicable)
- **food_category** (string) - fruits, vegetables, grains, proteins, etc.
- **brand_name** (string) - Brand name for packaged foods
- **barcode** (string) - Product barcode for packaged items

### **Nutritional Data Attributes:**
- **serving_sizes** (array) - Standard serving size options
- **calories_per_100g** (integer) - Calories per 100 grams
- **macronutrients_per_100g** (object) - Detailed macro breakdown per 100g
  - protein_g (float)
  - total_carbs_g (float)  
  - dietary_fiber_g (float)
  - sugars_g (float)
  - total_fat_g (float)
  - saturated_fat_g (float)
  - trans_fat_g (float)
  - cholesterol_mg (float)
  - sodium_mg (float)

### **Micronutrient Attributes:**
- **vitamins_per_100g** (object) - Vitamin content per 100g
  - vitamin_a_mcg (float)
  - vitamin_c_mg (float)
  - vitamin_d_mcg (float)
  - vitamin_e_mg (float)
  - vitamin_k_mcg (float)
  - thiamine_mg (float)
  - riboflavin_mg (float)
  - niacin_mg (float)
  - vitamin_b6_mg (float)
  - folate_mcg (float)
  - vitamin_b12_mcg (float)

- **minerals_per_100g** (object) - Mineral content per 100g
  - calcium_mg (float)
  - iron_mg (float)
  - magnesium_mg (float)
  - phosphorus_mg (float)
  - potassium_mg (float)
  - zinc_mg (float)
  - copper_mg (float)
  - manganese_mg (float)
  - selenium_mcg (float)

### **Advanced Nutritional Attributes:**
- **amino_acid_profile** (object) - Essential amino acids (for proteins)
- **fatty_acid_profile** (object) - Omega-3, omega-6 breakdown (for fats)
- **glycemic_index** (integer) - GI value (if applicable)
- **antioxidant_content** (object) - ORAC values, polyphenols
- **allergen_information** (array) - Contains allergens like nuts, dairy, etc.

### **Comparison Attributes:**
- **similar_foods** (array) - Foods in the same category for comparison
- **healthier_alternatives** (array) - Foods with better nutritional profiles
- **brand_variations** (array) - Different brands of the same food type
- **seasonal_variations** (object) - Nutritional changes by season (for fresh foods)

### **User Interaction Attributes:**
- **custom_serving_size** (float) - User-defined serving size
- **daily_value_percentages** (object) - % of daily values for each nutrient
- **health_benefits** (array) - Known health benefits of the food
- **nutritional_highlights** (array) - Key nutritional strengths
- **dietary_fit** (object) - How well food fits user's dietary goals
- **portion_recommendations** (string) - Suggested portion sizes

### **Reference Data Attributes:**
- **data_source** (string) - USDA, brand database, etc.
- **last_updated** (date) - When nutritional data was last verified
- **data_quality** (string) - high, medium, low confidence level
- **preparation_method** (string) - raw, cooked, processed
- **storage_recommendations** (string) - How to store for optimal nutrition

---

## **Cross-Journey Shared Attributes**

### **User Profile Attributes:**
- **user_id** (string) - Unique user identifier
- **dietary_restrictions** (array) - Global dietary restrictions
- **food_allergies** (array) - Known food allergies
- **cuisine_preferences** (array) - Preferred cuisine types
- **cooking_skill_level** (string) - beginner, intermediate, advanced
- **daily_calorie_goal** (integer) - User's daily calorie target
- **macro_ratio_preferences** (object) - Preferred protein/carbs/fats ratios
- **ingredient_dislikes** (array) - Ingredients user wants to avoid
- **kitchen_equipment** (array) - Available cooking equipment
- **household_size** (integer) - Number of people user cooks for
- **budget_preferences** (object) - Daily/weekly food budget limits

### **Session State Attributes:**
- **session_id** (string) - Unique session identifier
- **current_journey** (string) - Which journey user is currently in
- **journey_history** (array) - Previous journeys in the session
- **saved_items** (array) - Items user has saved during session
- **context_data** (object) - Data carried between journeys

### **Integration Attributes:**
- **favorites** (array) - User's saved favorite recipes/foods
- **meal_plans** (array) - User's saved meal plans
- **grocery_lists** (array) - User's saved grocery lists
- **food_log_history** (array) - User's food tracking history
- **recipe_ratings** (array) - User's ratings for recipes
- **cooking_notes** (array) - User's personal cooking notes

---

*This comprehensive attribute list provides the foundation for building the chatbot's data models, conversation flow, and integration between different journeys.*