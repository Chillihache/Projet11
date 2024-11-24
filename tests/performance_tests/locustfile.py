from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get('/')
        """
    @task
    def show_summary(self):
        self.client.post('/showSummary', {"email": "john@simplylift.co"})"""


