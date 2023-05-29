'''Universidad del valle de guatemala
Marco Jurado, Cristian Aguirre, Rodrigo Barrera
app.py'''

from neo4j import GraphDatabase
import logging
from datetime import datetime
from neo4j.exceptions import ServiceUnavailable

class App:
    def __init__(self, uri, user, password) -> None:
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    def close(self):
        self.driver.close()