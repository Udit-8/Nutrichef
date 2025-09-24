# 🎯 Calorie-based Meal Recommendations Visual Journey Map

## Decision Tree Flow Chart

```
                                👤 USER STARTS
                                       |
                                       ▼
                    ┌─────────────────────────────────────────────┐
                    │   🎯 CALORIE-BASED MEAL RECOMMENDATIONS   │
                    │        "Find meals by calorie target"      │
                    └─────────────────────┬───────────────────────┘
                                          │
                                          ▼
                    ┌─────────────────────────────────────────────┐
                    │      🔢 STEP 1: CALORIE GOAL DETERMINATION │
                    │     "What's your calorie target?"          │
                    └─────────────────────┬───────────────────────┘
                                          │
              ┌───────────┬───────────────┼───────────────┬───────────┐
              ▼           ▼               ▼               ▼           ▼
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │💯 EXACT     │ │📊 RANGE     │ │🏷️ CATEGORY │ │💬 NATURAL   │
      │ NUMBER      │ │SPECIFICATION│ │  BASED      │ │ LANGUAGE    │
      │"400         │ │"300-500     │ │"low calorie │ │"healthy     │
      │calories"    │ │calories"    │ │lunch"       │ │breakfast    │
      │             │ │             │ │             │ │under 350"   │
      └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
            │               │               │               │
            └───────────────┼───────────────┼───────────────┘
                            │               │
                            └───────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────────────┐
                    │       🍽️ STEP 2: MEAL TYPE SELECTION      │
                    │    "What type of meal are you looking for?"│
                    └─────────────────────┬───────────────────────┘
                                          │
              ┌───────────┬───────────────┼───────────────┬───────────┐
              ▼           ▼               ▼               ▼           ▼
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │🌅 BREAKFAST │ │🌞 LUNCH     │ │🌆 DINNER    │ │🍎 SNACK     │
      │Morning meal │ │Midday meal  │ │Evening meal │ │Light bite   │
      │High energy  │ │Balanced     │ │Satisfying   │ │Quick &      │
      │start        │ │nutrition    │ │nutrients    │ │portable     │
      └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
            │               │               │               │
            └───────────────┼───────────────┼───────────────┘
                            │               │
                            └───────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────────────┐
                    │      🍃 STEP 3: DIETARY PREFERENCES        │
                    │   "Any dietary restrictions or goals?"     │
                    └─────────────────────┬───────────────────────┘
                                          │
      ┌─────────┬─────────┬───────────────┼───────────────┬─────────┬─────────┐
      ▼         ▼         ▼               ▼               ▼         ▼         ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│🥕 VEGETAR  │ │🌱 VEGAN     │ │🥩 HIGH      │ │🌾 GLUTEN    │ │🥛 DAIRY     │ │✅ NO       │
│   IAN      │ │             │ │ PROTEIN     │ │  FREE       │ │  FREE       │ │RESTRICTIONS│
│Plant-based │ │All plants   │ │Muscle focus │ │No gluten    │ │No dairy     │ │All foods   │
│+ dairy/eggs│ │no animal    │ │building     │ │products     │ │products     │ │welcome     │
└─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
      │               │               │               │               │               │
      └───────────────┼───────────────┼───────────────┼───────────────┼───────────────┘
                      │               │               │               │
                      └───────────────┼───────────────┼───────────────┘
                                      │               │
                                      └───────────────┘
                                              │
                                              ▼
                    ┌─────────────────────────────────────────────┐
                    │      ⏰ STEP 4: TIME CONSTRAINTS           │
                    │  "How much time do you have to eat/prep?"  │
                    └─────────────────────┬───────────────────────┘
                                          │
              ┌───────────┬───────────────┼───────────────┬───────────┐
              ▼           ▼               ▼               ▼           ▼
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │⚡ IMMEDIATE │ │🏃 QUICK     │ │⏲️ MODERATE │ │🍽️ NO TIME  │
      │ (5 min)     │ │ (15 min)    │ │ (30 min)    │ │  LIMIT      │
      │Grab & go    │ │Minimal prep │ │Some cooking │ │Can take     │
      │ready foods  │ │simple meals │ │involved     │ │longer       │
      └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
            │               │               │               │
            └───────────────┼───────────────┼───────────────┘
                            │               │
                            └───────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────────────┐
                    │         🎲 STEP 5: PREFERENCE SCOPE        │
                    │    "Specific preferences or open to all?"  │
                    └─────────────────────┬───────────────────────┘
                                          │
              ┌───────────┬───────────────┼───────────────┬───────────┐
              ▼           ▼               ▼               ▼           ▼
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │🌍 CUISINE   │ │🥗 INGREDIENTS│ │🔥 COOKING   │ │✨ SURPRISE  │
      │  STYLE      │ │  SPECIFIC   │ │   STYLE     │ │    ME       │
      │Italian,     │ │Must/avoid   │ │Grilled,     │ │Open to all │
      │Asian, etc.  │ │certain items│ │baked, etc.  │ │suggestions  │
      └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
            │               │               │               │
            └───────────────┼───────────────┼───────────────┘
                            │               │
                            └───────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────────────┐
                    │       🔍 STEP 6: DATABASE SEARCH           │
                    │     "Searching meal database..."           │
                    └─────────────────────┬───────────────────────┘
                                          │
              ┌───────────┬───────────────┼───────────────┬───────────┐
              ▼           ▼               ▼               ▼           ▼
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │✅ EXACT     │ │🎯 CLOSE     │ │🔄 FALLBACK  │ │❌ NO       │
      │  MATCHES    │ │  MATCHES    │ │  SEARCH     │ │  RESULTS    │
      │Perfect fit  │ │Near target  │ │Expanded     │ │Try broader  │
      │for criteria │ │calories     │ │criteria     │ │search       │
      └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
            │               │               │               │
            └───────────────┼───────────────┼───────────────┘
                            │               │
                            └───────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────────────┐
                    │        📊 STEP 7: RESULTS FILTERING        │
                    │    "Ranking and filtering best matches"    │
                    └─────────────────────┬───────────────────────┘
                                          │
              ┌───────────┬───────────────┼───────────────┬───────────┐
              ▼           ▼               ▼               ▼           ▼
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │🎯 CALORIE   │ │🥗 DIETARY   │ │⏰ TIME      │ │⭐ QUALITY   │
      │ MATCHING    │ │COMPLIANCE   │ │CONSTRAINT   │ │  RANKING    │
      │Best calorie │ │Meets diet   │ │Fits time    │ │Highest      │
      │fit first    │ │restrictions │ │available    │ │rated meals  │
      └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
            │               │               │               │
            └───────────────┼───────────────┼───────────────┘
                            │               │
                            └───────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────────────┐
                    │        🍽️ STEP 8: MEAL SELECTION          │
                    │      "Choose your perfect meal!"           │
                    └─────────────────────┬───────────────────────┘
                                          │
              ┌───────────┬───────────────┼───────────────┬───────────┐
              ▼           ▼               ▼               ▼           ▼
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │1️⃣ MEAL A   │ │2️⃣ MEAL B   │ │3️⃣ MEAL C   │ │🔄 SEARCH    │
      │[Name]       │ │[Name]       │ │[Name]       │ │   AGAIN     │
      │[Calories]   │ │[Calories]   │ │[Calories]   │ │Different    │
      │[Nutrition]  │ │[Nutrition]  │ │[Nutrition]  │ │criteria     │
      └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
            │               │               │               │
            └───────────────┼───────────────┼───────────────┘
                            │               │
                            └───────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────────────────────────────────────────────────────────┐
                    │                    🎉 STEP 9: DETAILED MEAL INFORMATION                                │
                    │               "Perfect! Here's your personalized meal recommendation"                   │
                    │                                                                                         │
                    │  📊 NUTRITION BREAKDOWN: Complete macro and micronutrient analysis                     │
                    │  🛒 INGREDIENT LIST: Exact quantities and shopping information                          │
                    │  👩‍🍳 PREPARATION GUIDE: Step-by-step cooking instructions                             │
                    │  💡 TIPS & ALTERNATIVES: Substitutions and customization options                       │
                    └─────────────────────────────┬───────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
                                      ┌─────────────────────────┐
                                      │    🎯 NEXT ACTIONS      │
                                      │ "Ready to make this     │
                                      │      meal happen?"      │
                                      └─────────┬───────────────┘
                                                │
                    ┌─────────┬─────────┬───────┼───────┬─────────┬─────────┐
                    ▼         ▼         ▼       ▼       ▼         ▼         ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │🛒 GET       │ │👩‍🍳 START   │ │📊 LOG TO    │ │🔍 FIND      │ │🔄 NEW       │
            │INGREDIENTS  │ │  COOKING    │ │   DIARY     │ │ SIMILAR     │ │ JOURNEY     │
            │             │ │             │ │             │ │             │ │             │
            └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
                  │               │               │               │               │
                  ▼               ▼               ▼               ▼               ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │🛒 GROCERY   │ │🍳 COOKING   │ │📊 FOOD      │ │🔍 RECIPE    │ │🏠 MAIN MENU │
            │ ASSISTANCE  │ │ GUIDANCE    │ │ TRACKING    │ │ DISCOVERY   │ │   SELECT    │
            │  JOURNEY    │ │  JOURNEY    │ │  JOURNEY    │ │  JOURNEY    │ │   JOURNEY   │
            └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
                  │               │               │               │               │
                  ▼               ▼               ▼               ▼               ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │ TARGETED    │ │INTERACTIVE  │ │ CALORIE     │ │ EXPANDED    │ │ CHOOSE NEW  │
            │SHOPPING LIST│ │STEP-BY-STEP │ │ TRACKING    │ │RECIPE SEARCH│ │ NUTRITION   │
            │FOR MEAL     │ │  COOKING    │ │FOR MEAL     │ │& DISCOVERY  │ │   JOURNEY   │
            └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘

```

