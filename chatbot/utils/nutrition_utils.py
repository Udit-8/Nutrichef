"""
Nutrition Tracking Utility Classes
For Food Calorie Tracking Journey
"""

import json
import re
from datetime import datetime, date
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

@dataclass
class FoodEntry:
    """Represents a single food entry in the diary"""
    food_id: str
    food_name: str
    serving_id: str
    serving_description: str
    quantity: float
    calories: int
    macros: Dict[str, float]
    meal_type: str
    timestamp: datetime
    notes: Optional[str] = None

class FoodSearchEngine:
    """Advanced food search functionality"""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
        
    def search_foods(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search foods by name with smart matching"""
        if not query or not query.strip():
            return []
            
        query_lower = query.lower().strip()
        foods = self.data_loader.get_foods_nutrition()
        results = []
        
        # Direct name matches (highest priority)
        for food in foods:
            food_name = food.get('name', '').lower()
            if query_lower in food_name:
                score = self._calculate_match_score(query_lower, food_name, food)
                results.append((food, score))
        
        # Common names matches
        for food in foods:
            common_names = food.get('common_names', [])
            for common_name in common_names:
                if query_lower in common_name.lower():
                    score = self._calculate_match_score(query_lower, common_name.lower(), food)
                    results.append((food, score))
        
        # Category matches (lower priority)
        for food in foods:
            category = food.get('category', '').lower()
            subcategory = food.get('subcategory', '').lower()
            if query_lower in category or query_lower in subcategory:
                score = self._calculate_match_score(query_lower, category, food) * 0.5
                results.append((food, score))
        
        # Remove duplicates and sort by score
        seen_ids = set()
        unique_results = []
        for food, score in results:
            food_id = food.get('id')
            if food_id not in seen_ids:
                seen_ids.add(food_id)
                unique_results.append((food, score))
        
        # Sort by score descending and limit results
        unique_results.sort(key=lambda x: x[1], reverse=True)
        return [food for food, score in unique_results[:limit]]
    
    def _calculate_match_score(self, query: str, match_text: str, food: Dict[str, Any]) -> float:
        """Calculate relevance score for search matches"""
        score = 0.0
        
        # Exact match bonus
        if query == match_text:
            score += 10.0
        
        # Start of word bonus
        if match_text.startswith(query):
            score += 5.0
        
        # Word boundary bonus
        words = match_text.split()
        for word in words:
            if word.startswith(query):
                score += 3.0
        
        # Popularity bonus (foods with more serving options are likely more common)
        serving_options = food.get('serving_options', [])
        score += len(serving_options) * 0.5
        
        # Category bonus (protein foods get slight boost)
        category = food.get('category', '').lower()
        if category in ['protein', 'dairy']:
            score += 1.0
        
        return score
    
    def get_food_by_id(self, food_id: str) -> Optional[Dict[str, Any]]:
        """Get specific food by ID"""
        foods = self.data_loader.get_foods_nutrition()
        for food in foods:
            if food.get('id') == food_id:
                return food
        return None
    
    def get_recent_foods(self, diary_manager, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recently logged foods for quick re-entry"""
        recent_entries = diary_manager.get_recent_entries(limit * 2)  # Get more to filter duplicates
        
        # Extract unique foods from recent entries
        seen_food_ids = set()
        recent_foods = []
        
        for entry in recent_entries:
            food_id = entry.food_id
            if food_id not in seen_food_ids:
                food = self.get_food_by_id(food_id)
                if food:
                    # Add frequency and last used info
                    food['last_used'] = entry.timestamp
                    food['most_common_serving'] = entry.serving_description
                    recent_foods.append(food)
                    seen_food_ids.add(food_id)
                
                if len(recent_foods) >= limit:
                    break
        
        return recent_foods

class NutritionCalculator:
    """Nutrition calculations and analysis"""
    
    @staticmethod
    def calculate_serving_nutrition(food: Dict[str, Any], serving_id: str, quantity: float = 1.0) -> Dict[str, Any]:
        """Calculate nutrition for a specific serving and quantity"""
        serving_options = food.get('serving_options', [])
        
        # Find the specified serving
        selected_serving = None
        for serving in serving_options:
            if serving.get('id') == serving_id:
                selected_serving = serving
                break
        
        if not selected_serving:
            return {'error': 'Serving not found'}
        
        # Calculate scaled nutrition
        base_calories = selected_serving.get('calories', 0)
        base_macros = selected_serving.get('macros', {})
        
        scaled_nutrition = {
            'calories': int(base_calories * quantity),
            'macros': {}
        }
        
        for macro, value in base_macros.items():
            scaled_nutrition['macros'][macro] = round(value * quantity, 1)
        
        # Add serving info
        scaled_nutrition['serving_info'] = {
            'serving_id': serving_id,
            'description': selected_serving.get('description', ''),
            'quantity': quantity,
            'total_weight_g': selected_serving.get('weight_g', 0) * quantity
        }
        
        return scaled_nutrition
    
    @staticmethod
    def calculate_daily_totals(entries: List[FoodEntry]) -> Dict[str, Any]:
        """Calculate daily nutrition totals from food entries"""
        totals = {
            'calories': 0,
            'macros': {
                'protein': 0.0,
                'carbs': 0.0,
                'fat': 0.0,
                'fiber': 0.0,
                'sugar': 0.0
            },
            'meal_breakdown': {
                'breakfast': {'calories': 0, 'count': 0},
                'lunch': {'calories': 0, 'count': 0},
                'dinner': {'calories': 0, 'count': 0},
                'snack': {'calories': 0, 'count': 0}
            }
        }
        
        for entry in entries:
            # Add to totals
            totals['calories'] += entry.calories
            
            for macro, value in entry.macros.items():
                if macro in totals['macros']:
                    totals['macros'][macro] += value
            
            # Add to meal breakdown
            meal_type = entry.meal_type.lower()
            if meal_type in totals['meal_breakdown']:
                totals['meal_breakdown'][meal_type]['calories'] += entry.calories
                totals['meal_breakdown'][meal_type]['count'] += 1
        
        # Round macro values
        for macro in totals['macros']:
            totals['macros'][macro] = round(totals['macros'][macro], 1)
        
        return totals
    
    @staticmethod
    def analyze_nutrition_balance(totals: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze nutritional balance and provide insights"""
        calories = totals.get('calories', 0)
        macros = totals.get('macros', {})
        
        if calories == 0:
            return {
                'macro_percentages': {'protein': 0, 'carbs': 0, 'fat': 0},
                'balance_score': 0,
                'insights': ['No food entries logged yet today'],
                'recommendations': ['Start logging your meals to get nutritional insights']
            }
        
        # Calculate macro percentages
        protein_cal = macros.get('protein', 0) * 4
        carbs_cal = macros.get('carbs', 0) * 4
        fat_cal = macros.get('fat', 0) * 9
        
        macro_percentages = {
            'protein': round((protein_cal / calories) * 100, 1),
            'carbs': round((carbs_cal / calories) * 100, 1),
            'fat': round((fat_cal / calories) * 100, 1)
        }
        
        # Calculate balance score (0-100)
        balance_score = NutritionCalculator._calculate_balance_score(macro_percentages, macros, calories)
        
        # Generate insights
        insights = NutritionCalculator._generate_insights(macro_percentages, macros, calories)
        
        # Generate recommendations
        recommendations = NutritionCalculator._generate_recommendations(macro_percentages, macros, calories)
        
        return {
            'macro_percentages': macro_percentages,
            'balance_score': balance_score,
            'insights': insights,
            'recommendations': recommendations
        }
    
    @staticmethod
    def _calculate_balance_score(percentages: Dict[str, float], macros: Dict[str, float], calories: int) -> int:
        """Calculate nutrition balance score (0-100)"""
        score = 50  # Base score
        
        # Ideal ranges: Protein 15-25%, Carbs 45-65%, Fat 20-35%
        protein_pct = percentages['protein']
        carbs_pct = percentages['carbs']
        fat_pct = percentages['fat']
        
        # Protein scoring
        if 15 <= protein_pct <= 25:
            score += 15
        elif 10 <= protein_pct <= 30:
            score += 10
        else:
            score -= 5
        
        # Carbs scoring
        if 45 <= carbs_pct <= 65:
            score += 15
        elif 30 <= carbs_pct <= 75:
            score += 10
        else:
            score -= 5
        
        # Fat scoring
        if 20 <= fat_pct <= 35:
            score += 15
        elif 15 <= fat_pct <= 40:
            score += 10
        else:
            score -= 5
        
        # Fiber bonus
        fiber = macros.get('fiber', 0)
        if fiber >= 25:
            score += 10
        elif fiber >= 15:
            score += 5
        
        return min(100, max(0, score))
    
    @staticmethod
    def _generate_insights(percentages: Dict[str, float], macros: Dict[str, float], calories: int) -> List[str]:
        """Generate nutritional insights"""
        insights = []
        
        protein_pct = percentages['protein']
        carbs_pct = percentages['carbs']
        fat_pct = percentages['fat']
        fiber = macros.get('fiber', 0)
        
        # Protein insights
        if protein_pct >= 25:
            insights.append("🏋️ Excellent protein intake - great for muscle maintenance!")
        elif protein_pct < 15:
            insights.append("💪 Consider adding more protein sources to your meals")
        
        # Fiber insights
        if fiber >= 25:
            insights.append("🌾 Outstanding fiber intake - excellent for digestive health!")
        elif fiber < 15:
            insights.append("🥬 Try adding more vegetables, fruits, or whole grains for fiber")
        
        # Calorie insights
        if calories < 1200:
            insights.append("⚠️ Daily calories seem quite low - ensure you're meeting energy needs")
        elif calories > 2500:
            insights.append("🔥 High calorie day - great for active or high-energy days")
        
        # Balance insights
        if abs(carbs_pct - 55) <= 10 and abs(fat_pct - 30) <= 10:
            insights.append("⚖️ Well-balanced macronutrient distribution!")
        
        return insights[:4]  # Limit to top 4 insights
    
    @staticmethod
    def _generate_recommendations(percentages: Dict[str, float], macros: Dict[str, float], calories: int) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        protein_pct = percentages['protein']
        carbs_pct = percentages['carbs']
        fat_pct = percentages['fat']
        
        # Protein recommendations
        if protein_pct < 15:
            recommendations.append("Add lean protein: chicken breast, fish, Greek yogurt, or tofu")
        
        # Carb recommendations
        if carbs_pct < 45:
            recommendations.append("Include healthy carbs: quinoa, sweet potatoes, or whole grain bread")
        elif carbs_pct > 65:
            recommendations.append("Balance with more protein and healthy fats")
        
        # Fat recommendations
        if fat_pct < 20:
            recommendations.append("Add healthy fats: avocado, nuts, olive oil, or salmon")
        elif fat_pct > 35:
            recommendations.append("Reduce high-fat foods and focus on lean proteins")
        
        # Fiber recommendations
        fiber = macros.get('fiber', 0)
        if fiber < 15:
            recommendations.append("Boost fiber: add berries, broccoli, beans, or oatmeal")
        
        return recommendations[:3]  # Limit to top 3 recommendations

class DiaryManager:
    """Manages food diary entries and persistence"""
    
    def __init__(self, session_manager):
        self.session_manager = session_manager
        
    def add_entry(self, food_entry: FoodEntry) -> bool:
        """Add a food entry to the diary"""
        try:
            # Get today's entries
            today_key = f"food_diary_{date.today().isoformat()}"
            today_entries = self.session_manager.get(today_key, [])
            
            # Convert entry to dict for storage
            entry_dict = {
                'food_id': food_entry.food_id,
                'food_name': food_entry.food_name,
                'serving_id': food_entry.serving_id,
                'serving_description': food_entry.serving_description,
                'quantity': food_entry.quantity,
                'calories': food_entry.calories,
                'macros': food_entry.macros,
                'meal_type': food_entry.meal_type,
                'timestamp': food_entry.timestamp.isoformat(),
                'notes': food_entry.notes
            }
            
            today_entries.append(entry_dict)
            self.session_manager.set(today_key, today_entries)
            return True
            
        except Exception as e:
            print(f"Error adding diary entry: {e}")
            return False
    
    def get_today_entries(self) -> List[FoodEntry]:
        """Get all food entries for today"""
        today_key = f"food_diary_{date.today().isoformat()}"
        entries_data = self.session_manager.get(today_key, [])
        
        entries = []
        for entry_dict in entries_data:
            try:
                entry = FoodEntry(
                    food_id=entry_dict['food_id'],
                    food_name=entry_dict['food_name'],
                    serving_id=entry_dict['serving_id'],
                    serving_description=entry_dict['serving_description'],
                    quantity=entry_dict['quantity'],
                    calories=entry_dict['calories'],
                    macros=entry_dict['macros'],
                    meal_type=entry_dict['meal_type'],
                    timestamp=datetime.fromisoformat(entry_dict['timestamp']),
                    notes=entry_dict.get('notes')
                )
                entries.append(entry)
            except Exception as e:
                print(f"Error parsing diary entry: {e}")
                continue
        
        return entries
    
    def get_recent_entries(self, limit: int = 50) -> List[FoodEntry]:
        """Get recent entries across multiple days"""
        all_entries = []
        
        # Check last 30 days
        from datetime import timedelta
        today = date.today()
        
        for i in range(30):
            check_date = today - timedelta(days=i)
            date_key = f"food_diary_{check_date.isoformat()}"
            entries_data = self.session_manager.get(date_key, [])
            
            for entry_dict in entries_data:
                try:
                    entry = FoodEntry(
                        food_id=entry_dict['food_id'],
                        food_name=entry_dict['food_name'],
                        serving_id=entry_dict['serving_id'],
                        serving_description=entry_dict['serving_description'],
                        quantity=entry_dict['quantity'],
                        calories=entry_dict['calories'],
                        macros=entry_dict['macros'],
                        meal_type=entry_dict['meal_type'],
                        timestamp=datetime.fromisoformat(entry_dict['timestamp']),
                        notes=entry_dict.get('notes')
                    )
                    all_entries.append(entry)
                except Exception:
                    continue
        
        # Sort by timestamp descending and limit
        all_entries.sort(key=lambda x: x.timestamp, reverse=True)
        return all_entries[:limit]
    
    def delete_entry(self, timestamp: str) -> bool:
        """Delete a specific entry by timestamp"""
        try:
            today_key = f"food_diary_{date.today().isoformat()}"
            today_entries = self.session_manager.get(today_key, [])
            
            # Filter out the entry with matching timestamp
            updated_entries = [
                entry for entry in today_entries 
                if entry.get('timestamp') != timestamp
            ]
            
            if len(updated_entries) != len(today_entries):
                self.session_manager.set(today_key, updated_entries)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error deleting diary entry: {e}")
            return False
    
    def get_daily_summary(self) -> Dict[str, Any]:
        """Get summary of today's food intake"""
        entries = self.get_today_entries()
        totals = NutritionCalculator.calculate_daily_totals(entries)
        analysis = NutritionCalculator.analyze_nutrition_balance(totals)
        
        return {
            'date': date.today().isoformat(),
            'total_entries': len(entries),
            'nutrition_totals': totals,
            'nutrition_analysis': analysis,
            'entries': [
                {
                    'food_name': entry.food_name,
                    'serving': entry.serving_description,
                    'quantity': entry.quantity,
                    'calories': entry.calories,
                    'meal_type': entry.meal_type,
                    'time': entry.timestamp.strftime("%H:%M")
                }
                for entry in entries
            ]
        }

class ProgressTracker:
    """Tracks progress towards nutrition goals"""
    
    def __init__(self, session_manager):
        self.session_manager = session_manager
    
    def set_daily_goals(self, calorie_goal: int, protein_goal: float = None, 
                       carb_goal: float = None, fat_goal: float = None) -> None:
        """Set daily nutrition goals"""
        goals = {
            'calories': calorie_goal,
            'protein': protein_goal or calorie_goal * 0.15 / 4,  # 15% of calories as protein
            'carbs': carb_goal or calorie_goal * 0.55 / 4,      # 55% of calories as carbs
            'fat': fat_goal or calorie_goal * 0.30 / 9          # 30% of calories as fat
        }
        
        self.session_manager.set('daily_nutrition_goals', goals)
    
    def get_daily_goals(self) -> Dict[str, float]:
        """Get current daily nutrition goals"""
        return self.session_manager.get('daily_nutrition_goals', {
            'calories': 2000,
            'protein': 75.0,
            'carbs': 275.0,
            'fat': 67.0
        })
    
    def calculate_progress(self, current_totals: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate progress towards daily goals"""
        goals = self.get_daily_goals()
        current_calories = current_totals.get('calories', 0)
        current_macros = current_totals.get('macros', {})
        
        progress = {}
        
        # Calculate percentage progress for each goal
        progress['calories'] = {
            'current': current_calories,
            'goal': goals['calories'],
            'percentage': min(100, (current_calories / goals['calories']) * 100) if goals['calories'] > 0 else 0,
            'remaining': max(0, goals['calories'] - current_calories)
        }
        
        for macro in ['protein', 'carbs', 'fat']:
            current_value = current_macros.get(macro, 0)
            goal_value = goals.get(macro, 0)
            
            progress[macro] = {
                'current': current_value,
                'goal': goal_value,
                'percentage': min(100, (current_value / goal_value) * 100) if goal_value > 0 else 0,
                'remaining': max(0, goal_value - current_value)
            }
        
        # Calculate overall progress score
        avg_percentage = sum(progress[key]['percentage'] for key in progress) / len(progress)
        progress['overall'] = {
            'percentage': round(avg_percentage, 1),
            'status': self._get_progress_status(avg_percentage)
        }
        
        return progress
    
    def _get_progress_status(self, percentage: float) -> str:
        """Get status message based on progress percentage"""
        if percentage >= 90:
            return "🎯 Excellent progress - almost there!"
        elif percentage >= 70:
            return "👍 Good progress - keep it up!"
        elif percentage >= 50:
            return "📈 Making progress - you're halfway there!"
        elif percentage >= 25:
            return "🚀 Getting started - stay consistent!"
        else:
            return "💪 Just beginning - every meal counts!"
    
    def get_goal_recommendations(self, progress: Dict[str, Any]) -> List[str]:
        """Get recommendations based on current progress"""
        recommendations = []
        
        calories_pct = progress['calories']['percentage']
        protein_pct = progress['protein']['percentage']
        
        if calories_pct < 50:
            recommendations.append("You're under halfway to your calorie goal - consider adding a nutritious snack")
        elif calories_pct > 100:
            recommendations.append("You've exceeded your calorie goal - that's okay for active days!")
        
        if protein_pct < 70:
            protein_remaining = progress['protein']['remaining']
            recommendations.append(f"Add {protein_remaining:.0f}g more protein - try Greek yogurt or lean meat")
        
        if len(recommendations) == 0:
            recommendations.append("Great balance! You're on track with your nutrition goals")
        
        return recommendations[:2]