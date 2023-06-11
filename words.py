import random
import pickle
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from scipy.spatial.distance import cdist
import numpy as np
import string


wnl = WordNetLemmatizer()

def is_plural(word):
    singular = wnl.lemmatize(word, pos=wordnet.NOUN)
    return singular != word

def has_punctuation(word):
    return any(char in string.punctuation for char in word)

def generate_new_words(words):
    random_words = list(words)
    random.shuffle(random_words)
    blue_team = random.sample(random_words, 8)
    red_team = random.sample(set(random_words) - set(blue_team), 8)
    civilians = random.sample(set(random_words) - set(blue_team) - set(red_team), 8)
    assassin = random.sample(set(random_words) - set(blue_team) - set(red_team) - set(civilians), 1)
    codenames = blue_team + red_team + civilians + assassin
    random.shuffle(codenames)
    return codenames, blue_team, red_team, civilians, assassin

def find_most_similar_and_order(user_clue, num_words, codenames, glove, window):
    # Calculate the cosine similarity between the user_clue word and each word in the codenames list
    similarity_scores = []
    for word in codenames:
        if word in glove:
            try:
                similarity_score = np.dot(glove[user_clue], glove[word]) / (np.linalg.norm(glove[user_clue]) * np.linalg.norm(glove[word]))
                similarity_scores.append(similarity_score)
            except KeyError:
                # Update the '-USER_CLUE-' element with a message
                window['-USER_CLUE-'].update("Sorry this word does not exist. Try again!")
                return []
        else:
            similarity_scores.append(-0.5) # assign a default similarity score for out-of-vocabulary words

    # Order the word list based on the cosine similarity scores
    ordered_word_list = [word for _, word in sorted(zip(similarity_scores, codenames), reverse=True)]

    return ordered_word_list[:num_words]

def generate_clue(blue_team_words, glove, topn=10):
    target_word = random.choice(blue_team_words)
    
    # Find the most similar words to the target word
    if target_word not in glove:
        most_similar_words = []
    else:
        target_word_vector = glove[target_word]
        glove_filtered = {k: v for k, v in glove.items() if v.shape == target_word_vector.shape}
        distances = cdist(target_word_vector.reshape(1,-1), np.vstack(list(glove_filtered.values())), 'cosine')[0]
        sorted_distances = np.argsort(distances)
        closest_words = [list(glove_filtered.keys())[i] for i in sorted_distances[:topn+1]]
        most_similar_words = [w for w in closest_words if w != target_word and not is_plural(w) and not w.endswith('ing') and not w.endswith('ed') and not has_punctuation(w)][:topn]
    
    most_similar_word = random.choice(most_similar_words)
    clue = f"{most_similar_word.title()}"
    # Calculate the number of words on the game board that are similar to the most_similar_word
    num_words = 1
    for word in most_similar_words:
        ordered_words = find_most_similar_and_order(word, topn, blue_team_words, glove, window=None)
        if most_similar_word in ordered_words:
            num_words += 1
    return clue, num_words
