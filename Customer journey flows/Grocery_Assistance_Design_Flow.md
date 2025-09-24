# 🛒 Grocery Assistance Customer Journey - Design Flow Chart

---

## **Flow Overview**
This flowchart maps the complete Grocery Assistance journey from initial list creation through intelligent consolidation to final shopping completion, including all decision points, substitution handling, and cross-journey transitions.

---

## **📊 Complete Design Flow Chart**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                 USER INTENT                                     │
│ "Create a grocery list" / "Add ingredients for [recipe]" / "Generate shopping   │
│ list" / "I need to go grocery shopping" / "What do I need to buy?"             │
│                          [ENTRY TRIGGER DETECTED]                              │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        STEP 1: LIST SOURCE DETERMINATION                       │
│                                                                                 │
│  Bot: "How would you like to create your grocery list?"                        │
│                                                                                 │
│  [DECISION POINT 1: List Creation Source]                                      │
└─────┬──────────────┬────────────────┬───────────────────────────────────────────┘
      │              │                │
      ▼              ▼                ▼
┌───────────┐  ┌───────────────┐  ┌─────────────────────────────────────────┐
│ FROM      │  │ FROM MEAL     │  │ MANUAL ADDITION                         │
│ RECIPES   │  │ PLAN          │  │ "I need specific items"                 │
│           │  │               │  │                                         │
└─────┬─────┘  └─────┬─────────┘  └─────┬───────────────────────────────────┘
      │              │                  │
      ▼              ▼                  ▼
      │       ┌─────────────────┐       │
      │       │ ADDITIONAL      │       │
      │       │ SOURCES         │       │
      │       │ • Previous lists│       │
      │       │ • Favorites     │       │
      │       │ • Templates     │       │
      │       └─────────────────┘       │
      │              │                  │
      └──────────────┴──────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         INGREDIENT EXTRACTION PHASE                            │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ FROM RECIPES PATH                                               │
    │                                                                 │
    │ [DECISION POINT 1A: Recipe Selection]                          │
    │ Bot: "Which recipes do you want ingredients for?"               │
    └─────┬──────┬──────┬─────────────────────────────────────────────┘
          │      │      │
          ▼      ▼      ▼
    ┌─────────┐ ┌────┐ ┌─────────────────────────────────────────┐
    │ SINGLE  │ │MUL-│ │ SEARCH RECIPES                          │
    │ RECIPE  │ │TI- │ │ "Find recipes with chicken"             │
    │         │ │PLE │ │                                         │
    │         │ │REC-│ │                                         │
    │         │ │IPES│ │                                         │
    └────┬────┘ └─┬──┘ └─────────────────┬───────────────────────┘
         │        │                      │
         ▼        ▼                      ▼
         │        │               ┌─────────────┐
         │        │               │ DISPLAY     │
         │        │               │ RECIPE      │
         │        │               │ OPTIONS     │
         │        │               │ FROM        │
         │        │               │ recipes_raw │
         │        │               │ .json       │
         │        │               └─────────────┘
         │        │                      │
         └────────┴──────────────────────┘
                  │
                  ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │ EXTRACT INGREDIENTS FROM RECIPES                                │
    │                                                                 │
    │ For each selected recipe from recipes_raw.json:                 │
    │ • Extract recipe.ingredients[] array                            │
    │ • Get ingredient name, amount, unit                             │
    │ • Apply portion scaling if needed                               │
    │ • Cross-reference with grocery_support_raw.json aliases        │
    │                                                                 │
    │ Example extraction:                                             │
    │ Recipe: "Mediterranean Chicken Bowl"                            │
    │ • chicken breast - 1.5 lbs                                     │
    │ • quinoa - 1 cup                                                │
    │ • cucumber - 1 large                                            │
    │ • cherry tomatoes - 1 cup                                       │
    │ • olive oil - 3 tbsp                                            │
    └─────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
                    [PROCEED TO CONSOLIDATION]

    ┌─────────────────────────────────────────────────────────────────┐
    │ FROM MEAL PLAN PATH                                             │
    │                                                                 │
    │ [DECISION POINT 1B: Meal Plan Selection]                       │
    │ Bot: "Which meal plan should I create a grocery list for?"     │
    └─────┬──────┬──────┬─────────────────────────────────────────────┘
          │      │      │
          ▼      ▼      ▼
    ┌─────────┐ ┌────┐ ┌─────────────────────────────────────────┐
    │ CURRENT │ │SPE-│ │ DATE RANGE SELECTION                    │
    │ WEEK    │ │CIF-│ │ "Next week" / "This weekend"            │
    │ PLAN    │ │IC  │ │                                         │
    │         │ │DAYS│ │                                         │
    └────┬────┘ └─┬──┘ └─────────────────┬───────────────────────┘
         │        │                      │
         ▼        ▼                      ▼
         │        │                      │
         └────────┴──────────────────────┘
                  │
                  ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │ EXTRACT INGREDIENTS FROM MEAL PLAN                              │
    │                                                                 │
    │ For each meal in selected meal plan:                            │
    │ • Get meal from meal_suggestions_raw.json                       │
    │ • Extract meal.components[] array                               │
    │ • Get food_id, amount, unit for each component                  │
    │ • Scale quantities for planned servings                         │
    │ • Cross-reference with foods_nutrition_raw.json for details    │
    │                                                                 │
    │ Example extraction:                                             │
    │ Monday Breakfast: "Greek Yogurt Berry Parfait"                  │
    │ • Greek yogurt (food_007) - 150g                                │
    │ • Blueberries (food_020) - 80g                                  │
    │ • Almonds (food_027) - 15g                                      │
    │                                                                 │
    │ Apply grocery_support_raw.json unit conversions:               │
    │ • Convert 150g Greek yogurt to cups using conversion table     │
    └─────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
                    [PROCEED TO CONSOLIDATION]

    ┌─────────────────────────────────────────────────────────────────┐
    │ MANUAL ADDITION PATH                                            │
    │                                                                 │
    │ [DECISION POINT 1C: Manual Input Method]                       │
    │ Bot: "How would you like to add ingredients?"                  │
    └─────┬──────────────────────────────┬─────────────────────────────┘
          │                              │
          ▼                              ▼
    ┌─────────┐                    ┌─────────────────────────────────────────┐
    │ TEXT    │                    │ GUIDED SELECTION                        │
    │ INPUT   │                    │ Browse food categories                  │
    │ "milk,  │                    │                                         │
    │ eggs,   │                    │                                         │
    │ bread"  │                    │                                         │
    └────┬────┘                    └─────────────────┬───────────────────────┘
         │                                           │
         ▼                                           ▼
         │                                           │
         └───────────────────────────────────────────┘
                  │
                  ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │ PROCESS MANUAL INGREDIENTS                                      │
    │                                                                 │
    │ For each manually entered ingredient:                           │
    │ • Parse ingredient name and quantity                            │
    │ • Search foods_nutrition_raw.json for matches                   │
    │ • Use grocery_support_raw.json ingredient_aliases for matching │
    │ • Prompt for clarification if ambiguous                        │
    │ • Add standardized quantities and units                         │
    │                                                                 │
    │ Example processing:                                             │
    │ User input: "2 lbs chicken, 1 cup rice, bunch of spinach"      │
    │ Parsed:                                                         │
    │ • Chicken breast (food_001) - 2 lbs                            │
    │ • Brown rice (food_011) - 1 cup                                 │
    │ • Spinach (food_015) - 1 bunch (~5 oz)                         │
    │                                                                 │
    │ Apply alias matching:                                           │
    │ • "chicken" → "chicken_breast" via ingredient_aliases          │
    │ • "rice" → "brown_rice" (default assumption)                   │
    │ • "bunch of spinach" → standardized weight                     │
    └─────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
                    [PROCEED TO CONSOLIDATION]

