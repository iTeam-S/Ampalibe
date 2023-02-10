import inspect
from .model import DataBaseConfig
from .constant import AMPALIBE_LOGO
from sqlmodel import create_engine, SQLModel
from starlette_admin.contrib.sqlmodel.admin import Admin
from starlette_admin.contrib.sqlmodel.view import ModelView
from starlette_admin.views import Link, DropDown, CustomView


allCustomViews = []
engine = create_engine(
    DataBaseConfig().get_db_url(), connect_args={"check_same_thread": False}
)
SQLModel.metadata.create_all(engine)


try:
    import resources  # type: ignore

    clsmembers = inspect.getmembers(resources, inspect.isclass)
    for name, obj in clsmembers:
        if name in ("CustomView", "ModelView"):
            continue
        if issubclass(obj, (CustomView, ModelView)):
            allCustomViews.append(obj)

except ImportError as err:
    print(err)


admin_app = Admin(
    engine=engine,
    title="Ampalibe Admin",
    login_logo_url=AMPALIBE_LOGO,
    logo_url=AMPALIBE_LOGO,
)

admin_app.add_view(Link(label="Home Page", icon="fa fa-home", url="/admin"))
admin_app.add_view(DropDown("Content", icon="fa fa-list", views=allCustomViews))
admin_app.add_view(
    Link(
        label="Documentation",
        icon="fa fa-book",
        url="https://ampalibe.readthedocs.io",
        target="_blank",
    )
)
admin_app.add_view(
    Link(
        label="Github",
        icon="fa fa-link",
        url="https://github.com/iTeam-S/Ampalibe",
        target="_blank",
    )
)
admin_app.add_view(
    Link(
        label="PyPi",
        icon="fa fa-link",
        url="https://pypi.org/project/ampalibe/",
        target="_blank",
    )
)
admin_app.add_view(
    Link(
        label="Facebook Community",
        icon="fa fa-link",
        url="",
        target="_blank",
    )
)
