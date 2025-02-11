from flask import Flask, request, jsonify
from pymongo import MongoClient
import re
from bson.objectid import ObjectId


app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['eshop']
clients_collection = db['clients']
products_collection = db['products']



def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email) is not None

def rewrite(object, tipas, avoid=''):
    
    if tipas==True: 
        perrasytas = {"id": str(object['_id'])}
        
        for key in object: 
            if key!="_id" and key!=avoid: 
                perrasytas[key]=object[key]
                
    else: 
        if 'id' in object and object['id']: 
            id = str(object['id'])
        else:
            id = str(ObjectId())
            
        perrasytas = {"_id": id }
        
        for key in object: 
            if key!="id" and key!=avoid:
                perrasytas[key]=object[key]
    return perrasytas

@app.route('/clients', methods=['PUT'])
def register_new_client():
        data = request.get_json()

        if 'name' not in data or 'email' not in data:
            return jsonify({"error": "Trūksta vardo arba pašto adreso"}), 400

        if not is_valid_email(data['email']):
            return jsonify({"error": "Neteisingai įvestas pašto adresas"}), 400

        if clients_collection.find_one({'email':data['email']}):
            return jsonify({'error': 'Klaida. El. paštas jau naudojamas kito kliento.'}), 400
        
        if 'id' in data:
            if clients_collection.find_one({'_id': data['id']}):
                return jsonify({'error': 'Klaida. Klientas tokiu ID jau egzistuoja.'}), 400

        new_client = rewrite(data, 0)
        clients_collection.insert_one(new_client)
        return jsonify({'id': str(new_client['_id'])}), 201

@app.route('/clients/<clientId>', methods=['GET'])
def get_client(clientId):
    client = clients_collection.find_one({"_id": clientId})
    if not client:
        return jsonify({'error': 'Klaida. Klientas tokiu ID neegzistuoja.'}), 404
    else:
        client_1 = rewrite(client, 1, 'orders')
        return jsonify(client_1), 200

@app.route('/clients/<clientId>', methods=['DELETE'])
def delete_client(clientId):

    client_data = clients_collection.find_one({'_id': clientId})
    if not client_data:
        return jsonify({'error': 'Klaida. Klientas tokiu ID neegzistuoja.'}), 404

    client_delete_result = clients_collection.delete_one({'_id': clientId})
    if client_delete_result.deleted_count != 1:
        return jsonify({"error": "Kliento ištrinti nepavyko"}), 500
        
    return '', 204

@app.route('/products', methods=['PUT'])
def register_product():
    data = request.get_json()

    if 'name' not in data or 'price' not in data:
        return jsonify({"error": "Trūksta vardo arba kainos"}), 400

    if not isinstance(data['price'], (int, float)):
        return jsonify({"error": "Kaina turi būti skaičius"}), 400
    
    if 'id' in data:
        if products_collection.find_one({'_id': data['id']}):
            return jsonify({'error': 'Klaida. Produktas tokiu ID jau egzistuoja.'}), 400
    
    new_product = rewrite(data,0)
    products_collection.insert_one(new_product)
    return jsonify({"id":new_product['_id']}), 201

@app.route('/products', methods=['GET'])
def get_products_by_category():
    
    category = request.args.get('category')

    if category:
        products = list(products_collection.find({"category": category}))
    else:
        products = list(products_collection.find())

    if len(products)==0:
        return '', 204
    
    productsList = []
    for product in products:
        product_1 = rewrite(product,1)
        productsList.append(product_1)
    
    return jsonify(productsList), 200

@app.route('/products/<string:product_id>', methods=['GET'])
def get_product(product_id):
    
    product = products_collection.find_one({"_id": product_id})

    if not product:
        return jsonify({'error': 'Produktas tokiu ID neegzistuoja.'}), 404
    else:
        product_1 = rewrite(product, 1)
        return jsonify(product_1), 200

