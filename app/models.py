from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Text
from sqlalchemy.orm import relationship
from flask import Markup, url_for

from . import db, app

from flask_appbuilder.filemanager import get_file_original_name, ImageManager

# from functools import partial
"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
def code_generator(model, code_length):
	record = db.session.query(model).order_by(model.id.desc()).first()
	try:
		i = int(record.id) + 1
		num_0 = code_length - len(str(i))  
		id = num_0 * '0' + str(i)
	except (AttributeError):
		id = code_length * '0'

	app.logger.debug("tfy:" + id)
	return  id

def brand_code_generator():
    return code_generator(Brand, 3)

def project_code_generator():
    return code_generator(Project, 4)

def dealer_code_generator():
    return code_generator(Dealer, 7)

def round_code_generator():
    return code_generator(Round, 6)

def questionnaire_code_generator():
    return code_generator(Questionnaire, 8)

def questionnaire_item_code_generator():
    return code_generator(Questionnaire, 10)

def audit_code_generator():
    return code_generator(Audit, 14)

def project_file_code_generator():
    return code_generator(ProjectFiles,12)

def image_file_code_generator():
    return code_generator(ImageFiles,12)

def audit_item_code_generator():
    return code_generator(AuditItem,16)

class Brand(Model):
    id = Column(String(3), primary_key=True, default=brand_code_generator) 
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name


class Project(Model):
    id = Column(String(4), primary_key=True, default=project_code_generator)
    name = Column(String(150), unique = True, nullable=False)
    department = Column(String(100))
    personal_name = Column(String(100))	
    personal_email = Column(String(100))
    personal_phone = Column(String(20))
    personal_cellphone = Column(String(20))
    brand_id = Column(String(3), ForeignKey('brand.id'))
    brand = relationship("Brand")

    def __repr__(self):
        return self.name	
    
class Dealer(Model):
    id = Column(String(7), primary_key=True, default=dealer_code_generator)
    name = Column(String(50))
    source_dealer_code = Column(String(30))
    type = Column(String(10))
    address = Column(String(200))
    province = Column(String(20))
    city = Column(String(20))
    open_date = Column(Date)
    area_1 = Column(String(20))
    area_2 = Column(String(20))
    brand_id = Column(String(3), ForeignKey('brand.id'))
    brand = relationship("Brand")

    def __repr__(self):
        return self.name

class Round(Model):
    id = Column(String(6), primary_key=True, default=round_code_generator)
    name = Column(String(10))
    open_date = Column(Date)
    close_date = Column(Date)
    project_id = Column(String(4), ForeignKey('project.id'))
    project = relationship("Project")
    
    def __repr__(self):
        return self.name

class Questionnaire(Model):
    id = Column(String(8), primary_key=True, default=questionnaire_code_generator)
    name = Column(String(10))
    round_id = Column(String(4), ForeignKey('round.id'))
    round = relationship("Round")
    
    def __repr__(self):
        return self.name

class Audit(Model):
    id = Column(String(14), primary_key=True, default=audit_code_generator)
    start_date = Column(Date)
    end_date = Column(Date)

    dealer_id = Column(String(7), ForeignKey('dealer.id'))
    dealer = relationship("Dealer",  foreign_keys=dealer_id)    

    questionnaire_id = Column(String(8), ForeignKey('questionnaire.id'))
    questionnaire = relationship("Questionnaire", foreign_keys=questionnaire_id)    

    audit_stage = Column(String(3))

    auditor_id = Column(Integer, ForeignKey('ab_user.id'))
    reviewer1_id = Column(Integer, ForeignKey('ab_user.id'))
    reviewer2_id = Column(Integer, ForeignKey('ab_user.id'))
    reviewer3_id = Column(Integer, ForeignKey('ab_user.id'))
    auditor = relationship("User", foreign_keys=auditor_id)    
    reviewer1 = relationship("User", foreign_keys=reviewer1_id)   
    reviewer2 = relationship("User", foreign_keys=reviewer2_id)   
    reviewer3 = relationship("User", foreign_keys=reviewer3_id)   

    def __repr__(self):
        return self.id
    
