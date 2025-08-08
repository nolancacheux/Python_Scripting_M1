"""
List, Dictionary, and Set Operations Examples
=============================================

This module demonstrates comprehensive operations with Python's collection types:
lists, dictionaries, sets, and tuples. Includes practical examples for data
manipulation, searching, and transformation.

Author: Python Learning Examples
Date: 2025
"""

import copy
from collections import defaultdict, Counter
from operator import itemgetter


def demonstrate_list_basics():
    """Demonstrate fundamental list operations."""
    print("=== List Basics ===")
    
    # Creating lists
    empty_list = []
    numbers = [1, 2, 3, 4, 5]
    mixed = [1, "hello", 3.14, True]
    nested = [[1, 2], [3, 4], [5, 6]]
    
    print(f"Empty list: {empty_list}")
    print(f"Numbers: {numbers}")
    print(f"Mixed types: {mixed}")
    print(f"Nested lists: {nested}")
    
    # List properties
    print(f"Length of numbers: {len(numbers)}")
    print(f"Type: {type(numbers)}")
    
    # Accessing elements
    print(f"First element: {numbers[0]}")
    print(f"Last element: {numbers[-1]}")
    print(f"Second to fourth: {numbers[1:4]}")
    print(f"Every second element: {numbers[::2]}")


def demonstrate_list_modification():
    """Demonstrate list modification operations."""
    print("\n=== List Modification ===")
    
    fruits = ["apple", "banana"]
    print(f"Original: {fruits}")
    
    # Adding elements
    fruits.append("cherry")
    print(f"After append: {fruits}")
    
    fruits.insert(1, "orange")
    print(f"After insert at index 1: {fruits}")
    
    fruits.extend(["grape", "kiwi"])
    print(f"After extend: {fruits}")
    
    # Removing elements
    removed = fruits.pop()
    print(f"Popped '{removed}': {fruits}")
    
    fruits.remove("banana")
    print(f"After removing 'banana': {fruits}")
    
    # Modifying elements
    fruits[0] = "red apple"
    print(f"After modifying index 0: {fruits}")
    
    # Clear all elements
    backup = fruits.copy()
    fruits.clear()
    print(f"After clear: {fruits}")
    print(f"Backup: {backup}")


def demonstrate_list_methods():
    """Demonstrate useful list methods."""
    print("\n=== List Methods ===")
    
    numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    print(f"Original: {numbers}")
    
    # Counting and finding
    print(f"Count of 1: {numbers.count(1)}")
    print(f"Index of first 5: {numbers.index(5)}")
    
    # Sorting
    sorted_numbers = sorted(numbers)  # Creates new list
    print(f"Sorted (new list): {sorted_numbers}")
    print(f"Original unchanged: {numbers}")
    
    numbers_copy = numbers.copy()
    numbers_copy.sort()  # Modifies in place
    print(f"Sorted in place: {numbers_copy}")
    
    # Reverse
    numbers_copy.reverse()
    print(f"Reversed: {numbers_copy}")
    
    # Min, max, sum
    print(f"Min: {min(numbers)}")
    print(f"Max: {max(numbers)}")
    print(f"Sum: {sum(numbers)}")


def demonstrate_list_comprehensions():
    """Demonstrate list comprehensions and advanced techniques."""
    print("\n=== List Comprehensions ===")
    
    numbers = range(1, 11)
    print(f"Original range: {list(numbers)}")
    
    # Basic list comprehension
    squares = [x**2 for x in numbers]
    print(f"Squares: {squares}")
    
    # With condition
    even_squares = [x**2 for x in numbers if x % 2 == 0]
    print(f"Even squares: {even_squares}")
    
    # Multiple conditions
    filtered = [x for x in numbers if x > 3 and x < 8]
    print(f"Numbers 4-7: {filtered}")
    
    # With function
    words = ["hello", "world", "python", "programming"]
    lengths = [len(word) for word in words]
    print(f"Word lengths: {lengths}")
    
    # Nested comprehension
    matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]
    print(f"3x3 multiplication matrix: {matrix}")
    
    # Flattening nested list
    nested = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = [item for sublist in nested for item in sublist]
    print(f"Flattened: {flattened}")


def demonstrate_dictionary_basics():
    """Demonstrate fundamental dictionary operations."""
    print("\n=== Dictionary Basics ===")
    
    # Creating dictionaries
    empty_dict = {}
    person = {"name": "Alice", "age": 30, "city": "New York"}
    mixed_keys = {1: "one", "two": 2, (3, 4): "tuple key"}
    
    print(f"Empty dict: {empty_dict}")
    print(f"Person: {person}")
    print(f"Mixed keys: {mixed_keys}")
    
    # Accessing values
    print(f"Name: {person['name']}")
    print(f"Age using get(): {person.get('age')}")
    print(f"Country (default): {person.get('country', 'Unknown')}")
    
    # Dictionary properties
    print(f"Keys: {list(person.keys())}")
    print(f"Values: {list(person.values())}")
    print(f"Items: {list(person.items())}")
    print(f"Length: {len(person)}")


