import time

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from schemas import Device, Sample

app = FastAPI(name="continuous monitoring")
app.mount("/static", StaticFiles(directory="./static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", name="home", include_in_schema=False)
def get_home(req: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        name="home.html",
        context={"devices": []},
        request=req,
    )


@app.get("/device/handshake/{deviceId}")
def device_handshake(deviceId: str):
    return {"deviceId": deviceId, "id": 1}


@app.post("/sample/submit")
def receive_sample(sample: Sample):
    print(time.perf_counter() - sample.timeSampled)  # for benchmarking:
    return sample


@app.post("/device/register")
def register_device(device: Device):
    return device
