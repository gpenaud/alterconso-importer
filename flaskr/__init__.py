import json
import logging
import os
import sys

from flask import Flask, request, jsonify
from flask_api import status

from flaskr.utils.singleton import *

sys.path.append(".")
sys.path.append("..")

from flaskr.utils.singleton import *
from flaskr.product import Product

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

  @app.route('/test-config', methods=['GET'])
  def test_config():
    return "ok", status.HTTP_200_OK

  # a simple page that says hello
  @app.route('/product', methods=['POST'])
  def insert_product():
    data = request.get_json(silent=True)
    product = Product(data['producer'], data["product"])
    product.insert_in_database()
    return jsonify(product.get_name()), status.HTTP_201_CREATED

  return app
