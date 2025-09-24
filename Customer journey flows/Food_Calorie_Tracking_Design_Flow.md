r# 📊 Food and Calorie Tracking Customer Journey - Design Flow Chart

---

## **Flow Overview**
This flowchart maps the complete Food and Calorie Tracking journey from initial food entry through comprehensive nutritional analysis to goal achievement insights, including all decision points, progress monitoring, and cross-journey transitions.

---

## **📊 Complete Design Flow Chart**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                 USER INTENT                                     │
│ "Log my food for today" / "Track what I just ate" / "Show my food diary"       │
│ "Add this to my calories" / "How many calories have I eaten?" / "Log breakfast" │
│                          [ENTRY TRIGGER DETECTED]                              │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        STEP 1: TRACKING MODE DETERMINATION                     │
│                                                                                 │
│  Bot: "What would you like to do with food tracking today?"                    │
│                                                                                 │
│  [DECISION POINT 1: Tracking Action Type]                                      │
└─────┬──────────────┬────────────────┬───────────────────────────────────────────┘
      │              │                │
      ▼              ▼                ▼
┌───────────┐  ┌───────────────┐  ┌─────────────────────────────────────────┐
│ LOG NEW   │  │ VIEW DIARY    │  │ MANAGE EXISTING LOGS                    │
│ FOOD      │  │ & PROGRESS    │  │ Edit/delete previous entries            │
│           │  │               │  │                                         │
└─────┬─────┘  └─────┬─────────┘  └─────┬───────────────────────────────────┘
      │              │                  │
      ▼              ▼                  ▼
      │       ┌─────────────────┐       │
      │       │ DISPLAY CURRENT │       │
      │       │ DAILY STATUS    │       │
      │       │ AND TOTALS      │       │
      │       └─────────────────┘       │
      │              │                  │
      └──────────────┴──────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         FOOD ENTRY WORKFLOW                                    │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ STEP 2: FOOD ENTRY METHOD SELECTION                            │
    │                                                                 │
    │ Bot: "How would you like to add your food?"                    │
    │                                                                 │
    │ [DECISION POINT 2: Food Entry Method]                          │
    └─────┬──────────┬──────────┬─────────────────────────────────────┘
          │          │          │
          ▼          ▼          ▼
    ┌─────────┐ ┌─────────┐ ┌─────────────────────────────────────┐
    │ TEXT    │ │ MANUAL  │ │ RECENT FOODS                        │
    │ SEARCH  │ │ ENTRY   │ │ Quick select from history           │
    │         │ │         │ │                                     │
    │         │ │         │ │                                     │
    └────┬────┘ └────┬────┘ └─────────────────┬───────────────────┘
         │           │                        │
         ▼           ▼                        ▼
         │           │                        │
         │           │                        │
         │           │                        │
         ▼        ▼      ▼                      │
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         FOOD SEARCH & IDENTIFICATION                           │
│                                                                                 │
│  TEXT SEARCH PATH:                                                             │
│  • User input: "grilled chicken" or "apple" or "Greek yogurt"                 │
│  • Search foods_nutrition_raw.json by food.name                               │
│  • Use grocery_support_raw.json ingredient_aliases for matching              │
│  • Return ranked results by relevance and popularity                          │
│                                                                                 │
│  Example Search Process:                                                       │
│  User: "chicken breast"                                                        │
│  1. Direct match: food_001 "grilled chicken breast"                           │
│  2. Alias match: "chicken_breast" → ["chicken breast", "grilled chicken"]     │
│  3. Category match: protein → poultry foods                                   │
│                                                                                 │
│  MANUAL ENTRY PATH:                                                            │
│  • User provides: food name, calories, basic macros                           │
│  • Create temporary food entry for this session                               │
│  • Option to save as custom food for future use                               │
│                                                                                 │
│  RECENT FOODS PATH:                                                            │
│  • Display last 20 logged foods from user history                             │
│  • Show with most common portion sizes                                        │
│  • Enable quick re-logging with one tap                                       │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         STEP 3: FOOD SEARCH RESULTS                            │
│                                                                                 │
│  Display matching foods from foods_nutrition_raw.json:                        │
│                                                                                 │
│  🍗 Search Results for "chicken breast":                                       │
│                                                                                 │
│  1. Grilled Chicken Breast (food_001)                                         │
│     165 calories per 100g | 31g protein, 0g carbs, 4g fat                    │
│     Categories: protein, poultry                                               │
│                                                                                 │
│  2. Chicken Breast (generic, cooked)                                          │
│     185 calories per 100g | 29g protein, 0g carbs, 7g fat                    │
│     Categories: protein, poultry                                               │
│                                                                                 │
│  3. Raw Chicken Breast                                                        │
│     155 calories per 100g | 23g protein, 0g carbs, 6g fat                    │
│     Categories: protein, poultry, raw                                          │
│                                                                                 │
│  [DECISION POINT 3: Food Selection]                                            │
│  "Which food matches what you ate?"                                            │
└─────┬─────────────────────────────────────────────────────────────────────────────┘
      │
      ▼ [User selects specific food]
      │
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          STEP 4: PORTION SIZE SELECTION                        │
│                                                                                 │
│  Selected: Grilled Chicken Breast (food_001)                                  │
│  Nutrition per 100g: 165 cal, 31g protein, 0g carbs, 4g fat                   │
│                                                                                 │
│  Bot: "How much did you eat?"                                                  │
│                                                                                 │
│  PORTION SELECTION OPTIONS:                                                    │
│  📏 Standard Servings:                                                         │
│  • 1 small breast (85g) = 140 calories                                        │
│  • 1 medium breast (120g) = 198 calories                                      │
│  • 1 large breast (150g) = 248 calories                                       │
│                                                                                 │
│  ⚖️ Weight-Based:                                                              │
│  • Enter weight in grams/ounces                                               │
│  • Auto-calculate nutrition proportionally                                     │
│                                                                                 │
│  🥄 Volume-Based (where applicable):                                           │
│  • Cups, tablespoons, pieces                                                  │
│  • Use grocery_support_raw.json conversions                                   │
│                                                                                 │
│  🔢 Custom Amount:                                                             │
│  • "About half of what I usually eat"                                         │
│  • Percentage-based scaling                                                   │
│                                                                                 │
│  [DECISION POINT 4: Portion Specification]                                     │
│  User selects: "1 medium breast (120g)"                                       │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           STEP 5: MEAL ASSIGNMENT                              │
│                                                                                 │
│  Bot: "When did you eat this?"                                                │
│                                                                                 │
│  [DECISION POINT 5: Meal Timing]                                              │
└─────┬──────┬──────┬──────┬─────────────────────────────────────────────────────┘
      │      │      │      │
      ▼      ▼      ▼      ▼
   ┌─────┐ ┌────┐ ┌────┐ ┌─────────────┐
   │Brea-│ │Lun-│ │Din-│ │ Snack       │
   │kfast│ │ch  │ │ner │ │             │
   └──┬──┘ └─┬──┘ └─┬──┘ └──────┬──────┘
      │      │      │           │
      │      │      │           │
      └──────┴──────┴───────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         STEP 6: NUTRITION CALCULATION                          │
