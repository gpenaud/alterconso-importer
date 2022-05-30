from flask import current_app

import mysql.connector

_connection = None

def get_connection():
  global _connection
  if not _connection:
    _connection = mysql.connector.connect(
      host        = current_app.config["mysql"]["host"],
      port        = current_app.config["mysql"]["port"],
      user        = current_app.config["mysql"]["user"],
      passwd      = current_app.config["mysql"]["passwd"],
      database    = current_app.config["mysql"]["database"],
      charset     = current_app.config["mysql"]["charset"],
      collation   = current_app.config["mysql"]["collation"],
      use_unicode = current_app.config["mysql"]["use_unicode"],
    )

  return _connection
