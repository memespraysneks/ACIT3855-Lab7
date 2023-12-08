import connexion
import json
import datetime
import yaml
import datetime
import logging
import logging.config
import requests
import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS, cross_origin

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

with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(check_health,'interval',seconds=app_config['scheduler']['period_sec'])
    sched.start()

def check_health():

    logger.info("starting health check.")
    logger.info("checking reciever health")
    reciever_health = requests.get(url=app_config["eventstore"]["reciever"], timeout = 5)
    logger.info("checking storage health")
    storage_health = requests.get(url=app_config["eventstore"]["storage"], timeout = 5)
    logger.info("checking processing health")
    processing_health = requests.get(url=app_config["eventstore"]["processing"], timeout = 5)
    logger.info("checking audit health")
    audit_health = requests.get(url=app_config["eventstore"]["audit"], timeout = 5)

    reciever_health_string = reciever_health.content.decode('utf-8')
    reciever_health_list = json.loads(reciever_health_string)

    storage_health_string = storage_health.content.decode('utf-8')
    storage_health_list = json.loads(storage_health_string)

    processing_health_string = processing_health.content.decode('utf-8')
    processing_health_list = json.loads(processing_health_string)

    audit_health_string = audit_health.content.decode('utf-8')
    audit_health_list = json.loads(audit_health_string)

    current_timestamp = datetime.datetime.now()

    health_stats = {"reciever": "unhealthy", "storage": "unhealthy", "processing": "unhealthy", "audit": "unhealthy", "current_time": str(current_timestamp)}

    if reciever_health.status_code == 200:
        logger.info("reciever is healthy")
        health_stats["reciever"] = "healthy"
    
    if storage_health.status_code == 200:
        logger.info("storage is healthy")
        health_stats["storage"] = "healthy"
    
    if processing_health.status_code == 200:
        logger.info("processing is healthy")
        health_stats["processing"] = "healthy"

    if audit_health.status_code == 200:
        logger.info("audit is healthy")
        health_stats["audit"] = "healthy"
    
    

    with open(app_config["datastore"]["filename"], "w") as fs:
        json.dump(health_stats, fs)

def get_health():
    logger.info("received health check request")
    try:
        with open(app_config["datastore"]["filename"], "r") as fs:
            data = json.load(fs)

        return data, 200
    except:
        return {"message": "Health is not loaded yet"}, 400

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yml", strict_validation = True, validate_responses = True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8120)


