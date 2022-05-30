

```

   ______                 __  __                   ____                           __           
  / ____/___ _____ ____  / /_/ /____              /  _/___ ___  ____  ____  _____/ /____  _____
 / /   / __ `/ __ `/ _ \/ __/ __/ _ \   ______    / // __ `__ \/ __ \/ __ \/ ___/ __/ _ \/ ___/
/ /___/ /_/ / /_/ /  __/ /_/ /_/  __/  /_____/  _/ // / / / / / /_/ / /_/ / /  / /_/  __/ /    
\____/\__,_/\__, /\___/\__/\__/\___/           /___/_/ /_/ /_/ .___/\____/_/   \__/\___/_/     
           /____/                                           /_/                                

```
# Overview

[cagette-importer 💻](https://github.com/gpenaud/cagette-importer) is a microservice, developped in python, which allows you to easily import cagette Products, manage its taxonomy (through deduction and insertion of its related TxpCategory, TxpSubcategory and TxpProduct). The goal of that microservice is to import exported products from currently [official cagette](https://app.cagette.net)

Usage of this microservice is difficult and requires some advanced skills, that's why its usage will no be free ; that will allow me to pay my bills, so if you prefer pay a few instead of importing all of your products manually, please contact me on my mail address: **guillaume.penaud@gmail.com** for more information.

## Requirements

* `curl` (HTTP client for api calls)
* `python` (Python 3.6 up to 3.10 supported)
* `pip` (Python package manager)
* `pipenv` (Python venv manager)
* `Docker`

## Installing

Please clone the repository

```
git clone https://github.com/gpenaud/cagette-importer.git
```

Go to the repository folder, then execute importer through `pipenv.

**Note**: The api will by default be available on http://127.0.0.1:5000

## Example

Start cagette-importer in development mode by running:

```
% FLASK_APP=importer FLASK_ENV=development pipenv run flask run

  * Serving Flask app 'importer' (lazy loading)
  * Environment: development
  * Debug mode: on
  * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
  * Restarting with stat
  * Debugger is active!
  * Debugger PIN: 137-663-782

```

Then you can query the api by using curl:

```
% curl http://127.0.0.1:5000/healthcheck
  ok
```
