from ai.pathfinding import bfs_shortest_path_to_exit, compute_distances_from_nodes


def get_best_survival_move(start_node, police_nodes):
    """Return neighbor that maximizes distance from all police (survival mode)."""
    blocked_ids = {p.id for p in police_nodes}
    dist_map = compute_distances_from_nodes(police_nodes)

    valid_neighbors = [n for n in start_node.neighbors if n.id not in blocked_ids]
    if not valid_neighbors:
        return None  # Trapped

    return max(valid_neighbors, key=lambda n: dist_map.get(n.id, 999))


def choose_thief_move(thief_node, police_nodes):
    """Main AI entry point: try to reach exit, fall back to survival mode."""
    path = bfs_shortest_path_to_exit(thief_node, police_nodes)
    if path and len(path) > 1:
        return path[1]  # path[0] is current, path[1] is next step

    return get_best_survival_move(thief_node, police_nodes)
