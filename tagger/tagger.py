"""

Module which contain a Tagger class in order to tag sentences with intents.json's tags by
using neural network

"""
import json

import numpy as np
import spacy
from tensorflow.keras.models import load_model

from utils.packages_loader import load_packages

class Tagger:
    """
    This class is the neural network class, used to tag any sentence and
    determine which action launch.
    """
    
    def __init__(self, settings):
        self.settings = settings
        self.paths = self.settings['paths']

        self.nlp = spacy.load(settings['languages'][settings['current_language']])

        self.words = json.load(open(self.paths['words'], 'r'))
        self.classes = json.load(open(self.paths['classes'], 'r'))
        self.actions, self.intents = load_packages(settings)

        self.model = load_model(self.paths['model'])

    def bag_of_word(self, sentence):
        """
        Transform a sentence to a bag of word, understandable by the neural network

        Args:
            sentence (str): the sentence to transform

        Returns:
            numpy.ndarray: the bag of word
        """
        
        sentence_words = [token.lemma_ for token in self.nlp(sentence)]
        bag = [0] * len(self.words)

        for w in sentence_words:
            for i, word in enumerate(self.words):
                if w == word:
                    bag[i] = 1

        return np.array(bag)

    def predict_classes(self, sentence):
        """
        Use the neural network model to predict the intent of a sentence

        Args:
            sentence (str): the sentence to tag

        Returns:
            list: the list of all the intent and their probabilities
        """
        
        bow = self.bag_of_word(sentence)
        res = self.model.predict(np.array([bow]))[0]

        ERROR_THRESHOLD = 0.5

        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

        results.sort(key=lambda x: x[1], reverse=True)

        return_list = []

        for r in results:
            return_list.append({'action': self.classes[r[0]], 'probability': r[1]})

        return return_list

    def get_response(self, actions_probabilities):
        """
        Get the response from the lift of prediction : which actions to launch

        Args:
            actions_probabilities (list): the list of all the intents and prob

        Returns:
            dict: a dict which contain : the intent, the action and the probability
        """
        
        action_tag = actions_probabilities[0]['action']
        probability = actions_probabilities[0]['probability']

        for intent_name in self.intents:
            intent = self.intents[intent_name]

            for action_name in intent:
                if action_name == action_tag:
                    intent_tag = intent_name
                    break

        for intent_name in self.intents:
            intent = self.intents[intent_name]

            if intent_name == intent_tag:
                result = {
                    'intent': intent_tag,
                    'action': action_tag,
                    'probability': probability
                }
                break

        return result

    def tag_sentence(self, sentence):
        """
        Combine the action of 2 function to write less code

        Args:
            sentence (str): the sentence to tag

        Returns:
            dict: the dict returned by self.get_response()
        """
        
        actions_probabilities = self.predict_classes(sentence)
        response = self.get_response(actions_probabilities)

        return response