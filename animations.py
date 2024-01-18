import pygame
empty_render = [
    pygame.image.load('images/player/move right/1r.png'),
    pygame.image.load('images/player/move right/1r.png'),
    pygame.image.load('images/player/move right/1r.png'),
    pygame.image.load('images/player/move right/1r.png'),
    pygame.image.load('images/player/move right/1r.png'),
    pygame.image.load('images/player/move right/1r.png'),
    pygame.image.load('images/player/move right/1r.png'),
    pygame.image.load('images/player/move right/1r.png'),
    pygame.image.load('images/player/move right/1r.png'),
    pygame.image.load('images/player/move right/1r.png'),
    pygame.image.load('images/player/move right/1r.png'),
    pygame.image.load('images/player/move right/1r.png'),
    pygame.image.load('images/player/move right/1r.png'),
    pygame.image.load('images/player/move right/1r.png'),
    pygame.image.load('images/player/move right/1r.png')
]
player_move_right = [
    pygame.image.load('images/player/move right/1r.png'),  # 1
    pygame.image.load('images/player/move right/1r.png'),  # 2
    pygame.image.load('images/player/move right/2r.png'),  # 3
    pygame.image.load('images/player/move right/2r.png'),  # 4
    pygame.image.load('images/player/move right/2r.png'),  # 5
    pygame.image.load('images/player/move right/3r.png'),  # 6
    pygame.image.load('images/player/move right/3r.png'),  # 7
    pygame.image.load('images/player/move right/4r.png'),  # 8
    pygame.image.load('images/player/move right/4r.png'),  # 9
    pygame.image.load('images/player/move right/4r.png'),  # 10
    pygame.image.load('images/player/move right/5r.png'),  # 11
    pygame.image.load('images/player/move right/5r.png'),  # 12
    pygame.image.load('images/player/move right/5r.png'),  # 13
    pygame.image.load('images/player/move right/6r.png'),  # 14
    pygame.image.load('images/player/move right/6r.png')  # 15
]
player_move_left = [
    pygame.image.load('images/player/move left/1l.png'),  # 1
    pygame.image.load('images/player/move left/1l.png'),  # 2
    pygame.image.load('images/player/move left/2l.png'),  # 3
    pygame.image.load('images/player/move left/2l.png'),  # 4
    pygame.image.load('images/player/move left/2l.png'),  # 5
    pygame.image.load('images/player/move left/3l.png'),  # 6
    pygame.image.load('images/player/move left/3l.png'),  # 7
    pygame.image.load('images/player/move left/4l.png'),  # 8
    pygame.image.load('images/player/move left/4l.png'),  # 9
    pygame.image.load('images/player/move left/4l.png'),  # 10
    pygame.image.load('images/player/move left/5l.png'),  # 11
    pygame.image.load('images/player/move left/5l.png'),  # 12
    pygame.image.load('images/player/move left/5l.png'),  # 13
    pygame.image.load('images/player/move left/6l.png'),  # 14
    pygame.image.load('images/player/move left/6l.png')  # 15
]
player_idle = [
    pygame.image.load('images/player/idle/1i.png'),  # 1
    pygame.image.load('images/player/idle/1i.png'),  # 2
    pygame.image.load('images/player/idle/2i.png'),  # 3
    pygame.image.load('images/player/idle/2i.png'),  # 4
    pygame.image.load('images/player/idle/3i.png'),  # 5
    pygame.image.load('images/player/idle/3i.png'),  # 6
    pygame.image.load('images/player/idle/4i.png'),  # 7
    pygame.image.load('images/player/idle/4i.png'),  # 8
    pygame.image.load('images/player/idle/4i.png'),  # 9
    pygame.image.load('images/player/idle/5i.png'),  # 10
    pygame.image.load('images/player/idle/5i.png'),  # 11
    pygame.image.load('images/player/idle/6i.png'),  # 12
    pygame.image.load('images/player/idle/6i.png'),  # 13
    pygame.image.load('images/player/idle/7i.png'),  # 14
    pygame.image.load('images/player/idle/7i.png')  # 15
]
steam = [
    pygame.image.load('images/puzzles/steam/steam_wall_1.png'),   # 1
    pygame.image.load('images/puzzles/steam/steam_wall_2.png'),   # 2
    pygame.image.load('images/puzzles/steam/steam_wall_3.png'),   # 3
    pygame.image.load('images/puzzles/steam/steam_wall_4.png'),   # 4
    pygame.image.load('images/puzzles/steam/steam_wall_5.png'),   # 5
    pygame.image.load('images/puzzles/steam/steam_wall_6.png'),   # 6
    pygame.image.load('images/puzzles/steam/steam_wall_7.png'),   # 7
    pygame.image.load('images/puzzles/steam/steam_wall_8.png'),   # 8
    pygame.image.load('images/puzzles/steam/steam_wall_9.png'),   # 9
    pygame.image.load('images/puzzles/steam/steam_wall_10.png'),  # 10
    pygame.image.load('images/puzzles/steam/steam_wall_11.png'),  # 11
    pygame.image.load('images/puzzles/steam/steam_wall_12.png'),  # 12
    pygame.image.load('images/puzzles/steam/steam_wall_13.png'),  # 13
    pygame.image.load('images/puzzles/steam/steam_wall_14.png'),  # 14
    pygame.image.load('images/puzzles/steam/steam_wall_15.png')   # 15
]
rick = [
    pygame.image.load('images/characters/Rick/idle/1i.png'),  # 1
    pygame.image.load('images/characters/Rick/idle/1i.png'),  # 2
    pygame.image.load('images/characters/Rick/idle/1i.png'),  # 3
    pygame.image.load('images/characters/Rick/idle/1i.png'),  # 4
    pygame.image.load('images/characters/Rick/idle/1i.png'),  # 5
    pygame.image.load('images/characters/Rick/idle/1i.png'),  # 6
    pygame.image.load('images/characters/Rick/idle/1i.png'),  # 7
    pygame.image.load('images/characters/Rick/idle/1i.png'),  # 8
    pygame.image.load('images/characters/Rick/idle/2i.png'),  # 9
    pygame.image.load('images/characters/Rick/idle/2i.png'),  # 10
    pygame.image.load('images/characters/Rick/idle/2i.png'),  # 11
    pygame.image.load('images/characters/Rick/idle/2i.png'),  # 12
    pygame.image.load('images/characters/Rick/idle/2i.png'),  # 13
    pygame.image.load('images/characters/Rick/idle/2i.png'),  # 14
    pygame.image.load('images/characters/Rick/idle/2i.png'),  # 15
]
