from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from . import db, app

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