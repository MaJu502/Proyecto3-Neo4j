'''Universidad del valle de guatemala
Marco Jurado, Cristian Aguirre, Rodirgo Barrera'''
from Backend.backmain import App


if __name__ == "__main__":
    uri = "neo4j+s://b5ae0841.databases.neo4j.io "
    user = "neo4j"
    password = "L7lYs5A1-8jg-tDnY6Fs52C3jAfz42CTHaeJvfGSgOc"

    app = App(uri,user,password) #instanciar backend y la conexion a Cypher.

    '''
    motivos de fraude:
        - transferencia o retiro mayor a 1.5 veces el promedio 
        - transferencia o retiro con monto mayor a 100,000
        - transferencia a cuenta ligada a fraude
        - retiro de cuenta ligada a fraude
    accion o pipeline:
        -si se cumple condicion de fraude
            > no se ejecuta la transaccion
            > se bloquea la cuenta
            > se devuelve mensaje de error
        - si no cumple condicion se hace la transaccion
    '''


    # if salir del frontend
    app.close()