# 🍳 Cooking Guidance Visual Journey Map

## Decision Tree Flow Chart

```
                                👤 USER STARTS
                                       |
                                       ▼
                    ┌─────────────────────────────────────────────┐
                    │        🍳 COOKING GUIDANCE JOURNEY         │
                    │     "Interactive cooking assistant"        │
                    └─────────────────────┬───────────────────────┘
                                          │
                                          ▼
                    ┌─────────────────────────────────────────────┐
                    │         🔍 STEP 1: RECIPE VALIDATION       │
                    │      "What would you like to cook?"        │
                    └─────────────────────┬───────────────────────┘
                                          │
              ┌───────────┬───────────────┼───────────────┬───────────┐
              ▼           ▼               ▼               ▼           ▼
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │📝 RECIPE    │ │📖 SHOW      │ │🔍 SEARCH    │ │💡 SUGGEST   │
      │   NAME      │ │AVAILABLE    │ │ DATABASE    │ │  RECIPES    │
      │Enter        │ │  RECIPES    │ │Find by      │ │Based on     │
      │specific     │ │(8 recipes)  │ │ingredients  │ │preferences  │
      │recipe       │ │             │ │             │ │             │
      └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
            │               │               │               │
            └───────────────┼───────────────┼───────────────┘
                            │               │
                            └───────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────────────┐
                    │      🍽️ STEP 2: SERVING SIZE SETUP        │
                    │   "How many people are you cooking for?"   │
                    └─────────────────────┬───────────────────────┘
                                          │
              ┌───────────┬───────────────┼───────────────┬───────────┐
              ▼           ▼               ▼               ▼           ▼
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │1️⃣ SINGLE     │ │2️⃣ COUPLE    │ │3️⃣ FAMILY    │ │✍️ CUSTOM    │
      │   SERVING   │ │ (2 people)  │ │ (4 people)  │ │ SERVINGS    │
      │Just for me  │ │For two      │ │Standard     │ │User-defined │
      │             │ │             │ │family size  │ │amount       │
      └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
            │               │               │               │
            └───────────────┼───────────────┼───────────────┘
                            │               │
                            └───────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────────────┐
                    │    🧰 STEP 3: EQUIPMENT & INGREDIENT CHECK │
                    │  "Let's check your kitchen setup & prep"   │
                    └─────────────────────┬───────────────────────┘
                                          │
              ┌───────────┬───────────────┼───────────────┬───────────┐
              ▼           ▼               ▼               ▼           ▼
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │🔧 EQUIPMENT │ │🥕 INGREDIENT│ │📏 PREP WORK │ │✅ ALL       │
      │   CHECK     │ │    CHECK    │ │   REVIEW    │ │   READY     │
      │Tools &      │ │Scaled       │ │Cutting,     │ │Everything   │
      │cookware     │ │ingredients  │ │prep tasks   │ │prepared     │
      └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
            │               │               │               │
            └───────────────┼───────────────┼───────────────┘
                            │               │
                            └───────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────────────┐
                    │          🥄 STEP 4: PREP PHASE             │
                    │      "Complete preparation tasks"          │
                    └─────────────────────┬───────────────────────┘
                                          │
              ┌───────────┬───────────────┼───────────────┬───────────┐
              ▼           ▼               ▼               ▼           ▼
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │✂️ CHOPPING  │ │🧄 MEASURING │ │🔥 HEATING   │ │✅ PREP      │
      │   TASKS     │ │ INGREDIENTS │ │  EQUIPMENT  │ │ COMPLETE    │
      │Cut, dice,   │ │Accurate     │ │Preheat oven,│ │Ready to     │
      │prep items   │ │measurements │ │heat pans    │ │start cook   │
      └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
            │               │               │               │
            └───────────────┼───────────────┼───────────────┘
                            │               │
                            └───────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────────────┐
                    │      👩‍🍳 STEP 5: INTERACTIVE COOKING       │
                    │         "Step-by-step cooking!"            │
                    └─────────────────────┬───────────────────────┘
                                          │
              ┌───────────┬───────────────┼───────────────┬───────────┐
              ▼           ▼               ▼               ▼           ▼
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │📝 CURRENT   │ │⏰ TIMER     │ │⬅️ PREVIOUS │ │➡️ NEXT     │
      │   STEP      │ │  ACTIVE     │ │   STEP      │ │   STEP      │
      │Detailed     │ │Count down   │ │Go back &    │ │Advance      │
      │instructions │ │for timing   │ │review       │ │cooking      │
      └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
            │               │               │               │
            │           ┌─────────────┐     │               │
            │           │💡 TIPS &    │     │               │
            │           │   TRICKS    │     │               │
            │           │Context help │     │               │
            │           │& cooking    │     │               │
            │           │advice       │     │               │
            │           └─────┬───────┘     │               │
            │                 │             │               │
            └─────────────────┼─────────────┼───────────────┘
                              │             │
                              └─────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────────────┐
                    │           🎉 STEP 6: COMPLETION             │
                    │        "Congratulations! Recipe done!"     │
                    └─────────────────────┬───────────────────────┘
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
  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
  │📊 LOG TO    │ │⭐ RATE      │ │🍳 COOK      │ │🛒 SHOP FOR  │ │🔄 NEW       │
  │ FOOD DIARY  │ │  RECIPE     │ │ ANOTHER     │ │ GROCERIES   │ │ JOURNEY     │
  │             │ │             │ │             │ │             │ │             │
  └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
        │               │               │               │               │
        ▼               ▼               ▼               ▼               ▼
  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
  │📊 FOOD      │ │💾 RECIPE    │ │🍳 COOKING   │ │🛒 GROCERY   │ │🏠 MAIN MENU │
  │ TRACKING    │ │ RATINGS &   │ │ GUIDANCE    │ │ ASSISTANCE  │ │   SELECT    │
  │  JOURNEY    │ │  FEEDBACK   │ │  JOURNEY    │ │  JOURNEY    │ │   JOURNEY   │
  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
        │               │               │               │               │
        ▼               ▼               ▼               ▼               ▼
  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
  │ COOKED MEAL │ │ SAVED USER  │ │ START NEW   │ │ INGREDIENTS │ │ CHOOSE NEW  │
  │LOGGED WITH  │ │ PREFERENCES │ │COOKING      │ │FOR FUTURE   │ │ NUTRITION   │
  │NUTRITION    │ │& FAVORITES  │ │  SESSION    │ │  RECIPES    │ │   JOURNEY   │
  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘

```

