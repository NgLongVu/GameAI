from enum import Enum
from ai.bot import choose_thief_move

class Turn(Enum):
    POLICE = 0
    THIEF = 1
    GAME_OVER_POLICE_WIN = 2
    GAME_OVER_THIEF_WIN = 3

class Command:
    def __init__(self, entities, previous_states, new_states, freeze_state_before, freeze_state_after):
        # We store snapshots of where everyone was.
        # entities: dict of string -> Entity or List[Entity]
        # states: dict of string -> Node or List[Node]
        self.entities = entities
        self.prev = previous_states
        self.new = new_states
        self.fp_before = freeze_state_before
        self.fp_after = freeze_state_after
        
    def undo(self, game_state_manager):
        # Restore police
        for i, p in enumerate(self.entities['police']):
            p.move_to(self.prev['police'][i])
            # Also snap visual immediately on undo
            p.visual_x = float(p.current_node.x)
            p.visual_y = float(p.current_node.y)

        # Restore thief
        t = self.entities['thief']
        t.move_to(self.prev['thief'])
        t.visual_x = float(t.current_node.x)
        t.visual_y = float(t.current_node.y)
        
        # Restore freeze
        game_state_manager.is_thief_frozen = self.fp_before['active']
        game_state_manager.turn = Turn.POLICE

class GameState:
    def __init__(self, board, police_list, thief):
        self.board = board
        self.police = police_list
        self.thief = thief
        
        self.turn = Turn.POLICE
        self.history = []
        self.is_thief_frozen = False
        
        # UI Selection state
        self.selected_police = None
        
        # Save state at the START of the turn for complete Full Turn undo
        self.turn_start_state = self._capture_state()
        self.turn_start_state_freeze = self._capture_freeze_state()  # fix: init here

    def _capture_state(self):
        return {
            'police': [p.current_node for p in self.police],
            'thief': self.thief.current_node
        }
        
    def _capture_freeze_state(self):
        return {
            'active': self.is_thief_frozen
        }

    def can_undo(self):
        return len(self.history) > 0

    def undo(self):
        if self.can_undo():
            last_command = self.history.pop()
            last_command.undo(self)
            self.selected_police = None
            self.turn_start_state = self._capture_state()

    def use_freeze(self):
        if self.turn == Turn.POLICE and not self.is_thief_frozen:
            self.is_thief_frozen = True
            return True
        return False

    def check_win_condition(self):
        if self.thief.is_at_exit():
            self.turn = Turn.GAME_OVER_THIEF_WIN
            return True
        # Check if thief has no valid moves (trapped)
        p_ids = {p.current_node.id for p in self.police}
        can_move = any(n.id not in p_ids for n in self.thief.current_node.neighbors)
        if not can_move and not self.is_thief_frozen:
            # Trapped!
            self.turn = Turn.GAME_OVER_POLICE_WIN
            return True
        return False

    def process_police_move(self, destination_node):
        freeze_before = self._capture_freeze_state()
        
        # Move police
        self.selected_police.move_to(destination_node)
        self.selected_police = None
        
        if self.check_win_condition():
            return

        # End of police turn
        self.turn = Turn.THIEF

    def process_thief_turn(self):
        if self.turn != Turn.THIEF: return

        if self.is_thief_frozen:
            self.is_thief_frozen = False
        else:
            p_nodes = [p.current_node for p in self.police]
            next_node = choose_thief_move(self.thief.current_node, p_nodes, self.board.nodes)
            
            if next_node:
                self.thief.move_to(next_node)
            else:
                self.turn = Turn.GAME_OVER_POLICE_WIN
                return

        if self.check_win_condition():
            return
            
        # create command
        cmd = Command(
            entities={'police': self.police, 'thief': self.thief},
            previous_states=self.turn_start_state,
            new_states=self._capture_state(),
            freeze_state_before=self._capture_freeze_state(), # Need the state at start essentially, wait, we need the state before this turn
            freeze_state_after=self._capture_freeze_state()
        )
        # Because we want undo to restore freeze state to what it was BEFORE police acted
        # We should store the freeze state at turn start.
        cmd.fp_before = self.turn_start_state_freeze
        self.history.append(cmd)
        
        self.turn = Turn.POLICE
        self.turn_start_state = self._capture_state()
        self.turn_start_state_freeze = self._capture_freeze_state()

    def start_game(self):
        self.turn_start_state_freeze = self._capture_freeze_state()

    def update(self):
        # Allow entities to animate
        for p in self.police:
            p.update()
        self.thief.update()

        animating = any(p.is_animating() for p in self.police) or self.thief.is_animating()
        
        if not animating and self.turn == Turn.THIEF:
            self.process_thief_turn()

    def is_animating(self):
        return any(p.is_animating() for p in self.police) or self.thief.is_animating()
