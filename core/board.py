import json
import os
import pygame
import utils.constants as const

IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'images')

class Node:
    def __init__(self, id, x, y, node_type="normal"):
        self.id = id
        self.x = x
        self.y = y
        self.type = node_type
        self.neighbors = []

    def draw(self, screen, is_highlighted=False):
        color = const.NODE_COLOR
        if is_highlighted:
            color = (255, 255, 100)
            
        shadow_offset = 4
        shadow_color = (40, 40, 40)
            
        if self.type == "exit":
            # Draw shadow
            shadow_rect = pygame.Rect(self.x - const.EXIT_SIZE//2, self.y - const.EXIT_SIZE//2 + shadow_offset, const.EXIT_SIZE, const.EXIT_SIZE)
            pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=8)
            
            # Draw square for exit nodes
            rect = pygame.Rect(self.x - const.EXIT_SIZE//2, self.y - const.EXIT_SIZE//2, const.EXIT_SIZE, const.EXIT_SIZE)
            pygame.draw.rect(screen, const.EXIT_COLOR, rect, border_radius=8)
            pygame.draw.rect(screen, const.EXIT_FILL, rect.inflate(-8, -8), border_radius=4)
            pygame.draw.rect(screen, (0, 0, 0), rect, width=3, border_radius=8)
        else:
            # Draw shadow
            pygame.draw.circle(screen, shadow_color, (self.x, self.y + shadow_offset), const.NODE_RADIUS)
            
            # Draw circle for normal nodes (as seen in image)
            pygame.draw.circle(screen, color, (self.x, self.y), const.NODE_RADIUS)
            pygame.draw.circle(screen, const.NODE_BORDER_COLOR, (self.x, self.y), const.NODE_RADIUS, width=3)

class Board:
    def __init__(self, map_path):
        self.nodes = {}
        self.edges = []
        self.start_thief = None
        self.start_police = []
        self.bg_image = None
        self._load_map(map_path)
        self._normalize_map_coordinates()
        
        # Load background image
        bg_path = os.path.join(IMAGES_DIR, 'bg_game.png')
        if os.path.exists(bg_path):
            try:
                raw = pygame.image.load(bg_path).convert()
                self.bg_image = pygame.transform.smoothscale(raw, (const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
            except Exception:
                pass

    def _normalize_map_coordinates(self):
        if not self.nodes:
            return

        min_x = min(node.x for node in self.nodes.values())
        max_x = max(node.x for node in self.nodes.values())
        min_y = min(node.y for node in self.nodes.values())
        max_y = max(node.y for node in self.nodes.values())

        map_w = max_x - min_x
        map_h = max_y - min_y

        # Target bounding box (with padding)
        pad_x = 80
        pad_y = 180 # Increased to push map away from bottom buttons
        target_w = const.WINDOW_WIDTH - pad_x * 2
        target_h = const.WINDOW_HEIGHT - pad_y * 2

        scale_x = target_w / map_w if map_w > 0 else 1.0
        scale_y = target_h / map_h if map_h > 0 else 1.0
        # Preserve aspect ratio
        scale = min(scale_x, scale_y)

        # Optional: prevent tiny maps from becoming overly huge
        scale = min(scale, 1.8) 

        # Calculate bounding box of map after scaling
        scaled_w = map_w * scale
        scaled_h = map_h * scale

        # Calculate offset and shift upward to make room for buttons
        offset_x = (const.WINDOW_WIDTH - scaled_w) / 2
        offset_y = (const.WINDOW_HEIGHT - scaled_h) / 2 - 40 

        # Apply transformation to all nodes
        for node in self.nodes.values():
            node.x = int((node.x - min_x) * scale + offset_x)
            node.y = int((node.y - min_y) * scale + offset_y)
            
        # Also rescale background image to match new size
        if self.bg_image:
            bg_path = os.path.join(IMAGES_DIR, 'bg_game.png')
            if os.path.exists(bg_path):
                raw = pygame.image.load(bg_path).convert()
                self.bg_image = pygame.transform.smoothscale(raw, (const.WINDOW_WIDTH, const.WINDOW_HEIGHT))

    def _load_map(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
            
        for n_data in data['nodes']:
            self.nodes[n_data['id']] = Node(n_data['id'], n_data['x'], n_data['y'], n_data['type'])
            
        for edge in data['edges']:
            u, v = edge[0], edge[1]
            self.edges.append((u, v))
            self.nodes[u].neighbors.append(self.nodes[v])
            self.nodes[v].neighbors.append(self.nodes[u])
            
        self.start_thief = self.nodes[data['start']['thief']]
        self.start_police = [self.nodes[pid] for pid in data['start']['police']]

    def draw(self, screen, selectable_nodes=None):
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.fill(const.BG_COLOR)
        if selectable_nodes is None:
            selectable_nodes = []
            
        # First pass: Draw all shadows for edges
        for u, v in self.edges:
            pygame.draw.line(screen, (40, 40, 40), (self.nodes[u].x, self.nodes[u].y + 5), (self.nodes[v].x, self.nodes[v].y + 5), 12)
            
        # Second pass: Draw main edges and their highlights
        for u, v in self.edges:
            # Main line
            pygame.draw.line(screen, const.LINE_COLOR, (self.nodes[u].x, self.nodes[u].y), (self.nodes[v].x, self.nodes[v].y), 12)
            # Edge highlight (makes them look like 3D tubes/rods instead of flat lines)
            pygame.draw.line(screen, (130, 140, 210), (self.nodes[u].x, self.nodes[u].y - 2), (self.nodes[v].x, self.nodes[v].y - 2), 4)

        # Third pass: Draw shadows for nodes
        shadow_color = (40, 40, 40)
        shadow_offset = 5
        for node in self.nodes.values():
            if node.type == "exit":
                shadow_rect = pygame.Rect(node.x - const.EXIT_SIZE//2, node.y - const.EXIT_SIZE//2 + shadow_offset, const.EXIT_SIZE, const.EXIT_SIZE)
                pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=8)
            else:
                pygame.draw.circle(screen, shadow_color, (node.x, node.y + shadow_offset), const.NODE_RADIUS)

        # Fourth pass: Draw actual nodes
        for node in self.nodes.values():
            node.draw(screen, is_highlighted=(node in selectable_nodes))

    def get_node(self, node_id):
        return self.nodes.get(node_id)
