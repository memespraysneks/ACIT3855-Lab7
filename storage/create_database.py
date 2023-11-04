import sqlite3

conn = sqlite3.connect('POE.sqlite')

c = conn.cursor()
c.execute('''
            CREATE TABLE item_creation
            (id INTEGER PRIMARY KEY ASC, 
            user_id VARCHAR(250) NOT NULL,
            item_id VARCHAR(250) NOT NULL,
            strength INTEGER NOT NULL,
            dexterity INTEGER NOT NULL,
            intelligence INTEGER NOT NULL,
            timestamp VARCHAR(250) NOT NULL,
            date_created VARCHAR(250) NOT NULL,
            trace_id VARCHAR(250) NOT NULL)
        ''')

c.execute('''
            CREATE TABLE trade
            (id INTEGER PRIMARY KEY ASC,
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
            trace_id VARCHAR(250) NOT NULL)
        ''')

conn.commit()
conn.close()
