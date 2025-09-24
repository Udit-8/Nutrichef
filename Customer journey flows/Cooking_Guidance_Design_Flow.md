# 👨‍🍳 Cooking Guidance Customer Journey - Design Flow Chart

---

## **Flow Overview**
This flowchart maps the complete Cooking Guidance journey from recipe selection through interactive step-by-step cooking to completion, including all decision points, error handling, and cross-journey transitions.

---

## **📊 Complete Design Flow Chart**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                 USER INTENT                                     │
│  "Start Cooking" / "Guide me through cooking [recipe]" / "Help me cook"        │
│                          [ENTRY TRIGGER DETECTED]                              │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            ENTRY POINT DETERMINATION                           │
│                                                                                 │
│  [DECISION POINT 1: Entry Source]                                              │
└─────┬─────────────────────────────────────────────────────────────────────┬───┘
      │                                                                     │
      ▼                                                                     ▼
┌─────────────────┐                                              ┌─────────────────┐
│ PATH A:         │                                              │ PATH B:         │
│ From Recipe     │                                              │ Direct Request │
│ Discovery       │                                              │ (Recipe Name)   │
│ [Recipe Selected│                                              │ [Search Recipe  │
│  in Context]    │                                              │  Database]      │
└─────┬───────────┘                                              └─────┬───────────┘
      │                                                                │
      ▼                                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          STEP 1: RECIPE VALIDATION                             │
│  Load recipe data from recipes_raw.json and cooking_instructions_raw.json      │
│  • Verify recipe exists                                                        │
│  • Load cooking instructions                                                   │
│  • Check equipment requirements                                                │
│  • Estimate total cooking time                                                 │
│                                                                                 │
│  Bot: "Great! Let's cook [Recipe Name]. This will take about [X] minutes."     │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼ [Recipe found and loaded]
                      │
          ┌───────────┴─────────────┐
          ▼                         ▼
    [RECIPE FOUND]            [RECIPE NOT FOUND]
          │                         │
          ▼                         ▼
                              ┌─────────────────┐
                              │ ERROR HANDLING  │
                              │ "I couldn't     │
                              │ find that       │
                              │ recipe."        │
                              └─────┬───────────┘
                                    │
                                    ▼
                              [TRANSITION TO RECIPE DISCOVERY]

┌─────────────────────────────────────────────────────────────────────────────────┐
│                         STEP 2: SERVING SIZE SETUP                             │
│  Bot: "How many servings do you want to make?"                                 │
│  Default: [recipe.servings] servings                                           │
│                                                                                 │
│  [DECISION POINT 2: Serving Adjustment]                                        │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼ [User inputs desired servings]
                      │
          ┌───────────┴─────────────┐
          ▼                         ▼
    [SAME AS ORIGINAL]        [DIFFERENT AMOUNT]
          │                         │
          ▼                         ▼
    [KEEP ORIGINAL            [CALCULATE SCALING FACTOR]
     QUANTITIES]                   │
          │                       ▼
          │               [ADJUST ALL INGREDIENT 
          │                QUANTITIES PROPORTIONALLY]
          │                       │
          └───────────┬───────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      STEP 3: EQUIPMENT & INGREDIENT CHECK                      │
│  Display adjusted ingredient list and required equipment                       │
│                                                                                 │
│  Bot: "Here's what you'll need:"                                               │
│  • Show scaled ingredient list from cooking_instructions_raw.json              │
│  • Show equipment_needed array                                                 │
│  • Show estimated_active_time                                                  │
│                                                                                 │
│  [DECISION POINT 3: Proceed with Cooking]                                      │
│  "Should we proceed with cooking?"                                             │
└─────┬──────────────┬────────────────────────────────────────────────────────────┘
      │              │
      ▼              ▼
