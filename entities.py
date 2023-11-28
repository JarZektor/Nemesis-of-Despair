import objects
import schedule


class Entity:
    def __init__(self, x, y, sx, sy, entity_id, type, data=(0, 0)):
        super().__init__()
        if type == 'item':
            self.name = objects.items[entity_id][0]
        elif type == 'puzzle':
            self.name = objects.puzzles[entity_id][0]
        elif type == 'character' and (entity_id, data) in schedule.characters:
            self.name = schedule.characters[(entity_id, data)]
        else:
            self.name = -1
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.size_x = sx
        self.size_y = sy
        self.size = (self.size_x, self.size_y)


class AnimatedEntity(Entity):
    def __init__(self, speed, anim, anim_counter, x, y, sx, sy, entity_id, type, data=(0, 0)):
        super().__init__(x, y, sx, sy, entity_id, type, data)
        self.speed = speed
        self.anim = anim
        self.anim_counter = anim_counter

    def next_frame(self):
        self.anim += self.anim_counter
        if self.anim == 28:
            self.anim = 0


class Player(AnimatedEntity):
    def __init__(self, speed, anim, anim_counter, gx, gy, gz, x, y, sx, sy):
        super().__init__(speed, anim, anim_counter, x, y, sx, sy, (gx, gy, gz), 'player')
        self.global_x = gx
        self.global_y = gy
        self.global_z = gz
