import sqlite3
import pygame
import cv2
import json
from objects import inventory


def cut_scene_player(cut_scene_name, screen_size, sound_volume):
    cut_scene = cv2.VideoCapture(cut_scene_name + '4')
    cut_scene_win = pygame.display.set_mode((1280, 720))#, pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    success = True
    frame_count = int(cut_scene.get(cv2.CAP_PROP_FRAME_COUNT))
    sound = pygame.mixer.Sound(cut_scene_name + '3')
    sound.set_volume(sound_volume)
    sound.play()
    while success:
        clock.tick(60)
        success, image = cut_scene.read()
        if cut_scene.get(cv2.CAP_PROP_POS_FRAMES) == frame_count - 1:
            success = False
            pygame.display.set_mode(screen_size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                success = False
                sound.stop()
                pygame.display.set_mode(screen_size)
        cut_scene_win.blit(pygame.image.frombuffer(image.tobytes(), (1280, 720), "BGR"), (0, 0))
        pygame.display.update()



def lore_restart(TABLE: str):
    connection = sqlite3.connect('storyline.db')
    cursor = connection.cursor()

    cursor.execute(f"""UPDATE {TABLE} SET Activate=0 WHERE Activate=1""")
    cursor.execute(f"""UPDATE {TABLE} SET Activate=1 WHERE ID=1""")

    connection.commit()
    connection.close()

def quest_restart(TABLE: str):
    connection = sqlite3.connect('quest.db')
    cursor = connection.cursor()
    cursor.execute(f"""UPDATE {TABLE}_quest SET Enabled=1 WHERE Enabled=0""")
    connection.commit()
    connection.close()


def lore_fragment(TABLE: str, time) -> str:
    connection = sqlite3.connect('storyline.db')
    cursor = connection.cursor()

    id = cursor.execute(f"""SELECT ID FROM {TABLE} WHERE Activate=1""").fetchall()
    try:
        id = id[0][0] + 1
    except IndexError:
        connection.commit()
        connection.close()
        first = check_quest(TABLE + '_quest', time)
        second = check_quest(TABLE + '_quest', time)
        if first == second:
            return False
        return first

    cursor.execute(f"""UPDATE {TABLE} SET Activate=0 WHERE Activate=1""")
    cursor.execute(f"""UPDATE {TABLE} SET Activate=1 WHERE ID={id}""")
    text = cursor.execute(f"""SELECT Text FROM {TABLE} WHERE Activate=1""").fetchall()

    connection.commit()
    connection.close()

    if text[0][0] == -1:
        return (check_quest(TABLE + '_quest', time))

    if text:
        return text[0][0]

    return (check_quest(TABLE + '_quest', time))

def check_quest(TABLE: str, time):

    connection = sqlite3.connect('quest.db')
    cursor = connection.cursor()

    text = cursor.execute(f"""SELECT Enabled FROM {TABLE}""").fetchall()

    if set(text) == {(0,)}:
        return "Мне не о чем с тобой говорить"
    else:
        quest_id = cursor.execute(f"""SELECT MIN(ID) FROM {TABLE} WHERE Enabled=1""").fetchall()[0][0]
        cursor.execute(f"""UPDATE {TABLE} SET Enabled=0 WHERE ID={quest_id}""")

    text = cursor.execute(f"""SELECT Timer, Activate_time FROM {TABLE} WHERE ID={quest_id}""").fetchall()[0]
    if text[0] != 0 and time - text[1] > text[0]:
        connection.commit()
        connection.close()
        return 'Время - деньги. Не хочу иметь с тобой дел'

    text = cursor.execute(f"""SELECT Prime_item FROM {TABLE} WHERE ID={quest_id}""").fetchall()[0][0]
    text = json.loads(text)["response"]
    if text[0] != "пустота" and check_item_in_inventory(text):
        return "Нет вещи - проваливай"
    else:
        for item in text:
            inventory.remove(item)

    text = cursor.execute(f"""SELECT Text FROM {TABLE} WHERE ID={quest_id}""").fetchall()[0][0]

    connection.commit()
    connection.close()

    return text

def check_item_in_inventory(list_: list) -> bool:
    for item in list_:
        if item not in inventory:
            return True
    else:
        return False