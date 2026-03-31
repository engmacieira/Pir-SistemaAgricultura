from locust import HttpUser, task, between
import random
import string

def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

class PirAgroUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        # Cada usuário locust terá seu próprio email
        self.email = f"loadtest_{random_string()}@example.com"
        self.password = "LoadTest123!"

    @task(1)
    def register_and_login(self):
        # Primeiro, tentar registrar o usuário
        payload_register = {
            "email": self.email,
            "password": self.password,
            "full_name": "Locust User",
            "phone": "5511999999999"
        }

        with self.client.post("/auth/register", json=payload_register, catch_response=True) as response:
            if response.status_code == 201:
                response.success()
            elif response.status_code == 400 and "já registrado" in response.text:
                # Se já existe, ok, podemos prosseguir pro login
                response.success()
            else:
                response.failure(f"Failed to register: {response.status_code} - {response.text}")

        # Em seguida, logar
        payload_login = {
            "email": self.email,
            "password": self.password
        }

        with self.client.post("/auth/login", json=payload_login, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to login: {response.status_code} - {response.text}")
