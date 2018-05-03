#!/usr/bin/env python3

"""Spacy needs to be installed"""
"""This is done by:
        pip install -U spacy
    for the language packages:
        python3 -m spacy download en
        python3 -m spacy download nl"""

import spacy

class language_processor():

    def __init__(self, language_code):
        language = language_code[:2]
        self._nlp = spacy.load(language)

    def language_processing(self, sentence):
        doc = self._nlp(sentence)

        for word in doc:
            subtree_span = doc[word.left_edge.i: word.right_edge.i + 1]
            print(word.dep_ + " : " + subtree_span.root.text)

        return None