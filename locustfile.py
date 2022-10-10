"""
URL shortener load tests.
"""
from locust import HttpUser, task


class UrlShorteningUser(HttpUser):

    @task
    def shorten_url(self):
        self.client.post("/shorten_url/", data={"url": "https://google.com"})

    # @task
    # def shorten_url_fetch_content(self):
    #     url_key = "nonnonn0"  # 404 -> failure on locust ui
    #     for i in range(10):
    #         self.client.get(f"/{url_key}/")

    # @task
    # def shortened_urls_count(self):
    #     self.client.get("/shortened_urls_count/")
    #
    # @task
    # def most_popular_urls(self):
    #     self.client.get("/most_popular_urls/")
