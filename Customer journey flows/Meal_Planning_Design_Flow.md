# 📅 Daily and Weekly Meal Planning Customer Journey - Design Flow Chart

---

## **Flow Overview**
This flowchart maps the complete Meal Planning journey from initial planning scope through personalized meal scheduling to finalized meal plans with grocery lists, including all decision points, nutritional balancing, and cross-journey transitions.

---

## **📊 Complete Design Flow Chart**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                 USER INTENT                                     │
│ "Create a meal plan for me" / "Plan my meals for the week"                     │
│                "Help me organize my eating schedule" / "Weekly meal prep"       │
│                          [ENTRY TRIGGER DETECTED]                              │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        STEP 1: PLANNING SCOPE DETERMINATION                    │
│                                                                                 │
│  Bot: "What would you like to plan?"                                           │
│                                                                                 │
│  [DECISION POINT 1: Planning Duration]                                         │
└─────┬──────────────┬────────────────┬───────────────────────────────────────────┘
      │              │                │
      ▼              ▼                ▼
┌───────────┐  ┌───────────────┐  ┌─────────────────────────────────────────┐
│ DAILY     │  │ WEEKLY        │  │ CUSTOM RANGE                            │
│ Single    │  │ 7-day plan    │  │ "Plan for 3 days" / "Next 2 weeks"     │
│ day plan  │  │               │  │                                         │
└─────┬─────┘  └─────┬─────────┘  └─────┬───────────────────────────────────┘
      │              │                  │
      ▼              ▼                  ▼
      │       ┌─────────────────┐       │
      │       │ SET DURATION    │       │
      │       │ days = 7        │       │
      │       └─────────────────┘       │
      │              │                  │
      └──────────────┴──────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         STEP 2: MEAL SCOPE SELECTION                           │
│                                                                                 │
│  Bot: "Which meals should I plan for each day?"                                │
│                                                                                 │
│  [DECISION POINT 2: Meal Coverage]                                             │
└─────┬────────┬────────┬────────┬──────────────────────────────────────────────┘
      │        │        │        │
      ▼        ▼        ▼        ▼
┌─────────┐ ┌─────┐ ┌─────────┐ ┌─────────────────────────────────────────┐
│All Meals│ │Main │ │Specific │ │ Custom Selection                        │
│B+L+D+S  │ │Meals│ │ Meals   │ │ "Only breakfast and lunch"              │
│         │ │B+L+D│ │ Only    │ │ "Dinner + snacks"                       │
└────┬────┘ └──┬──┘ └────┬────┘ └─────┬───────────────────────────────────┘
     │         │         │            │
     │         │         │            │
     └─────────┴─────────┴────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      STEP 3: PERSONAL PROFILE SETUP                            │