## 🎯 Journey Summary

**Entry Point**: 👤 User says "Find meals by calories" or selects Calorie-based Meal Recommendations

**Step 1**: 🔢 Calorie Goal Determination (exact number, range, category, natural language)
**Step 2**: 🍽️ Meal Type Selection (breakfast, lunch, dinner, snack)
**Step 3**: 🍃 Dietary Preferences (vegetarian, vegan, high protein, gluten-free, dairy-free, no restrictions)
**Step 4**: ⏰ Time Constraints (immediate, quick, moderate, no limit)
**Step 5**: 🎲 Preference Scope (cuisine style, ingredients, cooking style, surprise me)
**Step 6**: 🔍 Database Search (exact matches, close matches, fallback search, no results)
**Step 7**: 📊 Results Filtering (calorie matching, dietary compliance, time constraints, quality ranking)
**Step 8**: 🍽️ Meal Selection (choose from 3 recommendations or search again)
**Step 9**: 🎉 Detailed Information (complete nutrition, ingredients, preparation, tips)

**Exit Points**: 
- 🛒 Get Ingredients → Grocery Assistance Journey
- 👩‍🍳 Start Cooking → Cooking Guidance Journey
- 📊 Log to Diary → Food Tracking Journey
- 🔍 Find Similar → Recipe Discovery Journey
- 🔄 New Journey → Main Menu

