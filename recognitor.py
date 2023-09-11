import re
import os
import subprocess
from itertools import chain


def start():
    wordlist_files = [
        'marksonad kirjakeele seletav sonaraamat.txt',
        'itvaatlik_wordlist.txt',
        'marksonad.txt'
    ]
    print("Preparing wordlists...")
    wordlist = initialize_wordlists(wordlist_files)
    print("Done, wordlist size is " + str(len(wordlist)) + " words.\n")

    print("Slicing image file (check README for the reason and more info)...")
    slice_image()

    print("\nStarting Google Vision API connection, uploading images and analyzing characters...")
    matrix = prepare_character_matrix()
    print("Characters recognized, matrix prepared!\n")

    # test_matrix = [
    #     ['T', 'K', 'R', 'T', 'X', 'X', 'D', 'U', 'G', 'C', 'I', 'X', 'B', 'X', 'Ä', 'I', 'M', 'P', 'L', 'K', 'T', 'K', 'R', 'T', 'X', 'X', 'D', 'U', 'G', 'C', 'I', 'X', 'B', 'X', 'Ä', 'I', 'M', 'P', 'L', 'K'],
    #     ['B', 'L', 'H', 'M', 'Y', 'Z', 'K', 'B', 'I', 'N', 'N', 'Z', 'Ö', 'X', 'O', 'R', 'F', 'B', 'P', 'O', 'B', 'L', 'H', 'M', 'Y', 'Z', 'K', 'B', 'I', 'N', 'N', 'Z', 'Ö', 'X', 'O', 'R', 'F', 'B', 'P', 'O'],
    #     ['Ö', 'V', 'H', 'P', 'Z', 'K', 'K', 'D', 'V', 'O', 'N', 'A', 'B', 'S', 'P', 'I', 'N', 'Z', 'L', 'D', 'Ö', 'V', 'H', 'P', 'Z', 'K', 'K', 'D', 'V', 'O', 'N', 'A', 'B', 'S', 'P', 'I', 'N', 'Z', 'L', 'D'],
    #     ['K', 'O', 'L', 'K', 'H', 'Ü', 'Q', 'B', 'C', 'O', 'V', 'S', 'Y', 'M', 'B', 'I', 'Y', 'O', 'K', 'L', 'K', 'O', 'L', 'K', 'H', 'Ü', 'Q', 'B', 'C', 'O', 'V', 'S', 'Y', 'M', 'B', 'I', 'Y', 'O', 'K', 'L'],
    #     ['Ä', 'S', 'K', 'H', 'N', 'B', 'O', 'Y', 'R', 'J', 'Ö', 'L', 'K', 'W', 'N', 'G', 'Q', 'Z', 'L', 'R', 'Ä', 'S', 'K', 'H', 'N', 'B', 'O', 'Y', 'R', 'J', 'Ö', 'L', 'K', 'W', 'N', 'G', 'Q', 'Z', 'L', 'R'],
    #     ['D', 'Q', 'X', 'M', 'V', 'E', 'J', 'T', 'D', 'O', 'N', 'J', 'U', 'O', 'R', 'I', 'Q', 'C', 'E', 'T', 'D', 'Q', 'X', 'M', 'V', 'E', 'J', 'T', 'D', 'O', 'N', 'J', 'U', 'O', 'R', 'I', 'Q', 'C', 'E', 'T'],
    #     ['S', 'A', 'X', 'U', 'D', 'R', 'J', 'L', 'F', 'Z', 'V', 'L', 'X', 'G', 'Q', 'P', 'E', 'D', 'Ő', 'N', 'S', 'A', 'X', 'U', 'D', 'R', 'J', 'L', 'F', 'Z', 'V', 'L', 'X', 'G', 'Q', 'P', 'E', 'D', 'Ő', 'N'],
    #     ['M', 'Q', 'Ä', 'Ä', 'Q', 'M', 'D', 'Y', 'U', 'I', 'N', 'M', 'B', 'O', 'J', 'I', 'O', 'Y', 'V', 'x', 'M', 'Q', 'Ä', 'Ä', 'Q', 'M', 'D', 'Y', 'U', 'I', 'N', 'M', 'B', 'O', 'J', 'I', 'O', 'Y', 'V', 'x'],
    #     ['M', 'C', 'N', 'L', 'A', 'A', 'B', 'B', 'A', 'M', 'J', 'J', 'Y', 'P', 'S', 'I', 'E', 'L', 'P', 'F', 'M', 'C', 'N', 'L', 'A', 'A', 'B', 'B', 'A', 'M', 'J', 'J', 'Y', 'P', 'S', 'I', 'E', 'L', 'P', 'F'],
    #     ['V', 'H', 'Ö', 'Q', 'V', 'A', 'J', 'H', 'A', 'M', 'U', 'R', 'C', 'Ü', 'D', 'R', 'O', 'L', 'E', 'J', 'V', 'H', 'Ö', 'Q', 'V', 'A', 'J', 'H', 'A', 'M', 'U', 'R', 'C', 'Ü', 'D', 'R', 'O', 'L', 'E', 'J'],
    #     ['A', 'O', 'B', 'K', 'Z', 'I', 'J', 'M', 'W', 'U', 'G', 'Q', 'Ä', 'A', 'F', 'E', 'K', 'N', 'N', 'V', 'A', 'O', 'B', 'K', 'Z', 'I', 'J', 'M', 'W', 'U', 'G', 'Q', 'Ä', 'A', 'F', 'E', 'K', 'N', 'N', 'V'],
    #     ['M', 'L', 'H', 'L', 'O', 'L', 'C', 'Ö', 'N', 'A', 'W', 'I', 'G', 'Y', 'P', 'O', 'Z', 'T', 'P', 'Ü', 'M', 'L', 'H', 'L', 'O', 'L', 'C', 'Ö', 'N', 'A', 'W', 'I', 'G', 'Y', 'P', 'O', 'Z', 'T', 'P', 'Ü'],
    #     ['E', 'L', 'X', 'O', 'B', 'M', 'T', 'J', 'W', 'T', 'A', 'U', 'R', 'I', 'X', 'L', 'H', 'C', 'K', 'H', 'E', 'L', 'X', 'O', 'B', 'M', 'T', 'J', 'W', 'T', 'A', 'U', 'R', 'I', 'X', 'L', 'H', 'C', 'K', 'H'],
    #     ['Ä', 'G', 'B', 'C', 'B', 'A', 'D', 'C', 'X', 'Q', 'Ö', 'E', 'C', 'N', 'Ü', 'Y', 'R', 'Z', 'F', 'F', 'Ä', 'G', 'B', 'C', 'B', 'A', 'D', 'C', 'X', 'Q', 'Ö', 'E', 'C', 'N', 'Ü', 'Y', 'R', 'Z', 'F', 'F'],
    #     ['Õ', 'Q', 'U', 'S', 'U', 'S', 'I', 'C', 'J', 'S', 'Ä', 'O', 'F', 'K', 'C', 'Ö', 'V', 'K', 'E', 'F', 'Õ', 'Q', 'U', 'S', 'U', 'S', 'I', 'C', 'J', 'S', 'Ä', 'O', 'F', 'K', 'C', 'Ö', 'V', 'K', 'E', 'F'],
    #     ['Ä', 'G', 'V', 'Q', 'V', 'J', 'D', 'I', 'F', 'Y', 'G', 'Y', 'E', 'U', 'G', 'K', 'I', 'B', 'M', 'E', 'Ä', 'G', 'V', 'Q', 'V', 'J', 'D', 'I', 'F', 'Y', 'G', 'Y', 'E', 'U', 'G', 'K', 'I', 'B', 'M', 'E']
    # ]

    transposed_matrix = transpose_matrix(matrix)
    south_east_diagonals = read_south_east_diagonals(matrix)
    north_east_diagonals = read_north_east_diagonals(transposed_matrix)

    print("Starting word-search (W->E, N->S, NW->SE, SW->NE) from matrix based on wordlists...")
    matches_from_rows = identify_words(matrix, wordlist)
    matches_from_columns = identify_words(transposed_matrix, wordlist)
    matches_from_south_east_diagonals = identify_words(south_east_diagonals, wordlist)
    matches_from_north_east_diagonals = identify_words(north_east_diagonals, wordlist)

    matches = sanitize_list(matches_from_rows + matches_from_columns + matches_from_south_east_diagonals + matches_from_north_east_diagonals)
    two_char_results = [match for match in matches if len(match) == 2]
    longer_than_two_results = [match for match in matches if match not in two_char_results]

    print("Lots of noise in 2-character length findings, giving them separately here: " + ', '.join(two_char_results) + "\n")
    print("Longer than 2-character words from the puzzle: " + ', '.join(longer_than_two_results) + "\n")

    print("Feed the previous results to ChatGPT and ask it to form sentences using ONLY these words: https://chat.openai.com")


