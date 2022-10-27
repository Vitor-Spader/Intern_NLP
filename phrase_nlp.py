from typing_extensions import Self
import function_nltk as nlp


class phrase_nlp:
    def __init__(self,phrase):
        self.phrase = phrase
        self.phrase_stem = nlp.token_stemm(phrase)
        self.phrase_return = nlp.return_question(self.phrase_stem)

    def __str__(self):
        return f"Frase:{self.phrase} \nToken/Stem:{self.phrase_stem}"

    def get_phrase(self):
        return self.phrase
    def get_stem(self):
        return self.phrase_stem
    def get_return(self):
        return self.phrase_return

