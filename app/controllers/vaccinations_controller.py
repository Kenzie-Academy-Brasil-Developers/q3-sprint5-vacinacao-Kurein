from flask import request, jsonify
from http import HTTPStatus
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Query
from app.configs.database import db
from app.models.vaccinations_model import VaccineCards
import datetime
from sqlalchemy.exc import IntegrityError

def post_vaccination():
   data = request.get_json()

   fieldnames= ["cpf", "name", "vaccine_name", "health_unit_name"]
   items = data.items()

   for key, value in items:
      if type(value) != str:
         return {'error': f'key {key} not a string'}, HTTPStatus.BAD_REQUEST

   try:
      if len(data["cpf"]) != 11:
         return {'error': 'cpf lenght not authorized'}, HTTPStatus.BAD_REQUEST
   except KeyError:
      return {'error': 'cpf key missing or wrong'}, HTTPStatus.BAD_REQUEST

   try:
      int(data["cpf"])
   except ValueError:
      return {'error': 'cpf has a character that is not a number'}, HTTPStatus.BAD_REQUEST

   filtered_data= dict()

   for key, value in items:
      if key in fieldnames:
         filtered_data[f'{key}'] = value

   try: 
      filtered_data["first_shot_date"] = datetime.datetime.now()
      filtered_data["second_shot_date"]= filtered_data["first_shot_date"] + datetime.timedelta(days=90)
      filtered_data["name"]= filtered_data["name"].title()
      filtered_data["vaccine_name"]= filtered_data["vaccine_name"].title()
      filtered_data["health_unit_name"]= filtered_data["health_unit_name"].title()
   except KeyError:
      return {'error': 'key missing, or spelled wrong', 'keys': fieldnames}, HTTPStatus.BAD_REQUEST

   vaccine_card = VaccineCards(**filtered_data)

   session: Session = db.session()

   try:
      session.add(vaccine_card)
      session.commit()
   except IntegrityError:
      return {'error': 'cpf already in use'}, HTTPStatus.CONFLICT
      
   return jsonify(vaccine_card), HTTPStatus.CREATED

def get_vaccinations():
   
   base_query: Query = db.session.query(VaccineCards)

   records = base_query.all()

   return jsonify(records), HTTPStatus.OK
