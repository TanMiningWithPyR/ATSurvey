from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView, CompactCRUDMixin

from . import appbuilder, db
from .models import  Brand, Project, Dealer, Round, Audit, Questionnaire, QuestionnaireItem, AuditItem, ImageFiles, ProjectFiles

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

class ProjectFilesView(ModelView):
    datamodel = SQLAInterface(ProjectFiles)

    list_columns = ['id', 'audit_item', 'file', 'description']
    add_columns = ['id', 'audit_item', 'file', 'description'] 

class ImageFilesView(ModelView):
    datamodel = SQLAInterface(ImageFiles)

    list_columns = ['id', 'audit_item', 'description', 'photo']
   # , 'photo_img_thumbnail']
    add_columns = ['id', 'audit_item', 'description', 'photo']
   # , 'photo_img_thumbnail']

class AuditItemView(ModelView):
    datamodel = SQLAInterface(AuditItem)

    # show_template = "appbuilder/general/model/show_cascade.html"
    # edit_template = "appbuilder/general/model/edit_cascade.html"

    list_columns = ['audit', 'questionnaire_item', 'answer_choose_audit','answer_content_audit',
    'answer_choose_viewer1','answer_content_viewer1',
    'answer_choose_viewer2','answer_content_viewer2',
    'answer_choose_viewer3','answer_content_viewer3']
    add_columns = ['audit', 'questionnaire_item', 'answer_choose_audit','answer_content_audit',
    'answer_choose_viewer1','answer_content_viewer1',
    'answer_choose_viewer2','answer_content_viewer2',
    'answer_choose_viewer3','answer_content_viewer3']
      
    related_views = [ImageFilesView, ProjectFilesView]  

class AuditView(ModelView):
    datamodel = SQLAInterface(Audit)

    list_columns = ['id', 'start_date', 'end_date', 'dealer', 'questionnaire', 'audit_stage', 'auditor','reviewer1','reviewer2','reviewer3']
    add_columns = ['id', 'start_date', 'end_date', 'dealer', 'questionnaire', 'audit_stage', 'auditor','reviewer1','reviewer2','reviewer3']

    show_fieldsets = [
        (
            'Summary',
            {'fields': ['start_date', 'end_date', 'dealer','questionnaire','audit_stage']}
        ),
        (
            'Audit Info',
            {'fields': ['auditor','reviewer1','reviewer2','reviewer3'], 'expanded': False}
        ),
    ]

    related_views = [AuditItemView]  

class QuestionnaireItemView(ModelView):
    datamodel = SQLAInterface(QuestionnaireItem)

    list_columns = ['id','questionnaire','source_level_1','source_level_2','source_level_3','source_level_4','source_level_5','source_level_6',
    'my_function_level_1','my_function_level_2','my_function_level_3','my_facility_area_code','my_information_code','my_car_lifecycle','my_dealer_lifecycle',
    'item_code','item', 'item_score']
    add_columns = ['id','questionnaire','source_level_1','source_level_2','source_level_3','source_level_4','source_level_5','source_level_6',
    'my_function_level_1','my_function_level_2','my_function_level_3','my_facility_area_code','my_information_code','my_car_lifecycle','my_dealer_lifecycle',
    'item_code','item', 'item_score']

    show_fieldsets = [
        (
            'Summary',
            {'fields': ['name', 'questionnaire', 'source_level_1','source_level_2','source_level_3','source_level_4','source_level_5','source_level_6']}
        ),
        (
            'Questionnaire Item Info',
            {'fields': ['item_code','item', 'item_score', 'my_function_level_1','my_function_level_2','my_function_level_3','my_facility_area_code','my_information_code','my_car_lifecycle','my_dealer_lifecycle'], 'expanded': False}
        ),
    ]

    related_views = [AuditItemView] 

class QuestionnaireView(ModelView):
    datamodel = SQLAInterface(Questionnaire)

    list_columns = ['id', 'name','round']
    add_columns = ['id', 'name', 'round']
      
    related_views = [QuestionnaireItemView, AuditView]  

class RoundModelView(ModelView):
    datamodel = SQLAInterface(Round)

    label_columns = {'project':'Project'}
    add_columns = ['id','project','name','open_date','close_date']
    list_columns = ['id','project', 'name','open_date','close_date']

    show_fieldsets = [
        (
            'Summary',
            {'fields': ['name', 'project']}
        ),
        (
            'Round Info',
            {'fields': ['open_date', 'close_date'], 'expanded': False}
        ),
    ]

    related_views = [QuestionnaireView]  


class DealerModelView(ModelView):
    datamodel = SQLAInterface(Dealer)

    label_columns = {'brand':'Brand'}
    add_columns = ['id','brand','type','source_dealer_code','name','address','province','city','open_date','area_1','area_2']
    list_columns = ['id','brand','type','source_dealer_code','name','address','province','city','open_date','area_1','area_2']

    show_fieldsets = [
        (
            'Summary',
            {'fields': ['name', 'source_dealer_code', 'brand','type']}
        ),
        (
            'Dealer Info',
            {'fields': ['address','province','city','open_date','area_1','area_2'], 'expanded': False}
        ),
    ]

    #related_views = [QuestionnaireView]

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

    related_views = [RoundModelView]

class BrandModelView(ModelView):
    datamodel = SQLAInterface(Brand)
    list_columns = ['id', 'name']
    add_columns = ['id', 'name']
    related_views = [ProjectModelView, DealerModelView]

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

appbuilder.add_view(
    DealerModelView,
    "List Dealers",
    icon = "fa-folder-open-o",
    category = "Brands"
)

appbuilder.add_view(
    RoundModelView,
    "List Rounds",
    icon = "fa-folder-open-o",
    category = "Questionnaires",
    category_icon = "fa-car"
)

appbuilder.add_view(
    QuestionnaireView,
    "List Questionnaires",
    icon = "fa-car",
    category = "Questionnaires"
)

appbuilder.add_view(
    QuestionnaireItemView,
    "List Questionnaire Item",
    icon = "fa-car",
    category = "Questionnaires"
)

appbuilder.add_view(
    AuditView,
    "List Audit",
    icon = "fa-car",
    category = "Audit"
)

appbuilder.add_view(
    AuditItemView,
    "List Audit Item",
    icon = "fa-car",
    category = "Audit"
)

# appbuilder.add_view_no_menu(ImageFilesView)
appbuilder.add_view_no_menu(ProjectFilesView)

appbuilder.add_view(
    ImageFilesView,
    "List Image Files",
    icon = "fa-car",
    category = "Audit"
)