from flask import Flask, jsonify
from elasticsearch import Elasticsearch, NotFoundError, ConnectionError

app = Flask(__name__)

el = Elasticsearch(hosts='http://elastic:9200')


@app.route('/show')
def show():
    try:
        hits = el.search(index='my-index', filter_path=['hits.hits._source']).body.get('hits', {}).get('hits', [])
    except (NotFoundError, ConnectionError):
        return jsonify(data=[])
    hits = [hit['_source'] for hit in hits]
    return jsonify(data=hits)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, threaded=True)
