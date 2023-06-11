import PySimpleGUI as sg
import itertools
from moviepy.editor import VideoFileClip
from spellchecker import SpellChecker
from words import generate_new_words, find_most_similar_and_order, generate_clue
from game import change_color, end_game

spell = SpellChecker()

def create_windows(codenames1, codenames2, blue_team, red_team, civilians,game_state):
    user_clue = sg.Text('', key="-USER_CLUE-", font=('arcadeclassic', 18))
    print_clue = sg.Text('', key="-COMPUTER_CLUE-", font=('arcadeclassic', 18))
    num_words_str = sg.Text('', key="-NUM_WORDS-", font=('arcadeclassic', 18))
    game_over = [sg.Text('', key="-GAME_OVER-", font = ('arcadeclassic', 30))]
    
    left = [
        [sg.Text('User Clue: ', font=('arcadeclassic', 16)), sg.InputText(key="-USER_CLUE_INPUT-", size = (10,2), pad = (10,0,0,10))],
        [sg.Text('Enter Number: ', font=('arcadeclassic', 16)), sg.InputText(key="-NUM_WORDS_INPUT-", size = (10,2), pad = (10,0,0,10))],
        [user_clue],
        [num_words_str],
        [sg.Column([[sg.Button('Submit Clue', font=('arcadeclassic', 16))]])]   
    ]

    center = [
        [sg.Text('Blue Score:', font=('arcadeclassic', 16)), sg.Text(game_state['blue_score'], key='blue_score', font=('arcadeclassic', 16))],
        [sg.Text('Red Score:', font=('arcadeclassic', 16)), sg.Text(game_state['red_score'], key='red_score', font=('arcadeclassic', 16))]
    ]
    
    right = [
        [sg.Text('Computer Clue: ', font=('arcadeclassic', 16))],
        [print_clue],
        [sg.Column([[sg.Button('Next Clue', font=('arcadeclassic', 16))]])]
    ]
    

    layout = [
        [sg.Column(left, element_justification='left'),
         sg.Column(center, element_justification='center'),
         sg.Column(right, element_justification='right')],
    ]
    
    codenames_iter = itertools.cycle(codenames1)

    for i in range(5):
        row = []
        for j in range(5):
            word = next(codenames_iter)
            row.append(sg.Button(word, key=(i, j), size=(12, 2), font=('arcadeclassic', 12)))
        layout.append(row)
    
    button_row = [
        sg.Button('Exit', font = 'arcadeclassic'), 
        sg.Button('Restart', font = 'arcadeclassic'),
        sg.Text('WE ARE ON THE BLUE TEAM', font=('arcadeclassic', 16), text_color='Blue', pad = (0,10,10,100))
    ]

    layout.append(button_row)
    
    layout.append(game_over)
     
    #Layout2
    
    codenames_iter2 = itertools.cycle(codenames2)
    
    layout2 = []
    for i in range(5):
        row2 = []
        for j in range(5):
            word = next(codenames_iter2)
            if word in blue_team:
                button_color=('blue', 'blue')
            elif word in red_team:
                button_color=('red', 'red')
            elif word in civilians:
                button_color=('gray', 'gray')
            else:
                button_color=('black', 'black')
            row2.append(sg.Button(key=(i, j), button_color = button_color, size=(4, 2)))
        layout2.append(row2)
    
    screen_width, screen_height = sg.Window.get_screen_size()
    window = sg.Window('Codenames Matrix', layout, size=(screen_width // 2, screen_height // 1))
    window2 = sg.Window('Codemaster Matrix', layout2, size=(screen_width // 2, screen_height // 2), finalize=True)
    
    return window, window2
