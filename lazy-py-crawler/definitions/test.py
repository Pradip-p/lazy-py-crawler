with open('output.txt', 'r') as file:
    # Create an empty dictionary to store word frequencies
    word_freq = {}

    # Loop through each line of the file
    for line in file:
        # Split the line into words
        words = line.split()

        # Loop through each word
        for word in words:
            # If the word is already in the dictionary, increment its frequency
            if word in word_freq:
                word_freq[word] += 1
            # Otherwise, add the word to the dictionary with a frequency of 1
            else:
                word_freq[word] = 1

    # Loop through the dictionary and print the words with a frequency greater than 1
    for word, freq in word_freq.items():
        if freq > 1:
            print(word, freq)
