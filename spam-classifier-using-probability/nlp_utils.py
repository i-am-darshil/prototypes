import spacy
nlp = spacy.load('en_core_web_sm', disable=['parser','ner'])


def normalize(text):
    '''
    Keeping it only if:
      tok.is_alpha: it’s an actual word (no numbers or special characters)
      not tok.is_stop: it’s not a stopword (like “and”, “the”, “is”, etc.)
      not tok.is_punct: it's not punctuation
    
    > normalize("The quick brown foxes were running around!")
    ['quick', 'brown', 'fox', 'run', 'around']
    '''
    doc = nlp(text.lower())
    return [tok.lemma_ for tok in doc if tok.is_alpha and not tok.is_stop and not tok.is_punct]
