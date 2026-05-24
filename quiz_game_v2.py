""" Maori NZ Quiz Game by Jade Akinbo
Version 2 - Game Loop
    - Question and Options displayed
    - Set up different screens for different questions
    - Feedback (correct or incorrect)
    - Added score variable
"""

import pygame

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

BLUE  = (173, 216, 230)
GREEN = (0, 200, 100)
RED   = (220, 50, 50)

main_screen = pygame.display.set_mode((1100, 550))
font = pygame.font.SysFont("Arial", 24)


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
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)
    return button_rect


def show_result(correct):
    if correct:
        main_screen.fill(GREEN)
        draw_text("Correct!", font, (255, 255, 255), main_screen, 550, 275, centre=True)
    else:
        main_screen.fill(RED)
        draw_text("Wrong!", font, (255, 255, 255), main_screen, 550, 275, centre=True)
    pygame.display.update()
    pygame.time.wait(1000)


def screen1():
    global score
    bg_colour = BLUE
    running = True
    while running:
        main_screen.fill(bg_colour)
        question = quiz_questions[1]["question"]
        options = quiz_questions[1]["options"]
        draw_text(question, font, (0, 0, 0), main_screen, 550, 50, centre=True)
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
    bg_colour = BLUE
    running = True
    while running:
        main_screen.fill(bg_colour)
        question = quiz_questions[2]["question"]
        options = quiz_questions[2]["options"]
        draw_text(question, font, (0, 0, 0), main_screen, 550, 50, centre=True)
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
    bg_colour = BLUE
    running = True
    while running:
        main_screen.fill(bg_colour)
        question = quiz_questions[3]["question"]
        options = quiz_questions[3]["options"]
        draw_text(question, font, (0, 0, 0), main_screen, 550, 50, centre=True)
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
    bg_colour = BLUE
    running = True
    while running:
        main_screen.fill(bg_colour)
        question = quiz_questions[4]["question"]
        options = quiz_questions[4]["options"]
        draw_text(question, font, (0, 0, 0), main_screen, 550, 50, centre=True)
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
    bg_colour = BLUE
    running = True
    while running:
        main_screen.fill(bg_colour)
        question = quiz_questions[5]["question"]
        options = quiz_questions[5]["options"]
        draw_text(question, font, (0, 0, 0), main_screen, 550, 50, centre=True)
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
    bg_colour = BLUE
    running = True
    while running:
        main_screen.fill(bg_colour)
        question = quiz_questions[6]["question"]
        options = quiz_questions[6]["options"]
        draw_text(question, font, (0, 0, 0), main_screen, 550, 50, centre=True)
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
    bg_colour = BLUE
    running = True
    while running:
        main_screen.fill(bg_colour)
        question = quiz_questions[7]["question"]
        options = quiz_questions[7]["options"]
        draw_text(question, font, (0, 0, 0), main_screen, 550, 50, centre=True)
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
    bg_colour = BLUE
    running = True
    while running:
        main_screen.fill(bg_colour)
        question = quiz_questions[8]["question"]
        options = quiz_questions[8]["options"]
        draw_text(question, font, (0, 0, 0), main_screen, 550, 50, centre=True)
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
    bg_colour = BLUE
    running = True
    while running:
        main_screen.fill(bg_colour)
        question = quiz_questions[9]["question"]
        options = quiz_questions[9]["options"]
        draw_text(question, font, (0, 0, 0), main_screen, 550, 50, centre=True)
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
    bg_colour = BLUE
    running = True
    while running:
        main_screen.fill(bg_colour)
        question = quiz_questions[10]["question"]
        options = quiz_questions[10]["options"]
        draw_text(question, font, (0, 0, 0), main_screen, 550, 50, centre=True)
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
    print(f"Game over! Final score: {score}/10") # print checks, results will be added next version


game_loop()
pygame.quit()