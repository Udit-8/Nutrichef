# 📊 Food Tracking Visual Journey Map

## Decision Tree Flow Chart

```
                                👤 USER STARTS
                                       |
                                       ▼
                    ┌─────────────────────────────────────────────┐
                    │        📊 FOOD TRACKING JOURNEY           │
                    │         "Track my food intake"             │
                    └─────────────────────┬───────────────────────┘
                                          │
                                          ▼
                    ┌─────────────────────────────────────────────┐
                    │          📋 STEP 1: ACTION SELECTION       │
                    │      "What would you like to do?"          │
                    └─────────────────────┬───────────────────────┘
                                          │
              ┌───────────┬───────────────┼───────────────┬───────────┐
              ▼           ▼               ▼               ▼           ▼
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │1️⃣ LOG NEW │ │2️⃣ VIEW     │ │3️⃣ SET      │ │4️⃣ CHECK    │
      │   FOOD     │ │   DIARY     │ │   GOALS     │ │  PROGRESS   │
      │ Add food   │ │Today's log  │ │Nutrition    │ │Weekly stats │
      │ eaten      │ │& summary    │ │targets      │ │& trends     │
      └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
            │               │               │               │
            │               │               │               │
            ▼               ▼               ▼               ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│📝 STEP 2A: FOOD    │ │📊 STEP 2B: DIARY   │ │🎯 STEP 2C: GOALS   │ │📈 STEP 2D: PROGRESS│
│   LOGGING METHOD    │ │    VIEWING          │ │    SETTING          │ │     CHECKING        │
│"How to add food?"   │ │"View logged foods"  │ │"Which goals modify?"│ │"What to review?"    │
└─────────┬───────────┘ └─────────┬───────────┘ └─────────┬───────────┘ └─────────┬───────────┘
          │                       │                       │                       │
┌─────────┼─────────┬─────────────┼─────────────┬─────────┼─────────────┬─────────┼─────────────┐
▼         ▼         ▼             ▼             ▼         ▼             ▼         ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│1️⃣ SEARCH  │ │2️⃣ QUICK    │ │3️⃣ MANUAL   │ │1️⃣ LOG MORE │ │2️⃣ DETAILS  │ │3️⃣ NEW GOAL │ │4️⃣ EXPORT   │
│ DATABASE   │ │  ENTRY      │ │   ENTRY     │ │   FOODS     │ │ BREAKDOWN   │ │  SETTING    │ │   DIARY     │
│Food by name│ │Common foods │ │Custom foods │ │Add new item │ │Nutrient view│ │Modify goals │ │Export data  │
└─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
      │               │               │               │               │               │               │
      └───────────────┼───────────────┼───────────────┼───────────────┼───────────────┼───────────────┘
                      │               │               │               │               │
                      └───────────────┼───────────────┼───────────────┼───────────────┘
                                      │               │               │
                                      └───────────────┼───────────────┘
                                                      │
                                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                🔍 STEP 3: DETAILED INPUT                                                    │
│                     "Provide specific food details and quantities"                                          │
└─────────────────────────────────┬───────────────────────────────────────────────────────────────────────────┘
                                  │
    ┌─────────────┬───────────────┼───────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
    ▼             ▼               ▼               ▼             ▼             ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│🔍 FOOD      │ │⚡ QUICK     │ │✏️ MANUAL    │ │📊 CALORIE   │ │🎯 GOAL      │ │📈 TREND     │ │📁 EXPORT    │
│  SEARCH     │ │  SELECT     │ │  DETAILS    │ │  TARGET     │ │ ADJUSTMENT  │ │  ANALYSIS   │ │  OPTIONS    │
│"Chicken     │ │Oatmeal with │ │Custom dish  │ │Daily calorie│ │Protein/carb │ │Weekly/      │ │PDF/CSV      │
│ breast"     │ │banana       │ │320 calories │ │limit 1800   │ │targets      │ │monthly view │ │format       │
└─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
      │               │               │               │               │               │               │
      └───────────────┼───────────────┼───────────────┼───────────────┼───────────────┼───────────────┘
                      │               │               │               │               │
                      └───────────────┼───────────────┼───────────────┼───────────────┘
                                      │               │               │
                                      └───────────────┼───────────────┘
                                                      │
                                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           ✅ STEP 4: CONFIRMATION & RESULTS                                                │
│                      "Food logged successfully! Here's your updated summary"                               │
│                                                                                                             │
│  📝 LOGGED FOODS: Today's intake added to diary                                                            │
│  📊 DAILY TOTALS: Calories, protein, carbs, fat updated                                                   │
│  🎯 PROGRESS: Goal achievement percentages calculated                                                      │
│  📈 INSIGHTS: Nutritional analysis and recommendations                                                     │
└─────────────────────────────┬───────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────────┐
                    │    🎯 NEXT ACTIONS      │
                    │  "What would you like   │
                    │      to do next?"       │
                    └─────────┬───────────────┘
                              │
          ┌─────────┬─────────┼─────────┬─────────┬─────────┬─────────┐
          ▼         ▼         ▼         ▼         ▼         ▼         ▼
  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
  │📝 LOG MORE  │ │📊 VIEW     │ │🍽️ PLAN     │ │🛒 GROCERY   │ │👩‍🍳 COOK    │ │🔄 NEW       │
  │   FOOD      │ │ FULL DIARY  │ │  MEALS      │ │   LIST      │ │  RECIPE     │ │ JOURNEY     │
  │             │ │             │ │             │ │             │ │             │ │             │
  └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
        │               │               │               │               │               │
        ▼               ▼               ▼               ▼               ▼               ▼
  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
  │🔄 CONTINUE   │ │📊 FOOD      │ │🍽️ MEAL     │   │🛒 GROCERY   │ │🍳 COOKING   │ │🏠 MAIN MENU │
  │FOOD LOGGING │ │ TRACKING    │ │ PLANNING    │ │ ASSISTANCE  │ │ GUIDANCE    │ │   SELECT    │
  │   SESSION   │ │  ANALYSIS   │ │  JOURNEY    │ │  JOURNEY    │ │  JOURNEY    │ │   JOURNEY   │
  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
        │               │               │               │               │               │
        ▼               ▼               ▼               ▼               ▼               ▼
  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
  │ ADD ANOTHER │ │ NUTRITION   │ │ PERSONALIZED│ │ ORGANIZED   │ │INTERACTIVE  │ │ CHOOSE NEW  │
  │ FOOD ITEM   │ │ INSIGHTS &  │ │MEAL PLANS   │ │SHOPPING LIST│ │STEP-BY-STEP │ │ NUTRITION   │
  │ TO DIARY    │ │ PROGRESS    │ │BY GOALS     │ │BY CATEGORIES│ │  COOKING    │ │   JOURNEY   │
  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘

```

