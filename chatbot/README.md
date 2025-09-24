# Nutrition Chatbot

A modular Python chatbot implementation for nutrition assistance, featuring multiple customer journeys including recipe discovery, meal planning, cooking guidance, calorie tracking, and grocery assistance.

## Features

- **Recipe Discovery**: Find recipes by cuisine, ingredients, dietary restrictions, cooking time, or occasion
- **Meal Planning**: Plan meals for different time periods with nutritional balance
- **Cooking Guidance**: Step-by-step cooking instructions with timer management
- **Calorie Tracking**: Track food intake and monitor nutritional goals
- **Grocery Assistance**: Generate smart shopping lists and manage ingredients

## Project Structure

```
chatbot/
├── main.py                 # Main entry point
├── core/                   # Core chatbot components
│   ├── chatbot_manager.py  # Main orchestrator
│   ├── intent_classifier.py # Intent recognition
│   └── session_manager.py  # Session state management
├── journeys/               # Customer journey implementations
│   ├── base_journey.py     # Abstract base class
│   └── recipe_discovery.py # Recipe discovery journey
├── data/                   # Data access layer
│   └── data_loader.py      # JSON data loading and access
└── utils/                  # Utility functions
```

## Installation

1. Clone or download the project
2. Navigate to the chatbot directory
3. Run the chatbot:

```bash
cd chatbot
python main.py
```

## Usage

1. Start the chatbot with `python main.py`
2. Follow the interactive prompts
3. Use natural language to express what you want to do:
   - "Find me a recipe"
   - "I need cooking help"
   - "Plan my meals"
   - "Track my calories"
   - "Create a grocery list"
   - "Find meals with 400 calories"
   - "I need low calorie meals"
   - "Show me high protein meals"

## Data Requirements

The chatbot expects JSON data files in the `../raw_data/` directory:
- `recipes_raw.json` - Recipe database
- `foods_nutrition_raw.json` - Nutritional information
- `meal_suggestions_raw.json` - Meal suggestions
- `cooking_instructions_raw.json` - Cooking instructions
- `grocery_support_raw.json` - Grocery and shopping data

## Currently Implemented

✅ **Recipe Discovery Journey** - Complete implementation
- Cuisine-based discovery
- Ingredient-based discovery  
- Dietary restriction filtering
- Time-based filtering
- Occasion-based discovery
- Recipe details and selection
- Cross-journey transitions

✅ **Calorie-Based Meal Recommendation Journey** - Complete implementation
- Flexible calorie goal input (specific/range/goal-based)
- Meal scope selection (single/daily/multi-day)
- Meal type and timing preferences
- Dietary restrictions filtering
- Smart meal search and matching
- Detailed nutritional analysis
- Session-based favorites
- Cross-journey transitions

## Coming Soon

🔄 **Other Journeys** (to be implemented):
- Meal Planning Journey
- Cooking Guidance Journey
- Food & Calorie Tracking Journey
- Grocery Assistance Journey
- Calorie-Based Meal Recommendations

## Architecture

The chatbot follows a modular architecture based on the customer journey design flows:

1. **Intent Classification**: Determines which journey to activate
2. **Session Management**: Tracks conversation state and context
3. **Journey Routing**: Routes to appropriate journey handler
4. **Step-by-Step Flow**: Follows predefined conversation flows
5. **Data Integration**: Accesses JSON data sources
6. **Cross-Journey Transitions**: Seamless movement between journeys

## Extending the Chatbot

To add a new customer journey:

1. Create a new class inheriting from `BaseJourney`
2. Implement the required abstract methods
3. Add intent patterns to `IntentClassifier`
4. Register the journey in `ChatbotManager`
5. Follow the step-by-step flow defined in your design document