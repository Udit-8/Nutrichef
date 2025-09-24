"""
Calorie and Nutrition Calculation Utilities
For Calorie-Based Meal Recommendation Journey
"""

from typing import Dict, Tuple, List, Any

class CalorieCalculator:
    """Utility class for calorie and nutrition calculations"""
    
    # Daily calorie distribution percentages
    DAILY_DISTRIBUTION = {
        'breakfast': 0.25,  # 25%
        'lunch': 0.35,      # 35%  
        'dinner': 0.35,     # 35%
        'snack': 0.05       # 5%
    }
    
    # Calorie goal categories
    CALORIE_GOALS = {
        'low': {'min': 0, 'max': 300, 'description': 'Low calorie meals (under 300 calories)'},
        'moderate': {'min': 300, 'max': 450, 'description': 'Moderate calorie meals (300-450 calories)'},
        'high': {'min': 450, 'max': 1000, 'description': 'High calorie meals (450+ calories)'}
    }
    
    # Meal type calorie ranges (based on 1800 cal/day average)
    MEAL_TYPE_RANGES = {
        'breakfast': {'min': 185, 'max': 315},  # 200-350 typical
        'lunch': {'min': 285, 'max': 445},      # 300-450 typical
        'dinner': {'min': 295, 'max': 465},     # 350-500 typical
        'snack': {'min': 50, 'max': 200}       # 50-200 typical
    }
    
    @staticmethod
    def parse_calorie_input(user_input: str) -> Tuple[int, int, str]:
        """
        Parse user calorie input and return min, max calories and input type
        
        Returns:
            Tuple of (min_calories, max_calories, input_type)
        """
        user_input = user_input.lower().strip()
        
        # Try to extract numbers from the input
        import re
        numbers = re.findall(r'\d+', user_input)
        
        # Range input: "300-500" or "between 300 and 500"
        if len(numbers) == 2:
            min_cal = int(numbers[0])
            max_cal = int(numbers[1])
            if min_cal > max_cal:
                min_cal, max_cal = max_cal, min_cal
            return min_cal, max_cal, "range"
        
        # Specific number: "400 calories"
        elif len(numbers) == 1:
            target = int(numbers[0])
            return target - 50, target + 50, "specific"
        
        # Goal-based input
        elif any(word in user_input for word in ['low', 'light', 'small']):
            goal = CalorieCalculator.CALORIE_GOALS['low']
            return goal['min'], goal['max'], "goal_low"
        
        elif any(word in user_input for word in ['high', 'large', 'big']):
            goal = CalorieCalculator.CALORIE_GOALS['high']
            return goal['min'], goal['max'], "goal_high"
        
        else:
            # Default to moderate
            goal = CalorieCalculator.CALORIE_GOALS['moderate']
            return goal['min'], goal['max'], "goal_moderate"
    
    @staticmethod
    def calculate_daily_distribution(total_calories: int) -> Dict[str, int]:
        """Calculate calorie distribution for each meal type"""
        distribution = {}
        for meal_type, percentage in CalorieCalculator.DAILY_DISTRIBUTION.items():
            distribution[meal_type] = int(total_calories * percentage)
        return distribution
    
    @staticmethod
    def get_meal_type_range(meal_type: str) -> Tuple[int, int]:
        """Get typical calorie range for a meal type"""
        meal_type_lower = meal_type.lower()
        if meal_type_lower in CalorieCalculator.MEAL_TYPE_RANGES:
            range_data = CalorieCalculator.MEAL_TYPE_RANGES[meal_type_lower]
            return range_data['min'], range_data['max']
        else:
            # Default range for unknown meal types
            return 200, 500
    
    @staticmethod
    def calculate_nutrition_percentages(nutrition: Dict[str, int], calories: int) -> Dict[str, float]:
        """Calculate macro percentages from nutrition data"""
        if not nutrition or calories == 0:
            return {'protein_pct': 0, 'carbs_pct': 0, 'fat_pct': 0}
        
        # Calories per gram: protein=4, carbs=4, fat=9
        protein_calories = nutrition.get('protein', 0) * 4
        carbs_calories = nutrition.get('carbs', 0) * 4
        fat_calories = nutrition.get('fat', 0) * 9
        
        return {
            'protein_pct': round((protein_calories / calories) * 100, 1),
            'carbs_pct': round((carbs_calories / calories) * 100, 1),
            'fat_pct': round((fat_calories / calories) * 100, 1)
        }
    
    @staticmethod
    def generate_nutrition_analysis(meal: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive nutritional analysis for a meal"""
        calories = meal.get('calories', 0)
        nutrition = meal.get('nutrition', {})
        
        # Calculate macro percentages
        percentages = CalorieCalculator.calculate_nutrition_percentages(nutrition, calories)
        
        # Generate insights
        insights = []
        
        # Protein analysis
        protein_pct = percentages['protein_pct']
        if protein_pct >= 25:
            insights.append("High protein content - great for muscle building!")
        elif protein_pct >= 15:
            insights.append("Good protein balance")
        else:
            insights.append("Consider adding protein sources")
        
        # Fiber analysis
        fiber = nutrition.get('fiber', 0)
        if fiber >= 10:
            insights.append("Excellent fiber content for digestive health")
        elif fiber >= 5:
            insights.append("Good fiber content")
        
        # Calorie density
        if calories <= 300:
            insights.append("Light meal - perfect for weight management")
        elif calories >= 500:
            insights.append("Hearty meal - great for active days")
        
        return {
            'calories': calories,
            'nutrition': nutrition,
            'percentages': percentages,
            'insights': insights,
            'macro_balance': CalorieCalculator._evaluate_macro_balance(percentages),
            'health_score': CalorieCalculator._calculate_health_score(nutrition, calories)
        }
    
    @staticmethod
    def _evaluate_macro_balance(percentages: Dict[str, float]) -> str:
        """Evaluate the balance of macronutrients"""
        protein_pct = percentages['protein_pct']
        carbs_pct = percentages['carbs_pct']
        fat_pct = percentages['fat_pct']
        
        # Ideal ranges: Protein 15-25%, Carbs 45-65%, Fat 20-35%
        if (15 <= protein_pct <= 25 and 
            45 <= carbs_pct <= 65 and 
            20 <= fat_pct <= 35):
            return "Excellent macro balance"
        elif (10 <= protein_pct <= 30 and 
              30 <= carbs_pct <= 70 and 
              15 <= fat_pct <= 40):
            return "Good macro balance"
        else:
            return "Could be better balanced"
    
    @staticmethod
    def _calculate_health_score(nutrition: Dict[str, int], calories: int) -> int:
        """Calculate a simple health score (0-100)"""
        score = 50  # Base score
        
        # Bonus for protein
        protein = nutrition.get('protein', 0)
        if protein >= 20:
            score += 15
        elif protein >= 10:
            score += 10
        
        # Bonus for fiber
        fiber = nutrition.get('fiber', 0)
        if fiber >= 8:
            score += 15
        elif fiber >= 5:
            score += 10
        
        # Penalty for very high calories without proportional nutrition
        if calories > 600 and protein < 15:
            score -= 10
        
        # Bonus for balanced calories
        if 200 <= calories <= 500:
            score += 10
        
        return min(100, max(0, score))  # Keep score between 0-100
    
    @staticmethod
    def format_calorie_range(min_cal: int, max_cal: int) -> str:
        """Format calorie range for display"""
        if min_cal == max_cal:
            return f"{min_cal} calories"
        else:
            return f"{min_cal}-{max_cal} calories"
    
    @staticmethod
    def suggest_calorie_alternatives(original_min: int, original_max: int) -> List[Dict[str, Any]]:
        """Suggest alternative calorie ranges when no meals found"""
        alternatives = []
        
        # Expand range by 100 calories
        alternatives.append({
            'type': 'expanded',
            'min': max(0, original_min - 100),
            'max': original_max + 100,
            'description': 'Expand calorie range'
        })
        
        # Suggest meal type categories
        for goal_name, goal_data in CalorieCalculator.CALORIE_GOALS.items():
            if not (goal_data['min'] <= original_min <= goal_data['max']):
                alternatives.append({
                    'type': 'category',
                    'min': goal_data['min'],
                    'max': goal_data['max'],
                    'description': goal_data['description']
                })
        
        return alternatives[:3]  # Return top 3 alternatives