import os
DEBUG = True
DIRNAME = os.path.dirname(__file__)
STATIC_PATH = os.path.join(DIRNAME, 'static')
TEMPLATE_PATH = os.path.join(DIRNAME, 'template')
ADMIN_ID="0"
ADMIN_NM="dbm"
ADMIN_PW="fullscore"
MYSQL_HOST="localhost"
MYSQL_USER="movielover"
MYSQL_PW="lovemovie"
MYSQL_DB="movielover"

import logging
import sys
#log linked to the standard error stream
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)-8s - %(message)s',
                    datefmt='%d/%m/%Y %Hh%Mm%Ss')
console = logging.StreamHandler(sys.stderr)

COOKIE_SECRET = 'WErm97e4RLqkfaB41qhDqbWykV4pjEB4gVGzinkZWKY='