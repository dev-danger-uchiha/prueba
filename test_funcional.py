import unittest
import requests
import time

# CAMBIA ESTO por tu URL de Render (ej. https://mi-app-flask.onrender.com)
BASE_URL = "http://127.0.0.1:5000" 

class TestIntegracionAplicacion(unittest.TestCase):

    def setUp(self):
        # Generar un email único basado en el timestamp para evitar fallos por llave única en la BD
        self.test_email = f"qa_tester_{int(time.time())}@adso.com"
        self.test_name = "QA Automation User"

    def test_a_home_page(self):
        """Verifica que el Home Page cargue correctamente (Página 1)"""
        response = requests.get(f"{BASE_URL}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Pruebas de Carga y Estrés", response.text)

    def test_b_registro_y_consulta(self):
        """Prueba End-to-End: Registra un usuario y verifica que aparezca en la consulta embebida (Página 2)"""
        
        # 1. Enviar el POST de registro
        payload = {
            "nombre": self.test_name,
            "email": self.test_email
        }
        response_post = requests.post(f"{BASE_URL}/registro", data=payload)
        
        # 2. Verificar que el registro procesó la redirección sin error del servidor
        self.assertEqual(response_post.status_code, 200)
        
        # 3. Hacer un GET a la misma página para ver la tabla
        response_get = requests.get(f"{BASE_URL}/registro")
        
        # 4. Validar que la consulta embebida muestra el nuevo usuario
        self.assertIn(self.test_name, response_get.text)
        self.assertIn(self.test_email, response_get.text)

if __name__ == "__main__":
    unittest.main(verbosity=2)