from flask import current_app

from pprint import pprint

import logging
import requests
import sys

from flaskr.utils.singleton import *

class Image:
  name       = None
  url        = None
  path = None

  def __init__(self, name, url):
    self.name = name.replace("'", "").replace(' ', '_').replace('/','_').replace("'", "").lower()
    self.url  = url

  def describe(self):
    """Describe the product object in a pretty way"""
    pprint(vars(self))

  def get_id(self):
    """Returns the image ID"""
    logging.debug('retrieving image_id from database')
    image_id = self.retrieve_id_from_database()

    if image_id is None:
      logging.debug('inserting image within the database')
      image_id = self.insert_in_database()

    return image_id

  def retrieve_id_from_database(self):
    """Retrieve the image ID from the database"""
    query = """SELECT id FROM File WHERE name = %s;"""

    cursor = get_connection().cursor()

    try:
      cursor.execute(query, (self.name,))
      row = cursor.fetchone()
    except mysql.connector.Error as err:
      logging.error("Something went wrong: {}".format(err))
      sys.exit()
    finally:
      cursor.close()

    if row is not None:
      logging.debug('image_id has been found in database')
      return row[0]
    else:
      logging.debug('no image_id found in database')
      return None

  def download_image_locally(self):
    """Download image on local host"""
    result = requests.get(self.url, stream = True)
    path = "%s/%s.png" % (current_app.config["images"]["path"], self.name)
    self.path = path

    if result.status_code == 200:
      logging.debug('image %s has been found on app.cagette.net, donwloading it locally' % path)
      open(path, "wb").write(result.content)

  def convert_to_binary(self):
    """Open image file and return its binary content"""
    try:
      file = open(self.path, 'rb')
    except OSError:
      logging.error("Could not open or read file %s: %s" % (file, err))
      sys.exit()

    with file:
      binary_data = file.read()
    return binary_data

  def insert_in_database(self):
    """Insert image in database"""
    self.download_image_locally()
    image_file = "%s.png" % self.name

    logging.debug('inserting image %s in database' % image_file)
    query="""INSERT INTO File (name, cdate, data) VALUES (%s, NOW(), %s)"""

    cursor = get_connection().cursor()

    try:
      cursor.execute(query, (image_file, self.convert_to_binary()))
      image_id = cursor.lastrowid
    except mysql.connector.Error as err:
      logging.error("Something went wrongwith query: %s" % err)
      sys.exit()
    finally:
      cursor.close()
      get_connection().commit()

    return image_id
