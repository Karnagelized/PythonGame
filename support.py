
import pygame
import os
import csv

# Read csv file
def import_csv(path:str) -> list:
    with open(path) as csv_file:
        try:
            return [line[0].split(';') for line in csv.reader(csv_file)]
        except Exception as Error:
            print(Error)

# Load image in pygame
def import_folder(path:str):
    if isinstance(path, str) and os.path.isdir(path):
        return [pygame.image.load(f'{path}/{item}').convert_alpha() for item in os.listdir(path)]
    else:
        return [pygame.image.load(item).convert_alpha() for item in path]

# Load sounds into list of sound
def import_sounds(path:list):
    return [pygame.mixer.Sound(sound) for sound in path]

