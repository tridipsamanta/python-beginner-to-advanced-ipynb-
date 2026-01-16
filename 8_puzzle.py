
import pygame
import sys
import heapq
import time
import random
import threading
from collections import deque
from enum import Enum
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
TILE_MARGIN = 3

# Colors
COLORS = {
    'background': (15, 15, 25),
    'tile_normal': (70, 130, 180),
    'tile_hover': (100, 150, 200),
    'tile_selected': (130, 170, 220),
    'tile_correct': (50, 205, 50),
    'text_primary': (255, 255, 255),
    'text_secondary': (200, 200, 200),
    'empty_space': (45, 45, 65),
    'border': (255, 255, 255),
    'button': (60, 60, 80),
    'button_hover': (80, 80, 100),
    'solution_path': (255, 215, 0),
    'ai_move': (255, 100, 100),
    'difficulty_easy': (100, 255, 100),
    'difficulty_medium': (255, 255, 100),
    'difficulty_hard': (255, 100, 100),
    'difficulty_expert': (255, 0, 255)
}

class PuzzleSize(Enum):
    EIGHT = (3, "8-Puzzle")
    FIFTEEN = (4, "15-Puzzle")
    TWENTY_FOUR = (5, "24-Puzzle")
    THIRTY_FIVE = (6, "35-Puzzle")

class SearchAlgorithm(Enum):
    BFS = "Breadth-First Search"
    DFS = "Depth-First Search"
    A_STAR_MANHATTAN = "A* (Manhattan Distance)"
    A_STAR_EUCLIDEAN = "A* (Euclidean Distance)"
    A_STAR_LINEAR_CONFLICT = "A* (Linear Conflict)"
    GREEDY_MANHATTAN = "Greedy (Manhattan)"
    IDA_STAR = "IDA* (Iterative Deepening A*)"

class DifficultyLevel(Enum):
    EASY = (10, "Easy", COLORS['difficulty_easy'])
    MEDIUM = (25, "Medium", COLORS['difficulty_medium'])
    HARD = (50, "Hard", COLORS['difficulty_hard'])
    EXPERT = (100, "Expert", COLORS['difficulty_expert'])

