import pyttsx3
from Gamer import Gamer
import random
import time
import pandas as pd

# configuring pyttsx3 to use English voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

class Giratron:
    cards = ["one", "two", "three", "four", "five", "six", "red", "green", "blue", "yellow"]  # static attribute

    def __init__(self, points):
        self.__sequence = []
        self.__points = points
        self.__level = 1

    # class method for show the rules
    @classmethod
    def rules(cls):
        print("\n----------------------------------- GAME RULES -----------------------------------------")
        print("- The game will speak a color or number "
              "\n- The objective of the game is for the player to remember what was said and write it down "
              "\n- Write only one word at a time")

        cls.menu()

    # static method for show the menu
    @staticmethod
    def menu():
        print("\n------ GAME GIRATRON ------")
        print("--- Welcome to the game ---\n")

        while True:
            try:
                option = int(input(f"---- {gamer.name_gamer}: ---- \n---- Type one option ---- \n"
                                   "[1] Start Game\n"
                                   "[2] Finish Game\n"))

                if option == 1:
                    giratron.levels()
                elif option == 2:
                    print("Finish Game...")
                    exit()

            except ValueError:
                print("\nType it the option value\n")
                continue

            break

    # speak the sequence for the player
    def speak_sequence(self):
        i = 0

        # each level increases a word
        while i < 2 + (self.__level + 1):
            seq = random.choice(Giratron.cards) # draw the sequence
            engine = pyttsx3.init()
            engine.say(seq) # says the drawn sequence
            self.__sequence.append(seq)
            engine.runAndWait()
            i += 1

        self.choose_player()

    # function for the player to match the drawn sequence
    def choose_player(self):
        gamer_sequence = []

        print("\n-------------------------")
        print("Write one word at a time!")
        print("-------------------------\n")

        for r in range(2 + (self.__level + 1)):
            g = input("Try to get the sequence right: ").lower().replace(" ", "")
            gamer_sequence.append(g)

        print("")
        self.check_sequence(self.__sequence, gamer_sequence) # checks the player sequence

    # checks the player sequence
    def check_sequence(self, sequence, gamer_sequence):
        # use for to check index by index of the word
        for i in range(2 + (self.__level + 1)):
            # If everything is ok, it adds points for the player
            if sequence[i] == gamer_sequence[i]:
                self.__points += 1
            # If everything is not correct, it shows the correct word and what the player got wrong
            else:
                print(" - Wrong Word: ", gamer_sequence[i], " - Rigth Word: ", sequence[i])

            i += 1

        # show the points of the player
        print(f"\n - You did it {self.__points} points")

        # If everything is ok, go to the next level
        if self.__sequence == gamer_sequence:
            print("\n - You got all the words right!")
            self.__level += 1
            if self.__level:
                print(f"\n - Advancing to the level {self.__level}\n")
                self.levels()

        # If you don't get everything right, the game ends
        else:
            print("\n - You didn't get all the words right. Finish Game!")

            # Options menu
            while True:
                try:
                    option = int(input("\nChoose an option:"
                                       "\n[1] Continue with the same player"
                                       "\n[2] Change player"
                                       "\n[3] Finish Game...\n"))

                    # in all cases first save the score in the excel spreadsheet before going to the option chosen
                    # by the player
                    if option == 1:
                        print(" - Exporting scores to excel...\n")
                        self.export_excel()
                        print(" - Restart the game with the same player...\n")
                        giratron.menu()
                    elif option == 2:
                        print(" - Exporting scores to excel...\n")
                        self.export_excel()
                        print(" - Restart the game with another player...\n")
                        # resets all player progress by creating a new
                        gamer.name_gamer = ""
                        self.__points = 0
                        self.__level = 1
                        self.__sequence = []
                        gamer.__init__()
                        giratron.rules()
                    elif option == 3:
                        print(" - Exporting scores to excel...\n")
                        self.export_excel()
                        print("Finish Game...")
                        exit()

                except ValueError:
                    print("\nType it the option value\n")
                    continue

                break

    # function to change level
    def levels(self):
        for i in range(1, 4):
            print(f"Start in {i}...")
            time.sleep(1)

        print(f"\n--- Level {self.__level} ----")

        if self.__level == 1:
            self.speak_sequence()

        # After level one, the sequence is repeated adding only one new word
        else:
            seq = random.choice(Giratron.cards)
            engine = pyttsx3.init()

            for s in self.__sequence:
                engine.say(s)

            engine.say(seq)
            self.__sequence.append(seq)
            engine.runAndWait()

            self.choose_player()

    # function to export to excel in descending order of points
    def export_excel(self):
        # Checks if the file already exists
        try:
            # Try to read the existing file
            file = pd.read_excel('ranking.xlsx')
        except FileNotFoundError:
            # If the file does not exist, create an empty DataFrame
            file = pd.DataFrame(columns=['Players', 'Punctuation'])

        # Adds the new entry to the DataFrame
        new_entry = pd.DataFrame({'Players': [gamer.name_gamer], 'Punctuation': [self.__points]})
        file = pd.concat([file, new_entry], ignore_index=True)

        # Sort the DataFrame by score in descending order
        file = file.sort_values(by='Punctuation', ascending=False)

        # Saves the DataFrame to the Excel file
        file.to_excel('ranking.xlsx', index=False)

# creates an object
gamer = Gamer()
giratron = Giratron(0)

if __name__ == "__main__":
    giratron.rules()
