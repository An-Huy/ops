import os 
from configobj import ConfigObj

exist = True 

if exist:
	CONF_FILE = os.path.abspath(os.path.join(
				os.path.dirname(os.path.abspath(__file__)),
				"../../etc/config.ini"))
else:
	CONF_FILE = '/opt/config/default.conf'

def load_config():
	config = ConfigObj(CONF_FILE, list_values=True)
	return config

CONF = load_config()