## 🎯 Journey Summary

**Entry Point**: 👤 User says "Track my food" or selects Food Tracking

**Step 1**: 📋 Action Selection (Log Food, View Diary, Set Goals, Check Progress)
**Step 2**: 🎯 Method Selection (varies by path - Search/Quick/Manual for logging, or view options)
**Step 3**: 🔍 Detailed Input (specific food details, quantities, or specific view requests)
**Step 4**: ✅ Confirmation & Results (logged successfully with updated summary)

**Exit Points**: 
- 📝 Continue Logging → Same journey continuation
- 📊 View Analysis → Detailed nutrition insights  
- 🍽️ Meal Planning → Meal Planning Journey
- 🛒 Shopping List → Grocery Assistance Journey
- 👩‍🍳 Cook Recipe → Cooking Guidance Journey
- 🔄 New Journey → Main Menu

**Key Features**:
✅ 4-step progressive disclosure with multiple paths
✅ Flexible input methods (search, quick select, manual entry)
✅ Real-time nutrition tracking and goal monitoring
✅ Detailed nutrient breakdowns and progress tracking
✅ Multiple exit pathways to other journeys
✅ Persistent session data and daily summaries

## Detailed Journey Flow

### 🎯 Entry Points
- **Direct Intent**: "Log my breakfast", "Track calories", "What did I eat today?"
- **Menu Selection**: Choose "Food Tracking" from main menu
- **Cross-Journey**: From recipe completion wanting to log meal

### 📊 Step-by-Step Breakdown

