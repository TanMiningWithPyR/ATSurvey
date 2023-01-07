from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from . import db, app
"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""

def key_generator():
	record = db.session.query(Brand).order_by(Brand.id.desc()).first()
	try:
		i = int(record.id) + 1
		if i < 10:
			id = '00' + str(i)
		elif i < 100 :
			id = '0' + str(i)
		else:
			id = str(i)
	except (AttributeError):
		id = '000'

	app.logger.debug("tfy:" + id)
	return  id

class Brand(Model):
	id = Column(String(3), primary_key=True, default=key_generator)
	name = Column(String(50), unique = True, nullable=False)

	def __repr__(self):
		return self.name

class Project(Model):
	id = Column(String(6), primary_key=True)
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