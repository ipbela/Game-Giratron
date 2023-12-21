import pyttsx3
from Gamer import Gamer
import random
import time


# class method com nome, por exemplo, mas vamos tentar pensar em outra coisa
# mudar o idioma para ingles e a voz do narrador

class Giratron:
    cards = ["one", "two", "three", "four", "five", "six", "red", "green", "blue", "yellow"]  # static attribute

    def __init__(self, chances, points):
        self.__sequence = []
        self.__chances = chances
        self.__points = points
        self.__level = 1

    @classmethod
    def rules(cls):
        print("\n----------------------------------- GAME RULES -----------------------------------------")
        print("- The game will speak a color or number "
              "\n- The objective of the game is for the player to remember what was said and write it down "
              "\n- Write only one word at a time")

        cls.menu()

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

    def speak_sequence(self):
        i = 0
        while i < 2 + (self.__level + 1):
            seq = random.choice(Giratron.cards)
            engine = pyttsx3.init()
            engine.say(seq)
            self.__sequence.append(seq)
            engine.runAndWait()
            i += 1

        self.choose_player()

    def choose_player(self):
        gamer_sequence = []

        print("\n-------------------------")
        print("Write one word at a time!")
        print("-------------------------\n")

        for r in range(2 + (self.__level + 1)):
            g = input("Try to get the sequence right: ").lower()  # split aqui
            gamer_sequence.append(g)

        print("")
        self.check_sequence(self.__sequence, gamer_sequence)

    def check_sequence(self, sequence, gamer_sequence):
        for i in range(2 + (self.__level + 1)):
            if sequence[i] == gamer_sequence[i]:
                self.__points += 1
            else:
                print(" - Wrong Word: ", gamer_sequence[i], " - Rigth Word: ", sequence[i])

            i += 1

        print(f"\n - You did it {self.__points} points")

        if self.__sequence == gamer_sequence:
            print("\n - You got all the words right!")
            self.__level += 1
            if self.__level:
                print(f"\n - Advancing to the level {self.__level}\n")
                self.levels()

        else:
            print("\n - You didn't get all the words right. Finish Game!")
            print(" - Restart...")
            giratron.menu()

    def levels(self):
        for i in range(1, 4):
            print(f"Start in {i}...")
            time.sleep(1)

        print(f"\n--- Level {self.__level} ----")
        if self.__level == 1:
            self.speak_sequence()
        else:
            seq = random.choice(Giratron.cards)
            engine = pyttsx3.init()

            for s in self.__sequence:
                engine.say(s)

            engine.say(seq)
            self.__sequence.append(seq)
            engine.runAndWait()

            self.choose_player()


gamer = Gamer()
giratron = Giratron(0, 0)

if __name__ == "__main__":
    giratron.rules()