│                                                                                 │
│  Calculate nutritional impact for selected portion:                           │
│                                                                                 │
│  📊 IMMEDIATE CALCULATION:                                                      │
│  Selected: 120g Grilled Chicken Breast                                        │
│  • Calories: 165 × (120÷100) = 198 calories                                   │
│  • Protein: 31 × (120÷100) = 37.2g                                            │
│  • Carbs: 0 × (120÷100) = 0g                                                  │
│  • Fat: 4 × (120÷100) = 4.8g                                                  │
│  • Fiber: 0g                                                                   │
│                                                                                 │
│  🎯 DAILY IMPACT ANALYSIS:                                                     │
│  Adding to Lunch:                                                             │
│  • Previous lunch total: 320 calories → New total: 518 calories              │
│  • Daily progress: 847 calories → New total: 1,045 calories                  │
│  • Remaining to goal (2,000 cal): 955 calories                               │
│                                                                                 │
│  📈 MACRO IMPACT:                                                              │
│  Daily protein: 45g → 82.2g (164% of 50g goal) ✅ EXCEEDING                  │
│  Daily carbs: 125g → 125g (42% of 300g goal)                                 │
│  Daily fat: 35g → 39.8g (60% of 67g goal)                                    │
│                                                                                 │
│  ⚠️ GOAL ALERTS:                                                               │
│  • "Great protein choice! You're exceeding your daily protein goal."         │
│  • "You have 955 calories left for the day."                                  │
│  • "Consider adding some carbs to balance your macros."                       │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           STEP 7: ENTRY CONFIRMATION                           │
│                                                                                 │
│  📝 LOG ENTRY SUMMARY:                                                         │
│  Food: Grilled Chicken Breast                                                 │
│  Amount: 120g (1 medium breast)                                               │
│  Meal: Lunch                                                                  │
│  Time: [Current time] or [User specified]                                     │
│  Nutrition: 198 cal, 37g protein, 0g carbs, 5g fat                            │
│                                                                                 │
│  [DECISION POINT 6: Entry Actions]                                            │
│  "Does this look correct?"                                                     │
└─────┬──────┬──────┬──────┬─────────────────────────────────────────────────────┘
      │      │      │      │
      ▼      ▼      ▼      ▼
   ┌─────┐ ┌────┐ ┌────┐ ┌─────────────┐
   │Conf-│ │Adj-│ │Add │ │ Cancel      │
   │irm  │ │ust │ │Not-│ │ Entry       │
   │& Log│ │Por-│ │es  │ │             │
   │     │ │tion│ │    │ │             │
   └──┬──┘ └─┬──┘ └─┬──┘ └──────┬──────┘
      │      │      │           │
      ▼      ▼      ▼           ▼
      │      │      │           │
      │      │      │     [RETURN TO ENTRY METHOD]
      │      │      │           
      │      ▼      ▼           
      │ [RETURN TO PORTION SELECTION WITH ADJUSTMENTS]
      │      
      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            STEP 8: FOOD LOG UPDATE                             │
