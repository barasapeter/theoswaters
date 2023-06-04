# Import MySQL connector
import mysql.connector
import quick_variables

# Connect to MySQL server
cnx = mysql.connector.connect(
    host='localhost',
    user='root', # Replace this with your username
    password='quantumsoft' # Replace this with your password
)

# Create a cursor object to execute queries
cursor = cnx.cursor()

# Create the 'TheosWaters' database
cursor.execute('CREATE DATABASE IF NOT EXISTS TheosWaters')
cursor.execute('USE TheosWaters')

def login_success(username, password):
    '''Authenticate username and password'''
    create_table_query = '''CREATE TABLE IF NOT EXISTS `merchants` (username VARCHAR(200) PRIMARY KEY, password VARCHAR(100));'''
    cursor.execute(create_table_query)
    cnx.commit()
    authenticator_query = f'SELECT * FROM merchants WHERE username = "{username}" AND password = "{password}"'
    cursor.execute(authenticator_query)
    if cursor.fetchone():
        return True
    return False

def fetch_customers(merchant_username) -> list:
    '''Fetch the customers details and return a list of tuples of each table database row'''
    create_table_query = f'''CREATE TABLE IF NOT EXISTS {merchant_username}_customers (`Serial NO` INT AUTO_INCREMENT PRIMARY KEY, `Full name` VARCHAR(50), `Address` VARCHAR(100), `Contact NO` VARCHAR(20), `Date Encoded` DATE);'''
    cursor.execute(create_table_query)
    cnx.commit()
    fetch_customers_query = f'SELECT * FROM {merchant_username}_customers'
    cursor.execute(fetch_customers_query)
    return cursor.fetchall()

def fetch_bottles(merchant_username):
    '''Fetches bottles of a merchat'''
    create_table_query = f'''CREATE TABLE IF NOT EXISTS {merchant_username}_bottles (`NO` INT AUTO_INCREMENT PRIMARY KEY, `Bottle size` INT, `Measurement unit` VARCHAR(100), `Cost` DECIMAL(10, 2));'''
    cursor.execute(create_table_query)
    fetch_bottles_query = f'SELECT * FROM {merchant_username}_bottles'
    cursor.execute(fetch_bottles_query)
    return cursor.fetchall()

def add_bottle(merchant_username, serial_number: str, bottle_size: str, measurement_unit, cost: str):
    '''Add new bottle to the database'''
    # Check if the bottles table for the logged in user exists
    create_table_query = f'''CREATE TABLE IF NOT EXISTS {merchant_username}_bottles (`NO` INT AUTO_INCREMENT PRIMARY KEY, `Bottle size` INT, `Measurement unit` VARCHAR(100), `Cost` DECIMAL(10, 2));'''
    cursor.execute(create_table_query)
    cnx.commit()
    try:
        if serial_number:
            insert_query = f'INSERT INTO {merchant_username}_bottles VALUES ("{serial_number}", "{bottle_size}", "{measurement_unit}", "{cost}")'
        else:
            insert_query = f'INSERT INTO {merchant_username}_bottles (`Bottle size`, `Measurement unit`, `Cost`) VALUES ("{bottle_size}", "{measurement_unit}", "{cost}")'
        try:
            cursor.execute(insert_query)
            return 'Record has been added successfully!'
        except mysql.connector.errors.IntegrityError:
            return f'The serial number "{serial_number}" already exists. Please enter another one. Use auto Increment instead? Leave the SN entry blank to use auto increment.'
    except mysql.connector.errors.DatabaseError:
        return 'You have entered an invalid data type(s). Use numbers for "Serial NO", "Bottle size" and "Cost"'

def delete_bottle(merchant_username, bottle_serial_number):
    delete_query = F'DELETE FROM {merchant_username}_bottles WHERE `NO` = {bottle_serial_number}'
    try:
        cursor.execute(delete_query)
        return f'Record {bottle_serial_number} has been deleted successfully'
    except mysql.connector.errors.ProgrammingError:
        return f'Record deletion failed! We cannot find record "{bottle_serial_number}" anywhere in your database'

def dispense(merchant_username, bottle_serial_number, cost):
    '''Record dispense data'''
    fetch_bottle_query = f'SELECT * FROM {merchant_username}_bottles WHERE `NO` = "{bottle_serial_number}"'
    cursor.execute(fetch_bottle_query)
    
    results = []
    for i in cursor.fetchall():
        results.append(i)
    
    try:
        float(cost)
    except:
        return 'Failed! Please enter a numeric value for cost'
    
    if results:
        date_today = quick_variables.CustomCalendar.date_today()
        day_today = quick_variables.CustomCalendar.day_name_today()
        time_now = quick_variables.CustomCalendar.time_now()
        create_stats_table_query = f'''CREATE TABLE IF NOT EXISTS {merchant_username}_sales (`Sale number` INT AUTO_INCREMENT PRIMARY KEY, `Bottle Description` VARCHAR(50), `Cost` DECIMAL(10, 2), `Date of transaction` DATE, `Day` VARCHAR(20), `Time` VARCHAR(20))'''
        create_stats_query = f'''INSERT INTO {merchant_username}_sales (`Bottle Description`, `Cost`, `Date of transaction`, `Day`, `Time`) VALUES ("{results[0][1]} {results[0][2]}", {cost}, "{date_today}", "{day_today}", "{time_now}")'''
        cursor.execute(create_stats_table_query), cursor.execute(create_stats_query)
        return f'This will dispense {results[0][1]} {results[0][2]} of water. Would you like to proceed?'
    
    return f'We could not find bottle with serial "{bottle_serial_number}" anywhere in your database'

def fetch_sales(merchant_username):
    '''Fetch sales stats'''
    create_stats_table_query = f'''CREATE TABLE IF NOT EXISTS {merchant_username}_sales (`Sale number` INT AUTO_INCREMENT PRIMARY KEY, `Bottle Description` VARCHAR(50), `Cost` DECIMAL(10, 2), `Date of transaction` DATE, `Day` VARCHAR(20), `Time` VARCHAR(20))'''
    cursor.execute(create_stats_table_query)
    cnx.commit()
    fetch_sales_stats_query = f'SELECT * FROM {merchant_username}_sales'
    cursor.execute(fetch_sales_stats_query)
    return cursor.fetchall()

# For tsting purposes
if __name__ =='__main__':
    print(dispense('abigail_thompson', 'b3', '80'))
    cnx.commit(),
    cnx.close()
