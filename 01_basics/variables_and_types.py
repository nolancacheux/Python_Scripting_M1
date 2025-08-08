"""
Variables and Data Types Examples
=================================

This module demonstrates fundamental Python data types, variables, and constants.
Includes examples of type conversion, type checking, and best practices.

Author: Python Learning Examples
Date: 2025
"""

# Constants (by convention, use UPPERCASE)
PI = 3.14159
MAX_RETRIES = 3
DEFAULT_NAME = "Unknown User"


def demonstrate_basic_types():
    """Demonstrate Python's basic data types."""
    print("=== Basic Data Types ===")
    
    # Integer
    age = 25
    print(f"Integer: {age} (type: {type(age).__name__})")
    
    # Float
    height = 5.9
    print(f"Float: {height} (type: {type(height).__name__})")
    
    # String
    name = "Alice"
    print(f"String: '{name}' (type: {type(name).__name__})")
    
    # Boolean
    is_student = True
    print(f"Boolean: {is_student} (type: {type(is_student).__name__})")
    
    # NoneType
    nothing = None
    print(f"None: {nothing} (type: {type(nothing).__name__})")


def demonstrate_collections():
    """Demonstrate collection data types."""
    print("\n=== Collection Types ===")
    
    # List (mutable, ordered)
    fruits = ["apple", "banana", "cherry"]
    print(f"List: {fruits} (type: {type(fruits).__name__})")
    
    # Tuple (immutable, ordered)
    coordinates = (10, 20)
    print(f"Tuple: {coordinates} (type: {type(coordinates).__name__})")
    
    # Dictionary (mutable, key-value pairs)
    person = {"name": "Bob", "age": 30, "city": "New York"}
    print(f"Dictionary: {person} (type: {type(person).__name__})")
    
    # Set (mutable, unique values)
    unique_numbers = {1, 2, 3, 3, 4}  # Duplicates are removed
    print(f"Set: {unique_numbers} (type: {type(unique_numbers).__name__})")


def demonstrate_type_conversion():
    """Demonstrate type conversion (casting)."""
    print("\n=== Type Conversion ===")
    
    # String to number
    str_number = "42"
    int_number = int(str_number)
    float_number = float(str_number)
    print(f"'{str_number}' -> int: {int_number}, float: {float_number}")
    
    # Number to string
    number = 123
    str_from_int = str(number)
    print(f"{number} -> string: '{str_from_int}'")
    
    # Boolean conversions
    print(f"bool('') = {bool('')}")  # Empty string is False
    print(f"bool('hello') = {bool('hello')}")  # Non-empty string is True
    print(f"bool(0) = {bool(0)}")  # Zero is False
    print(f"bool(1) = {bool(1)}")  # Non-zero is True


def demonstrate_type_checking():
    """Demonstrate type checking techniques."""
    print("\n=== Type Checking ===")
    
    value = 42
    
    # Using type() function
    print(f"type({value}) == int: {type(value) == int}")
    
    # Using isinstance() (preferred method)
    print(f"isinstance({value}, int): {isinstance(value, int)}")
    print(f"isinstance({value}, (int, float)): {isinstance(value, (int, float))}")
    
    # Check for numeric types
    def is_numeric(val):
        """Check if a value is numeric."""
        return isinstance(val, (int, float, complex))
    
    print(f"is_numeric(42): {is_numeric(42)}")
    print(f"is_numeric('42'): {is_numeric('42')}")


def demonstrate_variable_scope():
    """Demonstrate variable scope and naming conventions."""
    print("\n=== Variable Scope and Naming ===")
    
    # Global variable
    global_var = "I'm global"
    
    def inner_function():
        # Local variable
        local_var = "I'm local"
        print(f"Inside function: {global_var}")
        print(f"Inside function: {local_var}")
        
        # Modifying global variable
        global global_var
        global_var = "Modified global"
    
    print(f"Before function call: {global_var}")
    inner_function()
    print(f"After function call: {global_var}")
    
    # Naming conventions
    snake_case_variable = "Python convention"
    CONSTANT_VALUE = "Never changes"
    _private_variable = "Internal use"
    __very_private = "Name mangling"
    
    print(f"\nNaming examples:")
    print(f"snake_case_variable: {snake_case_variable}")
    print(f"CONSTANT_VALUE: {CONSTANT_VALUE}")


def demonstrate_string_operations():
    """Demonstrate string operations and formatting."""
    print("\n=== String Operations ===")
    
    text = "  Hello, Python World!  "
    
    # String methods
    print(f"Original: '{text}'")
    print(f"Stripped: '{text.strip()}'")
    print(f"Upper: '{text.upper()}'")
    print(f"Lower: '{text.lower()}'")
    print(f"Replace: '{text.replace('Python', 'Amazing')}'")
    
    # String formatting
    name = "Alice"
    age = 25
    
    # f-strings (Python 3.6+)
    print(f"\nf-string: Hello, {name}! You are {age} years old.")
    
    # format() method
    print("format(): Hello, {}! You are {} years old.".format(name, age))
    
    # % formatting (older style)
    print("% formatting: Hello, %s! You are %d years old." % (name, age))


def demonstrate_input_output():
    """Demonstrate basic input/output operations."""
    print("\n=== Input/Output Examples ===")
    
    # Note: input() is commented out for automatic execution
    # Uncomment when running interactively
    
    # name = input("Enter your name: ")
    # age = input("Enter your age: ")
    
    # Simulate user input for demonstration
    name = "Demo User"
    age = "25"
    
    try:
        age_int = int(age)
        print(f"Hello, {name}! Next year you'll be {age_int + 1}.")
    except ValueError:
        print("Please enter a valid age (number).")


def main():
    """Main function to run all demonstrations."""
    print("Python Variables and Data Types Examples")
    print("=" * 50)
    
    demonstrate_basic_types()
    demonstrate_collections()
    demonstrate_type_conversion()
    demonstrate_type_checking()
    demonstrate_variable_scope()
    demonstrate_string_operations()
    demonstrate_input_output()
    
    print("\n" + "=" * 50)
    print("Examples completed successfully!")


if __name__ == "__main__":
    # This code only runs when the script is executed directly
    main()


# Usage Examples:
"""
To run this script:
    python variables_and_types.py

Key concepts covered:
1. Basic data types: int, float, str, bool, None
2. Collection types: list, tuple, dict, set
3. Type conversion and checking
4. Variable scope and naming conventions
5. String operations and formatting
6. Input/output basics

Best practices demonstrated:
- Use descriptive variable names
- Follow Python naming conventions
- Use isinstance() for type checking
- Use f-strings for string formatting
- Include proper error handling
- Document your code with docstrings
"""