│                                                                                 │
│  Bot: "Let me get some details to create your perfect meal plan"               │
│                                                                                 │
│  [DECISION POINT 3: Profile Requirements]                                      │
└─────┬─────────────────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         CALORIE GOAL DETERMINATION                             │
│                                                                                 │
│  Bot: "What's your daily calorie target?"                                      │
│  • "I want to maintain my current weight" (calculate BMR + activity)          │
│  • "I have a specific goal: [X] calories per day"                             │
│  • "Help me determine my calorie needs"                                       │
│                                                                                 │
│  Default Distribution:                                                         │
│  • Breakfast: 25% of daily calories                                           │
│  • Lunch: 30% of daily calories                                               │
│  • Dinner: 35% of daily calories                                              │
│  • Snacks: 10% of daily calories                                              │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        DIETARY PREFERENCES COLLECTION                          │
│                                                                                 │
│  Bot: "Any dietary restrictions or preferences?"                               │
│                                                                                 │
│  Available from meal_suggestions_raw.json dietary_tags:                        │
│  • Diet Types: vegetarian, vegan, keto_friendly, mediterranean                 │
│  • Health Focus: heart_healthy, high_protein, high_fiber, low_carb            │
│  • Restrictions: gluten_free, dairy_free, nut_free                            │
│  • Special Needs: omega_3, anti_inflammatory, probiotic                       │
│                                                                                 │
│  [COLLECT DIETARY FILTERS]                                                     │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          LIFESTYLE CONSTRAINTS                                 │
│                                                                                 │
│  Bot: "Tell me about your cooking preferences"                                 │
│                                                                                 │
│  • Cooking Skill Level: "Beginner" / "Intermediate" / "Advanced"              │
│  • Time Constraints: "Quick meals only" / "I have time to cook"               │
│  • Batch Cooking: "I like meal prep" / "I cook fresh daily"                   │
│  • Number of People: 1-8+ servings per meal                                   │
│  • Kitchen Equipment: Basic / Full kitchen / Limited equipment                │
│                                                                                 │
│  Prep Time Preferences (from meal_suggestions_raw.json):                       │
│  • Quick: ≤15 minutes                                                         │
│  • Moderate: 15-30 minutes                                                    │
│  • Extended: 30+ minutes                                                      │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        STEP 4: MEAL PLAN GENERATION                            │
│                                                                                 │
│  Initialize Planning Algorithm:                                                │
│  • total_days = selected duration                                             │
│  • meals_per_day = selected meal types                                        │
│  • daily_calorie_target = user goal                                           │
│  • dietary_filters = user restrictions                                        │
│  • prep_time_limit = user preference                                          │
│                                                                                 │
│  For each day in total_days:                                                  │
│    For each meal_type in meals_per_day:                                       │
│      target_calories = daily_target × meal_percentage                         │
│      Search meal_suggestions_raw.json WHERE:                                  │
│        calories BETWEEN (target_calories ± 75)                                │
│        AND meal_type CONTAINS current_meal_type                               │
│        AND dietary_tags CONTAINS ALL user_dietary_filters                    │
│        AND prep_time ≤ user_time_constraint                                   │
│      Apply variety algorithm (avoid duplicate meals within 2 days)            │
│      Select optimal meal based on nutrition balance                           │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           NUTRITION BALANCING                                  │
│                                                                                 │
│  Balance macronutrients across the planning period:                           │
│                                                                                 │
│  Daily Targets:                                                                │
│  • Protein: 20-35% of calories                                                │
│  • Carbohydrates: 45-65% of calories                                          │
│  • Fats: 20-35% of calories                                                   │
│  • Fiber: 25-35g daily                                                        │
│                                                                                 │
│  Weekly Optimization:                                                          │
│  • Variety Score: Ensure 15+ different foods per week                         │
│  • Nutrient Density: Prioritize high-nutrition meals                          │
│  • Cuisine Diversity: Mix different cooking styles                            │
│  • Prep Time Distribution: Balance quick vs. involved meals                   │
│                                                                                 │
│  Rebalancing Algorithm:                                                        │
│  IF daily_protein < target: prioritize high_protein meals next                │
│  IF variety_score < threshold: force different cuisine/ingredients            │
│  IF prep_time > weekly_limit: swap for quicker alternatives                   │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         STEP 5: MEAL PLAN DISPLAY                              │
│                                                                                 │
│  Present generated meal plan in structured format:                            │
│                                                                                 │
│  📅 DAY-BY-DAY LAYOUT:                                                         │
│  Monday:                                                                       │
│    🌅 Breakfast: [meal_name] - [calories]cal ([prep_time]min)                  │
│    🌞 Lunch: [meal_name] - [calories]cal ([prep_time]min)                      │
│    🌙 Dinner: [meal_name] - [calories]cal ([prep_time]min)                     │
│    🍎 Snack: [meal_name] - [calories]cal ([prep_time]min)                      │
│    📊 Daily Total: [total_calories]cal                                         │
│                                                                                 │
│  Tuesday: [similar format]                                                    │
│  ...                                                                          │
│                                                                                 │
│  📈 WEEKLY NUTRITION SUMMARY:                                                  │
│  • Average daily calories: [X]                                                │
│  • Protein: [X]g avg ([Y]% of calories)                                       │
│  • Carbs: [X]g avg ([Y]% of calories)                                         │
│  • Fat: [X]g avg ([Y]% of calories)                                           │
│  • Fiber: [X]g avg                                                            │
│  • Prep time total: [X] hours/week                                            │
│                                                                                 │
│  📊 NUTRITIONAL ANALYSIS:                                                      │
│  • Daily calorie distribution                                                 │
│  • Macro balance visualization                                                │
│  • Nutrient goal tracking                                                     │
│  • ⚠️ RECOMMENDATIONS:                                                         │
│    - "Consider adding more protein on Wednesday"                              │
│    - "Your fiber intake is excellent!"                                        │
│    - "Try to include more omega-3 rich foods"                                 │
│                                                                                 │
│  [DECISION POINT 4: Plan Acceptance]                                           │
│  "How does this meal plan look?"                                              │
└─────┬──────┬──────┬─────────────────────────────────────────────────────────────┘
      │      │      │
      ▼      ▼      ▼
   ┌─────┐ ┌────┐ ┌─────────────┐
   │App- │ │Reg-│ │ Complete    │
   │rove │ │en- │ │ Rebuild     │
   │Plan │ │er- │ │             │
   └──┬──┘ └─┬──┘ └──────┬──────┘
      │      │      │           │
      ▼      ▼      ▼           ▼
      │      │      │     ┌─────────────┐
      │      │      │     │ RESTART     │
      │      │      │     │ GENERATION  │
      │      │      │     │ New criteria│
      │      │      │     │ or          │
      │      │      │     │ preferences │
      │      │      │     └─────────────┘
      │      │      │
      │      ▼      ▼
      │      │ ┌─────────────┐
      │      │ │ REGENERATE  │
      │      │ │ WITH NEW    │
      │      │ │ PARAMETERS  │
      │      │ └─────────────┘
      │      │
      ▼      ▼ [Proceed directly to Final Action Selection]
      │      │
      └──────┴──────────────────────────────┐
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        STEP 6: FINAL ACTION SELECTION                          │
│                                                                                 │
│  Bot: "Your meal plan is ready! What would you like to do next?"              │
│                                                                                 │
│  [DECISION POINT 5: Final Actions]                                             │
└─────┬──────┬──────┬──────┬─────────────────────────────────────────────────────┘
      │      │      │      │
      ▼      ▼      ▼      ▼
   ┌─────┐ ┌────┐ ┌────┐ ┌─────────────┐
   │Gene-│ │Exp-│ │Dow-│ │ Start       │
   │rate │ │ort │ │nlo-│ │ Cooking     │
   │Groc-│ │Plan│ │ad  │ │ First Meal  │
   │ery  │ │    │ │ICS │ │             │
   │List │ │    │ │File│ │             │
   └──┬──┘ └─┬──┘ └─┬──┘ └──────┬──────┘
      │      │      │           │
      ▼      ▼      ▼           ▼