**Key Features**:
✅ 9-step comprehensive meal matching system
✅ Real database integration with 50+ curated meals
✅ Flexible calorie range and fallback search mechanisms
✅ Advanced filtering by dietary restrictions and time constraints
✅ Detailed nutrition analysis and preparation guidance
✅ Seamless transitions to implementation journeys

## Detailed Journey Flow

### 🎯 Entry Points
- **Direct Intent**: "Find 400-calorie lunch", "Low-calorie breakfast ideas", "Healthy snack under 200 calories"
- **Menu Selection**: Choose "Calorie-based Meal Recommendations" from main menu
- **Cross-Journey**: From food tracking wanting specific calorie meals

### 📊 Step-by-Step Breakdown

#### **Step 1: Calorie Goal Determination** 
```
🎯 Step 1: Calorie Goal Determination

What's your calorie target for your meal?

Input Options:
💯 Exact Number: "400 calories" or just "400"
📊 Range: "300-500 calories" or "between 300 and 500"
🏷️ Category: "low calorie lunch" (under 400)
💬 Natural: "healthy breakfast under 350"

Common Targets:
🌅 Breakfast: 250-400 calories
🌞 Lunch: 350-600 calories  
🌆 Dinner: 400-800 calories
🍎 Snacks: 100-300 calories

Examples:
• "I want a 400-calorie lunch"
• "Something between 250-350 calories"
• "Low-calorie dinner under 500"
• "High-protein breakfast around 300"

What's your calorie goal? 🎯

CALL TO ACTION: Type your calorie target clearly!
```

