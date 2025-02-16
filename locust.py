from locust import HttpUser, task, between

class LoadTestUser(HttpUser):
    wait_time = between(1, 2)  # задержка между запросами (от 1 до 2 секунд)

    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM5NjkwNDcwLCJpYXQiOjE3Mzk2ODk4NzAsImp0aSI6ImVlYzNlMjljZjJmNzRmYThiZTY4MDUyZjc2YmNmMWEzIiwidXNlcl9pZCI6M30.x6SN2GCdEsktDxsSSzVrUWB-l_9qss1OnGrgZFlTSts"
    }

    @task
    def get_info(self):
        response = self.client.get("/api/info", headers=self.headers)
        if response.status_code != 200:
            print(f"Ошибка: {response.status_code} - {response.text}")
