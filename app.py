
import sqlite3
import json
from flask import Flask, jsonify, g, request, abort, render_template, redirect, url_for, flash
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy import text, and_
from datetime import datetime, timedelta

app = Flask(__name__)

app.secret_key = 'certificates-management'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///certificates.db'
#app.config['SQLALCHEMY_ECHO'] = True


db = SQLAlchemy(app)

class Certificates(db.Model):
    __tablename__ = 'certificates'
    id = db.Column(db.Integer, primary_key=True)
    completed = db.Column(db.String(255), nullable=True)
    worker = db.Column(db.String(255), nullable=True)
    team = db.Column(db.String(255), nullable=True)
    has_to_be_replaced_before = db.Column(db.Date(), nullable=True) 
    expiration_date = db.Column(db.Date(), nullable=True)
    ticket_number = db.Column(db.String(255), nullable=True)
    certificate = db.Column(db.String(255), nullable=True)
    server_name = db.Column(db.String(255), nullable=True)
    web_type = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(255), nullable=True)
    mail_to_co = db.Column(db.Date(), nullable=True)
    csr = db.Column(db.Date(), nullable=True)
    answer_co = db.Column(db.Date(), nullable=True)
    order_certificate = db.Column(db.Date(), nullable=True)
    delivery_from_siemens = db.Column(db.Date(), nullable=True)
    p12_and_zip = db.Column(db.Date(), nullable=True)
    moved_to_server = db.Column(db.Date(), nullable=True)
    implemented = db.Column(db.Date(), nullable=True)
    deleted_gm4web = db.Column(db.Date(), nullable=True)
    evidence_in_ticket = db.Column(db.Date(), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    def __init__(self,id,completed,worker,team,has_to_be_replaced_before,expiration_date,ticket_number,certificate,server_name,web_type,type,mail_to_co,csr,answer_co,order_certificate,delivery_from_siemens,p12_and_zip,moved_to_server,implemented,deleted_gm4web,evidence_in_ticket,notes):
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

def month_string_to_number(string):
    m = {
            'jan': '1',
            'feb': '2',
            'mar': '3',
            'apr': '4',
            'may': '5',
            'jun': '6',
            'jul': '7',
            'aug': '8',
            'sep': '9',
            'oct': '10',
            'nov': '11',
            'dec': '12'
        }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html')

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

create_table()
@app.route('/', methods=['GET'])
def index():
    today = datetime.now()
    in_a_week = today + timedelta(days=7)
    certificates = db.session.query(Certificates.id,
                                    Certificates.expiration_date,
                                    Certificates.worker,
                                    Certificates.certificate,
                                    Certificates.completed,
                                    Certificates.type).filter(Certificates.expiration_date.between(today.date(), in_a_week.date())).filter(Certificates.completed=='No').all()
    
    return render_template('index.html', result=certificates)

def insert_db(data):
    certificate = Certificates(data['id'],data['completed'],data['worker'],data['team'],data['has_to_be_replaced_before'],data['expiration_date'],data['ticket_number'],data['certificate'],data['server_name'],data['web_type'],data['type'],data['mail_to_co'],data['csr'],data['answer_co'],data['order_certificate'],data['delivery_from_siemens'],data['p12_and_zip'],data['moved_to_server'],data['implemented'],data['deleted_gm4web'],data['evidence_in_ticket'],data['notes'])
    db.session.add(certificate)
    db.session.commit()

@app.route('/add/new', methods=['GET'])
def add_new():
    return render_template('new.html')

@app.route('/add/new/parse', methods=['POST'])
def parse_new():
    text = request.form['text_from_mail']
    if text == '' or text == ' ' or text == None:
        return render_template('parse.html')
    else:
        text =  text.split(' ')
        if text[0] != 'Our':
            return render_template('parse.html')
        else:
            cert_type = text[9][1:-1]
            cert_cn = text[12]
            cert_exp_month = text[16]
            cert_exp_day = text[17][:-1]
            cert_exp_year = text[18]
            exp_date = cert_exp_year+"-"+month_string_to_number(cert_exp_month)+"-"+cert_exp_day
            data = {}
            data['cn_type'] = cert_type
            data['cn'] = cert_cn
            data['expiration_date'] = exp_date
            return render_template('parse.html', data=data)

@app.route('/edit/certificate/<int:id>')
def edit_certificate(id):
    certificate = db.session.query(Certificates).filter(Certificates.id==id).first()

    certificate.completed = '' if certificate.completed == 'None' else certificate.completed
    certificate.worker =  '' if certificate.worker == 'None' else certificate.worker
    certificate.team =  '' if certificate.team == 'None' else certificate.team
    certificate.has_to_be_replaced_before = '' if certificate.has_to_be_replaced_before == 'None' else certificate.has_to_be_replaced_before
    certificate.expiration_date = '' if certificate.expiration_date == 'None' else certificate.expiration_date
    certificate.ticket_number = '' if certificate.ticket_number == 'None' else certificate.ticket_number
    certificate.certificate = '' if certificate.certificate == 'None' else certificate.certificate
    certificate.server_name = '' if certificate.server_name == 'None' else certificate.server_name
    certificate.web_type = '' if certificate.web_type == 'None' else certificate.web_type
    certificate.type = '' if certificate.type == 'None' else certificate.type
    certificate.mail_to_co = '' if certificate.mail_to_co == 'None' else certificate.mail_to_co
    certificate.csr = '' if certificate.csr == 'None' else certificate.csr
    certificate.answer_co = '' if certificate.answer_co == 'None' else certificate.answer_co
    certificate.order_certificate = '' if certificate.order_certificate == 'None' else certificate.order_certificate
    certificate.delivery_from_siemens = '' if certificate.delivery_from_siemens == 'None' else certificate.delivery_from_siemens
    certificate.p12_and_zip = '' if certificate.p12_and_zip == 'None' else certificate.p12_and_zip
    certificate.moved_to_server = '' if certificate.moved_to_server == 'None' else certificate.moved_to_server
    certificate.implemented = '' if certificate.implemented == 'None' else certificate.implemented
    certificate.deleted_gm4web = '' if certificate.deleted_gm4web == 'None' else certificate.deleted_gm4web
    certificate.evidence_in_ticket = '' if certificate.evidence_in_ticket == 'None' else certificate.evidence_in_ticket
    certificate.notes = '' if certificate.notes == 'None' else certificate.notes

    workers = {'None','Adam Karendys', 'Adam Kordjaczynski', 'Krzysztof Barabasz','Piotr Karys','Raul Balestra','Ricardo Silva'}
    completed_states = {'No', 'Yes'}
    return render_template('edit.html', certificate=certificate, workers=workers, completed_states=completed_states)

@app.route('/delete/certificate/<int:id>')
def delete_certificate(id):
    certficate = db.session.query(Certificates).filter(Certificates.id==id).first()
    db.session.delete(certficate)
    db.session.commit()
    flash('Entry deleted successfully.','success')
    return redirect('/list/all')

@app.route('/complete/certificate/<int:id>')
def complete_certificate(id):
    certficate = db.session.query(Certificates).filter(Certificates.id==id).first()
    certficate.completed = 'Yes'
    db.session.commit()
    flash('Entry marked as Completed successfully.','success')
    return redirect('/list/all')

@app.route('/edit/certificate/save/<int:id>', methods=['POST'])
def save_edit_certificate(id):
    dict = request.form.to_dict()

    certificate = db.session.query(Certificates).filter(Certificates.id==id).first()

    if certificate.has_to_be_replaced_before != dict['has_to_be_replaced_before'] and dict['has_to_be_replaced_before'] != ''  and  datetime.strptime(dict['has_to_be_replaced_before'], '%Y-%m-%d'):
        certificate.has_to_be_replaced_before = datetime.strptime(dict['has_to_be_replaced_before'], '%Y-%m-%d').date() 

    if certificate.expiration_date != dict['expiration_date'] and dict['expiration_date'] != ''  and  datetime.strptime(dict['expiration_date'], '%Y-%m-%d'):
        certificate.expiration_date = datetime.strptime(dict['expiration_date'], '%Y-%m-%d').date() 

    if certificate.mail_to_co != dict['mail_to_co'] and dict['mail_to_co'] != ''  and  datetime.strptime(dict['mail_to_co'], '%Y-%m-%d'):
        certificate.mail_to_co = datetime.strptime(dict['mail_to_co'], '%Y-%m-%d').date()
    
    if certificate.csr != dict['csr'] and dict['csr'] != '' and datetime.strptime(dict['csr'], '%Y-%m-%d'):
        certificate.csr = datetime.strptime(dict['csr'], '%Y-%m-%d').date() 
    
    if certificate.answer_co != dict['answer_co'] and dict['answer_co'] != ''  and  datetime.strptime(dict['answer_co'], '%Y-%m-%d'):
        certificate.answer_co = datetime.strptime(dict['answer_co'], '%Y-%m-%d').date() 
    
    if certificate.order_certificate != dict['order_certificate'] and dict['order_certificate'] != ''  and  datetime.strptime(dict['order_certificate'], '%Y-%m-%d'):
        certificate.order_certificate = datetime.strptime(dict['order_certificate'], '%Y-%m-%d').date() 
    
    if certificate.delivery_from_siemens != dict['delivery_from_siemens'] and dict['delivery_from_siemens'] != ''  and  datetime.strptime(dict['delivery_from_siemens'], '%Y-%m-%d'):
        certificate.delivery_from_siemens = datetime.strptime(dict['delivery_from_siemens'], '%Y-%m-%d').date() 
    
    if certificate.p12_and_zip != dict['p12_and_zip'] and dict['p12_and_zip'] != ''  and  datetime.strptime(dict['p12_and_zip'], '%Y-%m-%d'):
        certificate.p12_and_zip = datetime.strptime(dict['p12_and_zip'], '%Y-%m-%d').date() 
    
    if certificate.moved_to_server != dict['moved_to_server'] and dict['moved_to_server'] != ''  and  datetime.strptime(dict['moved_to_server'], '%Y-%m-%d'):
        certificate.moved_to_server = datetime.strptime(dict['moved_to_server'], '%Y-%m-%d').date() 
    
    if certificate.implemented != dict['implemented'] and dict['implemented'] != ''  and  datetime.strptime(dict['implemented'], '%Y-%m-%d'):
        certificate.implemented = datetime.strptime(dict['implemented'], '%Y-%m-%d').date() 
    
    if certificate.deleted_gm4web != dict['deleted_gm4web'] and dict['deleted_gm4web'] != ''  and  datetime.strptime(dict['deleted_gm4web'], '%Y-%m-%d'):
        certificate.deleted_gm4web = datetime.strptime(dict['deleted_gm4web'], '%Y-%m-%d').date() 
    
    if certificate.evidence_in_ticket != dict['evidence_in_ticket'] and dict['evidence_in_ticket'] != ''  and  datetime.strptime(dict['evidence_in_ticket'], '%Y-%m-%d'):
        certificate.evidence_in_ticket = datetime.strptime(dict['evidence_in_ticket'], '%Y-%m-%d').date() 
        
    certificate.notes =  dict['notes']
    certificate.completed =  dict['completed']
    certificate.worker =  dict['worker']
    certificate.team =   dict['team']
    certificate.ticket_number =  dict['ticket_number']
    certificate.certificate = dict['cn']
    certificate.server_name = dict['server_name']
    certificate.web_type = dict['web_type']
    certificate.type = dict['type']

    db.session.commit()
    flash('Entry updated successfully.','success')
    return redirect('/list/all')

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        criteria = request.form['criteria']
        search_text = request.form['search_text']
        items = {}
        if criteria == 'worker':
            items = db.session.query(Certificates).filter(Certificates.worker.like('''%'''+search_text+'''%''')).all()
        if criteria == 'cn':
            items = db.session.query(Certificates).filter(Certificates.certificate.like('''%'''+search_text+'''%''')).all()
        if criteria == 'completed':
            items = db.session.query(Certificates).filter(Certificates.completed.like('Yes')).all()
        if criteria == 'not_completed':
            items = db.session.query(Certificates).filter(Certificates.completed.like('No')).all()
    else:
        criteria = request.args['criteria']
        search_text = request.args['search_text']
        items = {}
        if criteria == 'worker':
            items = db.session.query(Certificates).filter(Certificates.worker.like('''%'''+search_text+'''%''')).all()
        if criteria == 'cn':
            items = db.session.query(Certificates).filter(Certificates.certificate.like('''%'''+search_text+'''%''')).all()
        if criteria == 'completed':
            items = db.session.query(Certificates).filter(Certificates.completed.like('Yes')).all()
        if criteria == 'not_completed':
            items = db.session.query(Certificates).filter(Certificates.completed.like('No')).all()
        
    print items
    return render_template('search.html', result=items)

@app.route('/add/new/certificate/save', methods=['POST'])
def save_new_certificate():
    if request.method == 'POST':
        dict = request.form.to_dict()

        if dict['has_to_be_replaced_before'] != ''  and  datetime.strptime(dict['has_to_be_replaced_before'], '%Y-%m-%d'):
            has_to_be_replaced_before = datetime.strptime(dict['has_to_be_replaced_before'], '%Y-%m-%d').date() 
        else:
            has_to_be_replaced_before = None

        if dict['expiration_date'] != ''  and  datetime.strptime(dict['expiration_date'], '%Y-%m-%d'):
            expiration_date = datetime.strptime(dict['expiration_date'], '%Y-%m-%d').date() 
        else:
            expiration_date = None

        if dict['mail_to_co'] != ''  and  datetime.strptime(dict['mail_to_co'], '%Y-%m-%d'):
            mail_to_co = datetime.strptime(dict['mail_to_co'], '%Y-%m-%d').date()
        else:
            mail_to_co = None
        
        if dict['csr'] != '' and datetime.strptime(dict['csr'], '%Y-%m-%d'):
            csr = datetime.strptime(dict['csr'], '%Y-%m-%d').date() 
        else:
            csr = None

        if dict['answer_co'] != ''  and  datetime.strptime(dict['answer_co'], '%Y-%m-%d'):
            answer_co = datetime.strptime(dict['answer_co'], '%Y-%m-%d').date() 
        else:
            answer_co = None

        if dict['order_certificate'] != ''  and  datetime.strptime(dict['order_certificate'], '%Y-%m-%d'):
            order_certificate = datetime.strptime(dict['order_certificate'], '%Y-%m-%d').date() 
        else:
            order_certificate = None

        if dict['delivery_from_siemens'] != ''  and  datetime.strptime(dict['delivery_from_siemens'], '%Y-%m-%d'):
            delivery_from_siemens = datetime.strptime(dict['delivery_from_siemens'], '%Y-%m-%d').date() 
        else:
            delivery_from_siemens = None

        if dict['p12_and_zip'] != ''  and  datetime.strptime(dict['p12_and_zip'], '%Y-%m-%d'):
            p12_and_zip = datetime.strptime(dict['p12_and_zip'], '%Y-%m-%d').date() 
        else:
            p12_and_zip = None

        if dict['moved_to_server'] != ''  and  datetime.strptime(dict['moved_to_server'], '%Y-%m-%d'):
            moved_to_server = datetime.strptime(dict['moved_to_server'], '%Y-%m-%d').date() 
        else:
            moved_to_server = None

        if dict['implemented'] != ''  and  datetime.strptime(dict['implemented'], '%Y-%m-%d'):
            implemented = datetime.strptime(dict['implemented'], '%Y-%m-%d').date() 
        else:
            implemented = None

        if dict['deleted_gm4web'] != ''  and  datetime.strptime(dict['deleted_gm4web'], '%Y-%m-%d'):
            deleted_gm4web = datetime.strptime(dict['deleted_gm4web'], '%Y-%m-%d').date() 
        else:
            deleted_gm4web = None

        if dict['evidence_in_ticket'] != ''  and  datetime.strptime(dict['evidence_in_ticket'], '%Y-%m-%d'):
            evidence_in_ticket = datetime.strptime(dict['evidence_in_ticket'], '%Y-%m-%d').date() 
        else:
            evidence_in_ticket = None
            
        if dict['completed'] == '':
            dict['completed'] = None
        if dict['worker'] == '':
            dict['worker'] = None
        if dict['team'] == '':
            dict['team'] = None
        if dict['has_to_be_replaced_before'] == '':
            dict['has_to_be_replaced_before'] = None
        if dict['expiration_date'] == '':
            dict['expiration_date'] = None
        if dict['ticket_number'] == '':
            dict['ticket_number'] = None
        if dict['cn'] == '':
            dict['cn'] = None
        if dict['server_name'] == '':
            dict['server_name'] = None
        if dict['web_type'] == '':
            dict['web_type'] = None
        if dict['type'] == '':
            dict['type'] = None
        if dict['mail_to_co'] == '':
            dict['mail_to_co'] = None
        if dict['csr'] == '':
            dict['csr'] = None
        if dict['answer_co'] == '':
            dict['answer_co'] = None
        if dict['order_certificate'] == '':
            dict['order_certificate'] = None
        if dict['delivery_from_siemens'] == '':
            dict['delivery_from_siemens'] = None
        if dict['p12_and_zip'] == '':
            dict['p12_and_zip'] = None
        if dict['moved_to_server'] == '':
            dict['moved_to_server'] = None
        if dict['implemented'] == '':
            dict['implemented'] = None
        if dict['deleted_gm4web'] == '':
            dict['deleted_gm4web'] = None
        if dict['evidence_in_ticket'] == '':
            dict['evidence_in_ticket'] = None
        if dict['notes'] == '':
            dict['notes'] = None

        completed = dict['completed']
        worker =  dict['worker']
        team =  dict['team']
        ticket_number = dict['ticket_number']
        certificate = dict['cn']
        server_name = dict['server_name']
        web_type = dict['web_type']
        type = dict['type']
        notes = dict['notes']
        #has_to_be_replaced_before = dict['has_to_be_replaced_before']
        #expiration_date = dict['expiration_date']
        # #mail_to_co = dict['mail_to_co']
        #csr = dict['csr']
        #answer_co = dict['answer_co']
        #order_certificate = dict['order_certificate']
        #delivery_from_siemens = dict['delivery_from_siemens']
        #p12_and_zip = dict['p12_and_zip']
        #moved_to_server = dict['moved_to_server']
        #implemented = dict['implemented']
        #deleted_gm4web = dict['deleted_gm4web']
        #evidence_in_ticket = dict['evidence_in_ticket']
        

        obj = db.session.query(Certificates).order_by(Certificates.id.desc()).first()
        if obj is None:
            id = 1
        else:
            id = obj.id+1
        certificate = Certificates(id,
            completed=completed,
            worker=worker,
            team=team,
            has_to_be_replaced_before=has_to_be_replaced_before,
            expiration_date=expiration_date,
            ticket_number=ticket_number,
            certificate=certificate,
            server_name=server_name,
            web_type=web_type,
            type=type,
            mail_to_co=mail_to_co,
            csr=csr,
            answer_co=answer_co,
            order_certificate=order_certificate,
            delivery_from_siemens=delivery_from_siemens,
            p12_and_zip=p12_and_zip,
            moved_to_server=moved_to_server,
            implemented=implemented,
            deleted_gm4web=deleted_gm4web,
            evidence_in_ticket=evidence_in_ticket,
            notes=notes)
        db.session.add(certificate)
        db.session.commit()
        flash('Item added successfully.','success')
        return render_template('save_success.html')
    else:
        return render_template('parse.html')

@app.route('/add/new/certificate', methods=['POST'])
def create_task():
    if not request.json:
        abort(400)
    content = request.get_json()
    insert_db(content)
    return jsonify(content)

@app.route('/list/all', methods=['GET'])
def list_all_certs():

    certificate = db.session.query(Certificates).all()
    for item in certificate:
        item.completed = '' if item.completed == None else item.completed
        item.worker =  '' if item.worker == None else item.worker
        item.team =  '' if item.team == None else item.team
        item.has_to_be_replaced_before = '' if item.has_to_be_replaced_before == None else item.has_to_be_replaced_before
        item.expiration_date = '' if item.expiration_date == None else item.expiration_date
        item.ticket_number = '' if item.ticket_number == None else item.ticket_number
        item.certificate = '' if item.certificate == None else item.certificate
        item.server_name = '' if item.server_name == None else item.server_name
        item.web_type = '' if item.web_type == None else item.web_type
        item.type = '' if item.type == None else item.type
        item.mail_to_co = '' if item.mail_to_co == None else item.mail_to_co
        item.csr = '' if item.csr == None else item.csr
        item.answer_co = '' if item.answer_co == None else item.answer_co
        item.order_certificate = '' if item.order_certificate == None else item.order_certificate
        item.delivery_from_siemens = '' if item.delivery_from_siemens == None else item.delivery_from_siemens
        item.p12_and_zip = '' if item.p12_and_zip == None else item.p12_and_zip
        item.moved_to_server = '' if item.moved_to_server == None else item.moved_to_server
        item.implemented = '' if item.implemented == None else item.implemented
        item.deleted_gm4web = '' if item.deleted_gm4web == None else item.deleted_gm4web
        item.evidence_in_ticket = '' if item.evidence_in_ticket == None else item.evidence_in_ticket
        item.notes = '' if item.notes == None else item.notes

    return render_template('list_all.html',result=certificate)


if __name__ == '__main__':
    app.run()