import re
from urllib import parse, request
import pandas as pd

def get_dle_verb(verb):
    """
    Returns the conjugation table from the Diccionario
    de la Lengua Española (RAE) as a pandas data table.
    Verb must be in infinitive form.
    """
    search_string = parse.quote(verb, encoding='utf-8')
    url = 'https://dle.rae.es/{}?m=form#conjugacion'.format(search_string)
    req = request.Request(url)
    req.add_header(
    'User-agent',
    'Mozilla/5.0',
    )
    page = request.urlopen(req).read().decode('utf-8')
    tbl = pd.read_html(page)[0]
    return tbl

def make_conjug_dict(verb):
    """
    Create a dictionary with given verb's conjugation as given in
    Diccionario de la Lengua Española (RAE).
    Verb must be in infinitive form.
    """
    tbl = get_dle_verb(verb)
    tbl_indices = {
        'presente':[-2, 5],
        'pretérito':[-2,14],
        'imperfecto':[-1,5],
        'condicional':[-1,23], 
        'futuro':[-1,14],
        'presente subj': [-2,33],
        'imperfecto subj': [-1,42]
        }

    conjug = {
            'infinitivo': [tbl.iloc[0,-2]],
            'gerundio': [tbl.iloc[0,-1]],
            'participio': [tbl.iloc[2,-2]],
            'presente':[],
            'pretérito':[],
            'pretérito perf':[],
            'pretérito pluscuam':[],
            'imperfecto':[], 
            'futuro':[],
            'condicional':[],
            'presente subj': [],
            'imperfecto subj': [],
            'presente durativo': []
            }
    
    # positions of verb forms of interest relative
    # to start index
    poss = [0,1,3,4,5,6]
    
    for verb_form in tbl_indices.keys():
        start = tbl_indices[verb_form][1]
        column = tbl_indices[verb_form][0]
        for pos in poss:
            form = tbl.iloc[start+pos, column]
            # tú / vos case
            if verb_form == 'presente' and pos == 1:
                form = form.split(' / ')[0]
            # imperfecto subj case
            if verb_form == 'imperfecto subj':
                form = form.split(' o ')
                # add two forms at once
                conjug[verb_form] = conjug[verb_form] + form
            else:
                # add to conjug dict
                conjug[verb_form].append(form)
    
    # pretérito perfecto
    auxiliares = ['he', 'has','ha','hemos','habéis','han']
    for aux in auxiliares:
        form = aux + ' ' + conjug['participio'][0]
        conjug['pretérito perf'].append(form)

    # pretértico pluscuamperfecto
    auxiliares = ['había', 'habías','había','habíamos','habíais','habían']
    for aux in auxiliares:
        form = aux + ' ' + conjug['participio'][0]
        conjug['pretérito pluscuam'].append(form)

    # presente continuo: estar + gerundio
    auxiliares = ['estoy', 'estás', 'está', 'estamos', 'estáis', 'están']
    for aux in auxiliares:
        form = aux + ' ' + conjug['gerundio'][0]
        conjug['presente durativo'].append(form)

    return conjug
    
def get_verb_crea_frequency(verb, country=9):
    """
    Get raw number of cases and documents of given verb
    in different conjugation forms from CREA corpus in given
    country (Spain: 9)

    Return a pandas dataframe
    """
    frequency_dict = {}
    conjug = make_conjug_dict(verb)

    for verb_conjug in conjug.keys():
        forms = list(set(conjug[verb_conjug])) # remove duplicate forms

        # Create uppercase versions. Add quotes in compound verbs.
        if verb_conjug in ['pretérito perf', 'pretérito pluscuam',\
                            'presente durativo']:
            lowercase = ["'" + word + "'" for word in forms]
            capitals = ["'" + word.capitalize() + "'" \
                    for word in forms]
            uppercase = ["'" + word.upper() + "'" for word in forms]
            search_string = ' o '.join(lowercase + capitals + uppercase)
        else:
            capitals = [word.capitalize() for word in forms]
            uppercase = [word.upper() for word in forms]
            search_string = ' o '.join(forms + capitals + uppercase)
        
        search_string = parse.quote_plus(search_string, encoding='latin1')
        url = ('http://corpus.rae.es/cgi-bin/crpsrvEx.dll?MfcISAPICommand=buscar'
                '&tradQuery=1&destino=0&texto={}&autor=&titulo=&ano1=&ano2=&'
                'medio=1000&pais={}&tema=1000')
        url = url.format(search_string, country)

        page  = request.urlopen(url).read()
        pattern = '([0-9]+) casos en ([0-9]+) documentos'
        frequency_info = re.search(pattern, page.decode('latin1'))
        if frequency_info:
            frequency_dict[verb_conjug] = (frequency_info.group(1),
                                           frequency_info.group(2))
        else:
            frequency_dict[verb_conjug] = (0, 0)

        frequency_df = pd.DataFrame(frequency_dict)
        # make sure all columns have the same order
        frequency_df = frequency_df.reindex(columns=sorted(frequency_df.columns))
        frequency_df['verb'] = verb
        frequency_df['type'] = ['token', 'document']
    return frequency_df
