import os
import time, vlc
import win32gui
import sqlite3


os.add_dll_directory('C:\Program Files\VideoLAN\VLC') 


def vlc_video(src, k): 
    vlcplayer = vlc.MediaPlayer()
    vlcplayer.set_media(vlc.Media(src))

    vlcplayer.play()
    vlcplayer.video_set_scale(k)
    time.sleep(0.05)
    while vlcplayer.is_playing():
        pass
    
# vlc_video("cutscenes/start cutscene_1.mp4", 0.3)

def lore_restart(TABLE: str):
    connection = sqlite3.connect('storyline.db')
    cursor = connection.cursor()

    cursor.execute(f"""UPDATE {TABLE} SET Activate=0 WHERE Activate=1""")
    cursor.execute(f"""UPDATE {TABLE} SET Activate=1 WHERE ID=1""")

    connection.commit()
    connection.close()


def lore_fragment(TABLE: str) -> str:
    connection = sqlite3.connect('storyline.db')
    cursor = connection.cursor()

    id = cursor.execute(f"""SELECT ID FROM {TABLE} WHERE Activate=1""").fetchall()
    try:
        id = id[0][0] + 1
    except IndexError:
        connection.commit()
        connection.close()
        return False

    cursor.execute(f"""UPDATE {TABLE} SET Activate=0 WHERE Activate=1""")
    cursor.execute(f"""UPDATE {TABLE} SET Activate=1 WHERE ID={id}""")
    text = cursor.execute(f"""SELECT Text FROM {TABLE} WHERE Activate=1""").fetchall()

    connection.commit()
    connection.close()

    if text:
        return text[0][0]
    return ''