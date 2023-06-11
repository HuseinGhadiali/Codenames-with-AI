import pygame

pygame.mixer.init()
click_sound = pygame.mixer.Sound('Codenames/button.wav')
score_sound = pygame.mixer.Sound('Codenames/score.wav')
end_game_sound = pygame.mixer.Sound('Codenames/assassin.wav')
win_sound = pygame.mixer.Sound('Codenames/win.wav')

game_state = {
    'blue_score': 0,
    'red_score': 0,
}

custom_color_red = ('#6c757d', '#d00000')
custom_color_blue = ('#6c757d', 'blue')
custom_color_civilians = ('#6c757d','#D3D3D3')
custom_color_assassin = ('#6c757d', '#000000')

def change_color(button, blue_team, red_team, civilians, window, game_state):
    word = button.get_text()
    if word in blue_team:
        button.update(button_color = custom_color_blue)
        game_state['blue_score'] += 1
        window['blue_score'].update(game_state['blue_score'])
        score_sound.play()
        if game_state['blue_score'] == 8:
            end_game("blue", window)
    elif word in red_team:
        button.update(button_color = custom_color_red)
        game_state['red_score'] += 1
        window['red_score'].update(game_state['red_score'])
        click_sound.play()
        if game_state['red_score'] == 8:
            end_game("red", window)
    elif word in civilians:
        button.update(button_color = custom_color_civilians)
        click_sound.play()
    else:
        button.update(button_color = custom_color_assassin)
        window['-GAME_OVER-'].update(f"GAME OVER")
        # End the game if the assassin word is clicked
        for i in range(5):
            for j in range(5):
                button = window[(i, j)]
                button.update(disabled=True)
        end_game_sound.play()

def end_game(winner,window):
    # Disable all buttons and display the winner
    for i in range(5):
        for j in range(5):
            button = window[(i, j)]
            button.update(disabled=True)
    window['-GAME_OVER-'].update(f"{winner.upper()} TEAM WINS!")
    win_sound.play()
