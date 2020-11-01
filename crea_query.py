from urllib import parse, request

def crea_query(busqueda, autor="", titulo="", ano1="", ano2="", 
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

    """
    
    url = ("http://corpus.rae.es/cgi-bin/crpsrvEx.dll?"
           "MfcISAPICommand=buscar&tradQuery=1&")
    params = {'destino': destino,
              'texto': busqueda,
              'autor': autor,
              'titulo': titulo,
              'ano1': ano1,
              'ano2': ano2,
              'medio': medio,
              'pais': pais,
              'tema': tema
             }

#https://stackoverflow.com/questions/2506379/add-params-to-given-url-in-python
