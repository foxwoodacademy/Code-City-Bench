from translate import Translator

class InternationalizationEngine:
    def __init__(self, target_lang='en'):
        self.target_lang = target_lang

    def translate_narrative(self, text, to_lang):
        translator = Translator(to_lang=to_lang)
        return translator.translate(text)
