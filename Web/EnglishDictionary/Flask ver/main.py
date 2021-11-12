from flask import Flask, render_template, request
from PyDictionary import PyDictionary

app = Flask(__name__)

@app.route('/')
def base():
    ''' Loads a title/main page '''
    return render_template('base.html')

@app.route('/word')
def word_view():
    ''' Loads a page with word data or an error page'''
    word = request.args.get('search')
    dictionary = PyDictionary()
    try:
        # get definition from API
        definition = dictionary.meaning(word).items()
    except AttributeError:
        # PyDictionary returns an empty dict, no definitions found
        return render_template('error.html')
    # get synonyms and antonyms from API
    # empty list if no words found
    synonyms = dictionary.synonym(word) or []
    synonyms =  ', '.join(synonyms[:5])
    antonyms = dictionary.antonym(word) or []
    antonyms = ', '.join(antonyms[:5])
    # pass word, definitions(dict), first five synonyms and antonyms to render
    return render_template('word.html', word=word, definition=definition, synonyms=synonyms, antonyms=antonyms)


