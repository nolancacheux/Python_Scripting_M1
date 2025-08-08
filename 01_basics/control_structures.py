"""
Control Structures Examples
===========================

This module demonstrates Python's control structures including conditionals,
loops, functions, and exception handling. Includes practical examples and
best practices for flow control.

Author: Python Learning Examples
Date: 2025
"""

import random
import time


def demonstrate_conditionals():
    """Demonstrate if/elif/else statements."""
    print("=== Conditional Statements ===")
    
    # Simple if statement
    age = 18
    if age >= 18:
        print(f"Age {age}: You are an adult.")
    
    # if/else statement
    temperature = 75
    if temperature > 80:
        print(f"{temperature}°F: It's hot outside!")
    else:
        print(f"{temperature}°F: It's not too hot.")
    
    # if/elif/else chain
    score = 85
    if score >= 90:
        grade = 'A'
    elif score >= 80:
        grade = 'B'
    elif score >= 70:
        grade = 'C'
    elif score >= 60:
        grade = 'D'
    else:
        grade = 'F'
    
    print(f"Score {score}: Grade {grade}")
    
    # Ternary operator (conditional expression)
    status = "pass" if score >= 60 else "fail"
    print(f"Status: {status}")


def demonstrate_logical_operators():
    """Demonstrate logical operators in conditions."""
    print("\n=== Logical Operators ===")
    
    age = 25
    has_license = True
    has_car = False
    
    # AND operator
    if age >= 16 and has_license:
        print("Can drive (has age and license)")
    
    # OR operator
    if has_car or age >= 25:
        print("Can rent a car (has car or is 25+)")
    
    # NOT operator
    if not has_car:
        print("Needs to buy a car")
    
    # Complex conditions
    if (age >= 21 and has_license) or (age >= 25):
        print("Eligible for car rental")


def demonstrate_for_loops():
    """Demonstrate various for loop patterns."""
    print("\n=== For Loops ===")
    
    # Loop through a list
    fruits = ["apple", "banana", "cherry"]
    print("Fruits:")
    for fruit in fruits:
        print(f"  - {fruit}")
    
    # Loop with index using enumerate
    print("\nFruits with index:")
    for index, fruit in enumerate(fruits):
        print(f"  {index}: {fruit}")
    
    # Loop through range
    print("\nNumbers 1-5:")
    for i in range(1, 6):
        print(f"  {i}")
    
    # Loop through dictionary
    person = {"name": "Alice", "age": 30, "city": "New York"}
    print("\nPerson details:")
    for key, value in person.items():
        print(f"  {key}: {value}")
    
    # List comprehension (advanced for loop)
    squares = [x**2 for x in range(1, 6)]
    print(f"\nSquares: {squares}")
    
    # Conditional list comprehension
    even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
    print(f"Even squares: {even_squares}")


def demonstrate_while_loops():
    """Demonstrate while loops and loop control."""
    print("\n=== While Loops ===")
    
    # Basic while loop
    count = 0
    print("Counting to 3:")
    while count < 3:
        count += 1
        print(f"  Count: {count}")
    
    # While loop with break
    print("\nLoop with break:")
    number = 1
    while True:
        if number > 3:
            break
        print(f"  Number: {number}")
        number += 1
    
    # While loop with continue
    print("\nLoop with continue (skip 2):")
    i = 0
    while i < 5:
        i += 1
        if i == 2:
            continue
        print(f"  i: {i}")


def demonstrate_nested_loops():
    """Demonstrate nested loops and patterns."""
    print("\n=== Nested Loops ===")
    
    # Simple multiplication table
    print("3x3 Multiplication table:")
    for i in range(1, 4):
        for j in range(1, 4):
            print(f"{i*j:2d}", end=" ")
        print()  # New line after each row
    
    # Pattern printing
    print("\nTriangle pattern:")
    for i in range(1, 5):
        for j in range(i):
            print("*", end="")
        print()


def basic_function_examples():
    """Demonstrate basic function definitions and calls."""
    print("\n=== Basic Functions ===")
    
    # Simple function
    def greet():
        """A simple greeting function."""
        return "Hello, World!"
    
    print(greet())
    
    # Function with parameters
    def greet_person(name, greeting="Hello"):
        """Greet a person with a custom greeting."""
        return f"{greeting}, {name}!"
    
    print(greet_person("Alice"))
    print(greet_person("Bob", "Hi"))
    
    # Function with multiple returns
    def get_name_age():
        """Return multiple values."""
        return "Charlie", 28
    
    name, age = get_name_age()
    print(f"Name: {name}, Age: {age}")