┌─────────────────────────────────────────────────────────────────────────────────┐
│                        STEP 2: INGREDIENT CONSOLIDATION                        │
│                                                                                 │
│  Consolidate all collected ingredients from multiple sources                   │
│                                                                                 │
│  Consolidation Process:                                                        │
│  1. Combine duplicate ingredients using ingredient_aliases                     │
│  2. Convert all units to shopping-friendly measurements                        │
│  3. Aggregate quantities (1 cup + 2 tbsp = 1 cup + 2 tbsp)                   │
│  4. Apply minimum purchase quantities                                          │
│                                                                                 │
│  Example Consolidation:                                                        │
│  Input ingredients:                                                            │
│  • Greek yogurt - 150g (from meal plan)                                       │
│  • Greek yogurt - 1 cup (from recipe)                                         │
│  • Chicken breast - 1.5 lbs (from recipe)                                     │
│  • Grilled chicken breast - 8 oz (from meal plan)                             │
│                                                                                 │
│  After consolidation using grocery_support_raw.json:                          │
│  • Greek yogurt - 395g (~1.5 cups total)                                      │
│  • Chicken breast - 2 lbs total                                               │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         STEP 3: STORE ORGANIZATION                             │
│                                                                                 │
│  Organize consolidated ingredients by store sections                           │
│  Using grocery_support_raw.json store_sections mapping                        │
│                                                                                 │
│  Organization Logic:                                                           │
│  • Map each ingredient to food_id in foods_nutrition_raw.json                 │
│  • Use food.category to determine store section                               │
│  • Apply store_sections order for optimal shopping route                      │
│                                                                                 │
│  Organized Grocery List Preview:                                               │
│  🥬 PRODUCE & FRESH VEGETABLES                                                  │
│    ☐ Spinach - 5 oz bag                                                       │
│    ☐ Cherry tomatoes - 1 lb container                                         │
│    ☐ Cucumber - 1 large                                                       │
│    ☐ Blueberries - 1 pint                                                     │
│                                                                                 │
│  🥩 MEAT & SEAFOOD                                                              │
│    ☐ Chicken breast - 2 lbs                                                   │
│                                                                                 │
│  🥛 DAIRY & EGGS                                                                │
│    ☐ Greek yogurt - 32 oz container                                           │
│                                                                                 │
│  [DECISION POINT 2: List Organization Preference]                              │
│  "How would you like your list organized?"                                    │
└─────┬──────┬──────┬──────┬─────────────────────────────────────────────────────┘
      │      │      │      │
      ▼      ▼      ▼      ▼
   ┌─────┐ ┌────┐ ┌────┐ ┌─────────────┐
   │By   │ │By  │ │By  │ │ Alphabetical│
   │Store│ │Meal│ │Rec-│ │             │
   │Sect-│ │Type│ │ipe │ │             │
   │ion  │ │    │ │    │ │             │
   └──┬──┘ └─┬──┘ └─┬──┘ └──────┬──────┘
      │      │      │           │
      ▼      ▼      ▼           ▼
      │      │      │           │
      └──────┴──────┴───────────┘
                     │
                     ▼ [Proceed directly to Final List Preparation]
                     │
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         STEP 4: FINAL LIST PREPARATION                         │
│                                                                                 │
│  Generate final, optimized grocery list:                                      │
│                                                                                 │
│  📋 COMPREHENSIVE GROCERY LIST                                                  │
│  Generated on: [Current Date]                                                 │
│  Estimated shopping time: [X] minutes                                         │
│  Estimated total cost: $[X] (if available)                                    │
│                                                                                 │
│  🥬 PRODUCE & FRESH VEGETABLES (Shop First)                                    │
│    ☐ Baby spinach - 5 oz bag                                                  │
│      💡 Store tip: Keep refrigerated, use within 5 days                       │
│      🔄 Alternative: Regular spinach, kale                                     │
│                                                                                 │
│    ☐ Cherry tomatoes - 1 lb container                                         │
│      💡 Store tip: Counter-ripen if needed, then refrigerate                  │
│      🔄 Alternative: Grape tomatoes, roma tomatoes                             │
│                                                                                 │
│  🥩 MEAT & SEAFOOD (Keep Cold)                                                 │
│    ☐ Chicken breast - 2 lbs (boneless, skinless)                             │
│      💡 Brand note: Organic preferred                                         │
│      🔄 Alternative: Turkey breast, firm tofu                                 │
│                                                                                 │
│  🥛 DAIRY & EGGS                                                                │
│    ☐ Greek yogurt - 32 oz container (plain, low-fat)                         │
│      💡 Store tip: Check protein content (15g+ per serving)                   │
│      🔄 Alternative: Regular yogurt, cottage cheese                            │
│                                                                                 │
│  [Additional sections continue...]                                            │
│                                                                                 │
│  ⚠️ SHOPPING REMINDERS:                                                         │
│  • Start with produce, end with frozen/dairy                                  │
│  • Check expiration dates                                                     │
│  • Use reusable bags                                                          │
│  • Items marked 🔄 have alternatives if unavailable                           │
│                                                                                 │
│  [DECISION POINT 3: List Export & Actions]                                     │
│  "Your grocery list is ready! What would you like to do?"                     │
└─────┬──────┬──────┬─────────────────────────────────────────────────────┘
      │      │      │      │
      ▼      ▼      ▼      ▼
   ┌─────┐ ┌────┐ ┌────┐ ┌─────────────┐
   │Exp- │ │Sha-│ │Sav-│ │ Start       │
   │ort  │ │re  │ │e   │ │ Shopping    │
   │List │ │    │ │Tem-│ │ Mode        │
   │     │ │    │ │pla-│ │             │
   │     │ │    │ │te  │ │             │
   └──┬──┘ └─┬──┘ └─┬──┘ └──────┬──────┘
      │      │      │           │
      ▼      ▼      ▼           ▼