def demonstrate_dictionary_modification():
    """Demonstrate dictionary modification operations."""
    print("\n=== Dictionary Modification ===")
    
    student = {"name": "Bob", "grade": "A"}
    print(f"Original: {student}")
    
    # Adding/updating values
    student["age"] = 20
    student["subjects"] = ["Math", "Science"]
    print(f"After adding: {student}")
    
    student.update({"grade": "A+", "semester": "Fall"})
    print(f"After update: {student}")
    
    # Removing items
    age = student.pop("age")
    print(f"Popped age {age}: {student}")
    
    last_item = student.popitem()
    print(f"Popped last item {last_item}: {student}")
    
    # Dictionary comprehension
    numbers = {x: x**2 for x in range(1, 6)}
    print(f"Number squares: {numbers}")
    
    # Filtering dictionary
    high_values = {k: v for k, v in numbers.items() if v > 10}
    print(f"Values > 10: {high_values}")


def demonstrate_dictionary_methods():
    """Demonstrate useful dictionary methods and patterns."""
    print("\n=== Dictionary Methods ===")
    
    # setdefault - get or set default value
    inventory = {}
    inventory.setdefault("apples", 0)
    inventory.setdefault("bananas", 5)
    inventory["apples"] += 10
    print(f"Inventory: {inventory}")
    
    # Using defaultdict for automatic defaults
    word_count = defaultdict(int)
    text = "hello world hello python world"
    for word in text.split():
        word_count[word] += 1
    print(f"Word count: {dict(word_count)}")
    
    # Merging dictionaries (Python 3.9+)
    dict1 = {"a": 1, "b": 2}
    dict2 = {"c": 3, "d": 4}
    merged = dict1 | dict2  # Or use {**dict1, **dict2}
    print(f"Merged: {merged}")
    
    # Dictionary from lists
    keys = ["name", "age", "city"]
    values = ["Charlie", 25, "Boston"]
    person = dict(zip(keys, values))
    print(f"From lists: {person}")


def demonstrate_set_operations():
    """Demonstrate set operations and methods."""
    print("\n=== Set Operations ===")
    
    # Creating sets
    empty_set = set()
    numbers = {1, 2, 3, 4, 5}
    from_list = set([1, 2, 2, 3, 3, 4])  # Duplicates removed
    from_string = set("hello")  # Unique characters
    
    print(f"Empty set: {empty_set}")
    print(f"Numbers: {numbers}")
    print(f"From list (duplicates removed): {from_list}")
    print(f"From string: {from_string}")
    
    # Set operations
    set1 = {1, 2, 3, 4, 5}
    set2 = {4, 5, 6, 7, 8}
    
    print(f"Set1: {set1}")
    print(f"Set2: {set2}")
    print(f"Union (|): {set1 | set2}")
    print(f"Intersection (&): {set1 & set2}")
    print(f"Difference (-): {set1 - set2}")
    print(f"Symmetric difference (^): {set1 ^ set2}")
    
    # Set methods
    print(f"Is 3 in set1? {3 in set1}")
    print(f"Is set1 subset of {1,2,3,4,5,6}? {set1.issubset({1,2,3,4,5,6})}")
    print(f"Is set1 superset of {1,2}? {set1.issuperset({1,2})}")
    
    # Modifying sets
    colors = {"red", "blue"}
    colors.add("green")
    colors.update(["yellow", "orange"])
    print(f"Colors after adding: {colors}")
    
    colors.discard("blue")  # No error if not present
    colors.remove("red")    # Error if not present
    print(f"Colors after removing: {colors}")


def demonstrate_tuple_operations():
    """Demonstrate tuple operations and use cases."""
    print("\n=== Tuple Operations ===")
    
    # Creating tuples
    empty_tuple = ()
    single_item = (42,)  # Note the comma
    coordinates = (10, 20)
    person = ("Alice", 30, "Engineer")
    nested = ((1, 2), (3, 4), (5, 6))
    
    print(f"Empty tuple: {empty_tuple}")
    print(f"Single item: {single_item}")
    print(f"Coordinates: {coordinates}")
    print(f"Person: {person}")
    print(f"Nested: {nested}")
    
    # Tuple unpacking
    name, age, job = person
    print(f"Unpacked - Name: {name}, Age: {age}, Job: {job}")
    
    # Multiple assignment
    a, b = 10, 20
    print(f"a = {a}, b = {b}")
    
    # Swapping variables
    a, b = b, a
    print(f"After swap - a = {a}, b = {b}")
    
    # Tuple methods
    numbers = (1, 2, 3, 2, 4, 2, 5)
    print(f"Numbers: {numbers}")
    print(f"Count of 2: {numbers.count(2)}")
    print(f"Index of first 3: {numbers.index(3)}")
    
    # Named tuples (basic example)
    from collections import namedtuple
    Point = namedtuple('Point', ['x', 'y'])
    p = Point(10, 20)
    print(f"Named tuple: {p}")
    print(f"Access by name: x={p.x}, y={p.y}")


