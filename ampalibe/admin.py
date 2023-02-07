import inspect
from .model import DataBaseConfig
from sqlalchemy import create_engine
from starlette_admin.views import Link, DropDown
from sqlalchemy.ext.declarative import declarative_base
from starlette_admin.contrib.sqla.admin import Admin
from starlette_admin.contrib.sqla.view import ModelView

Base = declarative_base()
allModelViews = []


try:
    import models  # type: ignore

    clsmembers = inspect.getmembers(models, inspect.isclass)
    for name, obj in clsmembers:
        if name == "Base":
            continue
        if hasattr(obj, "__tablename__"):
            allModelViews.append(ModelView(obj))
except ImportError as err:
    print(err)

engine = create_engine(
    DataBaseConfig().get_db_url(), connect_args={"check_same_thread": False}
)
Base.metadata.create_all(engine)


admin_app = Admin(
    engine=engine,
    title="Ampalibe Admin",
    logo_url="https://raw.githubusercontent.com/iTeam-S/Ampalibe/main/docs/source/_static/ampalibe_logo.png",
)

admin_app.add_view(Link(label="Home Page", icon="fa fa-home", url="/admin"))
admin_app.add_view(DropDown("Content", icon="fa fa-list", views=allModelViews))
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
