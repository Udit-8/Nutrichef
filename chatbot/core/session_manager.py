"""
Session Management for Nutrition Chatbot
Handles user session state, context, and conversation flow
"""

from typing import Dict, Any, Optional
from datetime import datetime

class SessionManager:
    """Manages user session state throughout the conversation"""
    
    def __init__(self):
        self.session_data = {
            'session_id': self._generate_session_id(),
            'current_journey': None,
            'current_step': None,
            'user_context': {},
            'conversation_history': [],
            'journey_state': {},
            'user_preferences': self._load_default_preferences(),
            'created_at': datetime.now().isoformat()
        }
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return f"session_{int(datetime.now().timestamp())}"
    
    def _load_default_preferences(self) -> Dict[str, Any]:
        """Load default user preferences"""
        return {
            'dietary_restrictions': [],
            'allergies': [],
            'cuisine_preferences': [],
            'skill_level': 'beginner',
            'cooking_time_preference': 'medium',
            'serving_size': 4
        }
    
    def start_journey(self, journey_name: str) -> None:
        """Start a new customer journey"""
        self.session_data['current_journey'] = journey_name
        self.session_data['current_step'] = 1
        self.session_data['journey_state'] = {
            'journey_name': journey_name,
            'step_data': {},
            'decision_points': {},
            'user_inputs': []
        }
    
    def update_step(self, step_number: int, step_data: Dict[str, Any] = None) -> None:
        """Update current step and its data"""
        self.session_data['current_step'] = step_number
        if step_data:
            self.session_data['journey_state']['step_data'][step_number] = step_data
    
    def record_decision(self, decision_point: str, user_choice: Any) -> None:
        """Record user decision at a decision point"""
        self.session_data['journey_state']['decision_points'][decision_point] = {
            'choice': user_choice,
            'timestamp': datetime.now().isoformat()
        }
    
    def add_message(self, sender: str, message: str) -> None:
        """Add message to conversation history"""
        self.session_data['conversation_history'].append({
            'sender': sender,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_current_journey(self) -> Optional[str]:
        """Get current active journey"""
        return self.session_data.get('current_journey')
    
    def get_current_step(self) -> Optional[int]:
        """Get current step number"""
        return self.session_data.get('current_step')
    
    def get_journey_state(self) -> Dict[str, Any]:
        """Get current journey state"""
        return self.session_data.get('journey_state', {})
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """Get user preferences"""
        return self.session_data.get('user_preferences', {})
    
    def update_user_preferences(self, preferences: Dict[str, Any]) -> None:
        """Update user preferences"""
        self.session_data['user_preferences'].update(preferences)
    
    def update_context(self, key: str, value: Any) -> None:
        """Update user context with a key-value pair"""
        self.session_data['user_context'][key] = value
    
    def get_context(self, key: str) -> Any:
        """Get value from user context"""
        return self.session_data['user_context'].get(key)
    
    def clear_journey(self) -> None:
        """Clear current journey state"""
        self.session_data['current_journey'] = None
        self.session_data['current_step'] = None
        self.session_data['journey_state'] = {}
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in session storage"""
        self.session_data['user_context'][key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from session storage"""
        return self.session_data['user_context'].get(key, default)
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of current session"""
        return {
            'session_id': self.session_data['session_id'],
            'current_journey': self.session_data['current_journey'],
            'current_step': self.session_data['current_step'],
            'total_messages': len(self.session_data['conversation_history']),
            'created_at': self.session_data['created_at']
        }