class NPuzzleState:
    """Represents a state of the N-puzzle"""

    def __init__(self, board, size, parent=None, move=None, depth=0):
        self.board = [row[:] for row in board]  # Deep copy
        self.size = size
        self.parent = parent
        self.move = move
        self.depth = depth
        self.empty_pos = self.find_empty()
        self.hash_value = self._calculate_hash()

    def find_empty(self):
        """Find the position of the empty tile (0)"""
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def _calculate_hash(self):
        """Calculate hash for efficient state comparison"""
        return hash(tuple(tuple(row) for row in self.board))

    def __hash__(self):
        return self.hash_value

    def __eq__(self, other):
        return isinstance(other, NPuzzleState) and self.board == other.board

    def __lt__(self, other):
        return False

    def is_goal(self):
        """Check if this is the goal state"""
        goal = self.get_goal_state()
        return self.board == goal

    def get_goal_state(self):
        """Get the goal state for the current puzzle size"""
        goal = []
        num = 1
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:
                    row.append(0)  # Empty space at bottom right
                else:
                    row.append(num)
                    num += 1
            goal.append(row)
        return goal

    def manhattan_distance(self):
        """Calculate Manhattan distance heuristic"""
        distance = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    value = self.board[i][j]
                    target_row = (value - 1) // self.size
                    target_col = (value - 1) % self.size
                    distance += abs(i - target_row) + abs(j - target_col)
        return distance

    def euclidean_distance(self):
        """Calculate Euclidean distance heuristic"""
        distance = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    value = self.board[i][j]
                    target_row = (value - 1) // self.size
                    target_col = (value - 1) % self.size
                    distance += math.sqrt((i - target_row)**2 + (j - target_col)**2)
        return distance

    def linear_conflict(self):
        """Calculate Linear Conflict heuristic (Manhattan + conflicts)"""
        manhattan = self.manhattan_distance()
        conflicts = 0

        # Check row conflicts
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    value = self.board[i][j]
                    target_row = (value - 1) // self.size
                    if i == target_row:  # Tile is in correct row
                        for k in range(j + 1, self.size):
                            if self.board[i][k] != 0:
                                other_value = self.board[i][k]
                                other_target_row = (other_value - 1) // self.size
                                other_target_col = (other_value - 1) % self.size
                                if (i == other_target_row and 
                                    (value - 1) % self.size > other_target_col):
                                    conflicts += 1

        # Check column conflicts
        for j in range(self.size):
            for i in range(self.size):
                if self.board[i][j] != 0:
                    value = self.board[i][j]
                    target_col = (value - 1) % self.size
                    if j == target_col:  # Tile is in correct column
                        for k in range(i + 1, self.size):
                            if self.board[k][j] != 0:
                                other_value = self.board[k][j]
                                other_target_row = (other_value - 1) // self.size
                                other_target_col = (other_value - 1) % self.size
                                if (j == other_target_col and 
                                    (value - 1) // self.size > other_target_row):
                                    conflicts += 1

        return manhattan + 2 * conflicts

    def misplaced_tiles(self):
        """Calculate misplaced tiles heuristic"""
        goal = self.get_goal_state()
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0 and self.board[i][j] != goal[i][j]:
                    count += 1
        return count

    def is_solvable(self):
        """Check if the puzzle state is solvable"""
        # Convert 2D board to 1D array excluding the empty tile
        flat = []
        empty_row = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    empty_row = i
                else:
                    flat.append(self.board[i][j])

        # Count inversions
        inversions = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] > flat[j]:
                    inversions += 1

        # Apply solvability rules
        if self.size % 2 == 1:  # Odd size
            return inversions % 2 == 0
        else:  # Even size
            return (inversions + empty_row) % 2 == 1

    def get_neighbors(self):
        """Get all possible neighbor states"""
        neighbors = []
        row, col = self.empty_pos
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]

        for dr, dc, move_name in moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                # Create new board with swapped tiles
                new_board = [row[:] for row in self.board]
                new_board[row][col], new_board[new_row][new_col] = \
                    new_board[new_row][new_col], new_board[row][col]
                neighbors.append(NPuzzleState(new_board, self.size, self, move_name, self.depth + 1))

        return neighbors

    def get_path(self):
        """Get the path from start to this state"""
        path = []
        current = self
        while current.parent is not None:
            path.append(current.move)
            current = current.parent
        return path[::-1]

