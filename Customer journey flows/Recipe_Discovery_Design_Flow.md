# 🔍 Recipe Discovery Customer Journey - Design Flow Chart

---

## **Flow Overview**
This flowchart maps the complete Recipe Discovery journey from initial user intent through all possible decision points to final endpoints, including cross-journey transitions.

---

## **📊 Complete Design Flow Chart**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                 USER INTENT                                     │
│  "I want to find a recipe" / "Show me recipes" / "What should I cook?"          │
│                          [ENTRY TRIGGER DETECTED]                               │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            STEP 1: GREETING & CONTEXT                           │
│  Bot: "I'd love to help you find the perfect recipe!"                           │
│  • Check user profile for dietary restrictions                                  │
│  • Load user preferences (cuisine, skill level, etc.)                           │
│  • Initialize search session                                                    │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    STEP 2: DISCOVERY METHOD SELECTION                           │
│  Bot: "How would you like to discover recipes today?"                           │
│                                                                                 │
│  [DECISION POINT 1: User chooses discovery method]                              │
└─────┬──────┬──────┬──────┬──────────────────────────────────────────────────────┘
      │      │      │      │      │
      ▼      ▼      ▼      ▼      ▼
   ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌─────────┐
   │ A  │ │ B  │ │ C  │ │ D  │ │    E    │
   │Cui-│ │Ing-│ │Die-│ │Time│ │Occasion │
   │sine│ │red-│ │tary│ │    │ │         │
   │    │ │ient│ │    │ │    │ │         │
   └─┬──┘ └─┬──┘ └─┬──┘ └─┬──┘ └────┬────┘
     │      │      │      │           │
     ▼      ▼      ▼      ▼           ▼

┌─────────────────────────────────────────────────────────────────────────────────┐
│                          PATH A: CUISINE SELECTION                              │
│  Bot: "What cuisine are you in the mood for?"                                   │
│                                                                                 │
│  [DECISION POINT 2A: Cuisine Choice]                                            │
│  Options from recipes_raw.json:                                                 │
│  • Mediterranean (recipe_001, recipe_022, recipe_033)                           │
│  • Asian (recipe_002, recipe_008, recipe_027)                                   │
│  • Italian (recipe_003, recipe_009, recipe_012, recipe_017, recipe_028)         │
│  • American (recipe_004, recipe_007, recipe_011, recipe_021, recipe_030)        │
│  • Mexican (recipe_005, recipe_020, recipe_023, recipe_031)                     │
│  • Indian (recipe_006, recipe_018)                                              │
│  • Thai (recipe_010, recipe_027, recipe_047)                                    │
│  • Korean (recipe_013)                                                          │
│  • Greek (recipe_014, recipe_032, recipe_035, recipe_041)                       │
│  • Moroccan (recipe_015, recipe_046)                                            │
│  • Japanese (recipe_016)                                                        │
│  • French (recipe_019, recipe_024)                                              │
│  • Vietnamese (recipe_040)                                                      │
│  • Caribbean (recipe_043)                                                       │
│  • Latin American (recipe_049)                                                  │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼ [Filter recipes by selected cuisine]
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
    [RESULTS FOUND]         [NO RESULTS]
          │                       │
          ▼                       ▼
    [GO TO STEP 4]          [SUGGEST ALTERNATIVES]
                                  │
                                  ▼
                            [RETURN TO STEP 2]

┌─────────────────────────────────────────────────────────────────────────────────┐
│                        PATH B: INGREDIENT SEARCH                                │
│  Bot: "What ingredients do you have available?"                                 │
│  "You can list them separated by commas."                                       │
│                                                                                 │
│  [DECISION POINT 2B: Ingredient Input]                                          │
│  [USER INPUT: Free text ingredients]                                            │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼ [Parse ingredients & match to recipe database]
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
    [INGREDIENTS MATCH]     [PARTIAL/NO MATCH]
          │                       │
          ▼                       ▼
    [RANK BY MATCH %]       [SUGGEST SUBSTITUTIONS]
          │                       │
          ▼                       ▼
    [GO TO STEP 4]          [OFFER ALTERNATIVES]
                                  │
                                  ▼
                            [RETURN TO STEP 2]

