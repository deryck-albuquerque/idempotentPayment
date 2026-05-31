from concurrent.futures import ThreadPoolExecutor
import requests


def make_request(index):

    response = requests.post(
        "http://localhost:8000/payments",
        headers={
            "Idempotency-Key": "abc123"
        },
        json={
            "user_id": "1",
            "amount": 100
        }
    )

    print(
        f"Request {index}: "
        f"{response.status_code} "
        f"{response.json()}"
    )


with ThreadPoolExecutor(max_workers=10) as executor:

    for i in range(20):
        executor.submit(
            make_request,
            i
        )