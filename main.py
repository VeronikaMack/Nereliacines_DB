import redis
import re
from flask import (Flask, request, jsonify, abort)

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

licenseRegex = "^[A-Z0-9]{1,7}$"

app = Flask(__name__)

#PUT metodas garazo registracijai
@app.route('/garage', methods=['PUT'])
def register_garage():
    
    #pasiemame naudotojo ivesta info is postman body
    data = request.get_json()
    
    #tikriname ar sie laukai uzpildyti
    garage_id = data.get('id')
    spots = data.get('spots')
    address = data.get('address')
    
    if not garage_id:
        return jsonify({"error": "Nenurodytas id laukas"}), 400
    if not spots:
        return jsonify({"error": "Nenurodytas spots laukas"}), 400
    if not address:
        return jsonify({"error": "Nenurodytas adress laukas"}), 400
    
    #sukuriame rakta garazo saugojimui pagal ID
    key = f'garage:{garage_id}'
    while True:
        with r.pipeline() as trans: 
            try:
                trans.watch(key)
                if trans.exists(key):
                    trans.unwatch()
                    return jsonify ({"error": "Toks garažas jau užregistruotas."}), 400

                trans.multi()
                trans.hset(key, mapping={"id":data['id'], "spots": data['spots'], "address": data['address']})
                trans.execute()
                return jsonify({"message": "Garažas sėkmingai užregistruotas sistemoje."}), 200
            
            except redis.exceptions.WatchError:
                continue
            finally:
                trans.unwatch()

@app.route('/garage/<garage_id>', methods=['GET'])
def get_garage(garage_id):
    key = f'garage:{garage_id}'
    
    #tikriname ar toks garazas egzistuoja
    if not r.exists(key):
        return jsonify({"error": "Garažas tokiu ID nerastas"}), 404
    
    #Pasiemame informacija apie garaza is Redis
    id = r.hget(key, 'id')
    spots = r.hget(key, 'spots')
    address = r.hget(key, 'address')
    
    tekstas = {
            "id": str(id),
            "spots": int(spots),
            "address":str(address),
    }

    return jsonify(tekstas), 200
    
@app.route('/garage/<garage_id>/configuration/spots', methods=['GET'])
def get_garage_spots(garage_id):
    key = f'garage:{garage_id}'

    #tikriname ar toks garazas egzistuoja
    if not r.exists(key):
        return jsonify({"error": "Garažas tokiu ID nerastas"}), 404

    #Randame vietu kintamajo reiksme
    spots = r.hget(key, 'spots')

    #Graziname vietu reiksme
    return str(int(spots)), 200

@app.route('/garage/<garage_id>/configuration/spots', methods=['POST'])
def change_garage_spots(garage_id):
    key = f'garage:{garage_id}'
    
    #pasiemame naudotojo ivesta info is postman body
    data = request.get_json()
    new_spots = data.get('spots')
    
    #tikriname ar duotas skaicius ir ar teigiamas
    if not isinstance(new_spots, int) or new_spots <= 0:
        return jsonify({"error": "Neteisingas skaičius pateiktas. (Vietų skaičius turi buti teigiamas)"}), 400
    while True:
        with r.pipeline() as trans: 
            try:
                trans.watch(key)
                if not trans.exists(key):
                    trans.unwatch()
                    return jsonify({"error": "Garažas tokiu ID nerastas."}), 404

                trans.multi() 
                trans.hset(key, 'spots', new_spots)
                trans.execute()
                return jsonify({"message": "Garažo vietų skaičius pakeistas."}), 200
            
            except redis.exceptions.WatchError:
                continue
            finally:
                trans.unwatch()

