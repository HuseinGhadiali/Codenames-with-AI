import pickle
import random
import threading
from words import generate_new_words, find_most_similar_and_order, generate_clue
from game import change_color, end_game, game_state, click_sound
from ui import create_windows
import pygame
import PySimpleGUI as sg
from spellchecker import SpellChecker
from loadingscreen import play_video

# Call the play_video function from loadingscreen.py
play_video()

# Load the words list from the file
with open('Codenames/words.pkl', 'rb') as f:
    words = pickle.load(f)

# Generate words
codenames, blue_team, red_team, civilians, assassin = generate_new_words(words)
codenames1 = codenames.copy()
codenames2 = codenames.copy()
blue_team1 = blue_team.copy()
game_state = {
    'blue_score': 0,
    'red_score': 0,
}

# Create windows
themes = sg.theme_list()
theme = random.choice(themes)
sg.theme(theme)
window, window2 = create_windows(codenames1, codenames2, blue_team, red_team, civilians,game_state)

# Initialize the mixer module
pygame.mixer.init()
# Load the sound effects
click_sound = pygame.mixer.Sound('Codenames/button.wav')
score_sound = pygame.mixer.Sound('Codenames/score.wav')
end_game_sound = pygame.mixer.Sound('Codenames/assassin.wav')
win_sound = pygame.mixer.Sound('Codenames/win.wav')

with open('Codenames/gloveupdated1.pkl', 'rb') as f:
    glove = pickle.load(f)

# Create windows
window, window2 = create_windows(codenames1, codenames2, blue_team, red_team, civilians, game_state)

blue_team_words = blue_team.copy()
# Create a SpellChecker object
spell = SpellChecker()
while True:
    event2, values2 = window2.read(timeout=100)
    if event2 == sg.WINDOW_CLOSED:
        break
    event, values = window.read()
    if event in (None, 'Exit'):
        break
     # Exit button
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break
    # Restart button
    if event == 'Restart':
        # Reset the game state  
        game_state = {
            'blue_score': 0,
            'red_score': 0,
        }

        # Generate new words
        codenames, blue_team, red_team, civilians, assassin = generate_new_words(words)
        codenames1 = codenames.copy()
        codenames2 = codenames.copy()
        blue_team1 = blue_team.copy()

         # Update the blue_team_words list with the new blue team words
        blue_team_words = blue_team.copy()

        # Close and recreate the windows
        window.close()
        window2.close()

        # All themes available in PySimpleGUI
        themes = sg.theme_list()
        theme = random.choice(themes)
        sg.theme(theme)
        window, window2 = create_windows(codenames1, codenames2, blue_team, red_team, civilians,game_state)
    elif event == 'Submit Clue':
        user_clue = values["-USER_CLUE_INPUT-"].lower()
        # Check if the user's input word is spelled correctly
        misspelled = spell.unknown([user_clue])
        if misspelled:
            # Get the most likely correction
            correction = spell.correction(user_clue)
            # Replace the user's input word with the correction
            user_clue = correction
        window["-USER_CLUE-"].update(user_clue)
        num_words_str = values["-NUM_WORDS_INPUT-"]
        window["-NUM_WORDS-"].update(num_words_str)
        try:
            num_words = int(num_words_str)  # convert the value to an integer
        except ValueError:
            num_words = 0
        comp_guess = find_most_similar_and_order(user_clue, num_words, codenames, glove, window)
        for i in range(5):
            for j in range(5):
                button = window[(i, j)]
                if num_words == 0:
                    window['-USER_CLUE-'].update(f"Please Enter Valid Clue")
                else:
                    for word in comp_guess[:num_words]:
                        if game_state['blue_score'] == 8:
                            end_game("blue", window)
                        elif game_state['red_score'] == 8:
                            end_game("red", window)    
                        elif word == button.get_text():
                            change_color(button, blue_team, red_team, civilians, window, game_state)
                            if word in blue_team:
                                codenames.remove(word)
                                blue_team_words.remove(word)
                            elif word in red_team:
                                codenames.remove(word)
                            elif word in civilians:
                                codenames.remove(word)
                            else:
                                pass
                        else:
                            pass
    elif event == 'Next Clue':
        if len(blue_team_words) != 0:
            clue, num_words = generate_clue(blue_team_words, glove)
            window["-COMPUTER_CLUE-"].update(clue)
            window["-NUM_WORDS-"].update(num_words)
        else:
            pass
    elif isinstance(event, tuple): # Check if a button was clicked
        button = window[event]
        change_color(button, blue_team, red_team, civilians, window, game_state)
        word = button.get_text()
        if word in blue_team:
            blue_team_words.remove(word)
            click_sound.play()
            if len(blue_team_words) == 0:
                pass
window.close()
window2.close()
