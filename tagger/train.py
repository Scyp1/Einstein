import random
import json
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

import spacy

from utils.packages_loader import load_packages


def train(settings):
    """
    Train the neural network model with the intents of all the packages

    Args:
        settings (dict): the main settings
    """
    
    paths = settings['paths']

    nlp = spacy.load(settings['languages'][settings['current_language']])

    words = []
    classes = []
    documents = []

    excluded_chars = ['?', '!', '.', ',', ';', ':']

    actions, intents = load_packages(settings)

    # Set up the words list and the classes list for the neural network
    for intent_name in intents:
        intent = intents[intent_name]

        for action_name in intent:
            action = intent[action_name]

            for expression in action['expressions']:
                world_list = [token.lemma_ for token in nlp(expression) if token.lemma_ not in excluded_chars]
                words.extend(world_list)
                documents.append((world_list, action_name))

                if intent_name not in classes:
                    classes.append(action_name)
            

    # Save the words list and classes list
    json.dump(words, open(paths['words'], 'w'))
    json.dump(classes, open(paths['classes'], 'w'))

    training = []
    output_empty = [0] * len(classes)

    # Transform every sentence by a list of number using the words list and the classes list
    for document in documents:
        bag_of_word = []
        word_patterns = document[0]

        for word in words:
            bag_of_word.append(1) if word in word_patterns else bag_of_word.append(0)

        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        training.append([bag_of_word, output_row])

    random.shuffle(training)
    training = np.array(training, dtype=object)

    # Separate the training datas
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])

    # Create the model
    model = Sequential()
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation='softmax'))

    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    # Fit the model
    hist = model.fit(np.array(train_x), np.array(train_y), epochs=50, batch_size=5, verbose=1)

    # Save the model
    model_path = paths['model'].replace('/tagger', '')
    model.save(model_path, hist)

    print('Training neural network done.')