┌─────────────────────────────────────────────────────────────────────────────────┐
│                       PATH C: DIETARY RESTRICTIONS                              │
│  Bot: "Any dietary restrictions I should know about?"                           │
│                                                                                 │
│  [DECISION POINT 2C: Dietary Filter Selection]                                  │
│  Available filters from recipes_raw.json:                                       │
│  • Vegetarian (recipe_002, recipe_003, recipe_005, recipe_009, etc.)            │
│  • Vegan (recipe_002, recipe_005, recipe_015, recipe_018, recipe_026)           │ 
│  • Gluten-free (recipe_001, recipe_004, recipe_005, recipe_006, etc.)           │
│  • High-protein (recipe_001, recipe_007, recipe_008, recipe_011, etc.)          │ 
│  • Keto (recipe_004, recipe_009, recipe_035, recipe_038, recipe_042)            │
│  • Low-calorie (recipe_002, recipe_019, recipe_024)                             │
│  [Multiple selections allowed]                                                  │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼ [Filter recipes by dietary tags]
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
    [MATCHES FOUND]           [NO MATCHES]
          │                       │
          ▼                       ▼
    [GO TO STEP 4]          [RELAX CONSTRAINTS]
                                  │
                                  ▼
                            [RETURN TO STEP 2]

┌─────────────────────────────────────────────────────────────────────────────────┐
│                          PATH D: TIME-BASED SEARCH                              │
│  Bot: "How much time do you have to cook?"                                      │
│                                                                                 │
│  [DECISION POINT 2D: Time Constraint]                                           │
│  • Under 20 minutes (recipe_002, recipe_045)                                    │
│  • 20-45 minutes (recipe_001, recipe_004, recipe_005, recipe_007, etc.)         │
│  • 45+ minutes (recipe_003, recipe_006, recipe_013, recipe_040, recipe_046)     │
│  • No time limit                                                                │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼ [Filter by total_time from recipes]
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
    [TIME MATCHES]           [NO QUICK OPTIONS]
          │                       │
          ▼                       ▼
    [GO TO STEP 4]          [SUGGEST MEAL PREP]
                                  │
                                  ▼
                            [TRANSITION TO MEAL PLANNING]

┌─────────────────────────────────────────────────────────────────────────────────┐
│                        PATH E: OCCASION-BASED SEARCH                            │
│  Bot: "What's the occasion?"                                                    │
│                                                                                 │
│  [DECISION POINT 2E: Occasion Selection]                                        │
│  Map occasions to recipe attributes:                                            │
│  • Quick lunch → low prep_time + servings 1-2                                   │
│  • Family dinner → servings 4+ + medium difficulty                              │
│  • Date night → medium/hard difficulty + special cuisines                       │
│  • Party/entertaining → large servings + impressive dishes                      │
│  • Meal prep → easy difficulty + storage-friendly                               │
│  • Weekend cooking → any difficulty + longer cook times                         │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼ [Filter by occasion criteria]
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
    [OCCASION MATCHES]       [SUGGEST CLOSEST]
          │                       │
          ▼                       ▼
    [GO TO STEP 4]          [MODIFY SEARCH]
                                  │
                                  ▼
                            [RETURN TO STEP 2]

         ┌─────────────────────────────────────────────────────────┐
         │                    STEP 4: RESULTS DISPLAY              │
         │  Bot: "Here are some great recipes I found for you:"    │
         │                                                         │
         │  [DISPLAY 3-5 RECIPE CARDS]                             │
         │  Each card shows:                                       │
         │  • Recipe name + image                                  │
         │  • Prep time, cook time, difficulty                     │
         │  • Rating (from recipes_raw.json)                       │
         │  • Brief description                                    │
         │  • Dietary tags                                         │
         │                                                         │
         │  [DECISION POINT 3: User Action Choice]                 │
         └─────┬──────┬──────┬─────────────────────────────────────┘
               │      │      │
               ▼      ▼      ▼
         ┌─────────┐ ┌────┐ ┌─────────────┐
         │ View    │ │Save│ │ Get More    │
         │ Details │ │Recipe│ │ Options   │
         └────┬────┘ └─┬──┘ └──────┬──────┘
              │        │           │
              ▼        ▼           ▼
                                   │
    ┌─────────────────┐            │
    │ Add to Favorites│            │
    │ [ENDPOINT 1]    │            │
    │ Return to search│            │
    └─────────────────┘            │
                                   │
                    ┌──────────────┴──────────────┐
                    │ Expand Search Results       │
                    │ Show next 3-5 recipes       │
                    │ [LOOP BACK TO STEP 4]       │
                    └─────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                           STEP 5: RECIPE DETAIL VIEW                            │