┌─────────────────────────────────────────────────────────────────────────────────┐
│                             ENDPOINT ACTIONS                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ GENERATE CONSOLIDATED GROCERY LIST                              │
    │                                                                 │
    │ Process:                                                        │
    │ 1. Extract all meal.components from finalized meal plan        │
    │ 2. Cross-reference with foods_nutrition_raw.json for details   │
    │ 3. Aggregate quantities for duplicate ingredients:              │
    │    Example: 3 meals need "spinach" = sum all amounts needed    │
    │ 4. Organize by food categories:                                 │
    │    • Proteins (chicken, fish, tofu, eggs)                      │
    │    • Vegetables (leafy greens, root vegetables, etc.)          │
    │    • Grains & Starches (quinoa, rice, potatoes)                │
    │    • Pantry Items (oils, spices, condiments)                   │
    │    • Dairy & Alternatives                                       │
    │ 5. Add portion buffers (10% extra for cooking losses)          │
    │ 6. Include prep day suggestions for batch cooking               │
    │                                                                 │
    │ Output Format:                                                  │
    │ "🛒 GROCERY LIST - Week of [Date]"                              │
    │ "🥩 PROTEINS:"                                                  │
    │ "  • Chicken breast - 2.5 lbs"                                 │
    │ "  • Salmon fillets - 1 lb"                                    │
    │ "🥬 VEGETABLES:"                                                 │
    │ "  • Spinach - 300g"                                            │
    │ "  • Cherry tomatoes - 500g"                                    │
    │                                                                 │
    │ [TRANSITION 1: To Grocery Assistance Journey]                   │
    │ Pass: consolidated_list, meal_context, dietary_preferences     │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ EXPORT MEAL PLAN                                                │
    │                                                                 │
    │ Export Formats Available:                                       │
    │ 📧 EMAIL VERSION:                                               │
    │ • PDF attachment with daily meal schedules                     │
    │ • Grocery list included                                         │
    │ • Nutrition summary charts                                      │
    │ • Prep time estimates                                           │
    │                                                                 │
    │ 🗓️ CALENDAR INTEGRATION:                                        │
    │ • Create calendar events for each meal                          │
    │ • Include prep time blocks                                      │
    │ • Add grocery shopping reminders                                │
    │ • Set meal prep day events                                      │
    │                                                                 │
    │ 📱 MOBILE-FRIENDLY FORMAT:                                       │
    │ • Daily checklist view                                          │
    │ • Ingredient checkoff lists                                     │
    │ • Quick meal swap options                                       │
    │ • Progress tracking                                             │
    │                                                                 │
    │ [ENDPOINT 1: Plan Successfully Exported]                        │
    │ Bot: "Meal plan sent to your email/calendar!"                  │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ DOWNLOAD ICS CALENDAR FILE                                      │
    │                                                                 │
    │ ICS File Generation:                                            │
    │ For each meal in the plan:                                      │
    │ • Event title: "🍽️ [Meal Name] ([prep_time] min)"              │
    │ • Time: User's preferred meal times                             │
    │ • Description: Ingredient list + basic instructions            │
    │ • Location: Kitchen/Home                                        │
    │ • Reminders: 30 min before for prep                            │
    │                                                                 │
    │ Additional Calendar Events:                                     │
    │ • "🛒 Grocery Shopping" (day before start)                      │
    │ • "🥘 Meal Prep Day" (if batch cooking selected)               │
    │ • "📋 Weekly Menu Review" (end of week)                         │
    │                                                                 │
    │ File Format: Standard ICS format compatible with:              │
    │ • Google Calendar                                               │
    │ • Apple Calendar                                                │
    │ • Outlook                                                       │
    │ • Any ICS-compatible calendar app                               │
    │                                                                 │
    │ [ENDPOINT 2: ICS File Downloaded]                               │
    │ Bot: "Calendar file downloaded! Import it to your calendar."   │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ START COOKING FIRST MEAL                                        │
    │                                                                 │
    │ Process:                                                        │
    │ 1. Identify first meal in plan (typically tomorrow's breakfast) │
    │ 2. Check if detailed recipe exists in recipes_raw.json         │
    │ 3. Extract meal components and portions                         │
    │ 4. Prepare ingredient list for immediate cooking               │
    │ 5. Transfer to Cooking Guidance Journey                         │
    │                                                                 │
    │ Context Transfer:                                               │
    │ • Selected meal object                                          │
    │ • Portion scaling (number of people)                           │
    │ • Dietary restrictions                                          │
    │ • User skill level                                              │
    │ • Available prep time                                           │
    │                                                                 │
    │ If Recipe Not Available:                                        │
    │ • Use meal.components for basic guidance                       │
    │ • Create simple preparation instructions                        │
    │ • Offer to add detailed recipe later                           │
    │                                                                 │
    │ [TRANSITION 2: To Cooking Guidance Journey]                     │
    │ Pass: first_meal, meal_plan_context, user_preferences         │
    └─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                         ADDITIONAL CROSS-JOURNEY TRANSITIONS                   │
└─────────────────────────────────────────────────────────────────────────────────┘

    FROM STEP 8 - Extended Action Options:

    ┌─────────────────────────────────────────────────────────────────┐
    │ MEAL PLAN TRACKING                                              │
    │ • Set up daily meal logging                                     │
    │ • Track actual vs planned consumption                           │
    │ • Monitor adherence to nutrition goals                          │
    │ • Record meal satisfaction ratings                              │
    │                                                                 │
    │ [TRANSITION 3: To Food Tracking Journey]                        │
    │ Pass: planned_meals, target_nutrition, schedule               │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ NUTRITIONAL DEEP DIVE                                           │
    │ • Analyze specific nutrients in meal plan                       │
    │ • Compare with dietary guidelines                               │
    │ • Identify nutritional gaps or excesses                         │
    │ • Get recommendations for improvement                           │
    │                                                                 │
    │ [TRANSITION 4: To Nutritional Lookup Journey]                   │
    │ Pass: weekly_nutrition_summary, specific_nutrients             │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ RECIPE DISCOVERY FOR GAPS                                       │
    │ • Identify missing cuisine types in plan                        │
    │ • Find recipes that complement current selection                │
    │ • Discover new meals meeting same dietary criteria              │
    │                                                                 │
    │ [TRANSITION 5: To Recipe Discovery Journey]                     │
    │ Pass: current_meal_plan, gap_analysis, preferences            │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ EVENT PLANNING EXTENSION                                        │
    │ • "I have a dinner party this Saturday"                        │
    │ • Integrate special event meals into regular meal plan         │
    │ • Adjust weekly nutrition to accommodate special occasions     │
    │                                                                 │
    │ [TRANSITION 6: To Event Planning Journey]                       │
    │ Pass: current_plan, event_details, remaining_week_balance      │
    └─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                               ERROR HANDLING FLOWS                             │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ INSUFFICIENT MEAL OPTIONS                                       │
    │ • Not enough meals match dietary restrictions + calorie goals  │
    └─────┬───────────────────────────────────────────────────────────┘
          │
          ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │ [DECISION POINT: Constraint Relaxation]                        │
    │ Bot: "I'm having trouble finding enough variety. Let's adjust."│
    └─────┬──────┬──────┬─────────────────────────────────────────────┘
          │      │      │
          ▼      ▼      ▼
    ┌─────────┐ ┌────┐ ┌─────────────────────────────────────────┐
    │ EXPAND  │ │REL-│ │ PARTIAL PLAN + CUSTOM MEALS             │
    │ CALORIE │ │AX  │ │ Generate partial plan + suggest         │
    │ RANGES  │ │DI- │ │ custom meals for remaining slots        │
    │ ±100 cal│ │ETARY│ │                                         │
    │         │ │REQ │ │                                         │
    └────┬────┘ └─┬──┘ └─────────────────┬───────────────────────┘
         │        │                      │
         ▼        ▼                      ▼
    [RETRY GENERATION WITH RELAXED CONSTRAINTS]

    ┌─────────────────────────────────────────────────────────────────┐
    │ NUTRITIONAL IMBALANCE WARNING                                   │
    │ • Generated plan doesn't meet nutritional guidelines           │
    │ • Macro ratios outside healthy ranges                          │
    │ • Critical nutrient deficiencies detected                      │
    │                                                                 │
    │ Resolution:                                                     │
    │ • Highlight nutritional concerns to user                       │
    │ • Suggest specific meal swaps to improve balance               │
    │ • Offer to prioritize nutrition over other preferences         │
    │ • Provide educational content about balanced nutrition         │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ EXCESSIVE PREP TIME WARNING                                     │
    │ • Total weekly prep time exceeds user constraints              │
    │ • Daily cooking time unrealistic for lifestyle                 │
    │                                                                 │
    │ Auto-Resolution:                                                │
    │ • Swap complex meals for simpler alternatives                  │
    │ • Suggest batch cooking strategies                              │
    │ • Recommend meal prep day scheduling                           │
    │ • Offer partially prepared ingredient options                  │
    └─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              ENDPOINT SUMMARY                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

    ENDPOINT 1: Plan Successfully Exported
    ├─ User has complete meal plan
    ├─ Multiple export formats available
    └─ Ready for independent execution

    ENDPOINT 2: ICS File Downloaded
    ├─ Calendar file ready for import
    ├─ Compatible with all major calendar apps
    └─ Meal schedule and reminders included

    TRANSITION 1: To Grocery Assistance Journey
    ├─ Consolidated shopping list ready
    ├─ Ingredient procurement facilitated
    └─ Meal preparation supported

    TRANSITION 2: To Cooking Guidance Journey
    ├─ First meal ready to cook
    ├─ Step-by-step guidance initiated
    └─ Meal plan execution started

    TRANSITION 3: To Food Tracking Journey
    ├─ Planned vs actual tracking setup
    ├─ Nutrition goal monitoring
    └─ Long-term health insights

    TRANSITION 4: To Nutritional Lookup Journey
    ├─ Deep nutritional analysis
    ├─ Educational content access
    └─ Plan optimization insights

    TRANSITION 5: To Recipe Discovery Journey
    ├─ Cuisine gap identification
    ├─ Meal variety expansion
    └─ Preference refinement

    TRANSITION 6: To Event Planning Journey
    ├─ Special occasion integration
    ├─ Event-aware meal planning
    └─ Social dining coordination

    ERROR EXITS:
    ├─ Insufficient options → Constraint relaxation
    ├─ Nutritional imbalance → Plan rebalancing
    ├─ Time constraints → Meal simplification
    └─ System errors → Graceful degradation

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            DATA DEPENDENCIES                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

    FROM meal_suggestions_raw.json:
    ├─ meal.calories → Calorie target alignment
    ├─ meal.meal_type → Daily schedule placement
    ├─ meal.prep_time → Time constraint management
    ├─ meal.components[] → Ingredient aggregation
    ├─ meal.nutrition{} → Daily nutrition balancing
    ├─ meal.dietary_tags[] → Restriction compliance
    └─ meal.id → Plan uniqueness and variety

    FROM foods_nutrition_raw.json:
    ├─ food.calories → Component calorie calculations
    ├─ food.per_100g → Nutritional density analysis
    ├─ food.category → Food group balancing
    ├─ food.vitamins_per_100g → Micronutrient optimization
    ├─ food.minerals_per_100g → Essential nutrient coverage
    └─ food.dietary_tags → Ingredient-level filtering

    FROM recipes_raw.json:
    ├─ recipe.cuisine → Cuisine variety scoring
    ├─ recipe.difficulty → Skill level matching
    ├─ recipe.total_time → Realistic time planning
    ├─ recipe.servings → Portion scaling calculations
    └─ recipe.ingredients[] → Cross-referencing with meals

    CALCULATED METRICS:
    ├─ weekly_variety_score → Unique ingredients count
    ├─ macro_balance_score → Daily and weekly balance
    ├─ prep_time_distribution → Time management feasibility
    ├─ nutrient_density_score → Overall nutritional quality
    ├─ dietary_compliance_score → Restriction adherence
    └─ ingredient_overlap_score → Shopping efficiency

    USER PROFILE DATA (required for personalization):
    ├─ daily_calorie_target → Meal calorie distribution
    ├─ dietary_restrictions → Filtering criteria
    ├─ cooking_skill_level → Recipe complexity limits
    ├─ time_constraints → Prep time boundaries  
    ├─ household_size → Portion scaling factors
    ├─ cuisine_preferences → Variety weighting
    ├─ meal_timing_preferences → Schedule optimization
    └─ previous_meal_plans → Learning and improvement

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FLOW STATISTICS                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

    Total Decision Points: 6
    ├─ Planning duration (daily/weekly/custom)
    ├─ Meal coverage (all meals/main meals/specific)
    ├─ Profile setup (calorie goals, restrictions, lifestyle)
    ├─ Plan acceptance (approve/customize/regenerate)
    ├─ Customization type (swap/rearrange/substitute/leftover)
    └─ Final actions (export/save/calendar/cook)

    Possible Endpoints: 3
    ├─ Direct completion (exported/saved/scheduled)
    ├─ Cross-journey transitions (6 different journeys)
    └─ Error handling with constraint relaxation

    Planning Complexity Levels:
    ├─ Simple daily plan: 4-6 minutes
    ├─ Weekly plan with customization: 12-18 minutes
    ├─ Multi-week with constraints: 20-30 minutes
    └─ Family meal planning: 25-35 minutes

    Database Query Efficiency:
    ├─ Initial meal selection: O(n) where n = meal database size
    ├─ Variety algorithm: O(n²) for duplicate avoidance
    ├─ Nutrition balancing: O(mn) where m = days, n = meals per day
    ├─ Ingredient aggregation: O(k) where k = total components
    └─ Template storage: O(1) constant time operations

    Meal Plan Coverage:
    ├─ Daily plans: 1-3 days optimal
    ├─ Weekly plans: 7-14 days standard
    ├─ Extended plans: 14-28 days maximum
    ├─ Meal variety: 15+ unique meals per week target
    └─ Ingredient diversity: 30+ unique ingredients optimal

    Customization Success Rates:
    ├─ Meal swaps: 95% success rate (50 meal options)
    ├─ Dietary filtering: 100% compliance possible
    ├─ Calorie targeting: ±75 calorie accuracy
    ├─ Prep time management: ±10 minute accuracy
    └─ Nutritional balancing: 85% within guidelines

This comprehensive flowchart covers the complete meal planning experience, from scope determination through personalized plan generation to final implementation, with robust customization options and seamless integration with all other customer journeys.
```
