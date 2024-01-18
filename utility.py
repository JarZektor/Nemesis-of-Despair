import sqlite3
import pygame
import cv2
import json
from objects import inventory


def cut_scene_player(cut_scene_name, screen_size, sound_volume):
    cut_scene = cv2.VideoCapture(cut_scene_name + '4')
    cut_scene_win = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
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


def lore_fragment(TABLE: str, time):
    connection2 = sqlite3.connect('quest.db')
    cursor2 = connection2.cursor()

    flag1 = set(cursor2.execute(f"""SELECT Enabled FROM {TABLE + '_quest'}""").fetchall()) != {(0,)}
    quest_id = cursor2.execute(f"""SELECT MIN(ID) FROM {TABLE + '_quest'} WHERE Enabled=1""").fetchall()[0][0]

    text2 = cursor2.execute(f"""SELECT Prime_item FROM {TABLE + '_quest'} WHERE ID={quest_id}""").fetchall()[0][0]
    text2 = json.loads(text2)["response"]
    flag2 = (text2[0] != "пустота" and check_item_in_inventory(text2)) or text2[0] == "пустота"

    connection = sqlite3.connect('storyline.db')
    cursor = connection.cursor()

    id = cursor.execute(f"""SELECT ID FROM {TABLE} WHERE Activate=1""").fetchall()

    try:
        id = id[0][0] + 1
    except IndexError:
        return False

    cursor.execute(f"""UPDATE {TABLE} SET Activate=0 WHERE Activate=1""")
    cursor.execute(f"""UPDATE {TABLE} SET Activate=1 WHERE ID={id}""")
    connection.commit()

    try:
        text = cursor.execute(f"""SELECT Text FROM {TABLE} WHERE Activate=1""").fetchall()[0][0]
    except IndexError:
        connection.close()
        connection2.close()
        return False

    if flag1 and flag2:
        if text == '-2':
            text = cursor2.execute(f"""SELECT Text FROM {TABLE + '_quest'} WHERE ID={quest_id}""").fetchall()[0][0]
            connection.close()
            connection2.close()
            return text
        connection.close()
        connection2.close()
        return text
    else:
        if text == '-2':
            cursor.execute(f"""UPDATE {TABLE} SET Activate=0 WHERE Activate=1""")
            cursor.execute(f"""UPDATE {TABLE} SET Activate=1 WHERE ID={id - 1}""")
            connection.commit()
            connection.close()
            connection2.close()
            return False
        connection.close()
        connection2.close()
        return text


def check_item_in_inventory(list_: list) -> bool:
    for item in list_:
        if not (item in inventory):
            return False
    return True