┌─────────────┐ ┌─────────────────────────────────────┐
│ "Yes, let's │ │ "No, not ready"                     │
│ start"      │ │                                     │
└──────┬──────┘ └─────┬───────────────────────────────┘
       │              │
       ▼              ▼
       │        ┌─────────────────────────────────────┐
       │        │ RETURN TO JOURNEY BEGINNING         │
       │        │ Bot: "No problem! Let's start over  │
       │        │ when you're ready."                 │
       │        │                                     │
       │        │ [RETURN TO STEP 1: RECIPE          │
       │        │ VALIDATION]                         │
       │        └─────────────────────────────────────┘
       │              
       │              
       │              
       │              
       │              
       │              
       │              
       │              
       │              
       │              
       │              
       └──────────────────────────────
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           STEP 4: PREP PHASE                                   │
│  Begin with steps marked phase: "prep" from cooking instructions               │
│                                                                                 │
│  Bot: "Let's start by preparing our ingredients."                              │
│  • Show prep steps with can_prep_ahead: true                                   │
│  • Allow user to work at their own pace                                        │
│  • Provide tips and visual cues for each prep step                             │
│                                                                                 │
│  [DECISION POINT 4: Prep Completion Check]                                     │
│  "Ready to start cooking?"                                                     │
└─────┬───────────────────────────────────────────────────────────────────────────┘
      │
      ▼ [User confirms prep complete]
      │
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    STEP 5: INTERACTIVE COOKING STEPS                           │
│                                                                                 │
│  Initialize cooking session:                                                   │
│  • current_step = first cooking phase step                                     │
│  • total_steps = total step count                                              │
│  • active_timers = []                                                          │
│  • session_status = "active"                                                   │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         COOKING STEP DISPLAY LOOP                              │
│                                                                                 │
│  For each step in cooking_instructions_raw.json:                               │
│  Display:                                                                      │
│  • "Step [current_step] of [total_steps]"                                      │
│  • step.instruction                                                            │
│  • step.duration_minutes (if applicable)                                       │
│  • step.temperature setting                                                    │
│  • step.tips                                                                   │
│  • step.visual_cues                                                            │
│                                                                                 │
│  [DECISION POINT 5: Step Navigation]                                           │
└─────┬──────┬──────┬──────┬──────┬─────────────────────────────────────────────┘
      │      │      │      │      │
      ▼      ▼      ▼      ▼      ▼
   ┌─────┐ ┌────┐ ┌────┐ ┌────┐ ┌─────────┐
   │Next │ │Rep-│ │Prev│ │Paus│ │  Timer  │
   │Step │ │eat │ │Step│ │ e  │ │ Start   │
   └──┬──┘ └─┬──┘ └─┬──┘ └─┬──┘ └────┬────┘
      │      │      │      │           │
      ▼      ▼      ▼      ▼           ▼

   ┌─────────────────────────────────────────────────────────────────────────────────┐
   │                              NAVIGATION ACTIONS                               │
   └─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────┐
    │ NEXT STEP ACTION                                        │
    │ if (current_step < total_steps):                        │
    │   current_step += 1                                     │
    │   [LOAD NEXT STEP]                                      │
    │ else:                                                   │
    │   [GO TO COMPLETION PHASE]                              │
    └─────────────────┬───────────────────────────────────────┘
                      │
                      ▼
                [RETURN TO STEP DISPLAY LOOP]

    ┌─────────────────────────────────────────────────────────┐
    │ REPEAT STEP ACTION                                      │
    │ • Re-display current step instructions                  │
    │ • Reset any active timers for this step                │
    │ • Provide additional tips if available                  │
    └─────────────────┬───────────────────────────────────────┘
                      │
                      ▼
                [RETURN TO STEP DISPLAY LOOP]

    ┌─────────────────────────────────────────────────────────┐
    │ PREVIOUS STEP ACTION                                    │
    │ if (current_step > 1):                                  │
    │   current_step -= 1                                     │
    │   [LOAD PREVIOUS STEP]                                  │
    │   Bot: "Going back to step [current_step]"              │
    │ else:                                                   │
    │   Bot: "You're already at the first step"               │
    └─────────────────┬───────────────────────────────────────┘
                      │
                      ▼
                [RETURN TO STEP DISPLAY LOOP]

    ┌─────────────────────────────────────────────────────────┐
    │ PAUSE COOKING ACTION                                    │
    │ • session_status = "paused"                            │
    │ • Save current progress                                 │
    │ • Pause all active timers                              │
    │ • Bot: "Cooking paused. Say 'resume' when ready."      │
    │                                                         │
    │ [DECISION POINT 5A: Resume or Exit]                    │
    └─────┬─────────────────────────────────────────────┬─────┘
          │                                             │
          ▼                                             ▼
    ┌─────────────┐                               ┌─────────────┐
    │ "Resume"    │                               │ "Stop       │
    │ Cooking     │                               │ Cooking"    │
    └──────┬──────┘                               └──────┬──────┘
           │                                             │
           ▼                                             ▼
    [RESUME STEP                               [SAVE PROGRESS &
     DISPLAY LOOP]                            EXIT TO MAIN MENU]

    ┌─────────────────────────────────────────────────────────┐
    │ TIMER MANAGEMENT                                        │
    │ if (step.timer_needed == true):                         │
    │   • Start countdown timer for step.duration_minutes    │
    │   • Add to active_timers array                         │
    │   • Display timer status                               │
    │   • Alert when timer expires                           │
    │                                                         │
    │ [TIMER COMPLETION ALERT]                                │
    │ Bot: "Timer finished! [step.visual_cues]"               │
    └─────────────────┬───────────────────────────────────────┘
                      │
                      ▼
                [RETURN TO STEP DISPLAY LOOP]

