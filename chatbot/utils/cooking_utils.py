"""
Cooking Utility Classes
Handles timer management, step navigation, progress tracking, and serving scaling for cooking guidance
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import threading

class TimerManager:
    """Manages multiple concurrent cooking timers"""
    
    def __init__(self):
        self.active_timers = {}  # timer_id -> timer_info
        self.completed_timers = {}
        self.timer_counter = 0
    
    def start_timer(self, duration_minutes: int, description: str, step_number: int = None) -> str:
        """Start a new timer and return timer ID"""
        timer_id = f"timer_{self.timer_counter}"
        self.timer_counter += 1
        
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        timer_info = {
            'timer_id': timer_id,
            'description': description,
            'duration_minutes': duration_minutes,
            'step_number': step_number,
            'start_time': start_time,
            'end_time': end_time,
            'status': 'active',
            'remaining_minutes': duration_minutes
        }
        
        self.active_timers[timer_id] = timer_info
        return timer_id
    
    def get_timer_status(self, timer_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a timer"""
        if timer_id in self.active_timers:
            timer_info = self.active_timers[timer_id]
            now = datetime.now()
            
            if now >= timer_info['end_time']:
                # Timer has expired
                timer_info['status'] = 'completed'
                timer_info['remaining_minutes'] = 0
                self.completed_timers[timer_id] = self.active_timers.pop(timer_id)
                return self.completed_timers[timer_id]
            else:
                # Timer still active
                remaining = timer_info['end_time'] - now
                timer_info['remaining_minutes'] = max(0, remaining.total_seconds() / 60)
                return timer_info
        
        elif timer_id in self.completed_timers:
            return self.completed_timers[timer_id]
        
        return None
    
    def get_all_active_timers(self) -> List[Dict[str, Any]]:
        """Get status of all active timers"""
        active_status = []
        expired_timers = []
        
        for timer_id in list(self.active_timers.keys()):
            status = self.get_timer_status(timer_id)
            if status and status['status'] == 'active':
                active_status.append(status)
            elif status and status['status'] == 'completed':
                expired_timers.append(status)
        
        return active_status, expired_timers
    
    def pause_timer(self, timer_id: str) -> bool:
        """Pause a specific timer"""
        if timer_id in self.active_timers:
            timer_info = self.active_timers[timer_id]
            if timer_info['status'] == 'active':
                now = datetime.now()
                remaining_time = timer_info['end_time'] - now
                timer_info['remaining_seconds'] = max(0, remaining_time.total_seconds())
                timer_info['status'] = 'paused'
                timer_info['paused_at'] = now
                return True
        return False
    
    def resume_timer(self, timer_id: str) -> bool:
        """Resume a paused timer"""
        if timer_id in self.active_timers:
            timer_info = self.active_timers[timer_id]
            if timer_info['status'] == 'paused' and 'remaining_seconds' in timer_info:
                now = datetime.now()
                timer_info['end_time'] = now + timedelta(seconds=timer_info['remaining_seconds'])
                timer_info['status'] = 'active'
                del timer_info['remaining_seconds']
                del timer_info['paused_at']
                return True
        return False
    
    def cancel_timer(self, timer_id: str) -> bool:
        """Cancel a timer"""
        if timer_id in self.active_timers:
            self.active_timers[timer_id]['status'] = 'cancelled'
            del self.active_timers[timer_id]
            return True
        return False
    
    def get_expired_timers(self) -> List[Dict[str, Any]]:
        """Get all timers that have recently expired"""
        _, expired_timers = self.get_all_active_timers()
        return expired_timers
    
    def pause_all_timers(self):
        """Pause all active timers"""
        for timer_id in list(self.active_timers.keys()):
            self.pause_timer(timer_id)
    
    def resume_all_timers(self):
        """Resume all paused timers"""
        for timer_id in list(self.active_timers.keys()):
            self.resume_timer(timer_id)

class StepNavigator:
    """Handles navigation through cooking steps"""
    
    def __init__(self, total_steps: int):
        self.total_steps = total_steps
        self.current_step = 1
        self.step_history = [1]  # Track visited steps
        self.completed_steps = set()
    
    def next_step(self) -> Tuple[int, bool]:
        """Move to next step, returns (step_number, is_last_step)"""
        if self.current_step < self.total_steps:
            self.completed_steps.add(self.current_step)
            self.current_step += 1
            self.step_history.append(self.current_step)
            return self.current_step, (self.current_step == self.total_steps)
        return self.current_step, True
    
    def previous_step(self) -> Tuple[int, bool]:
        """Move to previous step, returns (step_number, is_first_step)"""
        if self.current_step > 1:
            self.current_step -= 1
            if self.current_step in self.completed_steps:
                self.completed_steps.remove(self.current_step)
            self.step_history.append(self.current_step)
            return self.current_step, (self.current_step == 1)
        return self.current_step, True
    
    def jump_to_step(self, step_number: int) -> bool:
        """Jump directly to a specific step"""
        if 1 <= step_number <= self.total_steps:
            self.current_step = step_number
            self.step_history.append(step_number)
            return True
        return False
    
    def get_current_step(self) -> int:
        """Get current step number"""
        return self.current_step
    
    def get_progress(self) -> Dict[str, Any]:
        """Get progress information"""
        return {
            'current_step': self.current_step,
            'total_steps': self.total_steps,
            'completed_steps': len(self.completed_steps),
            'progress_percentage': (len(self.completed_steps) / self.total_steps) * 100,
            'is_first_step': self.current_step == 1,
            'is_last_step': self.current_step == self.total_steps
        }
    
    def mark_step_complete(self, step_number: int = None):
        """Mark a step as completed"""
        step_to_mark = step_number or self.current_step
        if 1 <= step_to_mark <= self.total_steps:
            self.completed_steps.add(step_to_mark)
    
    def is_step_completed(self, step_number: int) -> bool:
        """Check if a step has been completed"""
        return step_number in self.completed_steps

