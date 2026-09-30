import httpx
import asyncio
import time


deviceStringIdentifier: str = "deviceId1322AssaD"  # hardcoded in each device, when setting it up, the MC (arduino), should have a kbd + LCD to do so
HandshakeURL: str = "http://localhost:8000/device/handshake/"
SAMPLE_URL: str = "http://localhost:8000/sample/submit/"
URL: str = "http://localhost:8000/sample/submit/"
DELTA_TIME: float = 0.2


async def main():
    req = httpx.get(URL)
    print(req)


asyncio.run(main())


# import requests
# import time
#
#
# def get_dad_joke() -> str:
#     response = requests.get("https://icanhazdadjoke.com/")
#     return response.text
#
#
# bt = time.perf_counter()
# for _ in range(3):
#     joke: str = get_dad_joke()
#     # print(joke)
#     print(_)
#     ct = time.perf_counter()
#     print(ct - bt)
