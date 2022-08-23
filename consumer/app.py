import signal
from threading import Event
from datetime import datetime

from flask import Flask
from flask_kafka import FlaskKafka
from elasticsearch import Elasticsearch

app = Flask(__name__)

INTERRUPT_EVENT = Event()

bus = FlaskKafka(INTERRUPT_EVENT,
                 bootstrap_servers=",".join(["kafka:9092"]),
                 group_id="consumer-grp-1"
                 )

el = Elasticsearch(hosts=['http://elastic:9200'])


def listen_kill_server():
    signal.signal(signal.SIGTERM, bus.interrupted_process)
    signal.signal(signal.SIGINT, bus.interrupted_process)
    signal.signal(signal.SIGQUIT, bus.interrupted_process)
    signal.signal(signal.SIGHUP, bus.interrupted_process)


@bus.handle('my-topic')
def test_topic_handler(msg):
    document = {'message': msg.value.decode('utf-8'),
                'timestamp': datetime.fromtimestamp(msg.timestamp / 1000)}
    el.index(index='my-index', document=document)


if __name__ == '__main__':
    bus.run()
    listen_kill_server()
    app.run(debug=True, port=5004)