**User Options:**
- Exact calorie number
- Calorie range
- Category descriptions
- Natural language input

**Data Stored:** `calorie_target`, `calorie_range`

#### **Step 2: Meal Type Selection**
```
✅ Calorie Target: [Target/Range] calories

🍽️ Step 2: Meal Type Selection

What type of meal are you looking for?

Meal Types:
🌅 Breakfast - Start your day right
   *Energy-focused, often with protein & carbs*

🌞 Lunch - Midday fuel  
   *Balanced nutrition, satisfying but not heavy*

🌆 Dinner - Evening satisfaction
   *Hearty, nutritious, often the main meal*

🍎 Snack - Quick bite
   *Light, portable, between-meal energy*

Each meal type has different nutritional focuses and preparation styles suited to the time of day.

What meal are you planning? 🕐

CALL TO ACTION: Choose breakfast, lunch, dinner, or snack
```

**User Options:**
- Meal type selection
- Natural language descriptions
- Multiple meal types

**Data Stored:** `meal_type`

#### **Step 3: Dietary Preferences**
```
🍽️ Meal Type: [Selected meal type]

🍃 Step 3: Dietary Preferences

Any dietary restrictions or specific goals?

Dietary Options:
🥕 Vegetarian - Plant-based with dairy/eggs
🌱 Vegan - Fully plant-based, no animal products
🥩 High Protein - Focus on muscle building & satiety
🌾 Gluten-Free - No wheat, barley, rye products
🥛 Dairy-Free - No milk, cheese, yogurt products
✅ No Restrictions - All foods welcome

Special Goals:
💪 Muscle gain, weight loss, athletic performance
🏃 Pre/post workout nutrition
🩺 Medical dietary requirements

Your dietary needs help me find the perfect meal match!

What dietary preferences should I consider? 🥗

CALL TO ACTION: Select restrictions or type "none"
```

**User Options:**
- Dietary restriction selection
- Special nutrition goals
- Multiple preferences
- No restrictions

**Data Stored:** `dietary_preferences`

#### **Step 4: Time Constraints**
```
🍃 Dietary: [Selected preferences]

⏰ Step 4: Time Constraints

How much time do you have to eat or prepare?

Time Options:
⚡ Immediate (5 min) - Grab & go ready foods
   *Pre-made, minimal assembly*

🏃 Quick (15 min) - Minimal prep, simple meals
   *Light cooking, basic preparation*

⏲️ Moderate (30 min) - Some cooking involved
   *Fresh cooking, multiple steps*

🍽️ No Time Limit - Can take longer
   *Complex preparation, elaborate cooking*

Time affects meal complexity and preparation method!

How much time do you have? ⏰

CALL TO ACTION: Choose your available time
```

**User Options:**
- Time constraint selection
- Custom time amounts
- No time limitations

**Data Stored:** `time_constraints`

#### **Step 5: Preference Scope**
```
⏰ Time: [Selected time constraint]

🎲 Step 5: Preference Scope

Any specific preferences or open to suggestions?

Preference Types:
🌍 Cuisine Style - Italian, Asian, Mexican, etc.
🥗 Ingredients - Must include/avoid certain foods
🔥 Cooking Style - Grilled, baked, raw, etc.
✨ Surprise Me - Open to all suggestions

Examples:
• "Something Italian with pasta"
• "Must include chicken, avoid dairy"
• "Prefer baked or grilled foods"
• "Surprise me with something healthy"

The more specific, the better I can match your taste!

Any specific preferences? 🎨

CALL TO ACTION: Describe preferences or say "surprise me"
```

**User Options:**
- Cuisine preferences
- Ingredient requirements
- Cooking method preferences
- Open to suggestions

**Data Stored:** `preference_scope`

