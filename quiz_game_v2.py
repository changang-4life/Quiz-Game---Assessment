""" Maori NZ Quiz Game by Jade Akinbo
Version 2 - Game Loop
    - Question and Options displayed
    - Set up different screens for different questions
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

main_screen = pygame.display.set_mode((1100, 550))
font = pygame.font.SysFont("Arial", 24)


def draw_text(text, font, colour, surface, x, y):
    text_surface = font.render(text, True, colour)
    surface.blit(text_surface, (x, y))


def screen1():
    running = True
    while running:
        main_screen.fill((230, 28, 68))

        question = quiz_questions[1]["question"]
        draw_text(question, font, (255, 255, 255), main_screen, 350, 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(60)


def game_loop():
    screen1()


game_loop()