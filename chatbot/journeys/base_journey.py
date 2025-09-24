"""
Base Journey Class
Abstract base class for all customer journeys
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from core.session_manager import SessionManager

class BaseJourney(ABC):
    """Abstract base class for customer journeys"""
    
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        self.journey_name = self.__class__.__name__.replace('Journey', '').lower()
    
    @abstractmethod
    def start_journey(self) -> str:
        """Start the customer journey"""
        pass
    
    @abstractmethod
    def process_input(self, user_input: str) -> Optional[str]:
        """Process user input within the journey"""
        pass
    
    def get_current_step(self) -> int:
        """Get current step number"""
        return self.session_manager.get_current_step() or 1
    
    def update_step(self, step_number: int, step_data: Dict[str, Any] = None) -> None:
        """Update current step"""
        self.session_manager.update_step(step_number, step_data)
    
    def record_decision(self, decision_point: str, user_choice: Any) -> None:
        """Record user decision"""
        self.session_manager.record_decision(decision_point, user_choice)
    
    def get_journey_state(self) -> Dict[str, Any]:
        """Get current journey state"""
        return self.session_manager.get_journey_state()
    
    def complete_journey(self) -> None:
        """Mark journey as complete"""
        self.session_manager.clear_journey()
    
    def format_options(self, options: list, option_type: str = "option") -> str:
        """Format a list of options for display"""
        if not options:
            return ""
        
        formatted = f"\nHere are your {option_type}s:\n"
        for i, option in enumerate(options, 1):
            formatted += f"{i}. {option}\n"
        
        formatted += f"\nPlease enter the number (1-{len(options)}) or type your choice:"
        return formatted
    
    def parse_user_choice(self, user_input: str, options: list) -> Optional[Any]:
        """Parse user choice from input"""
        user_input = user_input.strip()
        
        # Try to parse as number
        try:
            choice_num = int(user_input)
            if 1 <= choice_num <= len(options):
                return options[choice_num - 1]
        except ValueError:
            pass
        
        # Try to match text
        user_input_lower = user_input.lower()
        for option in options:
            if isinstance(option, str) and user_input_lower in option.lower():
                return option
            elif hasattr(option, 'name') and user_input_lower in option.name.lower():
                return option
        
        return None