class AdvancedAIEngine:
    """Advanced AI Engine with multiple search algorithms"""

    def __init__(self):
        self.stats = {
            'nodes_explored': 0,
            'max_depth': 0,
            'time_elapsed': 0,
            'memory_used': 0,
            'solution_length': 0
        }

    def reset_stats(self):
        """Reset search statistics"""
        self.stats = {
            'nodes_explored': 0,
            'max_depth': 0,
            'time_elapsed': 0,
            'memory_used': 0,
            'solution_length': 0
        }

    def breadth_first_search(self, initial_state, max_nodes=100000):
        """BFS with memory limit"""
        self.reset_stats()
        start_time = time.time()

        if initial_state.is_goal():
            return initial_state.get_path()

        queue = deque([initial_state])
        visited = {initial_state}

        while queue and len(visited) < max_nodes:
            current = queue.popleft()
            self.stats['nodes_explored'] += 1
            self.stats['max_depth'] = max(self.stats['max_depth'], current.depth)

            for neighbor in current.get_neighbors():
                if neighbor not in visited:
                    if neighbor.is_goal():
                        self.stats['time_elapsed'] = time.time() - start_time
                        self.stats['solution_length'] = len(neighbor.get_path())
                        return neighbor.get_path()

                    visited.add(neighbor)
                    queue.append(neighbor)

        self.stats['time_elapsed'] = time.time() - start_time
        return None

    def a_star_search(self, initial_state, heuristic_func, max_nodes=50000):
        """A* Search with memory limit"""
        self.reset_stats()
        start_time = time.time()

        if initial_state.is_goal():
            return initial_state.get_path()

        open_set = []
        heapq.heappush(open_set, (heuristic_func(initial_state), 0, initial_state))

        g_score = {initial_state: 0}
        visited = set()

        while open_set and len(visited) < max_nodes:
            _, current_g, current = heapq.heappop(open_set)

            if current in visited:
                continue

            visited.add(current)
            self.stats['nodes_explored'] += 1
            self.stats['max_depth'] = max(self.stats['max_depth'], current.depth)

            if current.is_goal():
                self.stats['time_elapsed'] = time.time() - start_time
                self.stats['solution_length'] = len(current.get_path())
                return current.get_path()

            for neighbor in current.get_neighbors():
                if neighbor in visited:
                    continue

                tentative_g = current_g + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic_func(neighbor)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))

        self.stats['time_elapsed'] = time.time() - start_time
        return None

    def ida_star_search(self, initial_state, heuristic_func, max_iterations=100):
        """IDA* Search implementation"""
        self.reset_stats()
        start_time = time.time()

        def search(node, g, threshold):
            f = g + heuristic_func(node)
            if f > threshold:
                return f, None

            if node.is_goal():
                return f, node.get_path()

            min_threshold = float('inf')
            for neighbor in node.get_neighbors():
                self.stats['nodes_explored'] += 1
                t, path = search(neighbor, g + 1, threshold)
                if path is not None:
                    return t, path
                if t < min_threshold:
                    min_threshold = t

            return min_threshold, None

        threshold = heuristic_func(initial_state)

        for iteration in range(max_iterations):
            t, path = search(initial_state, 0, threshold)
            if path is not None:
                self.stats['time_elapsed'] = time.time() - start_time
                self.stats['solution_length'] = len(path)
                return path
            if t == float('inf'):
                break
            threshold = t

        self.stats['time_elapsed'] = time.time() - start_time
        return None

