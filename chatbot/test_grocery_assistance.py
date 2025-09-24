#!/usr/bin/env python3
"""
Comprehensive Test Script for Grocery Assistance Journey
Tests all functionalities including ingredient extraction, consolidation, store organization, and more.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from data.data_loader import DataLoader
from core.session_manager import SessionManager
from core.intent_classifier import IntentClassifier
from core.chatbot_manager import ChatbotManager
from journeys.grocery_assistance import GroceryAssistanceJourney
from utils.grocery_utils import IngredientExtractor, ListConsolidator, StoreOrganizer, SubstitutionManager

class GroceryAssistanceTest:
    """Comprehensive test class for grocery assistance functionality"""
    
    def __init__(self):
        # Initialize core components
        self.data_loader = DataLoader()
        self.session_manager = SessionManager()
        self.intent_classifier = IntentClassifier()
        self.chatbot_manager = ChatbotManager(self.session_manager, self.intent_classifier, self.data_loader)
        
        # Initialize grocery assistance journey
        self.grocery_journey = GroceryAssistanceJourney(self.data_loader, self.session_manager)
        
        # Initialize utility classes for direct testing
        self.ingredient_extractor = IngredientExtractor(self.data_loader)
        self.list_consolidator = ListConsolidator(self.data_loader)
        self.store_organizer = StoreOrganizer(self.data_loader)
        self.substitution_manager = SubstitutionManager(self.data_loader)
        
        self.test_results = []
        
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🧪 STARTING COMPREHENSIVE GROCERY ASSISTANCE TESTS")
        print("=" * 60)
        
        # Test 1: Intent Classification
        self.test_intent_classification()
        
        # Test 2: Data Loading
        self.test_data_loading()
        
        # Test 3: Ingredient Extraction
        self.test_ingredient_extraction()
        
        # Test 4: List Consolidation
        self.test_list_consolidation()
        
        # Test 5: Store Organization
        self.test_store_organization()
        
        # Test 6: Substitution Management
        self.test_substitution_management()
        
        # Test 7: Unit Conversions
        self.test_unit_conversions()
        
        # Test 8: Journey Integration
        self.test_journey_integration()
        
        # Test 9: End-to-End Journey Flow
        self.test_end_to_end_flow()
        
        # Test 10: Error Handling
        self.test_error_handling()
        
        # Display test summary
        self.display_test_summary()
    
    def test_intent_classification(self):
        """Test intent classification for grocery assistance"""
        print("\n🔍 TEST 1: Intent Classification")
        print("-" * 40)
        
        test_cases = [
            ("Create a grocery list", "grocery_assistance"),
            ("I need a shopping list", "grocery_assistance"),
            ("Generate grocery list from my meal plan", "grocery_assistance"),
            ("What ingredients do I need to buy?", "grocery_assistance"),
            ("Help me with grocery shopping", "grocery_assistance"),
            ("I want to go shopping", "grocery_assistance"),
            ("Find me a recipe", "recipe_discovery"),  # Should NOT match grocery
            ("Plan my meals", "meal_planning")  # Should NOT match grocery
        ]
        
        passed = 0
        total = len(test_cases)
        
        for input_text, expected_intent in test_cases:
            classified_intent = self.intent_classifier.classify_intent(input_text)
            if classified_intent == expected_intent:
                print(f"  ✅ '{input_text}' → {classified_intent}")
                passed += 1
            else:
                print(f"  ❌ '{input_text}' → Expected: {expected_intent}, Got: {classified_intent}")
        
        self.test_results.append(("Intent Classification", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_data_loading(self):
        """Test grocery support data loading"""
        print("\n📊 TEST 2: Data Loading")
        print("-" * 40)
        
        passed = 0
        total = 6
        
        # Test grocery support data loading
        grocery_data = self.data_loader.get_grocery_support()
        if grocery_data:
            print("  ✅ Grocery support data loaded")
            passed += 1
        else:
            print("  ❌ Failed to load grocery support data")
        
        # Test unit conversions
        unit_conversions = self.data_loader.get_unit_conversions()
        if unit_conversions and 'volume' in unit_conversions:
            print("  ✅ Unit conversions loaded")
            passed += 1
        else:
            print("  ❌ Failed to load unit conversions")
        
        # Test store sections
        store_sections = self.data_loader.get_store_sections()
        if store_sections and 'produce' in store_sections:
            print("  ✅ Store sections loaded")
            passed += 1
        else:
            print("  ❌ Failed to load store sections")
        
        # Test ingredient aliases
        aliases = self.data_loader.get_ingredient_aliases()
        if aliases and 'chicken_breast' in aliases:
            print("  ✅ Ingredient aliases loaded")
            passed += 1
        else:
            print("  ❌ Failed to load ingredient aliases")
        
        # Test substitutions
        substitutions = self.data_loader.get_substitutions()
        if substitutions and 'chicken_breast' in substitutions:
            print("  ✅ Substitutions loaded")
            passed += 1
        else:
            print("  ❌ Failed to load substitutions")
        
        # Test alias lookup
        canonical_name = self.data_loader.find_ingredient_by_alias("grilled chicken breast")
        if canonical_name == "chicken_breast":
            print("  ✅ Alias lookup working")
            passed += 1
        else:
            print(f"  ❌ Alias lookup failed. Expected: chicken_breast, Got: {canonical_name}")
        
        self.test_results.append(("Data Loading", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_ingredient_extraction(self):
        """Test ingredient extraction from various sources"""
        print("\n🥘 TEST 3: Ingredient Extraction")
        print("-" * 40)
        
        passed = 0
        total = 3
        
        # Test manual input extraction
        manual_input = "2 lbs chicken breast, 1 cup quinoa, 3 apples, olive oil"
        manual_ingredients = self.ingredient_extractor.extract_from_manual_input(manual_input)
        
        if manual_ingredients and len(manual_ingredients) == 4:
            print(f"  ✅ Manual extraction: {len(manual_ingredients)} ingredients")
            for ing in manual_ingredients:
                print(f"    - {ing.get('name')} ({ing.get('amount')} {ing.get('unit')})")
            passed += 1
        else:
            print(f"  ❌ Manual extraction failed. Expected 4, got {len(manual_ingredients) if manual_ingredients else 0}")
        
        # Test recipe extraction (using sample data structure)
        sample_recipes = ["recipe_001"]  # Assuming this exists in recipes_raw.json
        recipe_ingredients = self.ingredient_extractor.extract_from_recipes(sample_recipes, 1.0)
        
        if recipe_ingredients:
            print(f"  ✅ Recipe extraction: {len(recipe_ingredients)} ingredients")
            passed += 1
        else:
            print("  ❌ Recipe extraction failed (no recipe data available)")
        
        # Test meal plan extraction
        sample_meal_plan = {
            "Day 1": {
                "breakfast": {
                    "components": [
                        {"name": "oats", "amount": 1, "unit": "cup", "food_id": "food_010"},
                        {"name": "banana", "amount": 1, "unit": "piece", "food_id": "food_035"}
                    ]
                }
            }
        }
        
        meal_plan_ingredients = self.ingredient_extractor.extract_from_meal_plan(sample_meal_plan, 1.0)
        
        if meal_plan_ingredients and len(meal_plan_ingredients) == 2:
            print(f"  ✅ Meal plan extraction: {len(meal_plan_ingredients)} ingredients")
            passed += 1
        else:
            print(f"  ❌ Meal plan extraction failed. Expected 2, got {len(meal_plan_ingredients) if meal_plan_ingredients else 0}")
        
        self.test_results.append(("Ingredient Extraction", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_list_consolidation(self):
        """Test ingredient list consolidation"""
        print("\n🔄 TEST 4: List Consolidation")
        print("-" * 40)
        
        passed = 0
        total = 2
        
        # Test consolidation with duplicate ingredients
        test_ingredients = [
            {"name": "chicken breast", "amount": 1, "unit": "lb", "source": "recipe1"},
            {"name": "grilled chicken breast", "amount": 0.5, "unit": "lb", "source": "recipe2"},
            {"name": "quinoa", "amount": 1, "unit": "cup", "source": "meal_plan"},
            {"name": "cooked quinoa", "amount": 0.5, "unit": "cup", "source": "recipe1"}
        ]
        
        consolidated = self.list_consolidator.consolidate_ingredients(test_ingredients)
        
        if consolidated and len(consolidated) <= 2:  # Should consolidate duplicates
            print(f"  ✅ Consolidation working: {len(test_ingredients)} → {len(consolidated)} ingredients")
            for ing in consolidated:
                print(f"    - {ing.get('display_name', ing.get('name'))}: {ing.get('amount')} {ing.get('unit')}")
            passed += 1
        else:
            print(f"  ❌ Consolidation failed. Expected ≤2, got {len(consolidated) if consolidated else 0}")
        
        # Test empty input
        empty_consolidated = self.list_consolidator.consolidate_ingredients([])
        if empty_consolidated == []:
            print("  ✅ Empty input handled correctly")
            passed += 1
        else:
            print("  ❌ Empty input not handled correctly")
        
        self.test_results.append(("List Consolidation", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_store_organization(self):
        """Test store section organization"""
        print("\n🏪 TEST 5: Store Organization")
        print("-" * 40)
        
        passed = 0
        total = 2
        
        # Test store organization
        test_ingredients = [
            {"name": "chicken_breast", "canonical_name": "chicken_breast", "amount": 1, "unit": "lb", "food_id": "food_001"},
            {"name": "spinach", "canonical_name": "spinach", "amount": 1, "unit": "bunch", "food_id": "food_015"},
            {"name": "quinoa", "canonical_name": "quinoa", "amount": 1, "unit": "cup", "food_id": "food_010"}
        ]
        
        organized = self.store_organizer.organize_by_store_sections(test_ingredients)
        
        if organized and len(organized) >= 2:  # Should organize into different sections
            print(f"  ✅ Store organization: {len(organized)} sections")
            for section, items in organized.items():
                print(f"    - {section}: {len(items)} items")
            passed += 1
        else:
            print(f"  ❌ Store organization failed. Expected ≥2 sections, got {len(organized) if organized else 0}")
        
        # Test section mapping
        section_info = self.store_organizer._get_store_section(test_ingredients[1])  # spinach
        if section_info and 'display_name' in section_info:
            print(f"  ✅ Section mapping: {section_info['display_name']}")
            passed += 1
        else:
            print("  ❌ Section mapping failed")
        
        self.test_results.append(("Store Organization", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_substitution_management(self):
        """Test ingredient substitution management"""
        print("\n🔄 TEST 6: Substitution Management")
        print("-" * 40)
        
        passed = 0
        total = 2
        
        # Test substitution lookup
        test_ingredient = {"canonical_name": "chicken_breast", "name": "chicken breast"}
        substitutions = self.substitution_manager.get_substitutions_for_ingredient(test_ingredient)
        
        if substitutions and len(substitutions) > 0:
            print(f"  ✅ Substitutions found: {len(substitutions)} options")
            for sub in substitutions[:2]:  # Show first 2
                print(f"    - {sub.get('substitute_name')} ({sub.get('ratio')})")
            passed += 1
        else:
            print("  ❌ No substitutions found")
        
        # Test dietary restriction filtering
        dietary_subs = self.substitution_manager.get_substitutions_for_ingredient(
            test_ingredient, ["vegetarian", "vegan"]
        )
        
        if dietary_subs:
            print(f"  ✅ Dietary-filtered substitutions: {len(dietary_subs)} options")
            passed += 1
        else:
            print("  ❌ Dietary filtering failed")
        
        self.test_results.append(("Substitution Management", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_unit_conversions(self):
        """Test unit conversion functionality"""
        print("\n⚖️ TEST 7: Unit Conversions")
        print("-" * 40)
        
        passed = 0
        total = 3
        
        # Test volume conversion
        ml_from_cup = self.data_loader.convert_unit("milk", 1, "cup", "ml")
        if ml_from_cup == 240:  # 1 cup = 240ml
            print(f"  ✅ Volume conversion: 1 cup → {ml_from_cup} ml")
            passed += 1
        else:
            print(f"  ❌ Volume conversion failed. Expected 240, got {ml_from_cup}")
        
        # Test weight conversion
        g_from_lb = self.data_loader.convert_unit("chicken", 1, "lb", "g")
        if abs(g_from_lb - 453.592) < 0.1:  # 1 lb ≈ 453.592g
            print(f"  ✅ Weight conversion: 1 lb → {g_from_lb:.1f} g")
            passed += 1
        else:
            print(f"  ❌ Weight conversion failed. Expected ~453.6, got {g_from_lb}")
        
        # Test ingredient-specific conversion
        flour_g = self.data_loader.convert_unit("flour", 1, "cup", "g")
        if flour_g > 0:  # Should have ingredient-specific conversion
            print(f"  ✅ Ingredient-specific conversion: 1 cup flour → {flour_g} g")
            passed += 1
        else:
            print("  ❌ Ingredient-specific conversion failed")
        
        self.test_results.append(("Unit Conversions", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_journey_integration(self):
        """Test grocery assistance journey integration"""
        print("\n🔗 TEST 8: Journey Integration")
        print("-" * 40)
        
        passed = 0
        total = 3
        
        # Test journey initialization
        try:
            journey_response = self.grocery_journey.start_journey()
            if "How would you like to create your grocery list?" in journey_response:
                print("  ✅ Journey initialization working")
                passed += 1
            else:
                print("  ❌ Journey initialization failed")
        except Exception as e:
            print(f"  ❌ Journey initialization error: {e}")
        
        # Test journey is registered in chatbot manager
        if 'grocery_assistance' in self.chatbot_manager.journeys:
            print("  ✅ Journey registered in chatbot manager")
            passed += 1
        else:
            print("  ❌ Journey not registered in chatbot manager")
        
        # Test journey step processing
        try:
            # Simulate manual input selection
            self.grocery_journey.current_step = "list_source"
            response = self.grocery_journey.process_user_input("3")  # manual entry
            if "MANUAL INGREDIENT ENTRY" in response:
                print("  ✅ Journey step processing working")
                passed += 1
            else:
                print("  ❌ Journey step processing failed")
        except Exception as e:
            print(f"  ❌ Journey step processing error: {e}")
        
        self.test_results.append(("Journey Integration", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_end_to_end_flow(self):
        """Test complete end-to-end grocery assistance flow"""
        print("\n🎯 TEST 9: End-to-End Flow")
        print("-" * 40)
        
        passed = 0
        total = 1
        
        try:
            # Create a fresh journey instance
            test_journey = GroceryAssistanceJourney(self.data_loader, SessionManager())
            
            # Start the journey
            response1 = test_journey.start_journey()
            print("  📝 Journey started")
            
            # Select manual input
            response2 = test_journey.process_user_input("3")
            print("  📝 Selected manual input")
            
            # Add ingredients manually
            response3 = test_journey.process_user_input("2 lbs chicken breast, 1 cup quinoa, spinach, 3 apples")
            print("  📝 Added ingredients manually")
            
            # Check if we got to organization step
            if "How would you like your grocery list organized?" in response3:
                print("  📝 Reached organization step")
                
                # Select store sections organization
                response4 = test_journey.process_user_input("1")
                
                # Check if final list was generated
                if "YOUR GROCERY LIST IS READY" in response4:
                    print("  ✅ End-to-end flow completed successfully")
                    print("  📋 Final grocery list generated with store sections")
                    passed += 1
                else:
                    print("  ❌ Final list generation failed")
            else:
                print("  ❌ Failed to reach organization step")
                
        except Exception as e:
            print(f"  ❌ End-to-end flow error: {e}")
        
        self.test_results.append(("End-to-End Flow", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        print("\n⚠️ TEST 10: Error Handling")
        print("-" * 40)
        
        passed = 0
        total = 4
        
        # Test invalid input handling
        try:
            response = self.grocery_journey.process_user_input("invalid_input")
            if "didn't understand" in response.lower() or "please choose" in response.lower():
                print("  ✅ Invalid input handled gracefully")
                passed += 1
            else:
                print("  ❌ Invalid input not handled properly")
        except Exception as e:
            print(f"  ❌ Invalid input caused error: {e}")
        
        # Test empty ingredient list
        try:
            empty_consolidated = self.list_consolidator.consolidate_ingredients([])
            if empty_consolidated == []:
                print("  ✅ Empty ingredient list handled")
                passed += 1
            else:
                print("  ❌ Empty ingredient list not handled")
        except Exception as e:
            print(f"  ❌ Empty ingredient list caused error: {e}")
        
        # Test malformed ingredient data
        try:
            bad_ingredient = {"name": "", "amount": "invalid", "unit": None}
            section_info = self.store_organizer._get_store_section(bad_ingredient)
            if section_info and 'display_name' in section_info:
                print("  ✅ Malformed ingredient data handled")
                passed += 1
            else:
                print("  ❌ Malformed ingredient data not handled")
        except Exception as e:
            print(f"  ❌ Malformed ingredient data caused error: {e}")
        
        # Test missing data graceful handling
        try:
            fake_substitutions = self.substitution_manager.get_substitutions_for_ingredient(
                {"canonical_name": "nonexistent_ingredient"}
            )
            if fake_substitutions == []:
                print("  ✅ Missing substitution data handled")
                passed += 1
            else:
                print("  ❌ Missing substitution data not handled")
        except Exception as e:
            print(f"  ❌ Missing substitution data caused error: {e}")
        
        self.test_results.append(("Error Handling", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def display_test_summary(self):
        """Display comprehensive test summary"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 60)
        
        total_passed = 0
        total_tests = 0
        
        for test_name, passed, total in self.test_results:
            percentage = (passed / total * 100) if total > 0 else 0
            status = "✅ PASS" if passed == total else "⚠️ PARTIAL" if passed > 0 else "❌ FAIL"
            print(f"{test_name:<25} {passed:>2}/{total:<2} ({percentage:>5.1f}%) {status}")
            total_passed += passed
            total_tests += total
        
        print("-" * 60)
        overall_percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0
        print(f"{'OVERALL RESULT':<25} {total_passed:>2}/{total_tests:<2} ({overall_percentage:>5.1f}%)")
        
        if overall_percentage >= 90:
            print("\n🎉 EXCELLENT! Grocery assistance is working perfectly!")
        elif overall_percentage >= 75:
            print("\n✅ GOOD! Grocery assistance is working well with minor issues.")
        elif overall_percentage >= 50:
            print("\n⚠️ PARTIAL! Grocery assistance has some issues that need attention.")
        else:
            print("\n❌ POOR! Grocery assistance needs significant fixes.")
        
        # Test completion message
        print("\n" + "=" * 60)
        print("🛒 GROCERY ASSISTANCE TESTING COMPLETE")
        print("=" * 60)
        
        if overall_percentage >= 75:
            print("The grocery assistance journey is ready for use!")
            print("\n💡 Try these commands to test manually:")
            print("   • 'Create a grocery list'")
            print("   • 'I need ingredients for shopping'")
            print("   • 'Generate shopping list from recipes'")
            print("   • 'Help me with grocery shopping'")

def main():
    """Run the comprehensive grocery assistance test suite"""
    print("🚀 Initializing Grocery Assistance Test Suite...")
    
    try:
        # Initialize and run tests
        test_suite = GroceryAssistanceTest()
        test_suite.run_all_tests()
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print("Please check your installation and data files.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())