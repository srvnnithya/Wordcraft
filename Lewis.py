import pygame
import sys
from collections import deque

pygame.init()
WIDTH, HEIGHT = 800, 600  
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Ladder Solver")


COLORS = {
    'BACKGROUND': (245, 246, 250),
    'PRIMARY': (52, 152, 219),    
    'SECONDARY': (44, 62, 80),   
    'WHITE': (255, 255, 255),
    'TEXT': (33, 47, 61),
    'HOVER': (41, 128, 185),      
    'SHADOW': (170, 178, 190)    
}

class FontManager:
    def __init__(self):
        self.title = pygame.font.Font(None, 48)
        self.input_font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 32)

class WordLadderSolver:
    def __init__(self, word_list):
        self.word_list = set(word_list)

    def find_word_ladder(self, start, end):
        if not start or not end:
            return None
        
        start = start.lower()
        end = end.lower()
        
        if start not in self.word_list or end not in self.word_list:
            return None
        
        # Bidirectional BFS (Previous implementation)
        forward_queue = deque([(start, [start])])
        backward_queue = deque([(end, [end])])
        
        forward_visited = {start: [start]}
        backward_visited = {end: [end]}

        while forward_queue and backward_queue:
            # Forward search
            current_word, current_path = forward_queue.popleft()
            
            for neighbor in self._get_neighbors(current_word):
                if neighbor in backward_visited:
                    full_path = current_path + backward_visited[neighbor][::-1][1:]
                    return full_path

                if neighbor not in forward_visited:
                    new_path = current_path + [neighbor]
                    forward_queue.append((neighbor, new_path))
                    forward_visited[neighbor] = new_path

            # Backward search
            current_word, current_path = backward_queue.popleft()
            
            for neighbor in self._get_neighbors(current_word):
                if neighbor in forward_visited:
                    full_path = forward_visited[neighbor] + current_path[::-1][1:]
                    return full_path

                if neighbor not in backward_visited:
                    new_path = current_path + [neighbor]
                    backward_queue.append((neighbor, new_path))
                    backward_visited[neighbor] = new_path

        return None

    def _get_neighbors(self, word):
        neighbors = []
        for i in range(len(word)):
            for char in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + char + word[i+1:]
                if new_word in self.word_list and new_word != word:
                    neighbors.append(new_word)
        return neighbors

