from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(0.01, 0.02)

    @task
    def hello_world(self):
        self.client.get("http://localhost:8000/exchange_rate/api/v1/courses")
