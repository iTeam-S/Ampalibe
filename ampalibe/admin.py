import inspect
import hashlib
from .logger import Logger
from typing import Optional
from datetime import datetime
from .model import DataBaseConfig
from .constant import AMPALIBE_LOGO
from starlette.requests import Request
from sqladmin import Admin, ModelView, BaseView
from sqladmin.authentication import AuthenticationBackend
from sqlmodel import select, create_engine, Field, Session, SQLModel


engine = create_engine(
    DataBaseConfig().get_db_url()
)


class AdminModel(SQLModel, table=True):
    __tablename__ = "admin_user"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True, nullable=False)
    password: str = None
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    last_edited: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class AdminUser(ModelView, model=AdminModel):
    column_list = [
        AdminModel.id,
        AdminModel.username,
        AdminModel.password,
        AdminModel.last_edited,
        AdminModel.created_at,
    ]
    icon = "fa-solid fa-user-secret"
    can_export = False

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True

    async def after_model_change(self, data, model, is_created):
        with Session(engine) as session:
            statement = select(AdminModel).where(AdminModel.id == model.id)
            results = session.exec(statement)
            admin_model = results.one()
            admin_model.username = data.get("username")
            admin_model.password = hashlib.sha256(
                data.get("password").encode()
            ).hexdigest()
            session.add(admin_model)
            session.commit()
            session.refresh(admin_model)


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        with Session(engine) as session:
            statement = (
                select(AdminModel)
                .where(AdminModel.username == username)
                .where(
                    AdminModel.password == hashlib.sha256(password.encode()).hexdigest()
                )
            )
            results = session.exec(statement)
            verif = len(results.all()) > 0

        if verif:
            request.session.update({"token": "..."})
        return verif

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            with Session(engine) as session:
                statement = select(AdminModel)
                results = session.exec(statement)
                if len(results.all()) == 0:
                    session.add(
                        AdminModel(
                            username="admin",
                            password=hashlib.sha256(b"ampalibe").hexdigest(),
                        )
                    )
                    session.commit()
            return False
        return True


def init_admin(app):
    views = get_user_resources()
    SQLModel.metadata.create_all(engine)
    admin = Admin(
        app,
        engine,
        title="Ampalibe Admin",
        logo_url=AMPALIBE_LOGO,
        authentication_backend=AdminAuth(secret_key="..."),
    )
    for view in views:
        admin.add_view(view)


def get_user_resources():
    allViews = [AdminUser]
    try:
        import resources  # type: ignore

        clsmembers = inspect.getmembers(resources, inspect.isclass)
        for name, obj in clsmembers:
            if name in ("ModelView", "BaseView"):
                continue
            if issubclass(obj, (ModelView, BaseView)):
                allViews.append(obj)

    except Exception as err:
        Logger.warning(err)

    finally:
        return allViews