# Main Game Class with Modern Design
class WordLadderGame:
    def __init__(self):
        # Initialize components
        self.fonts = FontManager()
        
        # Load word list
        self.word_list = self._load_dictionary()
        self.solver = WordLadderSolver(self.word_list)
        
        # Game state
        self.start_word = ""
        self.end_word = ""
        self.solution = None
        self.error_message = ""
        self.active_input = None

        # Input boxes with refined positioning
        self.start_input_box = pygame.Rect(WIDTH//2 - 250, 200, 500, 50)
        self.end_input_box = pygame.Rect(WIDTH//2 - 250, 300, 500, 50)
        self.solve_button = pygame.Rect(WIDTH//2 - 150, 400, 300, 60)

        # Hover state for button
        self.button_hover = False

    def _load_dictionary(self):
        try:
            with open('words.txt', 'r') as f:
                return [word.strip().lower() for word in f if 3 <= len(word.strip()) <= 5]
        except FileNotFoundError:
            return ['help', 'heal', 'head', 'tail', 'tell', 'tall']

    def _draw_background(self):
        # Soft gradient background
        for y in range(HEIGHT):
            r = int(245 - y * 0.1)
            g = int(246 - y * 0.1)
            b = int(250 - y * 0.1)
            pygame.draw.line(SCREEN, (r, g, b), (0, y), (WIDTH, y))

    def _draw_input_boxes(self):
        # Start word input with modern styling
        pygame.draw.rect(SCREEN, COLORS['WHITE'], self.start_input_box, border_radius=10)
        pygame.draw.rect(SCREEN, COLORS['PRIMARY'], self.start_input_box, 2, border_radius=10)
        start_text = self.fonts.input_font.render(self.start_word, True, COLORS['TEXT'])
        SCREEN.blit(start_text, (self.start_input_box.x + 15, self.start_input_box.y + 10))
        
        # End word input with modern styling
        pygame.draw.rect(SCREEN, COLORS['WHITE'], self.end_input_box, border_radius=10)
        pygame.draw.rect(SCREEN, COLORS['PRIMARY'], self.end_input_box, 2, border_radius=10)
        end_text = self.fonts.input_font.render(self.end_word, True, COLORS['TEXT'])
        SCREEN.blit(end_text, (self.end_input_box.x + 15, self.end_input_box.y + 10))
        
        # Enhanced button with hover and shadow effect
        button_color = COLORS['HOVER'] if self.button_hover else COLORS['PRIMARY']
        
        # Shadow effect
        shadow_rect = pygame.Rect(self.solve_button.x + 3, self.solve_button.y + 3, 
                                  self.solve_button.width, self.solve_button.height)
        pygame.draw.rect(SCREEN, COLORS['SHADOW'], shadow_rect, border_radius=15)
        
        # Button
        pygame.draw.rect(SCREEN, button_color, self.solve_button, border_radius=15)
        
        # Button text
        solve_text = self.fonts.button_font.render("Find Ladder", True, COLORS['WHITE'])
        solve_text_rect = solve_text.get_rect(center=self.solve_button.center)
        SCREEN.blit(solve_text, solve_text_rect)

    def _display_word_ladder(self):
        if not self.solution:
            return

        # Ladder display with modern, clean look
        ladder_surface = pygame.Surface((300, HEIGHT - 200), pygame.SRCALPHA)
        ladder_surface.fill((255, 255, 255, 200))

        # Title for ladder
        title = self.fonts.input_font.render("Word Ladder", True, COLORS['SECONDARY'])
        title_rect = title.get_rect(centerx=150, top=10)
        ladder_surface.blit(title, title_rect)

        # Render each word in the ladder
        for i, word in enumerate(self.solution):
            word_text = self.fonts.input_font.render(word, True, COLORS['TEXT'])
            word_rect = word_text.get_rect (centerx=150, y=50 + i * 30)
            ladder_surface.blit(word_text, word_rect)

        # Render path length
        length_text = self.fonts.input_font.render(
            f"Path Length: {len(self.solution)}", 
            True, 
            COLORS['PRIMARY']
        )
        length_rect = length_text.get_rect(centerx=150, bottom=ladder_surface.get_height() - 20)
        ladder_surface.blit(length_text, length_rect)

        # Blit ladder surface
        SCREEN.blit(ladder_surface, (WIDTH - 350, 100))

    def run(self):
        clock = pygame.time.Clock()

        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Mouse click events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_input_box.collidepoint(event.pos):
                        self.active_input = 'start'
                    elif self.end_input_box.collidepoint(event.pos):
                        self.active_input = 'end'
                    elif self.solve_button.collidepoint(event.pos):
                        self.solution = self.solver.find_word_ladder(self.start_word, self.end_word)

                # Mouse motion for button hover effect
                if event.type == pygame.MOUSEMOTION:
                    self.button_hover = self.solve_button.collidepoint(event.pos)

                # Keyboard events
                if event.type == pygame.KEYDOWN:
                    if self.active_input == 'start':
                        if event.key == pygame.K_BACKSPACE:
                            self.start_word = self.start_word[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.solution = self.solver.find_word_ladder(self.start_word, self.end_word)
                        else:
                            self.start_word += event.unicode
                    elif self.active_input == 'end':
                        if event.key == pygame.K_BACKSPACE:
                            self.end_word = self.end_word[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.solution = self.solver.find_word_ladder(self.start_word, self.end_word)
                        else:
                            self.end_word += event.unicode

            # Draw everything
            self._draw_background()
            self._draw_input_boxes()
            if self.solution:
                self._display_word_ladder()

            pygame.display.update()
            clock.tick(60)

# Main Execution
if __name__ == "__main__":
    game = WordLadderGame()
    game.run()