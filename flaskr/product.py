from pprint import pprint
import sys

sys.path.append(".")

from flaskr.image           import Image
from flaskr.taxonomy        import Taxonomy
from flaskr.utils.singleton import *
from flaskr.utils.tools     import *

class Product:
  producer       = None
  name           = None
  ref            = None
  price          = None
  vat            = None
  desc           = None
  stock          = None
  unit_type      = None
  qt             = None
  organic        = None
  variable_price = None
  multi_weight   = None
  wholesale      = None
  retail         = None
  bulk           = None
  has_float_qt   = None
  active         = None
  catalog_id     = None
  image_id       = None
  image_url      = None
  txp_product_id = None

  def __init__(self, producer, row):
    self.producer = producer
    self.name = row[1]
    self.ref = row[2]
    self.price = float(row[3])
    self.vat = float(row[4])
    self.desc = ''
    self.stock = float(10)
    self.unit_type = get_unit_type(row[7])
    self.qt = int(row[8])
    self.organic = float(1)
    self.variable_price = 0
    self.multi_weight = 0
    self.wholesale = 0
    self.retail = 0
    self.bulk = 0
    self.has_float_qt = 0
    self.active = cast_stringy_boolean(row[9])
    self.catalog_id = self.get_catalog_id()
    self.image_url = row[10]
    self.image_id = self.get_image_id()
    self.txp_product_id = self.get_txp_product_id()

  def describe(self):
    """Describe the product object in a pretty way"""
    pprint(vars(self))

  def get_name(self):
    """Returns the product name"""
    return self.name

  def get_catalog_id(self):
    """Returns the catalog id related to the product"""
    producer = self.producer.split("-", 1)[0]
    query="""SELECT id FROM Catalog WHERE LOWER(name) REGEXP '.*{producer}.*';""".format(producer = producer)

    cursor = get_connection().cursor()
    
    try:
      cursor.execute(query)
      row = cursor.fetchone()
    except mysql.connector.Error as err:
      logging.error("Something went wrong with query: %s" % err)
      sys.exit()
    finally:
      cursor.close()

    return row[0]

  def get_image_id(self):
    """Returns the product's image ID"""
    image = Image(self.name, self.image_url)
    return image.get_id()

  def get_txp_product_id(self):
    """Returns the product's TxpProduct ID"""
    txp = Taxonomy(self.name)
    return txp.get_txp_product_id()

  def insert_in_database(self):
    """Insert product in the database"""
    query = (
      """
      INSERT INTO Product
        (`name`,`ref`,`price`,`vat`,`desc`,`stock`,`unitType`,`qt`,`organic`,`variablePrice`,`multiWeight`,`wholesale`,`retail`,`bulk`,`hasFloatQt`,`active`,`catalogId`,`imageId`,`txpProductId`)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );
      """
    )

    cursor = get_connection().cursor()

    try:
      cursor.execute(query, (self.name, self.ref, self.price, self.vat, self.desc, self.stock, self.unit_type, self.qt, self.organic, self.variable_price, self.multi_weight, self.wholesale, self.retail, self.bulk, self.has_float_qt, self.active, self.catalog_id, self.image_id, self.txp_product_id))
    except mysql.connector.Error as err:
      logging.error("Something went wrong with query: %s" % err)
      sys.exit()
    finally:
      cursor.close()
      get_connection().commit()

    return self
