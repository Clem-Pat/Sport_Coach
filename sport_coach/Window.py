import tkinter as tk
from pynput.keyboard import Key
from pynput.keyboard import Controller as key_Controller

class tkinterWindow():

    def __init__(self,name_of_application):

        self.fen = tk.Tk()
        self.name = name_of_application

        if self.name == 'fen':
            self.x, self.y = 400, 150
            self.longueur, self.hauteur = 430, 400
            self.fen.title("Définition de l'objectif")
            self.fen.geometry("{}x{}+{}+{}".format(str(self.longueur), str(self.hauteur), str(self.x), str(self.y)))

        elif self.name == 'settings':
            self.x, self.y = 400, 150
            self.longueur, self.hauteur = 500, 400
            self.fen.title("Réglages")
            self.fen.geometry("{}x{}+{}+{}".format(str(self.longueur), str(self.hauteur), str(self.x), str(self.y)))

        elif self.name == 'main':
            self.x, self.y = 220, 0
            self.longueur, self.hauteur = 825, 645
            self.fen.title("Objectif 1000 pompes")
            self.fen.geometry("{}x{}+{}+{}".format(str(self.longueur), str(self.hauteur), str(self.x), str(self.y)))

        # self.fen.minsize(self.longueur, self.hauteur)
        self.fen.resizable(width=False, height=False)
        self.fen.configure(bg="light blue")


    def move(self, state):
        """cliquer sur le bouton directement"""
        keyboard = key_Controller()
        if self.name == 'fen':
            for i in range(7):
                keyboard.press(Key.tab)
                keyboard.release(Key.tab)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
