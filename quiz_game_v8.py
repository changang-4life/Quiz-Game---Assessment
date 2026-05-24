"""
FINAL VERSION - JADE AKINBO
    - Combined trials
    - Made final changes for logic
"""


import pygame
import time
import os

quiz_questions = {
    1: {
        "question": "What is the Māori name for New Zealand?",
        "options": ["Aotearoa", "Te Ika-a-Māui", "Pounamu", "Te Waka-a-Māui"],
        "answer": "Aotearoa"
    },
    2: {
        "question": "What is the name of the traditional Māori war dance performed by the All Blacks?",
        "options": ["Poi", "Haka", "Kapa Haka", "Waiata"],
        "answer": "Haka"
    },
    3: {
        "question": "What native New Zealand bird is flightless, nocturnal, and the national animal?",
        "options": ["Tui", "Kea", "Kiwi", "Pukeko"],
        "answer": "Kiwi"
    },
    4: {
        "question": "In te reo Māori, what does 'kia ora' mean?",
        "options": ["Goodbye", "Thank you", "Hello", "Good luck"],
        "answer": "Hello"
    },
    5: {
        "question": "What is the largest active volcano on the North Island, in Tongariro National Park?",
        "options": ["Mount Taranaki", "Mount Tongariro", "Mount Ruapehu", "Mount Ngauruhoe"],
        "answer": "Mount Ruapehu"
    },
    6: {
        "question": "What is a 'hangi'?",
        "options": [
            "A traditional Māori song",
            "A traditional Māori method of cooking food underground",
            "A Māori fishing technique",
            "A type of Māori cloak"
        ],
        "answer": "A traditional Māori method of cooking food underground"
    },
    7: {
        "question": "Which New Zealand city is known as the 'Garden City'?",
        "options": ["Wellington", "Auckland", "Dunedin", "Christchurch"],
        "answer": "Christchurch"
    },
    8: {
        "question": "What does the word 'pounamu' refer to?",
        "options": ["Greenstone", "Driftwood", "Volcanic rock", "Sea shell"],
        "answer": "Greenstone"
    },
    9: {
        "question": "What is the Māori name for the North Island?",
        "options": ["Te Waka-a-Māui", "Te Ika-a-Māui", "Aotearoa", "Rakiura"],
        "answer": "Te Ika-a-Māui"
    },
    10: {
        "question": "What is the name of the most common traditional Māori flute?",
        "options": ["Pūtātara", "Kōauau", "Nguru", "Pūkāea"],
        "answer": "Kōauau"
    },
}

pygame.init()
clock = pygame.time.Clock()

score = 0
game_start_time = 0
attribution_text = "Game icon image: https://www.flaticon.com/free-icons/quiz. This game icon has been designed using resources from Flaticon.com"

