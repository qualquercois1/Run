import pygame
import config
import math

class Car:
    def __init__(self):
        self.position = config.TRACK_DIVISION // 2
        self.size_x = config.DIV_POS - 250
        self.size_y = 100
        self.color = config.RED
        self.y = config.GAME_HEIGHT - self.size_y - config.GAP
        self.points = 0
        self.update_coordinates()

    def update_coordinates(self):
        self.x = self.position * config.DIV_POS + (config.DIV_POS - self.size_x) // 2

    def move(self, direction):
        if direction == "RIGHT" and self.position != config.TRACK_DIVISION - 1:
            self.position += 1
        elif direction == "LEFT" and self.position > 0:
            self.position -= 1
        
        self.update_coordinates()

    def draw(self, surface):
        x = self.x
        y = self.y
        
        rect = pygame.Rect(x, y, self.size_x, self.size_y)
        pygame.draw.rect(surface, self.color, rect, border_radius=4)

    def get_inputs(self, obstacles):
        sensors = []

        for offset in [-1,0,1]:
            check = self.position + offset

            # Verifica se é parede
            if check < 0 or check >= config.TRACK_DIVISION:
                sensors.append(0.0) # 0 é perigo
                continue

            track_obstacles = [
                obs for obs in obstacles if obs.position == check and obs.y < self.y
            ]

            if not track_obstacles:
                sensors.append(1.0) # 1 é livre
            else:
                closest_obs = max(track_obstacles, key=lambda o: o.y)

                dist = self.y - (closest_obs.y + closest_obs.size_y)

                normalized_dist = dist / config.GAME_HEIGHT

                sensors.append(max(0.0, min(1.0, normalized_dist)))

        return sensors


class Obstacle:
    def __init__(self, position):
        self.size_x = config.DIV_POS - 150
        self.size_y = 100
        self.y = -self.size_y
        self.color = config.BLUE
        self.velocity = 20
        self.position = position

    def draw(self, surface):
        x = self.position * config.DIV_POS + (config.DIV_POS - self.size_x) // 2
        rect = pygame.Rect(x, self.y, self.size_x, self.size_y)
        pygame.draw.rect(surface, self.color, rect, border_radius=4)

    def move(self):
        self.y += self.velocity