# sentence     = noun-phrase , verb-phrase , ? end of input ? ;
# noun-phrase  = article , { adjective } , noun ;                (* UPDATED *)
# verb-phrase  = [ adverb ] , verb , [ noun_phrase ] ;           (* UPDATED *)
# article      = "the" | "a" ;
# noun         = "man" | "ball" | "woman" | "table" ;
# verb         = "hit" | "took" | "saw" | "liked" ;
# adjective    = "digital" | "virtual" | "cyber" | "pixelated" ; (* NEW *)
# adverb       = "algorithmically" | "securely" | "wirelessly" | "recursively" ; (* NEW *)


class ParserError(Exception): 

    def __init__(self, message): 
        super().__init__(f'PARSER ERROR DETECTED:\n{message}') 


class Parser: # class variable

    EOI= "? end of input ?"
    NOUNS=["man", "woman", "ball", "table"]
    VERBS=["hit" , "took" , "saw" , "liked"]
    ADVERBS=["algorithmically" , "securely" , "wirelessly" , "recursively"]
    ADJECTIVES=["digital", "virtual" ,"cyber" ,"pixelated"]
    ARTICLES=["the", "a"]


    def __init__(self, source):
        self._tokens=iter(source.split()+[self.EOI])
        self.advance()

    def advance(self):
        try:
            self._current=next(self._tokens)
        except StopIteration:
            self._current=None

    def expect(self, expected_tokens): 
        if self._current not in expected_tokens: 
            token_found_str = f'"{self._current}"' 
            expected_tokens_str = \
                ", ".join([f'"{token}"' for token in expected_tokens]) 
            message = (f'Found the token: {token_found_str}\n' 
                       f'But was expecting one of: {expected_tokens_str}')
            raise ParserError(message) 
        original_current = self._current 
        self.advance() 
        return original_current 
    
    # sentence = noun-phrase, verb-phrase, EOI
    def sentence(self):
        self.noun_phrase()
        self.verb_phrase()
        self.expect([self.EOI])

    # article = "the" | "a";
    def article(self):
        self.expect(self.ARTICLES)

    # article + noun
    def noun_phrase(self):
        self.article()
        while self._current in self.ADJECTIVES:
            self.adjective()
        self.noun()

    def verb_phrase(self):
        if self._current in self.ADVERBS:
            self.adverb()
        self.verb()
        if self._current in self.ARTICLES:
            self.noun_phrase()

    def noun(self):
        self.expect(self.NOUNS)

    def verb(self):
        self.expect(self.VERBS)

    def adjective(self):
        self.expect(self.ADJECTIVES)

    def adverb(self):
        self.expect(self.ADVERBS)


if __name__ == '__main__':
    parser_example = Parser('a woman recursively saw a digital ball')
    try:
        parser_example.sentence()
        print('Syntax OK!')
    except ParserError as e:
        print(e)