BLUE  = (173, 216, 230)
GREEN = (0, 200, 100)
RED   = (220, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

main_screen = pygame.display.set_mode((1100, 550))
font = pygame.font.SysFont("Arial", 24)
font_large = pygame.font.SysFont("Arial", 40)
font_small = pygame.font.SysFont("Arial", 14)

pygame.display.set_caption("Quiz Game - Jade Akinbo")
icon = pygame.image.load("brain.png")
pygame.display.set_icon(icon)

STATS_FILE = "game_data.txt"
GAME_LOG_FILE = "game_data.txt"

DEFAULT_STATS = {
    "best_accuracy": 0,
    "best_time": None,
    "games_played": 0,
}


# Screen Class  =================================================

class Screen:
    """Represents a single question screen. Handles drawing and player input."""

    def __init__(self, question_number):
        self.question_number = question_number
        self.question = quiz_questions[question_number]["question"]
        self.options = quiz_questions[question_number]["options"]
        self.answer = quiz_questions[question_number]["answer"]
        self.answered = False

    def draw(self):
        main_screen.fill(BLUE)
        draw_text(self.question, font, BLACK, main_screen, 550, 50, centre=True)
        self.btn_rects = [
            draw_button(main_screen, self.options[0], font, 200, 150, 300, 60, (100, 149, 200)),
            draw_button(main_screen, self.options[1], font, 600, 150, 300, 60, (100, 149, 200)),
            draw_button(main_screen, self.options[2], font, 200, 280, 300, 60, (100, 149, 200)),
            draw_button(main_screen, self.options[3], font, 600, 280, 300, 60, (100, 149, 200)),
        ]
        draw_timer()

    def handle_click(self, pos):
        """Check if a button was clicked. Returns True if the player answered."""
        for i, rect in enumerate(self.btn_rects):
            if rect.collidepoint(pos):
                self.answered = True
                correct = self.options[i] == self.answer
                return correct
        return None

    def run(self):
        """Run this screen until the player picks an answer. Returns True/False."""
        global score
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    result = self.handle_click(event.pos)
                    if result is not None:
                        if result:
                            score += 1
                        show_result(result)
                        return
            pygame.display.update()
            clock.tick(60)


# File I/O  =================================================

def load_stats():
    stats = DEFAULT_STATS.copy()

    if not os.path.exists(STATS_FILE):
        with open(STATS_FILE, "w") as f:
            f.write(f"Best Accuracy = {stats['best_accuracy']}\n")
            f.write(f"Best Time = None\n")
            f.write(f"Games Played = {stats['games_played']}\n")
        print("No stats file found, creating one with default values.")
        return stats

    with open(STATS_FILE, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or "=" not in line:
            continue

        key, _, raw_value = line.partition("=")
        key = key.strip()
        raw_value = raw_value.strip().rstrip("%s")

        try:
            if key == "Best Accuracy":
                stats["best_accuracy"] = float(raw_value)
            elif key == "Best Time":
                stats["best_time"] = None if raw_value == "None" else float(raw_value)
            elif key == "Games Played":
                stats["games_played"] = int(raw_value)
        except ValueError:
            print(f"Warning: could not read '{key}' from the stats file, using default value instead.")

    print("Stats loaded successfully.")
    return stats


def save_stats(stats):
    existing_log_lines = []
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            lines = f.readlines()
        past_separator = False
        for line in lines:
            if line.strip() == "---":
                past_separator = True
            if past_separator:
                existing_log_lines.append(line)

    with open(STATS_FILE, "w") as f:
        f.write(f"Best Accuracy = {stats['best_accuracy']}%\n")
        best_time_value = f"{stats['best_time']:.2f}" if stats['best_time'] is not None else "None"
        f.write(f"Best Time = {best_time_value}s\n")
        f.write(f"Games Played = {stats['games_played']}\n")
        if existing_log_lines:
            f.writelines(existing_log_lines)

    print("Stats saved successfully.")


def export_game_data(accuracy, elapsed):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    separator_exists = False
    if os.path.exists(GAME_LOG_FILE):
        with open(GAME_LOG_FILE, "r") as f:
            for line in f:
                if line.strip() == "---":
                    separator_exists = True
                    break

    with open(GAME_LOG_FILE, "a") as f:
        if not separator_exists:
            f.write("---\n")
        f.write(
            f"[{timestamp}] Score = {score}/10 | Accuracy = {accuracy:.0f}% | Time = {minutes}m {seconds}s\n"
        )

    print("Game data exported successfully.")


def check_high_scores(stats, accuracy, elapsed):
    new_accuracy_record = False
    new_time_record = False

    current_best_accuracy = stats["best_accuracy"]
    current_best_time = stats["best_time"]

    if accuracy > current_best_accuracy:
        stats["best_accuracy"] = accuracy
        stats["best_time"] = elapsed
        new_accuracy_record = True
        new_time_record = True
        print("New best accuracy and time!")

    elif accuracy == current_best_accuracy:
        if current_best_time is None or elapsed < current_best_time:
            stats["best_time"] = elapsed
            new_time_record = True
            print("Same accuracy, but faster time!")

    stats["games_played"] += 1
    return new_accuracy_record, new_time_record


# Drawing Functions  =================================================

def draw_text(text, font, colour, surface, x, y, centre=False):
    text_surface = font.render(text, True, colour)
    if centre:
        text_rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, text_rect)
    else:
        surface.blit(text_surface, (x, y))


def draw_button(surface, text, font, x, y, width, height, colour):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, colour, button_rect, border_radius=8)

    button_font = font
    text_surface = button_font.render(text, True, WHITE)

    font_size = 24
    while text_surface.get_width() > width - 20 and font_size > 12:
        font_size -= 1
        button_font = pygame.font.SysFont("Arial", font_size)
        text_surface = button_font.render(text, True, WHITE)

    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)

    return button_rect


def draw_timer():
    elapsed_so_far = time.time() - game_start_time
    mins = int(elapsed_so_far // 60)
    secs = int(elapsed_so_far % 60)
    draw_text(f"Time: {mins}m {secs}s", font, BLACK, main_screen, 10, 10)


def show_result(correct):
    if correct:
        main_screen.fill(GREEN)
        draw_text("Correct!", font_large, WHITE, main_screen, 550, 275, centre=True)
    else:
        main_screen.fill(RED)
        draw_text("Wrong!", font_large, WHITE, main_screen, 550, 275, centre=True)
    pygame.display.update()
    pygame.time.wait(1000)


def results_screen(elapsed, accuracy, new_accuracy_record=False, new_time_record=False):
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    exported = False  # Tracks whether the player has already exported this game

    running = True
    while running:
        main_screen.fill(BLUE)

        draw_text("Quiz Complete!", font_large, BLACK, main_screen, 550, 100, centre=True)
        draw_text(f"Score: {score} / {len(quiz_questions)}", font, BLACK, main_screen, 550, 180, centre=True)

        # Accuracy row — highlight if new record
        draw_text(f"Accuracy: {accuracy:.0f}%", font, BLACK, main_screen, 550, 240, centre=True)
        if new_accuracy_record:
            draw_text("NEW BEST!", font, (180, 0, 180), main_screen, 760, 240, centre=True)

        # Time row — highlight if new record
        draw_text(f"Time: {minutes}m {seconds}s", font, BLACK, main_screen, 550, 300, centre=True)
        if new_time_record:
            draw_text("NEW BEST!", font, (180, 0, 180), main_screen, 760, 300, centre=True)

        # Export button — grey out after export to prevent duplicate entries
        export_colour = (150, 150, 150) if exported else (100, 149, 200)
        export_btn = draw_button(main_screen, "Save Results", font, 430, 390, 250, 55, export_colour)

        draw_text(attribution_text, font_small, BLACK, main_screen, 10, 525)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not exported and export_btn.collidepoint(event.pos):
                    export_game_data(accuracy, elapsed)
                    exported = True

        pygame.display.update()
        clock.tick(60)

# Game loop =================================================

def game_loop():
    global game_start_time
    stats = load_stats()

    game_start_time = time.time()
    start_time = game_start_time

    # Create a Screen object for each question and run them one at a time
    for question_number in len(quiz_questions) + 1:
        screen = Screen(question_number)
        screen.run()

    elapsed = time.time() - start_time
    accuracy = (score / 10) * 100

    new_accuracy_record, new_time_record = check_high_scores(stats, accuracy, elapsed)
    save_stats(stats)
    results_screen(elapsed, new_accuracy_record, new_time_record)


game_loop()
pygame.quit()