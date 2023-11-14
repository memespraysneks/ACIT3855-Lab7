import connexion
import json
import datetime
import yaml
import logging
import logging.config
from connexion import NoContent
from pykafka import KafkaClient


with open('app_conf.yml', 'r') as fs:
    app_config = yaml.safe_load(fs.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def item_creation(body):
    
    trace_id = str(datetime.datetime.now())
    body['trace_id'] = trace_id
    logger.info(f'Recieved event item-creation request with trace id {trace_id}')
    client = KafkaClient(hosts=f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}')
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    producer = topic.get_sync_producer()
    msg = {"type": "item_creation", "datetime" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "payload": body} 
    msg_str = json.dumps(msg) 
    producer.produce(msg_str.encode('utf-8'))
    
    
    # response = requests.post(url=app_config['eventstore1']['url'], json=body)
    logger.info(f'Returned event item-creation response (id: {trace_id})')
    return NoContent, 201

def trade(body):
    
    
    trace_id = str(datetime.datetime.now())
    body['trace_id'] = trace_id
    logger.info(f'Recieved event trade-item request with trace id {trace_id}')
    client = KafkaClient(hosts=f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}')
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    producer = topic.get_sync_producer()
    msg = {"type": "trade_item", "datetime" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "payload": body} 
    msg_str = json.dumps(msg) 
    producer.produce(msg_str.encode('utf-8'))
    # response = requests.post(url=app_config['eventstore2']['url'], json=body)
    logger.info(f'Returned event trade-item response (id: {trace_id})')
    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("CALEBSJSEEMAN-PathOfExileAPI-1.0.0-resolved.yaml", strict_validation = True, validate_responses = True)

if __name__ == "__main__":
    app.run(port=8080)