from locust import HttpUser, task, between


class LoadTestUser(HttpUser):
    wait_time = between(1, 2)
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM5NzE4ODQxLCJpYXQiOjE3Mzk3MTgyNDEsImp0aSI6IjhkNTA4N2NiZDc1NzQyMWY4ZjM4NzY1YWM5NTU0N2VhIiwidXNlcl9pZCI6NX0.LMTd48EneSpjbbQKm30LJvJupXwxRzJuKOHXYnHjoRo"
    }

    @task
    def get_info(self):
        response = self.client.get("/api/info", headers=self.headers)
        if response.status_code != 200:
            print(f"Ошибка: {response.status_code} - {response.text}")