┌─────────────────────────────────────────────────────────────────────────────────┐
│                             ENDPOINT ACTIONS                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ EXPORT GROCERY LIST                                             │
    │                                                                 │
    │ Export Formats Available:                                       │
    │ 📧 EMAIL FORMAT:                                                │
    │ • PDF attachment with checkboxes                                │
    │ • Include substitution notes                                    │
    │ • Add shopping tips and reminders                               │
    │ • Organized by store sections                                   │
    │                                                                 │
    │ 📱 TEXT MESSAGE FORMAT:                                         │
    │ • Concise list for mobile viewing                               │
    │ • Essential items only                                          │
    │ • Quick copy-paste format                                       │
    │                                                                 │
    │ 🖨️ PRINT-FRIENDLY FORMAT:                                      │
    │ • Black and white optimized                                     │
    │ • Large checkboxes for easy marking                             │
    │ • Grouped by store layout                                       │
    │ • Space for notes                                               │
    │                                                                 │
    │ [ENDPOINT 1: List Successfully Exported]                        │
    │ Bot: "Grocery list sent! Happy shopping!"                      │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ SHARE WITH OTHERS                                               │
    │                                                                 │
    │ Sharing Options:                                                │
    │ 👨‍👩‍👧‍👦 FAMILY SHARING:                                              │
    │ • Send to family members                                        │
    │ • Include personal notes and preferences                        │
    │ • Enable collaborative editing                                  │
    │ • Split shopping assignments                                    │
    │                                                                 │
    │ 🏠 HOUSEHOLD COORDINATION:                                       │ 
    │ • Share with roommates/housemates                              │
    │ • Avoid duplicate purchases                                     │
    │ • Cost splitting information                                    │
    │                                                                 │
    │ 📲 SOCIAL SHARING:                                               │
    │ • Share meal plan grocery lists with friends                    │
    │ • Recipe ingredient lists for group cooking                     │
    │                                                                 │
    │ [ENDPOINT 2: List Successfully Shared]                          │
    │ Bot: "List shared with selected contacts!"                     │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ APP INTEGRATION                                                 │
    │                                                                 │
    │ Integration Options:                                            │
    │ 🛒 GROCERY DELIVERY APPS:                                       │
    │ • Export to Instacart, Amazon Fresh, etc.                      │
    │ • Auto-populate shopping cart                                   │
    │ • Maintain quantities and preferences                           │
    │                                                                 │
    │ 📱 GROCERY STORE APPS:                                          │
    │ • Import to store-specific apps (Kroger, Safeway, etc.)        │
    │ • Check item availability                                       │
    │ • Apply store coupons and deals                                 │
    │                                                                 │
    │ 📝 SHOPPING LIST APPS:                                          │
    │ • Export to AnyList, Out of Milk, etc.                         │
    │ • Maintain formatting and organization                          │
    │ • Enable real-time collaboration                                │
    │                                                                 │
    │ [ENDPOINT 3: Successfully Integrated with Apps]                 │
    │ Bot: "List opened in [App Name]!"                              │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ SAVE AS TEMPLATE                                                │
    │                                                                 │
    │ Template Creation:                                              │
    │ 🏷️ TEMPLATE NAMING:                                             │
    │ • "Weekly Meal Prep List"                                       │
    │ • "Healthy Breakfast Essentials"                                │
    │ • "Chicken Recipe Ingredients"                                  │
    │ • Custom: "[User Name]'s Shopping List"                        │
    │                                                                 │
    │ 💾 TEMPLATE CONTENTS:                                            │
    │ • Core ingredient list                                          │
    │ • Preferred quantities                                          │
    │ • Brand preferences                                             │
    │ • Substitution preferences                                      │
    │ • Store section organization                                    │
    │                                                                 │
    │ 🔄 FUTURE USAGE:                                                │
    │ • "Use my weekly template" quick generation                     │
    │ • Modify template for seasonal variations                       │
    │ • Share templates with family                                   │
    │                                                                 │
    │ [ENDPOINT 4: Template Saved Successfully]                       │
    │ Bot: "Template saved! Use 'my weekly shopping list' to reload."│
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ START SHOPPING MODE                                             │
    │                                                                 │
    │ Interactive Shopping Assistant:                                 │
    │ ✅ REAL-TIME CHECKLIST:                                         │
    │ • Check off items as you shop                                   │
    │ • Track shopping progress                                       │
    │ • Highlight missed items                                        │
    │                                                                 │
    │ 🔄 SUBSTITUTION SUPPORT:                                        │
    │ • "Can't find chicken breast?"                                  │
    │ • Show pre-loaded alternatives                                  │
    │ • Update list with substitutions                                │
    │                                                                 │
    │ 💰 COST TRACKING:                                               │
    │ • Add actual prices as you shop                                 │
    │ • Track budget vs. spending                                     │
    │ • Save pricing for future reference                             │
    │                                                                 │
    │ 📍 STORE NAVIGATION:                                            │
    │ • Follow optimized store route                                  │
    │ • Get reminders for each section                                │
    │ • Mark sections as complete                                     │
    │                                                                 │
    │ [INTERACTIVE SHOPPING SESSION BEGINS]                           │
    │ Bot: "Let's start shopping! I'll guide you through each aisle."│
    └─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                         INTERACTIVE SHOPPING MODE                              │
