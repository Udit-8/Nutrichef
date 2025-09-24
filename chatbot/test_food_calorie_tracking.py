#!/usr/bin/env python3
"""
Comprehensive Test Script for Food Calorie Tracking Journey
Tests all 10 steps of the food tracking system with multiple scenarios
"""

import sys
import os
import json
from datetime import datetime, date
from typing import Dict, List, Any

# Add the chatbot directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

try:
    from core.session_manager import SessionManager
    from data.data_loader import DataLoader
    from journeys.food_calorie_tracking import FoodCalorieTrackingJourney
    from utils.nutrition_utils import FoodSearchEngine, NutritionCalculator, DiaryManager, ProgressTracker
except ImportError:
    # Handle import issues for relative imports
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from core.session_manager import SessionManager
    from data.data_loader import DataLoader
    # Import classes directly to avoid relative import issues
    exec(open('journeys/food_calorie_tracking.py').read())
    exec(open('utils/nutrition_utils.py').read())

class FoodCalorieTrackingTester:
    """Comprehensive tester for food calorie tracking functionality"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.data_loader = DataLoader()
        self.journey = FoodCalorieTrackingJourney(self.data_loader, self.session_manager)
        self.test_results = []
        
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = {
            'test': test_name,
            'passed': passed,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status}: {test_name}")
        if details and not passed:
            print(f"   Details: {details}")
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🧪 Starting Food Calorie Tracking Journey Test Suite\n")
        print("=" * 60)
        
        # Test 1: Data Loading and Initialization
        self.test_data_loading()
        
        # Test 2: Utility Classes
        self.test_utility_classes()
        
        # Test 3: Journey Initialization
        self.test_journey_initialization()
        
        # Test 4: Step-by-Step Journey Flow
        self.test_journey_flow()
        
        # Test 5: Food Search Functionality
        self.test_food_search()
        
        # Test 6: Nutrition Calculations
        self.test_nutrition_calculations()
        
        # Test 7: Diary Management
        self.test_diary_management()
        
        # Test 8: Progress Tracking
        self.test_progress_tracking()
        
        # Test 9: Error Handling
        self.test_error_handling()
        
        # Test 10: Integration Scenarios
        self.test_integration_scenarios()
        
        # Print final results
        self.print_test_summary()
    
    def test_data_loading(self):
        """Test data loading and access methods"""
        print("\n1️⃣ Testing Data Loading...")
        
        try:
            # Test food nutrition data loading
            foods = self.data_loader.get_foods_nutrition()
            self.log_test("Food nutrition data loaded", len(foods) > 0, f"Loaded {len(foods)} foods")
            
            # Test specific food retrieval
            chicken = self.data_loader.get_food_by_id("food_001")
            self.log_test("Retrieve specific food by ID", 
                         chicken is not None and chicken.get('name') == "Chicken Breast, Grilled")
            
            # Test food search
            search_results = self.data_loader.search_foods_by_name("chicken")
            self.log_test("Food name search", len(search_results) > 0, f"Found {len(search_results)} results")
            
            # Test food categories
            categories = self.data_loader.get_food_categories()
            self.log_test("Food categories", len(categories) > 0, f"Found {len(categories)} categories")
            
        except Exception as e:
            self.log_test("Data loading error handling", False, str(e))
    
    def test_utility_classes(self):
        """Test utility class functionality"""
        print("\n2️⃣ Testing Utility Classes...")
        
        try:
            # Test FoodSearchEngine
            food_search = FoodSearchEngine(self.data_loader)
            search_results = food_search.search_foods("chicken", limit=5)
            self.log_test("FoodSearchEngine basic search", 
                         len(search_results) > 0, f"Found {len(search_results)} results")
            
            # Test NutritionCalculator
            test_food = search_results[0] if search_results else None
            if test_food:
                serving_options = test_food.get('serving_options', [])
                if serving_options:
                    nutrition = NutritionCalculator.calculate_serving_nutrition(
                        test_food, serving_options[0]['id'], 1.0
                    )
                    self.log_test("Nutrition calculation", 
                                 'calories' in nutrition and nutrition['calories'] > 0)
            
            # Test DiaryManager
            diary = DiaryManager(self.session_manager)
            entries = diary.get_today_entries()
            self.log_test("Diary manager initialization", isinstance(entries, list))
            
            # Test ProgressTracker
            progress = ProgressTracker(self.session_manager)
            goals = progress.get_daily_goals()
            self.log_test("Progress tracker initialization", 
                         'calories' in goals and goals['calories'] > 0)
            
        except Exception as e:
            self.log_test("Utility class error handling", False, str(e))
    
    def test_journey_initialization(self):
        """Test journey initialization and state management"""
        print("\n3️⃣ Testing Journey Initialization...")
        
        try:
            # Test journey creation
            self.log_test("Journey creation", self.journey is not None)
            
            # Test initial state
            self.log_test("Initial step is 1", self.journey.current_step == 1 or self.journey.current_step == 0)
            
            # Test journey name
            self.log_test("Journey name set", self.journey.journey_name == "food_calorie_tracking")
            
            # Test step definitions
            self.log_test("Step definitions loaded", len(self.journey.steps) == 10)
            
        except Exception as e:
            self.log_test("Journey initialization error", False, str(e))
    
    def test_journey_flow(self):
        """Test complete journey flow through all steps"""
        print("\n4️⃣ Testing Journey Flow...")
        
        try:
            # Reset journey for clean test
            journey = FoodCalorieTrackingJourney(self.data_loader, SessionManager())
            
            # Step 1: Start journey
            response1 = journey.start_journey("log my food")
            self.log_test("Step 1: Journey start", 
                         "Food Calorie Tracking" in response1 and "tracking" in response1.lower())
            
            # Step 2: Choose entry method (text search)
            response2 = journey.handle_user_input("1")  # Log new food
            self.log_test("Step 2: Entry method selection", 
                         "search" in response2.lower() or "method" in response2.lower())
            
            # Step 3: Search for food
            response3 = journey.handle_user_input("1")  # Text search
            self.log_test("Step 3: Food search initiation", 
                         "search" in response3.lower() or "food" in response3.lower())
            
            # Search for chicken
            response4 = journey.handle_user_input("chicken")
            self.log_test("Step 4: Food search results", 
                         "chicken" in response4.lower() and ("1." in response4 or "option" in response4.lower()))
            
        except Exception as e:
            self.log_test("Journey flow error", False, str(e))
    
    def test_food_search(self):
        """Test food search functionality with various scenarios"""
        print("\n5️⃣ Testing Food Search...")
        
        try:
            food_search = FoodSearchEngine(self.data_loader)
            
            # Test exact match search
            chicken_results = food_search.search_foods("chicken breast")
            self.log_test("Exact match search", len(chicken_results) > 0)
            
            # Test partial match search
            partial_results = food_search.search_foods("salmon")
            self.log_test("Partial match search", len(partial_results) > 0)
            
            # Test case insensitive search
            case_results = food_search.search_foods("YOGURT")
            self.log_test("Case insensitive search", len(case_results) > 0)
            
            # Test empty search
            empty_results = food_search.search_foods("")
            self.log_test("Empty search handling", len(empty_results) == 0)
            
            # Test search with no results
            no_results = food_search.search_foods("nonexistent_food_xyz")
            self.log_test("No results handling", len(no_results) == 0)
            
            # Test food by ID retrieval
            if chicken_results:
                food_id = chicken_results[0]['id']
                retrieved_food = food_search.get_food_by_id(food_id)
                self.log_test("Food by ID retrieval", 
                             retrieved_food is not None and retrieved_food['id'] == food_id)
            
        except Exception as e:
            self.log_test("Food search error", False, str(e))
    
    def test_nutrition_calculations(self):
        """Test nutrition calculations and analysis"""
        print("\n6️⃣ Testing Nutrition Calculations...")
        
        try:
            # Get a test food with serving options
            foods = self.data_loader.get_foods_nutrition()
            test_food = next((f for f in foods if f.get('serving_options')), None)
            
            if test_food:
                serving_options = test_food['serving_options']
                if serving_options:
                    serving = serving_options[0]
                    
                    # Test basic nutrition calculation
                    nutrition = NutritionCalculator.calculate_serving_nutrition(
                        test_food, serving['id'], 1.0
                    )
                    self.log_test("Basic nutrition calculation", 
                                 'calories' in nutrition and nutrition['calories'] > 0)
                    
                    # Test scaled nutrition calculation
                    scaled_nutrition = NutritionCalculator.calculate_serving_nutrition(
                        test_food, serving['id'], 2.0
                    )
                    self.log_test("Scaled nutrition calculation", 
                                 scaled_nutrition['calories'] == nutrition['calories'] * 2)
                    
                    # Test macro percentage calculation
                    percentages = NutritionCalculator.calculate_nutrition_percentages(
                        scaled_nutrition['macros'], scaled_nutrition['calories']
                    )
                    self.log_test("Macro percentage calculation", 
                                 'protein_pct' in percentages and 
                                 'carbs_pct' in percentages and 
                                 'fat_pct' in percentages)
            
            # Test daily totals calculation (empty list)
            empty_totals = NutritionCalculator.calculate_daily_totals([])
            self.log_test("Empty daily totals", 
                         empty_totals['calories'] == 0 and 
                         empty_totals['macros']['protein'] == 0)
            
        except Exception as e:
            self.log_test("Nutrition calculations error", False, str(e))
    
    def test_diary_management(self):
        """Test diary management functionality"""
        print("\n7️⃣ Testing Diary Management...")
        
        try:
            diary = DiaryManager(SessionManager())
            
            # Test getting today's entries (should be empty initially)
            today_entries = diary.get_today_entries()
            self.log_test("Get today's entries", isinstance(today_entries, list))
            
            # Test daily summary with no entries
            summary = diary.get_daily_summary()
            self.log_test("Daily summary structure", 
                         'total_entries' in summary and 
                         'nutrition_totals' in summary and
                         'date' in summary)
            
            # Test empty summary values
            self.log_test("Empty summary values", 
                         summary['total_entries'] == 0 and
                         summary['nutrition_totals']['calories'] == 0)
            
        except Exception as e:
            self.log_test("Diary management error", False, str(e))
    
    def test_progress_tracking(self):
        """Test progress tracking and goal monitoring"""
        print("\n8️⃣ Testing Progress Tracking...")
        
        try:
            progress_tracker = ProgressTracker(SessionManager())
            
            # Test default goals
            goals = progress_tracker.get_daily_goals()
            self.log_test("Default goals loaded", 
                         goals['calories'] > 0 and 
                         goals['protein'] > 0 and
                         goals['carbs'] > 0 and
                         goals['fat'] > 0)
            
            # Test setting custom goals
            progress_tracker.set_daily_goals(1800, 90, 225, 60)
            custom_goals = progress_tracker.get_daily_goals()
            self.log_test("Custom goals setting", 
                         custom_goals['calories'] == 1800 and
                         custom_goals['protein'] == 90)
            
            # Test progress calculation with zero totals
            zero_totals = {
                'calories': 0,
                'macros': {'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0}
            }
            progress = progress_tracker.calculate_progress(zero_totals)
            self.log_test("Zero progress calculation", 
                         progress['overall']['percentage'] == 0)
            
            # Test progress calculation with some values
            partial_totals = {
                'calories': 900,  # 50% of 1800
                'macros': {'protein': 45, 'carbs': 112, 'fat': 30, 'fiber': 10}  # 50% of goals
            }
            partial_progress = progress_tracker.calculate_progress(partial_totals)
            self.log_test("Partial progress calculation", 
                         40 <= partial_progress['overall']['percentage'] <= 60)
            
            # Test goal recommendations
            recommendations = progress_tracker.get_goal_recommendations(partial_progress)
            self.log_test("Goal recommendations", 
                         isinstance(recommendations, list) and len(recommendations) > 0)
            
        except Exception as e:
            self.log_test("Progress tracking error", False, str(e))
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        print("\n9️⃣ Testing Error Handling...")
        
        try:
            journey = FoodCalorieTrackingJourney(self.data_loader, SessionManager())
            
            # Test invalid user input handling
            response = journey.handle_user_input("")
            self.log_test("Empty input handling", len(response) > 0)
            
            # Test invalid step navigation
            journey.current_step = 999  # Invalid step
            response = journey.handle_user_input("test")
            self.log_test("Invalid step handling", "wrong" in response.lower() or "restart" in response.lower())
            
            # Test food search with invalid ID
            invalid_food = self.data_loader.get_food_by_id("invalid_id")
            self.log_test("Invalid food ID handling", invalid_food is None)
            
            # Test nutrition calculation with invalid serving
            foods = self.data_loader.get_foods_nutrition()
            if foods:
                test_food = foods[0]
                invalid_nutrition = NutritionCalculator.calculate_serving_nutrition(
                    test_food, "invalid_serving_id", 1.0
                )
                self.log_test("Invalid serving ID handling", 
                             'error' in invalid_nutrition or invalid_nutrition.get('calories', 0) == 0)
            
        except Exception as e:
            self.log_test("Error handling test failed", False, str(e))
    
    def test_integration_scenarios(self):
        """Test realistic integration scenarios"""
        print("\n🔟 Testing Integration Scenarios...")
        
        try:
            # Scenario 1: Complete food logging workflow
            self._test_complete_logging_workflow()
            
            # Scenario 2: View diary workflow
            self._test_diary_viewing_workflow()
            
            # Scenario 3: Manual food entry workflow
            self._test_manual_entry_workflow()
            
        except Exception as e:
            self.log_test("Integration scenarios error", False, str(e))
    
    def _test_complete_logging_workflow(self):
        """Test complete food logging from start to finish"""
        journey = FoodCalorieTrackingJourney(self.data_loader, SessionManager())
        
        try:
            # Start journey
            response1 = journey.start_journey("log my breakfast")
            
            # Should detect log food intent and proceed to step 2
            if journey.current_step >= 2:
                # Choose text search method
                response2 = journey.handle_user_input("1")
                
                # Search for a food
                response3 = journey.handle_user_input("chicken")
                
                self.log_test("Complete logging workflow - search", 
                             "chicken" in response3.lower() and "1." in response3)
            else:
                self.log_test("Complete logging workflow - search", False, 
                             "Journey did not progress properly")
        
        except Exception as e:
            self.log_test("Complete logging workflow", False, str(e))
    
    def _test_diary_viewing_workflow(self):
        """Test diary viewing workflow"""
        journey = FoodCalorieTrackingJourney(self.data_loader, SessionManager())
        
        try:
            # Start with diary view intent
            response = journey.start_journey("show my food diary")
            
            self.log_test("Diary viewing workflow", 
                         "diary" in response.lower() or "entries" in response.lower())
        
        except Exception as e:
            self.log_test("Diary viewing workflow", False, str(e))
    
    def _test_manual_entry_workflow(self):
        """Test manual food entry workflow"""
        journey = FoodCalorieTrackingJourney(self.data_loader, SessionManager())
        
        try:
            # Start journey and choose manual entry
            journey.start_journey("log food")
            if journey.current_step >= 2:
                # Choose manual entry
                response = journey.handle_user_input("2")
                
                self.log_test("Manual entry workflow initiation", 
                             "manual" in response.lower() or "format" in response.lower())
        
        except Exception as e:
            self.log_test("Manual entry workflow", False, str(e))
    
    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print("🎯 TEST SUMMARY")
        print("=" * 60)
        
        passed_tests = sum(1 for test in self.test_results if test['passed'])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ Tests Passed: {passed_tests}/{total_tests}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        print(f"⏰ Test Duration: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Show failed tests
        failed_tests = [test for test in self.test_results if not test['passed']]
        if failed_tests:
            print(f"\n❌ Failed Tests ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  • {test['test']}")
                if test['details']:
                    print(f"    Details: {test['details']}")
        
        # Performance assessment
        print(f"\n📈 Assessment:")
        if success_rate >= 90:
            print("🟢 EXCELLENT - Food calorie tracking system is working perfectly!")
        elif success_rate >= 80:
            print("🟡 GOOD - System is working well with minor issues")
        elif success_rate >= 70:
            print("🟠 FAIR - System needs some improvements")
        else:
            print("🔴 POOR - System requires significant fixes")
        
        # Save detailed results
        self._save_test_results()
        print(f"\n💾 Detailed results saved to: test_results_food_tracking.json")
    
    def _save_test_results(self):
        """Save detailed test results to file"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': len(self.test_results),
                'passed_tests': sum(1 for test in self.test_results if test['passed']),
                'success_rate': (sum(1 for test in self.test_results if test['passed']) / len(self.test_results) * 100) if self.test_results else 0
            },
            'test_details': self.test_results
        }
        
        with open('test_results_food_tracking.json', 'w') as f:
            json.dump(results, f, indent=2)

def main():
    """Main test execution function"""
    print("🚀 Food Calorie Tracking Journey - Comprehensive Test Suite")
    print("Testing all components and workflows...")
    
    tester = FoodCalorieTrackingTester()
    tester.run_all_tests()
    
    print("\n🎉 Testing complete! Check the results above.")

if __name__ == "__main__":
    main()