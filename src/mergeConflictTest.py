import math
import sys
import random
import os
import time
import json

def main():
    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Print a welcome message and wait for a second
    print("Welcome to the Random Number List Builder!")
    time.sleep(1)

    # Initialize an empty list to store the random numbers
    numbers = []

    # Get user input for the number of random numbers to add to the list
    num_of_elements = int(input("How many random numbers would you like to add to the list? "))

    # Loop through the specified number of elements
    for i in range(num_of_elements):
        random_number = random.randint(1, 100)
        numbers.append(random_number)
        print(f"Adding {random_number} to the list...")
        time.sleep(0.5)

    print("\nHere's the final list of random numbers:")
    print(numbers)

    sum_of_numbers = sum(numbers)
    average_of_numbers = sum_of_numbers / len(numbers)

    # Print the sum and average, rounding the average to 2 decimal places
    print(f"\nThe sum of the numbers is: {sum_of_numbers}")
    print(f"The average of the numbers is: {round(average_of_numbers, 2)}")

    # Save the list of random numbers as a JSON file
    with open("random_numbers.json", "w") as outfile:
        json.dump(numbers, outfile)
    print("\nThe list of random numbers has been saved as 'random_numbers.json'.")

if __name__ == "__main__":
    main()