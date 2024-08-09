
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Date,Float
from datetime import date

import json
app = Flask(__name__)

users = {
    'Mamadou': 'mamadou',
    'Billo': 'billo',
    'Diallo': 'diallo'
}

ENV='dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:groupe7@db/immobilier'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI']=''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db=SQLAlchemy(app)

class immeuble(db.Model):
    __tablename__='immeuble'
    id_immeuble=db.Column(db.Integer, primary_key=True)
    nom=db.Column(db.String(100))
    nomProprio = db.Column(db.String(100))
    nbrEtage = db.Column(db.Integer)
    nbrAppart = db.Column(db.Integer)
    adresse = db.Column(db.String(100))

    def __init__(self,nom,nomProprio,nbrEtage,nbrAppart,adresse):
        self.nom=nom
        self.nomProprio = nomProprio
        self.nbrEtage = nbrEtage
        self.nbrAppart = nbrAppart
        self.adresse = adresse

class appartement(db.Model):
    __tablename__='appartement'
    id_appart=db.Column(db.Integer, primary_key=True)
    id_immeuble = db.Column(db.Integer, ForeignKey('immeuble.id_immeuble'))
    noAppart = db.Column(db.Integer)
    noEtage= db.Column(db.Integer)
    type= db.Column(db.String(100))
    def __init__(self,noAppart,noEtage,type,id_immeuble):
        self.noAppart=noAppart
        self.noEtage = noEtage
        self.type = type
        self.id_immeuble=id_immeuble

class client(db.Model):
    __tablename__='client'
    id_client=db.Column(db.Integer, primary_key=True)
    id_immeuble = db.Column(db.Integer, ForeignKey('immeuble.id_immeuble'))
    id_appart=db.Column(db.Integer, ForeignKey('appartement.id_appart'))
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    noAppart = db.Column(db.Integer)
    def __init__(self,noAppart,nom,prenom,id_immeuble,id_appart):
        self.nom=nom
        self.noAppart=noAppart
        self.prenom = prenom
        self.id_appart = id_appart
        self.id_immeuble=id_immeuble

class personnel(db.Model):
    __tablename__='personnel'
    id_personnel=db.Column(db.Integer, primary_key=True)
    id_immeuble = db.Column(db.Integer, ForeignKey('immeuble.id_immeuble'))
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))

    def __init__(self,nom,prenom,id_immeuble):
        self.nom=nom
        self.prenom = prenom
        self.id_immeuble=id_immeuble

class paiementLoyer(db.Model):
    __tablename__='paiementLoyer'
    id_paiement=db.Column(db.Integer, primary_key=True)
    id_immeuble = db.Column(db.Integer, ForeignKey('immeuble.id_immeuble'))
    id_appart=db.Column(db.Integer, ForeignKey('appartement.id_appart'))
    id_client=db.Column(db.Integer, ForeignKey('client.id_client'))
    Montant= db.Column(db.Float)
    date = Column(Date)
    payer = db.Column(db.String(3))


    def __init__(self, id_immeuble, id_appart, id_client,Montant, date, payer):
        self.id_immeuble = id_immeuble
        self.id_appart = id_appart
        self.id_client = id_client
        self.Montant=Montant
        self.date = date
        self.payer = payer


@app.route('/')
def index():
    return render_template('formulaireQuestion.html')

@app.route('/retour', methods=['GET'])
def retour():
    return render_template('Acceuil.html')

@app.route('/login', methods=['POST'])
def submit():
        nom = request.form['username']
        code = request.form['password']

        # Afficher les données dans la console
        print(f"nom: {nom}")
        print(f"password: {code}")

        if nom in users and users[nom] == code:
            return render_template('Acceuil.html')
        else:
            return "Nom d'utilisateur ou mot de passe incorrect"

@app.route('/ajouter_immeuble', methods=['GET', 'POST'])
def ajoutimmeuble():
    if request.method == 'POST':
        nom = request.form['nom']
        nomProprio = request.form['nomProprio']
        nbrEtage = request.form['nbrEtage']
        nbrAppart = request.form['nbrAppart']
        adresse = request.form['adresse']

        newImmeuble = immeuble(nom=nom, nomProprio=nomProprio, nbrEtage=nbrEtage, nbrAppart=nbrAppart, adresse=adresse)
        db.session.add(newImmeuble)
        db.session.commit()


        return render_template('Acceuil.html')
    else:
        return render_template('ajouterImmeuble.html')

