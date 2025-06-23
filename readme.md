# Modulo 3 Finite State Machine (FSM) Implementation

A production-ready implementation of a generic Finite State Machine and its specialized application for computing binary number modulo 3 without integer conversion.

## Overview

This project implements a **generic FSM class** following formal automaton theory and a **specialized ModThree FSM** that computes the remainder when a binary number is divided by 3. The solution demonstrates object-oriented design principles, comprehensive error handling, and extensive test coverage.

## Mathematical Foundation

The implementation is based on the formal definition of a finite automaton as a 5-tuple **(Q, Σ, q₀, F, δ)**:

- **Q**: Finite set of states `{S0, S1, S2}`
- **Σ**: Input alphabet `{0, 1}`  
- **q₀**: Initial state `S0`
- **F**: Set of final states `{S0, S1, S2}` (all states are accepting)
- **δ**: transition map based on modular arithmetic

### State Transitions for Mod-3

| Current State | Input '0' | Input '1' | Remainder |
|---------------|-----------|-----------|-----------|
| S0            | S0        | S1        | 0         |
| S1            | S2        | S0        | 1         |
| S2            | S1        | S2        | 2         |

The transitions are mathematically derived from the property that for each bit position, the contribution to the remainder follows the pattern of powers of 2 modulo 3.

## Project Structure

```
remainder_three_fsm/
├── logging_config.py   # Logging config
├── fsm.py              # Generic FSM implementation
├── mod_three.py        # Specialized ModThree FSM
├── example_usage.py    # Example usage
├── test_mod_three.py   # Comprehensive test suite
└── readme.md           # This documentation
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Quick Start

1. **Clone or download the project files**
   ```bash
   git clone <repository-url>
   cd remainder_three_fsm
   ```

2. **Run the tests to verify if everything is working as expected**
   ```bash
   python test_mod_three.py
   ```

3. **Example usage:**
   ```bash
   python example_usage.py
   ```

## Usage Examples

### Basic ModThree Usage

```python
from mod_three import ModThreeFSM

# Create a ModThree FSM instance
mod3_fsm = ModThreeFSM()

# Compute remainders for binary strings
print(mod3_fsm.get_remainder("1101"))  # Output: 1 (13 % 3 = 1)
print(mod3_fsm.get_remainder("1110"))  # Output: 2 (14 % 3 = 2)
print(mod3_fsm.get_remainder("1111"))  # Output: 0 (15 % 3 = 0)
```

### Generic FSM Usage

```python
from fsm import FSM

# Create a simple FSM that recognizes strings ending with "01"
states = {"START", "ZERO", "ACCEPT"}
alphabet = {"0", "1"}
transitions = {
    ("START", "0"): "ZERO",
    ("START", "1"): "START",
    ("ZERO", "0"): "ZERO", 
    ("ZERO", "1"): "ACCEPT",
    ("ACCEPT", "0"): "ZERO",
    ("ACCEPT", "1"): "START"
}

fsm = FSM(states, alphabet, transitions, "START", {"ACCEPT"})
final_state = fsm.process("10101")
```

### Error Handling Examples

```python
from mod_three import ModThreeFSM, ModThreeFSMError

mod3_fsm = ModThreeFSM()

try:
    # This will raise an exception due to invalid character
    mod3_fsm.get_remainder("102")
except ModThreeFSMError as e:
    print(f"Error: {e}")
```

## API Reference

### FSM Class

#### Constructor
```python
FSM(states, alphabet, transition_map, initial_state, final_states)
```
- **states**: Set of state names
- **alphabet**: Set of valid input symbols
- **transition_map**: Dict mapping (state, symbol) to next state
- **initial_state**: Starting state name
- **final_states**: Set of accepting state names

#### Methods
- `process(input_string)`: Process input and return final state
- `transition(symbol)`: Perform single state transition
- `reset()`: Reset to initial state
- `get_current_state()`: Get current state

### ModThreeFSM Class

#### Constructor
```python
ModThreeFSM()
```
No parameters required - automatically configured for mod-3 computation.

#### Methods
- `get_remainder(binary_string)`: Compute remainder (returns 0, 1, or 2)
- `get_current_state()`: Get current FSM state
- `reset()`: Reset FSM to initial state

## Testing

The project includes comprehensive tests covering:

- **Functional Testing**: Example test cases
- **Edge Case Testing**: Empty strings, single characters, long inputs
- **Error Testing**: Invalid inputs, malformed FSM configurations
- **Mathematical Verification**: Comparison with built-in modulo operation
- **Integration Testing**: FSM and ModThree interaction

### Running Tests

```bash
# Run all tests with verbose output
python test_mod_three.py

# Run specific test class
python -m unittest test_mod_three.TestModThreeFSM -v

# Run with coverage (if coverage.py is installed)
python -m coverage run test_mod_three.py
python -m coverage report
```

## Contributing

This implementation follows Python best practices:
- PEP 8 style guidelines
- Type hints throughout
- Comprehensive docstrings
- Unit test coverage
- Error handling with custom exceptions

## License

This project is implemented for educational purposes as part of a technical assignment.
