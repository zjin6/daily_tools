from pattern.en import pluralize, conjugate

def get_verb_tenses(word):
    tenses = {
        'infinitive': word,
        '1st singular present': conjugate(word, tense='1sg'),
        '2nd singular present': conjugate(word, tense='2sg'),
        '3rd singular present': conjugate(word, tense='3sg'),
        'plural present': conjugate(word, tense='pl'),
        'present participle': conjugate(word, tense='part'),
        'past tense': conjugate(word, tense='past'),
        'past participle': conjugate(word, tense='ppart')
    }
    return tenses

def get_plural(word):
    return pluralize(word)

# Example list of words
word_list = ['eat', 'run', 'jump']

for word in word_list:
    verb_tenses = get_verb_tenses(word)
    plural = get_plural(word)
    
    print('Word:', word)
    print('Verb Tenses:', verb_tenses)
    print('Plural:', plural)
    print()