@app.route('/garage/<garage_id>/spots/<int:spot_no>', methods=['POST'])
def register_spot(garage_id, spot_no):
    key = f'garage:{garage_id}'
    while True:
        with r.pipeline() as trans: 
            try:
                trans.watch(key)
                if not trans.exists(key):
                    trans.unwatch()
                    return jsonify({"error": "Garažas tokiu ID nerastas."}), 404

                trans.execute()
                trans.hget(key, 'spots')
                spots=trans.execute()
                
                if spot_no<1 or spot_no>int(spots[0]):
                    trans.unwatch()
                    return jsonify({"error":"Vieta nerasta."}), 404
                
                trans.execute()
                spot_key = f'garage:{garage_id}:spot:{spot_no}'
                trans.exists(spot_key)
                spot_exists=trans.execute()
                
                if spot_exists[0]:
                    trans.unwatch()
                    return ({"error":"Vieta jau užimta."}), 404
                
                data = request.get_json()
                license_no = data.get('licenseNo')
                
                if re.search(licenseRegex, license_no) == None:
                    trans.unwatch()
                    return jsonify({"error": "Neteisingi mašinos numeriai"}), 400
                
                trans.multi() 
                trans.set(spot_key, license_no)
                trans.execute()
                return jsonify({"message":"Vieta užimta sėkmingai."}), 200
            
            except redis.exceptions.WatchError:
                continue
            finally:
                trans.unwatch()

@app.route('/garage/<garage_id>/spots/<int:spot_no>', methods=['GET'])
def get_license_plate(garage_id, spot_no):
    key = f'garage:{garage_id}'

    #tikriname ar toks garazas egzistuoja
    if not r.exists(key):
        return jsonify({"error": "Garažas tokiu ID nerastas"}), 404

    #Gauname vietu kieki garaze
    spots = r.hget(key, "spots")
    spots = int(spots)

    #Tikriname ar pasirinktos vietos sk tinkamas
    if spot_no < 1 or spot_no > spots:
        return jsonify({"error": "Pasirinkta vieta neegizstuoja arba įvedėte neigiamą sk"}), 400

    #Sukuriame nauja rakta
    spot_key = f'garage:{garage_id}:spot:{spot_no}'

    #Tikriname ar vieta uzimta
    if not r.exists(spot_key):
        return "", 204 

    #Randame vietoje esancios masinos nr
    license_no = r.get(spot_key)

    return str(license_no), 200

@app.route('/garage/<garage_id>/spots/<int:spot_no>', methods=['DELETE'])
def free_spot(garage_id, spot_no):
    key = f'garage:{garage_id}'
    while True:
        with r.pipeline() as trans: 
            try:
                trans.watch(key)
                if not trans.exists(key):
                    trans.unwatch()
                    return jsonify({"error": "Garažas tokiu ID nerastas."}), 404

                
                spots = trans.hget(key, 'spots')
                trans.execute()
                
                if spot_no<1 or spot_no>int(spots):
                    trans.unwatch()
                    return jsonify({"error":"Vieta nerasta."}), 404
                
                
                spot_key = f'garage:{garage_id}:spot:{spot_no}'

                if not r.exists(spot_key):
                 trans.unwatch()
                 return jsonify({"error": "Vieta laisva."}), 400
                
                
                
                trans.multi() 
                trans.delete(spot_key)
                trans.execute()
                
                
                return ({"message":"Vieta atlaisvinta sėkmingai"}), 200
            
        
            except redis.exceptions.WatchError:
                continue
            finally:
                trans.unwatch()

@app.route('/garage/<garage_id>/status', methods=['GET'])
def get_garage_status(garage_id):
    key = f'garage:{garage_id}'

    #tikriname ar toks garazas egzistuoja
    if not r.exists(key):
        return jsonify({"error": "Garažas tokiu ID nerastas"}), 404

    #Vietu sk garaze
    spots = r.hget(key, "spots")
    total_spots = int(spots)

    occupied_spots = 0

    for spot_no in range(1, total_spots + 1):
        spot_key = f'garage:{garage_id}:spot:{spot_no}'
        if r.exists(spot_key):
            occupied_spots += 1

    #Randame kiek laisvu vietu
    free_spots = total_spots - occupied_spots

    return jsonify({
        "freeSpots": free_spots,
        "occupiedSpots": occupied_spots
    }), 200

@app.route('/flush', methods=['POST'])
def flush_database():
    r.flushdb()  
    return jsonify({"message": "Database cleared successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)