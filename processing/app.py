import connexion
import json
import datetime
import yaml
import datetime
import logging
import logging.config
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS, cross_origin
# from base import Base
# from item_creation import CreateItem
# from trade_item import TradeItem


with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,'interval',seconds=app_config['scheduler']['period_sec'])
    sched.start()

def populate_stats():
    logger.info("Start Periodic Testing")
    try:
        with open(app_config["datastore"]["filename"], "r") as fs:
            json_object = json.load(fs)
        num_items_created = json_object['num_items_created']
        num_trades = json_object['num_trades']
        max_str = json_object['max_str']
        max_dex = json_object['max_dex']
        max_int = json_object['max_int']
        last_updated = json_object['last_updated']
    except:
        num_items_created = 0
        num_trades = 0
        max_str = 200
        max_dex = 180
        max_int = 250
        last_updated = "2016-08-29T09:12:33Z"
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    response_item_creations = requests.get(url=app_config['eventstore']['url1'], params={"start_timestamp": last_updated, "end_timestamp": current_timestamp})
    item_creations_string = response_item_creations.content.decode('utf-8')
    response_item_creations_list = json.loads(item_creations_string)
    if response_item_creations.status_code == 200:
        logger.info(f"Retrieved {len(response_item_creations_list)} item creations")
    else:
        logger.error(f"Failed to retrieve with error code ${response_item_creations.status_code}")
    response_trades = requests.get(url=app_config['eventstore']['url2'], params={"start_timestamp": last_updated, "end_timestamp": current_timestamp})
    trades_string = response_trades.content.decode('utf-8')
    response_trades_list = json.loads(trades_string)
    if response_item_creations.status_code == 200:
        logger.info(f"Retrieved {len(response_trades_list)} trades")
    else:
        logger.error(f"Failed to retrieve with error code {response_trades.status_code}")
    for item in response_item_creations_list:
        if item['item']['strength'] > max_str:
            max_str = item['item']['strength']
        if item['item']['dexterity'] > max_dex:
            max_dex = item['item']['dexterity']
        if item['item']['intelligence'] > max_int:
            max_int = item['item']['intelligence']
    for item in response_trades_list:
        if item['offer_item']['strength'] > max_str:
            max_str = item['offer_item']['strength']
        if item['trade_item']['strength'] > max_str:
            max_str = item['trade_item']['strength']
        if item['offer_item']['dexterity'] > max_dex:
            max_dex = item['offer_item']['dexterity']
        if item['trade_item']['dexterity'] > max_dex:
            max_dex = item['trade_item']['dexterity']
        if item['offer_item']['intelligence'] > max_int:
            max_dex = item['offer_item']['intelligence']
        if item['trade_item']['intelligence'] > max_int:
            max_dex = item['trade_item']['intelligence']
    num_items_created += len(response_item_creations_list)
    num_trades += len(response_trades_list)
    updated_stats = {"num_items_created": num_items_created, "num_trades": num_trades, "max_str": max_str, "max_dex": max_dex, "max_int": max_int, "last_updated": current_timestamp}
    with open(app_config["datastore"]["filename"], "w") as fs:
        json.dump(updated_stats, fs)
    logger.debug(f"Updated stats: num_items_created {num_items_created}, num_trades {num_trades}, max_str {max_str}, max_dex {max_dex}, max_int {max_int}")
    logger.info("Ending Periodic Testing")

def get_stats():
    logger.info("get_stats requests has started")
    try:
        with open(app_config["datastore"]["filename"], "r") as fs:
            json_object = json.load(fs)
        return_dict = {"num_items_created": json_object['num_items_created'], "num_trades": json_object['num_trades'], "max_str": json_object['max_str'], "max_dex": json_object['max_dex'], "max_int": json_object['max_int'], "last_updated": json_object['last_updated']}
        logger.debug(return_dict)
        logger.info("get_stats request completed")
        return return_dict, 200
    except:
        logger.error("No statistics currently exist")
        return "Statistics do not exist", 404

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("CALEBSJSEEMAN-PathOfExileAPI-1.0.0-resolved.yaml", strict_validation = True, validate_responses = True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100)