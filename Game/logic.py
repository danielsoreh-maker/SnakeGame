import random


class SnakeGame:

    def __init__(self, window_size, block_size):
        self.window_size = window_size
        self.block_size = block_size

        # Čūskas sākuma pozīcija un ķermenis
        self.snake_body = [
            [100, 50],
            [75, 50],
            [50, 50],
        ]
        self.direction = "RIGHT"
        self.change_to = self.direction

        # Punkti un ātrums
        self.score = 0
        self.current_speed = 7

        #Energy līmenis matrix funkcijai
        self.energy = 100
        self.is_matrix_active = False

        # Ābols un superābols
        self.is_super_fruit = False
        self.fruit_position = [300, 300]

    def activate_matrix_effect(self):
        if self.energy > 0:
            self.is_matrix_active = not self.is_matrix_active


    def update(self):
        if self.change_to == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        if self.change_to == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        if self.change_to == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        if self.change_to == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

        # Pārvietojam galvu
        head_x, head_y = self.snake_body[0]
        if self.direction == "UP":
            head_y -= self.block_size
        elif self.direction == "DOWN":
            head_y += self.block_size
        elif self.direction == "LEFT":
            head_x -= self.block_size
        elif self.direction == "RIGHT":
            head_x += self.block_size

        # Pārbaudām, vai nav ietriecies sienā
        if (
            head_x < 0
            or head_x >= self.window_size
            or head_y < 0
            or head_y >= self.window_size
            or [head_x, head_y]
            in self.snake_body[:-1]
        ):
            return False  # Spēle beigusies!

        # Pievienojam jaunu galvu
        self.snake_body.insert(0, [head_x, head_y])

        # Pārbaudām, vai čūska apēda ābolu
        if [head_x, head_y] == self.fruit_position:
            if self.is_super_fruit:
                self.score += 150
            else:
                self.score += 10
            # Sarežģītības līmeņa regulēšana atkarībā no punktiem
            if self.score in [150, 300, 450, 600, 750]:
                self.current_speed += 1 # Ātruma mainīšana
            # Uzģenerējam jaunu ābolu nejaušā vietā uz režģim atbilstošām koordinātām
            while True:
                new_fruit = [
                    random.randrange(0, self.window_size // self.block_size)
                    * self.block_size,
                    random.randrange(0, self.window_size // self.block_size)
                    * self.block_size,
                ]
                if new_fruit not in self.snake_body:
                    self.fruit_position = new_fruit
                    break
            
            self.is_super_fruit = random.random() < 0.05    
        else:
            # Ja neapēda, noņemam asti (saglabājam garumu)
            self.snake_body.pop()
        if self.is_matrix_active:
            self.energy -= 4  # Tērējam enerģiju
            if self.energy <= 0:
                self.energy = 0
                self.is_matrix_active = False
        else:
            if self.energy < 100:
                self.energy += 1  # Lēnām atjaunojam enerģiju, kad nelieto

        return True  # Viss kārtībā, spēle turpinās