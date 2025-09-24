# 🔍 Recipe Discovery Visual Journey Map

## Decision Tree Flow Chart

```
                                👤 USER STARTS
                                       |
                                       ▼
                    ┌─────────────────────────────────────────────┐
                    │        🔍 RECIPE DISCOVERY JOURNEY         │
                    │          "Find me recipes"                  │
                    └─────────────────────┬───────────────────────┘
                                          │
                                          ▼
                    ┌─────────────────────────────────────────────┐
                    │           📋 STEP 1: CUISINE TYPE          │
                    │      "What cuisine are you looking for?"   │
                    └─────────────────────┬───────────────────────┘
                                          │
                ┌────────────┬────────────┼────────────┬────────────┬────────────┬────────────┐
                ▼            ▼            ▼            ▼            ▼            ▼            ▼
         ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
         │1️⃣ ITALIAN   │  │2️⃣ ASIAN     │ │3️⃣ MEXICAN   │ │4️⃣ AMERICAN  │ │5️⃣ MEDITERR   │ │6️⃣ INDIAN    │ │✍️ CUSTOM    
         │Pasta, Pizza │ │Stir-fry     │ │Tacos        │ │Burgers      │ │Greek        │ │Curry        │ │Specific     │
         │Risotto      │ │Curry        │ │Burritos     │ │BBQ          │ │Turkish      │ │Biryani      │ │Dish Name    │
         └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
               │               │               │               │               │               │               │
               └───────────────┼───────────────┼───────────────┼───────────────┼───────────────┼───────────────┘
                               │               │               │               │               │
                               └───────────────┼───────────────┼───────────────┼───────────────┘
                                               │               │               │
                                               └───────────────┼───────────────┘
                                                               │
                                                               ▼
                    ┌─────────────────────────────────────────────────────────────────────┐
                    │                ⏰ STEP 2: TIME & SKILL LEVEL                         │
                    │            "How much time do you have for cooking?"                 │
                    └─────────────────────────────┬───────────────────────────────────────┘
                                                  │
                    ┌─────────────┬───────────────┼───────────────┬─────────────┬─────────────┬─────────────┐
                    ▼             ▼               ▼               ▼             ▼             ▼             ▼
            ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
            │1️⃣ QUICK &    │ │2️⃣ MODERATE   │ │3️⃣ ELABORATE  │   │4️⃣ NO TIME    │ │🥄 BEGINNER   │ │👨‍🍳 INTERMED │ │👩‍🍳 ADVANCED │
            │   EASY        │ │               │ │               │ │   LIMIT       │ │   LEVEL       │ │   LEVEL       │ │   LEVEL       │
            │15-30 minutes  │ │30-60 minutes  │ │1+ hours       │ │Any duration   │ │Simple recipes │ │Moderate skill │ │Complex tech   │
            └───────┬───────┘ └───────┬───────┘ └───────┬───────┘ └───────┬───────┘ └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
                    │                 │                 │                 │                 │                 │                 │
                    └─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┘
                                      │                 │                 │                 │                 │
                                      └─────────────────┼─────────────────┼─────────────────┼─────────────────┘
                                                        │                 │                 │
                                                        └─────────────────┼─────────────────┘
                                                                          │
                                                                          ▼
                    ┌─────────────────────────────────────────────────────────────────────────────────────────┐
                    │                     🥗 STEP 3: DIETARY RESTRICTIONS                                    │
                    │                "Any dietary needs or preferences?"                                     │
                    └─────────────────────────────────┬───────────────────────────────────────────────────────┘
                                                      │
                    ┌─────────┬─────────┬─────────┬───┼───┬─────────┬─────────┬─────────┬─────────┬─────────┐
                    ▼         ▼         ▼         ▼   ▼   ▼         ▼         ▼         ▼         ▼         ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │1️⃣ VEGETAR │ │2️⃣ VEGAN    │ │3️⃣ GLUTEN   │ │4️⃣ LOW-CARB │ │5️⃣ DAIRY    │ │6️⃣ HIGH     │ │7️⃣ LOW      │
            │   IAN 🥕   │ │   🌱        │ │   FREE 🚫🌾 │ │   KETO 🥩   │ │   FREE 🚫🥛 │ │   PROTEIN💪 │ │   SODIUM🧂  │
            └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
                  │               │               │               │               │               │               │
            ┌─────────────┐ ┌─────────────┐       │               │               │               │               │
            │8️⃣ NO       │  │✍️ CUSTOM     │         │               │               │               │               │
            │RESTRICTIONS│ │ALLERGIES    │        │               │               │               │               │
            │    ✅       │ │Nuts, etc.   │       │               │               │               │               │
            └─────┬───────┘ └─────┬───────┘       │               │               │               │               │
                  │               │               │               │               │               │               │
                  └───────────────┼───────────────┼───────────────┼───────────────┼───────────────┼───────────────┘
                                  │               │               │               │               │
                                  └───────────────┼───────────────┼───────────────┼───────────────┘
                                                  │               │               │
                                                  └───────────────┼───────────────┘
                                                                  │
                                                                  ▼
                    ┌─────────────────────────────────────────────────────────────────────────────────────────┐
                    │                      🎉 STEP 4: PERSONALIZED RESULTS                                   │
                    │               "Perfect! Here are your personalized recipes"                            │
                    │                                                                                         │
                    │  🍝 RECIPE RECOMMENDATIONS (3-5 tailored recipes)                                     │
                    │  • Recipe Name, Cook Time, Calories, Description                                       │
                    │  • Based on: [Cuisine] + [Time] + [Dietary] preferences                               │
                    └─────────────────────────────┬───────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
                                      ┌─────────────────────────┐
                                      │    🎯 NEXT ACTIONS      │
                                      │  "What interests you?"  │
                                      └─────────┬───────────────┘
                                                │
                    ┌─────────┬─────────┬───────┼───────┬─────────┬─────────┐
                    ▼         ▼         ▼       ▼       ▼         ▼         ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │📋 GET FULL │ │🛒 CREATE    │ │👩‍🍳 START   │ │📊 LOG TO    │ │🔄 START NEW │
            │   RECIPE   │ │ SHOPPING    │ │  COOKING    │ │ FOOD DIARY  │ │  JOURNEY    │
            │            │ │    LIST     │ │             │ │             │ │             │
            └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘ └─────┬───────┘
                  │               │               │               │               │
                  ▼               ▼               ▼               ▼               ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │📖 RECIPE   │ │🛒 GROCERY   │ │🍳 COOKING   │ │📊 FOOD      │ │🏠 MAIN MENU │
            │  DETAILS    │ │ ASSISTANCE  │ │ GUIDANCE    │ │ TRACKING    │ │   SELECT    │
            │   VIEW      │ │  JOURNEY    │ │  JOURNEY    │ │  JOURNEY    │ │   JOURNEY   │
            └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
                  │               │               │               │               │
                  ▼               ▼               ▼               ▼               ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │  DETAILED   │ │ ORGANIZED   │ │INTERACTIVE  │ │ NUTRITION   │ │ CHOOSE NEW  │
            │ INGREDIENTS │ │SHOPPING LIST│ │STEP-BY-STEP │ │ DATA LOGGED │ │ NUTRITION   │
            │ & INSTRUC   │ │BY CATEGORIES│ │  COOKING    │ │             │ │   JOURNEY   │
            └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘

```

