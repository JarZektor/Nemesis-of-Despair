# Nemesis of Despair
Авторы проекта: Умнов Ярослав, Курдогло Александр

Nemesis of Despair - это квест с элементами повествования, в котором игроку предстоит разгадать все
тайны как прошлого главного героя, так и гигантского корабля Элинос.
В Nemesis of Despair игрок должен будет исследовать локации, разговаривать с персонажами и применять смекалку для
прохождения различных головоломок.
-----

## Управление:
- За ходьбу отвечают кнопки AD[ФВ]
- За взаимодействие с окружением отвечает кнопка E[У]
- За переключение предметов в инвентаре отвечает кнопка Q[Й]
- За подъём и спуск по лестнице отвечают кнопки WS[ЦЫ]
- За меню паузы отвечает кнопка ESC
- За переключение режима полного экрана отвечает кнопка F11
- За пропуск катсцены отвечает сочетание клавиш Alt+F4 (не шутка)
- За консоль отладки отвечает кнопка F1 (не работает с выключенной настройкой "Debug mode")
- За тестовую отрисовку катсцен отвечает кнопка F2 (не работает с выключенной настройкой "Debug mode")
- За переключение отрисовки интерфейса отладки отвечает кнопка F3 (не работает с выключенной настройкой "Debug mode")
-----

## Локации:
Корабль Элинос разделён на 3 секции, а именно: командную, пассажирскую и техническую - и в общей сумме насчитывает около 170 комнат/экранов
-----

## Необходимые библиотеки:
1. pygame
2. random
3. sqlite3
4. cv2
5. json
6. re
-----

## Окна игры:
1. Окно настроек
2. Окно игры
3. Окно с катсценами
-----

## Классы:
1. Entity - Объект с размерами и местоположением
2. AnimatedEntity(Entity) - то же самое, что и Entity, но содержит функцию, позволяющую производить отсчёт от 0 до 28 для привязки смены кадров анимаций к счётчику
3. Player(AnimatedEntity) - то же самое, что и AnimatedEntity, но также хранит в себе глобальные координаты и скорость
-----

## Функции игры:
1. Передвижение по локальным и глобальным координатам
2. Проигрывание анимаций для различных анимированных сущностей
3. Пропорциональное изменение спрайтов, коллайдеров, координат от размера окна игры
4. Режим полного экрана
5. Возможность изменения окна игры через изменение переменной
6. Взаимодействие с окружением
7. Возможность подбора предметов в инвентарь
8. Воспроизведение звуков при практически всех доступных игровых действиях
9. Воспроизведение звуков при всех доступных игровых действиях
10. Проигрывание фоновой музыки
11. Система противодействия выходу за игровое поле, доступное игроку
12. Отрисовка интерфейса отладки
13. Воспроизведение катсцен
14. Консоль отладки
15. Карта корабля в меню паузы
16. Достижения(в планах)

## Геймплейный тизер игры: https://youtu.be/e9ZuslQLjII
## Консоль с включенным интерфейсом отладки
![Консоль с включенным интерфейсом отладки](https://github.com/JarZektor/Nemesis-of-Despair/blob/master/Screenshot_60.png)
## Взаимодействие с головоломками
![Взаимодействие с головоломками](https://github.com/JarZektor/Nemesis-of-Despair/blob/master/Screenshot_61.png)
## Разговоры с другими персонажами
![Разговоры с другими персонажами](https://github.com/JarZektor/Nemesis-of-Despair/blob/master/Screenshot_62.png)
