import json
import logging
import os
import sys

from flask import Flask, request, jsonify
from flask_api import status

from importer.utils.singleton import *

sys.path.append(".")
sys.path.append("..")

from importer.utils.singleton import *
from importer.product import Product
from importer.user import User

def create_app(test_config=None):
  # create and configure the app
  current_path = os.path.abspath(".")
  app = Flask(__name__, instance_path=current_path)
  app.config.from_mapping(
    SECRET_KEY='dev',
  )

  if test_config is None:
    config_path = "config.json"

    try:
      config_as_json = open(config_path, "r")
    except OSError as err:
      logging.error("Could not open or read file %s: %s" % (config_path, err))
      sys.exit()

    with config_as_json:
      config = json.load(config_as_json)
      app.config.update(config)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

  # returns a simple healthcheck
  @app.route('/healthcheck', methods=['GET'])
  def healthcheck():
    return "ok", status.HTTP_200_OK

  # insert a product
  @app.route('/product', methods=['POST'])
  def insert_product():
    data = request.get_json(silent=True)
    product = Product(data['producer'], data["product"])

    if not product.exists_in_database():
      product.insert_in_database()
      ret = jsonify("Product \"%s (ref: %s)\" successfully created" % (product.get_name(), product.get_ref())), status.HTTP_201_CREATED
    else:
      ret =  jsonify("Product \"%s (ref: %s)\" already exists in the database" % (product.get_name(), product.get_ref())), status.HTTP_409_CONFLICT

    return ret

  # insert a user
  @app.route('/user', methods=['POST'])
  def insert_user():
    data = request.get_json(silent=True)
    user = User(data["user"], data["group_name"])

    if not user.exists_in_database():
      user.insert_in_database()
      ret = jsonify("USer \"%s\" successfully created" % user.get_name()), status.HTTP_201_CREATED
    else:
      ret =  jsonify("User \"%s\" already exists in the database" % user.get_name()), status.HTTP_409_CONFLICT

    return ret

  return app
