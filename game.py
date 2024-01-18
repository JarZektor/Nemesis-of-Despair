import pygame
import random
import json
import re

import animations
import entities
import sounds
import objects
import schedule
from utility import lore_fragment, lore_restart, cut_scene_player, quest_restart
from entities import  Entity, AnimatedEntity, Player


# консоль
checklist = ["get_inventory", "add_tick \'number\'", "set_time \'d:hh:mm\'", "teleport \'x*y\'", "help"]
def print_hint(user_text):
    hint = []
    for i in checklist:
        if user_text in i:
            hint.append(i)
    if not hint:
        hint.append("unresorved referense")
    return hint

def get_help(var=''):
    return checklist

def get_inventory(var=""):
    return objects.inventory

def add_tick(tick_player):
    return int(tick_player)

def set_time(string_data):
    p = re.compile('[0-9]{1}:[0-9]{2}:[0-9]{2}')
    if p.match(string_data):
        hour = (int(string_data[0]) - 1) * 24
        minute = (int(string_data[2:4]) + hour) * 60
        time = (int(string_data[5:]) + minute) * 60
        return time

def teleport(coordinate):
    x, y = coordinate.split('*')[0], coordinate.split('*')[1]
    return (int(x), int(y))

get_command = {
"help": get_help,
"get_inventory": get_inventory,
"add_tick": add_tick, 
"set_time": set_time,
"teleport": teleport
}

def console_input(final_text):
    try:
        command = final_text.split()[0]
    except:
        command = help
    if len(final_text.split()) > 1:
        var = final_text.split()[1]
    else:
        var = ''
    try:
        (get_command[command](var), command)
    except:
        command = "help"
    return (get_command[command](var), command)


