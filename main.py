'''Universidad del valle de guatemala
Marco Jurado, Cristian Aguirre, Rodirgo Barrera'''
from Backend.backmain import App


if __name__ == "__main__":
    uri = "neo4j+s://b5ae0841.databases.neo4j.io "
    user = "neo4j"
    password = "L7lYs5A1-8jg-tDnY6Fs52C3jAfz42CTHaeJvfGSgOc"

    app = App(uri,user,password) #instanciar backend y la conexion a Cypher.

    '''
    if monto 
    '''


    # if salir del frontend
    app.close()