def advanced_function_examples():
    """Demonstrate advanced function features."""
    print("\n=== Advanced Functions ===")
    
    # Function with *args (variable positional arguments)
    def sum_all(*numbers):
        """Sum any number of arguments."""
        return sum(numbers)
    
    print(f"Sum of 1,2,3: {sum_all(1, 2, 3)}")
    print(f"Sum of 1,2,3,4,5: {sum_all(1, 2, 3, 4, 5)}")
    
    # Function with **kwargs (variable keyword arguments)
    def create_profile(**info):
        """Create a profile from keyword arguments."""
        profile = []
        for key, value in info.items():
            profile.append(f"{key}: {value}")
        return ", ".join(profile)
    
    print(create_profile(name="Dave", age=25, city="Boston"))
    
    # Lambda functions (anonymous functions)
    square = lambda x: x**2
    print(f"Square of 5: {square(5)}")
    
    # Using lambda with built-in functions
    numbers = [1, 2, 3, 4, 5]
    squared_numbers = list(map(lambda x: x**2, numbers))
    print(f"Squared numbers: {squared_numbers}")


def demonstrate_exception_handling():
    """Demonstrate exception handling with try/except."""
    print("\n=== Exception Handling ===")
    
    # Basic try/except
    try:
        result = 10 / 0
    except ZeroDivisionError:
        print("Cannot divide by zero!")
    
    # Multiple exception types
    def safe_divide(a, b):
        """Safely divide two numbers."""
        try:
            result = float(a) / float(b)
            return f"{a} / {b} = {result}"
        except ZeroDivisionError:
            return "Error: Cannot divide by zero"
        except ValueError:
            return "Error: Invalid number format"
        except Exception as e:
            return f"Unexpected error: {e}"
    
    print(safe_divide(10, 2))
    print(safe_divide(10, 0))
    print(safe_divide("abc", 2))
    
    # try/except/else/finally
    def process_file(filename):
        """Demonstrate complete exception handling."""
        try:
            # Simulate file processing
            if filename == "good_file.txt":
                data = "File contents here"
            else:
                raise FileNotFoundError("File not found")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None
        else:
            # Runs only if no exception occurred
            print("File processed successfully")
            return data
        finally:
            # Always runs, regardless of exceptions
            print("Cleaning up resources")
    
    process_file("good_file.txt")
    process_file("bad_file.txt")


def practical_examples():
    """Demonstrate practical applications of control structures."""
    print("\n=== Practical Examples ===")
    
    # Number guessing game logic
    def number_guessing_game_logic():
        """Simulate number guessing game logic."""
        secret_number = random.randint(1, 10)
        max_attempts = 3
        
        print(f"Number Guessing Game (1-10, {max_attempts} attempts)")
        
        for attempt in range(1, max_attempts + 1):
            # Simulate user guess
            guess = random.randint(1, 10)
            print(f"Attempt {attempt}: Guessing {guess}")
            
            if guess == secret_number:
                print("Congratulations! You guessed it!")
                break
            elif guess < secret_number:
                print("Too low!")
            else:
                print("Too high!")
        else:
            # This runs if the loop completes without breaking
            print(f"Game over! The number was {secret_number}")
    
    number_guessing_game_logic()
    
    # Grade calculator
    def calculate_grade(scores):
        """Calculate letter grade from numeric scores."""
        if not scores:
            return "No scores provided"
        
        average = sum(scores) / len(scores)
        
        if average >= 90:
            return f"A ({average:.1f}%)"
        elif average >= 80:
            return f"B ({average:.1f}%)"
        elif average >= 70:
            return f"C ({average:.1f}%)"
        elif average >= 60:
            return f"D ({average:.1f}%)"
        else:
            return f"F ({average:.1f}%)"
    
    test_scores = [85, 92, 78, 88, 95]
    print(f"\nGrade for scores {test_scores}: {calculate_grade(test_scores)}")
    
    # Password validator
    def validate_password(password):
        """Validate password strength."""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        if not (has_upper and has_lower and has_digit):
            return False, "Password must contain uppercase, lowercase, and digits"
        
        return True, "Password is strong"
    
    passwords = ["weak", "StrongPass123", "nodigits"]
    for pwd in passwords:
        is_valid, message = validate_password(pwd)
        print(f"'{pwd}': {message}")


def main():
    """Main function to run all demonstrations."""
    print("Python Control Structures Examples")
    print("=" * 50)
    
    demonstrate_conditionals()
    demonstrate_logical_operators()
    demonstrate_for_loops()
    demonstrate_while_loops()
    demonstrate_nested_loops()
    basic_function_examples()
    advanced_function_examples()
    demonstrate_exception_handling()
    practical_examples()
    
    print("\n" + "=" * 50)
    print("All examples completed successfully!")


if __name__ == "__main__":
    main()


# Usage Examples:
"""
To run this script:
    python control_structures.py

Key concepts covered:
1. Conditional statements (if/elif/else)
2. Logical operators (and, or, not)
3. For loops with various patterns
4. While loops and loop control
5. Nested loops and patterns
6. Function definitions and calls
7. Advanced function features (*args, **kwargs)
8. Exception handling (try/except/else/finally)
9. Practical applications

Best practices demonstrated:
- Use descriptive function names
- Include docstrings for functions
- Handle exceptions appropriately
- Use enumerate() for indexed loops
- Use list comprehensions when appropriate
- Break complex conditions into readable parts
- Always include proper error handling
"""