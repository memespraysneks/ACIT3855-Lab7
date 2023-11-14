import mysql.connector
db_conn = mysql.connector.connect(host="caleblab6a3855.eastus2.cloudapp.azure.com", user="root", password="FuckMysql123!", database="events")
db_cursor = db_conn.cursor()
db_cursor.execute('''
    CREATE TABLE item_creation
    (id INT NOT NULL AUTO_INCREMENT, 
    user_id VARCHAR(250) NOT NULL,
    item_id VARCHAR(250) NOT NULL,
    strength INTEGER NOT NULL,
    dexterity INTEGER NOT NULL,
    intelligence INTEGER NOT NULL,
    timestamp VARCHAR(250) NOT NULL,
    date_created VARCHAR(250) NOT NULL,
    trace_id VARCHAR(250) NOT NULL,
    CONSTRAINT item_creation_pk PRIMARY KEY (id))
    ''')

db_cursor.execute('''
    CREATE TABLE trade_item
    (id INT NOT NULL AUTO_INCREMENT, 
    trade_id VARCHAR(250) NOT NULL,
    initial_user_id VARCHAR(250) NOT NULL,
    secondary_user_id VARCHAR(250) NOT NULL,
    offer_item_id VARCHAR(250) NOT NULL,
    offer_item_strength INTEGER NOT NULL,
    offer_item_dexterity INTEGER NOT NULL,
    offer_item_intelligence INTEGER NOT NULL,
    trade_item_id VARCHAR(250) NOT NULL,
    trade_item_strength INTEGER NOT NULL,
    trade_item_dexterity INTEGER NOT NULL,
    trade_item_intelligence INTEGER NOT NULL,
    timestamp VARCHAR(250) NOT NULL,
    date_created VARCHAR(250) NOT NULL,
    trace_id VARCHAR(250) NOT NULL,
    CONSTRAINT trade_item_pk PRIMARY KEY (id))
    ''')
db_conn.commit()
db_conn.close()