class Button:
    """Enhanced button class"""

    def __init__(self, x, y, width, height, text, font, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hovered = False
        self.color = color or COLORS['button']
        self.hover_color = COLORS['button_hover']

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, COLORS['border'], self.rect, 2, border_radius=5)

        text_surface = self.font.render(self.text, True, COLORS['text_primary'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False

class UltimateNPuzzle:
    """Ultimate N-Puzzle game supporting multiple sizes"""

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Ultimate N-Puzzle: World's Most Advanced Puzzle Game")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        self.font_title = pygame.font.Font(None, 48)

        # Game settings
        self.current_size = PuzzleSize.EIGHT
        self.difficulty = DifficultyLevel.MEDIUM
        self.size = self.current_size.value[0]
        self.tile_size = self.calculate_tile_size()

        # Game state
        self.board = []
        self.empty_pos = (self.size - 1, self.size - 1)
        self.moves = 0
        self.game_won = False
        self.selected_tile = None
        self.start_time = time.time()

        # AI components
        self.ai_engine = AdvancedAIEngine()
        self.current_algorithm = SearchAlgorithm.A_STAR_MANHATTAN
        self.solution_path = []
        self.solution_index = 0
        self.solving = False
        self.auto_solve = False

        # Statistics
        self.best_scores = {}
        self.solve_statistics = []

        # UI elements
        self.create_buttons()

        # Initialize puzzle
        self.reset_puzzle()

    def calculate_tile_size(self):
        """Calculate appropriate tile size based on puzzle size"""
        available_space = min(500, 600)  # Max space for board
        return (available_space - (self.size + 1) * TILE_MARGIN) // self.size

    def calculate_board_position(self):
        """Calculate board position for centering"""
        board_width = self.size * self.tile_size + (self.size - 1) * TILE_MARGIN
        board_height = board_width

        self.board_x = 50
        self.board_y = (WINDOW_HEIGHT - board_height) // 2

    def create_buttons(self):
        """Create UI buttons"""
        button_width = 140
        button_height = 25
        button_x = WINDOW_WIDTH - 180
        start_y = 150

        self.buttons = {
            # Puzzle size buttons
            '8_puzzle': Button(button_x, start_y, button_width, button_height, "8-Puzzle", self.font_small),
            '15_puzzle': Button(button_x, start_y + 30, button_width, button_height, "15-Puzzle", self.font_small),
            '24_puzzle': Button(button_x, start_y + 60, button_width, button_height, "24-Puzzle", self.font_small),
            '35_puzzle': Button(button_x, start_y + 90, button_width, button_height, "35-Puzzle", self.font_small),

            # Difficulty buttons
            'easy': Button(button_x, start_y + 130, button_width//2 - 2, button_height, "Easy", self.font_small, COLORS['difficulty_easy']),
            'medium': Button(button_x + button_width//2 + 2, start_y + 130, button_width//2 - 2, button_height, "Med", self.font_small, COLORS['difficulty_medium']),
            'hard': Button(button_x, start_y + 160, button_width//2 - 2, button_height, "Hard", self.font_small, COLORS['difficulty_hard']),
            'expert': Button(button_x + button_width//2 + 2, start_y + 160, button_width//2 - 2, button_height, "Exp", self.font_small, COLORS['difficulty_expert']),

            # Game control buttons
            'shuffle': Button(button_x, start_y + 200, button_width, button_height, "Shuffle", self.font_small),
            'reset': Button(button_x, start_y + 230, button_width, button_height, "Reset", self.font_small),

            # AI solver buttons
            'solve_bfs': Button(button_x, start_y + 270, button_width, button_height, "Solve (BFS)", self.font_small),
            'solve_astar_m': Button(button_x, start_y + 300, button_width, button_height, "Solve (A* Manhattan)", self.font_small),
            'solve_astar_lc': Button(button_x, start_y + 330, button_width, button_height, "Solve (A* Linear)", self.font_small),
            'solve_ida': Button(button_x, start_y + 360, button_width, button_height, "Solve (IDA*)", self.font_small),

            'auto_solve': Button(button_x, start_y + 400, button_width, button_height, "Auto Solve", self.font_small),
            'next_move': Button(button_x, start_y + 430, button_width, button_height, "Next Move", self.font_small),
            'analyze': Button(button_x, start_y + 460, button_width, button_height, "Analyze Puzzle", self.font_small),
        }

    def reset_puzzle(self):
        """Reset puzzle to solved state"""
        self.board = []
        num = 1
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:
                    row.append(0)  # Empty space
                else:
                    row.append(num)
                    num += 1
            self.board.append(row)

        self.empty_pos = (self.size - 1, self.size - 1)
        self.moves = 0
        self.game_won = False
        self.solution_path = []
        self.start_time = time.time()
        self.calculate_board_position()

    def shuffle_puzzle(self):
        """Shuffle the puzzle based on difficulty"""
        shuffle_moves = self.difficulty.value[0]
        for _ in range(shuffle_moves):
            possible_moves = self.get_possible_moves()
            if possible_moves:
                row, col = random.choice(possible_moves)
                self.move_tile(row, col, count_move=False)

        # Ensure puzzle is solvable
        state = NPuzzleState(self.board, self.size)
        if not state.is_solvable():
            # Make one more move to fix solvability
            possible_moves = self.get_possible_moves()
            if possible_moves:
                row, col = possible_moves[0]
                self.move_tile(row, col, count_move=False)

        self.moves = 0
        self.start_time = time.time()

    def change_puzzle_size(self, new_size):
        """Change the puzzle size"""
        self.current_size = new_size
        self.size = new_size.value[0]
        self.tile_size = self.calculate_tile_size()
        self.reset_puzzle()

    def get_possible_moves(self):
        """Get tiles that can move to empty space"""
        empty_row, empty_col = self.empty_pos
        possible = []

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = empty_row + dr, empty_col + dc
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                possible.append((new_row, new_col))

        return possible

    def move_tile(self, tile_row, tile_col, count_move=True):
        """Move a tile to the empty space"""
        empty_row, empty_col = self.empty_pos

        if abs(tile_row - empty_row) + abs(tile_col - empty_col) == 1:
            self.board[empty_row][empty_col], self.board[tile_row][tile_col] = \
                self.board[tile_row][tile_col], self.board[empty_row][empty_col]
            self.empty_pos = (tile_row, tile_col)

            if count_move:
                self.moves += 1
                self.check_win()
            return True
        return False

    def check_win(self):
        """Check if puzzle is solved"""
        state = NPuzzleState(self.board, self.size)
        self.game_won = state.is_goal()

    def solve_with_algorithm(self, algorithm):
        """Solve puzzle using specified algorithm"""
        if self.solving:
            return

        self.solving = True
        current_state = NPuzzleState(self.board, self.size)

        def solve_thread():
            try:
                solution = None
                if algorithm == SearchAlgorithm.BFS:
                    solution = self.ai_engine.breadth_first_search(current_state)
                elif algorithm == SearchAlgorithm.A_STAR_MANHATTAN:
                    solution = self.ai_engine.a_star_search(current_state, NPuzzleState.manhattan_distance)
                elif algorithm == SearchAlgorithm.A_STAR_LINEAR_CONFLICT:
                    solution = self.ai_engine.a_star_search(current_state, NPuzzleState.linear_conflict)
                elif algorithm == SearchAlgorithm.IDA_STAR:
                    solution = self.ai_engine.ida_star_search(current_state, NPuzzleState.manhattan_distance)

                self.solution_path = solution if solution else []
                self.solution_index = 0
                self.current_algorithm = algorithm

                # Store statistics
                if solution:
                    stats = self.ai_engine.stats.copy()
                    stats['algorithm'] = algorithm.value
                    stats['puzzle_size'] = self.current_size.value[1]
                    stats['difficulty'] = self.difficulty.value[1]
                    self.solve_statistics.append(stats)

            except Exception as e:
                print(f"Solver error: {e}")
                self.solution_path = []
            finally:
                self.solving = False

        threading.Thread(target=solve_thread, daemon=True).start()

    def execute_next_move(self):
        """Execute the next move in the solution path"""
        if not self.solution_path or self.solution_index >= len(self.solution_path):
            return False

        move = self.solution_path[self.solution_index]
        empty_row, empty_col = self.empty_pos

        # Convert move direction to tile position
        move_map = {
            'UP': (empty_row + 1, empty_col),
            'DOWN': (empty_row - 1, empty_col),
            'LEFT': (empty_row, empty_col + 1),
            'RIGHT': (empty_row, empty_col - 1)
        }

        if move in move_map:
            tile_pos = move_map[move]
            if self.move_tile(tile_pos[0], tile_pos[1]):
                self.solution_index += 1
                return True
        return False

    def analyze_puzzle(self):
        """Analyze current puzzle state"""
        state = NPuzzleState(self.board, self.size)

        analysis = {
            'solvable': state.is_solvable(),
            'manhattan_distance': state.manhattan_distance(),
            'euclidean_distance': state.euclidean_distance(),
            'linear_conflict': state.linear_conflict(),
            'misplaced_tiles': state.misplaced_tiles(),
            'puzzle_size': self.current_size.value[1],
            'difficulty': self.difficulty.value[1]
        }

        return analysis

    def draw_board(self):
        """Draw the puzzle board"""
        for row in range(self.size):
            for col in range(self.size):
                x = self.board_x + col * (self.tile_size + TILE_MARGIN)
                y = self.board_y + row * (self.tile_size + TILE_MARGIN)

                if self.board[row][col] == 0:
                    # Empty space
                    pygame.draw.rect(self.screen, COLORS['empty_space'], 
                                   pygame.Rect(x, y, self.tile_size, self.tile_size), border_radius=5)
                    pygame.draw.rect(self.screen, COLORS['border'], 
                                   pygame.Rect(x, y, self.tile_size, self.tile_size), 2, border_radius=5)
                else:
                    # Tile
                    number = self.board[row][col]
                    target_row, target_col = (number - 1) // self.size, (number - 1) % self.size

                    if row == target_row and col == target_col:
                        color = COLORS['tile_correct']
                    else:
                        color = COLORS['tile_normal']

                    pygame.draw.rect(self.screen, color, 
                                   pygame.Rect(x, y, self.tile_size, self.tile_size), border_radius=5)
                    pygame.draw.rect(self.screen, COLORS['border'], 
                                   pygame.Rect(x, y, self.tile_size, self.tile_size), 2, border_radius=5)

                    # Draw number
                    font_size = min(self.tile_size // 3, 24)
                    font = pygame.font.Font(None, font_size)
                    text = font.render(str(number), True, COLORS['text_primary'])
                    text_rect = text.get_rect(center=(x + self.tile_size // 2, y + self.tile_size // 2))
                    self.screen.blit(text, text_rect)

    def draw_ui(self):
        """Draw the user interface"""
        # Title
        title = self.font_title.render("Ultimate N-Puzzle", True, COLORS['text_primary'])
        self.screen.blit(title, (20, 20))

        subtitle = self.font_medium.render("World's Most Advanced Puzzle Game", True, COLORS['text_secondary'])
        self.screen.blit(subtitle, (20, 65))

        # Current puzzle info
        puzzle_info = f"{self.current_size.value[1]} - {self.difficulty.value[1]} Difficulty"
        info_text = self.font_medium.render(puzzle_info, True, self.difficulty.value[2])
        self.screen.blit(info_text, (20, 100))

        # Game statistics
        stats_y = 130
        game_stats = [
            f"Moves: {self.moves}",
            f"Time: {int(time.time() - self.start_time)}s",
            f"Status: {'Solved!' if self.game_won else 'Playing'}",
        ]

        for i, text in enumerate(game_stats):
            surface = self.font_medium.render(text, True, COLORS['text_secondary'])
            self.screen.blit(surface, (20, stats_y + i * 25))

        # AI Analysis
        if hasattr(self, 'current_analysis'):
            analysis_y = 650
            analysis_title = self.font_medium.render("Puzzle Analysis:", True, COLORS['text_primary'])
            self.screen.blit(analysis_title, (20, analysis_y))

            analysis_items = [
                f"Solvable: {'Yes' if self.current_analysis['solvable'] else 'No'}",
                f"Manhattan Distance: {self.current_analysis['manhattan_distance']}",
                f"Linear Conflict: {self.current_analysis['linear_conflict']}",
                f"Misplaced Tiles: {self.current_analysis['misplaced_tiles']}"
            ]

            for i, text in enumerate(analysis_items):
                surface = self.font_small.render(text, True, COLORS['text_secondary'])
                self.screen.blit(surface, (20, analysis_y + 25 + i * 20))

        # AI Statistics
        if hasattr(self.ai_engine, 'stats') and self.ai_engine.stats['nodes_explored'] > 0:
            ai_stats_y = 350
            ai_title = self.font_medium.render("AI Search Statistics:", True, COLORS['text_primary'])
            self.screen.blit(ai_title, (20, ai_stats_y))

            ai_stats = [
                f"Algorithm: {self.current_algorithm.value}",
                f"Nodes Explored: {self.ai_engine.stats['nodes_explored']:,}",
                f"Max Depth: {self.ai_engine.stats['max_depth']}",
                f"Time: {self.ai_engine.stats['time_elapsed']:.3f}s",
                f"Solution Length: {self.ai_engine.stats['solution_length']}",
                f"Nodes/Second: {int(self.ai_engine.stats['nodes_explored'] / max(self.ai_engine.stats['time_elapsed'], 0.001)):,}"
            ]

            for i, text in enumerate(ai_stats):
                surface = self.font_small.render(text, True, COLORS['text_secondary'])
                self.screen.blit(surface, (20, ai_stats_y + 25 + i * 20))

        # Solution progress
        if self.solution_path:
            progress_y = 550
            progress_text = f"Solution Progress: {self.solution_index}/{len(self.solution_path)}"
            surface = self.font_medium.render(progress_text, True, COLORS['solution_path'])
            self.screen.blit(surface, (20, progress_y))

            # Progress bar
            if len(self.solution_path) > 0:
                bar_width = 200
                bar_height = 10
                progress_ratio = self.solution_index / len(self.solution_path)

                pygame.draw.rect(self.screen, COLORS['empty_space'], 
                               pygame.Rect(20, progress_y + 25, bar_width, bar_height))
                pygame.draw.rect(self.screen, COLORS['solution_path'], 
                               pygame.Rect(20, progress_y + 25, int(bar_width * progress_ratio), bar_height))

        # Solving indicator
        if self.solving:
            solving_text = self.font_medium.render("AI is thinking...", True, COLORS['ai_move'])
            # Add blinking effect
            if int(time.time() * 2) % 2:
                self.screen.blit(solving_text, (20, 600))

        # Draw buttons
        for button in self.buttons.values():
            button.draw(self.screen)

        # Instructions
        instructions = [
            "Puzzle Sizes & Controls:",
            "• Click tiles to move them",
            "• Use AI solvers for optimal solutions",
            "• Try different puzzle sizes and difficulties",
            "• Analyze puzzle complexity with heuristics"
        ]

        instr_y = WINDOW_HEIGHT - 120
        for i, instr in enumerate(instructions):
            color = COLORS['text_primary'] if i == 0 else COLORS['text_secondary']
            surface = self.font_small.render(instr, True, color)
            self.screen.blit(surface, (WINDOW_WIDTH - 350, instr_y + i * 18))

    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Handle button clicks
            for name, button in self.buttons.items():
                if button.handle_event(event):
                    if name == '8_puzzle':
                        self.change_puzzle_size(PuzzleSize.EIGHT)
                    elif name == '15_puzzle':
                        self.change_puzzle_size(PuzzleSize.FIFTEEN)
                    elif name == '24_puzzle':
                        self.change_puzzle_size(PuzzleSize.TWENTY_FOUR)
                    elif name == '35_puzzle':
                        self.change_puzzle_size(PuzzleSize.THIRTY_FIVE)
                    elif name == 'easy':
                        self.difficulty = DifficultyLevel.EASY
                    elif name == 'medium':
                        self.difficulty = DifficultyLevel.MEDIUM
                    elif name == 'hard':
                        self.difficulty = DifficultyLevel.HARD
                    elif name == 'expert':
                        self.difficulty = DifficultyLevel.EXPERT
                    elif name == 'shuffle':
                        self.shuffle_puzzle()
                    elif name == 'reset':
                        self.reset_puzzle()
                    elif name == 'solve_bfs':
                        self.solve_with_algorithm(SearchAlgorithm.BFS)
                    elif name == 'solve_astar_m':
                        self.solve_with_algorithm(SearchAlgorithm.A_STAR_MANHATTAN)
                    elif name == 'solve_astar_lc':
                        self.solve_with_algorithm(SearchAlgorithm.A_STAR_LINEAR_CONFLICT)
                    elif name == 'solve_ida':
                        self.solve_with_algorithm(SearchAlgorithm.IDA_STAR)
                    elif name == 'auto_solve':
                        self.auto_solve = not self.auto_solve
                        button.text = "Stop Auto" if self.auto_solve else "Auto Solve"
                    elif name == 'next_move':
                        self.execute_next_move()
                    elif name == 'analyze':
                        self.current_analysis = self.analyze_puzzle()

            # Handle tile clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos

                # Check if click is on board
                board_width = self.size * (self.tile_size + TILE_MARGIN) - TILE_MARGIN
                board_height = board_width

                if (self.board_x <= mouse_x <= self.board_x + board_width and 
                    self.board_y <= mouse_y <= self.board_y + board_height):

                    col = (mouse_x - self.board_x) // (self.tile_size + TILE_MARGIN)
                    row = (mouse_y - self.board_y) // (self.tile_size + TILE_MARGIN)

                    if (0 <= row < self.size and 0 <= col < self.size and 
                        self.board[row][col] != 0):
                        self.move_tile(row, col)

        return True

    def update(self):
        """Update game state"""
        if self.auto_solve and self.solution_path and self.solution_index < len(self.solution_path):
            current_time = pygame.time.get_ticks()
            if not hasattr(self, 'last_auto_move') or current_time - self.last_auto_move > 300:
                self.execute_next_move()
                self.last_auto_move = current_time

    def run(self):
        """Main game loop"""
        running = True

        while running:
            running = self.handle_events()
            self.update()

            # Clear screen
            self.screen.fill(COLORS['background'])

            # Draw game elements
            self.draw_board()
            self.draw_ui()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = UltimateNPuzzle()
    game.run()
