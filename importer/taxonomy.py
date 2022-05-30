from flask import current_app
from pprint import pprint

import logging
import re
import yaml

from importer.utils.singleton import *

class Taxonomy:
  txp_data = None
  product = None

  def __init__(self, product):
    try:
      file = open(current_app.config["taxonomy"]["path"], "r")
    except OSError as err:
      logging.error("Could not open or read file %s: %s" % (current_app.config["taxonomy"]["path"], err))
      sys.exit()

    with file:
      self.txp_data = yaml.safe_load(file)

    self.product = product
    return None

  def describe(self):
    """Describe the taxonomy object in a pretty way"""
    pprint(vars(self))

  def search_subcategory(self, d, value, default=None):
    """Search recursively a TxpSubCategory from list of value"""
    for k, v in d.items():
      v = [s.lower() for s in v]
      for product_type in v:
        if re.search(product_type, value.lower()):
          return k

  def get_txp_category_id(self):
    """Return the TxpCategory ID of the current product"""
    txp_subcategory_name = self.search_subcategory(self.txp_data, self.product)
    query="""SELECT categoryId FROM TxpSubCategory WHERE name = %s;"""

    cursor = get_connection().cursor()

    try:
      cursor.execute(query, (txp_subcategory_name,))
      row = cursor.fetchone()
    except mysql.connector.Error as err:
      logging.error("Something went wrong with query: %s" % err)
      sys.exit()
    finally:
      cursor.close()

    return row[0]

  def get_txp_subcategory_id(self):
    """Return the TxpSubCategory ID of the current product"""
    txp_subcategory_name = self.search_subcategory(self.txp_data, self.product)
    query="""SELECT id FROM TxpSubCategory WHERE name = %s;"""

    cursor = get_connection().cursor()

    try:
      cursor.execute(query, (txp_subcategory_name,))
      row = cursor.fetchone()
    except mysql.connector.Error as err:
      logging.error("Something went wrong with query: %s" % err)
      sys.exit()
    finally:
      cursor.close()

    return row[0]

  def get_txp_product_id(self):
    """Return the TxpProduct ID of the current product"""
    query="""SELECT id FROM TxpProduct WHERE name = %s LIMIT 1;"""

    cursor = get_connection().cursor()

    try:
      cursor.execute(query, (self.product,))
      row = cursor.fetchone()
    except mysql.connector.Error as err:
      logging.error("Something went wrong with query: %s" % err)
      sys.exit()
    finally:
      cursor.close()

    if row is not None:
      txp_product_id = row[0]
    else:
      txp_product_id = self.insert_txp_product_id()

    return txp_product_id

  def insert_txp_product_id(self):
    """Insert the TxpProduct in database"""
    query="""INSERT INTO TxpProduct (name, categoryId, subCategoryId) VALUES (%s, %s, %s)"""

    cursor = get_connection().cursor()

    try:
      cursor.execute(query, (self.product, self.get_txp_category_id(), self.get_txp_subcategory_id()))
      txp_product_id = cursor.lastrowid
    except mysql.connector.Error as err:
      logging.error("Something went wrong with query: %s" % err)
      sys.exit()
    finally:
      cursor.close()
      get_connection().commit()

    return txp_product_id
