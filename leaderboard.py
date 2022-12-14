#counts "lowest" scores for time at a given level

def get_low_score():
    # Default winning score
    lowest_score = 100000

    # Try to read the winning score from a file
    try:
        low_score_file = open("low_score.txt", "r")
        lowest_score = int(low_score_file.read())
        low_score_file.close()
        print("The low score is", lowest_score)
    except IOError:
        # Error reading file, no low score
        print("There is no lowest score yet.")
        pass
    except ValueError:
        # There's a file there, but we don't understand the number.
        print("I'm confused. Starting with no low score.")

    return lowest_score


def save_low_score(new_low_score):
    try:
        # Write the file to disk
        low_score_file = open("low_score.txt", "w")
        low_score_file.write(str(new_low_score))
        low_score_file.close()
    except IOError:
        # Hm, can't write it.
        print("Unable to save the low score.")

def isless(your_score, lowest_score):
    try:
        # Ask the user for his/her score
        current_score = int(input("What is your score? "))
    except ValueError:
        # Error, can't turn what they typed into a number
        print("I don't understand the input.")

    # See if we have a new low score
    if current_score < lowest_score:
        # We do! Save to disk
        print("Congrats! You have the new shortest time!")
        save_low_score(current_score)
    else:
        print("Better luck next time.")


def main():
    """ Main program is here. """
    # Get the lowest score

    # Get the score from the current game
    current_score = 0
    lowest_score = get_low_score()
    isless(current_score, lowest_score)

# Call the main function, start up the game
if __name__ == "__main__":
    main()