import asyncio
import os
from queue import Queue
from typing import Annotated

from fastapi import Depends, FastAPI, Request, WebSocket, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.orm import Session

os.system("clear")

from database import get_db_session
from models import Device
from schemas import DeviceInfo, Sample
from tools import WSManager

app = FastAPI(name="continuous monitoring")
app.mount("/static", StaticFiles(directory="./static"), name="static")

wsManger = WSManager()
readings: Queue[Sample] = Queue()
currentId: int = 0

templates = Jinja2Templates(directory="templates")


def RequestLogger(req: Request):
    print(req)


# app.mount("/", RequestLogger)


@app.get("/", name="home", include_in_schema=False)
def get_home(req: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        name="home.html",
        context={"devices": []},
        request=req,
    )


@app.get("/device/handshake/{deviceId}")
def device_handshake(
    deviceId: str,
    db_session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> int:
    device: Device | None = db_session.execute(
        select(Device).where(Device.identifier == deviceId)
    ).scalar_one_or_none()
    if not device:
        print(
            f"device with identifier {deviceId} does not exist.",
        )
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"device with identifier {deviceId} does not exist.",
        )

    return device.id


@app.post("/sample/submit")
def receive_sample(sample: Sample):
    readings.put(sample)
    return {"status": "ok"}  # TODO(bader): what is the practice here ?


@app.post("/device/register")
def register_device(
    device: DeviceInfo,
    db_session: Annotated[Session, Depends(get_db_session)],
):
    existing_device: Device | None = (
        db_session.execute(select(Device).where(Device.identifier == device.identifier))
        .scalars()
        .one_or_none()
    )
    if existing_device:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, f"device {device.identifier} already exists."
        )

    db_session.add(
        Device(
            deviceName=device.name,
            identifier=device.identifier,
            category=device.deviceType,
        )
    )
    return device


@app.post("/device/info")
def get_device_info(
    identifier: str, db_session: Annotated[Session, Depends(get_db_session)]
):
    deviceInDb: Device | None = (
        db_session.execute(select(Device).where(Device.identifier == identifier))
        .scalars()
        .one_or_none()
    )
    if not deviceInDb:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"no device with id {identifier}",
        )
    return DeviceInfo.from_orm(deviceInDb)


@app.post("/device/byid")
def get_device_by_id(
    id: int,
    db_session: Annotated[Session, Depends(get_db_session)],
):
    device: Device | None = (
        db_session.execute(select(Device).where(Device.id == id))
        .scalars()
        .one_or_none()
    )
    if not device:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"device {id} does not exist.")

    return device


@app.get("/device/all")
def get_all_devices(
    db_session: Annotated[Session, Depends(get_db_session)],
):
    return db_session.execute(select(Device)).scalars().all()


@app.websocket("/ws")
async def manage_websockets(ws: WebSocket):
    await wsManger.connect(ws)
    try:
        while True:
            if readings.qsize() > 0:
                await ws.send_text(readings.get().model_dump_json())
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print(f"ws {ws} closed.")
        # log instead
        await wsManger.disconnect(ws)
