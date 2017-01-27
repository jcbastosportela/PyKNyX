# -*- coding: utf-8 -*-

from pyknyx.common import config

DEVICE_NAME = "alert"
DEVICE_IND_ADDR = "1.1.1"
DEVICE_VERSION = "0.1"

# Override default logger level
config.LOGGER_LEVEL = "info"

# Email settings
FROM = "pyknyx@localhost"  # From' header field
TO = "pyknyx@localhost"  # 'To' header field
SUBJECT = "PyKNyX alert"  # 'Subject' header field
SMTP = "localhost"  # SMTP server name

# Temperatures limits
TEMP_LIMITS = {"temp_1": [19., 24.],
               "temp_2": [5., 30.]
              }
