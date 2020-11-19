import re
from urllib import parse, request

def crea_query(texto, autor="", titulo="", ano1="", ano2="", 
               medio=1000, pais=1000, tema=1000, destino=1):
    """
    Destino:
        1  CREA
        2  CORDE
    Pais:
        0  Argentina
        1  Bolivia
        2  Chile
        3  Colombia
        4  Costa Rica
        5  Cuba
        6  Ecuador
        7  El Salvador
        8  EE.UU.
        9  España
        10 Filipinas
        11 Guatemala
        12 Honduras
        13 México
        14 Nicaragua
        15 Panamá
        16 Paraguay
        17 Perú
        18 NO COUNTRY
        19 Puerto Rico
        20 Rep. Dominicana
        21 Uruguay
        22 Venezuela

    Medio:
        0  Libros
        1  Periódicos
        2  Revistas
        3  Miscelánea
        4  Oral
        1000 Todos
    Tema:
        Check online / comprobar en línea
    
    Returns number of occurrences and documents
    """
    
    url = ("http://corpus.rae.es/cgi-bin/crpsrvEx.dll?"
           "MfcISAPICommand=buscar&tradQuery=1&")
    query = ""
    # add params in order
    # Corpus ------
    if destino in [0,1]:
        query += "destino={}&".format(destino)
    else:
        raise Exception("Valores válidos para destino: "
                        "0: CREA, 1: CORDE")
    # Query -----
    query += "texto={}&".format(texto)
    # Author -----
    query += "autor={}&".format(autor)
    # Title -----
    query += "titulo={}&".format(titulo)
    # Beginning year
    query += "ano1={}&".format(ano1)
    # End year -----
    query += "ano2={}&".format(ano2)
    # Means -----
    if  isinstance(medio, int):
        query += "medio={}&".format(medio)
    elif isinstance(medio, list):
        for m in medio:
            query += "medio={}&".format(m)
    else:
        raise Exception("Valores válidos para Medio:"
                       "entero o lista de enteros")
    # Country -----
    if  isinstance(pais, int):
        query += "pais={}&".format(pais)
    elif isinstance(pais, list):
        for p in pais:
            query += "pais={}&".format(p)
    else:
        raise Exception("Valores válidos para Pais:"
                       "entero o lista de enteros")
   # Tema -----
    if  isinstance(tema, int):
        query += "tema={}&".format(tema)
    elif isinstance(pais, list):
        for t in tema:
            query += "tema={}&".format(t)
        query = query[:-1] # remove last &
    else:
        raise Exception("Valores válidos para Tema:"
                       "entero o lista de enteros")
    
    # Parse query into valid format
    query = parse.quote_plus(query, encoding='latin1', safe="=&")
    url = url + query
    print(url)
    
    # Make query
    page = request.urlopen(url).read()

    pattern = "([0-9]+) casos en ([0-9]+) documentos"
    frequency_info = re.search(pattern, page.decode("latin1"))
    if frequency_info:
        return frequency_info.group(1), frequency_info.group(2)
    else:
        return 0, 0



