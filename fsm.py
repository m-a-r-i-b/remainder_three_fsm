from typing import Dict, Tuple, Set
from logging_config import get_logger

logger = get_logger(__name__)

class FSMError(Exception):
    """Custom exception for FSM-related errors"""
    pass

class FSM:
    """
    A generic Finite State Machine implementation.
    
    This class implements a deterministic finite automaton that can process
    input strings symbol by symbol and transition between states according
    to a predefined transition map.
    
    Attributes:
        states (Set[str]): Set of all possible states
        alphabet (Set[str]): Set of all valid input symbols
        transition_map (Dict[Tuple[str, str], str]): Mapping from (state, symbol) to next state
        initial_state (str): The starting state
        final_states (Set[str]): Set of accepting/final states
        current_state (str): Current state of the machine
    """
    
    def __init__(self, 
                 states: Set[str],
                 alphabet: Set[str],
                 transition_map: Dict[Tuple[str, str], str],
                 initial_state: str,
                 final_states: Set[str]) -> None:
        """
        Initialize the FSM with the given parameters.
        
        Args:
            states: Set of all possible states
            alphabet: Set of all valid input symbols
            transition_map: Dict mapping (state, symbol) tuples to next states
            initial_state: The starting state
            final_states: Set of accepting/final states
            
        Raises:
            FSMError: If the FSM configuration is invalid
        """
        self._validate_fsm_configuration(states, alphabet, transition_map, 
                                       initial_state, final_states)
        
        self.states = states.copy()
        self.alphabet = alphabet.copy()
        self.transition_map = transition_map.copy()
        self.initial_state = initial_state
        self.final_states = final_states.copy()
        self.current_state = initial_state
        
        logger.info(f"FSM initialized with {len(states)} states and {len(alphabet)} symbols")

    def _validate_fsm_configuration(self, 
                                  states: Set[str],
                                  alphabet: Set[str],
                                  transition_map: Dict[Tuple[str, str], str],
                                  initial_state: str,
                                  final_states: Set[str]) -> None:
        """
        Validate the FSM configuration for consistency.
        
        Args:
            states: Set of all possible states
            alphabet: Set of all valid input symbols
            transition_map: Dict mapping (state, symbol) tuples to next states
            initial_state: The starting state
            final_states: Set of accepting/final states
            
        Raises:
            FSMError: If the configuration is invalid
        """
        if not states:
            raise FSMError("States set cannot be empty")
        if not alphabet:
            raise FSMError("Alphabet set cannot be empty")
        if initial_state not in states:
            raise FSMError(f"Initial state '{initial_state}' not in states set")
        if not final_states.issubset(states):
            raise FSMError("Final states must be a subset of states")
        
        # Validate transition map
        for (state, symbol), next_state in transition_map.items():
            if state not in states:
                raise FSMError(f"State '{state}' in transition map not in states set")
            if symbol not in alphabet:
                raise FSMError(f"Symbol '{symbol}' in transition map not in alphabet")
            if next_state not in states:
                raise FSMError(f"Next state '{next_state}' in transition map not in states set")

    def reset(self) -> None:
        """
        Reset the FSM to its initial state.
        
        This method can be called to restart the FSM processing from the beginning.
        """
        self.current_state = self.initial_state
        logger.debug(f"FSM reset to initial state: {self.initial_state}")

    def transition(self, symbol: str) -> None:
        """
        Perform a single state transition based on the input symbol.
        
        Args:
            symbol: The input symbol to process
            
        Raises:
            FSMError: If the symbol is not in the alphabet or no transition exists
        """
        if symbol not in self.alphabet:
            raise FSMError(f"Symbol '{symbol}' not in alphabet {self.alphabet}")
        
        transition_key = (self.current_state, symbol)
        if transition_key not in self.transition_map:
            raise FSMError(f"No transition defined for state '{self.current_state}' with input '{symbol}'")
        
        previous_state = self.current_state
        self.current_state = self.transition_map[transition_key]
        logger.debug(f"Transition: {previous_state} --{symbol}--> {self.current_state}")

    def process(self, input_string: str) -> str:
        """
        Process an entire input string and return the final state.
        
        Args:
            input_string: The string of symbols to process
            
        Returns:
            The final state after processing all symbols
            
        Raises:
            FSMError: If any symbol is invalid, transition is undefined, or final state is not accepting
        """
        self.reset()
        
        if not input_string:
            logger.debug("Empty input string, returning initial state")
            if self.current_state not in self.final_states:
                raise FSMError(f"Input string rejected: final state '{self.current_state}' is not in final states {self.final_states}")
            return self.current_state
        
        logger.debug(f"Processing input string: '{input_string}'")
        
        for i, symbol in enumerate(input_string):
            try:
                self.transition(symbol)
            except FSMError as e:
                raise FSMError(f"Error at position {i} while processing '{symbol}': {e}")
        
        logger.debug(f"Processing complete. Final state: {self.current_state}")
        
        if self.current_state not in self.final_states:
            raise FSMError(f"Input string rejected: final state '{self.current_state}' is not in final states {self.final_states}")
        
        return self.current_state

    def get_current_state(self) -> str:
        """
        Get the current state of the FSM.
        
        Returns:
            The current state
        """
        return self.current_state

    def __str__(self) -> str:
        """String representation of the FSM"""
        return (f"FSM(states={len(self.states)}, alphabet={self.alphabet}, "
                f"current_state={self.current_state})")