@app.route('/AfficherImmeuble', methods=['GET', 'POST'])
def AfficherImmeuble():
    users = []

    if request.method == 'POST':
        nomProprio = request.form.get('nomProprio')
        if nomProprio:
            users = immeuble.query.filter_by(nomProprio=nomProprio).all()
        else:
            users = immeuble.query.all()
    else:
        users = immeuble.query.all()

    return render_template('afficherImmeubles.html', users=users)


@app.route('/modifier_immeuble', methods=['GET', 'POST'])
def modifier_immeuble():
    if request.method == 'POST':
        id_immeuble = request.form['id_immeuble']
        immeuble_obj = immeuble.query.get_or_404(id_immeuble)
        immeuble_obj.nom = request.form['nom']
        immeuble_obj.nomProprio = request.form['nomProprio']
        immeuble_obj.nbrEtage = int(request.form['nbrEtage'])
        immeuble_obj.nbrAppart = int(request.form['nbrAppart'])
        immeuble_obj.adresse = request.form['adresse']
        db.session.commit()
        return render_template('Acceuil.html')
    else:
        return render_template('modifierImmeuble.html')
@app.route('/supprimer_immeuble', methods=['GET', 'POST'])
def supprimer_immeuble():
    if request.method == 'POST':
        id_immeuble = request.form['id_immeuble']
        immeuble_obj = immeuble.query.get_or_404(id_immeuble)
        db.session.delete(immeuble_obj)
        db.session.commit()
        return render_template('Acceuil.html')
    else:
        return render_template('supprimerImmeuble.html')


@app.route('/ajouter_appartement', methods=['GET', 'POST'])
def ajouter_appartement():
    if request.method == 'POST':
        noAppart = request.form['noAppart']
        noEtage = int(request.form['noEtage'])  # Convertir en entier
        type = request.form['type']
        id_immeuble = int(request.form['id_immeuble'])  # Convertir en entier

        # Vérifier si l'id_immeuble existe
        immeuble_exist = immeuble.query.filter_by(id_immeuble=id_immeuble).first()

        if immeuble_exist:
            # Récupérer l'objet immeuble correspondant
            immeuble_obj = immeuble.query.filter_by(id_immeuble=id_immeuble).first()

            # Vérifier si le noEtage est valide par rapport à nbrEtage de l'immeuble
            if noEtage > immeuble_obj.nbrEtage:
                return "Erreur : Le numéro d'étage spécifié est supérieur au nombre d'étages de l'immeuble."

            # Tout est valide, ajouter l'appartement à la base de données
            newAppart = appartement(noAppart=noAppart, noEtage=noEtage, type=type, id_immeuble=id_immeuble)
            db.session.add(newAppart)
            db.session.commit()

            return render_template('Acceuil.html')
        else:
            return "Erreur : L'id de l'immeuble spécifié n'existe pas."

    else:
        return render_template('ajouterAppartement.html')

@app.route('/AfficherAppartement', methods=['GET', 'POST'])
def AfficherAppartement():
    immeubles = immeuble.query.all()
    appartements = []

    if request.method == 'POST':
        id_immeuble = request.form.get('id_immeuble')
        if id_immeuble:
            appartements = appartement.query.filter_by(id_immeuble=id_immeuble).all()
        else:
            appartements = appartement.query.all()
    else:
        appartements = appartement.query.all()

    return render_template('afficherAppartements.html', appartements=appartements, immeubles=immeubles)


@app.route('/modifier_appartement', methods=['GET', 'POST'])
def modifier_appartement():
    if request.method == 'POST':
        id_appart = request.form['id_appart']
        appartement_obj = appartement.query.get_or_404(id_appart)
        appartement_obj.noAppart = int(request.form['noAppart'])
        appartement_obj.noEtage = int(request.form['noEtage'])
        appartement_obj.type = request.form['type']
        db.session.commit()
        return render_template('Acceuil.html')
    else:
        return render_template('modifierAppartement.html')


