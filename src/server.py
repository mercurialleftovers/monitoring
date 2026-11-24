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
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, func
from sqlalchemy.orm import Session

os.system("clear")

from database import get_db_session
from enums import DeviceType, Department, Role
from models import Device, User, Event

# from schemas import DeviceInfo, Sample, UserSchema
from schemas import DeviceInfo, Sample, UserCreateRequest, UserCreateResponse
from tools import WSManager
from constants import (
    DIRS,
)

DEBUG: bool = False


auth_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI(title="continuous monitoring")
app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")
role_emojis: dict[Role, str] = {
    Role.TECHNICIAN: "⚙",
    Role.ENGINEER: "⚙",
    Role.SUPERVISOR: "👁",
    Role.OPERATOR: "🖐",
    Role.INTERN: "👶",
}

wsManger = WSManager()
readings: Queue[Sample] = Queue()
currentId: int = 0

templates = Jinja2Templates(directory="./frontend/templates")

# TODO(bader): logging
# TODO(bader): uv init and reordering project files
# TODO(bader): dockerization (delivery)


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


@app.post("/sample/submit", tags=["data"])
async def receive_sample(sample: Sample):
    # TODO(bader): instead of adding a datum to the quque, sendi t directly through ws
    for ws_connection in wsManger.active_connections:
        try:
            await ws_connection.send_text(sample.model_dump_json())
        except WebSocketDisconnect:
            await wsManger.disconnect(ws_connection)

    return {"status": "ok"}  # TODO(bader): what is the practice here ?


@app.post("/ap1/device/register", name="register_device_api_1", tags=["devices"])
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


@app.get(
    "/device/register",
    name="register_device_view",
    tags=["devices"],
    include_in_schema=False,
)
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


@app.post("/device/info", tags=["devices"])
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
    return DeviceInfo.from_orm(deviceInDb)


@app.post("/device/byid", tags=["devices"])
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


@app.get("/device/all", tags=["devices"])
def get_all_devices(
    db_session: Annotated[Session, Depends(get_db_session)],
):
    return db_session.execute(select(Device)).scalars().all()


@app.get("/device/control/{{id}}", include_in_schema=False, tags=["devices"])
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
            "title": f"{device_in_db.name}",
            "device": device_in_db,
        },
    )


@app.post(
    "/device/register",
    name="register_device_api",
    tags=[
        "device",
    ],
)
async def add_device_api(
    req: Request,
    db_session: Annotated[Session, Depends(get_db_session)],
    # device fields
    name: Annotated[str, Form()],
    tag: Annotated[str, Form()],
    department: Annotated[Department, Form()],
    category: Annotated[DeviceType, Form()],
    # device image file
    device_image: UploadFile,
):
    # checking if username exsits:
    device_in_db: Device | None = db_session.execute(
        select(Device).where(Device.tag == tag)
    ).scalar_one_or_none()

    if device_in_db:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"device @{tag} already exists",
        )

    # TODO(bader): img file validation: extension + size

    device_image_saved: bool = False
    if device_image:
        device_image_path: str = f"frontend/static/images/devices_images/{tag}"
        print(device_image_path)

        with open(device_image_path, "wb") as device_image_file:
            device_image_file.write(device_image.file.read())
            device_image_saved = True
            print(f"device image saved: {device_image.file.read()}")
    else:
        print(f"device image not saved: {device_image.file.read()}")

    new_device: Device = Device(
        name=name,
        tag=tag,
        department=department,
        category=category,
        has_image=device_image_saved,
    )

    # adding new device to db
    db_session.add(new_device)
    return RedirectResponse("/devices")


@app.get("/devices", name="devices_view", include_in_schema=False, tags=["devices"])
def get_devices(
    req: Request,
    db_session: Annotated[Session, Depends(get_db_session)],
):
    devices = db_session.execute(select(Device)).scalars().all()
    return templates.TemplateResponse(
        request=req,
        name="devices.html",
        context={
            "title": "devices",
            "devices": devices,
        },
    )


@app.get(
    "/user/register", name="register_user_view", include_in_schema=False, tags=["users"]
)
def add_user_view(req: Request):
    return templates.TemplateResponse(
        name="create_user.html",
        request=req,
        context={
            "roles": [role for role in Role],
            "emojis": role_emojis,
            "title": "New User",
        },
    )


