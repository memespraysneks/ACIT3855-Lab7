import mysql.connector
db_conn = mysql.connector.connect(host="caleblab6a3855.eastus2.cloudapp.azure.com", user="root", password="FuckMysql123!", database="events")
db_cursor = db_conn.cursor()
db_cursor.execute('''
    DROP TABLE item_creation, trade_item
    ''')
db_conn.commit()
db_conn.close()