@app.route('/supprimer_appartement', methods=['GET', 'POST'])
def supprimer_appartement():
    if request.method == 'POST':
        id_appart = request.form['id_appart']
        appartement_obj = appartement.query.get_or_404(id_appart)
        db.session.delete(appartement_obj)
        db.session.commit()
        return render_template('Acceuil.html')
    else:
        return render_template('supprimerAppartement.html')




@app.route('/Ajouter_Client', methods=['GET', 'POST'])
def Ajouter_Client():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        noAppart = int(request.form['noAppart'])  # Convertir en entier
        id_immeuble = int(request.form['id_immeuble'])  # Convertir en entier
        id_appart = int(request.form['id_appart'])  # Convertir en entier

        # Vérifier si l'id_immeuble existe
        immeuble_exist = immeuble.query.filter_by(id_immeuble=id_immeuble).first()

        if immeuble_exist:
            # Récupérer l'objet immeuble correspondant
            immeuble_obj = immeuble.query.filter_by(id_immeuble=id_immeuble).first()

            # Vérifier si l'id_appart existe
            appartement_exist = appartement.query.filter_by(id_appart=id_appart).first()

            if appartement_exist:
                # Récupérer l'objet appartement correspondant
                appartement_obj = appartement.query.filter_by(id_appart=id_appart).first()

                # Vérifier si le noAppart est valide par rapport à l'appartement
                if noAppart > appartement_obj.noAppart:
                    return "Erreur : Le numéro d'appartement spécifié est supérieur au nombre d'appartements."

                # Tout est valide, ajouter le client à la base de données
                newClient = client(nom=nom, prenom=prenom, noAppart=noAppart, id_immeuble=id_immeuble, id_appart=id_appart)
                db.session.add(newClient)
                db.session.commit()

                return render_template('Acceuil.html')
            else:
                return "Erreur : L'id de l'appartement spécifié n'existe pas."
        else:
            return "Erreur : L'id de l'immeuble spécifié n'existe pas."

    else:
        return render_template('ajouterClient.html')


@app.route('/AfficherClient', methods=['GET', 'POST'])
def AfficherClient():
    immeubles = immeuble.query.all()
    clients = []

    if request.method == 'POST':
        id_immeuble = request.form.get('id_immeuble')
        if id_immeuble:
            clients = client.query.filter_by(id_immeuble=id_immeuble).all()
        else:
            clients = client.query.all()
    else:
        clients = client.query.all()

    return render_template('afficherClients.html', clients=clients, immeubles=immeubles)


@app.route('/modifier_client', methods=['GET', 'POST'])
def modifier_client():
    if request.method == 'POST':
        id_client = request.form['id_client']
        client_obj = client.query.get_or_404(id_client)
        client_obj.nom = request.form['nom']
        client_obj.prenom = request.form['prenom']
        client_obj.noAppart = int(request.form['noAppart'])
        db.session.commit()
        return render_template('Acceuil.html')
    else:
        return render_template('modifierClient.html')


@app.route('/supprimer_client', methods=['GET', 'POST'])
def supprimer_client():
    if request.method == 'POST':
        id_client = request.form['id_client']
        client_obj = client.query.get_or_404(id_client)
        db.session.delete(client_obj)
        db.session.commit()
        return render_template('Acceuil.html')
    else:
        return render_template('supprimerClient.html')



@app.route('/ajouter_personnel', methods=['GET', 'POST'])
def ajouter_personnel():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        id_immeuble = int(request.form['id_immeuble'])

        immeuble_exist = immeuble.query.filter_by(id_immeuble=id_immeuble).first()

        if immeuble_exist:
            newPersonnel = personnel(nom=nom, prenom=prenom, id_immeuble=id_immeuble)
            db.session.add(newPersonnel)
            db.session.commit()

            return render_template('Acceuil.html')
        else:
            return "Erreur : L'id de l'immeuble spécifié n'existe pas."
    else:
        return render_template('ajouter_personnel.html')

