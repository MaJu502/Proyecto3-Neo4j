'''def create_transaccion_relationship_realiza(self, account1_number, account2_number, divisa, monto, fecha):
    
    necesita:
        - numero_cuenta de cuenta origen
        - numero_transferencia de transferencia realizada
        - divisa de la transferencia
        - monto de la transferencia
        - fecha o timestamp que se realiza la transferencia
    
    with self.driver.session(database="neo4j") as session:
        result = session.run(
            "MATCH (cuenta1:Cuenta {numero_cuenta: $account1_number})"
            "MATCH (t2:Transferencia {numero_transferencia: $account2_number})"
            "MERGE (cuenta1)-[transaccion:REALIZA]->(t2)"
            "ON CREATE SET transaccion.divisa = $divi, transaccion.monto = $mont, transaccion.timestamp = $fechaT"
            "ON MATCH SET transaccion.monto = transaccion.monto + $mont",
            account1_number=account1_number,
            account2_number=account2_number,
            divi=divisa,
            mont=monto,
            fechaT=fecha
        )
        print(f" >> REALIZA: Transaction relationship created on {account1_number} to {account2_number}")
        return result

def create_transaccion_relationship_involucra(self, transaction_number, account2_number, divisa, tipo_cuenta, fecha):
    
    necesita:
        - numero_cuenta de cuenta destino
        - numero_transferencia de transferencia realizada
        - divisa de la transferencia
        - tipo_cuenta de la cuenta destino
        - fecha o timestamp que se realiza la transferencia
    
    with self.driver.session(database="neo4j") as session:
        result = session.run(
            "MATCH (t1:Transferencia {numero_transferencia: $transaction_number})"
            "MATCH (cuenta2:Cuenta {numero_cuenta: $account2_number})"
            "MERGE (t1)-[transaccion:INVOLUCRA]->(cuenta2)"
            "ON CREATE SET transaccion.divisa = $divi, transaccion.tipo_cuenta = $tipo, transaccion.timestamp = $fechaT"
            "ON MATCH SET transaccion.monto = transaccion.monto + $mont",
            transaction_number=transaction_number,
            account2_number=account2_number,
            divi=divisa,
            tipo=tipo_cuenta,
            fechaT=fecha
        )
        print(f" >> INVOLUCRA: Transaction relationship created on {transaction_number} to {account2_number}")
        return result'''