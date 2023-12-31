import animations

cutscenes = {
    'tick': 'cutscene name',
    0: 'cutscenes/start cutscene.mp'
}
ladders_up = [
    (1, 0)
]
ladders_down = [
    (1, 1)
]
doors = [
    (0, 0),
    (3, 0)
]
impasses = [
    (-1, 5),
    (-1, 4),
    (-1, 3),
    (-1, 2),
    (-1, 1), (2, 1),
    (-1, 0), (4, 0),
    (-1, -1),
    (-1, -2),
    (-1, -3),
    (-1, -4),
    (-1, -5)
]
items = {
    (-1, -1, -1): ['название', 'sx', 'sy', 'x', 'y'],
    (0, 0, 1): ['тестовый_предмет', 150, 150, 100, 200],
    (2, 0, 0): ['тестовый_предмет1', 150, 150, 100, 200]
}
inventory = ['1r', 'вентиль']
puzzles = {
    (-1, -1, -1): ['название', 'sx', 'sy', 'x', 'y'],
    (2, 0, 0): ['вентиль', 200, 400, 300, 50]
}
puzzles_renders = {
    -1: animations.empty_render,
    'вентиль': animations.steam
}
characters = {
    'имя': ('название','sx','sy','x','y'),
    'Рик': ('Рик', 200, 400, 600, 50)
}
character_renders = {
    -1: animations.empty_render,
    'Рик': animations.rick
}

