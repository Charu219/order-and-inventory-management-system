import os

MYSQL_HOST = os.getenv("MYSQLHOST")
MYSQL_USER = os.getenv("MYSQLUSER")
MYSQL_PASSWORD = os.getenv("MYSQLPASSWORD")
MYSQL_DB = os.getenv("MYSQLDATABASE")
MYSQL_PORT = int(os.getenv("MYSQLPORT", 3306))

SECRET_KEY = os.getenv("SECRET_KEY", "secret123")





# MYSQL_HOST = 'shuttle.proxy.rlwy.net'
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = 'HKvodaHSZjqWsRZifHmrLqTixpzApjAx'
# MYSQL_DB = 'railway'
# MYSQL_PORT = 44877

# SECRET_KEY = 'secret123'





# import os

# MYSQL_HOST = os.getenv('MYSQLHOST')
# MYSQL_USER = os.getenv('MYSQLUSER')
# MYSQL_PASSWORD = os.getenv('MYSQLPASSWORD')
# MYSQL_DB = os.getenv('MYSQLDATABASE')
# MYSQL_PORT = int(os.getenv('MYSQLPORT', 3306))

# SECRET_KEY = 'secret123'

# import os

# MYSQL_HOST = os.getenv('MYSQLHOST', 'localhost')
# MYSQL_USER = os.getenv('MYSQLUSER', 'root')
# MYSQL_PASSWORD = os.getenv('MYSQLPASSWORD', '')
# MYSQL_DB = os.getenv('MYSQLDATABASE', 'inventory_db')
# MYSQL_PORT = int(os.getenv('MYSQLPORT', 3306))

# SECRET_KEY = 'secret123'



# MYSQL_HOST = 'localhost'
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = 'Charu@060905'
# MYSQL_DB = 'inventory_db'
# SECRET_KEY = 'secret123'
