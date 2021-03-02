#-*- coding: utf-8 -*-

"""

This script load every packages saved in einstein/packages/
It loads the intents, the actions corresponding to each intent, and the functions corresponding to each action.

"""


import os
import json
from inspect import getmembers, isfunction


def load_packages(settings):
    """
    Load all the packages : their intents and their actions

    Args:
        settings (dict): the main settings

    Returns:
        tuple: the actions dict and the intents dict
    """
    
    packages_path = settings['paths']['packages']

    # Loading actions from packages
    actions = {}
    intents = {}

    for package_name in os.listdir(packages_path):

        # Ignore os directories
        if package_name in ['__pycache__', '.DS_Store', 'template']:
            continue

        # Load the actions
        package = __import__('packages.' + package_name, fromlist=['main'])
        package_module = getattr(package, 'main')
        functions_from_package = getmembers(package_module, isfunction)
        
        for function in functions_from_package:
            action_function = function[1]
            action_name = action_function.__name__
            
            actions[action_name] = action_function
            


        # Load the intents
        package_expressions = json.load(open(packages_path + package_name + '/datas/expressions.json'))[package_name]
        
        # Load the action parameters
        for action_name in package_expressions:
            action = package_expressions[action_name]
            action_expressions = []
            
            for expression in action['expressions']:
                if len(action['parameters']) == 0:
                    action_expressions.append(expression)
                
                for parameter in action['parameters']:
                    for possible_parameter_value in parameter['possibles_values']:
                        action_expressions.append(expression.replace('@' + parameter['name'], possible_parameter_value))
                        
            action['expressions'] = action_expressions
        
        # Update the intents
        intents[package_name] = package_expressions


    return actions, intents