#### **Step 6: Database Search**
```
🎲 Preferences: [Selected preferences]

🔍 Step 6: Database Search

Searching meal database for your perfect match...

Search Process:
1️⃣ Primary Search: Exact calorie and preference match
2️⃣ Secondary Search: Close calorie match (±50 calories)
3️⃣ Fallback Search: Broader criteria, flexible ranges
4️⃣ Alternative Search: Similar meals, different approach

Database Info:
📊 50+ curated meals in database
🔍 Advanced filtering by all criteria
⚖️ Intelligent calorie range expansion
🎯 Quality ranking and relevance scoring

Searching... ⏳

[Search results processing...]
```

**Search Logic:**
- Exact match attempt
- Close match with expanded range
- Fallback with relaxed criteria
- No results handling

#### **Step 7: Results Filtering**
```
🔍 Search Complete!

📊 Step 7: Results Filtering

Found [X] potential meals, filtering by best matches...

Filtering Criteria:
🎯 Calorie Accuracy: How close to your target
🥗 Dietary Compliance: Meets all restrictions  
⏰ Time Feasibility: Fits your available time
⭐ Quality Score: Nutritional balance & taste rating

Ranking Process:
1. Perfect calorie matches first
2. Dietary restriction compliance
3. Time constraint satisfaction
4. Overall nutritional quality
5. User preference alignment

Filtering results... 📊

Best matches identified! Moving to selection...
```

**Filtering Logic:**
- Calorie proximity scoring
- Dietary compliance verification
- Time constraint checking
- Quality and nutrition ranking

#### **Step 8: Meal Selection**
```
📊 Results Filtered!

🍽️ Step 8: Meal Selection

Choose your perfect meal from these top recommendations:

🥗 MEAL OPTION 1: [Meal Name]
• Calories: [X] (target: [target])
• Protein: [X]g | Carbs: [X]g | Fat: [X]g
• Prep Time: [X] minutes
• Diet: [Dietary tags]
• Description: [Brief meal description]

🍲 MEAL OPTION 2: [Meal Name]  
• Calories: [X] (target: [target])
• Protein: [X]g | Carbs: [X]g | Fat: [X]g
• Prep Time: [X] minutes
• Diet: [Dietary tags]
• Description: [Brief meal description]

🥙 MEAL OPTION 3: [Meal Name]
• Calories: [X] (target: [target])
• Protein: [X]g | Carbs: [X]g | Fat: [X]g
• Prep Time: [X] minutes
• Diet: [Dietary tags]
• Description: [Brief meal description]

🔄 Or search again with different criteria

Which meal looks perfect? 🍽️

CALL TO ACTION: Choose 1, 2, 3, or "search again"
```

**User Options:**
- Select meal option (1-3)
- Request more details
- Search again with different criteria

**Data Stored:** `selected_meal`

#### **Step 9: Detailed Meal Information**
```
🎉 Perfect! Here's your personalized meal recommendation:

🍽️ [MEAL NAME] - [Calories] calories

📊 COMPLETE NUTRITION BREAKDOWN:
• Total Calories: [X] cal (perfect for your [target] goal!)
• Protein: [X]g ([X]% of calories) - [protein source benefits]
• Carbohydrates: [X]g ([X]% of calories) - [carb source benefits]  
• Fat: [X]g ([X]% of calories) - [fat source benefits]
• Fiber: [X]g | Sodium: [X]mg | Sugar: [X]g

🛒 EXACT INGREDIENT LIST:
• [Ingredient 1]: [Quantity] - [nutritional note]
• [Ingredient 2]: [Quantity] - [nutritional note]
• [Ingredient 3]: [Quantity] - [nutritional note]
• [Additional ingredients...]

👩‍🍳 PREPARATION GUIDE:
1. [Step 1 with timing]
2. [Step 2 with timing]
3. [Step 3 with timing]
Total Prep Time: [X] minutes

💡 CUSTOMIZATION OPTIONS:
• Substitutions: [Alternative ingredients]
• Scaling: Can serve [X] people with [scaling notes]
• Storage: [Storage and leftover information]
• Dietary Mods: [How to adapt for other diets]

🎯 WHY THIS MEAL WORKS:
• Fits your [calorie target] perfectly
• Meets [dietary preferences] requirements
• [Time constraint] preparation time
• [Additional benefits - protein, nutrients, etc.]

Next Steps:
🛒 Get shopping list for ingredients
👩‍🍳 Start step-by-step cooking guidance
📊 Log this meal to your food diary
🔍 Find similar meals with different flavors

Ready to make this delicious meal? 🌟

CALL TO ACTION: Choose your next step!
```