│                                                                                 │
│  Add confirmed entry to user's daily food log:                                │
│                                                                                 │
│  💾 DATABASE UPDATE:                                                           │
│  • Create new food_log_entry with timestamp                                   │
│  • Link to food_id from foods_nutrition_raw.json                              │
│  • Store actual portion consumed                                              │
│  • Record calculated nutritional values                                       │
│  • Assign to meal category and date                                           │
│                                                                                 │
│  🔄 DAILY TOTALS RECALCULATION:                                                │
│  • Update daily calorie total                                                 │
│  • Recalculate macro percentages                                              │
│  • Update progress toward daily goals                                         │
│  • Check for goal achievements or warnings                                    │
│                                                                                 │
│  ✅ CONFIRMATION MESSAGE:                                                      │
│  "✅ Logged: Grilled Chicken Breast (198 cal) to Lunch"                       │
│  "📊 Daily total: 1,045 calories (52% of 2,000 goal)"                        │
│  "🎯 955 calories remaining for today"                                        │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         STEP 9: DAILY SUMMARY DISPLAY                          │
│                                                                                 │
│  Present comprehensive daily nutrition summary:                               │
│                                                                                 │
│  📅 TODAY'S FOOD DIARY - [Current Date]                                        │
│                                                                                 │
│  🌅 BREAKFAST (285 calories):                                                   │
│  • Greek Yogurt Berry Parfait - 245 cal                                       │
│  • Coffee with milk - 40 cal                                                  │
│                                                                                 │
│  🌞 LUNCH (518 calories):                                                       │
│  • Quinoa Power Bowl - 320 cal                                                │
│  • Grilled Chicken Breast - 198 cal ⬅️ JUST ADDED                           │
│                                                                                 │
│  🌙 DINNER (0 calories):                                                        │
│  • [No entries yet]                                                           │
│                                                                                 │
│  🍎 SNACKS (242 calories):                                                      │
│  • Apple with almond butter - 185 cal                                         │
│  • Green tea - 0 cal                                                          │
│  • Mixed nuts - 57 cal                                                        │
│                                                                                 │
│  📊 DAILY TOTALS:                                                              │
│  🔥 Calories: 1,045 / 2,000 (52%) [955 remaining]                            │
│  💪 Protein: 82g / 50g (164%) ✅ GOAL EXCEEDED                                │
│  🌾 Carbs: 125g / 300g (42%)                                                  │
│  🥑 Fat: 40g / 67g (60%)                                                       │
│  🥬 Fiber: 28g / 25g (112%) ✅ GOAL EXCEEDED                                  │
│                                                                                 │
│  📈 PROGRESS VISUALIZATION:                                                     │
│  Calories:  ████████████░░░░░░░░░░░ 52%                                       │
│  Protein:   ████████████████████████ 164% ✅                                  │
│  Carbs:     ████████░░░░░░░░░░░░░░░░░ 42%                                      │
│  Fat:       ████████████░░░░░░░░░░░░░ 60%                                      │
│                                                                                 │
│  [DECISION POINT 7: Next Actions]                                              │
│  "What would you like to do next?"                                            │
└─────┬──────┬─────────────────────────────────────────────────────────────────────┘
      │      │
      ▼      ▼
   ┌─────┐ ┌─────────────┐
   │Add  │ │ View        │
   │More │ │ Progress    │
   │Food │ │ Trends      │
   │     │ │             │
   │     │ │             │
   │     │ │             │
   └──┬──┘ └──────┬──────┘
      │           │
      ▼           ▼
      │           │
      │           │
      │           │
      ▼           ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           ADVANCED TRACKING FEATURES                           │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ FOOD LOG MANAGEMENT                                             │
    │                                                                 │
    │ Edit Existing Entries:                                          │
    │ • "Change portion size of breakfast yogurt"                     │
    │ • Update quantities and recalculate nutrition                   │
    │ • Modify meal timing or category                                │
    │                                                                 │
    │ Delete Entries:                                                 │
    │ • "Remove the afternoon snack"                                  │
    │ • Adjust daily totals automatically                             │
    │ • Confirm deletion to prevent accidents                         │
    │                                                                 │
    │ Copy Meals:                                                     │
    │ • "Repeat yesterday's breakfast"                                │
    │ • "Use last week's lunch combo"                                 │
    │ • Enable quick logging of regular meals                         │
    │                                                                 │
    │ Meal Templates:                                                 │
    │ • Save frequent meal combinations                               │
    │ • "My usual breakfast" quick entry                              │
    │ • Custom meal building and saving                               │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ WEEKLY TRENDS & INSIGHTS                                        │
    │                                                                 │
    │ 📈 WEEKLY OVERVIEW:                                             │
    │ Monday: 1,890 cal (95% of goal)                                 │
    │ Tuesday: 2,150 cal (108% of goal) ⚠️                           │
    │ Wednesday: 1,045 cal (52% of goal - TODAY)                     │
    │ Thursday: [Planned]                                             │
    │ ...                                                             │
    │                                                                 │
    │ 📊 WEEKLY AVERAGES:                                             │
    │ • Average daily calories: 1,695                                │
    │ • Average protein: 78g (156% of goal)                          │
    │ • Average carbs: 203g (68% of goal)                            │
    │ • Average fat: 58g (87% of goal)                               │
    │                                                                 │
    │ 🎯 GOAL ACHIEVEMENT:                                            │
    │ • Days meeting calorie goal: 4/7 (57%)                         │
    │ • Days meeting protein goal: 7/7 (100%) ✅                     │
    │ • Longest streak staying within goals: 3 days                  │
    │                                                                 │
    │ 💡 INSIGHTS & RECOMMENDATIONS:                                  │
    │ • "You consistently exceed protein goals - great job!"         │
    │ • "Try adding more carbs on Wednesday and Friday"              │
    │ • "Your Tuesday calories tend to be higher - plan ahead"       │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ PERSONALIZED INSIGHTS ENGINE                                    │
    │                                                                 │
    │ 🔍 PATTERN RECOGNITION:                                         │
    │ • "You eat 300 more calories on weekends"                      │
    │ • "Your protein intake drops on Mondays"                       │
    │ • "You're most consistent with breakfast logging"              │
    │                                                                 │
    │ 🎯 GOAL OPTIMIZATION SUGGESTIONS:                               │
    │ • "Based on your activity level, consider 2,200 calories"     │
    │ • "Your protein goals seem too high - try 40g instead"        │
    │ • "Add 50g more carbs for better workout energy"               │
    │                                                                 │
    │ 🥗 FOOD VARIETY ANALYSIS:                                       │
    │ • "You've eaten 47 unique foods this week"                     │
    │ • "Try adding more colorful vegetables"                        │
    │ • "You're missing omega-3 rich foods"                          │
    │                                                                 │
    │ ⏰ TIMING INSIGHTS:                                             │
    │ • "Your largest meals are at dinner - consider shifting"      │
    │ • "You eat 65% of calories after 6 PM"                        │
    │ • "Try a larger breakfast to reduce evening cravings"         │
    └─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                         STEP 10: PROGRESS INSIGHTS & RECOMMENDATIONS           │
