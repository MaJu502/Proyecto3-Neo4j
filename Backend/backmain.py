'''Universidad del valle de guatemala
Marco Jurado, Cristian Aguirre, Rodrigo Barrera
app.py'''

from neo4j import GraphDatabase
import logging
from datetime import datetime
from neo4j.exceptions import ServiceUnavailable

# Constantes
ACTUALIZADO_MSG = ' >> Actualizado!'
ARROW_MSG = ' --> '


class BackendConn:
    def __init__(self, uri, user, password) -> None:
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, node_labels, attributes):
        '''
        necesita:
            - lista de labels del nodo
            - atributos del nodo
        '''
        query = f"CREATE (n:{':'.join(node_labels)} {{ {', '.join([f'{k}: ${k}' for k in attributes.keys()])} }}) RETURN n "
        with self.driver.session(database="neo4j") as session:
            result = session.run(query, **attributes)
            node = result.single()[0]
            print(f' >> Node creado: {node}')
            return node

    def create_transaccion_relationship(self, account1_number, account2_number, transaction_number, divisa, monto, fecha, tipo_cuenta):
        '''
        necesita:
            - account1_number: número de cuenta de origen
            - account2_number: número de cuenta de destino
            - transaction_number: número de transferencia
            - divisa: divisa de la transferencia
            - monto: monto de la transferencia
            - fecha: fecha o timestamp de la transferencia
            - tipo_cuenta: tipo de cuenta de destino
        '''
        with self.driver.session(database="neo4j") as session:
            result1 = session.run(
                "MATCH (cuenta1:Cuenta {numero_cuenta: $account1_number}) "
                "MATCH (t2:Transferencia {numero_transferencia: $transaction_number}) "
                "MERGE (cuenta1)-[transaccion:REALIZA]->(t2) "
                "ON CREATE SET transaccion.divisa = $divisa, transaccion.monto = $monto, transaccion.fecha = $fecha "
                "ON MATCH SET transaccion.monto = transaccion.monto + $monto ",
                account1_number=account1_number,
                transaction_number=transaction_number,
                divisa=divisa,
                monto=monto,
                fecha=fecha
            )
            print(
                f" >> REALIZA: Transaction relationship created from {account1_number} to {transaction_number}")

            result2 = session.run(
                "MATCH (t1:Transferencia {numero_transferencia: $transaction_number}) "
                "MATCH (cuenta2:Cuenta {numero_cuenta: $account2_number}) "
                "MERGE (t1)-[transaccion:INVOLUCRA]->(cuenta2) "
                "ON CREATE SET transaccion.divisa = $divisa, transaccion.tipo_cuenta = $tipo_cuenta, transaccion.fecha = $fecha "
                "ON MATCH SET transaccion.monto = transaccion.monto + $monto ",
                transaction_number=transaction_number,
                account2_number=account2_number,
                divisa=divisa,
                tipo_cuenta=tipo_cuenta,
                monto=monto,
                fecha=fecha
            )
            print(
                f" >> INVOLUCRA: Transaction relationship created from {transaction_number} to {account2_number}")
            return [result1, result2]

    def create_fraud_relationship_transferencia(self, transferencia_numero, fraud_id, cuenta_numero, motivo, monto, fecha):
        '''
        necesita:
            - transferencia_numero: número de la transferencia
            - fraud_id: ID del nodo Fraud
            - cuenta_numero: número de cuenta
            - motivo: motivo de la relación Fraud
            - monto: monto de la relación Fraud
            - fecha: fecha o timestamp de la relación Fraud
        '''
        with self.driver.session(database="neo4j") as session:
            result1 = session.run(
                "MATCH (t:Transferencia {numero_transferencia: $transferencia_numero}) "
                "MATCH (f:Fraude {numero_fraude: $fraud_id}) "
                "MERGE (t)-[rel:GENERO]->(f) "
                "ON CREATE SET rel.motivo = $motivo, rel.monto = $monto, rel.fecha = $fecha ",
                transferencia_numero=transferencia_numero,
                fraud_id=fraud_id,
                motivo=motivo,
                monto=monto,
                fecha=fecha
            )
            print(
                f" >> GENERO: Fraud relationship created for Transferencia {transferencia_numero} and Fraud {fraud_id}")

            result2 = session.run(
                "MATCH (c:Cuenta {numero_cuenta: $cuenta_numero}) "
                "MATCH (f:Fraude {numero_fraude: $fraud_id}) "
                "MERGE (c)-[rel:INVOLUCRADA_EN]->(f) "
                "ON CREATE SET rel.motivo = $motivo, rel.numero_cuenta = $cuenta_numero, rel.fecha = $fecha ",
                cuenta_numero=cuenta_numero,
                fraud_id=fraud_id,
                motivo=motivo,
                fecha=fecha
            )
            print(
                f" >> INVOLUCRADA_EN: Fraud relationship created for Cuenta {cuenta_numero} and Fraud {fraud_id}")

            return [result1, result2]

    def create_owner_relationship(self, cuenta_numero, cliente_id, inicio_propiedad, fecha, comentarios):
        '''
        necesita:
            - cuenta_numero: número de la cuenta
            - cliente_id: DPI del cliente
            - inicio_propiedad: fecha de inicio de propiedad
            - fecha: fecha de la operacion actual o timestamp actual
            - comentarios: comentarios adicionales
        '''
        with self.driver.session(database="neo4j") as session:
            result1 = session.run(
                "MATCH (c:Cliente {DPI: $cliente_id}) "
                "MATCH (c1:Cuenta {numero_cuenta: $cuenta_numero}) "
                "MERGE (c)-[rel:ES_PROPIETARIO_DE]->(c1) "
                "ON CREATE SET rel.fecha_inicio_propiedad = $inicio_propiedad, rel.fecha = $fecha, rel.comentarios = $comentarios ",
                cliente_id=cliente_id,
                cuenta_numero=cuenta_numero,
                inicio_propiedad=inicio_propiedad,
                fecha=fecha,
                comentarios=comentarios
            )
            print(
                f" >> ES_PROPIETARIO_DE: Ownership relationship created for client {cliente_id} on account {cuenta_numero}")

            result2 = session.run(
                "MATCH (c:Cliente {DPI: $cliente_id}) "
                "MATCH (c1:Cuenta {numero_cuenta: $cuenta_numero}) "
                "MERGE (c1)-[rel:TIENE]->(c)"
                "ON CREATE SET rel.titular = $titular, rel.fecha = $fecha, rel.beneficiario = $beneficiario ",
                cliente_id=cliente_id,
                cuenta_numero=cuenta_numero,
                titular=True,
                fecha=fecha,
                beneficiario=True
            )
            print(
                f" >> TIENE: relationship created for client {cliente_id} on account {cuenta_numero}")

            return [result1, result2]

    def create_tiene_cuenta_relationship(self, cuenta_numero, cliente_id, titular, beneficiario, fecha):
        '''
        necesita:
            - cuenta_numero: número de la cuenta
            - cliente_id: DPI del cliente
            - titular: bool
            - fecha: fecha de la operacion actual o timestamp actual
            - beneficiario: bool
        '''
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (c:Cliente {DPI: $cliente_id}) "
                "MATCH (c1:Cuenta {numero_cuenta: $cuenta_numero}) "
                "MERGE (c1)-[rel:TIENE]->(c) "
                "ON CREATE SET rel.titular = $titular, rel.fecha = $fecha, rel.beneficiario = $beneficiario ",
                cliente_id=cliente_id,
                cuenta_numero=cuenta_numero,
                titular=titular,
                fecha=fecha,
                beneficiario=beneficiario
            )
            print(
                f" >> TIENE: relationship created for client {cliente_id} on account {cuenta_numero}")

            return result

    def create_parentesco_relationship(self, cliente_id1, cliente_id2, tipo, grado, familia):
        '''
        necesita:
            - cliente_id1: DPI del cliente1
            - cliente_id2: DPI del cliente2
            - tipo: tipode parentesco
            - grado: grado del parentesco
            - familia: bool
        '''
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (c:Cliente {DPI: $cliente_id1}) "
                "MATCH (c1:Cliente {DPI: $cliente_id2}) "
                "MERGE (c1)-[rel:PARENTESCO]->(c) "
                "ON CREATE SET rel.tipo = $tipo, rel.grado = $grado, rel.familia = $familia ",
                cliente_id1=cliente_id1,
                cliente_id2=cliente_id2,
                tipo=tipo,
                grado=grado,
                familia=familia
            )
            print(
                f" >> PARENTESCO: relationship created for client {cliente_id1} with {cliente_id2}")

            return result

    def create_withdrawal_relationship(self, retiro_id, cuenta_numero, cliente_id, monto, divisa, fecha, es_propietario):
        '''
        necesita:
            - retiro_id: ID del nodo Retiro
            - cuenta_numero: número de cuenta
            - cliente_id: DPI del nodo Cliente
            - monto: monto de la relación INVOLUCRA
            - divisa: divisa de la relación INVOLUCRA
            - fecha: fecha o timestamp de la relación INVOLUCRA
            - es_propietario: valor booleano indicando si el Cliente es propietario del Retiro
        '''
        with self.driver.session(database="neo4j") as session:
            result1 = session.run(
                "MATCH (r:Retiro {numero_retiro: $retiro_id}) "
                "MATCH (c:Cuenta {numero_cuenta: $cuenta_numero}) "
                "MERGE (r)-[rel:INVOLUCRA]->(c) "
                "ON CREATE SET rel.monto = $monto, rel.divisa = $divisa, rel.fecha = $fecha ",
                retiro_id=retiro_id,
                cuenta_numero=cuenta_numero,
                monto=monto,
                divisa=divisa,
                fecha=fecha
            )
            print(
                f" >> INVOLUCRA: Withdrawal relationship created for Retiro {retiro_id} and Cuenta {cuenta_numero}")

            result2 = session.run(
                "MATCH (cl:Cliente {DPI: $cliente_id}) "
                "MATCH (r:Retiro {numero_retiro: $retiro_id}) "
                "MERGE (cl)-[rel:REALIZA]->(r) "
                "ON CREATE SET rel.es_propietario = $es_propietario, rel.monto = $monto, rel.fecha = $fecha ",
                cliente_id=cliente_id,
                retiro_id=retiro_id,
                es_propietario=es_propietario,
                monto=monto,
                fecha=fecha
            )
            print(
                f" >> REALIZA: Withdrawal relationship created for Cliente {cliente_id} and Retiro {retiro_id}")

            return [result1, result2]

    def create_fraud_relationship_retiro(self, retiro_id, fraude_id, cuenta_numero, monto, divisa, fecha, motivo):
        '''
        necesita:
            - retiro_id: ID del nodo Retiro
            - fraude_id: ID del nodo Fraude
            - cuenta_numero: número de cuenta
            - monto: monto de la relación GENERO
            - divisa: divisa de la relación GENERO
            - fecha: fecha o timestamp de la relación GENERO
            - motivo: motivo de la relación INVOLUCRADA_EN
        '''
        with self.driver.session(database="neo4j") as session:
            result1 = session.run(
                "MATCH (r:Retiro {numero_retiro: $retiro_id}) "
                "MATCH (f:Fraude {numero_fraude: $fraude_id}) "
                "MERGE (r)-[rel:GENERO]->(f) "
                "ON CREATE SET rel.monto = $monto, rel.divisa = $divisa, rel.fecha = $fecha ",
                retiro_id=retiro_id,
                fraude_id=fraude_id,
                monto=monto,
                divisa=divisa,
                fecha=fecha
            )
            print(
                f" >> GENERO: Fraud relationship created for Retiro {retiro_id} and Fraude {fraude_id}")

            result2 = session.run(
                "MATCH (c:Cuenta {numero_cuenta: $cuenta_numero}) "
                "MATCH (f:Fraude {numero_fraude: $fraude_id}) "
                "MERGE (c)-[rel:INVOLUCRADA_EN]->(f) "
                "ON CREATE SET rel.motivo = $motivo, rel.numero_cuenta = $cuenta_numero, rel.fecha = $fecha ",
                cuenta_numero=cuenta_numero,
                fraude_id=fraude_id,
                motivo=motivo,
                fecha=fecha
            )
            print(
                f" >> INVOLUCRADA_EN: Fraud relationship created for Cuenta {cuenta_numero} and Fraude {fraude_id}")

            return [result1, result2]

    def create_beneficiary_relationship(self, retiro_id, cliente_id, es_propietario, monto, fecha):
        '''
        necesita:
            - retiro_id: ID del nodo Retiro
            - cliente_id: DPI del nodo Cliente
            - es_propietario: valor de la relación BENEFICIARIO
            - monto: monto de la relación BENEFICIARIO
            - fecha: fecha o timestamp de la relación BENEFICIARIO
        '''
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (r:Retiro {numero_retiro: $retiro_id}) "
                "MATCH (c:Cliente {DPI: $cliente_id}) "
                "MERGE (r)-[rel:BENEFICIARIO]->(c) "
                "ON CREATE SET rel.es_propietario = $es_propietario, rel.monto = $monto, rel.fecha = $fecha ",
                retiro_id=retiro_id,
                cliente_id=cliente_id,
                es_propietario=es_propietario,
                monto=monto,
                fecha=fecha
            )
            print(
                f" >> BENEFICIARIO: Beneficiary relationship created for Retiro {retiro_id} and Cliente {cliente_id}")
            return result

    def find_and_return_node(self, node_label, attribute_name, attribute_value):
        '''
        necesita:
            - label del nodo a buscar
            - atributo por el cual esta buscandose
            - valor del atributo por el cual se esta buscando
        '''
        query = (
            f"MATCH (n:{node_label}) "
            f"WHERE n.{attribute_name} = $attribute_value "
            "RETURN n "
        )
        with self.driver.session(database="neo4j") as session:
            result = session.run(query, attribute_value=attribute_value)
            nodes = [record["n"] for record in result]
            return nodes

    def find_and_return_relationship(self, label1, attr_name1, attr_value1, label2, attr_name2, attr_value2, relationship_type):
        '''
        necesita:
            - label del nodo a buscar inicio 
            - label del nodo a buscar fin
            - atributo por el cual esta buscandose nodo inicio
            - valor del atributo por el cual se esta buscando nodo inicio
            - atributo por el cual esta buscandose nodo fin
            - valor del atributo por el cual se esta buscando nodo fin
            - tipo de relacion que estamos buscando entre los nodos
        '''
        query = (
            f"MATCH (n1:{label1}{{{attr_name1}: $attr_value1}})-[r:{relationship_type}]-"
            f"(n2:{label2}{{{attr_name2}: $attr_value2}}) RETURN r"
        )
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                query, attr_value1=attr_value1, attr_value2=attr_value2)
            relationships = [row["r"] for row in result]
            print(f' >> Se han encontrado estas relaciones: {relationships}')
            return relationships

    def find_average_transfer_amount(self, account_id):
        '''
        necesita:
            - numero_cuenta de la cuenta que queremos el promedio de transferencias
        '''
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (account:Cuenta {numero_cuenta: $account_id})-[transfer:REALIZA]->(t2:Transferencia) "
                "RETURN AVG(transfer.monto) AS average_amount ",
                account_id=account_id
            )
            average_amount = result.single()["average_amount"]
            print(
                f" >> Transaccion promedio para cuenta {account_id}: {average_amount}")
            return average_amount

    def find_average_retiro_amount(self, account_id):
        '''
        necesita:
            - dpi del cliente que queremos el promedio de retiros
        '''
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (account:Cliente {DPI: $account_id})-[transfer:REALIZA]->(account:Retiro) "
                "RETURN AVG(transfer.monto) AS average_amount ",
                account_id=account_id
            )
            average_amount = result.single()["average_amount"]
            print(
                f" >> Retiro promedio para cliente con DPI {account_id}: {average_amount}")
            return average_amount

    def disable_account(self, account_number):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (c:Cuenta {numero_cuenta: $account_number}) "
                "SET c.habilitada = False "
                "RETURN c", account_number=account_number
            )
            print(f' >> Cuenta {account_number} deshabilitada')
            return result.single()["c"]

    def activate_account(self, account_number):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (c:Cuenta {numero_cuenta: $account_number}) "
                "SET c.habilitada = True "
                "RETURN c", account_number=account_number
            )
            print(f' >> Cuenta {account_number} habilitada nuevamente')
            return result.single()["c"]

    def is_account_enabled(self, account_number):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (c:Cuenta {numero_cuenta: $account_number}) "
                "RETURN c.habilitada AS habilitada", account_number=account_number
            )
            return result.single()["habilitada"]

    def get_account_bank(self, account_number):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (c:Cuenta {numero_cuenta: $account_number}) "
                "RETURN c.banco AS banco", account_number=account_number
            )
            return result.single()["banco"]

    def delete_account(self, account_number):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (c:Cuenta {numero_cuenta: $account_number}) "
                "DETACH DELETE c", account_number=account_number
            )
            return result

    def update_involucra_motivo(self, account_number, fraud_number, new_motivo):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (c:Cuenta {numero_cuenta: $account_number})"
                "-[r:INVOLUCRADA_EN]->(f:Fraude {numero_fraude: $fraud_number}) "
                "SET r.motivo = $new_motivo ",
                account_number=account_number,
                fraud_number=fraud_number,
                new_motivo=new_motivo
            )
            print(ACTUALIZADO_MSG)
            return result

    def update_cuenta_banco(self, account_number, new_banco):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (c:Cuenta {numero_cuenta: $account_number}) "
                "SET c.banco = $new_banco", account_number=account_number, new_banco=new_banco
            )
            print(ACTUALIZADO_MSG)
            return result

    def delete_involucra_relationship(self, account_number, fraud_number):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (c:Cuenta {numero_cuenta: $account_number})-[r:INVOLUCRADA_EN]->(f:Fraude {numero_fraude: $fraud_number}) "
                "DELETE r", account_number=account_number, fraud_number=fraud_number
            )
            print(ACTUALIZADO_MSG)
            return result

    def delete_fecha_alerta(self, fraud_number):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (f:Fraude {numero_fraude: $fraud_number}) "
                "REMOVE f.fecha_alerta", fraud_number=fraud_number
            )
            print(ACTUALIZADO_MSG)
            return result

    def modificar_estado_accion_fraude(self, numero_fraude, nuevo_estado, nueva_accion):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (fraude:Fraude {numero_fraude: $numero_fraude}) "
                "SET fraude.estado = $nuevo_estado, fraude.accion_tomada = $nueva_accion ",
                numero_fraude=numero_fraude,
                nuevo_estado=nuevo_estado,
                nueva_accion=nueva_accion
            )
            print(
                f" >> Estado y acción del fraude {numero_fraude} modificados")
            return result

    def delete_parentesco_tipo(self, cliente1_id, cliente2_id):
        with self.driver.session(database="neo4j") as session:
            result1 = session.run(
                "MATCH (c1:Cliente {DPI: $cliente1_id})-[r:PARENTESCO]->(c2:Cliente {DPI: $cliente2_id}) "
                "DELETE r", cliente1_id=cliente1_id, cliente2_id=cliente2_id
            )

            result2 = session.run(
                "MATCH (c1:Cliente {DPI: $cliente2_id})-[r:PARENTESCO]->(c2:Cliente {DPI: $cliente1_id}) "
                "DELETE r", cliente1_id=cliente1_id, cliente2_id=cliente2_id
            )
            print(ACTUALIZADO_MSG)
            return [result1, result2]

    def has_relationship_with_fraud(self, account_number):
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (c:Cuenta {numero_cuenta: $account_number}) "
                "-[:INVOLUCRADA_EN]->(f:Fraude) "
                "RETURN COUNT(f) > 0 AS has_relationship "
            )
            result = session.run(query, account_number=account_number)
            record = result.single()
            has_relationship = record["has_relationship"]
            print(' >> relacion fraude creada')
            return has_relationship

    def get_max_transaction_number(self):
        with self.driver.session(database="neo4j") as session:
            query = "MATCH (t:Transferencia) RETURN MAX(t.numero_transferencia) AS max_number"
            result = session.run(query)
            max_number = result.single()["max_number"]
            return max_number

    def get_max_withdrawal_number(self):
        with self.driver.session(database="neo4j") as session:
            query = "MATCH (w:Retiro) RETURN MAX(w.numero_retiro) AS max_number"
            result = session.run(query)
            max_number = result.single()["max_number"]
            return max_number

    def get_max_fraud_number(self):
        with self.driver.session(database="neo4j") as session:
            query = "MATCH (f:Fraude) RETURN MAX(f.numero_fraude) AS max_number"
            result = session.run(query)
            max_number = result.single()["max_number"]
            return max_number

    def get_account_type(self, account_number):
        with self.driver.session(database="neo4j") as session:
            query = "MATCH (c:Cuenta {numero_cuenta: $account_number}) RETURN c.tipo_cuenta AS account_type"
            result = session.run(query, account_number=account_number)
            account_type = result.single()["account_type"]
            return account_type

    def compare_account_banks(self, account1_number, account2_number):
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (c1:Cuenta {numero_cuenta: $account1_number}) "
                "MATCH (c2:Cuenta {numero_cuenta: $account2_number}) "
                "RETURN c1.banco = c2.banco AS same_banks"
            )
            result = session.run(
                query, account1_number=account1_number, account2_number=account2_number)
            same_banks = result.single()["same_banks"]
            return same_banks

    def get_max_account_number(self):
        with self.driver.session(database="neo4j") as session:
            query = "MATCH (c:Cuenta) RETURN MAX(c.numero_cuenta) AS max_number"
            result = session.run(query)
            max_number = result.single()["max_number"]
            return max_number

    def check_account_exists(self, account_number):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (c:Cuenta {numero_cuenta: $account_number}) RETURN COUNT(c) AS count",
                account_number=account_number
            )
            count = result.single()["count"]
            return count > 0

    def get_cliente_dpi(self, account_number):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (cuenta:Cuenta {numero_cuenta: $account_number})"
                "-[:ES_PROPIETARIO_DE]->(cliente:Cliente)"
                "RETURN cliente.dpi AS dpi",
                account_number=account_number
            )
            record = result.single()
            if record:
                dpi = record["dpi"]
                return dpi
            else:
                return None

    # ======================== QUERIES PARA INFO/EVALUACION ============================================================ #
    def get_top_accounts_with_fraud_relations(self):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (c:Cuenta)-[r:INVOLUCRADA_EN]->(f:Fraude) "
                "WITH c.numero_cuenta AS numero_cuenta, COUNT(r) AS fraud_count "
                "RETURN numero_cuenta, fraud_count "
                "ORDER BY fraud_count DESC "
                "LIMIT 5"
            )
            accounts = [(row["numero_cuenta"], row["fraud_count"])
                        for row in result]
            print(' >> Devolviendo nodos cuenta top 5 en fraudes')
            print(ARROW_MSG, accounts)
            return accounts

    def get_client_names_related_to_fraud(self):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (cl:Cliente)-[:ES_PROPIETARIO_DE]->(c:Cuenta)-[:INVOLUCRADA_EN]->(f:Fraude) "
                "RETURN cl.nombre AS nombre, cl.DPI AS DPI"
            )
            client_names = [(row["nombre"], row["DPI"]) for row in result]
            client_names = list(set(client_names))
            print(' >> Devolviendo nombres de clientes owner de cuentas en fraudes')
            print(ARROW_MSG, client_names)  # blanco ?

            return client_names

    def count_banks_related_to_fraud(self):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (c:Cuenta)-[:INVOLUCRADA_EN]->(f:Fraude) "
                "RETURN c.banco AS banco, count(*) AS count "
            )
            bank_counts = {row["banco"]: row["count"] for row in result}
            print(' >> Devolviendo nombres de bancos en fraudes')
            print(ARROW_MSG, bank_counts)
            return bank_counts

    def get_top_5_high_amount_transactions_related_to_fraud(self):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (f:Fraude)<-[:INVOLUCRADA_EN]-(c:Cuenta)-[t:REALIZA]->(t2:Transferencia) "
                "RETURN t2.numero_transferencia AS numero_transferencia, t2.monto AS monto "
                "ORDER BY t2.monto DESC "
                "LIMIT 5 "
            )
            transactions = [(row["numero_transferencia"], row["monto"])
                            for row in result]
            print(' >> Devolviendo top 5 montos mas altos transfer')
            print(ARROW_MSG, transactions)
            return transactions

    def get_top_5_high_amount_withdrawals_related_to_fraud(self):
        with self.driver.session(database="neo4j") as session:
            result = session.run(
                "MATCH (f:Fraude)<-[:INVOLUCRADA_EN]-(c:Cuenta)<-[r:INVOLUCRA]-(r2:Retiro) "
                "RETURN r2.numero_retiro AS numero_retiro, r2.monto AS monto "
                "ORDER BY r2.monto DESC "
                "LIMIT 5 "
            )
            withdrawals = [(row["numero_retiro"], row["monto"])
                           for row in result]
            print(' >> Devolviendo 5 high amount retiro')
            print(ARROW_MSG, withdrawals)  # no sirve
            return withdrawals
