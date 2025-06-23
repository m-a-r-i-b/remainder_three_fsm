from logging_config import setup_logging, get_logger
from mod_three import ModThreeFSM, ModThreeFSMError
setup_logging()
logger = get_logger(__name__)


def demo_mod_three_fsm():
    """Demonstrate the ModThree FSM with various examples"""
    logger.info("=" * 60)
    logger.info("ModThree FSM Demonstration")
    logger.info("=" * 60)
    
    mod3_fsm = ModThreeFSM()
    
    # Test cases from the assignment
    test_cases = [
        "1101",  # Should be 1 (13 % 3 = 1)
        "1110",  # Should be 2 (14 % 3 = 2) 
        "1111",  # Should be 0 (15 % 3 = 0)
        "110",   # Should be 0 (6 % 3 = 0)
        "1010",  # Should be 1 (10 % 3 = 1)
    ]
    
    additional_cases = [
        "0",      # 0 % 3 = 0
        "1",      # 1 % 3 = 1
        "10",     # 2 % 3 = 2
        "11",     # 3 % 3 = 0
        "100",    # 4 % 3 = 1
        "101",    # 5 % 3 = 2
        "",       # Empty string = 0
    ]
    
    logger.info("Assignment Examples:")
    for binary_str in test_cases:
        remainder = mod3_fsm.get_remainder(binary_str)
        decimal_val = int(binary_str, 2)
        expected = decimal_val % 3
        status = "✓" if remainder == expected else "✗"
        logger.info(f"  {binary_str:>6} (decimal {decimal_val:2d}) → remainder: {remainder} {status}")
    
    logger.info("\nAdditional Test Cases:")
    for binary_str in additional_cases:
        remainder = mod3_fsm.get_remainder(binary_str)
        decimal_val = int(binary_str, 2) if binary_str else 0
        expected = decimal_val % 3
        status = "✓" if remainder == expected else "✗"
        logger.info(f"  {binary_str:>6} (decimal {decimal_val:2d}) → remainder: {remainder} {status}")
    
    # Demonstrate error handling
    logger.info("\nError Handling:")
    try:
        mod3_fsm.get_remainder("102")
    except ModThreeFSMError as e:
        logger.info(f"  Invalid input '102': {e}")
    
    try:
        mod3_fsm.get_remainder("abc")
    except ModThreeFSMError as e:
        logger.info(f"  Invalid input 'abc': {e}")

    try:
        mod3_fsm.get_remainder(12)
    except ModThreeFSMError as e:
        logger.info(f"  Invalid input '12': {e}")

    try:
        mod3_fsm.get_remainder(None)
    except ModThreeFSMError as e:
        logger.info(f"  Invalid input 'None': {e}")
        

def main():
    """Main demonstration function"""
    logger.info("Finite State Machine Implementation Demo")
    logger.info("Modulo 3 computation without integer conversion")
    
    try:
        demo_mod_three_fsm()
        
        logger.info("\n" + "=" * 60)
        logger.info("All demonstrations completed successfully!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Error during demonstration: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())