class QuestionnaireItem(Model):
    id = Column(String(10), primary_key=True, default=questionnaire_item_code_generator)
    source_level_1 = Column(String(50))
    source_level_2 = Column(String(50))
    source_level_3 = Column(String(50))
    source_level_4 = Column(String(50))
    source_level_5 = Column(String(50))
    source_level_6 = Column(String(50))
    my_function_level_1 = Column(String(50))
    my_function_level_2 = Column(String(50))
    my_function_level_3 = Column(String(50))
    my_facility_area_code = Column(String(10))
    my_information_code = Column(String(10))
    my_car_lifecycle = Column(String(10))
    my_dealer_lifecycle = Column(String(10))
    item_code = Column(String(20))  # source_level_1_code & source_level_2_code & source_level_3_code & source_level_4_code & source_level_5_code & source_level_6_code 
    item = Column(String(200))
    item_score = Column(Float)
    questionnaire_id = Column(String(8), ForeignKey('questionnaire.id'))
    questionnaire = relationship("Questionnaire")
    
    def __repr__(self):
        return self.item

class AuditItem(Model):
    id = Column(String(16), primary_key=True, default=audit_item_code_generator)
    questionnaire_item_id = Column(String(10), ForeignKey('questionnaire_item.id'))
    questionnaire_item = relationship("QuestionnaireItem", foreign_keys = questionnaire_item_id)

    audit_id = Column(String(10), ForeignKey('audit.id'))
    audit = relationship('Audit', foreign_keys = audit_id)

    # answer content for audit, review.
    answer_choose_audit = Column(Integer)
    answer_content_audit = Column(Text)

    answer_choose_viewer1 = Column(Integer)
    answer_content_viewer1 = Column(Text)

    answer_choose_viewer2 = Column(Integer)
    answer_content_viewer2 = Column(Text)

    answer_choose_viewer3 = Column(Integer)
    answer_content_viewer3 = Column(Text)

    def __repr__(self):
        return self.id

class ProjectFiles(Model):
    id = Column(String(12), primary_key=True, default=project_file_code_generator)
    audit_item_id = Column(String(16), ForeignKey("audit_item.id"))
    audit_item = relationship("AuditItem")
    file = Column(FileColumn, nullable=False)
    description = Column(String(150))

    def download(self):
        return Markup(
            '<a href="'
            + url_for("ProjectFilesView.download", filename=str(self.file))
            + '">Download</a>'
        )

    def file_name(self):
        return get_file_original_name(str(self.file))

class ImageFiles(Model):
    id = Column(String(12), primary_key=True, default=image_file_code_generator)
    audit_item_id = Column(String(16), ForeignKey("audit_item.id"))
    audit_item = relationship("AuditItem")
    photo = Column(ImageColumn(thumbnail_size=(30, 30, True), size=(300, 300, True)))
    description = Column(String(150))

    def photo_img(self):
        im = ImageManager()
        if self.photo:
            return Markup(
                '<a href="' +
                url_for("ImageFilesView.show", pk=str(self.id)) +
                '" class="thumbnail"><img src="' +
                im.get_url(self.photo) +
                '" alt="Photo" class="img-rounded img-responsive"></a>'
            )
        else:
            return Markup(
                '<a href="' +
                url_for("ImageFilesView.show", pk=str(self.id)) +
                '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive">'
                '</a>'
            )

    def photo_img_thumbnail(self):
        im = ImageManager()
        if self.photo:
            return Markup(
                '<a href="' +
                url_for("ImageFilesView.show", pk=str(self.id)) +
                '" class="thumbnail"><img src="' +
                im.get_url_thumbnail(self.photo) +
                '" alt="Photo" class="img-rounded img-responsive"></a>'
            )
        else:
            return Markup(
                '<a href="' +
                url_for("ImageFilesView.show", pk=str(self.id)) +
                '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive">'
                '</a>'
            )