def demonstrate_advanced_operations():
    """Demonstrate advanced operations with collections."""
    print("\n=== Advanced Operations ===")
    
    # Sorting complex data
    students = [
        {"name": "Alice", "grade": 85, "age": 20},
        {"name": "Bob", "grade": 92, "age": 19},
        {"name": "Charlie", "grade": 78, "age": 21}
    ]
    
    print("Original students:")
    for student in students:
        print(f"  {student}")
    
    # Sort by grade
    by_grade = sorted(students, key=lambda x: x["grade"], reverse=True)
    print("\nSorted by grade (descending):")
    for student in by_grade:
        print(f"  {student['name']}: {student['grade']}")
    
    # Sort by multiple criteria
    by_age_then_grade = sorted(students, key=lambda x: (x["age"], -x["grade"]))
    print("\nSorted by age (asc), then grade (desc):")
    for student in by_age_then_grade:
        print(f"  {student['name']}: age {student['age']}, grade {student['grade']}")
    
    # Using itemgetter for performance
    by_name = sorted(students, key=itemgetter("name"))
    print("\nSorted by name:")
    for student in by_name:
        print(f"  {student['name']}")
    
    # Grouping data
    from itertools import groupby
    
    # Group students by age
    age_sorted = sorted(students, key=itemgetter("age"))
    for age, group in groupby(age_sorted, key=itemgetter("age")):
        students_in_age = list(group)
        print(f"\nAge {age}:")
        for student in students_in_age:
            print(f"  {student['name']}")


def demonstrate_practical_examples():
    """Demonstrate practical applications with collections."""
    print("\n=== Practical Examples ===")
    
    # Shopping cart implementation
    class ShoppingCart:
        """Simple shopping cart using collections."""
        
        def __init__(self):
            self.items = {}  # item_name: quantity
            self.prices = {"apple": 0.5, "banana": 0.3, "orange": 0.8}
        
        def add_item(self, item, quantity=1):
            """Add item to cart."""
            if item in self.prices:
                self.items[item] = self.items.get(item, 0) + quantity
                return True
            return False
        
        def remove_item(self, item, quantity=1):
            """Remove item from cart."""
            if item in self.items:
                self.items[item] = max(0, self.items[item] - quantity)
                if self.items[item] == 0:
                    del self.items[item]
        
        def get_total(self):
            """Calculate total price."""
            return sum(self.prices[item] * qty for item, qty in self.items.items())
        
        def __str__(self):
            """String representation of cart."""
            if not self.items:
                return "Cart is empty"
            
            lines = ["Shopping Cart:"]
            for item, qty in self.items.items():
                price = self.prices[item] * qty
                lines.append(f"  {item}: {qty} x ${self.prices[item]:.2f} = ${price:.2f}")
            lines.append(f"Total: ${self.get_total():.2f}")
            return "\n".join(lines)
    
    # Demo shopping cart
    cart = ShoppingCart()
    cart.add_item("apple", 3)
    cart.add_item("banana", 2)
    cart.add_item("orange", 1)
    print(cart)
    
    cart.remove_item("banana", 1)
    print(f"\nAfter removing 1 banana:\n{cart}")
    
    # Word frequency analyzer
    def analyze_text(text):
        """Analyze text and return statistics."""
        # Clean and split text
        words = text.lower().replace(".", "").replace(",", "").split()
        
        # Count words using Counter
        word_freq = Counter(words)
        
        # Find unique words
        unique_words = set(words)
        
        # Create statistics
        stats = {
            "total_words": len(words),
            "unique_words": len(unique_words),
            "most_common": word_freq.most_common(3),
            "longest_word": max(words, key=len) if words else "",
            "average_length": sum(len(word) for word in words) / len(words) if words else 0
        }
        
        return stats
    
    sample_text = """
    Python is a powerful programming language. Python is easy to learn and 
    Python is widely used in data science, web development, and automation.
    """
    
    analysis = analyze_text(sample_text)
    print(f"\nText Analysis:")
    print(f"Text: {sample_text.strip()[:50]}...")
    for key, value in analysis.items():
        if key == "average_length":
            print(f"  {key.replace('_', ' ').title()}: {value:.1f}")
        else:
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Data transformation example
    def process_survey_data(responses):
        """Process survey responses into summary statistics."""
        # Group responses by category
        by_category = defaultdict(list)
        for response in responses:
            by_category[response["category"]].append(response["score"])
        
        # Calculate statistics for each category
        summary = {}
        for category, scores in by_category.items():
            summary[category] = {
                "count": len(scores),
                "average": sum(scores) / len(scores),
                "min": min(scores),
                "max": max(scores),
                "scores": sorted(scores)
            }
        
        return summary
    
    survey_responses = [
        {"category": "Service", "score": 4},
        {"category": "Quality", "score": 5},
        {"category": "Service", "score": 3},
        {"category": "Price", "score": 2},
        {"category": "Quality", "score": 4},
        {"category": "Service", "score": 5},
        {"category": "Price", "score": 3},
    ]
    
    summary = process_survey_data(survey_responses)
    print(f"\nSurvey Summary:")
    for category, stats in summary.items():
        print(f"  {category}:")
        print(f"    Average: {stats['average']:.1f}")
        print(f"    Range: {stats['min']}-{stats['max']}")
        print(f"    Count: {stats['count']}")