## 🎯 Journey Summary

**Entry Point**: 👤 User says "Start cooking" or selects Cooking Guidance

**Step 1**: 🔍 Recipe Validation (Recipe name, show available, search database, suggest recipes)
**Step 2**: 🍽️ Serving Size Setup (1 person, couple, family, custom servings)
**Step 3**: 🧰 Equipment & Ingredient Check (tools, ingredients, prep review, all ready)
**Step 4**: 🥄 Prep Phase (chopping, measuring, heating equipment, prep complete)
**Step 5**: 👩‍🍳 Interactive Cooking (step-by-step with timers, navigation, tips)
**Step 6**: 🎉 Completion (congratulations with results and next actions)

**Exit Points**: 
- 📊 Log to Diary → Food Tracking Journey
- ⭐ Rate Recipe → Recipe feedback system
- 🍳 Cook Another → New Cooking Guidance session
- 🛒 Shop for Groceries → Grocery Assistance Journey
- 🔄 New Journey → Main Menu

**Key Features**:
✅ 6-step interactive cooking assistance
✅ Real recipe database integration (8 recipes available)
✅ Automatic ingredient scaling for different serving sizes
✅ Interactive timers and step navigation
✅ Equipment and ingredient verification
✅ Contextual cooking tips and troubleshooting

## Detailed Journey Flow

### 🎯 Entry Points
- **Direct Intent**: "Help me cook", "Start cooking [recipe name]", "I want to cook something"
- **Menu Selection**: Choose "Cooking Guidance" from main menu
- **Cross-Journey**: From recipe discovery or meal planning wanting to cook

### 📊 Step-by-Step Breakdown

#### **Step 1: Recipe Validation** 
```
🍳 Cooking Guidance - Step 1/6

What would you like to cook today?

Options:
📝 Enter a specific recipe name
   "Chicken Curry", "Spaghetti Carbonara", "Beef Stir-fry"

📖 Show available recipes
   See all 8 recipes in our cooking database

🔍 Search by ingredients
   "What can I make with chicken and rice?"

💡 Get recipe suggestions
   Based on your preferences and dietary needs

Available Recipes:
• Chicken Curry
• Spaghetti Carbonara  
• Beef Stir-fry
• Vegetable Pad Thai
• Grilled Salmon
• Mushroom Risotto
• Turkey Meatballs
• Quinoa Buddha Bowl

What sounds delicious? 🍽️

CALL TO ACTION: Type a recipe name or "show available recipes"
```

**User Options:**
- Specific recipe name
- "show available recipes" command
- Ingredient-based search
- Request for suggestions

**Data Stored:** `requested_recipe`

#### **Step 2: Serving Size Setup**
```
✅ Recipe Selected: [Recipe Name]

🍽️ Cooking Guidance - Step 2/6

How many people are you cooking for?

Serving Options:
1️⃣ Single Serving - Just for me
   *Perfect portions for one person*

2️⃣ Couple (2 people) - For two
   *Ideal for date night or couple's meal*

3️⃣ Family (4 people) - Standard family size
   *Great for family dinners*

✍️ Custom Amount - Specify servings
   *Tell me exactly how many people*

Original recipe serves: [X] people
I'll automatically scale all ingredients for your chosen serving size!

How many servings do you need? 👥

CALL TO ACTION: Choose 1, 2, 3, or tell me the exact number
```

