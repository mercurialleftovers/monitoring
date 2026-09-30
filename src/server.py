from queue import Queue

from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocketDisconnect

from schemas import Device, Sample
from tools import WSManager

app = FastAPI(name="continuous monitoring")
app.mount("/static", StaticFiles(directory="./static"), name="static")

wsManger = WSManager()
readings: Queue[Sample] = Queue()

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
    readings.put(sample)
    return {"status": "ok"}  # TODO(bader): what is the practice here ?


@app.post("/device/register")
def register_device(device: Device):
    return device


@app.websocket("/ws")
async def manage_websockets(ws: WebSocket):
    await wsManger.connect(ws)
    try:
        while True:
            # send it sensor data
            if readings.qsize() > 0:
                await ws.send_text(
                    # json.dumps(readings.get().model_dump())
                    # readings.get().model_dump_json()
                    readings.get(block=True).model_dump_json()
                )  # NOTE(bader): Queue.get has a block=True arg, which makes the thread wait until elements exist
    except WebSocketDisconnect:
        print(f"ws {ws} closed.")
        await wsManger.disconnect(ws)