@app.route('/afficher_personnel', methods=['GET', 'POST'])
def afficher_personnel():
    immeubles = immeuble.query.all()
    personnels = []

    if request.method == 'POST':
        id_immeuble = request.form.get('id_immeuble')
        if id_immeuble:
            personnels = personnel.query.filter_by(id_immeuble=id_immeuble).all()
        else:
            personnels = personnel.query.all()
    else:
        personnels = personnel.query.all()

    return render_template('afficher_personnel.html', personnels=personnels, immeubles=immeubles)

@app.route('/modifier_personnel', methods=['GET', 'POST'])
def modifier_personnel():
    if request.method == 'POST':
        id_personnel = request.form['id_personnel']
        personnel_obj = personnel.query.get_or_404(id_personnel)
        personnel_obj.nom = request.form['nom']
        personnel_obj.prenom = request.form['prenom']
        db.session.commit()
        return render_template('Acceuil.html')
    else:
        return render_template('modifier_personnel.html')

@app.route('/supprimer_personnel', methods=['GET', 'POST'])
def supprimer_personnel():
    if request.method == 'POST':
        id_personnel = request.form['id_personnel']
        personnel_obj = personnel.query.get_or_404(id_personnel)
        db.session.delete(personnel_obj)
        db.session.commit()
        return render_template('Acceuil.html')
    else:
        return render_template('supprimer_Personnel.html')

@app.route('/ajouter_paiement', methods=['GET', 'POST'])
def ajouter_paiement():
    if request.method == 'POST':
        id_immeuble = request.form['id_immeuble']
        id_appart = request.form['id_appart']
        id_client = request.form['id_client']
        Montant = request.form['Montant']
        date = request.form['date']
        payer = request.form['payer']

        newPaiement = paiementLoyer(id_immeuble=id_immeuble, id_appart=id_appart, id_client=id_client, Montant=Montant, date=date, payer=payer)
        db.session.add(newPaiement)
        db.session.commit()

        return render_template('Acceuil.html')
    else:
        return render_template('ajouterPaiement.html')

@app.route('/afficher_paiements', methods=['GET', 'POST'])
def afficher_paiements():
    paiements = []
    clients = client.query.all()  # Assurez-vous de récupérer les clients

    if request.method == 'POST':
        id_immeuble = request.form.get('id_immeuble')
        id_client = request.form.get('client')
        date = request.form.get('date')

        query = paiementLoyer.query

        if id_immeuble:
            query = query.filter_by(id_immeuble=id_immeuble)
        if id_client:
            query = query.filter_by(id_client=id_client)
        if date:
            query = query.filter_by(date=date)

        paiements = query.all()
    else:
        paiements = paiementLoyer.query.all()

    return render_template('afficherPaiements.html', paiements=paiements, clients=clients)


@app.route('/modifier_paiement', methods=['GET', 'POST'])
def modifier_paiement():
    if request.method == 'POST':
        id_paiement = request.form['id_paiement']
        paiement_obj = paiementLoyer.query.get_or_404(id_paiement)
        paiement_obj.id_immeuble = request.form['id_immeuble']
        paiement_obj.id_appart = request.form['id_appart']
        paiement_obj.id_client = request.form['id_client']
        paiement_obj.Montant = request.form['Montant']
        paiement_obj.date = request.form['date']
        paiement_obj.payer = request.form['payer']
        db.session.commit()
        return render_template('Acceuil.html')
    else:
        return render_template('modifierPaiement.html')

@app.route('/supprimer_paiement', methods=['GET', 'POST'])
def supprimer_paiement():
    if request.method == 'POST':
        id_paiement = request.form['id_paiement']
        paiement_obj = paiementLoyer.query.get_or_404(id_paiement)
        db.session.delete(paiement_obj)
        db.session.commit()
        return render_template('Acceuil.html')
    else:
        return render_template('supprimerPaiement.html')


if __name__ == '__main__':
    with app.app_context():
        # Créer toutes les tables définies dans les modèles SQLAlchemy
        db.create_all()

    app.run(host='0.0.0.0', port=5000)

