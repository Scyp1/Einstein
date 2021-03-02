#-*- coding: utf-8 -*-

"""

This script prepare the data in ./datas/training_template.json to write it in ./datas/training.json.
With this script, we can use a specific syntax in the json string which make us write less.

"""

import json
import re

def main():
    """
    Prepare the training datas to train the custom named entity recognizer
    """
    
    # Load the training template
    training_template = json.load(open('datas/training_template.json'))
    output = []
    
    # For each entity's examples list
    for entity in training_template:
        
        # For each example sentence in the list
        for sentence in entity['sentences']:
            
            # For each possible value of the entity
            for possible_value in entity['possibles_values']:
                # Make all the possibles example sentences
                new_sentence = sentence.replace('@entity', possible_value)
                new_sentence_object = [new_sentence]
                
                starts = [match.span()[0] for match in re.finditer('@entity', sentence)]
                spans = [(start, start + len(possible_value), entity['entity_type']) for start in starts]
                
                entities_dict = {
                    "entities": spans
                }
                
                new_sentence_object.append(entities_dict)
                output.append(new_sentence_object)
    
    json.dump(output, open('datas/training.json', 'w'))
    
if __name__ == '__main__':
    main()
