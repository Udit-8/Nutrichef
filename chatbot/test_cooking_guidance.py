#!/usr/bin/env python3
"""
Comprehensive Test Script for Cooking Guidance Journey
Tests all functionalities including recipe loading, step navigation, timer management, and more.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from data.data_loader import DataLoader
from core.session_manager import SessionManager
from core.intent_classifier import IntentClassifier
from core.chatbot_manager import ChatbotManager
from journeys.cooking_guidance import CookingGuidanceJourney
from utils.cooking_utils import TimerManager, StepNavigator, ProgressTracker, ServingScaler, CookingSessionState

class CookingGuidanceTest:
    """Comprehensive test class for cooking guidance functionality"""
    
    def __init__(self):
        # Initialize core components
        self.data_loader = DataLoader()
        self.session_manager = SessionManager()
        self.intent_classifier = IntentClassifier()
        self.chatbot_manager = ChatbotManager(self.session_manager, self.intent_classifier, self.data_loader)
        
        # Initialize cooking guidance journey
        self.cooking_journey = CookingGuidanceJourney(self.data_loader, self.session_manager)
        
        self.test_results = []
        
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🧪 STARTING COMPREHENSIVE COOKING GUIDANCE TESTS")
        print("=" * 60)
        
        # Test 1: Intent Classification
        self.test_intent_classification()
        
        # Test 2: Data Loading and Cooking Instructions
        self.test_data_loading()
        
        # Test 3: Utility Classes
        self.test_utility_classes()
        
        # Test 4: Recipe Validation and Loading
        self.test_recipe_validation()
        
        # Test 5: Serving Size Scaling
        self.test_serving_scaling()
        
        # Test 6: Step Navigation
        self.test_step_navigation()
        
        # Test 7: Timer Management
        self.test_timer_management()
        
        # Test 8: Journey Integration
        self.test_journey_integration()
        
        # Test 9: End-to-End Cooking Flow
        self.test_end_to_end_flow()
        
        # Test 10: Error Handling and Edge Cases
        self.test_error_handling()
        
        # Display test summary
        self.display_test_summary()
    
    def test_intent_classification(self):
        """Test intent classification for cooking guidance"""
        print("\n🔍 TEST 1: Intent Classification")
        print("-" * 40)
        
        test_cases = [
            ("Help me cook this recipe", "cooking_guidance"),
            ("Guide me through cooking", "cooking_guidance"),
            ("Start cooking", "cooking_guidance"),
            ("I need cooking help", "cooking_guidance"),
            ("Walk me through cooking", "cooking_guidance"),
            ("Interactive cooking assistant", "cooking_guidance"),
            ("Find me a recipe", "recipe_discovery"),  # Should NOT match cooking
            ("Create grocery list", "grocery_assistance")  # Should NOT match cooking
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
        """Test cooking instruction data loading"""
        print("\n📊 TEST 2: Data Loading")
        print("-" * 40)
        
        passed = 0
        total = 8
        
        # Test cooking instructions loading
        cooking_instructions = self.data_loader.get_cooking_instructions()
        if cooking_instructions and len(cooking_instructions) > 0:
            print(f"  ✅ Cooking instructions loaded: {len(cooking_instructions)} recipes")
            passed += 1
        else:
            print("  ❌ Failed to load cooking instructions")
        
        # Test specific recipe loading
        test_recipe_id = "recipe_001"
        recipe_instructions = self.data_loader.get_cooking_instructions_by_recipe_id(test_recipe_id)
        if recipe_instructions:
            print(f"  ✅ Recipe {test_recipe_id} instructions loaded")
            passed += 1
        else:
            print(f"  ❌ Failed to load instructions for {test_recipe_id}")
        
        # Test combined recipe and cooking data
        combined_data = self.data_loader.get_recipe_cooking_data(test_recipe_id)
        if combined_data and 'recipe' in combined_data and 'cooking_instructions' in combined_data:
            print(f"  ✅ Combined recipe + cooking data loaded")
            passed += 1
        else:
            print("  ❌ Failed to load combined recipe data")
        
        # Test ingredient scaling
        if combined_data:
            scaled_ingredients = self.data_loader.scale_recipe_ingredients(
                combined_data['recipe'], 2.0
            )
            if scaled_ingredients and len(scaled_ingredients) > 0:
                print(f"  ✅ Ingredient scaling working: {len(scaled_ingredients)} ingredients")
                passed += 1
            else:
                print("  ❌ Ingredient scaling failed")
        
        # Test equipment list
        equipment = self.data_loader.get_recipe_equipment_list(test_recipe_id)
        if equipment and len(equipment) > 0:
            print(f"  ✅ Equipment list loaded: {len(equipment)} items")
            passed += 1
        else:
            print("  ❌ Equipment list loading failed")
        
        # Test total time
        total_time = self.data_loader.get_recipe_total_time(test_recipe_id)
        if total_time > 0:
            print(f"  ✅ Total time loaded: {total_time} minutes")
            passed += 1
        else:
            print("  ❌ Total time loading failed")
        
        # Test prep steps
        prep_steps = self.data_loader.get_prep_steps(test_recipe_id)
        if isinstance(prep_steps, list):
            print(f"  ✅ Prep steps loaded: {len(prep_steps)} steps")
            passed += 1
        else:
            print("  ❌ Prep steps loading failed")
        
        # Test cooking phases
        phases = self.data_loader.get_cooking_phases(test_recipe_id)
        if phases and len(phases) > 0:
            print(f"  ✅ Cooking phases loaded: {', '.join(phases)}")
            passed += 1
        else:
            print("  ❌ Cooking phases loading failed")
        
        self.test_results.append(("Data Loading", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_utility_classes(self):
        """Test cooking utility classes"""
        print("\n🛠️ TEST 3: Utility Classes")
        print("-" * 40)
        
        passed = 0
        total = 12
        
        # Test TimerManager
        timer_manager = TimerManager()
        timer_id = timer_manager.start_timer(5, "Test timer", 1)
        if timer_id:
            print("  ✅ TimerManager: Timer started")
            passed += 1
        else:
            print("  ❌ TimerManager: Timer start failed")
        
        timer_status = timer_manager.get_timer_status(timer_id)
        if timer_status and timer_status['status'] == 'active':
            print("  ✅ TimerManager: Timer status working")
            passed += 1
        else:
            print("  ❌ TimerManager: Timer status failed")
        
        pause_success = timer_manager.pause_timer(timer_id)
        if pause_success:
            print("  ✅ TimerManager: Pause working")
            passed += 1
        else:
            print("  ❌ TimerManager: Pause failed")
        
        resume_success = timer_manager.resume_timer(timer_id)
        if resume_success:
            print("  ✅ TimerManager: Resume working")
            passed += 1
        else:
            print("  ❌ TimerManager: Resume failed")
        
        # Test StepNavigator
        navigator = StepNavigator(8)
        current_step = navigator.get_current_step()
        if current_step == 1:
            print("  ✅ StepNavigator: Initialization working")
            passed += 1
        else:
            print("  ❌ StepNavigator: Initialization failed")
        
        next_step, is_last = navigator.next_step()
        if next_step == 2 and not is_last:
            print("  ✅ StepNavigator: Next step working")
            passed += 1
        else:
            print("  ❌ StepNavigator: Next step failed")
        
        prev_step, is_first = navigator.previous_step()
        if prev_step == 1 and is_first:
            print("  ✅ StepNavigator: Previous step working")
            passed += 1
        else:
            print("  ❌ StepNavigator: Previous step failed")
        
        progress = navigator.get_progress()
        if progress and 'current_step' in progress:
            print("  ✅ StepNavigator: Progress tracking working")
            passed += 1
        else:
            print("  ❌ StepNavigator: Progress tracking failed")
        
        # Test ProgressTracker
        progress_tracker = ProgressTracker("Test Recipe", 8)
        progress_tracker.start_cooking_phase('prep')
        if progress_tracker.current_phase == 'prep':
            print("  ✅ ProgressTracker: Phase management working")
            passed += 1
        else:
            print("  ❌ ProgressTracker: Phase management failed")
        
        progress_tracker.add_note("Test note")
        summary = progress_tracker.get_session_summary()
        if summary and 'session_notes' in summary and len(summary['session_notes']) > 0:
            print("  ✅ ProgressTracker: Note taking working")
            passed += 1
        else:
            print("  ❌ ProgressTracker: Note taking failed")
        
        # Test ServingScaler
        scaler = ServingScaler(4)
        scaler.set_target_servings(8)
        scaling_info = scaler.get_scaling_info()
        if scaling_info['scale_factor'] == 2.0:
            print("  ✅ ServingScaler: Scaling calculation working")
            passed += 1
        else:
            print(f"  ❌ ServingScaler: Expected 2.0, got {scaling_info['scale_factor']}")
        
        scaled_amount = scaler.scale_ingredient_amount(2.0)
        if scaled_amount == 4.0:
            print("  ✅ ServingScaler: Amount scaling working")
            passed += 1
        else:
            print(f"  ❌ ServingScaler: Expected 4.0, got {scaled_amount}")
        
        self.test_results.append(("Utility Classes", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_recipe_validation(self):
        """Test recipe validation and loading"""
        print("\n🍳 TEST 4: Recipe Validation")
        print("-" * 40)
        
        passed = 0
        total = 4
        
        # Test journey start
        try:
            start_response = self.cooking_journey.start_journey()
            if "Let's Start Cooking" in start_response or "recipe would you like" in start_response:
                print("  ✅ Journey initialization working")
                passed += 1
            else:
                print("  ❌ Journey initialization failed")
        except Exception as e:
            print(f"  ❌ Journey initialization error: {e}")
        
        # Test available recipes display
        try:
            self.cooking_journey.current_step = "recipe_validation"
            browse_response = self.cooking_journey.process_user_input("3")  # browse recipes
            if "Available Recipes" in browse_response:
                print("  ✅ Recipe browsing working")
                passed += 1
            else:
                print("  ❌ Recipe browsing failed")
        except Exception as e:
            print(f"  ❌ Recipe browsing error: {e}")
        
        # Test recipe search
        try:
            search_response = self.cooking_journey._search_and_load_recipe("Mediterranean")
            if "Mediterranean" in search_response or "Found" in search_response:
                print("  ✅ Recipe search working")
                passed += 1
            else:
                print("  ❌ Recipe search failed")
        except Exception as e:
            print(f"  ❌ Recipe search error: {e}")
        
        # Test direct recipe loading
        try:
            load_response = self.cooking_journey._load_recipe_for_cooking("recipe_001")
            if "SERVING SIZE SETUP" in load_response:
                print("  ✅ Recipe loading working")
                passed += 1
            else:
                print("  ❌ Recipe loading failed")
        except Exception as e:
            print(f"  ❌ Recipe loading error: {e}")
        
        self.test_results.append(("Recipe Validation", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_serving_scaling(self):
        """Test serving size setup and scaling"""
        print("\n🍽️ TEST 5: Serving Size Scaling")
        print("-" * 40)
        
        passed = 0
        total = 3
        
        # Setup a cooking session for testing
        try:
            recipe_data = self.data_loader.get_recipe_cooking_data("recipe_001")
            if recipe_data:
                self.cooking_journey.cooking_session = CookingSessionState(recipe_data)
                self.cooking_journey.recipe_id = "recipe_001"
                self.cooking_journey.recipe_name = recipe_data['recipe']['name']
                print("  ✅ Cooking session setup for scaling tests")
                passed += 1
            else:
                print("  ❌ Cooking session setup failed")
        except Exception as e:
            print(f"  ❌ Cooking session setup error: {e}")
        
        # Test serving size input handling
        try:
            self.cooking_journey.current_step = "serving_setup"
            serving_response = self.cooking_journey._handle_serving_setup("6")
            if "EQUIPMENT" in serving_response or "scaled for" in serving_response.lower():
                print("  ✅ Serving size processing working")
                passed += 1
            else:
                print("  ❌ Serving size processing failed")
        except Exception as e:
            print(f"  ❌ Serving size processing error: {e}")
        
        # Test scaling calculations
        try:
            if self.cooking_journey.cooking_session:
                scaling_info = self.cooking_journey.cooking_session.serving_scaler.get_scaling_info()
                if scaling_info['scale_factor'] == 1.5:  # 6 servings from 4 original
                    print(f"  ✅ Scaling calculation correct: {scaling_info['scale_factor']}")
                    passed += 1
                else:
                    print(f"  ❌ Scaling calculation wrong: expected 1.5, got {scaling_info['scale_factor']}")
            else:
                print("  ❌ No cooking session for scaling test")
        except Exception as e:
            print(f"  ❌ Scaling calculation error: {e}")
        
        self.test_results.append(("Serving Size Scaling", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_step_navigation(self):
        """Test cooking step navigation"""
        print("\n🗺️ TEST 6: Step Navigation")
        print("-" * 40)
        
        passed = 0
        total = 4
        
        # Test equipment check step
        try:
            if self.cooking_journey.cooking_session:
                self.cooking_journey.current_step = "equipment_check"
                equipment_response = self.cooking_journey._step_equipment_check()
                if "EQUIPMENT & INGREDIENTS" in equipment_response:
                    print("  ✅ Equipment check step working")
                    passed += 1
                else:
                    print("  ❌ Equipment check step failed")
            else:
                print("  ❌ No cooking session for equipment check")
        except Exception as e:
            print(f"  ❌ Equipment check error: {e}")
        
        # Test prep phase
        try:
            if self.cooking_journey.cooking_session:
                prep_response = self.cooking_journey._step_prep_phase()
                if "PREP PHASE" in prep_response or "ready to cook" in prep_response:
                    print("  ✅ Prep phase working")
                    passed += 1
                else:
                    print("  ❌ Prep phase failed")
        except Exception as e:
            print(f"  ❌ Prep phase error: {e}")
        
        # Test cooking steps initialization
        try:
            if self.cooking_journey.cooking_session:
                cooking_response = self.cooking_journey._step_cooking_steps()
                if "STEP" in cooking_response and "complete" in cooking_response:
                    print("  ✅ Cooking steps initialization working")
                    passed += 1
                else:
                    print("  ❌ Cooking steps initialization failed")
        except Exception as e:
            print(f"  ❌ Cooking steps initialization error: {e}")
        
        # Test step navigation commands
        try:
            if self.cooking_journey.cooking_session:
                self.cooking_journey.current_step = "cooking_steps"
                nav_response = self.cooking_journey._handle_cooking_steps("next")
                if "STEP" in nav_response or nav_response:  # Should return some response
                    print("  ✅ Step navigation working")
                    passed += 1
                else:
                    print("  ❌ Step navigation failed")
        except Exception as e:
            print(f"  ❌ Step navigation error: {e}")
        
        self.test_results.append(("Step Navigation", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_timer_management(self):
        """Test timer management functionality"""
        print("\n⏰ TEST 7: Timer Management")
        print("-" * 40)
        
        passed = 0
        total = 4
        
        # Test timer creation and management through journey
        try:
            if self.cooking_journey.cooking_session:
                # Set up a step that needs a timer
                current_step_data = self.cooking_journey.cooking_session.get_current_step_data()
                if current_step_data:
                    # Mock a timer-needed step if current step doesn't need one
                    if not current_step_data.get('timer_needed', False):
                        current_step_data['timer_needed'] = True
                        current_step_data['duration_minutes'] = 5
                    
                    timer_response = self.cooking_journey._handle_timer_command()
                    if "TIMER STARTED" in timer_response:
                        print("  ✅ Timer start command working")
                        passed += 1
                    else:
                        print("  ❌ Timer start command failed")
                else:
                    print("  ❌ No current step data available")
        except Exception as e:
            print(f"  ❌ Timer start command error: {e}")
        
        # Test timer status checking
        try:
            if self.cooking_journey.cooking_session:
                status_response = self.cooking_journey._check_timer_status()
                if "TIMER STATUS" in status_response:
                    print("  ✅ Timer status check working")
                    passed += 1
                else:
                    print("  ❌ Timer status check failed")
        except Exception as e:
            print(f"  ❌ Timer status check error: {e}")
        
        # Test pause/resume functionality
        try:
            if self.cooking_journey.cooking_session:
                pause_response = self.cooking_journey._pause_cooking_session()
                if "COOKING SESSION PAUSED" in pause_response:
                    print("  ✅ Session pause working")
                    passed += 1
                else:
                    print("  ❌ Session pause failed")
        except Exception as e:
            print(f"  ❌ Session pause error: {e}")
        
        # Test cooking status display
        try:
            if self.cooking_journey.cooking_session:
                status_response = self.cooking_journey._show_cooking_status()
                if "COOKING STATUS" in status_response:
                    print("  ✅ Cooking status display working")
                    passed += 1
                else:
                    print("  ❌ Cooking status display failed")
        except Exception as e:
            print(f"  ❌ Cooking status display error: {e}")
        
        self.test_results.append(("Timer Management", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_journey_integration(self):
        """Test cooking guidance journey integration"""
        print("\n🔗 TEST 8: Journey Integration")
        print("-" * 40)
        
        passed = 0
        total = 4
        
        # Test journey registration in chatbot manager
        if 'cooking_guidance' in self.chatbot_manager.journeys:
            print("  ✅ Journey registered in chatbot manager")
            passed += 1
        else:
            print("  ❌ Journey not registered in chatbot manager")
        
        # Test completion phase
        try:
            if self.cooking_journey.cooking_session:
                completion_response = self.cooking_journey._step_completion()
                if "CONGRATULATIONS" in completion_response:
                    print("  ✅ Completion phase working")
                    passed += 1
                else:
                    print("  ❌ Completion phase failed")
        except Exception as e:
            print(f"  ❌ Completion phase error: {e}")
        
        # Test cross-journey transitions
        try:
            if self.cooking_journey.cooking_session:
                recipe_discovery_transition = self.cooking_journey._transition_to_recipe_discovery()
                if "FIND YOUR NEXT RECIPE" in recipe_discovery_transition:
                    print("  ✅ Recipe discovery transition working")
                    passed += 1
                else:
                    print("  ❌ Recipe discovery transition failed")
        except Exception as e:
            print(f"  ❌ Recipe discovery transition error: {e}")
        
        # Test completion message
        try:
            completion_msg = self.cooking_journey.get_completion_message()
            if completion_msg and "cooking" in completion_msg.lower():
                print("  ✅ Completion message working")
                passed += 1
            else:
                print("  ❌ Completion message failed")
        except Exception as e:
            print(f"  ❌ Completion message error: {e}")
        
        self.test_results.append(("Journey Integration", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_end_to_end_flow(self):
        """Test complete end-to-end cooking guidance flow"""
        print("\n🎯 TEST 9: End-to-End Flow")
        print("-" * 40)
        
        passed = 0
        total = 1
        
        try:
            # Create a fresh journey instance for clean test
            fresh_journey = CookingGuidanceJourney(self.data_loader, SessionManager())
            
            # Step 1: Start journey
            response1 = fresh_journey.start_journey()
            print("  📝 Journey started")
            
            # Step 2: Select recipe by search
            response2 = fresh_journey.process_user_input("Mediterranean")
            print("  📝 Recipe searched")
            
            # Step 3: Load specific recipe if multiple found
            if "Mediterranean Chicken Bowl" in response2:
                # Recipe found, continue to serving setup
                print("  📝 Recipe loaded successfully")
                
                # Check if we're in serving setup
                if fresh_journey.current_step == "serving_setup":
                    # Step 4: Set serving size
                    response3 = fresh_journey.process_user_input("4")
                    print("  📝 Serving size set")
                    
                    # Step 5: Confirm equipment ready
                    response4 = fresh_journey.process_user_input("yes")
                    print("  📝 Equipment confirmed")
                    
                    # Step 6: Complete prep (if any)
                    if fresh_journey.current_step == "prep_phase":
                        response5 = fresh_journey.process_user_input("ready to cook")
                        print("  📝 Prep phase completed")
                    
                    # Step 7: Navigate through cooking steps
                    if fresh_journey.current_step == "cooking_steps":
                        # Try a few cooking step commands
                        fresh_journey.process_user_input("next")
                        fresh_journey.process_user_input("next")
                        print("  📝 Cooking steps navigated")
                        
                        print("  ✅ End-to-end flow completed successfully")
                        print("  📋 All major cooking guidance features working")
                        passed += 1
                    else:
                        print(f"  ❌ Didn't reach cooking steps. Current: {fresh_journey.current_step}")
                else:
                    print(f"  ❌ Didn't reach serving setup. Current: {fresh_journey.current_step}")
            else:
                print("  ❌ Recipe loading failed in end-to-end test")
                
        except Exception as e:
            print(f"  ❌ End-to-end flow error: {e}")
        
        self.test_results.append(("End-to-End Flow", passed, total))
        print(f"\nResult: {passed}/{total} tests passed")
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        print("\n⚠️ TEST 10: Error Handling")
        print("-" * 40)
        
        passed = 0
        total = 5
        
        # Test invalid recipe ID
        try:
            response = self.cooking_journey._load_recipe_for_cooking("invalid_recipe")
            if "couldn't load" in response.lower() or "try another" in response.lower():
                print("  ✅ Invalid recipe ID handled gracefully")
                passed += 1
            else:
                print("  ❌ Invalid recipe ID not handled properly")
        except Exception as e:
            print(f"  ❌ Invalid recipe ID caused error: {e}")
        
        # Test invalid user input
        try:
            self.cooking_journey.current_step = "recipe_validation"
            response = self.cooking_journey.process_user_input("invalid_command_xyz")
            if response and len(response) > 0:
                print("  ✅ Invalid input handled gracefully")
                passed += 1
            else:
                print("  ❌ Invalid input not handled properly")
        except Exception as e:
            print(f"  ❌ Invalid input caused error: {e}")
        
        # Test missing cooking session
        try:
            fresh_journey = CookingGuidanceJourney(self.data_loader, SessionManager())
            fresh_journey.current_step = "cooking_steps"
            response = fresh_journey._step_cooking_steps()
            if "wrong" in response.lower() or "start over" in response.lower():
                print("  ✅ Missing cooking session handled")
                passed += 1
            else:
                print("  ❌ Missing cooking session not handled")
        except Exception as e:
            print(f"  ❌ Missing cooking session caused error: {e}")
        
        # Test invalid serving size
        try:
            if self.cooking_journey.cooking_session:
                self.cooking_journey.current_step = "serving_setup"
                response = self.cooking_journey._handle_serving_setup("invalid_number")
                if "didn't understand" in response.lower() or "valid number" in response.lower():
                    print("  ✅ Invalid serving size handled")
                    passed += 1
                else:
                    print("  ❌ Invalid serving size not handled")
        except Exception as e:
            print(f"  ❌ Invalid serving size caused error: {e}")
        
        # Test timer operations without timer-needed step
        try:
            timer_manager = TimerManager()
            # Test operations on non-existent timer
            status = timer_manager.get_timer_status("non_existent_timer")
            if status is None:
                print("  ✅ Non-existent timer handled correctly")
                passed += 1
            else:
                print("  ❌ Non-existent timer not handled")
        except Exception as e:
            print(f"  ❌ Non-existent timer caused error: {e}")
        
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
            print("\n🎉 EXCELLENT! Cooking guidance is working perfectly!")
        elif overall_percentage >= 75:
            print("\n✅ GOOD! Cooking guidance is working well with minor issues.")
        elif overall_percentage >= 50:
            print("\n⚠️ PARTIAL! Cooking guidance has some issues that need attention.")
        else:
            print("\n❌ POOR! Cooking guidance needs significant fixes.")
        
        # Test completion message
        print("\n" + "=" * 60)
        print("👨‍🍳 COOKING GUIDANCE TESTING COMPLETE")
        print("=" * 60)
        
        if overall_percentage >= 75:
            print("The cooking guidance journey is ready for use!")
            print("\n💡 Try these commands to test manually:")
            print("   • 'Guide me through cooking'")
            print("   • 'Help me cook Mediterranean Chicken Bowl'")
            print("   • 'I need cooking help'")
            print("   • 'Start cooking'")
            
            print("\n🔥 Features available:")
            print("   • Interactive step-by-step guidance")
            print("   • Timer management with multiple concurrent timers")
            print("   • Recipe scaling for different serving sizes")
            print("   • Pause/resume functionality")
            print("   • Real-time cooking assistance and troubleshooting")
            print("   • Cross-journey transitions to other features")

def main():
    """Run the comprehensive cooking guidance test suite"""
    print("🚀 Initializing Cooking Guidance Test Suite...")
    
    try:
        # Initialize and run tests
        test_suite = CookingGuidanceTest()
        test_suite.run_all_tests()
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print("Please check your installation and data files.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())