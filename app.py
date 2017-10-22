#!flask/bin/python
import sqlite3
import json
from flask import Flask, jsonify, g, request, abort

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}, 404)

    #columns = [
    #           'id', 
    #           'completed', 
    #           'worker', 
    #           'team', 
    #           'has_to_be_replaced_before', 
    #           'expiration_date',
    #           'ticket_number',
    #           'certificate',
    #           'server_name',
    #           'web_type',
    #           'type',
    #           'mail_to_co',
    #           'csr',
    #           'answer_co',
    #           'order_certificate',
    #           'delivery_from_siemens',
    #           'p12_and_zip',
    #           'moved_to_server',
    #           'implemented',
    #           'deleted_gm4web',
    #           'evidence_in_ticket',
    #           'notes'
    # ]

def create_table():
    try:
        with sqlite3.connect('certificates.db') as con:
            cur = con.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS certificates (
                            id INTEGER PRIMARY KEY NOT NULL,
                            completed BOOLEAN,
                            worker VARCHAR(255) NOT NULL,
                            team VARCHAR(255),
                            has_to_be_replaced_before DATE,
                            expiration_date DATE,
                            ticket_number VARCHAR(255),
                            certificate VARCHAR(255),
                            server_name VARCHAR(255),
                            web_type VARCHAR(255),
                            type VARCHAR(255),
                            mail_to_co DATE,
                            csr DATE,
                            answer_co DATE,
                            order_certificate DATE,
                            delivery_from_siemens DATE,
                            p12_and_zip DATE,
                            moved_to_server DATE,
                            implemented DATE,
                            deleted_gm4web DATE,
                            evidence_in_ticket DATE,
                            notes TEXT);
                            ''')
            con.commit()
    except sqlite3.OperationalError, msg:
        print msg
        con.rollback()
    finally:
        con.close()

print "call create table"
create_table()

def query_like_db(field, data):
    field = field.lower()
    if type(data) == str:
        data = data.lower()
    con = sqlite3.connect("certificates.db")
    con.row_factory = sqlite3.Row
    result = []
    cur = con.cursor()
    sql = '''select * from certificates where '''+field+''' like "%{wk}%"'''.format(wk=data)
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        result.append([x for x in row])
    return result

def query_db(field, data):
    field = field.lower()
    if type(data) == str:
        data = data.lower()
    con = sqlite3.connect("certificates.db")
    con.row_factory = sqlite3.Row
    result = []
    cur = con.cursor()
    cur.execute('''select * from certificates where '''+str(field)+''' = "{d}"'''.format(d=data))
    rows = cur.fetchall()
    for row in rows:
        result.append([x for x in row])
    return result

def query_db_all():
    con = sqlite3.connect("certificates.db")
    con.row_factory = sqlite3.Row
    result = []
    cur = con.cursor()
    cur.execute('''select * from certificates''')
    rows = cur.fetchall()
    for row in rows:
        result.append([x for x in row])
    return result

def insert_db(data):
    DATABASE = 'certificates.db'
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        parameters = []
        for key, value in data.items():
            parameters.append(value)
            
        #sql = '''INSERT INTO certificates VALUES ({1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20},{21},{22}) '''.format(1=parameters[0],2=parameters[1],3=parameters[2],4=parameters[3],5=parameters[4],6=parameters[5],7=parameters[6],8=parameters[7],9=parameters[8],10=parameters[9],11=parameters[10],12=parameters[11],13=parameters[12],14=parameters[13],15=parameters[14],16=parameters[15],17=parameters[16],18=parameters[17],19=parameters[18],20=parameters[19],21=parameters[20],22=parameters[21])

        cur.execute('''INSERT INTO certificates VALUES (?) ''', *parameters)

        con.commit()

@app.route('/api/certificate', methods=['POST'])
def create_task():
    if not request.json:
        abort(400)
    content = request.get_json()
    insert_db(content)
    return jsonify(content)

@app.route('/api/all', methods=['GET'])
def index():
    return jsonify(query_db_all())

@app.route('/api/worker/<string:worker>', methods=['GET'])
def get_task_by_worker(worker):
    return jsonify(query_like_db('worker', worker))

@app.route('/api/cert/<int:id>', methods=['GET'])
def get_task_by_id(id):
    return jsonify(query_db('id', id))

@app.route('/api/completed/yes', methods=['GET'])
def all_completed():
    return jsonify(query_db('completed', 'yes'))

@app.route('/api/completed/no', methods=['GET'])
def all_not_completed():
    return jsonify(query_like_db('completed', 'no'))

@app.route('/api/team/<string:team>', methods=['GET'])
def get_cert_by_team(team):
    return jsonify(query_like_db('team', team))

@app.route('/api/cn/<string:cn>', methods=['GET'])
def get_cert_by_cn(cn):
    return jsonify(query_like_db('certificate', cn))

@app.route('/api/cn/<string:cn>/full', methods=['GET'])
def get_cert_by_cn_full(cn):
    return jsonify(query_db('certificate', cn))


if __name__ == '__main__':
    app.run()