CUSTOMER_KEY = ""
CUSTOMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_SECRET = ""
DATA_DIR = "data"
NEO4J_IP = "localhost"
YCSB_LOGS_DIR = "ASRL-YCSB/scripts/logs"
TESTING_PLOT_DIR = "figures"

try:
	from private import *
except Exception:
	pass