#### **Step 1: Action Selection** 
```
📊 Food Calorie Tracking - Step 1/4
What would you like to do?

Options:
1️⃣ Log New Food - Add what you just ate
2️⃣ View Food Diary - See today's summary
3️⃣ Set Goals - Define nutrition targets
4️⃣ Check Progress - Review your stats

Choose an option (1-4) or tell me what you ate! 🍎
```

**User Options:**
- Number selection (1-4)
- Direct food description
- Natural language food logging

**Data Stored:** `tracking_action`, `user_choice`

#### **Step 2A: Food Logging Method (if chose 1)**
```
✅ Action: Log New Food

📝 Food Logging - Step 2/4
How would you like to add your food?

Methods:
1️⃣ Search Database - Find food by name
   "chicken breast", "apple", "greek yogurt"

2️⃣ Quick Entry - Common foods
   Breakfast, lunch, dinner basics

3️⃣ Manual Entry - Custom foods
   Restaurant meals, homemade dishes

Examples:
• "I ate grilled chicken with rice"
• "Log breakfast: oatmeal and banana"  
• "Add snack: trail mix"

What did you eat? 🍽️
```

**User Options:**
- Search database (1)
- Quick entry options (2)
- Manual entry (3)
- Direct food description

**Data Stored:** `food_method`

#### **Step 2B: Diary Viewing (if chose 2)**
```
✅ Action: View Food Diary

📊 Food Diary - Step 2/4

Today's Logged Foods:
• 08:30: Oatmeal with banana (320 cal)
• 12:45: Grilled chicken salad (350 cal)
• 15:20: Greek yogurt (180 cal)

Daily Totals:
• Calories: 850 / 1800 goal (47%)
• Protein: 45g / 120g goal (38%)
• Carbs: 95g / 225g goal (42%)
• Fat: 18g / 60g goal (30%)

What would you like to do next?
1️⃣ Log more food
2️⃣ View detailed breakdown
3️⃣ Set new goals
4️⃣ Export diary

Choose your next action! 📝
```

#### **Step 2C: Goal Setting (if chose 3)**
```
✅ Action: Set Goals

🎯 Goal Setting - Step 2/4

Current Goals:
• Daily Calories: 1800 cal
• Protein: 120g
• Carbs: 225g
• Fat: 60g

What would you like to adjust?
1️⃣ Daily calorie target
2️⃣ Protein goals
3️⃣ Carb/fat balance
4️⃣ Weight loss/gain goals

Which goal would you like to modify? ⚖️
```

#### **Step 2D: Progress Checking (if chose 4)**
```
✅ Action: Check Progress

📈 Progress Check - Step 2/4

This Week's Summary:
• Average Calories: 1,650 /day
• Days on Track: 5/7 days
• Weight: -1.2 lbs this week
• Streak: 12 days logging

Achievements:
🏆 Protein Master - Hit protein goals 6/7 days
⭐ Consistent Logger - 12 day streak
🥗 Veggie Champion - 5+ servings daily

What would you like to review?
1️⃣ Weekly trends
2️⃣ Nutrient breakdown
3️⃣ Goal progress
4️⃣ Achievement history

What interests you most? 📊
```

#### **Step 3: Detailed Input (varies by path)**

**Search Database Path:**
```
🔍 Method: Search Database

📝 Food Logging - Step 3/4

Enter the food you want to search for:

Popular searches:
• Chicken breast
• Greek yogurt  
• Apple
• Salmon
• Rice
• Eggs

Or be specific:
• "Grilled chicken breast"
• "Honeycrisp apple"
• "Brown rice cooked"

What food would you like to search for? 🔍
```

**Quick Entry Path:**
```
⚡ Method: Quick Entry

📝 Food Logging - Step 3/4

Quick food options:

Breakfast:
1️⃣ Oatmeal with banana (320 cal)
2️⃣ Greek yogurt with berries (180 cal)
3️⃣ Scrambled eggs (2 eggs, 140 cal)

Lunch/Dinner:
4️⃣ Grilled chicken salad (350 cal)
5️⃣ Turkey sandwich (420 cal)
6️⃣ Pasta with marinara (380 cal)

Snacks:
7️⃣ Apple with peanut butter (190 cal)
8️⃣ Mixed nuts (160 cal)
9️⃣ String cheese (80 cal)

Choose a number or describe your food! 🍽️
```

