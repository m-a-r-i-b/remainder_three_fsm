from fsm import FSM, FSMError
from logging_config import get_logger

logger = get_logger(__name__)

class ModThreeFSMError(Exception):
    """Custom exception for ModThree FSM-related errors"""
    pass

class ModThreeFSM:
    """
    A specialized FSM for computing modulo 3 of binary numbers.
    
    This class uses a finite state machine to compute the remainder when
    a binary number (represented as a string) is divided by 3, without
    converting to integer arithmetic.
    
    The FSM has three states representing remainders 0, 1, and 2.
    State transitions are designed based on the mathematical property
    that each bit position contributes to the remainder based on powers of 2 mod 3.
    
    Attributes:
        _fsm (FSM): The underlying generic FSM
        _state_to_remainder (Dict[str, int]): Mapping from FSM states to remainder values
    """
    
    def __init__(self) -> None:
        """
        Initialize the ModThree FSM with appropriate states and transitions.
        
        The FSM is configured with:
        - States: S0, S1, S2 (representing remainders 0, 1, 2)
        - Alphabet: 0, 1 (binary digits)
        - Transitions based on modular arithmetic properties
        """
        # Define the FSM components according to the assignment specification
        states = {"S0", "S1", "S2"}
        alphabet = {"0", "1"}
        
        # transition map based on modulo 3 arithmetic
        # δ(S0,0) = S0; δ(S0,1) = S1; δ(S1,0) = S2; δ(S1,1) = S0; δ(S2,0) = S1; δ(S2,1) = S2
        transitions = {
            ("S0", "0"): "S0",  # 0*2 + 0 = 0 mod 3
            ("S0", "1"): "S1",  # 0*2 + 1 = 1 mod 3
            ("S1", "0"): "S2",  # 1*2 + 0 = 2 mod 3
            ("S1", "1"): "S0",  # 1*2 + 1 = 3 = 0 mod 3
            ("S2", "0"): "S1",  # 2*2 + 0 = 4 = 1 mod 3
            ("S2", "1"): "S2"   # 2*2 + 1 = 5 = 2 mod 3
        }
        
        initial_state = "S0"
        final_states = {"S0", "S1", "S2"}  # All states are accepting
        
        try:
            self._fsm = FSM(states, alphabet, transitions, initial_state, final_states)
        except FSMError as e:
            raise ModThreeFSMError(f"Failed to initialize ModThree FSM: {e}")
        
        # Mapping from final states to remainder values
        self._state_to_remainder = {
            "S0": 0,
            "S1": 1, 
            "S2": 2
        }
        
        logger.info("ModThree FSM initialized successfully")

    def get_remainder(self, binary_string: str) -> int:
        """
        Compute the remainder when the binary number is divided by 3.
        
        Args:
            binary_string: A string of binary digits (0s and 1s)
            
        Returns:
            The remainder (0, 1, or 2) when the binary number is divided by 3
            
        Raises:
            ModThreeFSMError: If the input is invalid or FSM processing fails
        """
        if not isinstance(binary_string, str):
            raise ModThreeFSMError(f"Input must be a string, got {type(binary_string)}")
        
        # Handle empty string - represents 0
        if not binary_string:
            logger.debug("Empty binary string, returning remainder 0")
            return 0
        
        # Validate that string contains only binary digits
        if not all(c in '01' for c in binary_string):
            invalid_chars = set(binary_string) - {'0', '1'}
            raise ModThreeFSMError(f"Binary string contains invalid characters: {invalid_chars}")
        
        logger.debug(f"Computing remainder for binary string: '{binary_string}'")
        
        try:
            final_state = self._fsm.process(binary_string)
            remainder = self._state_to_remainder[final_state]
            
            logger.debug(f"Final state: {final_state}, Remainder: {remainder}")
            return remainder
            
        except FSMError as e:
            raise ModThreeFSMError(f"FSM processing failed: {e}")
    
    def get_current_state(self) -> str:
        """
        Get the current state of the underlying FSM.
        
        Returns:
            The current state name
        """
        return self._fsm.get_current_state()
    
    def reset(self) -> None:
        """
        Reset the FSM to its initial state.
        """
        self._fsm.reset()
        logger.debug("ModThree FSM reset to initial state")
    
    def __str__(self) -> str:
        """String representation of the ModThree FSM"""
        return f"ModThreeFSM(current_state={self.get_current_state()})"
   