# стартовая настройка игры
def start():
    lore_restart('story')
    lore_restart('Рик')
    quest_restart('Рик')

    with open("values.json", "r") as file:
        data = json.load(file)['object_value']

    pygame.init()
    screen_size = []
    for i in data[2].split('x'):
        screen_size.append(int(i))
    setup_screen_width = screen_size[0]
    setup_screen_height = screen_size[1]
    screen_width = setup_screen_width
    screen_height = setup_screen_height

    # коэфициент для разных разрешений так как разработка идёт на разрешении 800x450px
    k = setup_screen_height / 450  # НЕ МЕНЯТЬ!!!

    fullscreen = data[0]
    fullscreen_error = False
    if tuple(screen_size) in [(800, 450), (960, 540)]:
        fullscreen = False
    if fullscreen:
        screen = pygame.display.set_mode((screen_width, screen_height), flags=pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Nemesis of Despair')
    pygame.display.set_icon(pygame.image.load('images/icon.png'))
    clock = pygame.time.Clock()

    action_font = pygame.font.Font('fonts/RookiePunk.ttf', int(28 * k))
    dialogue_font = pygame.font.Font('fonts/RookiePunk.ttf', int(28 * k))
    debug_font = pygame.font.Font('fonts/RookiePunk.ttf', int(16 * k))
    glitch_font = pygame.font.Font('fonts/RubikGlitch-Regular.ttf', int(20 * k))

    music_volume = data[4] / 100 * data[6] / 100 # music_volume% * master_volume%
    sound_volume = data[5] / 100 * data[6] / 100

    bg_music = random.choice(sounds.bg_melodies)
    bg_music.play()
    bg_music.set_volume(music_volume)

    sound = sounds.sound['fail']
    sound.set_volume(sound_volume)

    footstep = sounds.sound['footstep']
    footstep.set_volume(sound_volume)

    selected = 0
    footstep_timer = -1
    can_move_up = False
    can_move_down = False
    can_enter = False
    can_pickup = False
    glitch_bounds = False
    pause = False
    dialogue = False
    cutscene = False
    debug_render = False
    debug_console = False
    console_text = ''
    text_output = ['']
    debug = data[1]

    # цифра перед * k - это размер объекта по x при разрешении 800x450px
    usage = 50 * k
    ladder_side = 200 * k
    door_size = 150 * k

    global_anim = 0
    anim_counter = 2
    time_counter = 2
    now_time = -2
    minute = now_time // 60 % 60
    hour = now_time // 3600 % 24
    day = now_time // 86400 + 1
    puzzle = AnimatedEntity(0, anim_counter, -1, -1, 1, 1, -1, -1)
    puzzle_render = objects.puzzles_renders[puzzle.name]
    character = AnimatedEntity(0, anim_counter, -1, -1, 1, 1, -1, -1)
    character_render = objects.character_renders[character.name]
    player = Player(k * 5, 0, anim_counter, 0, 0, 0, 100 * k, 100 * k, 100 * k, 350 * k)

    player.global_x = 22
    player.global_y = 8
    player.global_z = False  # == 1 только в специальных комнатах

    fps = int(data[3][:2])  # можно изменять в настройках, варианты: 30, 60
    if fps == 60:
        player.speed //= 2
        player.anim_counter = 1
        anim_counter = 1
        time_counter = 1

    while True:
        screen_width = pygame.display.Info().current_w
        screen_height = pygame.display.Info().current_h
        screen_size = (screen_width, screen_height)
        global_xy = (player.global_x, player.global_y)
        global_xyz = (player.global_x, player.global_y, player.global_z)
        if not pause:
            minute = now_time // 60 % 60
            hour = now_time // 3600 % 24
            day = now_time // 86400 + 1
            data = (day, hour)
            footstep.set_volume(sound_volume)
            sound.set_volume(sound_volume)
            now_time += time_counter
            clock.tick(fps)
        footstep_timer -= anim_counter
        if footstep_timer == 0:
            footstep.stop()
        if not pygame.mixer.get_busy():
            bg_music = random.choice(sounds.bg_melodies)
            bg_music.set_volume(music_volume)
            bg_music.play()
        if now_time in objects.cutscenes:
            bg_music.set_volume(0)
            pause = True
            cut_scene_player(objects.cutscenes[now_time], screen_size, sound_volume)
            bg_music.set_volume(music_volume)
            pause = False

        try:
            screen.blit(pygame.transform.scale(pygame.image.load(f'images/backgrounds/X{player.global_x}Y{player.global_y}Z{int(player.global_z)}.png'), screen_size), (0, 0))
        except FileNotFoundError:
            player.global_x = 22
            player.global_y = 8
            player.global_z = 0
            screen.blit(pygame.transform.scale(pygame.image.load(f'images/backgrounds/X{player.global_x}Y{player.global_y}Z{int(player.global_z)}.png'), screen_size), (0, 0))
            glitch_bounds = True

        if glitch_bounds:
            screen.blit(glitch_font.render('Я, кажется, сломал реальность', False, 'Red'), (0, screen_height - 60 * k))
            screen.blit(glitch_font.render('и вышел за её пределы,', False, 'Red'), (0, screen_height - 40 * k))
            screen.blit(glitch_font.render('не стоит мне так больше делать', False, 'Red'), (0, screen_height - 20 * k))
        if (player.global_x, player.global_y, player.global_z) != (22, 8, 0):
            glitch_bounds = False

        # предметы взаимодействие и отрисовка
        if global_xyz in objects.items:
            item = objects.items[global_xyz]
            item = Entity(item[3], item[4], item[1], item[2], global_xyz, 'item')
            screen.blit(pygame.transform.scale(pygame.image.load(f'images/items/{item.name}.png'), (item.size_x * k, item.size_y * k)), (item.x * k, item.y * k))
        else:
            item = Entity(-99, -99, -99, -99, -99, -99)  # создаём фантомный объект за пределами экрана для избежания поломок
        if item.x - usage < player.x < item.x + item.size_x + usage:
            screen.blit(action_font.render('нажмите E для подбора', False, 'Red'), (player.x + 60, player.y - 20))
            can_pickup = True
        else:
            can_pickup = False

        keys = pygame.key.get_pressed()

        # анимации
        if global_anim == 28:
            global_anim = 0
        elif not pause:
            global_anim += anim_counter
            player.next_frame()
            puzzle.next_frame()
            character.next_frame()
        screen.blit(pygame.transform.scale(puzzle_render[puzzle.anim // 2], puzzle.size), (puzzle.x, puzzle.y))

        screen.blit(pygame.transform.scale(character_render[character.anim // 2], character.size), (character.x + usage, character.y))


        if keys[pygame.K_a] and not pause:
            screen.blit(pygame.transform.scale(animations.player_move_left[player.anim // 2], player.size), (player.x, player.y))
        elif keys[pygame.K_d] and not pause:
            screen.blit(pygame.transform.scale(animations.player_move_right[player.anim // 2], player.size), (player.x, player.y))
        else:
            screen.blit(pygame.transform.scale(animations.player_idle[player.anim // 2], player.size), (player.x, player.y))

        # головоломки
        if global_xyz in objects.puzzles:
            if puzzle.name == -1:
                puzzle = objects.puzzles[global_xyz]
                puzzle = entities.AnimatedEntity(0, anim_counter, puzzle[3] * k, puzzle[4] * k, puzzle[1] * k, puzzle[2] * k, global_xyz, 'puzzle')
                puzzle_render = objects.puzzles_renders[puzzle.name]
        else:
            puzzle = AnimatedEntity(0, anim_counter, -999, -999, 1, 1, -1, -1)
            puzzle_render = objects.puzzles_renders[puzzle.name]
        if puzzle.x - usage < player.x < puzzle.x + puzzle.size_x + usage:
            screen.blit(action_font.render('нажмите E для взаимодействия', False, 'Red'), (player.x + 60, player.y - 20))
            can_use = True
        else:
            can_use = False

        # персонажи
        cords_data = (global_xyz, data)
        if cords_data in schedule.characters:
            if character.name == -1:
                character = objects.characters[schedule.characters[cords_data]]
                character = entities.AnimatedEntity(0, anim_counter, character[3] * k, character[4] * k, character[1] * k, character[2] * k, global_xyz, 'character', data)
                character_render = objects.character_renders[character.name]
        else:
            character = AnimatedEntity(0, anim_counter, -999, -999, 1, 1, -1, -1)
            character_render = objects.character_renders[character.name]
        if character.x - usage < player.x < character.x + character.size_x + usage:
            screen.blit(action_font.render('нажмите E для взаимодействия', False, 'Red'), (player.x + 60, player.y - 20))
            can_interact = True
        else:
            can_interact = False

        # кнопки передвижения
        if keys[pygame.K_a] and player.x > 0 and (
                player.x < puzzle.x + 10 or player.x > puzzle.x + puzzle.size_x) and not pause:
            player.x -= player.speed
            footstep_timer = -1
        if keys[pygame.K_d] and player.x < screen_width - player.size_x and (player.x < puzzle.x or player.x > puzzle.x + puzzle.size_x - 10) and not pause:
            player.x += player.speed
            footstep_timer = -1

        # перемещение по глобальному X
        if player.x < 20 * k and not ((player.global_x - 1, player.global_y) in objects.impasses) and not player.global_z:
            player.global_x -= 1
            player.x = screen_width - screen_width // 8 - player.size_x
        if player.x > screen_width - player.size_x - 20 * k and not ((player.global_x + 1, player.global_y) in objects.impasses) and not player.global_z:
            player.global_x += 1
            player.x = 100 * k

        # перемещение по глобальным Y
        if (screen_width - ladder_side) < player.x * 2 < (screen_width + ladder_side) and global_xy in objects.ladders_up:
            screen.blit(action_font.render('нажмите W для подъёма', False, 'Red'), (player.x + 60, player.y - 20))
            can_move_up = True
        else:
            can_move_up = False
        if (screen_width - ladder_side) < player.x * 2 < (screen_width + ladder_side) and global_xy in objects.ladders_down:
            screen.blit(action_font.render('нажмите S для спуска', False, 'Red'), (player.x + 60, player.y - 20))
            can_move_down = True
        else:
            can_move_down = False

        # перемещение по глобальным Z
        if (screen_width - door_size) < player.x * 2 < (screen_width + door_size) and global_xy in objects.doors:
            screen.blit(action_font.render('нажмите E для входа', False, 'Red'), (player.x + 60, player.y - 20))
            can_enter = True
        else:
            can_enter = False

        if dialogue:
            screen.blit(pygame.transform.scale(pygame.image.load(f'images/dialogues/Игрок.png'), (100 * k, 100 * k)), (0, 350 * k))
            screen.blit(pygame.transform.scale(pygame.image.load(f'images/dialogues/Фон.png'), (600 * k, 100 * k)), (100 * k, 350 * k))
            screen.blit(pygame.transform.scale(pygame.image.load(f'images/dialogues/{character.name}.png'), (100 * k, 100 * k)), (700 * k, 350 * k))
            screen.blit(dialogue_font.render(phrase, False, 'Red'), (110 * k, 360 * k))

        # дебаг отрисовка
        if debug:
            all_sprites = pygame.sprite.Group()
            debug_sprite = pygame.sprite.Sprite()
            debug_sprite.image = pygame.transform.scale(pygame.image.load("images/UI/debug.jpg"), (80 * k, 80 * k))
            debug_sprite.rect = debug_sprite.image.get_rect()
            debug_sprite.rect.x = int(screen_width - 280 * k)
            debug_sprite.rect.y = 0
            all_sprites.add(debug_sprite)
            all_sprites.draw(screen)
        if debug_render:
            screen.blit(debug_font.render(f'Room: X{player.global_x} Y{player.global_y} Z{int(player.global_z)}', False, 'Black'), (0, 0))
            screen.blit(debug_font.render(f'Player: X{round(player.x, 2)} Y{player.y}', False, 'Black'), (0, debug_font.get_height()))
            screen.blit(debug_font.render(f'Screen: X{screen_width} Y{screen_height} k {k} fullscreen {fullscreen}', False, 'Black'), (0, 2 * debug_font.get_height()))
            screen.blit(debug_font.render(f'Time: d{day} h{hour} m{minute} tick {now_time}',  False, 'Black'), (0, 3 * debug_font.get_height()))
            screen.blit(debug_font.render(f'Glitch: {glitch_bounds}', False, 'Black'), (0, 6 * debug_font.get_height()))
            screen.blit(debug_font.render(f'Music volume: {music_volume}', False, 'Black'), (0, 5 * debug_font.get_height()))
            screen.blit(debug_font.render(f'Sounds volume: {sound_volume}', False, 'Black'), (0, 4 * debug_font.get_height()))
            screen.blit(debug_font.render(f'Inventory item: {objects.inventory[selected]}', False, 'Black'), (0, 7 * debug_font.get_height()))
            screen.blit(debug_font.render(f'Puzzle: {puzzle.name}', False, 'Black'), (0, 8 * debug_font.get_height()))
            screen.blit(debug_font.render(f'Character: {character.name}', False, 'Black'), (0, 9 * debug_font.get_height()))
        if debug_console:
            hint = print_hint(console_text)
            screen.blit(pygame.transform.scale(pygame.image.load('images/UI/console.png'), (700 * k, 150 * k)), (0, 300 * k))
            screen.blit(debug_font.render(f'{console_text}', False, 'Black'), (0, screen_height - 10 - debug_font.get_height()))
            for h in range(len(hint)):
                screen.blit(debug_font.render(f'{hint[h]}', False, 'Black'), (0, screen_height - 10 - (2+h) * debug_font.get_height()))
            for t in range(len(text_output)):
                screen.blit(debug_font.render(f'{text_output[t]}', False, 'Black'), (200*k, screen_height - 10 - (2+t) * debug_font.get_height()))


        # отрисовка интерфейса
        if fullscreen_error:
            screen.blit(debug_font.render(f'При данном разрешении режим полного экрана не работает', False, 'Black'), (0, 0))
            screen.blit(debug_font.render(f'Нажмите на F11 ещё раз для скрытия надписи', False, 'Black'), (0, debug_font.get_height()))
        screen.blit(pygame.transform.scale(pygame.image.load(f'images/UI/clock/{hour}.png'), (80 * k, 80 * k)), (screen_width - 180 * k, 0))
        screen.blit(pygame.transform.scale(pygame.image.load(f'images/UI/inventory.png'), (80 * k, 80 * k)), (screen_width - 80 * k, 0))
        try:
            screen.blit(pygame.transform.scale(pygame.image.load(f'images/items/{objects.inventory[selected]}.png'), (50 * k, 50 * k)), (screen_width - 65 * k, 15 * k))
        except:
            selected = 0
        # экран паузы
        if pause and not dialogue and not cutscene and not debug_console:
            screen.blit(pygame.transform.scale(pygame.image.load(f'images/UI/pause_screen.png'), screen_size), (0, 0))
            screen.blit(pygame.transform.scale(pygame.image.load(f'images/UI/map.png'), (700 * k, 250 * k)), (50 * k, 81 * k))
            screen.blit(pygame.transform.scale(pygame.image.load(f'images/UI/player_icon.png'), (18 * k, 18 * k)), ((50 + player.global_x * 25) * k, (313 - player.global_y * 17) * k))

        pygame.display.update()
        # прочее и кнопки действия
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    footstep_timer = 10
            if event.type == pygame.KEYDOWN and not pause:
                if event.key == pygame.K_e and can_enter:
                    player.global_z = not player.global_z
                    sound = sounds.sound['door']
                    sound.play()
                if event.key == pygame.K_e and can_pickup:
                    objects.inventory.append(objects.items[global_xyz][0])
                    objects.items.pop(global_xyz)
                    sound = sounds.sound['pickup']
                    sound.play()
                if event.key == pygame.K_e and can_use:
                    if puzzle.name == objects.inventory[selected]:
                        objects.puzzles.pop(global_xyz)
                        objects.inventory.remove(objects.inventory[selected])
                        selected -= 1
                        sound = sounds.sound['success']
                        sound.play()
                    else:
                        sound = sounds.sound['fail']
                        sound.play()
                if event.key == pygame.K_e and can_interact:
                    pause = True
                    dialogue = True

                if event.key == pygame.K_q:
                    selected += 1
                    if selected + 1 > len(objects.inventory):
                        selected = 0
                if event.key == pygame.K_w and can_move_up:
                    sound = sounds.sound['ladder']
                    sound.play()
                    player.global_y += 1
                if event.key == pygame.K_s and can_move_down:
                    sound = sounds.sound['ladder']
                    sound.play()
                    player.global_y -= 1
                if event.key == pygame.K_d:
                    player.anim = 0
                    footstep.stop()
                    footstep.play(loops=-1)
                if event.key == pygame.K_a:
                    player.anim = 0
                    footstep.stop()
                    footstep.play(loops=-1)
            if event.type == pygame.KEYDOWN:
                if dialogue:
                    phrase = lore_fragment(character.name, now_time)
                    if not phrase:
                        pause = False
                        dialogue = False

                if event.key == pygame.K_F11:
                    if screen_size in [(1280, 720), (1920, 1080)]:
                        fullscreen = not fullscreen
                    else:
                        fullscreen_error = not fullscreen_error
                    if fullscreen:
                        screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((setup_screen_width, setup_screen_height))
                    player.y = 100 * k
                if event.key == pygame.K_ESCAPE and not dialogue:
                    pause = not pause
                if debug:
                    if event.key == pygame.K_F1 and debug:
                        debug_console = not debug_console
                        pause = not pause
                    if event.key == pygame.K_F2 and debug:
                        bg_music.set_volume(0)
                        pause = True
                        cut_scene_player("cutscenes/start cutscene.mp", screen_size, sound_volume)
                        bg_music.set_volume(music_volume)
                        pause = False
                    if event.key == pygame.K_F3 and debug:
                        debug_render = not debug_render
                    if debug_console:
                        if event.key == pygame.K_RETURN:
                            console_output = console_input(console_text)
                            text = console_output[1]
                            if text == "set_time":
                                if console_output[0]:
                                    now_time = console_output[0]
                            elif text == "add_tick":
                                now_time += console_output[0]
                            elif text == "teleport":
                                player.global_x, player.global_y = console_output[0]
                            elif text == "get_inventory" or text == "help":
                                text_output = console_output[0]
                            console_text = ''
                        elif event.key == pygame.K_ESCAPE:
                            debug_console = False
                        elif event.key == pygame.K_BACKSPACE:
                            console_text = console_text[:-1]
                        else:
                            console_text += event.unicode