┌─────────────────────────────────────────────────────────────────────────────────┐
│                           HANDS-FREE FEATURES                                  │
│                                                                                 │
│  Auto-Updates:                                                                 │
│  • Progress tracking: "You're on step [X] of [Y]"                              │
│  • Time estimates: "[Z] minutes remaining"                                     │
│  • Contextual tips based on current phase                                      │
│  • Automatic timer alerts when durations complete                              │
│  • Visual progress indicators throughout cooking                               │
│  • Step completion confirmations                                               │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            ERROR HANDLING FLOWS                                │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ COOKING PROBLEMS DURING STEPS                                   │
    └─────┬───────────────────────────────────────────────────────────┘
          │
          ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │ [DECISION POINT: Problem Type]                                  │
    │ User reports: "This isn't working" / "Something's wrong"        │
    └─────┬──────┬──────┬─────────────────────────────────────────────┘
          │      │      │
          ▼      ▼      ▼
    ┌─────────┐ ┌────┐ ┌─────────────────────────────────────────┐
    │ Timing  │ │Temp│ │ Technique Issues                    │
    │ Issues  │ │ or │ │ (not browning, not thickening, etc.)│
    │         │ │Heat│ │                                     │
    └────┬────┘ └─┬──┘ └─────────────────┬───────────────────┘
         │        │                      │
         ▼        ▼                      ▼
         │ ┌─────────────┐         ┌─────────────┐
         │ │ PROVIDE     │         │ PROVIDE     │
         │ │ TEMPERATURE │         │ TECHNIQUE   │
         │ │ GUIDANCE    │         │ HELP        │
         │ └─────────────┘         │ Show tips   │
         │                         │ Visual cues │
         │                         │ Adjustments │
         │                         └─────────────┘
         │
         ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │ TIMING ADJUSTMENTS                                              │
    │ • Extend timer if needed                                        │
    │ • Provide visual doneness cues                                  │
    │ • Offer to continue with current step                           │
    │ • Show step.visual_cues for guidance                            │
    └─────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
                    ┌─────────────┐
                    │ CONTINUE    │
                    │ WITH STEP   │
                    │ GUIDANCE    │
                    └─────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                           STEP 6: COOKING COMPLETION                           │
