"""
Intent Classification for Nutrition Chatbot
Maps user input to specific journey intents
"""

import re
from typing import Dict, Optional

class IntentClassifier:
    """Simple rule-based intent classifier for customer journeys"""
    
    def __init__(self):
        self.intent_patterns = {
            # More specific patterns come first to avoid false matches
            'cooking_guidance': [
                r'guide.*through.*cooking', r'guide.*me.*cooking', r'walk.*through.*cooking', 
                r'help.*me.*cook', r'cooking.*guidance', r'interactive.*cooking', 
                r'cooking.*assistant', r'start.*cooking', r'cook.*this', r'step.*step.*cook',
                r'cooking.*help', r'help.*cook.*this', r'cook.*with.*me'
            ],
            'meal_planning': [
                r'meal.*plan', r'plan.*meal', r'weekly.*plan', r'plan.*week',
                r'menu.*plan', r'plan.*menu', r'create.*meal.*plan', r'generate.*meal.*plan',
                r'help.*plan', r'daily.*plan', r'plan.*eating', r'organize.*meal',
                r'schedule.*meal', r'meal.*schedule', r'eating.*schedule'
            ],
            'recipe_discovery': [
                r'find.*recipe', r'what.*cook', r'show.*recipe', r'recipe.*for', 
                r'want.*recipe', r'suggest.*recipe', r'search.*recipe', r'get.*recipe'
            ],
            'food_calorie_tracking': [
                r'track.*calorie', r'log.*food', r'calorie.*count', r'food.*diary',
                r'nutrition.*track', r'track.*food', r'add.*food', r'log.*meal',
                r'food.*log', r'track.*what.*ate', r'record.*food', r'diary.*food',
                r'nutrition.*diary', r'calorie.*diary', r'food.*tracking', r'my.*food.*diary',
                r'show.*diary', r'view.*diary', r'daily.*food', r'track.*eating',
                r'log.*breakfast', r'log.*lunch', r'log.*dinner', r'log.*snack'
            ],
            'grocery_assistance': [
                r'grocery.*list', r'shopping.*list', r'buy.*ingredient',
                r'what.*buy', r'grocery.*help', r'create.*grocery', r'generate.*grocery',
                r'need.*ingredients', r'shopping.*assistance', r'grocery.*shopping',
                r'make.*list', r'ingredient.*list', r'what.*ingredients',
                r'go.*shopping', r'need.*shop', r'grocery.*store'
            ],
            'calorie_meal_recommendation': [
                r'calorie.*meal', r'low.*calorie', r'healthy.*meal',
                r'diet.*meal', r'weight.*loss', r'calorie.*recommendation',
                r'meals.*with.*\d+.*calorie', r'find.*meal.*calorie',
                r'need.*\d+.*calorie', r'under.*\d+.*calorie', r'high.*calorie.*meal',
                r'moderate.*calorie', r'calorie.*goal', r'calorie.*target'
            ]
        }
    
    def classify_intent(self, user_input: str) -> Optional[str]:
        """
        Classify user input into one of the journey intents
        
        Args:
            user_input: User's message
            
        Returns:
            Intent name or None if no match
        """
        user_input_lower = user_input.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input_lower):
                    return intent
        
        return None
    
    def get_confidence_score(self, user_input: str, intent: str) -> float:
        """Get confidence score for a specific intent"""
        if intent not in self.intent_patterns:
            return 0.0
        
        user_input_lower = user_input.lower()
        matches = 0
        total_patterns = len(self.intent_patterns[intent])
        
        for pattern in self.intent_patterns[intent]:
            if re.search(pattern, user_input_lower):
                matches += 1
        
        return matches / total_patterns if total_patterns > 0 else 0.0