│                                                                                 │
│  Generate personalized insights based on tracking history:                    │
│                                                                                 │
│  🎯 ACHIEVEMENT HIGHLIGHTS:                                                     │
│  • "7-day protein goal streak! 💪"                                             │
│  • "Best week for vegetable variety: 23 different types"                      │
│  • "Lowest sodium week in 2 months"                                           │
│                                                                                 │
│  📊 PROGRESS TRENDS:                                                            │
│  • Weight trend: -2.3 lbs over 4 weeks                                        │
│  • Average daily calories: Decreased from 2,150 to 1,950                      │
│  • Protein consistency: Improved 34% this month                               │
│                                                                                 │
│  🔮 PREDICTIVE INSIGHTS:                                                        │
│  • "At current rate, you'll reach goal weight in 6-8 weeks"                   │
│  • "Your Tuesday overeating pattern suggests meal prep on Monday"             │
│  • "Adding 200 cal breakfast reduces 400 cal evening snacking"                │
│                                                                                 │
│  💡 ACTIONABLE RECOMMENDATIONS:                                                 │
│  • "Try meal prepping Sunday for consistent weekday nutrition"                │
│  • "Your best days include protein at breakfast - make it a habit"           │
│  • "Consider tracking water intake - affects hunger signals"                   │
│                                                                                 │
│  [DECISION POINT 9: Final Action Selection]                                    │
│  "Great tracking session! What would you like to do next?"                    │
└─────┬──────┬──────┬──────┬─────────────────────────────────────────────────┘
      │      │      │      │
      ▼      ▼      ▼      ▼
   ┌─────┐ ┌────┐ ┌────┐ ┌─────────────┐
   │Plan │ │Fin-│ │Sta-│ │ Export      │
   │Next │ │d   │ │rt  │ │ Progress    │
   │Meal │ │Rec-│ │Coo-│ │ Report      │
   │     │ │ipe │ │king│ │             │
   │     │ │    │ │    │ │             │
   └──┬──┘ └─┬──┘ └─┬──┘ └──────┬──────┘
      │      │      │           │
      ▼      ▼      ▼           ▼

