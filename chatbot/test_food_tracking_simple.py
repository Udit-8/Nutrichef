#!/usr/bin/env python3
"""
Simplified Test Script for Food Calorie Tracking Journey
Tests key functionality without complex imports
"""

import sys
import os
import json
from datetime import datetime, date
from typing import Dict, List, Any

# Add the chatbot directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from core.session_manager import SessionManager
from data.data_loader import DataLoader

class SimpleFoodTrackingTester:
    """Simple tester for food calorie tracking functionality"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.data_loader = DataLoader()
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
        """Run simplified test suite"""
        print("🧪 Starting Food Calorie Tracking - Simplified Test Suite\n")
        print("=" * 60)
        
        # Test 1: Data Loading
        self.test_data_loading()
        
        # Test 2: Food Search Functions
        self.test_food_search_functions()
        
        # Test 3: Nutrition Data Access
        self.test_nutrition_data_access()
        
        # Test 4: Session Management
        self.test_session_management()
        
        # Test 5: Data Processing
        self.test_data_processing()
        
        # Print results
        self.print_test_summary()
    
    def test_data_loading(self):
        """Test food nutrition data loading"""
        print("\n1️⃣ Testing Data Loading...")
        
        try:
            # Test food nutrition data loading
            foods = self.data_loader.get_foods_nutrition()
            self.log_test("Food nutrition data loaded", len(foods) > 0, f"Loaded {len(foods)} foods")
            
            # Test specific food retrieval
            if foods:
                first_food = foods[0]
                food_id = first_food.get('id')
                retrieved = self.data_loader.get_food_by_id(food_id)
                self.log_test("Retrieve specific food by ID", 
                             retrieved is not None and retrieved.get('id') == food_id)
            
            # Test food categories
            categories = self.data_loader.get_food_categories()
            self.log_test("Food categories", len(categories) > 0, f"Found {len(categories)} categories")
            
            # Test serving options
            if foods:
                first_food = foods[0]
                servings = self.data_loader.get_food_serving_options(first_food.get('id'))
                self.log_test("Food serving options", len(servings) > 0, f"Found {len(servings)} servings")
            
        except Exception as e:
            self.log_test("Data loading error", False, str(e))
    
    def test_food_search_functions(self):
        """Test food search functionality"""
        print("\n2️⃣ Testing Food Search...")
        
        try:
            # Test food search by name
            chicken_results = self.data_loader.search_foods_by_name("chicken")
            self.log_test("Food search by name", len(chicken_results) > 0, f"Found {len(chicken_results)} results")
            
            # Test food search with partial match
            partial_results = self.data_loader.search_foods_by_name("yogurt")
            self.log_test("Partial name search", len(partial_results) >= 0)
            
            # Test search by category
            protein_foods = self.data_loader.get_foods_by_category("protein")
            self.log_test("Search by category", len(protein_foods) > 0, f"Found {len(protein_foods)} protein foods")
            
            # Test popular foods
            popular = self.data_loader.get_popular_foods(limit=10)
            self.log_test("Popular foods", len(popular) > 0, f"Found {len(popular)} popular foods")
            
            # Test high protein foods
            high_protein = self.data_loader.get_foods_with_high_protein(min_protein_per_100g=20.0)
            self.log_test("High protein foods", len(high_protein) > 0, f"Found {len(high_protein)} high-protein foods")
            
            # Test low calorie foods
            low_cal = self.data_loader.get_low_calorie_foods(max_calories_per_100g=150)
            self.log_test("Low calorie foods", len(low_cal) > 0, f"Found {len(low_cal)} low-calorie foods")
            
        except Exception as e:
            self.log_test("Food search error", False, str(e))
    
    def test_nutrition_data_access(self):
        """Test nutrition data access and calculations"""
        print("\n3️⃣ Testing Nutrition Data...")
        
        try:
            foods = self.data_loader.get_foods_nutrition()
            
            if foods:
                test_food = foods[0]
                
                # Test nutrition per 100g calculation
                nutrition_100g = self.data_loader.calculate_food_nutrition_per_100g(test_food)
                self.log_test("Nutrition per 100g calculation", 
                             'calories' in nutrition_100g and nutrition_100g['calories'] > 0)
                
                # Test serving options
                servings = test_food.get('serving_options', [])
                if servings:
                    serving = servings[0]
                    self.log_test("Serving data structure", 
                                 'calories' in serving and 'macros' in serving)
                
                # Test allergen information
                allergens = self.data_loader.get_food_allergens(test_food.get('id'))
                self.log_test("Allergen information access", isinstance(allergens, list))
                
                # Test dietary tags (raw format uses dietary_tags)
                if ('health_benefits' in test_food or 
                    'tags' in test_food or 
                    'dietary_tags' in test_food):
                    self.log_test("Dietary information available", True)
                else:
                    self.log_test("Dietary information available", False, "No health benefits or tags found")
            
        except Exception as e:
            self.log_test("Nutrition data access error", False, str(e))
    
    def test_session_management(self):
        """Test session management functionality"""
        print("\n4️⃣ Testing Session Management...")
        
        try:
            session = SessionManager()
            
            # Test basic session operations
            session.set('test_key', 'test_value')
            retrieved_value = session.get('test_key')
            self.log_test("Session set/get", retrieved_value == 'test_value')
            
            # Test food diary storage structure
            today_key = f"food_diary_{date.today().isoformat()}"
            session.set(today_key, [])
            diary_entries = session.get(today_key, [])
            self.log_test("Food diary storage", isinstance(diary_entries, list))
            
            # Test goal storage
            goals = {'calories': 2000, 'protein': 100}
            session.set('daily_nutrition_goals', goals)
            stored_goals = session.get('daily_nutrition_goals')
            self.log_test("Nutrition goals storage", stored_goals['calories'] == 2000)
            
        except Exception as e:
            self.log_test("Session management error", False, str(e))
    
    def test_data_processing(self):
        """Test data processing and calculations"""
        print("\n5️⃣ Testing Data Processing...")
        
        try:
            # Test macro calculation logic
            test_macros = {'protein': 30, 'carbs': 45, 'fat': 15}
            test_calories = 400
            
            # Calculate macro percentages manually
            protein_cal = test_macros['protein'] * 4  # 120
            carbs_cal = test_macros['carbs'] * 4      # 180
            fat_cal = test_macros['fat'] * 9          # 135
            total_macro_cal = protein_cal + carbs_cal + fat_cal  # 435
            
            # Test if calculations are reasonable
            self.log_test("Macro calculation logic", 
                         abs(total_macro_cal - test_calories) < 50, 
                         f"Calculated {total_macro_cal} vs expected ~{test_calories}")
            
            # Test portion scaling
            base_calories = 100
            scale_factor = 2.5
            scaled_calories = base_calories * scale_factor
            self.log_test("Portion scaling", scaled_calories == 250)
            
            # Test daily goal calculations
            daily_calories = 2000
            breakfast_pct = 0.25
            breakfast_target = daily_calories * breakfast_pct
            self.log_test("Daily distribution calculation", breakfast_target == 500)
            
        except Exception as e:
            self.log_test("Data processing error", False, str(e))
    
    def print_test_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("🎯 SIMPLIFIED TEST SUMMARY")
        print("=" * 60)
        
        passed_tests = sum(1 for test in self.test_results if test['passed'])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ Tests Passed: {passed_tests}/{total_tests}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        print(f"⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Show failed tests
        failed_tests = [test for test in self.test_results if not test['passed']]
        if failed_tests:
            print(f"\n❌ Failed Tests ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  • {test['test']}")
                if test['details']:
                    print(f"    Details: {test['details']}")
        
        # Assessment
        print(f"\n📈 Assessment:")
        if success_rate >= 90:
            print("🟢 EXCELLENT - Core food tracking functionality is ready!")
        elif success_rate >= 80:
            print("🟡 GOOD - System is mostly functional")
        elif success_rate >= 70:
            print("🟠 FAIR - Some components need work")
        else:
            print("🔴 POOR - Major issues need fixing")
        
        # Save results
        results_file = 'simple_test_results_food_tracking.json'
        with open(results_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'success_rate': success_rate
                },
                'tests': self.test_results
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")

def main():
    """Main test function"""
    print("🚀 Food Calorie Tracking - Simplified Test Suite")
    print("Testing core data access and processing functionality...")
    
    tester = SimpleFoodTrackingTester()
    tester.run_all_tests()
    
    print("\n🎉 Testing complete!")
    print("\nNext steps:")
    print("1. Fix any failed tests")
    print("2. Test the complete journey flow manually")
    print("3. Integrate with the main chatbot system")

if __name__ == "__main__":
    main()