"""
Maori NZ Quiz Game by Jade Akinbo
Version 5 - Save Statistics
    - Changes the values inside the appropriate txt files as the user generates more data
    - The user can choose to export the statistics of each game after each play (data is added after every game - game_data.txt)
    - Before the user quits, the game checks whether the player has beaten their previous high score (split into time and accuracy)

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

STATS_FILE = "game_data.txt"
GAME_LOG_FILE = "game_data.txt"  # Per-game export records are appended to the same file

# Default stats structure used when creating a fresh file
DEFAULT_STATS = {
    "best_accuracy": 0,        # Highest accuracy % ever achieved (0-100)
    "best_time": None,         # Fastest completion time in seconds (None = never completed)
    "games_played": 0,         # Total number of completed games
}


def load_stats():
    stats = DEFAULT_STATS.copy()

    if not os.path.exists(STATS_FILE):
        with open(STATS_FILE, "w") as f:
            f.write(f"Best Accuracy = {stats['Best Accuracy']}\n")
            f.write(f"Best Time = {stats['best_time']}\n")
            f.write(f"Games Played = {stats['games_played']}\n")
        print(f"[Stats] No stats file found. Created '{STATS_FILE}' with default values.")
        return stats

    with open(STATS_FILE, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or "=" not in line:
            continue

        key, _, raw_value = line.partition("=")
        key = key.strip()
        raw_value = raw_value.strip()

        try:
            if key == "best_accuracy":
                stats["best_accuracy"] = float(raw_value)
            elif key == "best_time":
                stats["best_time"] = None if raw_value == "None" else float(raw_value)
            elif key == "games_played":
                stats["games_played"] = int(raw_value)
        except ValueError:
            print(f"[Stats] Warning: could not parse '{line}', using default for '{key}'.")

    print(f"[Stats] Loaded from '{STATS_FILE}': {stats}")
    return stats


def save_stats(stats):
    """
    Overwrites game_data.txt with the updated high-score stats block.

    This only touches the three high-score fields (best_accuracy, best_time,
    games_played). Per-game export records appended by export_game_data() are
    stored below a separator line and are preserved by re-reading the file
    first and writing them back after the updated header.

    Parameters:
        stats (dict): the current stats dict, already updated with any new bests.
    """
    # Preserve any per-game log lines that sit below the "---" separator
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
        f.write(f"best_accuracy={stats['best_accuracy']}\n")
        f.write(f"best_time={stats['best_time']}\n")
        f.write(f"games_played={stats['games_played']}\n")
        # Re-write the log section if it existed
        if existing_log_lines:
            f.writelines(existing_log_lines)

    print(f"[Stats] Saved to '{STATS_FILE}': {stats}")


def export_game_data(accuracy, elapsed):
    """
    Appends a single-game record to game_data.txt.

    Called only if the player chooses to export after a game. Each record is
    written below the "---" separator so it is easy to distinguish from the
    high-score header block. The record includes the timestamp, score,
    accuracy, and time taken.

    Parameters:
        accuracy (float) : accuracy percentage for this game (0-100).
        elapsed  (float) : time taken in seconds for this game.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    # If the separator line doesn't exist yet, add it first
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
            f"[{timestamp}] Score = {score}/10 | Accuracy = {accuracy:.0f}% | Time = {minutes}minutes {seconds}seconds\n"
        )

    print(f"[Stats] Game record exported to '{GAME_LOG_FILE}'.") # testing purposes


def check_high_scores(stats, accuracy, elapsed):
    """
    Compares this game's results against the stored high scores and updates
    stats in-place if either record is beaten.

    The two high scores are independent:
        - best_accuracy : beaten if this game's accuracy is strictly higher.
        - best_time     : beaten if this game's time is strictly lower
                          (or no time was previously recorded).

    Parameters:
        stats    (dict)  : the loaded stats dict; mutated directly.
        accuracy (float) : accuracy percentage for this game (0-100).
        elapsed  (float) : time taken in seconds for this game.

    Returns:
        new_accuracy_record (bool): True if a new accuracy high score was set.
        new_time_record     (bool): True if a new time high score was set.
    """
    new_accuracy_record = False
    new_time_record = False

    if accuracy > stats["best_accuracy"]:
        stats["best_accuracy"] = accuracy
        new_accuracy_record = True
        print(f"[Stats] New accuracy record: {accuracy:.0f}%")

    if stats["best_time"] is None or elapsed < stats["best_time"]:
        stats["best_time"] = elapsed
        new_time_record = True
        print(f"[Stats] New time record: {elapsed:.1f}s")

    stats["games_played"] += 1

    return new_accuracy_record, new_time_record


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


def results_screen(elapsed, new_accuracy_record=False, new_time_record=False):
    """
    Displays the end-of-game results screen.

    Shows the player's score, accuracy, and time. If either high score was
    beaten this game, a congratulatory label is shown next to the relevant
    stat. An "Export Results" button lets the player append this game's data
    to game_data.txt; the button turns grey once clicked to confirm the save.

    Parameters:
        elapsed             (float): total time taken in seconds.
        new_accuracy_record (bool) : whether this game set a new accuracy best.
        new_time_record     (bool) : whether this game set a new time best.
    """
    accuracy = (score / 10) * 100
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    exported = False  # Tracks whether the player has already exported this game

    running = True
    while running:
        main_screen.fill(BLUE)

        draw_text("Quiz Complete!", font_large, BLACK, main_screen, 550, 100, centre=True)
        draw_text(f"Score: {score} / 10", font, BLACK, main_screen, 550, 180, centre=True)

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
        export_btn = draw_button(main_screen, "Export Results", font, 375, 390, 250, 55, export_colour)

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
    stats = load_stats()

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
    accuracy = (score / 10) * 100

    # Check whether either high score was beaten and update stats in-place
    new_accuracy_record, new_time_record = check_high_scores(stats, accuracy, elapsed)

    # Persist the updated high scores (and games_played) to game_data.txt
    save_stats(stats)

    # Show results; player can optionally export this game's record from here
    results_screen(elapsed, new_accuracy_record, new_time_record)


game_loop()
pygame.quit()