┌─────────────────────────────────────────────────────────────────────────────────┐
│                             ENDPOINT ACTIONS                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ PLAN NEXT MEAL                                                  │
    │                                                                 │
    │ Based on current daily progress:                                │
    │ • Remaining calories: 955                                       │
    │ • Needed macros: 175g carbs, 27g fat                          │
    │ • Micronutrient gaps: Iron, Vitamin C                          │
    │                                                                 │
    │ Meal Suggestions:                                               │
    │ 🍽️ "For dinner, try salmon with quinoa and broccoli"           │
    │ 🥗 "A large salad with nuts would balance your day perfectly"   │
    │ 🍝 "Whole grain pasta with tomato sauce fills your carb needs"  │
    │                                                                 │
    │ Smart Planning:                                                 │
    │ • Auto-generate meal options within remaining calorie budget   │
    │ • Prioritize foods that fill micronutrient gaps                │
    │ • Consider prep time and available ingredients                  │
    │                                                                 │
    │ [TRANSITION 1: To Meal Planning Journey]                        │
    │ Pass: remaining_calories, macro_gaps, micronutrient_needs      │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ FIND RECIPES FOR REMAINING CALORIES                             │
    │                                                                 │
    │ Recipe Search Criteria:                                         │
    │ • Target calories: 900-1000 (for remaining meals)              │
    │ • High in: Carbohydrates, moderate fat                         │
    │ • Rich in: Iron, Vitamin C, Fiber                              │
    │ • Prep time: Match user's available time                       │
    │                                                                 │
    │ Personalized Recommendations:                                   │
    │ • Recipes using foods you've never tracked                     │
    │ • Cuisine types you haven't tried this week                    │
    │ • Difficulty level matching your cooking skills                │
    │                                                                 │
    │ Nutritional Optimization:                                       │
    │ • "This curry provides the iron you're missing today"         │
    │ • "Try this smoothie bowl - it adds 3 servings of fruit"      │
    │                                                                 │
    │ [TRANSITION 2: To Recipe Discovery Journey]                     │
    │ Pass: nutritional_gaps, calorie_budget, dietary_preferences   │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ START COOKING WITH TRACKED INGREDIENTS                          │
    │                                                                 │
    │ Cooking Integration:                                            │
    │ • "You have chicken and quinoa - let's make that bowl!"        │
    │ • Use logged food portions for recipe scaling                  │
    │ • Adjust cooking instructions for tracked serving sizes        │
    │                                                                 │
    │ Pre-Cooking Nutrition Lock-in:                                  │
    │ • Reserve calories for planned cooking session                 │
    │ • Pre-log the meal you're about to make                        │
    │ • Adjust ingredients based on nutrition targets                │
    │                                                                 │
    │ Post-Cooking Verification:                                      │
    │ • Confirm actual portions consumed                              │
    │ • Adjust logs based on cooking modifications                   │
    │ • Account for added oils, seasonings, etc.                     │
    │                                                                 │
    │ [TRANSITION 3: To Cooking Guidance Journey]                     │
    │ Pass: available_ingredients, nutrition_targets, portion_goals  │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ EXPORT PROGRESS REPORT                                          │
    │                                                                 │
    │ 📊 COMPREHENSIVE NUTRITION REPORT:                              │
    │                                                                 │
    │ 📅 Daily Summary Report:                                        │
    │ • Complete food log with timestamps                             │
    │ • Nutritional breakdown by meal                                 │
    │ • Goal achievement status                                       │
    │ • Recommendations for tomorrow                                  │
    │                                                                 │
    │ 📈 Weekly Progress Report:                                       │
    │ • 7-day nutrition trends and patterns                          │
    │ • Goal consistency metrics                                      │
    │ • Food variety analysis                                         │
    │ • Weight change correlation (if tracked)                       │
    │                                                                 │
    │ 🎯 Monthly Health Dashboard:                                     │
    │ • Long-term trend analysis                                      │
    │ • Habit formation progress                                      │
    │ • Seasonal eating pattern insights                             │
    │ • Health goal achievement timeline                              │
    │                                                                 │
    │ Export Formats:                                                 │
    │ • PDF for healthcare provider sharing                          │
    │ • CSV for personal analysis                                     │
    │ • Infographic for social sharing                               │
    │                                                                 │
    │ [ENDPOINT 1: Progress Report Generated]                         │
    │ Bot: "Report exported! Share with your nutritionist or doctor."│
    └─────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────┐