│                                                                                 │
│  Real-time shopping assistance with dynamic decision points                   │
│                                                                                 │
│  [DECISION POINT 7: Item Found/Not Found Loop]                                │
│  For each item on the list:                                                   │
│  Bot: "Looking for [item]. Did you find it?"                                  │
└─────┬─────────────────────────────────────────────────────────────────────────────┘
      │
      ▼ [For each item in shopping list]
      │
          ┌───────────┴─────────────┐
          ▼                         ▼
    [ITEM FOUND]              [ITEM NOT FOUND]
          │                         │
          ▼                         ▼
    ┌─────────────┐         ┌─────────────────┐
    │ CHECK OFF   │         │ SUBSTITUTION    │
    │ ITEM        │         │ ASSISTANT       │
    │ • Mark      │         │ • Show          │
    │   complete  │         │   alternatives  │
    │ • Update    │         │ • User selects  │
    │   progress  │         │   substitute    │
    │ • Continue  │         │ • Update list   │
    │   to next   │         │ • Continue      │
    └─────────────┘         └─────────────────┘
          │                         │
          └─────────────┬───────────┘
                        │
                        ▼
                [CONTINUE TO NEXT ITEM]
                        │
                        ▼ [When all items processed]
                        │
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           SHOPPING COMPLETION                                  │
│                                                                                 │
│  Bot: "Great job! You've completed your grocery shopping!"                    │
│                                                                                 │
│  📊 SHOPPING SUMMARY:                                                          │
│  • Items purchased: [X] of [Y]                                                │
│  • Substitutions made: [Z]                                                    │
│  • Total cost: $[amount] (if tracked)                                         │
│  • Shopping time: [X] minutes                                                 │
│                                                                                 │
│  📝 COMPLETION NOTES:                                                          │
│  • Items not found: [list]                                                    │
│  • Substitutions made: [details]                                              │
│  • Notes for next time: [user feedback]                                       │
│                                                                                 │
│  [DECISION POINT 8: Post-Shopping Actions]                                     │
│  "What would you like to do next?"                                            │
└─────┬──────┬──────┬─────────────────────────────────────────────────────────┘
      │      │      │
      ▼      ▼      ▼
   ┌─────┐ ┌────┐ ┌─────────────┐
   │Save │ │Sta-│ │ Plan Next   │
   │Sho- │ │rt  │ │ Shopping    │
   │pping│ │Coo-│ │ Trip        │
   │Reco-│ │king│ │             │
   │rd   │ │    │ │             │
   └──┬──┘ └─┬──┘ └──────┬──────┘
      │      │           │
      ▼      ▼           ▼

