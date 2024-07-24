import csv
from tqdm import tqdm
import sqlite3
import os


database_name = 'complete_numbers.db'
# remove the database file if it already exists
if os.path.exists(database_name):
    os.remove(database_name)


conn = sqlite3.connect(database_name)
c = conn.cursor()
c.execute('''CREATE TABLE numbers (number integer, operator text)''')
conn.close()


def generate_numbers(pattern):
    # Normalize the pattern by removing hyphens and spaces
    pattern = pattern.replace('-', '').replace(' ', '')

    if 'x' in pattern:
        x_count = pattern.count('x')
        start = pattern.split('x')[0]
        end_pattern = "{:0" + str(x_count) + "d}"
        return [f"{start}{end_pattern.format(i)}" for i in range(10**x_count)]
    else:
        raise ValueError(f"Unexpected pattern format: {pattern}")

# Read the ranges and operators from the input CSV file
input_file = 'input_ranges.csv'
ranges = []

with open(input_file, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header
    for row in reader:
        ranges.append((row[0], row[1]))

# Calculate total number of numbers to be generated for the progress bar
total_numbers = sum(10**pattern.count('x') for pattern, _ in ranges)

#  Insert the complete list of numbers and operators

conn = sqlite3.connect(database_name)
c = conn.cursor()
# SQLite synchornous mode is set to OFF to speed up the insertion
c.execute('PRAGMA synchronous = OFF')
c.execute('PRAGMA journal_mode = MEMORY')
c.execute('BEGIN TRANSACTION')
with tqdm(total=total_numbers, desc="Generating numbers") as pbar:
    for number_range, operator in ranges:
        numbers = generate_numbers(number_range)
        for number in numbers:
            c.execute('INSERT INTO numbers VALUES (?, ?)', (number, operator))
            pbar.update(1)

c.execute('COMMIT')

print ("Creating index on the number column")
# Create an index on the number column to speed up the search
c.execute('CREATE INDEX number_index ON numbers (number)')

conn.close()

print(f"file '{database_name}' has been created.")
