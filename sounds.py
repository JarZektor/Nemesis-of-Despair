import pygame

pygame.mixer.init()
bg_melodies = [
    pygame.mixer.Sound('sounds/music/Coridors of Elinos.mp3'),
    pygame.mixer.Sound('sounds/music/Elevation of soul.mp3'),
    pygame.mixer.Sound('sounds/music/Canteen of Elinos.mp3')
]
sound = {
    'footstep': pygame.mixer.Sound('sounds/sounds/footsteps.mp3'),
    'fail': pygame.mixer.Sound('sounds/sounds/fail.mp3'),
    'success': pygame.mixer.Sound('sounds/sounds/success.mp3'),
    'pickup': pygame.mixer.Sound('sounds/sounds/pickup.mp3'),
    'ladder': pygame.mixer.Sound('sounds/sounds/ladder.mp3'),
    'door': pygame.mixer.Sound('sounds/sounds/door use.mp3')
}