│  [Triggered by "View Details" action]                                           │
│                                                                                 │
│  Display complete recipe information:                                           │
│  • Full ingredients list with quantities                                        │
│  • Complete cooking instructions                                                │
│  • Nutrition facts per serving                                                  │
│  • Equipment needed                                                             │
│  • Storage instructions                                                         │
│  • Substitution suggestions                                                     │
│                                                                                 │
│  [DECISION POINT 4: Final User Action]                                          │
└─────┬──────┬──────┬──────┬──────┬─────────────────────────────────────────────--┘
      │      │      │      │      │
      ▼      ▼      ▼      ▼      ▼
   ┌────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
   │ Start      │ │ Save to     │ │ Add to      │ │ Add to      │ │ Back to     │
   │ Cooking    │ │ Favorites   │ │ Meal Plan   │ │ Grocery     │ │ Results     │
   │            │ │             │ │             │ │ List        │ │             │
   └──────┬─────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
          │              │               │               │               │
          ▼              ▼               ▼               ▼               ▼
                                                                         │
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │
    │ TRANSITION  │ │ ENDPOINT 2  │ │ TRANSITION  │ │ TRANSITION  │      │
    │ TO:         │ │ Recipe      │ │ TO:         │ │ TO:         │      │
    │ Cooking     │ │ Saved       │ │ Meal        │ │ Grocery     │      │
    │ Guidance    │ │ Success     │ │ Planning    │ │ Assistance  │      │
    │ Journey     │ │ Message     │ │ Journey     │ │ Journey     │      │
    └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘      │
                                                                         │
                              ┌──────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────────────────┐
                    │ LOOP BACK TO STEP 4             │
                    │ Return to Results Display       │
                    │ User can select different recipe│
                    └─────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              ERROR HANDLING FLOWS                               │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ NO RESULTS FOUND (Any Search Path)                              │
    └─────┬───────────────────────────────────────────────────────────┘
          │
          ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │ [DECISION POINT: Recovery Action]                               │
    │ Bot: "I couldn't find recipes matching your criteria."          │
    │ "Would you like to:"                                            │
    └─────┬──────┬──────┬─────────────────────────────────────────────┘
          │      │      │
          ▼      ▼      ▼
    ┌─────────┐ ┌────┐ ┌─────────────────────────────────────────┐
    │ Broaden │ │Try │ │ Get Popular Recommendations         │
    │ Search  │ │New │ │ (Show top-rated recipes)            │
    │ Criteria│ │Path│ │                                     │
    └────┬────┘ └─┬──┘ └─────────────────┬───────────────────┘
         │        │                      │
         ▼        ▼                      ▼
         │ ┌─────────────┐         ┌─────────────┐
         │ │ RETURN TO   │         │ SHOW        │
         │ │ STEP 2      │         │ POPULAR     │
         │ │ (New Method)│         │ RECIPES     │
         │ └─────────────┘         │ GO TO STEP 4│
         │                         └─────────────┘
         │
         ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │ RELAX CONSTRAINTS                                               │
    │ • Remove least important filter                                 │
    │ • Expand time range                                             │
    │ • Include similar cuisines                                      │
    │ • Suggest ingredient substitutions                              │
    └─────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
                    ┌─────────────┐
                    │ RE-SEARCH   │
                    │ GO TO STEP 4│
                    └─────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                               ENDPOINT SUMMARY                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

    ENDPOINT 1: Recipe Saved to Favorites
    ├─ Success message displayed
    ├─ User can continue browsing or exit
    └─ Recipe stored in user profile

    ENDPOINT 2: User Satisfaction (Recipe Found)
    ├─ User found suitable recipe
    ├─ May bookmark for later
    └─ Natural conversation end

    TRANSITION 1: To Cooking Guidance Journey
    ├─ Recipe data passed to cooking flow
    ├─ User preferences maintained
    └─ Seamless experience continuation

    TRANSITION 2: To Meal Planning Journey  
    ├─ Recipe added to meal plan
    ├─ User can schedule for specific day
    └─ Nutrition data calculated

    TRANSITION 3: To Grocery Assistance Journey
    ├─ Recipe ingredients extracted
    ├─ Quantities calculated for servings
    └─ Shopping list generated

    LOOP BACK POINTS:
    ├─ Return to Results (Step 4)
    ├─ Return to Method Selection (Step 2)  
    ├─ Try Different Search Approach
    └─ Browse More Results

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            DATA DEPENDENCIES                                    │
└─────────────────────────────────────────────────────────────────────────────────┘

    FROM recipes_raw.json:
    ├─ recipe.cuisine → PATH A filtering
    ├─ recipe.ingredients → PATH B matching
    ├─ recipe.dietary_tags → PATH C filtering  
    ├─ recipe.total_time → PATH D filtering
    ├─ recipe.servings + recipe.difficulty → PATH E filtering
    ├─ recipe.calories_per_serving → Results display
    └─ All recipe data → Detail view

    FROM user_profiles.json (if available):
    ├─ dietary_restrictions → Auto-apply filters
    ├─ cuisine_preferences → Suggest popular cuisines
    ├─ cooking_skill → Filter by difficulty
    └─ favorites → Personalized recommendations

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FLOW STATISTICS                                    │ 
└─────────────────────────────────────────────────────────────────────────────────┘

    Total Decision Points: 7
    ├─ Method Selection (1)
    ├─ Path-specific choices (5: A, B, C, D, E)
    └─ Action selections (2: Results + Detail view)

    Possible Endpoints: 8
    ├─ Recipe Saved (2)
    ├─ Cross-journey Transitions (3)  
    ├─ Loop backs (2)
    └─ Natural conversation end (1)

    Error Recovery Paths: 3
    ├─ Broaden search criteria
    ├─ Try new discovery method
    └─ Show popular recommendations

    Average Flow Length: 4-6 steps
    Maximum Flow Length: 8 steps (with error recovery)
    Minimum Flow Length: 3 steps (direct to popular recipes)
```

---

## **🔍 Decision Points Analysis**

### **Critical Decision Points:**

1. **Discovery Method Selection** - Determines entire flow path
2. **Search Criteria Input** - Filters available recipes  
3. **Results Action Choice** - Determines user satisfaction vs continuation
4. **Detail View Actions** - Determines endpoint or journey transition

### **Data Integration Points:**

1. **Recipe Database Queries** - All paths filter recipes_raw.json
2. **User Profile Integration** - Personalization throughout flow
3. **Cross-Journey Data Transfer** - Seamless handoffs with context

### **Success Metrics:**

1. **Recipe Found & Saved** - Primary success indicator
2. **Transition to Other Journey** - Extended engagement
3. **User Returns to Browse** - Continued exploration
4. **Quick Resolution** - Efficient need fulfillment

This comprehensive flowchart covers all possible user paths, decision points, error scenarios, and endpoints for the Recipe Discovery customer journey, integrated with the raw data structure.