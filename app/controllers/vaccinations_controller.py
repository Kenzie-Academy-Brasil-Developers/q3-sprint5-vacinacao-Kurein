from flask import request, jsonify
from http import HTTPStatus
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Query
from app.configs.database import db
from app.models.vaccinations_model import VaccineCards


def post_vaccination():

   data = request.get_json()

   vaccine_card = VaccineCards(**data)

   session: Session = db.session()

   session.add(vaccine_card)
   session.commit()
   
   return jsonify(vaccine_card), HTTPStatus.CREATED

def get_vaccinations():
   
   base_query: Query = db.session.query(VaccineCards)

   records = base_query.all()

   return jsonify(records), HTTPStatus.OK
