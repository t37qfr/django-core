'''
Start dajgno with remote CloudSql
runserver --settings=core.cloudsql
'''

import os
os.environ["CLOUD_SQL"] = '1'

from .settings import *