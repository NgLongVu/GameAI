import pygame
import math
import os
from utils.constants import LERP_SPEED, WINDOW_WIDTH, WINDOW_HEIGHT

ICON_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icons')

class Entity:
    def __init__(self, start_node, color=(0,0,0), image_file=None, radius=20):
        self.current_node = start_node
        self.target_node = start_node
        self.visual_x = float(start_node.x)
        self.visual_y = float(start_node.y)
        self.color = color
        self.radius = radius
        self.idle_timer = 0
        
        self.image = None
        if image_file:
            path = os.path.join(ICON_DIR, image_file)
            if os.path.exists(path):
                # Load once
                raw_img = pygame.image.load(path).convert_alpha()
                # Use a higher quality scaling method (rotozoom with scale factor)
                target_size = self.radius * 2
                current_size = raw_img.get_width()
                scale_factor = target_size / current_size
                self.image = pygame.transform.rotozoom(raw_img, 0, scale_factor)

    def move_to(self, node):
        self.current_node = node
        self.target_node = node

    def is_animating(self):
        dx = abs(self.visual_x - self.target_node.x)
        dy = abs(self.visual_y - self.target_node.y)
        return dx > 1.0 or dy > 1.0

    def update(self):
        """LERP to target node"""
        self.visual_x += (self.target_node.x - self.visual_x) * LERP_SPEED
        self.visual_y += (self.target_node.y - self.visual_y) * LERP_SPEED

    def draw(self, screen):
        ix, iy = int(self.visual_x), int(self.visual_y)
        
        if self.image:
            rect = self.image.get_rect(center=(ix, iy))
            screen.blit(self.image, rect)
        else:
            pygame.draw.circle(screen, self.color, (ix, iy), self.radius)
            pygame.draw.circle(screen, (0, 0, 0), (ix, iy), self.radius, 2)

class Police(Entity):
    def __init__(self, start_node):
        super().__init__(start_node, color=(20, 40, 100), image_file='police.png', radius=48)

class Thief(Entity):
    def __init__(self, start_node):
        super().__init__(start_node, color=(80, 80, 80), image_file='thief.png', radius=48)

    def is_at_exit(self):
        return self.current_node.type == 'exit'
