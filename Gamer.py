class Gamer:
    def __init__(self):
        while True:
            self.name_gamer = input("Enter with the name: \n").upper()
            if all(c.isalpha() or c.isspace() for c in self.name_gamer):
                break
            else:
                print("\nPlease enter with only letters\n")

        self.game_lives = 5