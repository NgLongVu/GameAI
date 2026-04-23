import math
from ai.pathfinding import compute_distances_from_nodes, get_all_exits

def evaluate_state(thief_node, police_nodes, exit_nodes):
    """Heuristic: Higher is better for Thief."""
    exit_dist_map = compute_distances_from_nodes(exit_nodes)
    d_exit = exit_dist_map.get(thief_node.id, 999)
    
    police_dist_map = compute_distances_from_nodes(police_nodes)
    d_police = police_dist_map.get(thief_node.id, 999)
    
    if d_police == 0: return -99999
    if d_exit == 0: return 99999
    
    mobility = len(thief_node.neighbors)
    
    # NEW WEIGHTS: Much higher priority on d_exit.
    # d_police is only critical when it's small (< 5)
    police_weight = 2 if d_police > 5 else 10
    
    return (d_police * police_weight) - (d_exit * 15) + (mobility * 1)

def minimax(thief_node, police_nodes, exit_nodes, depth, is_maximizing, alpha, beta):
    if depth == 0 or thief_node.type == 'exit' or any(p.id == thief_node.id for p in police_nodes):
        return evaluate_state(thief_node, police_nodes, exit_nodes)
        
    if is_maximizing:
        max_eval = -math.inf
        for neighbor in thief_node.neighbors:
            if any(p.id == neighbor.id for p in police_nodes): continue
            eval = minimax(neighbor, police_nodes, exit_nodes, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha: break
        return max_eval if max_eval != -math.inf else -99999
    else:
        min_eval = math.inf
        # Only simulate the 2 closest police for performance
        thief_dist_map = compute_distances_from_nodes([thief_node])
        sorted_police = sorted(police_nodes, key=lambda p: thief_dist_map.get(p.id, 999))
        
        for p_node in sorted_police[:2]:
            for neighbor in p_node.neighbors:
                if any(other_p.id == neighbor.id for other_p in police_nodes if other_p.id != p_node.id):
                    continue
                new_police_nodes = [neighbor if p.id == p_node.id else p for p in police_nodes]
                eval = minimax(thief_node, new_police_nodes, exit_nodes, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha: break
            if beta <= alpha: break
        return min_eval if min_eval != math.inf else 99999

def choose_thief_move(thief_node, police_nodes, all_nodes):
    exit_nodes = get_all_exits(all_nodes)
    exit_dist_map = compute_distances_from_nodes(exit_nodes)
    
    best_move = None
    max_val = -math.inf
    min_exit_dist = math.inf
    
    moves = [n for n in thief_node.neighbors if not any(p.id == n.id for p in police_nodes)]
    if not moves: return None
    
    for neighbor in moves:
        val = minimax(neighbor, police_nodes, exit_nodes, 3, False, -math.inf, math.inf)
        d_exit = exit_dist_map.get(neighbor.id, 999)
        
        # Tie-breaker logic: 
        # If score is same, pick the one closer to exit
        if val > max_val:
            max_val = val
            min_exit_dist = d_exit
            best_move = neighbor
        elif val == max_val:
            if d_exit < min_exit_dist:
                min_exit_dist = d_exit
                best_move = neighbor
            
    return best_move
