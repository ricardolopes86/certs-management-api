#!flask/bin/python
import sqlite3
import json
from flask import Flask, jsonify, g, request, abort
from flask_sqlalchemy import Model, SQLAlchemy
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///certificates.db'
app.config['SQLALCHEMY_ECHO'] = True


db = SQLAlchemy(app)

class Certificates(db.Model):
    __tablename__ = 'certificates'
    id = db.Column(db.Integer, primary_key=True)
    completed = db.Column(db.String(255))
    worker = db.Column(db.String(255))
    team = db.Column(db.String(255))
    has_to_be_replaced_before = db.Column(db.Date()) 
    expiration_date = db.Column(db.Date())
    ticket_number = db.Column(db.String(255))
    certificate = db.Column(db.String(255))
    server_name = db.Column(db.String(255))
    web_type = db.Column(db.String(255))
    type = db.Column(db.String(255))
    mail_to_co = db.Column(db.Date())
    csr = db.Column(db.Date())
    answer_co = db.Column(db.Date())
    order_certificate = db.Column(db.Date())
    delivery_from_siemens = db.Column(db.Date())
    p12_and_zip = db.Column(db.Date())
    moved_to_server = db.Column(db.Date())
    implemented = db.Column(db.Date())
    deleted_gm4web = db.Column(db.Date())
    evidence_in_ticket = db.Column(db.Date())
    notes = db.Column(db.Text)

    def __init__(self,id,completed,worker,team,has_to_be_replaced_before,expiration_date,ticket_number,certificate,server_name,web_type,type,mail_to_co,csr,answer_co,order_certificate,delivery_from_siemens,p12_and_zip,moved_to_server,implemented,deleted_gm4web,evidence_in_ticket,notes):
        if has_to_be_replaced_before != '':
            has_to_be_replaced_before = has_to_be_replaced_before.split('-')
            has_to_be_replaced_before = datetime.date(int(has_to_be_replaced_before[0]),int(has_to_be_replaced_before[1]),int(has_to_be_replaced_before[2]))
        else:
            has_to_be_replaced_before = None

        if expiration_date != '':
            expiration_date = expiration_date.split('-') 
            expiration_date = datetime.date(int(expiration_date[0]),int(expiration_date[1]),int(expiration_date[2]))
        else:
            expiration_date = None

        if mail_to_co != '':
            mail_to_co = mail_to_co.split('-')
            mail_to_co =  datetime.date(int(mail_to_co[0]),int(mail_to_co[1]),int(mail_to_co[2]))
        else:
            mail_to_co = None
            
        if csr != '':
            csr = csr.split('-')
            csr = datetime.date(int(csr[0]),int(csr[1]),int(csr[2]))
        else:
            csr = None

        if answer_co != '':
            answer_co = answer_co.split('-')
            answer_co = datetime.date(int(answer_co[0]),int(answer_co[1]),int(answer_co[2]))
        else:
            answer_co = None

        if order_certificate != '':
            order_certificate = order_certificate.split('-')
            order_certificate = datetime.date(int(order_certificate[0]),int(order_certificate[1]),int(order_certificate[2]))
        else:
            order_certificate = None

        if delivery_from_siemens != '':
            delivery_from_siemens = delivery_from_siemens.split('-')
            delivery_from_siemens =  datetime.date(int(delivery_from_siemens[0]),int(delivery_from_siemens[1]),int(delivery_from_siemens[2]))
        else:
            delivery_from_siemens = None

        if p12_and_zip != '':
            p12_and_zip = p12_and_zip.split('-')
            p12_and_zip =  datetime.date(int(p12_and_zip[0]),int(p12_and_zip[1]),int(p12_and_zip[2]))
        else:
            p12_and_zip = None

        if moved_to_server != '':
            moved_to_server = moved_to_server.split('-')
            moved_to_server =  datetime.date(int(moved_to_server[0]),int(moved_to_server[1]),int(moved_to_server[2]))
        else:
            moved_to_server = None

        if implemented != '':
            implemented = implemented.split('-')
            implemented =  datetime.date(int(implemented[0]),int(implemented[1]),int(implemented[2]))
        else:
            implemented = None

        if deleted_gm4web != '':
            deleted_gm4web = deleted_gm4web.split('-')
            deleted_gm4web =  datetime.date(int(deleted_gm4web[0]),int(deleted_gm4web[1]),int(deleted_gm4web[2]))
        else:
            deleted_gm4web = None

        if evidence_in_ticket != '':
            evidence_in_ticket = evidence_in_ticket.split('-')
            evidence_in_ticket =  datetime.date(int(evidence_in_ticket[0]),int(evidence_in_ticket[1]),int(evidence_in_ticket[2]))
        else:
            evidence_in_ticket = None

        self.id = id
        self.completed = completed
        self.worker = worker
        self.team = team
        self.has_to_be_replaced_before = has_to_be_replaced_before
        self.expiration_date = expiration_date
        self.ticket_number = ticket_number
        self.certificate = certificate
        self.server_name = server_name
        self.web_type = web_type
        self.type = type
        self.mail_to_co = mail_to_co
        self.csr = csr
        self.answer_co = answer_co
        self.order_certificate = order_certificate
        self.delivery_from_siemens = delivery_from_siemens
        self.p12_and_zip = p12_and_zip
        self.moved_to_server = moved_to_server
        self.implemented = implemented
        self.deleted_gm4web = deleted_gm4web
        self.evidence_in_ticket = evidence_in_ticket
        self.notes = notes


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
    certificate = Certificates(data['id'],data['completed'],data['worker'],data['team'],data['has_to_be_replaced_before'],data['expiration_date'],data['ticket_number'],data['certificate'],data['server_name'],data['web_type'],data['type'],data['mail_to_co'],data['csr'],data['answer_co'],data['order_certificate'],data['delivery_from_siemens'],data['p12_and_zip'],data['moved_to_server'],data['implemented'],data['deleted_gm4web'],data['evidence_in_ticket'],data['notes'])
    db.session.add(certificate)
    db.session.commit()

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