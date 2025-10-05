import random
import ntpath
import time
import datetime
from datetime import datetime
import disnake
from disnake.ext import commands
import random

class RandomWordle(commands.Cog):
    def __init__(self, client, filename):
        self.client = client
        with open("txt/fiveletter.txt", 'r') as f:
            self.words = f.read().splitlines()
        self.wordle_word = None


    def get_random_wordle(self):
        self.wordle_word = random.choice(self.words)
        return self.wordle_word


def setup(client):
    client.add_cog(RandomWordle(client, 'txt/fiveletter.txt'))