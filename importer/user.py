import hashlib
import logging
from pprint import pprint
import sys

sys.path.append(".")

from importer.utils.singleton import *
from importer.utils.tools     import *

class User:
  lang               = None
  password           = None
  rights             = None
  firstName          = None
  lastName           = None
  email              = None
  phone	             = None
  firstName2         = None
  lastName2          = None
  email2             = None
  phone2             = None
  address1           = None
  address2           = None
  zipCode            = None
  city               = None
  birthDate          = None
  nationality        = None
  countryOfResidence = None
  cdate	             = None
  ldate              = None
  flags              = None
  tos                = None
  tutoState          = None
  apiKey             = None
  group_name         = None

  def __init__(self, row, group_name):
    self.lang               = "fr"
    self.rights             = ""
    self.firstName          = row[1]
    self.lastName           = row[2]
    self.password           = self.generate_password()
    self.email              = row[9]
    self.phone	            = row[10]
    self.firstName2         = cast_string_as_none(row[3])
    self.lastName2          = cast_string_as_none(row[4])
    self.email2             = cast_string_as_none(row[11])
    self.phone2             = cast_string_as_none(row[12])
    self.address1           = row[7]
    self.address2           = cast_string_as_none(row[8])
    self.zipCode            = row[6]
    self.city               = row[5]
    self.birthDate          = ""
    self.nationality        = "FR"
    self.countryOfResidence = "FR"
    self.cdate	            = ""
    self.ldate              = ""
    self.flags              = "4"
    self.tos                = ""
    self.tutoState          = cast_string_as_none("")
    self.apiKey             = cast_string_as_none("")
    self.group_name         = group_name

  def describe(self):
    """Describe the user object in a pretty way"""
    pprint(vars(self))

  def get_name(self):
    """Returns the user name"""
    return "%s %s" % (self.firstName, self.lastName)

  def get_group_id(self, group_name):
    """Returns the current group id"""
    query="""SELECT id FROM `Group` WHERE LOWER(name) REGEXP '.*%s.*'""" % group_name
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

  def generate_password(self):
    """Returns a password for user"""
    password = "%s%s%s" % ("localdevkey", self.firstName.replace(" ", "").lower(), self.lastName.replace(" ", "").lower())
    return hashlib.md5(password.encode('utf-8')).hexdigest()

  def exists_in_database(self):
    """Checks if such a user already exists in database"""
    exists = False
    query="""SELECT id FROM User WHERE firstName = '{firstName}' AND lastName = '{lastName}' AND email = '{email}'""".format(
      firstName = self.firstName,
      lastName  = self.lastName,
      email     = self.email
    )
    cursor = get_connection().cursor()

    try:
      cursor.execute(query)
      row = cursor.fetchone()
    except mysql.connector.Error as err:
      logging.error("Something went wrong with query: %s" % err)
      sys.exit()
    finally:
      cursor.close()

    if row is not None:
      exists = True

    return exists

  def insert_in_database(self):
    """Insert User in the database"""
    query = (
      """
      INSERT INTO User
        (`lang`,`pass`,`rights`,`firstName`,`lastName`,`email`,`phone`,`firstName2`,`lastName2`,`email2`,`phone2`,`address1`,`address2`,`zipCode`,`city`,`birthDate`,`nationality`,`countryOfResidence`,`cdate`, `ldate`, `flags`, `tos`, `tutoState`, `apiKey`)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
      """
    )

    cursor = get_connection().cursor()

    try:
      cursor.execute(query, (
        self.lang,
        self.password,
        self.rights,
        self.firstName,
        self.lastName,
        self.email,
        self.phone,
        self.firstName2,
        self.lastName2,
        self.email2,
        self.phone2,
        self.address1,
        self.address2,
        self.zipCode,
        self.city,
        self.birthDate,
        self.nationality,
        self.countryOfResidence,
        self.cdate,
        self.ldate,
        self.flags,
        self.tos,
        self.tutoState,
        self.apiKey,
      ))

      self.insert_user_group(self.get_group_id(self.group_name), cursor.lastrowid)
    except mysql.connector.Error as err:
      logging.error("Something went wrong with query: %s" % err)
      sys.exit()
    finally:
      cursor.close()
      get_connection().commit()

    return self

  def insert_user_group(self, group_id, user_id):
    """Insert User group membership in the database"""
    query = (
      """
      INSERT INTO UserGroup
        (`rights`,`rights2`,`balance`,`groupId`,`userId`)
      VALUES (%s, %s, %s, %s, %s);
      """
    )

    cursor = get_connection().cursor()

    print(group_id)
    print(user_id)

    try:
      cursor.execute(query, (None, None, 0, group_id, user_id))
    except mysql.connector.Error as err:
      logging.error("Something went wrong with query: %s" % err)
      sys.exit()
    finally:
      cursor.close()
      get_connection().commit()
