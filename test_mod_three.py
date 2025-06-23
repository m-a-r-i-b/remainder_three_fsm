import unittest
import sys
from logging_config import setup_logging, get_logger
from mod_three import ModThreeFSM, ModThreeFSMError
from fsm import FSM, FSMError
setup_logging()
logger = get_logger(__name__)

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class ElegantTestResult(unittest.TextTestResult):
    """Custom test result class with elegant formatting"""
    
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.test_count = 0
        self.success_count = 0
        
    def startTest(self, test):
        super().startTest(test)
        self.test_count += 1
        test_name = test._testMethodName.replace('_', ' ').title()
        class_name = test.__class__.__name__
        print(f"{Colors.CYAN}{'─' * 60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}[{self.test_count:02d}] {class_name}: {test_name}{Colors.END}")
        print(f"{Colors.CYAN}{'─' * 60}{Colors.END}")
        
    def addSuccess(self, test):
        super().addSuccess(test)
        self.success_count += 1
        print(f"{Colors.GREEN}✓ PASSED{Colors.END}")
        print()
        
    def addError(self, test, err):
        super().addError(test, err)
        print(f"{Colors.RED}✗ ERROR{Colors.END}")
        self._print_error_details(err)
        print()
        
    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"{Colors.RED}✗ FAILED{Colors.END}")
        self._print_error_details(err)
        print()
        
    def _print_error_details(self, err):
        """Print error details with better formatting"""
        print(f"{Colors.YELLOW}Error Details:{Colors.END}")
        error_lines = str(err[1]).split('\n')
        for line in error_lines:
            if line.strip():
                print(f"  {line}")

class ElegantTestRunner(unittest.TextTestRunner):
    """Custom test runner with elegant formatting"""
    
    def __init__(self, **kwargs):
        kwargs['resultclass'] = ElegantTestResult
        kwargs['verbosity'] = 0  # We handle our own verbosity
        super().__init__(**kwargs)
        
    def run(self, test):
        print(f"\n{Colors.BOLD}{Colors.UNDERLINE}🧪 Running Test Suite{Colors.END}")
        print(f"{Colors.CYAN}{'═' * 80}{Colors.END}")
        
        result = super().run(test)
        
        # Print summary
        print(f"{Colors.CYAN}{'═' * 80}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.UNDERLINE}📊 Test Summary{Colors.END}")
        print(f"{Colors.CYAN}{'═' * 80}{Colors.END}")
        
        total_tests = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)
        successes = total_tests - failures - errors
        
        print(f"{Colors.BOLD}Total Tests:{Colors.END} {total_tests}")
        print(f"{Colors.GREEN}✓ Passed:{Colors.END} {successes}")
        
        if failures > 0:
            print(f"{Colors.RED}✗ Failed:{Colors.END} {failures}")
        if errors > 0:
            print(f"{Colors.RED}⚠ Errors:{Colors.END} {errors}")
            
        # Success rate
        if total_tests > 0:
            success_rate = (successes / total_tests) * 100
            color = Colors.GREEN if success_rate == 100 else Colors.YELLOW if success_rate >= 80 else Colors.RED
            print(f"{Colors.BOLD}Success Rate:{Colors.END} {color}{success_rate:.1f}%{Colors.END}")
        
        print(f"{Colors.CYAN}{'═' * 80}{Colors.END}")
        
        if failures == 0 and errors == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 All tests passed! 🎉{Colors.END}")
        else:
            print(f"{Colors.RED}{Colors.BOLD}❌ Some tests failed. Please review the details above.{Colors.END}")
            
        print()
        return result


