from tagger.tagger import Tagger

import tagger.train as tagger_train
import ner.train as ner_train

from utils.args.parser import ArgsParser

from utils.packages_loader import load_packages

import json
import argparse
import sys

# Load settings/config
settings = json.load(open('settings.json', 'r'))
paths = settings['paths']

# Training
parser = argparse.ArgumentParser()

parser.add_argument('-t',
                    '--train',
                    action='store_true'
                    )

args = parser.parse_args()

if args.train:
    tagger_train.train(settings)
    ner_train.train()
    sys.exit()

# Load the argument parser
args_parser = ArgsParser(settings)

# Load datas
actions, intents = load_packages(settings)

# Load the neural network model
nn_tagger = Tagger(settings)


while True:
    message = input('> ')

    if message == 'exit':
        break

    # Get the result from the neural network
    result_from_nn = nn_tagger.tag_sentence(message)

    # If the neural network is sure of what it predicted
    if result_from_nn['probability'] > 0.7:

        # Load the action's function
        action_function = actions[result_from_nn['action']]
        action_name = result_from_nn['action']

        # Load the parameters of this function
        action_parameters = [intents[intent_name][action_name]['parameters'] for intent_name in intents if intent_name == result_from_nn['intent']][0]

        # Get all the parameters which were included in the message
        sentence_parameters = args_parser.parse_sentence(message, action_parameters)
        sentence_parameters_types = [parameter['type'] for parameter in sentence_parameters]

        # This are the parameters whiches will be passed to the action's function
        parameters_to_function = []

        for action_parameter in action_parameters:
            parameter_to_function = None

            # Search the corresponding parameter to the action's one in the sentence
            for sentence_parameter in sentence_parameters:
                if sentence_parameter['type'] == action_parameter['type']:
                    parameter_to_function = sentence_parameter
                    parameter_to_function['name'] = action_parameter['name']
                    break

            # Add it to the parameters which will be passed to the action's function
            if action_parameter['type'] in sentence_parameters_types:
                parameters_to_function.append(parameter_to_function)


        # Print what will return the action's function
        print(action_function(parameters_to_function))
        
        # Stop the bot if the user says goodbye
        if result_from_nn['action'] == 'goodbye':
            break
    else:
        # Else, (that means that the chatbot didn't understand the message) just say that he didn't understand
        print('I do not understand you, sorry.')