**Manual Entry Path:**
```
✏️ Method: Manual Entry

📝 Food Logging - Step 3/4

Manual food entry:

Please provide the following details:

Format: "[Food name] - [Amount] - [Calories]"

Examples:
• "Homemade pizza slice - 1 slice - 320 calories"
• "Restaurant pasta - 1 bowl - 450 calories" 
• "Protein smoothie - 16 oz - 280 calories"

Or just describe it:
• "Large coffee with milk and sugar"
• "Handful of trail mix"
• "Leftover dinner from yesterday"

What did you eat? ✏️
```

#### **Step 4: Confirmation & Results**
```
✅ Food logged successfully!

📊 Food Tracking - Step 4/4 (Results)

LOGGED: Grilled chicken breast - 6oz - 280 calories
• Protein: 52g
• Carbs: 0g  
• Fat: 6g
• Added at: 14:30

UPDATED DAILY TOTALS:
• Calories: 1,130 / 1800 goal (63%) ✅
• Protein: 97g / 120g goal (81%) ✅
• Carbs: 95g / 225g goal (42%)
• Fat: 24g / 60g goal (40%)

INSIGHTS:
🎯 Great protein choice! You're 81% to your protein goal
💡 Consider adding some carbs for energy
📈 On track for your daily calorie goal

Next Steps:
📝 Log more food
📊 View full food diary
🍽️ Plan your next meal
🛒 Create shopping list

What would you like to do next? 🍽️
Ready to start a new journey? Type /start! 🚀
```

### 🔄 Exit Points & Transitions

#### **Successful Completion**
- **Continue Logging** → Same journey with new food item
- **View Full Diary** → Detailed nutrition analysis view
- **Plan Meals** → Meal Planning Journey  
- **Shopping List** → Grocery Assistance Journey
- **Cook Recipe** → Cooking Guidance Journey
- **New Journey** → Main Menu

#### **Cross-Journey Transitions**
1. **To Meal Planning**: User wants to plan future meals based on logged data
2. **To Grocery Assistance**: User wants shopping list for planned foods
3. **To Cooking Guidance**: User wants to cook a logged recipe
4. **To Recipe Discovery**: User wants new recipe ideas based on nutrition gaps
5. **To Main Menu**: User wants different journey

### 📋 Session Data Persistence
- `tracking_action`: Selected action (log, view, goals, progress)
- `food_method`: Logging method (search, quick, manual)
- `logged_foods`: Array of daily food entries with timestamps
- `daily_totals`: Real-time calorie and macro totals
- `nutrition_goals`: User's custom daily targets
- `current_journey`: "food_tracking"

### 🎯 Key Features
- **Multiple Input Methods**: Search, quick select, manual entry
- **Real-time Tracking**: Instant updates to daily totals and progress
- **Goal Monitoring**: Custom nutrition targets with progress percentages
- **Rich Food Database**: Searchable nutrition information
- **Detailed Analysis**: Nutrient breakdowns and insights
- **Progress Tracking**: Weekly trends and achievement system
- **Export Capabilities**: Diary data export in multiple formats

### 📊 Food Database Structure

#### **Quick Entry Categories**
- Breakfast items (oatmeal, eggs, yogurt)
- Lunch/Dinner items (salads, sandwiches, pasta)
- Snack items (fruits, nuts, dairy)
- Common beverages (coffee, smoothies, water)

#### **Food Entry Information**
- Food Name
- Serving Size
- Calories per serving
- Protein content
- Carbohydrate content
- Fat content
- Micronutrients (when available)

### 🔍 Nutrition Calculation Logic
1. **Food Selection**: User chooses food item
2. **Portion Scaling**: Adjust nutrition based on serving size
3. **Daily Addition**: Add to running daily totals
4. **Goal Comparison**: Calculate progress percentages
5. **Insight Generation**: Provide recommendations based on gaps

### ⚡ Performance Optimizations
- **Session Persistence**: Food log data stored throughout session
- **Real-time Updates**: Instant calculation of totals and percentages
- **Quick Entry**: Pre-calculated common food nutrition
- **Smart Defaults**: Fallback portion sizes for easy logging

---

*This journey map represents the complete Food Tracking flow as implemented in the nutrition chatbot, showing all possible user paths and decision points.*