### 🔄 Exit Points & Transitions

#### **Successful Completion**
- **Get Ingredients** → Grocery Assistance Journey with meal-specific shopping list
- **Start Cooking** → Cooking Guidance Journey for selected meal
- **Log to Diary** → Food Tracking Journey with meal pre-populated
- **Find Similar** → Recipe Discovery Journey with similar nutrition profiles
- **New Journey** → Main Menu

#### **Mid-Journey Options**
- **Search Again** → Return to any previous step with modified criteria
- **Modify Preferences** → Adjust dietary or calorie requirements
- **Compare Options** → Review multiple meal choices side-by-side

#### **Cross-Journey Transitions**
1. **To Grocery Assistance**: User wants shopping list for selected meal
2. **To Cooking Guidance**: User wants step-by-step cooking instructions
3. **To Food Tracking**: User wants to log meal to daily diary
4. **To Recipe Discovery**: User wants similar recipes with different approaches
5. **To Meal Planning**: User wants to incorporate meal into weekly plan
6. **To Main Menu**: User wants different journey

### 📋 Session Data Persistence
- `calorie_target`: Target calorie amount
- `calorie_range`: Acceptable calorie range
- `meal_type`: Breakfast, lunch, dinner, or snack
- `dietary_preferences`: Array of dietary restrictions and goals
- `time_constraints`: Available preparation time
- `preference_scope`: Cuisine, ingredient, or cooking preferences
- `search_results`: Array of matching meals from database
- `selected_meal`: Chosen meal with full details
- `current_journey`: "calorie_meal_recommendations"

### 🎯 Key Features
- **Comprehensive 9-Step Process**: Thorough preference gathering
- **Real Database Integration**: 50+ curated meals with complete nutrition data
- **Intelligent Search Algorithm**: Multi-tier search with fallback mechanisms
- **Flexible Calorie Matching**: Exact match, close match, and range expansion
- **Advanced Filtering**: Multiple criteria ranking and relevance scoring
- **Detailed Nutrition Analysis**: Complete macro and micronutrient breakdowns
- **Practical Preparation Guidance**: Step-by-step cooking instructions
- **Customization Options**: Substitutions, scaling, and dietary modifications

### 🔍 Database Search Algorithm

#### **Search Tier System**
1. **Tier 1**: Exact calorie match + all preferences
2. **Tier 2**: ±25 calorie range + all preferences
3. **Tier 3**: ±50 calorie range + core preferences
4. **Tier 4**: ±100 calorie range + meal type only
5. **Tier 5**: Meal type only, any calories

#### **Fallback Mechanisms**
- **Breakfast Range**: 220-335 calories (database reality)
- **Lunch Range**: 280-520 calories
- **Dinner Range**: 320-680 calories
- **Snack Range**: 120-280 calories

### 📊 Meal Database Structure

#### **Database Contents**
- **50 Curated Meals**: Professionally designed for nutrition balance
- **Complete Nutrition Data**: Calories, macros, micronutrients
- **Ingredient Lists**: Exact quantities and preparation notes
- **Dietary Tags**: Vegetarian, vegan, gluten-free, etc.
- **Preparation Times**: Realistic cooking and prep estimates
- **Quality Ratings**: Taste, nutrition, and satisfaction scores

#### **Meal Categories**
- **Breakfast**: 12 options (220-335 cal range)
- **Lunch**: 15 options (280-520 cal range)
- **Dinner**: 18 options (320-680 cal range)
- **Snacks**: 8 options (120-280 cal range)

### ⚡ Performance Optimizations
- **Cached Search Results**: Faster subsequent searches
- **Intelligent Filtering**: Pre-filter by hard constraints
- **Relevance Scoring**: Multi-factor ranking algorithm
- **Fallback Strategies**: Graceful degradation for edge cases
- **User Learning**: Preference tracking for better future recommendations

---

*This journey map represents the complete Calorie-based Meal Recommendations flow as implemented in the nutrition chatbot, showing all possible user paths and decision points for the comprehensive 9-step meal matching system.*