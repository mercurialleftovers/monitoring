import shutil
from pathlib import Path
import asyncio
import os
from queue import Queue
from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
    Request,
    WebSocket,
    status,
    Form,
    UploadFile,
)

from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocketDisconnect
from sqlalchemy import select, func
from sqlalchemy.orm import Session

os.system("clear")

from database import get_db_session
from enums import DeviceType, Department, Role
from models import Device
from schemas import DeviceInfo, Sample, User
from tools import WSManager

app = FastAPI(title="continuous monitoring")
app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")

wsManger = WSManager()
readings: Queue[Sample] = Queue()
currentId: int = 0

templates = Jinja2Templates(directory="./frontend/templates")


def RequestLogger(req: Request):
    print(req)


# app.mount("/", RequestLogger)


@app.get("/", name="home", include_in_schema=False)
def get_home(
    req: Request, db_session: Annotated[Session, Depends(get_db_session)]
) -> HTMLResponse:
    devices = db_session.execute(select(Device)).scalars().all()
    categories = db_session.execute(select(Device.category).distinct()).scalars()
    return templates.TemplateResponse(
        name="home.html",
        context={
            "devices": devices,
            # "categories": [category.value for category in DeviceType],
            "categories": categories,
            "title": "Home",
        },
        request=req,
    )


@app.get("/favicon.ico")
def favicon() -> RedirectResponse:
    return RedirectResponse("/static/images/favicon.png")


@app.get("/device/handshake/{deviceId}")
def device_handshake(
    deviceId: str,
    db_session: Annotated[
        Session,
        Depends(get_db_session),
    ],
) -> int:
    device: Device | None = db_session.execute(
        select(Device).where(Device.tag == deviceId)
    ).scalar_one_or_none()
    if not device:
        print(
            f"device with id {deviceId} does not exist.",
        )
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"device with id {deviceId} does not exist.",
        )

    # TODO(bader): use sessions for security
    return device.id


@app.post("/sample/submit")
async def receive_sample(sample: Sample):
    # TODO(bader): instead of adding a datum to the quque, sendi t directly through ws
    for ws_connection in wsManger.active_connections:
        try:
            await ws_connection.send_text(sample.model_dump_json())
        except WebSocketDisconnect:
            await wsManger.disconnect(ws_connection)

    return {"status": "ok"}  # TODO(bader): what is the practice here ?


@app.post("/device/register", name="register_device_api")
def register_device(
    # device: DeviceInfo,
    device: Annotated[DeviceInfo, Form()],
    db_session: Annotated[Session, Depends(get_db_session)],
):
    existing_device: Device | None = (
        db_session.execute(select(Device).where(Device.tag == device.tag))
        .scalars()
        .one_or_none()
    )
    if existing_device:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, f"device {device.tag} already exists."
        )

    db_session.add(
        Device(
            deviceName=device.name,
            tag=device.tag,
            category=device.deviceType,
            department=device.department,
        )
    )
    return device


@app.get("/device/register", name="register_device_view", include_in_schema=False)
def register_device_view(req: Request):
    return templates.TemplateResponse(
        name="register_device.html",
        request=req,
        context={
            "categories": [t.value for t in DeviceType],
            "departments": [t.value for t in Department],
            "title": "New Device",
        },
    )


@app.post("/device/info")
def get_device_info(tag: str, db_session: Annotated[Session, Depends(get_db_session)]):
    deviceInDb: Device | None = (
        db_session.execute(select(Device).where(Device.tag == tag))
        .scalars()
        .one_or_none()
    )
    if not deviceInDb:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"no device with id {tag}",
        )
    return tag.from_orm(deviceInDb)


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


@app.get("/device/control/{{id}}", include_in_schema=False)
def setup_device(
    db_session: Annotated[Session, Depends(get_db_session)],
    id: int,
    req: Request,
):
    device_in_db: Device | None = db_session.execute(
        select(Device).where(Device.id == id)
    ).scalar_one_or_none()

    if not device_in_db:
        return templates.TemplateResponse(
            name="error",
            request=req,
            context={"title": "error", "message": f"device {id} does not exists."},
        )

    return templates.TemplateResponse(
        name="devicePage",
        request=req,
        context={
            "title": f"{device_in_db.deviceName}",
            "device": device_in_db,
        },
    )


@app.get("/user/register", name="register_user_view", include_in_schema=False)
def add_user_view(req: Request):
    return templates.TemplateResponse(
        name="create_user.html",
        request=req,
        context={
            "roles": [role.value for role in Role],
            "title": "New User",
        },
    )


@app.post(
    "/user/register",
    name="register_user_api",
    tags=[
        "user management",
    ],
)
# def add_user_api(user: Annotated[User, Form()]):
async def add_user_api(
    req: Request,
    username: Annotated[str, Form()],
    firstname: Annotated[str, Form()],
    lastname: Annotated[str, Form()],
    password: Annotated[str, Form()],
    email: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    function: Annotated[Role, Form()],
    # profile_pic: Annotated[bytes | None, File()] = None,
    profile_pic: UploadFile,
):
    print(type(profile_pic))  # whether an api is needed to extract the actual file

    # validation
    # inserting user into the db
    # moving the profile_pic into the static profile_pics folder
    if profile_pic:
        profile_pics_dir: Path = Path(req.url_for("static", path="images/profile_pics"))
        print(profile_pics_dir)
        # print(type(profile_pic.file))
        print(profile_pic.file.read())
        print(type(profile_pic.file.read()))

        # TODO(bader): img file validation: extension + size
        # print(profile_pics_dir)
        # with open()
        # shutil.copyfileobj

    return {
        "username": username,
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "password": password,
        "function": function,
        "phone": phone,
        "profile_pic": profile_pic,
    }


@app.get("/devices/count")
def get_device_count(
    db_session: Annotated[Session, Depends(get_db_session)],
) -> dict[str, int]:
    count_func = func.count(Device.id)
    return {"count": db_session.execute(select(count_func)).scalar_one()}


@app.get("/canvas")
def render_canvas(req: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        name="canvas_demo.html",
        context={"title": "Canvas Demo"},
        request=req,
    )


@app.websocket("/ws")
async def manage_websockets(ws: WebSocket):
    await wsManger.connect(ws)
    # print("ws connection established")
    # print(f"{len(wsManger.active_connections)} connections maintained connections md")
    # TODO(bader): fixing this asap
    # try:
    # while True:
    #     if readings.qsize() > 0:
    #         await ws.send_text(readings.get().model_dump_json())
    #     await asyncio.sleep(1)

    # except WebSocketDisconnect:
    #     print(f"ws {ws} closed.")
    #     # log instead
    #     await wsManger.disconnect(ws)
    while True:
        try:
            await asyncio.sleep(5)
        except WebSocketDisconnect:
            await wsManger.disconnect(ws)
            return
