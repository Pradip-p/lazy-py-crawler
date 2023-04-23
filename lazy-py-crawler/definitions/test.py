# Open the input file
with open('phrases.txt', 'r') as input_file:
    # Open the output file
    with open('unique_phrases.txt', 'w') as output_file:
        # Loop through each line in the input file
        for line in input_file:
            # Split the line into words
            words = line.strip().split()
            
            # Remove duplicate words
            unique_words = list(set(words))

            # Check if there are any unique words
            if unique_words:
                # Write the unique words to the output file
                output_file.write(' '.join(unique_words) + '\n')

