#-*- coding: utf-8 -*-

"""

This script train the custom named entity recognizer with examples in ./datas/training.json.
It save the model in ./einstein/ner/model/

"""

import random
import json

import spacy
from spacy.training import Example
from spacy.util import minibatch

# Define script variables
model = './ner/model/'
epochs = 100

TRAINING_DATA = json.load(open('./ner/datas/training.json'))

# This is just in order to test the ner precision at the end of the training
# SPOILER : the precision is not good, not good at all
test_sample = 'How can you be like yesterday ?'

# If we don't have any model yet, create new one
if model is not None:
    nlp = spacy.load(model)
else:
    nlp = spacy.blank('en')

# Get the ner pipe from the pipeline
if 'ner' not in nlp.pipe_names:
    ner = nlp.add_pipe('ner', last=True)
else:
    ner = nlp.get_pipe('ner')

# Train the model
def train():
    """
    Train the custom named entity recognizer
    """
    
    # Add all the entities's labels to the ner
    for sentence, annotations in TRAINING_DATA:
        for entity in annotations.get('entities'):
            ner.add_label(entity[2])

    # Search for all the other pipe
    pipe_exceptions = ['ner']
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

    # Disable all the other pipes to train only the ner
    with nlp.disable_pipes(*other_pipes):
        if model is None:
            nlp.begin_training()
            
        examples = []
        
        # Get the example
        for text, annotations in TRAINING_DATA:
            examples.append(Example.from_dict(nlp.make_doc(text), annotations))

        nlp.initialize(lambda: examples)
        
        # Train the ner
        for _ in range(epochs):
            random.shuffle(examples)

            for batch in minibatch(examples, size=8):
                nlp.update(batch)

    # Save the ner
    nlp.to_disk('./ner/model/')

# Test it with the test sentence
def test():
    """
    Test the custom named entity recognizer to see if everything worked
    """
    doc = nlp(test_sample)
    print(test_sample)
    print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
    print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])
    
if __name__ == '__main__':
    train()
    test()