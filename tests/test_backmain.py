from unittest.mock import MagicMock, patch, ANY
from Backend.backmain import BackendConn
import unittest

# Constantes
JOHNDOE_MSG = "John Doe"

class TestBackendConn(unittest.TestCase):

    def setUp(self):
        # Mockear el driver de Neo4j
        self.mock_driver = MagicMock()
        # Parchar el driver de Neo4j para que use el mock
        patcher = patch('Backend.backmain.GraphDatabase.driver', return_value=self.mock_driver)
        self.addCleanup(patcher.stop)
        patcher.start()

        # Mock para la sesión, agregando soporte para 'with'
        self.mock_session = MagicMock()
        # Soporte para el contexto with
        self.mock_driver.session.return_value.__enter__.return_value = self.mock_session

        # Instancia del BackendConn con los valores de mock
        self.backend = BackendConn("mock://uri", "user", "pass")

    def tearDown(self):
        self.backend.close()

    def test_create_node(self):
        # Configuración del mock para la sesión
        self.mock_session.run.return_value.single.return_value = ["mock_node"]

        # Llamada a la función a probar
        node_labels = ["Cuenta"]
        attributes = {"numero_cuenta": "12345"}
        self.backend.create_node(node_labels, attributes)

        # Verificar que se haya llamado a session y run sin espacios extra
        self.mock_session.run.assert_called_with(
            "CREATE (n:Cuenta { numero_cuenta: $numero_cuenta }) RETURN n ",  # Eliminar el espacio aquí
            numero_cuenta="12345"
        )

    def test_create_transaccion_relationship(self):
        account1_number = "123456"
        account2_number = "654321"
        transaction_number = "7890"
        divisa = "Quetzales"
        monto = 1000
        fecha = "2024-10-18"
        tipo_cuenta = "Ahorro"

        # Llamada a la función a probar
        result = self.backend.create_transaccion_relationship(
            account1_number, account2_number, transaction_number, divisa, monto, fecha, tipo_cuenta
        )

        # Verificar que se hayan llamado las consultas esperadas
        self.mock_session.run.assert_any_call(
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

        self.mock_session.run.assert_any_call(
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

        self.assertIsInstance(result, list)

    def test_disable_account(self):
        account_number = "123456"

        # Llamada a la función a probar
        self.backend.disable_account(account_number)

        # Verificar que se haya ejecutado la consulta correcta sin espacios extra
        self.mock_session.run.assert_called_once_with(
            "MATCH (c:Cuenta {numero_cuenta: $account_number}) "
            "SET c.habilitada = False "
            "RETURN c",  # Eliminar el espacio aquí
            account_number=account_number
        )

    def test_find_and_return_node(self):
        self.mock_session.run.return_value = [MagicMock()]

        node_label = 'TestNode'
        attribute_name = 'name'
        attribute_value = 'John Doe'

        # Llamada a la función a probar
        result_nodes = self.backend.find_and_return_node(node_label, attribute_name, attribute_value)

        # Verificar que se haya llamado a run sin espacios extra
        self.mock_session.run.assert_called_once_with(
            f"MATCH (n:{node_label}) "
            f"WHERE n.{attribute_name} = $attribute_value "
            "RETURN n ",  # Eliminar el espacio aquí
            attribute_value=attribute_value
        )

        self.assertTrue(len(result_nodes) > 0)

    def test_get_account_bank(self):
        self.mock_session.run.return_value.single.return_value = {"banco": "BI"}

        account_number = "123456"

        # Llamada a la función a probar
        bank = self.backend.get_account_bank(account_number)

        # Verificar que se haya ejecutado la consulta correcta sin espacios extra
        self.mock_session.run.assert_called_once_with(
            "MATCH (c:Cuenta {numero_cuenta: $account_number}) "
            "RETURN c.banco AS banco",  # Eliminar el espacio aquí
            account_number=account_number
        )

        self.assertEqual(bank, "BI")

    def test_create_fraud_relationship_transferencia(self):
        # Configuración de los parámetros de la función
        transferencia_numero = "123456789"
        fraud_id = "987654321"
        cuenta_numero = "111222333"
        motivo = "Suspicious Activity"
        monto = 10000
        fecha = "2024-10-22"

        # Llamada a la función a probar
        result = self.backend.create_fraud_relationship_transferencia(
            transferencia_numero, fraud_id, cuenta_numero, motivo, monto, fecha
        )

        # Verificar que la primera consulta fue ejecutada correctamente
        self.mock_session.run.assert_any_call(
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

        # Verificar que la segunda consulta fue ejecutada correctamente
        self.mock_session.run.assert_any_call(
            "MATCH (c:Cuenta {numero_cuenta: $cuenta_numero}) "
            "MATCH (f:Fraude {numero_fraude: $fraud_id}) "
            "MERGE (c)-[rel:INVOLUCRADA_EN]->(f) "
            "ON CREATE SET rel.motivo = $motivo, rel.numero_cuenta = $cuenta_numero, rel.fecha = $fecha ",
            cuenta_numero=cuenta_numero,
            fraud_id=fraud_id,
            motivo=motivo,
            fecha=fecha
        )

        # Verificar que el resultado contiene los dos resultados de las consultas
        self.assertEqual(result, [self.mock_session.run.return_value, self.mock_session.run.return_value])

    def test_create_owner_relationship(self):
        # Configuración de los parámetros de la función
        cuenta_numero = "123456"
        cliente_id = "654321"
        inicio_propiedad = "2023-01-01"
        fecha = "2024-10-22"
        comentarios = "Propiedad compartida"

        # Llamada a la función a probar
        result = self.backend.create_owner_relationship(
            cuenta_numero, cliente_id, inicio_propiedad, fecha, comentarios
        )

        # Verificar que la primera consulta fue ejecutada correctamente
        self.mock_session.run.assert_any_call(
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

        # Verificar que la segunda consulta fue ejecutada correctamente
        self.mock_session.run.assert_any_call(
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

        # Verificar que el resultado contiene los dos resultados de las consultas
        self.assertEqual(result, [self.mock_session.run.return_value, self.mock_session.run.return_value])

    def test_create_tiene_cuenta_relationship(self):
        # Configuración de los parámetros de la función
        cuenta_numero = "123456"
        cliente_id = "654321"
        titular = True
        beneficiario = False
        fecha = "2024-10-22"

        # Llamada a la función a probar
        result = self.backend.create_tiene_cuenta_relationship(
            cuenta_numero, cliente_id, titular, beneficiario, fecha
        )

        # Verificar que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
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

        # Verificar que el resultado fue retornado
        self.assertEqual(result, self.mock_session.run.return_value)

    def test_create_parentesco_relationship(self):
        # Configuración de los parámetros de la función
        cliente_id1 = "123456789"
        cliente_id2 = "987654321"
        tipo = "Hermano"
        grado = 1
        familia = True

        # Llamada a la función a probar
        result = self.backend.create_parentesco_relationship(
            cliente_id1, cliente_id2, tipo, grado, familia
        )

        # Verificar que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
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

        # Verificar que el resultado fue retornado
        self.assertEqual(result, self.mock_session.run.return_value)

    def test_create_withdrawal_relationship(self):
        # Configuración de los parámetros de la función
        retiro_id = "1001"
        cuenta_numero = "2002"
        cliente_id = "3003"
        monto = 5000
        divisa = "USD"
        fecha = "2024-10-22"
        es_propietario = True

        # Llamada a la función a probar
        result = self.backend.create_withdrawal_relationship(
            retiro_id, cuenta_numero, cliente_id, monto, divisa, fecha, es_propietario
        )

        # Verificar que la primera consulta fue ejecutada correctamente
        self.mock_session.run.assert_any_call(
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

        # Verificar que la segunda consulta fue ejecutada correctamente
        self.mock_session.run.assert_any_call(
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

        # Verificar que el resultado de ambas consultas fue retornado
        self.assertEqual(result, [self.mock_session.run.return_value, self.mock_session.run.return_value])

    def test_create_fraud_relationship_retiro(self):
        # Configuración de los parámetros de la función
        retiro_id = "1001"
        fraude_id = "5005"
        cuenta_numero = "2002"
        monto = 10000
        divisa = "USD"
        fecha = "2024-10-22"
        motivo = "Fraud Alert"

        # Llamada a la función a probar
        result = self.backend.create_fraud_relationship_retiro(
            retiro_id, fraude_id, cuenta_numero, monto, divisa, fecha, motivo
        )

        # Verificar que la primera consulta fue ejecutada correctamente
        self.mock_session.run.assert_any_call(
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

        # Verificar que la segunda consulta fue ejecutada correctamente
        self.mock_session.run.assert_any_call(
            "MATCH (c:Cuenta {numero_cuenta: $cuenta_numero}) "
            "MATCH (f:Fraude {numero_fraude: $fraude_id}) "
            "MERGE (c)-[rel:INVOLUCRADA_EN]->(f) "
            "ON CREATE SET rel.motivo = $motivo, rel.numero_cuenta = $cuenta_numero, rel.fecha = $fecha ",
            cuenta_numero=cuenta_numero,
            fraude_id=fraude_id,
            motivo=motivo,
            fecha=fecha
        )

        # Verificar que el resultado de ambas consultas fue retornado
        self.assertEqual(result, [self.mock_session.run.return_value, self.mock_session.run.return_value])

    def test_create_beneficiary_relationship(self):
        # Configuración de los parámetros de la función
        retiro_id = "1001"
        cliente_id = "3003"
        es_propietario = True
        monto = 5000
        fecha = "2024-10-22"

        # Llamada a la función a probar
        result = self.backend.create_beneficiary_relationship(
            retiro_id, cliente_id, es_propietario, monto, fecha
        )

        # Verificar que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
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

        # Verificar que el resultado fue retornado correctamente
        self.assertEqual(result, self.mock_session.run.return_value)

    def test_find_average_transfer_amount(self):
        # Configuración de los parámetros de la función
        account_id = "12345"

        # Valor simulado para el promedio de transferencias
        self.mock_session.run.return_value.single.return_value = {"average_amount": 1000.0}

        # Llamada a la función a probar
        result = self.backend.find_average_transfer_amount(account_id)

        # Verificar que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (account:Cuenta {numero_cuenta: $account_id})-[transfer:REALIZA]->(t2:Transferencia) "
            "RETURN AVG(transfer.monto) AS average_amount ",
            account_id=account_id
        )

        # Verificar que el resultado sea el promedio esperado
        self.assertEqual(result, 1000.0)

    def test_activate_account(self):
        # Configuración del número de cuenta
        account_number = "12345"

        # Simulación del resultado de la consulta
        self.mock_session.run.return_value.single.return_value = {"c": {"numero_cuenta": account_number, "habilitada": True}}

        # Llamada a la función a probar
        result = self.backend.activate_account(account_number)

        # Verificar que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (c:Cuenta {numero_cuenta: $account_number}) "
            "SET c.habilitada = True "
            "RETURN c", account_number=account_number
        )

        # Verificar que el resultado es el esperado
        self.assertEqual(result["numero_cuenta"], account_number)
        self.assertTrue(result["habilitada"])

    def test_is_account_enabled(self):
        # Configuración del número de cuenta
        account_number = "67890"

        # Simulación del estado de habilitación de la cuenta
        self.mock_session.run.return_value.single.return_value = {"habilitada": True}

        # Llamada a la función a probar
        result = self.backend.is_account_enabled(account_number)

        # Verificar que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (c:Cuenta {numero_cuenta: $account_number}) "
            "RETURN c.habilitada AS habilitada", account_number=account_number
        )

        # Verificar que el resultado sea el esperado (habilitada=True)
        self.assertTrue(result)

    def test_delete_account(self):
        # Configuración del número de cuenta
        account_number = "67890"

        # Simulación del resultado de la consulta
        self.mock_session.run.return_value = MagicMock()

        # Llamada a la función a probar
        result = self.backend.delete_account(account_number)

        # Verificar que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (c:Cuenta {numero_cuenta: $account_number}) "
            "DETACH DELETE c", account_number=account_number
        )

        # En este caso, no es necesario verificar el resultado como None
        self.assertIsNotNone(result)  # Cambiar para asegurarse de que result no sea None

    def test_get_account_bank(self):
        # Configuración del número de cuenta y banco
        account_number = "12345"
        bank_name = "Bank of America"

        # Simulación del resultado de la consulta
        self.mock_session.run.return_value.single.return_value = {"banco": bank_name}

        # Llamada a la función a probar
        result = self.backend.get_account_bank(account_number)

        # Verificar que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (c:Cuenta {numero_cuenta: $account_number}) "
            "RETURN c.banco AS banco", account_number=account_number
        )

        # Verificar que el resultado es el esperado
        self.assertEqual(result, bank_name)

    def test_update_involucra_motivo(self):
        # Configuración de los parámetros de entrada
        account_number = "123456"
        fraud_number = "654321"
        new_motivo = "Motivo actualizado"

        # Simulación del resultado de la consulta
        self.mock_session.run.return_value = MagicMock()

        # Llamada a la función a probar
        result = self.backend.update_involucra_motivo(account_number, fraud_number, new_motivo)

        # Verificar que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (c:Cuenta {numero_cuenta: $account_number})"
            "-[r:INVOLUCRADA_EN]->(f:Fraude {numero_fraude: $fraud_number}) "
            "SET r.motivo = $new_motivo ",
            account_number=account_number,
            fraud_number=fraud_number,
            new_motivo=new_motivo
        )

        # Verificar que el resultado fue retornado
        self.assertEqual(result, self.mock_session.run.return_value)

    def test_update_cuenta_banco(self):
        # Configuración de los parámetros de entrada
        account_number = "123456"
        new_banco = "Nuevo Banco"

        # Simulación del resultado de la consulta
        self.mock_session.run.return_value = MagicMock()

        # Llamada a la función a probar
        result = self.backend.update_cuenta_banco(account_number, new_banco)

        # Verificar que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (c:Cuenta {numero_cuenta: $account_number}) "
            "SET c.banco = $new_banco",
            account_number=account_number,
            new_banco=new_banco
        )

        # Verificar que el resultado fue retornado
        self.assertEqual(result, self.mock_session.run.return_value)

    def test_delete_involucra_relationship(self):
        account_number = "123456"
        fraud_number = "654321"

        # Simulación del resultado de la consulta
        self.mock_session.run.return_value = MagicMock()

        # Llamada a la función a probar
        result = self.backend.delete_involucra_relationship(account_number, fraud_number)

        # Verificación de que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (c:Cuenta {numero_cuenta: $account_number})-[r:INVOLUCRADA_EN]->(f:Fraude {numero_fraude: $fraud_number}) "
            "DELETE r", account_number=account_number, fraud_number=fraud_number
        )

        # Verificación del resultado retornado
        self.assertEqual(result, self.mock_session.run.return_value)

    def test_delete_fecha_alerta(self):
        fraud_number = "5005"

        # Simulación del resultado de la consulta
        self.mock_session.run.return_value = MagicMock()

        # Llamada a la función a probar
        result = self.backend.delete_fecha_alerta(fraud_number)

        # Verificación de que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (f:Fraude {numero_fraude: $fraud_number}) "
            "REMOVE f.fecha_alerta", fraud_number=fraud_number
        )

        # Verificación del resultado retornado
        self.assertEqual(result, self.mock_session.run.return_value)

    def test_modificar_estado_accion_fraude(self):
        numero_fraude = "5005"
        nuevo_estado = "Activo"
        nueva_accion = "Investigación iniciada"

        # Simulación del resultado de la consulta
        self.mock_session.run.return_value = MagicMock()

        # Llamada a la función a probar
        result = self.backend.modificar_estado_accion_fraude(numero_fraude, nuevo_estado, nueva_accion)

        # Verificación de que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (fraude:Fraude {numero_fraude: $numero_fraude}) "
            "SET fraude.estado = $nuevo_estado, fraude.accion_tomada = $nueva_accion ",
            numero_fraude=numero_fraude,
            nuevo_estado=nuevo_estado,
            nueva_accion=nueva_accion
        )

        # Verificación del resultado retornado
        self.assertEqual(result, self.mock_session.run.return_value)

    def test_delete_parentesco_tipo(self):
        cliente1_id = "123456789"
        cliente2_id = "987654321"

        # Simulación del resultado de las consultas
        self.mock_session.run.return_value = MagicMock()

        # Llamada a la función a probar
        result = self.backend.delete_parentesco_tipo(cliente1_id, cliente2_id)

        # Verificación de que la primera consulta fue ejecutada correctamente
        self.mock_session.run.assert_any_call(
            "MATCH (c1:Cliente {DPI: $cliente1_id})-[r:PARENTESCO]->(c2:Cliente {DPI: $cliente2_id}) "
            "DELETE r", cliente1_id=cliente1_id, cliente2_id=cliente2_id
        )

        # Verificación de que la segunda consulta fue ejecutada correctamente
        self.mock_session.run.assert_any_call(
            "MATCH (c1:Cliente {DPI: $cliente2_id})-[r:PARENTESCO]->(c2:Cliente {DPI: $cliente1_id}) "
            "DELETE r", cliente1_id=cliente1_id, cliente2_id=cliente2_id
        )

        # Verificación del resultado retornado
        self.assertEqual(result, [self.mock_session.run.return_value, self.mock_session.run.return_value])

    def test_has_relationship_with_fraud(self):
        account_number = "123456"

        # Simulación del resultado de la consulta
        self.mock_session.run.return_value.single.return_value = {"has_relationship": True}

        # Llamada a la función a probar
        result = self.backend.has_relationship_with_fraud(account_number)

        # Verificación de que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (c:Cuenta {numero_cuenta: $account_number}) "
            "-[:INVOLUCRADA_EN]->(f:Fraude) "
            "RETURN COUNT(f) > 0 AS has_relationship ",
            account_number=account_number
        )

        # Verificación del resultado retornado
        self.assertTrue(result)

    def test_get_max_transaction_number(self):
        # Simulación del resultado de la consulta
        self.mock_session.run.return_value.single.return_value = {"max_number": 999}

        # Llamada a la función a probar
        max_number = self.backend.get_max_transaction_number()

        # Verificación de que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (t:Transferencia) RETURN MAX(t.numero_transferencia) AS max_number"
        )

        # Verificación del resultado retornado
        self.assertEqual(max_number, 999)

    def test_get_max_withdrawal_number(self):
        # Simulación del resultado de la consulta
        self.mock_session.run.return_value.single.return_value = {"max_number": 500}

        # Llamada a la función a probar
        max_number = self.backend.get_max_withdrawal_number()

        # Verificación de que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (w:Retiro) RETURN MAX(w.numero_retiro) AS max_number"
        )

        # Verificación del resultado retornado
        self.assertEqual(max_number, 500)

    def test_get_max_fraud_number(self):
        # Simulación del resultado de la consulta
        self.mock_session.run.return_value.single.return_value = {"max_number": 100}

        # Llamada a la función a probar
        max_number = self.backend.get_max_fraud_number()

        # Verificación de que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (f:Fraude) RETURN MAX(f.numero_fraude) AS max_number"
        )

        # Verificación del resultado retornado
        self.assertEqual(max_number, 100)

    def test_get_account_type(self):
        account_number = "123456"

        # Simulación del resultado de la consulta
        self.mock_session.run.return_value.single.return_value = {"account_type": "Ahorro"}

        # Llamada a la función a probar
        account_type = self.backend.get_account_type(account_number)

        # Verificación de que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (c:Cuenta {numero_cuenta: $account_number}) RETURN c.tipo_cuenta AS account_type",
            account_number=account_number
        )

        # Verificación del resultado retornado
        self.assertEqual(account_type, "Ahorro")

    def test_compare_account_banks(self):
        account1_number = "123456"
        account2_number = "654321"

        # Simulación del resultado de la consulta
        self.mock_session.run.return_value.single.return_value = {"same_banks": True}

        # Llamada a la función a probar
        same_banks = self.backend.compare_account_banks(account1_number, account2_number)

        # Verificación de que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (c1:Cuenta {numero_cuenta: $account1_number}) "
            "MATCH (c2:Cuenta {numero_cuenta: $account2_number}) "
            "RETURN c1.banco = c2.banco AS same_banks",
            account1_number=account1_number,
            account2_number=account2_number
        )

        # Verificación del resultado retornado
        self.assertTrue(same_banks)

    def test_get_max_account_number(self):
        # Simulación del resultado de la consulta
        self.mock_session.run.return_value.single.return_value = {"max_number": 999999}

        # Llamada a la función a probar
        max_number = self.backend.get_max_account_number()

        # Verificación de que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (c:Cuenta) RETURN MAX(c.numero_cuenta) AS max_number"
        )

        # Verificación del resultado retornado
        self.assertEqual(max_number, 999999)

    def test_check_account_exists(self):
        account_number = "123456"

        # Simulación del resultado de la consulta
        self.mock_session.run.return_value.single.return_value = {"count": 1}

        # Llamada a la función a probar
        exists = self.backend.check_account_exists(account_number)

        # Verificación de que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (c:Cuenta {numero_cuenta: $account_number}) RETURN COUNT(c) AS count",
            account_number=account_number
        )

        # Verificación del resultado retornado
        self.assertTrue(exists)

    def test_get_cliente_dpi(self):
        account_number = "123456"

        # Simulación del resultado de la consulta
        self.mock_session.run.return_value.single.return_value = {"dpi": "987654321"}

        # Llamada a la función a probar
        dpi = self.backend.get_cliente_dpi(account_number)

        # Verificación de que la consulta fue ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (cuenta:Cuenta {numero_cuenta: $account_number})"
            "-[:ES_PROPIETARIO_DE]->(cliente:Cliente)"
            "RETURN cliente.dpi AS dpi",
            account_number=account_number
        )

        # Verificación del resultado retornado
        self.assertEqual(dpi, "987654321")

    def test_get_top_accounts_with_fraud_relations(self):
        # Simulación del resultado de la consulta
        self.mock_session.run.return_value = [
            {"numero_cuenta": "12345", "fraud_count": 3},
            {"numero_cuenta": "67890", "fraud_count": 2},
        ]

        # Llamada a la función
        result = self.backend.get_top_accounts_with_fraud_relations()

        # Verificación de la consulta ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (c:Cuenta)-[r:INVOLUCRADA_EN]->(f:Fraude) "
            "WITH c.numero_cuenta AS numero_cuenta, COUNT(r) AS fraud_count "
            "RETURN numero_cuenta, fraud_count "
            "ORDER BY fraud_count DESC "
            "LIMIT 5"
        )

        # Verificación del resultado esperado
        expected_result = [("12345", 3), ("67890", 2)]
        self.assertEqual(result, expected_result)

    def test_get_client_names_related_to_fraud(self):
        # Simulación del resultado de la consulta
        self.mock_session.run.return_value = [
            {"nombre": JOHNDOE_MSG, "DPI": "123456789"},
            {"nombre": "Jane Smith", "DPI": "987654321"},
            {"nombre": JOHNDOE_MSG, "DPI": "123456789"},  # Duplicado
        ]

        # Llamada a la función
        result = self.backend.get_client_names_related_to_fraud()

        # Verificación de la consulta ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (cl:Cliente)-[:ES_PROPIETARIO_DE]->(c:Cuenta)-[:INVOLUCRADA_EN]->(f:Fraude) "
            "RETURN cl.nombre AS nombre, cl.DPI AS DPI"
        )

        # Verificación del resultado esperado (sin duplicados y ordenado)
        expected_result = [(JOHNDOE_MSG, "123456789"), ("Jane Smith", "987654321")]

        # Ordenar ambas listas para asegurarse de que el orden no afecte la prueba
        self.assertEqual(sorted(result), sorted(expected_result))

    def test_count_banks_related_to_fraud(self):
        # Simulación del resultado de la consulta
        self.mock_session.run.return_value = [
            {"banco": "Banco A", "count": 5},
            {"banco": "Banco B", "count": 3},
        ]

        # Llamada a la función
        result = self.backend.count_banks_related_to_fraud()

        # Verificación de la consulta ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (c:Cuenta)-[:INVOLUCRADA_EN]->(f:Fraude) "
            "RETURN c.banco AS banco, count(*) AS count "
        )

        # Verificación del resultado esperado
        expected_result = {"Banco A": 5, "Banco B": 3}
        self.assertEqual(result, expected_result)

    def test_get_top_5_high_amount_transactions_related_to_fraud(self):
        # Simulación del resultado de la consulta
        self.mock_session.run.return_value = [
            {"numero_transferencia": "T123", "monto": 1000},
            {"numero_transferencia": "T456", "monto": 800},
        ]

        # Llamada a la función
        result = self.backend.get_top_5_high_amount_transactions_related_to_fraud()

        # Verificación de la consulta ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (f:Fraude)<-[:INVOLUCRADA_EN]-(c:Cuenta)-[t:REALIZA]->(t2:Transferencia) "
            "RETURN t2.numero_transferencia AS numero_transferencia, t2.monto AS monto "
            "ORDER BY t2.monto DESC "
            "LIMIT 5 "
        )

        # Verificación del resultado esperado
        expected_result = [("T123", 1000), ("T456", 800)]
        self.assertEqual(result, expected_result)

    def test_get_top_5_high_amount_withdrawals_related_to_fraud(self):
        # Simulación del resultado de la consulta
        self.mock_session.run.return_value = [
            {"numero_retiro": "R123", "monto": 2000},
            {"numero_retiro": "R456", "monto": 1500},
        ]

        # Llamada a la función
        result = self.backend.get_top_5_high_amount_withdrawals_related_to_fraud()

        # Verificación de la consulta ejecutada correctamente
        self.mock_session.run.assert_called_once_with(
            "MATCH (f:Fraude)<-[:INVOLUCRADA_EN]-(c:Cuenta)<-[r:INVOLUCRA]-(r2:Retiro) "
            "RETURN r2.numero_retiro AS numero_retiro, r2.monto AS monto "
            "ORDER BY r2.monto DESC "
            "LIMIT 5 "
        )

        # Verificación del resultado esperado
        expected_result = [("R123", 2000), ("R456", 1500)]
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