def demonstrate_memory_and_performance():
    """Demonstrate memory and performance considerations."""
    print("\n=== Memory and Performance Tips ===")
    
    # Shallow vs deep copy
    original = [[1, 2, 3], [4, 5, 6]]
    shallow = original.copy()
    deep = copy.deepcopy(original)
    
    print(f"Original: {original}")
    print(f"Shallow copy: {shallow}")
    print(f"Deep copy: {deep}")
    
    # Modify original
    original[0][0] = 999
    print(f"\nAfter modifying original[0][0] = 999:")
    print(f"Original: {original}")
    print(f"Shallow copy: {shallow}")  # Also affected!
    print(f"Deep copy: {deep}")        # Not affected
    
    # List vs set for membership testing
    import time
    
    large_list = list(range(10000))
    large_set = set(range(10000))
    
    # Time list membership
    start = time.time()
    9999 in large_list  # This is slow O(n)
    list_time = time.time() - start
    
    # Time set membership
    start = time.time()
    9999 in large_set   # This is fast O(1)
    set_time = time.time() - start
    
    print(f"\nMembership testing (finding 9999):")
    print(f"List time: {list_time:.6f} seconds")
    print(f"Set time: {set_time:.6f} seconds")
    print(f"Set is {list_time/set_time:.0f}x faster")
    
    # Memory-efficient techniques
    print(f"\nMemory tips:")
    print(f"- Use sets for unique items and fast membership testing")
    print(f"- Use tuples for immutable sequences (less memory)")
    print(f"- Use generators for large sequences (lazy evaluation)")
    print(f"- Use dictionaries for key-value lookups (O(1) average)")


def main():
    """Main function to run all demonstrations."""
    print("Python List, Dictionary, and Set Operations Examples")
    print("=" * 60)
    
    demonstrate_list_basics()
    demonstrate_list_modification()
    demonstrate_list_methods()
    demonstrate_list_comprehensions()
    demonstrate_dictionary_basics()
    demonstrate_dictionary_modification()
    demonstrate_dictionary_methods()
    demonstrate_set_operations()
    demonstrate_tuple_operations()
    demonstrate_advanced_operations()
    demonstrate_practical_examples()
    demonstrate_memory_and_performance()
    
    print("\n" + "=" * 60)
    print("All collection operations examples completed!")


if __name__ == "__main__":
    main()


# Usage Examples:
"""
To run this script:
    python list_dict_operations.py

Key concepts covered:
1. List operations (creation, modification, methods, comprehensions)
2. Dictionary operations (CRUD, methods, comprehensions)
3. Set operations (unique collections, mathematical operations)
4. Tuple operations (immutable sequences, unpacking)
5. Advanced sorting and grouping techniques
6. Practical applications (shopping cart, text analysis)
7. Performance and memory considerations

Best practices demonstrated:
- Use appropriate collection type for each use case
- Leverage list/dict comprehensions for readable code
- Use sets for membership testing and unique items
- Consider memory and performance implications
- Use defaultdict and Counter for common patterns
- Implement proper error handling
- Use meaningful variable names and documentation
- Prefer built-in methods over custom implementations

Collection Type Guidelines:
- List: Ordered, mutable, allows duplicates - use for sequences
- Tuple: Ordered, immutable, allows duplicates - use for fixed data
- Set: Unordered, mutable, no duplicates - use for unique items
- Dict: Key-value pairs, ordered (Python 3.7+) - use for mappings
"""