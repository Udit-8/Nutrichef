"""
Main Chatbot Manager
Orchestrates conversation flow and routes to appropriate journey modules
"""

from typing import Optional
from core.session_manager import SessionManager
from core.intent_classifier import IntentClassifier
from journeys.recipe_discovery import RecipeDiscoveryJourney
from journeys.calorie_meal_recommendation import CalorieMealRecommendationJourney
from journeys.meal_planning import MealPlanningJourney
from journeys.grocery_assistance import GroceryAssistanceJourney
from journeys.cooking_guidance import CookingGuidanceJourney
from journeys.food_calorie_tracking import FoodCalorieTrackingJourney

class ChatbotManager:
    """Main chatbot orchestrator"""
    
    def __init__(self, session_manager: SessionManager, intent_classifier: IntentClassifier, data_loader):
        self.session_manager = session_manager
        self.intent_classifier = intent_classifier
        self.data_loader = data_loader
        self.journeys = {
            'recipe_discovery': RecipeDiscoveryJourney(session_manager),
            'calorie_meal_recommendation': CalorieMealRecommendationJourney(session_manager),
            'meal_planning': MealPlanningJourney(data_loader, session_manager),
            'grocery_assistance': GroceryAssistanceJourney(data_loader, session_manager),
            'cooking_guidance': CookingGuidanceJourney(data_loader, session_manager),
            'food_calorie_tracking': FoodCalorieTrackingJourney(data_loader, session_manager)
        }
        self.greeting_given = False
    
    def start_conversation(self) -> None:
        """Start the main conversation loop"""
        if not self.greeting_given:
            self._show_greeting()
            self.greeting_given = True
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    self._show_goodbye()
                    break
                
                if not user_input:
                    print("🤖 Bot: I didn't catch that. Please tell me what you'd like to help with!")
                    continue
                
                self.session_manager.add_message('user', user_input)
                response = self._process_user_input(user_input)
                
                if response:
                    print(f"🤖 Bot: {response}")
                    self.session_manager.add_message('bot', response)
                
            except KeyboardInterrupt:
                self._show_goodbye()
                break
            except Exception as e:
                print(f"🤖 Bot: I'm sorry, something went wrong. Let's try again!")
                print(f"Error: {e}")
    
    def _show_greeting(self) -> None:
        """Display initial greeting"""
        print("🤖 Bot: Hello! I'm your nutrition assistant! I can help you with:")
        print("  🔍 Finding recipes")
        print("  📋 Planning meals")
        print("  👩‍🍳 Cooking guidance")
        print("  📊 Food calorie tracking")
        print("  🛒 Grocery assistance")
        print("  🥗 Healthy meal recommendations")
        print("\nWhat would you like to do today?")
    
    def _show_goodbye(self) -> None:
        """Display goodbye message"""
        print("\n🤖 Bot: Thanks for using the nutrition assistant! Stay healthy! 👋")
    
    def _process_user_input(self, user_input: str) -> Optional[str]:
        """Process user input and route to appropriate handler"""
        current_journey = self.session_manager.get_current_journey()
        
        # If user is already in a journey, continue with that journey
        if current_journey and current_journey in self.journeys:
            return self.journeys[current_journey].process_input(user_input)
        
        # Otherwise, classify intent and start appropriate journey
        intent = self.intent_classifier.classify_intent(user_input)
        
        if intent and intent in self.journeys:
            # Start the identified journey
            self.session_manager.start_journey(intent)
            return self.journeys[intent].start_journey()
        
        # No intent detected - provide help
        return self._provide_help_options()
    
    def _provide_help_options(self) -> str:
        """Provide help when intent is unclear"""
        return ("I'm not sure what you'd like to do. Try saying things like:\n"
                "• 'Find me a recipe'\n"
                "• 'Help me plan meals'\n"
                "• 'Create a meal plan'\n"
                "• 'Plan my meals for the week'\n"
                "• 'I need cooking help'\n"
                "• 'Log my food' or 'Track calories'\n"
                "• 'Show my food diary'\n"
                "• 'Add food to my log'\n"
                "• 'Create a grocery list'\n"
                "• 'Guide me through cooking'\n"
                "• 'Help me cook this recipe'\n"
                "• 'Find meals with 400 calories'\n"
                "• 'I need low calorie meals'")
    
    def get_session_info(self) -> dict:
        """Get current session information"""
        return self.session_manager.get_session_summary()