## 🎯 Journey Summary

**Entry Point**: 👤 User says "Find me recipes" or selects Recipe Discovery

**Step 1**: 📋 Cuisine Selection (Italian, Asian, Mexican, American, Mediterranean, Indian, Custom)
**Step 2**: ⏰ Time & Skill (Quick/Moderate/Elaborate + Beginner/Intermediate/Advanced)  
**Step 3**: 🥗 Dietary Restrictions (Vegetarian, Vegan, Gluten-free, etc.)
**Step 4**: 🎉 Personalized Results (3-5 tailored recipes)

**Exit Points**: 
- 📖 Recipe Details → Full recipe view
- 🛒 Shopping List → Grocery Assistance Journey
- 🍳 Start Cooking → Cooking Guidance Journey  
- 📊 Food Logging → Food Tracking Journey
- 🔄 New Journey → Main Menu

**Key Features**:
✅ 4-step progressive disclosure
✅ Flexible input (numbers or natural language)
✅ Personalized recommendations
✅ Multiple exit pathways to other journeys
✅ Rich recipe database organized by preferences

## Detailed Journey Flow

### 🎯 Entry Points
- **Direct Intent**: "Find me Italian recipes", "Show me vegetarian dishes"
- **Menu Selection**: Choose "Recipe Discovery" from main menu
- **Cross-Journey**: From other journeys needing recipe recommendations

### 📊 Step-by-Step Breakdown

#### **Step 1: Cuisine Selection** 
```
🔍 Recipe Discovery - Step 1/4
What type of cuisine or dish are you looking for?

Popular Options:
1️⃣ Italian (Pasta, Pizza, Risotto)
2️⃣ Asian (Stir-fry, Curry, Noodles)
3️⃣ Mexican (Tacos, Burritos, Enchiladas)
4️⃣ American (Burgers, BBQ, Comfort food)
5️⃣ Mediterranean (Greek, Turkish, Middle Eastern)
6️⃣ Indian (Curry, Biryani, Tandoori)

Or specify:
• A specific dish name
• Main ingredient (chicken, beef, vegetarian)
• Dietary preference (low-carb, gluten-free, vegan)

What sounds good to you? 🍽️
```

**User Options:**
- Number selection (1-6)
- Custom cuisine name
- Specific dish request
- Ingredient-based request
- Dietary preference

