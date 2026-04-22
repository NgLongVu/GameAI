import json
import pygame
from utils.constants import LINE_COLOR, NODE_COLOR, NODE_BORDER_COLOR, EXIT_COLOR, EXIT_FILL, BG_COLOR, NODE_RADIUS, EXIT_SIZE

class Node:
    def __init__(self, id, x, y, node_type="normal"):
        self.id = id
        self.x = x
        self.y = y
        self.type = node_type
        self.neighbors = []

    def draw(self, screen, is_highlighted=False):
        color = NODE_COLOR
        if is_highlighted:
            color = (255, 255, 100)
            
        if self.type == "exit":
            # Draw square for exit nodes
            rect = pygame.Rect(self.x - EXIT_SIZE//2, self.y - EXIT_SIZE//2, EXIT_SIZE, EXIT_SIZE)
            pygame.draw.rect(screen, EXIT_COLOR, rect, width=4)
            pygame.draw.rect(screen, EXIT_FILL, rect.inflate(-8, -8))
        else:
            # Draw circle for normal nodes (as seen in image)
            pygame.draw.circle(screen, color, (self.x, self.y), NODE_RADIUS)
            pygame.draw.circle(screen, NODE_BORDER_COLOR, (self.x, self.y), NODE_RADIUS, width=2)

class Board:
    def __init__(self, map_path):
        self.nodes = {}
        self.edges = []
        self.start_thief = None
        self.start_police = []
        self._load_map(map_path)

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
        screen.fill(BG_COLOR)
        if selectable_nodes is None:
            selectable_nodes = []
            
        # Draw edges first
        for u, v in self.edges:
            pygame.draw.line(screen, LINE_COLOR, (self.nodes[u].x, self.nodes[u].y), (self.nodes[v].x, self.nodes[v].y), 8)
            
        # Draw nodes
        for node in self.nodes.values():
            node.draw(screen, is_highlighted=(node in selectable_nodes))

    def get_node(self, node_id):
        return self.nodes.get(node_id)
