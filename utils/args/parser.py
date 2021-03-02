#-*- coding: utf-8 -*-

"""

This script recongnize entity using the default spacy's ner and the custom trained ner saved in einstein/ner/model/

"""


import spacy

class ArgsParser:
    def __init__(self, settings):
        # Load the pipelines
        self.classic_nlp = spacy.load(settings['languages'][settings['current_language']])
        self.custom_ner_nlp = spacy.load('./ner/model')

    def parse_sentence(self, sentence, entities_to_search):
        """
        Parse a sentence to get all the parameters using the default spacy's ner and a custom ner

        Args:
            sentence (str): the sentence to parse
            entities_to_search (list): a list of entities represented by a dict

        Returns:
            list: a list of entities represented by a dict
        """
        
        # Use default spacy's ner
        document = self.classic_nlp(sentence)

        entities_labels = [entity['type'] for entity in entities_to_search]
        entities_to_return = []

        for entity in document.ents:
            if 'spacy.' + entity.label_ in entities_labels:
                entities_to_return.append({
                    'value': entity.text,
                    'type': 'spacy.' + entity.label_
                })

        # Use custom ner
        doc = self.custom_ner_nlp(sentence)
        for entity in doc.ents:
            if entity.label_ in entities_labels:
                entities_to_return.append({
                    'value': entity.text,
                    'type': entity.label_
                })

        return entities_to_return