@app.post("/user/register", name="register_user_api", tags=["users"])
def add_user(
    userRequst: Annotated[UserCreateRequest, Form()],
    db_session: Annotated[Session, Depends(get_db_session)],
):

    # creating the user, initially w/o a profile_picture
    new_user = User(
        username=userRequst.username,
        password=userRequst.password,
        email=userRequst.email,
        phone=userRequst.phone,
        firstname=userRequst.firstname,
        lastname=userRequst.lastname,
        role=userRequst.role,
    )

    user_profile_pic_filename: str | None = None

    if userRequst.profile_picture:
        image_filename: str | None = (
            userRequst.profile_picture.filename
        )  # NOTE(bader): how is it supposed to be None if profile_picture exists ?

        if DEBUG:
            print(userRequst.model_dump())
            from PIL import Image

            profile_picture = Image.open(userRequst.profile_picture.file)
            profile_picture.show()
            # print(f"result of opening: {result}")
            return

        if image_filename:
            # TODO(bader): profile pictures should be (username).(ext)
            # regex ought to do it
            import re

            raw_regex: str = r"(.+)\.([\w|\d]{3,8})$"  # filename . extension
            regex = re.compile(raw_regex)
            matched = regex.search(image_filename)
            if matched:
                _, extension = matched.group(1, 2)  # _ is the filename as uploaded
                user_profile_pic_filename = f"{userRequst.username}.{extension}"
                # saving image file to static storage:
                with open(
                    f"{DIRS.user_profile_pictures}/{user_profile_pic_filename}",
                    "wb",
                ) as new_profile_image:
                    new_profile_image.write(userRequst.profile_picture.file.read())

    if user_profile_pic_filename:
        new_user.profile_picture = user_profile_pic_filename

    db_session.add(new_user)

    return UserCreateResponse(**userRequst.model_dump())


@app.get("/users", name="users_view", include_in_schema=False)
def get_users(
    req: Request,
    db_session: Annotated[Session, Depends(get_db_session)],
):
    users = db_session.execute(select(User)).scalars().all()
    return templates.TemplateResponse(
        request=req,
        name="users.html",
        context={
            "title": "users",
            "users": users,
            "roles": db_session.execute(select(User.role).distinct()).scalars(),
            "emojis": role_emojis,
        },
    )


@app.post(
    "/token",
    tags=[
        "security",
    ],
)
def auth_user(token: Annotated[str, Depends(auth_scheme)]):
    return {"token": token}


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


@app.get("/events", name="events_view", include_in_schema=False)
def render_events_view(
    req: Request,
    db_session: Annotated[Session, Depends(get_db_session)],
):
    events = db_session.execute(
        select(Event)
        .order_by(Event.date.desc)
        .limit(
            100
        )  # TODO(bader): refactor into a constant, or a dotenv entry, maybe even an admin table (admin dashboard)
    ).scalars()

    return templates.TemplateResponse(
        request=req,
        name="events.html",
        context={
            "title": "events",
            "events": events,
        },
    )


@app.websocket("/ws")
async def manage_websockets(ws: WebSocket):
    await wsManger.connect(ws)
    # TODO(bader): find a better alternative (while keeps the connection from closing)
    while True:
        try:
            await asyncio.sleep(5)
        except WebSocketDisconnect:
            await wsManger.disconnect(ws)
            return


# --- testing stuff NOTE(bader): non-production stuff
from pydantic import BaseModel


class DataModel(BaseModel):
    username: str
    pasword: str
    email: str
    image: UploadFile


@app.get("/test", include_in_schema=False)
def receive_files_and_data_view(req: Request):
    return templates.TemplateResponse(
        name="form_with_files.html",
        request=req,
        context={"title": "a form with a file"},
    )


@app.post("/files_n_data")
def receive_files_and_data(data: Annotated[DataModel, Form()], file_: UploadFile):
    return {"data": data, "file": file_}


from faker import Faker

my_faker = Faker()
import random


@app.get("/populate_db/{num_users}/{num_devices}")
async def populate(
    num_users: int,
    num_devices: int,
    db_session: Annotated[Session, Depends(get_db_session)],
):
    for i in range(num_users):
        first_name = random.choice(
            [
                my_faker.first_name(),
                my_faker.first_name(),
            ]
        )
        last_name = random.choice(
            [
                my_faker.last_name(),
                my_faker.last_name(),
            ]
        )
        username = my_faker.user_name()
        role = random.choice(list(Role))
        email = my_faker.email()
        phone = my_faker.phone_number()
        password = my_faker.password()

        db_session.add(
            User(
                username=username,
                password=password,
                lastname=last_name,
                firstname=first_name,
                email=email,
                phone=phone,
                role=role,
            )
        )

    for i in range(num_devices):
        prefix = random.choice(
            [
                my_faker.first_name(),
                my_faker.first_name(),
            ]
        )
        category = random.choice(list(DeviceType))
        department = random.choice(list(Department))
        tag = f"category_{prefix} {i}"
        name = f"{prefix} {i} {category.value} {department.value}"

        db_session.add(
            Device(
                name=name,
                category=category,
                tag=tag,
                department=department,
            )
        )