# Process image-file in Google Cloud Vision API to get the characters from it
def identify_chars(path):
    """Detects text in the file."""
    from google.cloud import vision_v1p4beta1 as vision
    import io

    # Initialize the client
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    # Estonian language only
    image_context = vision.ImageContext(language_hints='et')

    response = client.text_detection(image=image, image_context=image_context)
    texts = response.text_annotations
    
    letters = []
    for text in texts:
        letter = re.sub(r'\s', '', text.description)
        
        if letter: # don't add if empty string
            letters += letter

    if response.error.message:
        raise Exception(
            f'{response.error.message}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'
        )

    return letters


# Identify words from rows in a matrix (or diagonals-collection)
def identify_words(matrix, wordlist):
    pattern = "|".join(re.escape(word) for word in wordlist)

    # Search for the words in the input string
    matches = []
    for row in matrix:
        print("RIDA: " + (''.join(row)))
        matches.append(re.findall(pattern, ''.join(row), flags=re.IGNORECASE))

    return matches


# Merge all wordlist files' contents into one big unique wordlist
def initialize_wordlists(wordlist_files):
    wordlists = []

    for wordlist_file in wordlist_files:
        try:
            with open(wordlist_file, 'r') as file:
                # Read all rows from the file into a list.
                # Remove line feeds and whitespace characters.
                rows = [row.replace("\n", "") for row in file.readlines() if len(row) > 2]

        except FileNotFoundError:
            print(f"File '{wordlist_file}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        wordlists.append(rows)

    general_wordlist = sanitize_list(wordlists)

    return general_wordlist


# Flatten and "unique-ify"
def sanitize_list(messy_list):
    # Flatten the list using nested list comprehension
    flattened_wordlist = list(chain.from_iterable(messy_list))
    # Convert the list to a set to ensure all elements are unique
    unique_wordlist_set = set(flattened_wordlist)
    # Convert the set back to a list
    wordlist = list(unique_wordlist_set)

    return wordlist


# Check for columns as well
def transpose_matrix(matrix):
    # Transpose the matrix using list comprehensions
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


# Extract all rows from image
def slice_image():
    # Define the path to your Bash script file
    bash_script_path = 'slicer.sh'

    # Use subprocess to run the Bash script
    try:
        # Run the Bash script
        subprocess.run(['bash', bash_script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Bash script: {e}")


# Extract characters from the sliced images and put them into a matrix
def prepare_character_matrix():
    directory_path = './cropped'
    # Get a list of files in the directory
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    # Sort files by last modified time to make sure rows are in order
    files.sort(key=lambda x: os.path.getmtime(os.path.join(directory_path, x)))

    matrix = []
    for filename in files:
        path = directory_path + '/' + filename
        print(path)
        matrix.append(identify_chars(path))

    return matrix


def read_south_east_diagonals(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    south_east_diagonals = []

    for d in range(rows + cols - 1):
        diagonal = []
        if d < cols:
            i, j = 0, cols - d - 1
        else:
            i, j = d - cols + 1, 0
        while i < rows and j < cols:
            diagonal.append(matrix[i][j])
            i += 1
            j += 1
        south_east_diagonals.append(diagonal)

    return south_east_diagonals


def read_north_east_diagonals(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    north_east_diagonals = []

    for d in range(rows + cols - 1):
        diagonal = []
        if d < cols:
            i, j = 0, d
        else:
            i, j = d - cols + 1, cols - 1
        while i < rows and j >= 0:
            diagonal.append(matrix[i][j])
            i += 1
            j -= 1
        north_east_diagonals.append(diagonal)

    return north_east_diagonals

start()