from flask import Flask, jsonify, request
from cassandra.cluster import Cluster
import uuid
from datetime import datetime, timezone

app = Flask(__name__)

cluster = Cluster(['127.0.0.1']) 
session = cluster.connect()


with app.app_context():
    
    session.execute("DROP keyspace if exists chatservice")
    
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS chatservice
        WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 1 };
    """)
    
    session.execute("""
        CREATE TABLE IF NOT EXISTS chatservice.channels (
            id text,
            owner text,
            topic text,
            PRIMARY KEY (id, owner)
        );
    """)
    
    # Messages 1
    session.execute("""
        CREATE TABLE IF NOT EXISTS chatservice.messagesId (
            channel_id text,
            text text,
            author text,
            timestamp timestamp,
            PRIMARY KEY (channel_id, author, timestamp)
        );
    """)    
    
    # Messages 2
    session.execute("""
        CREATE TABLE IF NOT EXISTS chatservice.messagesIdDate (
            channel_id text,
            text text,
            author text,
            timestamp timestamp,
            PRIMARY KEY (channel_id, timestamp, author)
        );
    """)
    
    session.execute("""
        CREATE TABLE IF NOT EXISTS chatservice.members (
            channel_id text,
            member text,
            PRIMARY KEY (channel_id, member)
        );
    """)
    

@app.route('/channels', methods=['PUT'])
def create_channel():
    
    data = request.json

    if 'owner' not in data or not data['owner'] or data['owner']==" ":
        return jsonify ({"error":"Klaida. Neįvestas savininko vardas."}), 400

    if 'id' not in data or not data['id'] or data['id']==" ":
        channel_id = str(uuid.uuid4())
        was_given = False
    else:
        channel_id = data['id']
        was_given = True
        
    owner = data['owner']
    topic = data.get('topic', '') 

    insert_channel_query = f"INSERT INTO chatservice.channels (id, owner, topic) VALUES (%s, %s, %s) IF NOT EXISTS"
    
    while True:
        result = session.execute(insert_channel_query, (channel_id, owner, topic))
        if result.was_applied:
            insert_member_query = f"INSERT INTO chatservice.members (channel_id, member) VALUES (%s, %s) IF NOT EXISTS"
            session.execute(insert_member_query, (channel_id, owner))
            return jsonify({"id": channel_id}), 201
        elif not result.was_applied and was_given:
            return jsonify({"error": "Kanalas tokiu ID jau egzistuoja."}), 400
        else:
            channel_id = str(uuid.uuid4())

@app.route('/channels/<string:channel_id>', methods=['GET'])
def get_channel(channel_id):
    
    get_channel_query = f"SELECT * FROM chatservice.channels WHERE id = %s"
    result = session.execute(get_channel_query, (channel_id,))
    channel = result.one() 
    
    if channel:
        info = {
            'id': str(channel.id),
            'owner': str(channel.owner),
        }
        if channel.topic:
            info['topic'] = str(channel.topic)
        return jsonify(info), 200
    else:
        return jsonify({"error": "Kanalas tokiu ID nerastas"}), 404

@app.route('/channels/<channel_id>', methods=['DELETE'])
def delete_channel(channel_id):
    
    get_channel_query = f"SELECT id FROM chatservice.channels WHERE id = %s"
    result = session.execute(get_channel_query, (channel_id,))
    channel = result.one()
    if not channel:
        return jsonify({"error": "Kanalas tokiu ID nerastas"}), 404
    
    delete_query1="""
    DELETE FROM chatservice.messagesId
    WHERE channel_id=%s;
    """
    
    delete_query2="""
    DELETE FROM chatservice.messagesIdDate
    WHERE channel_id=%s;
    """
    
    delete_query3="""
    DELETE FROM chatservice.members
    WHERE channel_id=%s;
    """
    
    delete_query4="""
    DELETE FROM chatservice.channels
    WHERE id=%s;
    """
    
    session.execute(delete_query1, (channel_id,))
    session.execute(delete_query2, (channel_id,))
    session.execute(delete_query3, (channel_id,))
    session.execute(delete_query4, (channel_id,))
    
    return jsonify(), 204

@app.route('/channels/<string:channel_id>/messages', methods=['PUT'])
def post_message(channel_id):
    
    data = request.get_json()
    
    if 'text' not in data or not data['text'] or data['text']==" ":
        return jsonify({"error":"Klaida. Neįvestas žinutės tekstas."}), 400
    elif 'author' not in data or not data['author'] or data['author']==" ":
        return jsonify({"error":"Klaida. Neįvestas žinutės autorius."}), 400
    
    get_channel_query = f"SELECT id FROM chatservice.channels WHERE id = %s"
    result = session.execute(get_channel_query, (channel_id,))
    channel = result.one()
    if not channel:
        return jsonify({"error": "Kanalas tokiu ID nerastas"}), 404
    
    timestamp = datetime.now(timezone.utc)
    
    post_message_query1="""
    INSERT INTO chatservice.messagesId (channel_id, text, author, timestamp)
    VALUES (%s, %s, %s, %s)
    IF NOT EXISTS;
    """
    
    post_message_query2="""
    INSERT INTO chatservice.messagesIdDate (channel_id, text, author, timestamp)
    VALUES (%s, %s, %s, %s)
    IF NOT EXISTS;
    """
    
    session.execute(post_message_query1, (channel_id, data['text'], data['author'], timestamp))
    session.execute(post_message_query2, (channel_id, data['text'], data['author'], timestamp))
    
    return jsonify({"message":"Žinutė pridėta sėkmingai."}), 201
    
@app.route('/channels/<string:channel_id>/messages', methods=['GET'])
def get_messages(channel_id):
    
    start_at = request.args.get('startAt')
    author = request.args.get('author')
    
    get_channel_query = f"SELECT id FROM chatservice.channels WHERE id = %s"
    result = session.execute(get_channel_query, (channel_id,))
    channel = result.one()
    if not channel:
        return jsonify({"error": "Kanalas tokiu ID nerastas"}), 404
    
    if not start_at and not author:
        get_message_query="""
        SELECT text, author, timestamp FROM chatservice.messagesIdDate
        WHERE channel_id=%s
        ORDER BY timestamp ASC;
        """
        rows=session.execute(get_message_query, (channel_id,))    

    elif author and not start_at:
        get_message_query="""
        SELECT text, author, timestamp FROM chatservice.messagesId
        WHERE channel_id=%s and author=%s
        ORDER BY timestamp ASC;
        """
        rows=session.execute(get_message_query, (channel_id, author))

    elif start_at and not author:
        timestamp = datetime.fromisoformat(str(start_at))
        get_message_query="""
        SELECT text, author, timestamp FROM chatservice.messagesIdDate
        WHERE channel_id=%s and timestamp>=%s
        ORDER BY timestamp ASC;
        """
        rows=session.execute(get_message_query, (channel_id, timestamp))
    
    else: 
        timestamp = datetime.fromisoformat(str(start_at))
        get_message_query="""
        SELECT text, author, timestamp FROM chatservice.messagesId
        WHERE channel_id=%s and author=%s and timestamp>=%s
        ORDER BY timestamp ASC;
        """
        rows=session.execute(get_message_query, (channel_id, author, timestamp))
        
    if rows:   
        messages = [{'text': row.text, 'author': row.author, 'timestamp': str(row.timestamp)} for row in rows]  
        return jsonify(messages), 200
    else:
        return jsonify({"message":"Nėra žinučių atitinkančių paieškos kriterijus."}), 200
            
@app.route('/channels/<string:channel_id>/members', methods=['PUT'])
def register_member(channel_id):
    
    data=request.get_json()
    
    if 'member' not in data or not data['member'] or data['member']==" ":
        return jsonify({"error":"Klaida. Įveskite narį."}), 400

    get_channel_query = f"SELECT id FROM chatservice.channels WHERE id = %s"
    result = session.execute(get_channel_query, (channel_id,))
    channel = result.one()
    if not channel:
        return jsonify({"error": "Kanalas tokiu ID nerastas"}), 404
    
    get_member_query="""
        SELECT * FROM chatservice.members
        WHERE channel_id=%s and member=%s;
        """
    rows=session.execute(get_member_query, (channel_id, data['member']))
    
    members = rows.one()
    if members:
        return jsonify ({"error":f"Narys '{data['member']}' jau registruotas kanale."}), 400
    
    register_member_query="""
    INSERT INTO chatservice.members (channel_id, member)
    VALUES (%s, %s)
    IF NOT EXISTS;
    """
    
    session.execute(register_member_query, (channel_id, data['member']))
    
    return jsonify({"message":f"Narys '{data['member']}' užregistruotas sėkmingai."}), 201
    
@app.route('/channels/<string:channel_id>/members', methods=['GET'])
def get_members(channel_id):
    
    get_channel_query = f"SELECT id FROM chatservice.channels WHERE id = %s"
    result = session.execute(get_channel_query, (channel_id,))
    channel = result.one()
    if not channel:
        return jsonify({"error": "Kanalas tokiu ID nerastas"}), 404
    
    get_members_query="""
    SELECT member from chatservice.members
    WHERE channel_id=%s;
    """
    rows=session.execute(get_members_query, (channel_id,))
    
    if rows:
        members = [str(row.member) for row in rows]
        return jsonify(members), 200
    else:
        return jsonify({"message":"Kanalas neturi narių."}), 200 
    
@app.route('/channels/<channel_id>/members/<member_id>', methods=['DELETE'])
def delete_member(channel_id, member_id):
    
    get_channel_query = f"SELECT id FROM chatservice.channels WHERE id = %s"
    result = session.execute(get_channel_query, (channel_id,))
    channel = result.one()
    if not channel:
        return jsonify({"error": "Kanalas tokiu ID nerastas"}), 404
    
    get_member_query="""
    SELECT member FROM chatservice.members
    WHERE channel_id=%s and member=%s;
    """
    rows=session.execute(get_member_query, (channel_id, member_id))
    
    if not rows:
        return jsonify({"error":"Toks narys nurodytame kanale neegzistuoja."}), 404
    
    delete_member_query="""
    DELETE FROM chatservice.members
    WHERE channel_id=%s and member=%s;
    """
    
    session.execute(delete_member_query, (channel_id, member_id))
    
    return jsonify(), 204
    
if __name__ == '__main__':
    app.run(debug=True, port=8080)