class ProgressTracker:
    """Tracks overall cooking session progress"""
    
    def __init__(self, recipe_name: str, total_steps: int):
        self.recipe_name = recipe_name
        self.total_steps = total_steps
        self.session_start_time = datetime.now()
        self.current_phase = None
        self.completed_phases = []
        self.session_notes = []
        self.modifications = []
        self.session_status = 'prep'  # prep, cooking, paused, completed
    
    def start_cooking_phase(self, phase: str):
        """Start a new cooking phase"""
        if self.current_phase and self.current_phase not in self.completed_phases:
            self.completed_phases.append(self.current_phase)
        self.current_phase = phase
        
        if phase == 'cooking':
            self.session_status = 'cooking'
    
    def pause_session(self):
        """Pause the cooking session"""
        self.session_status = 'paused'
        self.add_note(f"Session paused at {datetime.now().strftime('%H:%M')}")
    
    def resume_session(self):
        """Resume the cooking session"""
        previous_status = 'cooking' if self.current_phase != 'prep' else 'prep'
        self.session_status = previous_status
        self.add_note(f"Session resumed at {datetime.now().strftime('%H:%M')}")
    
    def complete_session(self):
        """Mark session as completed"""
        self.session_status = 'completed'
        if self.current_phase and self.current_phase not in self.completed_phases:
            self.completed_phases.append(self.current_phase)
    
    def add_note(self, note: str):
        """Add a cooking session note"""
        timestamp = datetime.now().strftime('%H:%M')
        self.session_notes.append(f"[{timestamp}] {note}")
    
    def add_modification(self, step_number: int, modification: str):
        """Record a modification made during cooking"""
        self.modifications.append({
            'step_number': step_number,
            'modification': modification,
            'timestamp': datetime.now()
        })
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get comprehensive session summary"""
        elapsed_time = datetime.now() - self.session_start_time
        
        return {
            'recipe_name': self.recipe_name,
            'session_status': self.session_status,
            'elapsed_time_minutes': elapsed_time.total_seconds() / 60,
            'current_phase': self.current_phase,
            'completed_phases': self.completed_phases,
            'session_notes': self.session_notes,
            'modifications': self.modifications,
            'start_time': self.session_start_time.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_time_estimate(self, total_estimated_minutes: int) -> Dict[str, Any]:
        """Get time estimates for completion"""
        elapsed_minutes = (datetime.now() - self.session_start_time).total_seconds() / 60
        
        return {
            'elapsed_minutes': round(elapsed_minutes, 1),
            'estimated_total_minutes': total_estimated_minutes,
            'estimated_remaining_minutes': max(0, total_estimated_minutes - elapsed_minutes),
            'is_over_estimate': elapsed_minutes > total_estimated_minutes
        }

class ServingScaler:
    """Handles scaling of recipe ingredients and timing based on serving size"""
    
    def __init__(self, original_servings: int):
        self.original_servings = original_servings
        self.target_servings = original_servings
        self.scale_factor = 1.0
    
    def set_target_servings(self, target_servings: int):
        """Set the target number of servings"""
        if target_servings > 0:
            self.target_servings = target_servings
            self.scale_factor = target_servings / self.original_servings
    
    def scale_ingredient_amount(self, original_amount: float) -> float:
        """Scale an ingredient amount"""
        return original_amount * self.scale_factor
    
    def scale_cooking_time(self, original_minutes: int, time_type: str = 'linear') -> int:
        """Scale cooking time based on serving size"""
        if time_type == 'linear':
            # Most cooking times scale linearly
            return max(1, round(original_minutes * self.scale_factor))
        elif time_type == 'logarithmic':
            # Some cooking times (like baking) scale logarithmically
            import math
            if self.scale_factor > 1:
                return max(1, round(original_minutes * (1 + math.log(self.scale_factor))))
            else:
                return max(1, round(original_minutes * self.scale_factor))
        else:
            # No scaling for fixed times
            return original_minutes
    
    def get_scaling_info(self) -> Dict[str, Any]:
        """Get scaling information"""
        return {
            'original_servings': self.original_servings,
            'target_servings': self.target_servings,
            'scale_factor': round(self.scale_factor, 2),
            'scaling_needed': self.scale_factor != 1.0,
            'scaling_up': self.scale_factor > 1.0,
            'scaling_down': self.scale_factor < 1.0
        }
    
    def format_scaled_amount(self, original_amount: float, unit: str = '') -> str:
        """Format scaled amount with appropriate precision"""
        scaled = self.scale_ingredient_amount(original_amount)
        
        if scaled == int(scaled):
            return f"{int(scaled)} {unit}".strip()
        elif scaled < 1:
            # Convert to fractions for small amounts
            if scaled == 0.5:
                return f"1/2 {unit}".strip()
            elif scaled == 0.25:
                return f"1/4 {unit}".strip()
            elif scaled == 0.75:
                return f"3/4 {unit}".strip()
            elif scaled == 0.33:
                return f"1/3 {unit}".strip()
            elif scaled == 0.67:
                return f"2/3 {unit}".strip()
            else:
                return f"{scaled:.1f} {unit}".strip()
        else:
            return f"{scaled:.1f} {unit}".strip()

class CookingSessionState:
    """Manages the complete state of a cooking session"""
    
    def __init__(self, recipe_data: Dict[str, Any]):
        self.recipe = recipe_data['recipe']
        self.cooking_instructions = recipe_data.get('cooking_instructions')
        
        # Handle case where cooking instructions might be None
        if not self.cooking_instructions:
            # Create a minimal cooking instruction structure
            self.cooking_instructions = {
                'total_steps': 1,
                'estimated_active_time': 30,
                'equipment_needed': [],
                'steps': [{
                    'step_number': 1,
                    'phase': 'cooking',
                    'instruction': 'Follow the recipe instructions to prepare this dish.',
                    'duration_minutes': 30,
                    'timer_needed': False,
                    'temperature': None,
                    'equipment': [],
                    'tips': 'Take your time and taste as you go.',
                    'visual_cues': 'Dish should be cooked through and properly seasoned.',
                    'can_prep_ahead': False
                }]
            }
        
        # Initialize utility classes
        self.timer_manager = TimerManager()
        self.step_navigator = StepNavigator(self.cooking_instructions['total_steps'])
        self.progress_tracker = ProgressTracker(
            self.recipe['name'], 
            self.cooking_instructions['total_steps']
        )
        self.serving_scaler = ServingScaler(self.recipe.get('servings', 4))
        
        # Session state
        self.current_step_data = None
        self.scaled_ingredients = []
        self.equipment_ready = False
        self.prep_completed = False
    
    def get_current_step_data(self) -> Optional[Dict[str, Any]]:
        """Get data for the current step"""
        current_step_num = self.step_navigator.get_current_step()
        steps = self.cooking_instructions.get('steps', [])
        
        for step in steps:
            if step.get('step_number') == current_step_num:
                return step
        
        return None
    
    def get_session_status(self) -> Dict[str, Any]:
        """Get comprehensive session status"""
        current_step = self.get_current_step_data()
        progress = self.step_navigator.get_progress()
        active_timers, expired_timers = self.timer_manager.get_all_active_timers()
        
        return {
            'recipe_name': self.recipe['name'],
            'current_step': current_step,
            'progress': progress,
            'active_timers': active_timers,
            'expired_timers': expired_timers,
            'session_summary': self.progress_tracker.get_session_summary(),
            'scaling_info': self.serving_scaler.get_scaling_info(),
            'equipment_ready': self.equipment_ready,
            'prep_completed': self.prep_completed
        }
    
    def save_session_state(self) -> Dict[str, Any]:
        """Save current session state for pause/resume"""
        return {
            'recipe_id': self.recipe.get('recipe_id'),
            'current_step': self.step_navigator.get_current_step(),
            'completed_steps': list(self.step_navigator.completed_steps),
            'target_servings': self.serving_scaler.target_servings,
            'session_notes': self.progress_tracker.session_notes,
            'modifications': self.progress_tracker.modifications,
            'equipment_ready': self.equipment_ready,
            'prep_completed': self.prep_completed,
            'session_status': self.progress_tracker.session_status
        }
    
    def restore_session_state(self, saved_state: Dict[str, Any]):
        """Restore session from saved state"""
        if saved_state.get('current_step'):
            self.step_navigator.jump_to_step(saved_state['current_step'])
        
        if saved_state.get('completed_steps'):
            self.step_navigator.completed_steps = set(saved_state['completed_steps'])
        
        if saved_state.get('target_servings'):
            self.serving_scaler.set_target_servings(saved_state['target_servings'])
        
        self.equipment_ready = saved_state.get('equipment_ready', False)
        self.prep_completed = saved_state.get('prep_completed', False)
        
        # Restore session notes and modifications
        if saved_state.get('session_notes'):
            self.progress_tracker.session_notes = saved_state['session_notes']
        if saved_state.get('modifications'):
            self.progress_tracker.modifications = saved_state['modifications']