@app.route('/products/<string:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = products_collection.find_one({'_id': product_id})
    if not product:
        return jsonify({'error': 'Produktas tokiu ID neegzistuoja.'}), 404
    else:
        products_collection.delete_one(product)
        return '', 204
    
@app.route('/orders', methods=['PUT'])
def place_order():
    data = request.get_json()
    
    if 'clientId' not in data or 'items' not in data or not data['items']:
        return jsonify({'error':'Klaida. Nenurodytas kliento ID arba užsakymo prekės.'}), 400

    client = clients_collection.find_one({"_id":data['clientId']})
    
    if not client:
        return jsonify({'error':'Klientas tokiu ID neegzistuoja.'}), 404
    
    for item in data['items']:
        if 'productId' not in item or 'quantity' not in item or not item['quantity']:
            return jsonify({'message': 'Klaida. Nenurodytas produkto ID arba kiekis'}), 400
         
        product = products_collection.find_one({'_id': item['productId']})
        if not product:
            return jsonify({'error': f"Produktas su ID {item['productId']} neegzistuoja."}), 404
        
    new_order = rewrite(data, 0)
        
    clients_collection.update_one(
        {"_id": data['clientId']},
        {"$push": {"orders": new_order}} 
    )
    
    return jsonify({"id":new_order['_id']}), 201

@app.route('/clients/<string:clientId>/orders', methods=['GET'])
def get_client_orders(clientId):

    client = clients_collection.find_one({"_id": clientId})
    
    if not client:
        return jsonify({'error':'Klientas tokiu ID neegzistuoja.'}), 404

    orders = client.get('orders', [])
    
    if len(orders)==0:
        return jsonify({'message': 'Šis klientas nėra pateikęs nei vieno užsakymo.'}), 200
    
    order_list = []
    for order in orders:
        order = rewrite(order, 1, 'clientId')
        order_list.append(order)
    
    return jsonify(order_list), 200

@app.route('/statistics/top/clients', methods=['GET'])
def get_top_clients():
    pipeline = [
        {
            "$project": {
                "_id": 0,
                "id": "$_id",  
                "name": "$name",  
                "totalOrders": {"$size": {"$ifNull": ["$orders", []]}}  
            }
        },
        {
            "$sort": {"totalOrders": -1}  
        },
        {
            "$limit": 10 
        }
    ]
    top_clients = list(clients_collection.aggregate(pipeline))
    return jsonify(top_clients), 200

@app.route('/statistics/top/products', methods=['GET'])
def get_top_products():
    pipeline = [
    {
        "$unwind": "$orders"  
    },
    {
        "$unwind": "$orders.items" 
    },
    {
        "$group": {
            "_id": "$orders.items.productId",  
            "quantity": {"$sum": "$orders.items.quantity"} 
        }
    },
    {
        "$lookup": {
            "from": "products",  
            "localField": "_id", 
            "foreignField": "_id",
            "as": "product_info"
        }
    },
    {
        "$unwind": "$product_info"  
    },
    {
        "$project": {
            "_id": 0,
            "productId": "$product_info._id", 
            "name": "$product_info.name",  
            "quantity": 1
        }
    },
    {
        "$sort": {"quantity": -1}  
    },
    {
        "$limit": 10  
    }
    ]
    
    top_products = list(clients_collection.aggregate(pipeline))
    return jsonify(top_products), 200

@app.route('/statistics/orders/total', methods=['GET'])
def get_number_of_orders_placed():
    pipeline = [
        {
            "$unwind":{"path":"$orders"}
        },
        {
            "$count": "orders"
        },
        {
            "$project": {"total":"$orders"}
        }
    ]
    ordersTotal = list(clients_collection.aggregate(pipeline))
    
    if not ordersTotal:
        return jsonify({"total": 0}), 200
     
    return jsonify(ordersTotal[0]), 200

@app.route('/statistics/orders/totalValue', methods=['GET'])
def get_total_order_value():
    pipeline = [
        {
            "$unwind": 
            {"path": "$orders"}
        },
        {
            "$unwind": 
            {"path": "$orders.items"}
        },
        {
            "$group": 
            {
                "_id": "$orders.items.productId",
                "quantity": {"$sum": "$orders.items.quantity"}
            }
        },
        {
            "$lookup": 
            {
                "from": "products",
                "localField": "_id",
                "foreignField": "_id",
                "as": "productInfo"
            }
        },
        {
            "$unwind": 
            {"path": "$productInfo"}
        },
        {
            "$project": 
            {
                "_id": 0,
                "value": {"$multiply": ["$quantity", "$productInfo.price"]}
            }
        },
        {
            "$group": 
            {
                "_id": None,
                "totalValue": {"$sum": "$value"}
            }
        },
        {
            "$project": 
            {
                "_id": 0,
                "totalValue": {"$round": ["$totalValue", 2] }
            }
        }
    ]
    
    totalValue = list(clients_collection.aggregate(pipeline))
    
    if not totalValue:
        return jsonify({"totalValue": 0}), 200
    
    return jsonify(totalValue[0]), 200


@app.route('/cleanup', methods=['POST'])
def cleanup():
    clients_collection.drop()
    products_collection.drop()  
    return '', 204
    


if __name__ == '__main__':
    app.run(debug=True, port=8080)