**User Options:**
- Number selection (1-3)
- Custom serving amount
- Natural language ("for 6 people")

**Data Stored:** `serving_size`, `ingredient_scaling_factor`

#### **Step 3: Equipment & Ingredient Check**
```
🧰 Cooking Guidance - Step 3/6
Recipe: [Recipe Name] for [X] servings

Let's check your kitchen setup and ingredients!

REQUIRED EQUIPMENT:
🔧 [Equipment list based on recipe]
• Large skillet or wok
• Medium saucepan  
• Sharp knife
• Cutting board
• Measuring cups

SCALED INGREDIENTS:
🥕 [Ingredient list scaled for serving size]
• 2 chicken breasts (1 lb total)
• 1 cup jasmine rice
• 2 tbsp vegetable oil
• 1 medium onion, diced
• 2 cloves garlic, minced

PREP TASKS:
📏 Before we start cooking:
• Dice onion and mince garlic
• Cut chicken into bite-sized pieces
• Measure out rice and spices

Do you have everything ready?

CALL TO ACTION: 
✅ Type "READY" when you have equipment and ingredients
🛒 Type "SHOP" if you need to get ingredients
❓ Type "HELP" for substitution suggestions
```

**User Options:**
- "READY" to proceed
- "SHOP" for grocery list
- "HELP" for substitutions
- Specific questions about equipment/ingredients

#### **Step 4: Prep Phase**
```
🥄 Cooking Guidance - Step 4/6
Let's get everything prepped before we start cooking!

PREP CHECKLIST:

✂️ CHOPPING TASKS:
□ Dice 1 medium onion (about 1 cup)
□ Mince 2 cloves garlic
□ Cut chicken into 1-inch pieces
□ [Additional prep based on recipe]

🧄 MEASURING:
□ Measure 1 cup rice
□ Measure 2 tbsp oil
□ [Additional measurements]

🔥 EQUIPMENT SETUP:
□ Preheat large skillet over medium-high heat
□ Fill medium saucepan with water for rice
□ [Recipe-specific setup]

Complete each task and check it off!

COOKING TIPS:
💡 Sharp knife makes chopping safer and faster
💡 Mise en place - having everything ready makes cooking smooth
💡 [Recipe-specific tips]

CALL TO ACTION:
✅ Type "PREP DONE" when all prep is complete
⏰ Type "START COOKING" to begin the interactive cooking steps
❓ Ask questions about any prep step
```

**User Options:**
- "PREP DONE" to confirm completion
- "START COOKING" to begin
- Questions about specific prep tasks

#### **Step 5: Interactive Cooking Steps**
```
👩‍🍳 Cooking Guidance - Step 5/6
[Recipe Name] - Cooking Step [X] of [Total]

CURRENT STEP:
🔥 Heat 2 tbsp oil in large skillet over medium-high heat
   Add diced onion and cook for 3-4 minutes until translucent

⏰ TIMER ACTIVE: 4 minutes
   [Timer countdown display]

WHAT TO WATCH FOR:
👀 Onions should sizzle when added to pan
👀 Stir occasionally to prevent burning
👀 Onions are ready when edges are golden

COOKING TIPS:
💡 Don't overcrowd the pan - this lowers temperature
💡 If onions brown too fast, reduce heat slightly

NAVIGATION:
⬅️ Previous Step - Review last instruction
➡️ Next Step - Continue when ready  
⏰ Set Timer - Start/stop cooking timers
❓ Get Help - Tips for this step

Current Progress: ████████░░ (Step [X] of [Total])

CALL TO ACTION:
➡️ Type "NEXT" when this step is complete
⏰ Type "TIMER" to set/check cooking timers
❓ Type "HELP" if you need assistance
```

**User Options:**
- "NEXT" to advance
- "PREVIOUS" to go back
- "TIMER" for timer controls
- "HELP" for step-specific assistance

