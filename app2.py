from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timedelta

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')

database = client['nodejs']

collection = database['newone']

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    order = {
        'orderId': data['orderId'],
        'title': data['title'],
        'description': data['description'],
        'createdAt': datetime.now()
    }

    result = collection.insert_one(order)

    return {'inserted_document_id': str(result.inserted_id)}

@app.route('/orders', methods=['GET'])
def get_orders():
    seven_days_ago = datetime.now() - timedelta(days=7)

    query = {
        'createdAt': {'$gte': seven_days_ago}
    }

    orders = collection.find(query)

    response = []
    for order in orders:
        response.append({
            'orderId': order['orderId'],
            'title': order['title'],
            'description': order['description'],
            'createdAt': order['createdAt']
        })

    return jsonify(response)

if __name__ == '__main__':
    app.run()
