import sqlite3
from objects import inventory
import json


def check_quest(TABLE: str):
    # В ооп просто используй self.clock
    time_now = 4

    connection = sqlite3.connect('quest.db')
    cursor = connection.cursor()

    text = cursor.execute(f"""SELECT Enabled FROM {TABLE}""").fetchall()

    if set(text) == {(0,)}:
        return "Мне не о чем с тобой говорить"
    else:
        quest_id = cursor.execute(f"""SELECT MIN(ID) FROM {TABLE} WHERE Enabled=1""").fetchall()[0][0]
        cursor.execute(f"""UPDATE {TABLE} SET Enabled=0 WHERE ID={quest_id}""")

    text = cursor.execute(f"""SELECT Timer, Activate_time FROM {TABLE} WHERE ID={quest_id}""").fetchall()[0]
    if text[0] != 0 and time_now - text[1] > text[0]:
        connection.commit()
        connection.close()
        return 'Время - деньги. Не хочу иметь с тобой дел'

    text = cursor.execute(f"""SELECT Prime_item FROM {TABLE} WHERE ID={quest_id}""").fetchall()[0][0]
    text = json.loads(text)["response"]
    if text[0] != "пустота" and check_item_in_inventory(text):
        return "Нет вещи - проваливай"

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


npc_name = ''
print(check_quest(npc_name + '_quest'))
print(check_quest(npc_name + '_quest'))