class TestFSM(unittest.TestCase):
    """Test the generic FSM implementation"""
    
    def setUp(self):
        # Create a simple FSM for testing
        states = {"S0", "S1"}
        alphabet = {"a", "b"}
        transitions = {
            ("S0", "a"): "S1",
            ("S0", "b"): "S0",
            ("S1", "a"): "S0",
            ("S1", "b"): "S1"
        }
        self.fsm = FSM(states, alphabet, transitions, "S0", {"S0", "S1"})
    
    def test_fsm_basic_functionality(self):
        """Test basic FSM operations"""
        self.assertEqual(self.fsm.process("ab"), "S1")
        self.assertEqual(self.fsm.process("aa"), "S0")
    
    def test_fsm_invalid_symbol(self):
        """Test FSM with invalid symbol in alphabet"""
        with self.assertRaises(FSMError) as context:
            self.fsm.process("ac")
        self.assertIn("Symbol 'c' not in alphabet", str(context.exception))
    
    def test_fsm_invalid_transition(self):
        """Test FSM with invalid transition"""
        # Create FSM with incomplete transition map
        states = {"S0", "S1"}
        alphabet = {"a", "b"}
        transitions = {("S0", "a"): "S1"}  # Missing transitions
        fsm = FSM(states, alphabet, transitions, "S0", {"S0", "S1"})
        
        with self.assertRaises(FSMError) as context:
            fsm.process("ab")
        self.assertIn("No transition defined for state", str(context.exception))
    
    def test_fsm_reset(self):
        """Test FSM reset functionality"""
        self.fsm.process("ab")
        self.assertEqual(self.fsm.current_state, "S1")
        self.fsm.reset()
        self.assertEqual(self.fsm.current_state, "S0")

    def test_fsm_final_state_not_accepted(self):
        """Test FSM rejection when final state is not in accepted final states"""
        # Create FSM where only S0 is a final state
        states = {"S0", "S1", "S2"}
        alphabet = {"a", "b"}
        transitions = {
            ("S0", "a"): "S1",
            ("S0", "b"): "S2",
            ("S1", "a"): "S0",
            ("S1", "b"): "S2",
            ("S2", "a"): "S2",
            ("S2", "b"): "S2"
        }
        # Only S0 is accepting state
        fsm = FSM(states, alphabet, transitions, "S0", {"S0"})
        
        # Input "a" should lead to S1, which is not in final_states
        with self.assertRaises(FSMError) as context:
            fsm.process("a")
        self.assertIn("Input string rejected: final state 'S1' is not in final states", str(context.exception))
        
        # Input "b" should lead to S2, which is not in final_states
        with self.assertRaises(FSMError) as context:
            fsm.process("b")
        self.assertIn("Input string rejected: final state 'S2' is not in final states", str(context.exception))
        
        # Empty string should be accepted (stays in S0)
        self.assertEqual(fsm.process(""), "S0")
        
        # Input "aa" should lead to S0, which is accepted
        self.assertEqual(fsm.process("aa"), "S0")

class TestModThreeFSM(unittest.TestCase):
    """Test the ModThree FSM implementation"""
    
    def setUp(self):
        self.mod3_fsm = ModThreeFSM()
    
    def test_provided_examples(self):
        """Test the examples provided in assignment"""
        self.assertEqual(self.mod3_fsm.get_remainder("1101"), 1)
        self.assertEqual(self.mod3_fsm.get_remainder("1110"), 2)
        self.assertEqual(self.mod3_fsm.get_remainder("1111"), 0)
        self.assertEqual(self.mod3_fsm.get_remainder("110"), 0)
        self.assertEqual(self.mod3_fsm.get_remainder("1010"), 1)
    
    def test_edge_cases(self):
        """Test edge cases"""
        # Single bits
        self.assertEqual(self.mod3_fsm.get_remainder("0"), 0)
        self.assertEqual(self.mod3_fsm.get_remainder("1"), 1)
        
        # Two bits
        self.assertEqual(self.mod3_fsm.get_remainder("00"), 0)
        self.assertEqual(self.mod3_fsm.get_remainder("01"), 1)
        self.assertEqual(self.mod3_fsm.get_remainder("10"), 2)
        self.assertEqual(self.mod3_fsm.get_remainder("11"), 0)
        
        # Longer strings
        self.assertEqual(self.mod3_fsm.get_remainder("101010"), 0)  # 42 % 3 = 0
        self.assertEqual(self.mod3_fsm.get_remainder("111111"), 0)
        self.assertEqual(self.mod3_fsm.get_remainder("000000"), 0)
    
    def test_invalid_input(self):
        """Test invalid input handling"""
        with self.assertRaises(ModThreeFSMError):
            self.mod3_fsm.get_remainder("102")  # Invalid character
        
        with self.assertRaises(ModThreeFSMError):
            self.mod3_fsm.get_remainder("abc")  # Invalid characters
    
    def test_empty_string(self):
        """Test empty string input"""
        # Empty string should return 0 (S0 state)
        self.assertEqual(self.mod3_fsm.get_remainder(""), 0)
    
    def test_mathematical_correctness(self):
        """Test mathematical correctness by comparing with actual modulo"""
        test_cases = [
            "0", "1", "10", "11", "100", "101", "110", "111",
            "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111",
            "10101010", "11111111", "10000000", "11001100"
        ]
        
        for binary_str in test_cases:
            expected = int(binary_str, 2) % 3
            actual = self.mod3_fsm.get_remainder(binary_str)
            self.assertEqual(actual, expected, 
                           f"Failed for {binary_str}: expected {expected}, got {actual}")


if __name__ == "__main__":
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    # Run with elegant formatter
    runner = ElegantTestRunner()
    runner.run(suite)