│  Triggered when current_step > total_steps                                     │
│                                                                                 │
│  Bot: "Congratulations! You've finished cooking [recipe_name]!"                │
│  • Show serving suggestions                                                    │
│  • Display final plating instructions                                          │
│  • Calculate total cooking time taken                                          │
│                                                                                 │
│  [DECISION POINT 6: Completion Actions]                                        │
│  "How did it turn out?"                                                        │
└─────┬──────┬──────┬──────┬─────────────────────────────────────────────────────┘
      │      │      │      │
      ▼      ▼      ▼      ▼
   ┌─────┐ ┌────┐ ┌────┐ ┌─────────────┐
   │Rate │ │Add │ │Shar│ │ Cook        │
   │Reci-│ │Not-│ │e   │ │ Something   │
   │ pe  │ │es  │ │    │ │ Else        │
   └──┬──┘ └─┬──┘ └─┬──┘ └──────┬──────┘
      │      │      │           │
      ▼      ▼      ▼           ▼

    ┌─────────────────────────────────────────────────────────────────┐
    │ RATING & FEEDBACK                                               │
    │ • 1-5 star rating scale                                         │
    │ • Optional text feedback                                        │
    │ • Save to user profile                                          │
    │ • Update recipe rating in recipes_raw.json                      │
    │                                                                 │
    │ [ENDPOINT 1: Feedback Saved]                                    │
    │ Bot: "Thanks for the feedback!"                                 │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ COOKING NOTES                                                   │
    │ • Allow user to add personal notes for this cooking session    │
    │ • Track modifications made during cooking                       │
    │ • Notes available during current session only                  │
    │                                                                 │
    │ [ENDPOINT 2: Session Notes Recorded]                            │
    │ Bot: "Got it! I'll remember that for this cooking session."    │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ SHARE RECIPE                                                    │
    │ • Generate cooking summary                                      │
    │ • Include user's modifications                                  │
    │ • Share via email/text                                          │
    │                                                                 │
    │ [ENDPOINT 3: Recipe Shared]                                     │
    │ Bot: "Recipe shared successfully!"                              │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ COOK SOMETHING ELSE                                             │
    │ • Transition back to Recipe Discovery                           │
    │ • Carry cooking skill assessment                                │
    │ • Suggest complementary recipes                                 │
    │                                                                 │
    │ [TRANSITION 1: To Recipe Discovery Journey]                     │
    └─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            CROSS-JOURNEY TRANSITIONS                           │