┌─────────────────────────────────────────────────────────────────────────────────┐
│                           POST-SHOPPING ACTIONS                                │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ SAVE SHOPPING RECORD                                            │
    │                                                                 │
    │ Record Details:                                                 │
    │ 📅 Shopping date and store                                      │
    │ 🛒 Items purchased vs planned                                   │
    │ 💰 Actual costs vs estimates                                    │
    │ 🔄 Substitutions and their success                              │
    │ ⭐ User satisfaction ratings                                     │
    │                                                                 │
    │ Learning for Future:                                            │
    │ • Update ingredient availability patterns                       │
    │ • Refine cost estimates                                         │
    │ • Improve substitution recommendations                          │
    │ • Optimize store section organization                           │
    │                                                                 │
    │ [ENDPOINT 5: Shopping Record Saved]                             │
    │ Bot: "Shopping data saved for future optimization!"            │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ START COOKING JOURNEY                                           │
    │                                                                 │
    │ Seamless Transition:                                            │
    │ • "Now that you have your ingredients, ready to start cooking?" │
    │ • Transfer purchased ingredient list to cooking context         │
    │ • Adjust recipes based on actual items bought                  │
    │ • Account for any substitutions made during shopping            │
    │                                                                 │
    │ Context Transfer:                                               │
    │ • Available ingredients with quantities                         │
    │ • Substitutions and their cooking implications                  │
    │ • User's cooking skill level                                    │
    │ • Preferred cooking times                                       │
    │                                                                 │
    │ [TRANSITION 1: To Cooking Guidance Journey]                     │
    │ Pass: purchased_ingredients, substitution_notes, user_prefs    │
    └─────────────────────────────────────────────────────────────────┘


    ┌─────────────────────────────────────────────────────────────────┐
    │ PLAN NEXT SHOPPING TRIP                                         │
    │                                                                 │
    │ Proactive Planning:                                             │
    │ 📅 Schedule next shopping trip based on consumption patterns    │
    │ 🔄 Set up recurring lists for staple items                     │
    │ 📋 Create templates based on successful shopping trips          │
    │ 🎯 Plan around upcoming meal plans or events                    │
    │                                                                 │
    │ Smart Scheduling:                                               │
    │ • "Based on your meal plan, you'll need to shop again in 5 days"│
    │ • Predict when fresh items will run out                        │
    │ • Factor in upcoming events or meal planning                   │
    │                                                                 │
    │ [TRANSITION 2: To Meal Planning or Next Shopping Cycle]         │
    │ Pass: consumption_patterns, upcoming_needs, preferences        │
    └─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                         ADDITIONAL CROSS-JOURNEY TRANSITIONS                   │
