import sqlite3


# Передеётся имя объекта с которым перс взаимодействует
def lore_fragment(TABLE: str) -> str:
    connection = sqlite3.connect('storyline.db')
    cursor = connection.cursor()

    id = cursor.execute(f"""SELECT ID FROM {TABLE} WHERE Activate=1""").fetchall()
    try:
        id = id[0][0] + 1
    except IndexError:
        connection.commit()
        connection.close()
        return 'Мы закончили разговор'

    cursor.execute(f"""UPDATE {TABLE} SET Activate=0 WHERE Activate=1""")
    cursor.execute(f"""UPDATE {TABLE} SET Activate=1 WHERE ID={id}""")
    text = cursor.execute(f"""SELECT Text FROM {TABLE} WHERE Activate=1""").fetchall()

    connection.commit()
    connection.close()

    if text:
        return text[0][0]
    return ''