└─────────────────────────────────────────────────────────────────────────────────┘

    FROM STEP 6 - Additional Actions Available:

    ┌─────────────────────────────────────────────────────────────────┐
    │ TRACK THIS MEAL                                                 │
    │ • Extract nutrition data from recipe                            │
    │ • Calculate actual servings consumed                            │
    │ • Log to food tracking                                          │
    │                                                                 │
    │ [TRANSITION 2: To Food Tracking Journey]                        │
    │ Pass: recipe_nutrition × servings_consumed                      │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ PLAN LEFTOVERS                                                  │
    │ • Calculate remaining servings                                  │
    │ • Suggest storage methods                                       │
    │ • Add to meal plan for later                                    │
    │                                                                 │
    │ [TRANSITION 3: To Meal Planning Journey]                        │
    │ Pass: leftover_servings, recipe_data                            │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │ SAVE TO FAVORITES                                               │
    │ • Add recipe to user favorites                                  │
    │ • Include user's modifications                                  │
    │ • Set quick-access for future cooking                           │
    │                                                                 │
    │ [ENDPOINT 4: Added to Favorites]                                │
    └─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              ENDPOINT SUMMARY                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

    ENDPOINT 1: Recipe Rated & Feedback Given
    ├─ User satisfaction captured
    ├─ Recipe database updated
    └─ Cooking session completed

    ENDPOINT 2: Cooking Notes Saved
    ├─ Personal modifications stored
    ├─ Future cooking reference created
    └─ Session completed with documentation

    ENDPOINT 3: Recipe Shared Successfully
    ├─ Recipe and modifications shared
    ├─ Social engagement completed
    └─ Session ends with sharing success

    ENDPOINT 4: Added to Favorites
    ├─ Quick access for future cooking
    ├─ Personal recipe collection updated
    └─ Session completed with save

    TRANSITION 1: To Recipe Discovery Journey
    ├─ Carry cooking success/feedback
    ├─ Suggest difficulty progression
    └─ Continue culinary exploration

    TRANSITION 2: To Food Tracking Journey
    ├─ Nutrition data transferred
    ├─ Actual consumption logged
    └─ Health goals tracking updated

    TRANSITION 3: To Meal Planning Journey
    ├─ Leftover planning initiated
    ├─ Storage recommendations provided
    └─ Future meal scheduling

    ERROR EXITS:
    ├─ Recipe not found → Recipe Discovery
    ├─ Missing ingredients → Grocery Assistance
    ├─ Equipment issues → Recipe substitution
    └─ Cooking failure → Problem solving or exit

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            DATA DEPENDENCIES                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

    FROM recipes_raw.json:
    ├─ recipe.name → Session identification
    ├─ recipe.servings → Default serving size
    ├─ recipe.ingredients[] → Quantity calculations
    ├─ recipe.nutrition → Nutrition tracking data
    └─ recipe.dietary_tags → User preference matching

    FROM cooking_instructions_raw.json:
    ├─ total_steps → Progress tracking
    ├─ estimated_active_time → Time planning
    ├─ equipment_needed[] → Setup requirements
    ├─ steps[].instruction → Step-by-step guidance
    ├─ steps[].duration_minutes → Timer management
    ├─ steps[].timer_needed → Timer triggers
    ├─ steps[].temperature → Heat settings
    ├─ steps[].tips → Contextual help
    ├─ steps[].visual_cues → Success indicators
    ├─ steps[].can_prep_ahead → Prep planning
    └─ steps[].phase → Cooking stage management

    FROM user_profiles.json (if available):
    ├─ cooking_skill → Difficulty appropriate tips
    ├─ kitchen_equipment → Equipment availability check
    ├─ previous_ratings → Personalized suggestions
    └─ dietary_restrictions → Safety alerts

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FLOW STATISTICS                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

    Total Decision Points: 8
    ├─ Entry source (1)
    ├─ Serving adjustment (1)
    ├─ Readiness checks (2: ingredients, prep)
    ├─ Step navigation (1: continuous)
    ├─ Problem handling (1: errors)
    ├─ Pause/resume (1)
    └─ Completion actions (1)

    Possible Endpoints: 7
    ├─ Successful completion with feedback (4)
    ├─ Cross-journey transitions (3)
    └─ Error exits (multiple)

    Session Management Features: 
    ├─ Timer management (multiple concurrent)
    ├─ Progress persistence (pause/resume)
    ├─ Step navigation (forward/backward)
    ├─ Voice command support
    ├─ Error recovery (technique help)
    └─ Hands-free operation

    Average Cooking Session: 
    ├─ Setup: 5-10 minutes
    ├─ Cooking: Varies by recipe (18-102 minutes)
    ├─ Completion: 2-5 minutes
    └─ Total: Recipe-dependent + ~10 minutes overhead

    Data Integration Points:
    ├─ Real-time ingredient scaling
    ├─ Dynamic timer management  
    ├─ Progress state persistence
    ├─ Cross-journey data transfer
    └─ User feedback collection

This comprehensive flowchart covers all aspects of the interactive cooking guidance experience, from initial setup through completion, with robust error handling and seamless integration with other customer journeys.
```