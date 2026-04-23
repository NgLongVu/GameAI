"""BFS pathfinding utilities used by the thief AI bot."""
from collections import deque


def bfs_shortest_path_to_exit(start_node, police_nodes):
    """Find shortest path from start_node to any exit node, avoiding police positions."""
    blocked_ids = {p.id for p in police_nodes}

    queue = deque([(start_node, [start_node])])
    visited = {start_node.id}

    while queue:
        current, path = queue.popleft()

        if current.type == 'exit':
            return path

        for neighbor in current.neighbors:
            if neighbor.id not in visited and neighbor.id not in blocked_ids:
                visited.add(neighbor.id)
                queue.append((neighbor, path + [neighbor]))

    return None


def compute_distances_from_nodes(start_nodes):
    """BFS multi-source distance map: node_id → distance from nearest start_node."""
    distances = {}
    queue = deque()

    for sn in start_nodes:
        queue.append((sn, 0))
        distances[sn.id] = 0

    while queue:
        current, dist = queue.popleft()
        for neighbor in current.neighbors:
            if neighbor.id not in distances:
                distances[neighbor.id] = dist + 1
                queue.append((neighbor, dist + 1))

    return distances

def get_all_exits(nodes):
    """Return a list of all nodes marked as exits."""
    all_nodes = nodes.values() if isinstance(nodes, dict) else nodes
    return [n for n in all_nodes if n.type == 'exit']
