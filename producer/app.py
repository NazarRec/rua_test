from flask import Flask, jsonify
from kafka import KafkaProducer
import re

app = Flask(__name__)

producer = KafkaProducer(bootstrap_servers=['kafka:9092'])


@app.route('/insert/<string:message>')
def insert(message):
    if re.match(r'^[\dA-z]{1,20}$', message):
        producer.send('my-topic', message.encode())
        return jsonify(success=True), 201
    return jsonify(success=False, error='Validation error'), 422


if __name__ == '__main__':
    app.run('0.0.0.0', threaded=True)
