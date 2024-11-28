from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get('/')

    @task
    def show_summary(self):
        self.client.post('/showSummary', data={"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get('/book/Fall Classic/Simply Lift')

    @task
    def purchase_places(self):
        self.client.post('/purchasePlaces', {"competition": "Fall Classic", "club": "Simply Lift", "places": "2"})

    @task
    def clubs_points_board(self):
        self.client.get('/clubs')

    @task
    def logout(self):
        self.client.get('/logout')