**Data Stored:** `cuisine_choice`

#### **Step 2: Time & Skill Preference**
```
⏰ Time noted: [User's Choice]

🔍 Recipe Discovery - Step 2/4
How much time do you have for cooking?

Time Options:
1️⃣ Quick & Easy (15-30 minutes)
2️⃣ Moderate (30-60 minutes)
3️⃣ Elaborate (1+ hours)
4️⃣ No time limit

Skill Level:
🥄 Beginner - Simple recipes
👨‍🍳 Intermediate - Moderate complexity
👩‍🍳 Advanced - Complex techniques

Reply with time preference and skill level!
```

**User Options:**
- Time preference (1-4 or custom)
- Skill level (beginner/intermediate/advanced)
- Combined input

**Data Stored:** `time_preference`

#### **Step 3: Dietary Restrictions**
```
🔍 Recipe Discovery - Step 3/4
Any dietary restrictions or preferences?

Common Restrictions:
1️⃣ Vegetarian 🥕
2️⃣ Vegan 🌱
3️⃣ Gluten-free 🚫🌾
4️⃣ Low-carb/Keto 🥩
5️⃣ Dairy-free 🚫🥛
6️⃣ High-protein 💪
7️⃣ Low-sodium 🧂
8️⃣ No restrictions ✅

Allergies to avoid:
• Nuts, shellfish, eggs, etc.

What dietary needs should I consider? 🥗
```

**User Options:**
- Number selection (1-8)
- Custom dietary restriction
- Multiple restrictions
- Allergy specifications

**Data Stored:** `dietary_restrictions`

#### **Step 4: Personalized Results**
```
🎉 Perfect! Here are your personalized recipes:

🔍 Recipe Discovery - Step 4/4 (Results)
Your preferences: [Cuisine], [Time], [Dietary]

🍝 RECIPE RECOMMENDATIONS:

[3-5 Personalized Recipe Cards]
• Name, Cook Time, Calories, Description
• Tailored to user's exact preferences

Next Steps:
📋 Get full recipe with instructions
🛒 Create shopping list for ingredients
👩‍🍳 Start cooking with step-by-step guidance
📊 Log this meal in your food diary

Which recipe interests you most? 🍽️
Ready to start cooking? Type /start to begin a new journey! 🚀
```

**User Options:**
- Select specific recipe
- Request full recipe details
- Generate shopping list
- Start cooking guidance
- Log to food diary
- Start new journey

### 🔄 Exit Points & Transitions

#### **Successful Completion**
- **Recipe Selected** → Cooking Guidance Journey
- **Shopping List** → Grocery Assistance Journey  
- **Food Logging** → Food Tracking Journey
- **New Journey** → Main Menu

#### **Cross-Journey Transitions**
1. **To Cooking Guidance**: User selects recipe to cook
2. **To Grocery Assistance**: User wants shopping list
3. **To Food Tracking**: User wants to log recipe
4. **To Meal Planning**: User wants to schedule recipe
5. **To Main Menu**: User wants different journey

### 📋 Session Data Persistence
- `cuisine_choice`: Selected cuisine type
- `time_preference`: Cooking time and skill level
- `dietary_restrictions`: Dietary needs and restrictions
- `selected_recipes`: Generated recipe recommendations
- `current_journey`: "recipe_discovery"

### 🎯 Key Features
- **Flexible Input**: Numbers, keywords, or natural language
- **Personalization**: Adapts recommendations to user preferences
- **Rich Recipe Database**: Organized by cuisine and dietary needs
- **Clear Progression**: Step counter and progress indicators
- **Multiple Exit Points**: Seamless journey transitions
- **User Guidance**: Clear instructions and options at each step

### 📊 Recipe Database Structure

#### **Cuisine Categories**
- Italian (default, vegetarian, vegan)
- Asian (default, vegetarian, vegan)  
- Mexican (default, vegetarian, vegan)
- American (default, vegetarian, vegan)
- Mediterranean (default, vegetarian, vegan)
- Indian (default, vegetarian, vegan)

#### **Recipe Information**
- Recipe Name
- Cook Time
- Calorie Count
- Description
- Dietary Tags
- Difficulty Level

### 🔍 Search Algorithm
1. **Primary Filter**: Cuisine selection
2. **Secondary Filter**: Time constraints
3. **Tertiary Filter**: Dietary restrictions
4. **Ranking**: By relevance and user preferences
5. **Presentation**: Top 3-5 most relevant recipes

### ⚡ Performance Optimizations
- **Cached Results**: Common combinations pre-computed
- **Progressive Loading**: Steps load incrementally
- **Smart Defaults**: Fallback to popular options
- **Error Handling**: Graceful degradation for invalid inputs

---

*This journey map represents the complete Recipe Discovery flow as implemented in the nutrition chatbot, showing all possible user paths and decision points.*