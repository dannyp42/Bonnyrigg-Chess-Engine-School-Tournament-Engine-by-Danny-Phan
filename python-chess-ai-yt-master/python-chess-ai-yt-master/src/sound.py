import pygame
import os

class Sound:

    def __init__(self, path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(current_dir, ".."))
        full_path = os.path.join(project_dir, path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Sound file not found:\n{full_path}")

        self.sound = pygame.mixer.Sound(full_path)

    def play(self):
     self.sound.play()