from django.shortcuts import render
from PyDictionary import PyDictionary


def main_view(request):
    '''Loads a title page'''
    return render(request, 'base.html')


def word_view(request):
    ''' Loads a page with word data or an error page'''
    word = request.GET.get('search')
    dictionary = PyDictionary()
    try:
        definition = dictionary.meaning(word).items()
    except AttributeError:
        # PyDictionary returns an empty dict, no definitions found
        return render(request, 'error.html')
    # empty list if no words found
    synonyms = dictionary.synonym(word) or []
    antonyms = dictionary.antonym(word) or []
    # pass word, definitions(dict), first five synonyms and antonyms to render
    context = {
        'word': word,
        'definition': definition,
        'synonyms': ', '.join(synonyms[:5]),
        'antonyms': ', '.join(antonyms[:5])
    }
    return render(request, 'word.html', context)