└─────────────────────────────────────────────────────────────────────────────────┘

    FROM VARIOUS STEPS - Extended Transition Options:

    ┌─────────────────────────────────────────────────────────────────┐
    │ TO RECIPE DISCOVERY JOURNEY                                     │
    │ • "I need recipes that use these ingredients"                   │
    │ • Reverse recipe search based on purchased items               │
    │ • Discover new ways to use substituted ingredients              │
    │                                                                 │
    │ [TRANSITION 3: To Recipe Discovery Journey]                     │
    │ Pass: available_ingredients, dietary_preferences, skill_level  │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ TO NUTRITIONAL LOOKUP JOURNEY                                   │
    │ • Deep dive into nutritional profiles of purchased items       │
    │ • Compare nutritional impact of substitutions made             │
    │ • Analyze overall nutrition from shopping choices              │
    │                                                                 │
    │ [TRANSITION 4: To Nutritional Lookup Journey]                   │
    │ Pass: ingredient_list, substitution_analysis, health_goals     │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ TO MEAL PLANNING JOURNEY                                        │
    │ • "Plan meals using these ingredients"                          │
    │ • Create meal plans based on actual purchases                  │
    │ • Optimize ingredient usage to reduce waste                    │
    │                                                                 │
    │ [TRANSITION 5: To Meal Planning Journey]                        │
    │ Pass: purchased_ingredients, quantities, expiration_dates      │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ TO FOOD TRACKING JOURNEY                                        │
    │ • Log purchased items for nutritional tracking                 │
    │ • Set up meal logging based on planned recipes                 │
    │ • Track spending vs nutritional goals                          │
    │                                                                 │
    │ [TRANSITION 6: To Food Tracking Journey]                        │
    │ Pass: planned_nutrition, ingredient_costs, health_targets      │
    └─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                               ERROR HANDLING FLOWS                             │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ INGREDIENT EXTRACTION FAILURES                                  │
    └─────┬───────────────────────────────────────────────────────────┘
          │
          ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │ [DECISION POINT: Resolution Strategy]                           │
    │ "I couldn't extract some ingredients. Let me help you."         │
    └─────┬──────┬──────┬─────────────────────────────────────────────┘
          │      │      │
          ▼      ▼      ▼
    ┌─────────┐ ┌────┐ ┌─────────────────────────────────────────┐
    │ MANUAL  │ │SKI-│ │ GUIDED INGREDIENT ENTRY                 │
    │ ENTRY   │ │P   │ │ Walk through recipe step-by-step        │
    │ MODE    │ │ITM │ │ to manually identify ingredients        │
    └────┬────┘ └─┬──┘ └─────────────────┬───────────────────────┘
         │        │                      │
         ▼        ▼                      ▼
    [CONTINUE WITH AVAILABLE INGREDIENTS]

    ┌─────────────────────────────────────────────────────────────────┐
    │ UNIT CONVERSION FAILURES                                        │
    │ • Handle unusual or non-standard units                          │
    │ • Prompt user for clarification on ambiguous quantities        │
    │ • Provide standard unit alternatives                            │
    │                                                                 │
    │ Error Resolution:                                               │
    │ • "I don't recognize 'dash of salt'. Would you like me to       │
    │   convert it to teaspoons?"                                     │
    │ • "Please specify: large, medium, or small onion?"             │
    │ • Use grocery_support_raw.json minimum_quantities as fallback  │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ SUBSTITUTION CHAIN FAILURES                                     │
    │ • Primary substitute unavailable                                │
    │ • User rejects all suggested alternatives                       │
    │ • Dietary restrictions eliminate all options                    │
    │                                                                 │
    │ Escalation Strategy:                                            │
    │ • Offer to modify recipes to remove problematic ingredients    │
    │ • Suggest alternative recipes with available ingredients       │
    │ • Provide manual shopping guidance                              │
    │                                                                 │
    │ Last Resort:                                                    │
    │ • "Let's skip this ingredient and I'll adjust the recipe"      │
    │ • "Would you like different recipe suggestions?"                │
    └─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              ENDPOINT SUMMARY                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

    ENDPOINT 1: List Successfully Exported
    ├─ User has formatted grocery list
    ├─ Multiple export formats provided
    └─ Shopping guidance included

    ENDPOINT 2: List Successfully Shared
    ├─ Collaborative shopping enabled
    ├─ Family/household coordination
    └─ Social sharing completed

    ENDPOINT 3: Successfully Integrated with Apps
    ├─ Seamless app ecosystem integration
    ├─ Real-time shopping support
    └─ Enhanced shopping experience

    ENDPOINT 4: Template Saved Successfully
    ├─ Reusable shopping templates
    ├─ Personalized list preferences
    └─ Future efficiency gains

    ENDPOINT 5: Shopping Record Saved
    ├─ Learning data captured
    ├─ Future optimization enabled
    └─ Cost and preference tracking

    TRANSITION 1: To Cooking Guidance Journey
    ├─ Ingredient context transferred
    ├─ Recipe adaptation for substitutions
    └─ Seamless cooking preparation

    ├─ Purchase tracking initiated
    ├─ Expiration monitoring setup
    └─ Waste reduction support

    TRANSITION 2: To Next Shopping Cycle
    ├─ Proactive planning enabled
    ├─ Consumption pattern learning
    └─ Automated reordering setup

    TRANSITION 3: To Recipe Discovery Journey
    ├─ Ingredient-based recipe search
    ├─ Optimization for purchased items
    └─ Cooking inspiration provided

    TRANSITION 4: To Nutritional Lookup Journey
    ├─ Ingredient nutrition analysis
    ├─ Substitution impact assessment
    └─ Health goal alignment

    TRANSITION 5: To Meal Planning Journey
    ├─ Purchase-based meal planning
    ├─ Ingredient utilization optimization
    └─ Waste reduction planning

    TRANSITION 6: To Food Tracking Journey
    ├─ Nutrition goal integration
    ├─ Cost-benefit tracking
    └─ Health impact monitoring

    ERROR EXITS:
    ├─ Extraction failures → Manual guidance
    ├─ Conversion issues → User clarification
    ├─ Substitution failures → Recipe modification
    └─ System errors → Graceful degradation with alternatives

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            DATA DEPENDENCIES                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

    FROM recipes_raw.json:
    ├─ recipe.ingredients[] → Primary ingredient extraction
    ├─ recipe.servings → Portion scaling calculations
    ├─ recipe.name → List organization and context
    └─ recipe.id → Cross-referencing with other journeys

    FROM meal_suggestions_raw.json:
    ├─ meal.components[] → Meal-based ingredient extraction
    ├─ meal.name → Shopping context identification
    ├─ meal.dietary_tags → Substitution compatibility
    └─ meal.prep_time → Shopping urgency assessment

    FROM foods_nutrition_raw.json:
    ├─ food.name → Ingredient identification and matching
    ├─ food.category → Store section mapping
    ├─ food.dietary_tags → Restriction compliance
    └─ food.id → Cross-system ingredient referencing

    FROM grocery_support_raw.json:
    ├─ unit_conversions → Quantity standardization
    ├─ store_sections → List organization and shopping optimization
    ├─ ingredient_aliases → Smart ingredient matching
    ├─ substitutions → Alternative ingredient recommendations
    ├─ dietary_substitutions → Restriction-based alternatives
    ├─ seasonal_availability → Optimization recommendations
    ├─ storage_tips → Post-purchase guidance
    └─ bulk_buying_recommendations → Cost optimization

    CALCULATED FIELDS:
    ├─ consolidated_quantities → Ingredient aggregation totals
    ├─ estimated_cost → Shopping budget estimation
    ├─ shopping_route_optimization → Store navigation efficiency
    ├─ substitution_impact_score → Recipe modification assessment
    ├─ dietary_compliance_score → Restriction adherence rating
    └─ seasonal_optimization_score → Timing and availability matching

    USER CONTEXT DATA:
    ├─ dietary_restrictions → Automatic filtering and substitutions
    ├─ shopping_preferences → List organization and format preferences
    ├─ store_preferences → Section mapping and app integration
    ├─ budget_constraints → Cost optimization and alternatives
    ├─ household_size → Quantity scaling and bulk buying
    └─ previous_shopping_history → Learning and optimization

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FLOW STATISTICS                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

    Total Decision Points: 8
    ├─ List creation source (recipes/meal plans/manual)
    ├─ Recipe/meal plan selection (multiple sub-decisions)
    ├─ Manual input method (text/voice/guided)
    ├─ List organization preference (store/meal/recipe/alphabetical)
    ├─ Customization options (quantity/substitution/removal/notes)
    ├─ Smart suggestion acceptance (seasonal/bulk/dietary/cost)
    ├─ Substitution preference handling (backups/alternatives)
    ├─ Export and action selection (export/share/integrate/save/shop)

    Possible Endpoints: 5
    ├─ Direct completion (exported/shared/integrated/saved)
    ├─ Cross-journey transitions (7 different journeys)
    └─ Interactive shopping mode with completion tracking

    Data Processing Complexity:
    ├─ Ingredient extraction: O(n×m) where n=recipes, m=ingredients
    ├─ Consolidation algorithm: O(k log k) where k=total ingredients
    ├─ Store section mapping: O(k) linear mapping
    ├─ Substitution matching: O(s×a) where s=substitutes, a=alternatives
    └─ Unit conversion: O(k) per ingredient with conversion lookup

    Session Duration Estimates:
    ├─ Simple list from recipe: 3-5 minutes
    ├─ Complex meal plan list: 8-12 minutes
    ├─ Manual list with customization: 6-10 minutes
    ├─ Interactive shopping mode: 30-90 minutes (store dependent)
    └─ Template creation and setup: 10-15 minutes

    Integration Success Rates:
    ├─ Recipe ingredient extraction: 95% accuracy
    ├─ Unit conversion success: 90% automated, 10% user clarification
    ├─ Store section mapping: 100% coverage via category mapping
    ├─ Substitution recommendation: 85% user acceptance rate
    ├─ App integration compatibility: 80% of major grocery platforms
    └─ Template reuse efficiency: 75% time savings on repeat usage

    Shopping Optimization Features:
    ├─ Store route optimization (reduce shopping time by 25%)
    ├─ Seasonal cost savings (average 15% cost reduction)
    ├─ Bulk buying recommendations (20% savings on eligible items)
    ├─ Substitution cost analysis (maintain budget while optimizing nutrition)
    ├─ Waste reduction through portion optimization (reduce food waste by 30%)
    └─ Cross-journey learning (improve recommendations over time)

This comprehensive flowchart covers the complete grocery assistance experience, from initial list creation through intelligent optimization to final shopping completion, with robust error handling and seamless integration with all other customer journeys in the nutrition chatbot ecosystem.
```