│                         ADDITIONAL CROSS-JOURNEY TRANSITIONS                   │
└─────────────────────────────────────────────────────────────────────────────────┘

    FROM VARIOUS STEPS - Extended Integration Options:

    ┌─────────────────────────────────────────────────────────────────┐
    │ TO NUTRITIONAL LOOKUP JOURNEY                                   │
    │ • Deep dive into specific food's nutritional profile           │
    │ • "Tell me more about the vitamins in this spinach"            │
    │ • Compare nutritional profiles of similar foods                │
    │ • Understand micronutrient functions and benefits              │
    │                                                                 │
    │ [TRANSITION 4: To Nutritional Lookup Journey]                   │
    │ Pass: selected_food, nutrition_curiosity, health_goals        │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ TO GROCERY ASSISTANCE JOURNEY                                   │
    │ • "I need to buy foods that help me meet my goals"             │
    │ • Generate shopping list for nutritional gap foods             │
    │ • Plan grocery shopping based on tracking insights             │
    │ • Find foods rich in nutrients you're consistently missing     │
    │                                                                 │
    │ [TRANSITION 5: To Grocery Assistance Journey]                   │
    │ Pass: nutritional_gaps, preferred_foods, budget_considerations │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ TO MEAL PLANNING INTEGRATION                                    │
    │ • "Plan tomorrow's meals based on today's tracking"            │
    │ • Use tracking patterns to inform weekly meal planning         │
    │ • Balance multi-day nutrition across planned meals             │
    │ • Create meal plans that address consistent nutritional gaps   │
    │                                                                 │
    │ [TRANSITION 6: To Advanced Meal Planning]                       │
    │ Pass: tracking_patterns, goal_adherence, food_preferences     │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ TO CALORIE-BASED MEAL SUGGESTIONS                               │
    │ • "Find meals that fit my remaining calories"                   │
    │ • Get meal suggestions optimized for current daily progress    │
    │ • Discover foods that complement today's nutritional intake    │
    │                                                                 │
    │ [TRANSITION 7: To Calorie-Based Meal Recommendations]           │
    │ Pass: remaining_calories, consumed_nutrients, meal_timing      │
    └─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                               ERROR HANDLING FLOWS                             │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ FOOD SEARCH FAILURES                                            │
    └─────┬───────────────────────────────────────────────────────────┘
          │
          ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │ [DECISION POINT: Search Resolution]                             │
    │ "I couldn't find that food. Let me help you."                  │
    └─────┬──────┬──────┬─────────────────────────────────────────────┘
          │      │      │
          ▼      ▼      ▼
    ┌─────────┐ ┌────┐ ┌─────────────────────────────────────────┐
    │ SIMILAR │ │CUS-│ │ MANUAL NUTRITION ENTRY                  │
    │ FOODS   │ │TOM │ │ Guide user through calorie and macro    │
    │ SUGGEST │ │FOO-│ │ input for unknown foods                 │
    │         │ │D   │ │                                         │
    │         │ │CREA│ │                                         │
    │         │ │TION│ │                                         │
    └────┬────┘ └─┬──┘ └─────────────────┬───────────────────────┘
         │        │                      │
         ▼        ▼                      ▼
    [CONTINUE WITH SELECTED ALTERNATIVE OR CREATED FOOD]

    ┌─────────────────────────────────────────────────────────────────┐
    │ PORTION SIZE AMBIGUITY                                          │
    │ • Handle unusual serving descriptions                           │
    │ • Clarify "medium" vs "large" portion ambiguity                │
    │ • Convert unclear measurements to standard units               │
    │                                                                 │
    │ Resolution Strategies:                                          │
    │ • "Can you describe the size? (palm-sized, deck of cards)"     │
    │ • Show visual portion guides                                    │
    │ • Offer weight/volume alternatives                              │
    │ • Use grocery_support_raw.json conversion references           │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ GOAL CALCULATION CONFLICTS                                      │
    │ • User's manual goals conflict with calculated recommendations  │
    │ • Extremely high or low calorie targets                        │
    │ • Impossible macro ratio combinations                           │
    │                                                                 │
    │ Safety Guardrails:                                              │
    │ • Minimum 1,200 calories for women, 1,500 for men             │
    │ • Maximum 4,000 calories without medical supervision           │
    │ • Macro ratios within healthy ranges (10-35% protein, etc.)    │
    │                                                                 │
    │ Resolution:                                                     │
    │ • Flag concerning goals to user                                │
    │ • Suggest consulting healthcare provider                       │
    │ • Offer evidence-based alternatives                            │
    └─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              ENDPOINT SUMMARY                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

    ENDPOINT 1: Progress Report Generated
    ├─ Comprehensive nutrition analysis exported
    ├─ Shareable health data for professionals
    └─ Personal tracking insights documented


    TRANSITION 1: To Meal Planning Journey
    ├─ Nutrition-aware meal planning
    ├─ Goal-optimized food selection
    └─ Calorie-budget meal generation

    TRANSITION 2: To Recipe Discovery Journey
    ├─ Nutrition-gap recipe recommendations
    ├─ Calorie-targeted recipe search
    └─ Health-goal recipe filtering

    TRANSITION 3: To Cooking Guidance Journey
    ├─ Portion-aware cooking instructions
    ├─ Nutrition-optimized meal preparation
    └─ Real-time calorie tracking during cooking

    TRANSITION 4: To Nutritional Lookup Journey
    ├─ Deep nutritional education
    ├─ Food comparison analysis
    └─ Micronutrient gap understanding

    TRANSITION 5: To Grocery Assistance Journey
    ├─ Nutrition-targeted shopping lists
    ├─ Goal-supporting food procurement
    └─ Healthy choice grocery guidance

    TRANSITION 6: To Advanced Meal Planning
    ├─ Pattern-informed meal planning
    ├─ Multi-day nutrition balancing
    └─ Habit-aware food scheduling

    TRANSITION 7: To Calorie-Based Meal Recommendations
    ├─ Real-time calorie-budget meals
    ├─ Complement-based food suggestions
    └─ Daily-progress meal optimization

    ERROR EXITS:
    ├─ Food search failures → Alternative food suggestions
    ├─ Portion ambiguity → Visual guidance and clarification
    ├─ Goal conflicts → Safety guardrails and recommendations
    └─ System errors → Graceful degradation with manual entry

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            DATA DEPENDENCIES                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

    FROM foods_nutrition_raw.json:
    ├─ food.name → Search matching and identification
    ├─ food.per_100g → Portion-based nutrition calculations
    ├─ food.calories → Daily calorie tracking totals
    ├─ food.protein, carbs, fat → Macro tracking and ratios
    ├─ food.vitamins_per_100g → Micronutrient goal tracking
    ├─ food.minerals_per_100g → Nutritional gap analysis
    ├─ food.category → Food group variety analysis
    └─ food.dietary_tags → Goal compatibility checking

    FROM meal_suggestions_raw.json:
    ├─ meal.components[] → Quick meal logging options
    ├─ meal.nutrition → Complete meal nutrition calculation
    ├─ meal.calories → Meal-based calorie tracking
    └─ meal.dietary_tags → Goal-aligned meal suggestions

    FROM grocery_support_raw.json:
    ├─ ingredient_aliases → Food search optimization
    ├─ unit_conversions → Portion standardization
    ├─ substitutions → Alternative food suggestions
    └─ dietary_substitutions → Goal-compatible alternatives

    FROM user_profiles.json (tracking-specific):
    ├─ daily_calorie_goal → Progress calculation baseline
    ├─ macro_ratio_targets → Daily balance assessment
    ├─ dietary_restrictions → Food filtering and suggestions
    ├─ activity_level → Dynamic calorie goal adjustment
    ├─ health_goals → Personalized insight generation
    ├─ tracking_history → Pattern recognition and trends
    └─ preferred_foods → Personalized food suggestions

    CALCULATED TRACKING METRICS:
    ├─ daily_calorie_total → Real-time goal progress
    ├─ macro_percentages → Balance assessment and visualization
    ├─ micronutrient_totals → Gap analysis and recommendations
    ├─ food_variety_score → Nutritional diversity tracking
    ├─ goal_adherence_rate → Consistency measurement
    ├─ weekly_trend_analysis → Pattern identification
    ├─ nutritional_density_score → Food quality assessment
    └─ habit_formation_metrics → Behavior change tracking

    REAL-TIME CALCULATIONS:
    ├─ remaining_calories → Budget-based meal suggestions
    ├─ macro_gaps → Targeted food recommendations
    ├─ micronutrient_deficiencies → Health optimization alerts
    ├─ portion_scaling → Accurate nutrition from actual consumption
    ├─ meal_timing_impact → Circadian rhythm optimization
    └─ hydration_correlation → Hunger signal accuracy

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FLOW STATISTICS                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

    Total Decision Points: 9
    ├─ Tracking action type (log/view/manage)
    ├─ Food entry method (search/manual/recent)
    ├─ Food selection from search results
    ├─ Portion size specification
    ├─ Meal timing assignment
    ├─ Entry confirmation and adjustments
    ├─ Next action selection after logging
    ├─ Progress insights review
    └─ Final action selection

    Possible Endpoints: 1
    ├─ Direct completion (reports exported)
    ├─ Cross-journey transitions (7 different journeys)
    └─ Continuous tracking cycle (return to logging)

    Data Processing Features:
    ├─ Real-time nutrition calculation and goal tracking
    ├─ Intelligent food search with alias matching
    ├─ Pattern recognition for personalized insights
    ├─ Multi-day trend analysis and forecasting
    ├─ Automatic portion scaling and unit conversion
    ├─ Cross-journey nutrition data integration
    └─ Adaptive goal optimization based on progress

    Session Duration Estimates:
    ├─ Quick food logging: 1-3 minutes
    ├─ Detailed food entry with search: 4-7 minutes
    ├─ Daily summary review: 3-5 minutes
    ├─ Weekly trend analysis: 8-12 minutes
    ├─ Goal adjustment session: 10-15 minutes
    └─ Comprehensive progress review: 15-25 minutes

    Accuracy & Reliability:
    ├─ Food database coverage: 50 detailed foods
    ├─ Portion estimation accuracy: ±15% with visual guides
    ├─ Calorie calculation precision: ±5% for logged portions
    ├─ Macro ratio calculations: Real-time, mathematically accurate
    ├─ Goal tracking consistency: 100% data integrity
    ├─ Cross-journey data sync: Seamless bidirectional updates
    └─ Pattern recognition reliability: Improves with usage data

    Health & Safety Features:
    ├─ Calorie goal safety limits (1200-4000 cal range)
    ├─ Macro ratio health boundary enforcement
    ├─ Micronutrient deficiency early warning system
    ├─ Eating pattern concern flagging
    ├─ Healthcare provider report generation
    └─ Evidence-based recommendation engine

    Gamification & Motivation:
    ├─ Streak tracking for consistency rewards
    ├─ Goal achievement celebration triggers
    ├─ Progress milestone recognition system
    ├─ Social sharing of healthy achievements
    ├─ Weekly challenge generation
    └─ Habit formation progress visualization

This comprehensive flowchart covers the complete food and calorie tracking experience, from initial food logging through advanced progress analysis to goal achievement, with robust integration across all nutrition chatbot journeys and intelligent personalization based on user behavior patterns.
```
