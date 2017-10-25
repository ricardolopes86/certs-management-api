
import sqlite3
import json
from flask import Flask, jsonify, g, request, abort, render_template, redirect, url_for, flash
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy import text
import datetime

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
        if has_to_be_replaced_before != '' and has_to_be_replaced_before != None and has_to_be_replaced_before != 'None':
            has_to_be_replaced_before = has_to_be_replaced_before.split('-')
            has_to_be_replaced_before = datetime.date(int(has_to_be_replaced_before[0]),int(has_to_be_replaced_before[1]),int(has_to_be_replaced_before[2]))
        else:
            has_to_be_replaced_before = None

        if expiration_date != '' and expiration_date != None and expiration_date != 'None':
            expiration_date = expiration_date.split('-') 
            expiration_date = datetime.date(int(expiration_date[0]),int(expiration_date[1]),int(expiration_date[2]))
        else:
            expiration_date = None

        if mail_to_co != '' and mail_to_co != None and mail_to_co != 'None':
            mail_to_co = mail_to_co.split('-')
            mail_to_co =  datetime.date(int(mail_to_co[0]),int(mail_to_co[1]),int(mail_to_co[2]))
        else:
            mail_to_co = None
            
        if csr != '' and csr != None and csr != 'None':
            csr = csr.split('-')
            csr = datetime.date(int(csr[0]),int(csr[1]),int(csr[2]))
        else:
            csr = None

        if answer_co != '' and answer_co != None and answer_co != 'None':
            answer_co = answer_co.split('-')
            answer_co = datetime.date(int(answer_co[0]),int(answer_co[1]),int(answer_co[2]))
        else:
            answer_co = None

        if order_certificate != '' and order_certificate != None and order_certificate != 'None':
            order_certificate = order_certificate.split('-')
            order_certificate = datetime.date(int(order_certificate[0]),int(order_certificate[1]),int(order_certificate[2]))
        else:
            order_certificate = None

        if delivery_from_siemens != '' and delivery_from_siemens != None and delivery_from_siemens != 'None':
            delivery_from_siemens = delivery_from_siemens.split('-')
            delivery_from_siemens =  datetime.date(int(delivery_from_siemens[0]),int(delivery_from_siemens[1]),int(delivery_from_siemens[2]))
        else:
            delivery_from_siemens = None

        if p12_and_zip != '' and p12_and_zip != None and p12_and_zip != 'None':
            p12_and_zip = p12_and_zip.split('-')
            p12_and_zip =  datetime.date(int(p12_and_zip[0]),int(p12_and_zip[1]),int(p12_and_zip[2]))
        else:
            p12_and_zip = None

        if moved_to_server != '' and moved_to_server != None and moved_to_server != 'None':
            moved_to_server = moved_to_server.split('-')
            moved_to_server =  datetime.date(int(moved_to_server[0]),int(moved_to_server[1]),int(moved_to_server[2]))
        else:
            moved_to_server = None

        if implemented != '' and implemented != None and implemented != 'None':
            implemented = implemented.split('-')
            implemented =  datetime.date(int(implemented[0]),int(implemented[1]),int(implemented[2]))
        else:
            implemented = None

        if deleted_gm4web != '' and deleted_gm4web != None and deleted_gm4web != 'None':
            deleted_gm4web = deleted_gm4web.split('-')
            deleted_gm4web =  datetime.date(int(deleted_gm4web[0]),int(deleted_gm4web[1]),int(deleted_gm4web[2]))
        else:
            deleted_gm4web = None

        if evidence_in_ticket != '' and evidence_in_ticket != None and evidence_in_ticket != 'None':
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
    return render_template('index.html')

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
    return render_template('edit.html', certificate=certificate)

@app.route('/delete/certificate/<int:id>')
def delete_certificate(id):
    certficate = db.session.query(Certificates).filter(Certificates.id==id).first()
    db.session.delete(certficate)
    db.session.commit()
    flash('Entry deleted successfully.','success')
    return redirect('/list/all' + '#myModal')

@app.route('/complete/certificate/<int:id>')
def complete_certificate(id):
    certficate = db.session.query(Certificates).filter(Certificates.id==id).first()
    certficate.completed = 'Yes'
    db.session.commit()
    flash('Entry marked as Completed successfully.','success')
    return redirect('/list/all' + '#myModal')

@app.route('/edit/certificate/save/<int:id>', methods=['POST'])
def save_edit_certificate(id):
    dict = request.form.to_dict()
    
    certficate = db.session.query(Certificates).filter(Certificates.id==id).first()
    certficate.completed = dict['completed']
    certficate.worker =  dict['worker']
    certficate.team =  dict['team']
    certficate.has_to_be_replaced_before = dict['has_to_be_replaced_before']
    certficate.expiration_date = dict['expiration_date']
    certficate.ticket_number = dict['ticket_number']
    certficate.certificate = dict['cn']
    certficate.server_name = dict['server_name']
    certficate.web_type = dict['web_type']
    certficate.type = dict['type']
    certficate.mail_to_co = dict['mail_to_co']
    certficate.csr = dict['csr']
    certficate.answer_co = dict['answer_co']
    certficate.order_certificate = dict['order_certificate']
    certficate.delivery_from_siemens = dict['delivery_from_siemens']
    certficate.p12_and_zip = dict['p12_and_zip']
    certficate.moved_to_server = dict['moved_to_server']
    certficate.implemented = dict['implemented']
    certficate.deleted_gm4web = dict['deleted_gm4web']
    certficate.evidence_in_ticket = dict['evidence_in_ticket']
    certficate.notes = dict['notes']

    db.session.commit()
    flash('Entry saved successfully.','success')
    return redirect('/list/all' + '#myModal')

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
        # print dict
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

        # for item in dict:
        #     print item

        completed = dict['completed']
        worker =  dict['worker']
        team =  dict['team']
        has_to_be_replaced_before = dict['has_to_be_replaced_before']
        expiration_date = dict['expiration_date']
        ticket_number = dict['ticket_number']
        certificate = dict['cn']
        server_name = dict['server_name']
        web_type = dict['web_type']
        type = dict['type']
        mail_to_co = dict['mail_to_co']
        csr = dict['csr']
        answer_co = dict['answer_co']
        order_certificate = dict['order_certificate']
        delivery_from_siemens = dict['delivery_from_siemens']
        p12_and_zip = dict['p12_and_zip']
        moved_to_server = dict['moved_to_server']
        implemented = dict['implemented']
        deleted_gm4web = dict['deleted_gm4web']
        evidence_in_ticket = dict['evidence_in_ticket']
        notes = dict['notes']

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
    return render_template('list_all.html',result=db.session.query(Certificates).all())


if __name__ == '__main__':
    app.run()