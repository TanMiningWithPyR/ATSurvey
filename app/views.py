from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi

from . import appbuilder, db
from .models import  Brand, Project

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )

class ProjectModelView(ModelView):
    datamodel = SQLAInterface(Project)

    label_columns = {'brand':'Brand'}
    add_columns = ['id','brand','name','department','personal_name','personal_email','personal_phone','personal_cellphone']
    list_columns = ['id','brand', 'name','department','personal_name','personal_email','personal_phone','personal_cellphone']

    show_fieldsets = [
        (
            'Summary',
            {'fields': ['name', 'department', 'brand']}
        ),
        (
            'Personal Info',
            {'fields': ['personal_name', 'personal_email', 'personal_phone', 'personal_cellphone'], 'expanded': False}
        ),
    ]

class BrandModelView(ModelView):
    datamodel = SQLAInterface(Brand)
    list_columns = ['id', 'name']
    add_columns = ['id', 'name']
    related_views = [ProjectModelView]

db.create_all()
appbuilder.add_view(
    BrandModelView,
    "List Brands",
    icon = "fa-car",
    category = "Brands",
    category_icon = "fa-car"
)
appbuilder.add_view(
    ProjectModelView,
    "List Projects",
    icon = "fa-folder-open-o",
    category = "Brands"
)
