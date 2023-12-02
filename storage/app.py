import connexion
import json
import datetime
import pymysql
import time
import yaml
import datetime
import logging
import logging.config
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from item_creation import CreateItem
from trade_item import TradeItem
from connexion import NoContent
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
from sqlalchemy import and_

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())




DB_ENGINE = create_engine(f'mysql+pymysql://{app_config["datastore"]["user"]}:{app_config["datastore"]["password"]}@{app_config["datastore"]["hostname"]}:{app_config["datastore"]["port"]}/{app_config["datastore"]["db"]}')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)
# def item_creation(body):
#     """ Creates a new item """
#     logger.info(f'Connecting to DB. Hostname:{app_config["datastore"]["hostname"]}, Port:{app_config["datastore"]["port"]}')
#     session = DB_SESSION()

#     item_creation = CreateItem(body['user_id'],
#                        body['item']['item_id'],
#                        body['item']['strength'],
#                        body['item']['dexterity'],
#                        body['item']['intelligence'],
#                        body['timestamp'],
#                        body['trace_id'])

#     session.add(item_creation)

#     session.commit()
#     session.close()

#     logger.debug(f"Stored event item_creation request with a trace id of {body['trace_id']}")

#     return NoContent, 201

# def trade(body):
#     """ Trades an Item """
#     logger.info(f'Connecting to DB. Hostname:{app_config["datastore"]["hostname"]}, Port:{app_config["datastore"]["port"]}')
#     session = DB_SESSION()
    
#     trade_item = TradeItem(body['trade_id'],
#                    body['initial_user_id'],
#                    body['secondary_user_id'],
#                    body['offer_item']['item_id'],
#                    body['offer_item']['strength'],
#                    body['offer_item']['dexterity'],
#                    body['offer_item']['intelligence'],
#                    body['trade_item']['item_id'],
#                    body['trade_item']['strength'],
#                    body['trade_item']['dexterity'],
#                    body['trade_item']['intelligence'],
#                    body['timestamp'],
#                    body['trace_id'])

#     session.add(trade_item)

#     session.commit()
#     session.close()

#     logger.debug(f"Stored event trade_item request with a trace id of {body['trace_id']}")

#     return NoContent, 201

def get_item_creations(start_timestamp, end_timestamp):
    """ Gets new item creations after the timestamp """
    session = DB_SESSION()
    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%S")
    readings = session.query(CreateItem).filter(and_(CreateItem.date_created >= start_timestamp_datetime, CreateItem.date_created < end_timestamp_datetime))
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for Item Creations after %s returns %d results" % (start_timestamp, len(results_list)))
    return results_list, 200

def get_trades(start_timestamp, end_timestamp):
    """ Gets new trades after the timestamp """
    session = DB_SESSION()
    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%S")
    readings = session.query(TradeItem).filter(and_(TradeItem.date_created >= start_timestamp_datetime, TradeItem.date_created < end_timestamp_datetime))
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for Trades after %s returns %d results" % (start_timestamp, len(results_list)))
    return results_list, 200

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("CALEBSJSEEMAN-PathOfExileAPI-1.0.0-resolved.yaml", strict_validation = True, validate_responses = True)

def process_messages():
    hostname = "%s:%d" % (app_config["events"]["hostname"],app_config["events"]["port"])
    current_retry = 0
    while current_retry <= app_config["datastore"]["max_retries"]:
        try:
            client = KafkaClient(hosts=hostname)
            topic = client.topics[str.encode(app_config["events"]["topic"])]
        except:
            logger.error("Connecting to Kafka Client has failed trying again")
            time.sleep(app_config["datastore"]["sleep_time"])

        current_retry += 1
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',reset_offset_on_start=False,auto_offset_reset=OffsetType.LATEST)
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]

        session = DB_SESSION()
        if msg["type"] == "item_creation":
            item_creation = CreateItem(payload['user_id'],
                       payload['item']['item_id'],
                       payload['item']['strength'],
                       payload['item']['dexterity'],
                       payload['item']['intelligence'],
                       payload['timestamp'],
                       payload['trace_id'])
            session.add(item_creation)
            session.commit()
            session.close()
            logger.debug(f"Stored event item_creation request with a trace id of {payload['trace_id']}")
        elif msg["type"] == "trade_item":
            trade_item = TradeItem(payload['trade_id'],
                   payload['initial_user_id'],
                   payload['secondary_user_id'],
                   payload['offer_item']['item_id'],
                   payload['offer_item']['strength'],
                   payload['offer_item']['dexterity'],
                   payload['offer_item']['intelligence'],
                   payload['trade_item']['item_id'],
                   payload['trade_item']['strength'],
                   payload['trade_item']['dexterity'],
                   payload['trade_item']['intelligence'],
                   payload['timestamp'],
                   payload['trace_id'])
            session.add(trade_item)

            session.commit()
            session.close()

            logger.debug(f"Stored event trade_item request with a trace id of {payload['trace_id']}")
        consumer.commit_offsets()

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)