#### **Step 6: Completion**
```
🎉 Cooking Guidance - Step 6/6

CONGRATULATIONS! Your [Recipe Name] is ready! 🍽️

FINAL RESULT:
✅ Perfectly cooked [dish description]
✅ Serves [X] people
✅ Total cooking time: [X] minutes
✅ Estimated calories per serving: [X]

NUTRITION HIGHLIGHTS:
📊 [Nutritional information based on recipe]
• Protein: [X]g per serving
• Carbohydrates: [X]g per serving  
• Healthy fats from [ingredients]

SERVING SUGGESTIONS:
🍽️ Serve hot with [suggested sides]
🌿 Garnish with [recommended garnishes]
💡 Pairs well with [beverage suggestions]

🎯 WHAT'S NEXT?

📊 Log this meal to your food diary
⭐ Rate this recipe (help improve recommendations)
🍳 Cook another recipe
🛒 Create shopping list for future cooking
🔄 Start a new nutrition journey

How was your cooking experience? 🌟

CALL TO ACTION:
📊 Type "LOG MEAL" to add to food diary
⭐ Type "RATE RECIPE" to provide feedback
🍳 Type "COOK AGAIN" for another recipe
```

### 🔄 Exit Points & Transitions

#### **Successful Completion**
- **Log Meal** → Food Tracking Journey with completed recipe nutrition
- **Rate Recipe** → Recipe feedback and preference learning system
- **Cook Another** → New Cooking Guidance session with different recipe
- **Shopping List** → Grocery Assistance Journey for future ingredients
- **New Journey** → Main Menu

#### **Mid-Journey Exits**
- **Need Ingredients** → Grocery Assistance Journey for missing items
- **Save for Later** → Save progress and return to Main Menu
- **Get Substitutions** → Recipe modification assistance

#### **Cross-Journey Transitions**
1. **To Grocery Assistance**: User needs missing ingredients
2. **To Food Tracking**: User wants to log completed meal
3. **To Recipe Discovery**: User wants different recipe options
4. **To Meal Planning**: User wants to schedule this recipe
5. **To Main Menu**: User wants different journey

### 📋 Session Data Persistence
- `requested_recipe`: Selected recipe name
- `recipe_data`: Full recipe details from database
- `cooking_instructions`: Step-by-step cooking guidance
- `serving_size`: Number of people being served
- `ingredient_scaling_factor`: Multiplication factor for ingredients
- `current_cooking_step`: Current step in cooking process
- `active_timers`: Array of active cooking timers
- `session_status`: Cooking session state (prep, cooking, complete)
- `current_journey`: "cooking_guidance"

### 🎯 Key Features
- **Real Database Integration**: 8 actual recipes with detailed instructions
- **Automatic Scaling**: Ingredients adjusted for any serving size
- **Interactive Timers**: Built-in timing for cooking steps
- **Step Navigation**: Go forward/backward through cooking process
- **Equipment Verification**: Check kitchen tools before starting
- **Contextual Tips**: Recipe-specific cooking advice
- **Error Recovery**: Restart options if issues occur

### 🍳 Recipe Database Structure

#### **Available Recipes (8 total)**
1. **Chicken Curry** - Traditional Indian-style curry
2. **Spaghetti Carbonara** - Classic Italian pasta dish
3. **Beef Stir-fry** - Quick Asian-inspired stir-fry
4. **Vegetable Pad Thai** - Vegetarian Thai noodle dish
5. **Grilled Salmon** - Healthy fish with herbs
6. **Mushroom Risotto** - Creamy Italian rice dish
7. **Turkey Meatballs** - Lean protein comfort food
8. **Quinoa Buddha Bowl** - Healthy grain bowl

#### **Recipe Information Structure**
- **Name**: Recipe title
- **Servings**: Original serving size
- **Cook Time**: Total preparation and cooking time
- **Difficulty**: Beginner/Intermediate/Advanced
- **Ingredients**: Detailed ingredient list with measurements
- **Equipment**: Required cooking tools
- **Instructions**: Step-by-step cooking guidance
- **Nutrition**: Calorie and macro information
- **Tips**: Recipe-specific cooking advice

### ⏰ Timer Management System
- **Multiple Timers**: Track several cooking processes simultaneously
- **Step Integration**: Timers automatically suggested for time-sensitive steps
- **Audio/Visual Alerts**: Notifications when timers complete
- **Pause/Resume**: Ability to pause cooking session
- **Timer History**: Track completed timing events

### 🔧 Equipment & Ingredient Logic
1. **Equipment Check**: Verify user has required tools
2. **Ingredient Scaling**: Mathematical scaling based on serving size
3. **Substitution Suggestions**: Alternative ingredients for missing items
4. **Prep Optimization**: Organize prep tasks for maximum efficiency
5. **Quality Checks**: Verify ingredient freshness and equipment function

### ⚡ Performance Optimizations
- **Database Caching**: Recipe data loaded once per session
- **Smart Navigation**: Skip irrelevant steps based on user experience
- **Error Handling**: Graceful recovery from cooking mistakes
- **Progress Saving**: Resume cooking sessions if interrupted
- **Mobile Optimization**: Works well with phone timers and notifications

---

*This journey map represents the complete Cooking Guidance flow as implemented in the nutrition chatbot, showing all possible user paths and decision points for the interactive cooking assistant.*