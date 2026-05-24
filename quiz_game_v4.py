"""
Maori NZ Quiz Game by Jade Akinbo
Version 3 - Load Statistics
    - Handles high score and general game statistics
    - If ther eis no txt file, a new one is created
    - Checks if there are already existing txt files under certain names
    - Checks if there is no txt file, a new one is creates
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

STATS_FILE = "game_stats.txt"

# Default stats structure used when creating a fresh file
DEFAULT_STATS = {
    "best_accuracy": 0,        # Highest accuracy % ever achieved (0-100)
    "best_time": None,         # Fastest completion time in seconds (None = never completed)
    "games_played": 0,         # Total number of completed games
}


def load_statistics():
    """
    Loads game statistics from STATS_FILE.

    If the file does not exist, it is created with default values and those
    defaults are returned. If the file exists but a field is missing or
    corrupted, the missing field falls back to its default value so the
    game never crashes due to a bad stats file.

    Returns a dict with keys:
        best_accuracy (float) : highest accuracy percentage recorded
        best_time (float|None) : fastest time in seconds, or None if no run finished yet
        games_played (int): total completed games
    """
    stats = DEFAULT_STATS.copy()

    if not os.path.exists(STATS_FILE):
        # First run — write a fresh stats file so it exists for future saves
        with open(STATS_FILE, "w") as f:
            f.write(f"best_accuracy={stats['best_accuracy']}\n")
            f.write(f"best_time={stats['best_time']}\n")
            f.write(f"games_played={stats['games_played']}\n")
        print(f"[Stats] No stats file found. Created '{STATS_FILE}' with default values.")
        return stats

    # File exists — read and parse it
    with open(STATS_FILE, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or "=" not in line:
            continue  # Skip blank lines or malformed lines

        key, _, raw_value = line.partition("=")
        key = key.strip()
        raw_value = raw_value.strip()

        try:
            if key == "best_accuracy":
                stats["best_accuracy"] = float(raw_value)

            elif key == "best_time":
                # "None" is stored as the string "None" when no time exists yet
                stats["best_time"] = None if raw_value == "None" else float(raw_value)

            elif key == "games_played":
                stats["games_played"] = int(raw_value)

        except ValueError:
            # Corrupted value — keep the default and warn
            print(f"[Stats] Warning: could not parse '{line}', using default for '{key}'.")

    print(f"[Stats] Loaded from '{STATS_FILE}': {stats}")
    return stats


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
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)
    return button_rect


def show_result(correct):
    if correct:
        main_screen.fill(GREEN)
        draw_text("Correct!", font_large, WHITE, main_screen, 550, 275, centre=True)
    else:
        main_screen.fill(RED)
        draw_text("Wrong!", font_large, WHITE, main_screen, 550, 275, centre=True)
    pygame.display.update()
    pygame.time.wait(1000)


def results_screen(elapsed):
    accuracy = (score / 10) * 100
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    running = True
    while running:
        main_screen.fill(BLUE)

        draw_text("Quiz Complete!", font_large, BLACK, main_screen, 550, 100, centre=True)
        draw_text(f"Score: {score} / 10", font, BLACK, main_screen, 550, 200, centre=True)
        draw_text(f"Accuracy: {accuracy:.0f}%", font, BLACK, main_screen, 550, 260, centre=True)
        draw_text(f"Time: {minutes}m {seconds}s", font, BLACK, main_screen, 550, 320, centre=True)
        draw_text(attribution_text, font_small, BLACK, main_screen, 10, 525)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(60)


def screen1():
    global score
    running = True
    while running:
        main_screen.fill(BLUE)
        question = quiz_questions[1]["question"]
        options = quiz_questions[1]["options"]
        draw_text(question, font, BLACK, main_screen, 550, 50, centre=True)
        button_1 = draw_button(main_screen, options[0], font, 200, 150, 300, 60, (100, 149, 200))
        button_2 = draw_button(main_screen, options[1], font, 600, 150, 300, 60, (100, 149, 200))
        button_3 = draw_button(main_screen, options[2], font, 200, 280, 300, 60, (100, 149, 200))
        button_4 = draw_button(main_screen, options[3], font, 600, 280, 300, 60, (100, 149, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate([button_1, button_2, button_3, button_4]):
                    if button.collidepoint(event.pos):
                        selected = options[i]
                        correct = selected == quiz_questions[1]["answer"]
                        if correct:
                            score += 1
                        show_result(correct)
                        return
        pygame.display.update()
        clock.tick(60)


def screen2():
    global score
    running = True
    while running:
        main_screen.fill(BLUE)
        question = quiz_questions[2]["question"]
        options = quiz_questions[2]["options"]
        draw_text(question, font, BLACK, main_screen, 550, 50, centre=True)
        button_1 = draw_button(main_screen, options[0], font, 200, 150, 300, 60, (100, 149, 200))
        button_2 = draw_button(main_screen, options[1], font, 600, 150, 300, 60, (100, 149, 200))
        button_3 = draw_button(main_screen, options[2], font, 200, 280, 300, 60, (100, 149, 200))
        button_4 = draw_button(main_screen, options[3], font, 600, 280, 300, 60, (100, 149, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate([button_1, button_2, button_3, button_4]):
                    if button.collidepoint(event.pos):
                        selected = options[i]
                        correct = selected == quiz_questions[2]["answer"]
                        if correct:
                            score += 1
                        show_result(correct)
                        return
        pygame.display.update()
        clock.tick(60)


def screen3():
    global score
    running = True
    while running:
        main_screen.fill(BLUE)
        question = quiz_questions[3]["question"]
        options = quiz_questions[3]["options"]
        draw_text(question, font, BLACK, main_screen, 550, 50, centre=True)
        button_1 = draw_button(main_screen, options[0], font, 200, 150, 300, 60, (100, 149, 200))
        button_2 = draw_button(main_screen, options[1], font, 600, 150, 300, 60, (100, 149, 200))
        button_3 = draw_button(main_screen, options[2], font, 200, 280, 300, 60, (100, 149, 200))
        button_4 = draw_button(main_screen, options[3], font, 600, 280, 300, 60, (100, 149, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate([button_1, button_2, button_3, button_4]):
                    if button.collidepoint(event.pos):
                        selected = options[i]
                        correct = selected == quiz_questions[3]["answer"]
                        if correct:
                            score += 1
                        show_result(correct)
                        return
        pygame.display.update()
        clock.tick(60)


def screen4():
    global score
    running = True
    while running:
        main_screen.fill(BLUE)
        question = quiz_questions[4]["question"]
        options = quiz_questions[4]["options"]
        draw_text(question, font, BLACK, main_screen, 550, 50, centre=True)
        button_1 = draw_button(main_screen, options[0], font, 200, 150, 300, 60, (100, 149, 200))
        button_2 = draw_button(main_screen, options[1], font, 600, 150, 300, 60, (100, 149, 200))
        button_3 = draw_button(main_screen, options[2], font, 200, 280, 300, 60, (100, 149, 200))
        button_4 = draw_button(main_screen, options[3], font, 600, 280, 300, 60, (100, 149, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate([button_1, button_2, button_3, button_4]):
                    if button.collidepoint(event.pos):
                        selected = options[i]
                        correct = selected == quiz_questions[4]["answer"]
                        if correct:
                            score += 1
                        show_result(correct)
                        return
        pygame.display.update()
        clock.tick(60)


def screen5():
    global score
    running = True
    while running:
        main_screen.fill(BLUE)
        question = quiz_questions[5]["question"]
        options = quiz_questions[5]["options"]
        draw_text(question, font, BLACK, main_screen, 550, 50, centre=True)
        button_1 = draw_button(main_screen, options[0], font, 200, 150, 300, 60, (100, 149, 200))
        button_2 = draw_button(main_screen, options[1], font, 600, 150, 300, 60, (100, 149, 200))
        button_3 = draw_button(main_screen, options[2], font, 200, 280, 300, 60, (100, 149, 200))
        button_4 = draw_button(main_screen, options[3], font, 600, 280, 300, 60, (100, 149, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate([button_1, button_2, button_3, button_4]):
                    if button.collidepoint(event.pos):
                        selected = options[i]
                        correct = selected == quiz_questions[5]["answer"]
                        if correct:
                            score += 1
                        show_result(correct)
                        return
        pygame.display.update()
        clock.tick(60)


def screen6():
    global score
    running = True
    while running:
        main_screen.fill(BLUE)
        question = quiz_questions[6]["question"]
        options = quiz_questions[6]["options"]
        draw_text(question, font, BLACK, main_screen, 550, 50, centre=True)
        button_1 = draw_button(main_screen, options[0], font, 200, 150, 300, 60, (100, 149, 200))
        button_2 = draw_button(main_screen, options[1], font, 600, 150, 300, 60, (100, 149, 200))
        button_3 = draw_button(main_screen, options[2], font, 200, 280, 300, 60, (100, 149, 200))
        button_4 = draw_button(main_screen, options[3], font, 600, 280, 300, 60, (100, 149, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate([button_1, button_2, button_3, button_4]):
                    if button.collidepoint(event.pos):
                        selected = options[i]
                        correct = selected == quiz_questions[6]["answer"]
                        if correct:
                            score += 1
                        show_result(correct)
                        return
        pygame.display.update()
        clock.tick(60)


def screen7():
    global score
    running = True
    while running:
        main_screen.fill(BLUE)
        question = quiz_questions[7]["question"]
        options = quiz_questions[7]["options"]
        draw_text(question, font, BLACK, main_screen, 550, 50, centre=True)
        button_1 = draw_button(main_screen, options[0], font, 200, 150, 300, 60, (100, 149, 200))
        button_2 = draw_button(main_screen, options[1], font, 600, 150, 300, 60, (100, 149, 200))
        button_3 = draw_button(main_screen, options[2], font, 200, 280, 300, 60, (100, 149, 200))
        button_4 = draw_button(main_screen, options[3], font, 600, 280, 300, 60, (100, 149, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate([button_1, button_2, button_3, button_4]):
                    if button.collidepoint(event.pos):
                        selected = options[i]
                        correct = selected == quiz_questions[7]["answer"]
                        if correct:
                            score += 1
                        show_result(correct)
                        return
        pygame.display.update()
        clock.tick(60)


def screen8():
    global score
    running = True
    while running:
        main_screen.fill(BLUE)
        question = quiz_questions[8]["question"]
        options = quiz_questions[8]["options"]
        draw_text(question, font, BLACK, main_screen, 550, 50, centre=True)
        button_1 = draw_button(main_screen, options[0], font, 200, 150, 300, 60, (100, 149, 200))
        button_2 = draw_button(main_screen, options[1], font, 600, 150, 300, 60, (100, 149, 200))
        button_3 = draw_button(main_screen, options[2], font, 200, 280, 300, 60, (100, 149, 200))
        button_4 = draw_button(main_screen, options[3], font, 600, 280, 300, 60, (100, 149, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate([button_1, button_2, button_3, button_4]):
                    if button.collidepoint(event.pos):
                        selected = options[i]
                        correct = selected == quiz_questions[8]["answer"]
                        if correct:
                            score += 1
                        show_result(correct)
                        return
        pygame.display.update()
        clock.tick(60)


def screen9():
    global score
    running = True
    while running:
        main_screen.fill(BLUE)
        question = quiz_questions[9]["question"]
        options = quiz_questions[9]["options"]
        draw_text(question, font, BLACK, main_screen, 550, 50, centre=True)
        button_1 = draw_button(main_screen, options[0], font, 200, 150, 300, 60, (100, 149, 200))
        button_2 = draw_button(main_screen, options[1], font, 600, 150, 300, 60, (100, 149, 200))
        button_3 = draw_button(main_screen, options[2], font, 200, 280, 300, 60, (100, 149, 200))
        button_4 = draw_button(main_screen, options[3], font, 600, 280, 300, 60, (100, 149, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate([button_1, button_2, button_3, button_4]):
                    if button.collidepoint(event.pos):
                        selected = options[i]
                        correct = selected == quiz_questions[9]["answer"]
                        if correct:
                            score += 1
                        show_result(correct)
                        return
        pygame.display.update()
        clock.tick(60)


def screen10():
    global score
    running = True
    while running:
        main_screen.fill(BLUE)
        question = quiz_questions[10]["question"]
        options = quiz_questions[10]["options"]
        draw_text(question, font, BLACK, main_screen, 550, 50, centre=True)
        button_1 = draw_button(main_screen, options[0], font, 200, 150, 300, 60, (100, 149, 200))
        button_2 = draw_button(main_screen, options[1], font, 600, 150, 300, 60, (100, 149, 200))
        button_3 = draw_button(main_screen, options[2], font, 200, 280, 300, 60, (100, 149, 200))
        button_4 = draw_button(main_screen, options[3], font, 600, 280, 300, 60, (100, 149, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate([button_1, button_2, button_3, button_4]):
                    if button.collidepoint(event.pos):
                        selected = options[i]
                        correct = selected == quiz_questions[10]["answer"]
                        if correct:
                            score += 1
                        show_result(correct)
                        return
        pygame.display.update()
        clock.tick(60)


def game_loop():
    stats = load_statistics()

    start_time = time.time()

    screen1()
    screen2()
    screen3()
    screen4()
    screen5()
    screen6()
    screen7()
    screen8()
    screen9()
    screen10()

    elapsed = time.time() - start_time
    results_screen(elapsed)


game_loop()
pygame.quit()