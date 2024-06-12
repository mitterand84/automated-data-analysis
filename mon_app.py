from flask import Flask, render_template, request, redirect, url_for, session
import os
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/xlsx'
app.secret_key = "8766dd518c48f5b4bda2d338d6fb8e06d2290048144a6037344d752be8ffd24c"

# Configuration de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'kollomitter@gmail.com'
app.config['MAIL_PASSWORD'] = 'xpbgqpllotwkuiyr'
app.config['MAIL_DEFAULT_SENDER'] = 'kollomitter@gmail.com'

mail = Mail(app)

# Créer les dossiers si nécessaire
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists('static/pdf'):
    os.makedirs('static/pdf')

@app.route("/")
def index():
    return render_template("index.html")

utilisateurs = [
    {"nom": "admin", "mdp": "admin"},
    {"nom": "kollo", "mdp": "groupe2"},
    {"nom": "kotue", "mdp": "groupe2"},
    {"nom": "guiche", "mdp": "groupe2"},
    {"nom": "essong", "mdp": "groupe2"}
]

@app.route("/create_account", methods=["POST", "GET"])

def create_account():
    if request.method == "POST":
        donnees = request.form
        nom = donnees.get('nom')
        mdp = donnees.get('mdp')

        if recherche_utilisateur(nom, mdp) is None:
            utilisateurs.append({"nom": nom, "mdp": mdp})
            session['nom_utilisateur'] = nom
            return redirect(url_for('index'))
        else:
            return redirect(request.url)
    else:
        return render_template("create_account.html")

def recherche_utilisateur(nom_utilisateur, mot_de_passe):
    for utilisateur in utilisateurs:
        if utilisateur['nom'] == nom_utilisateur and utilisateur['mdp'] == mot_de_passe:
            return utilisateur
    return None

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        donnees = request.form
        nom = donnees.get('nom')
        mdp = donnees.get('mdp')

        utilisateur = recherche_utilisateur(nom, mdp)

        if utilisateur is not None:
            print("utilisateur trouvé")
            session['nom_utilisateur'] = utilisateur['nom']
            print(session)
            return redirect(url_for('index'))
        else:
            print("utilisateur inconnu")
            return redirect(request.url)
    else:
        print(session)
        if 'nom_utilisateur' in session:
            return redirect(url_for('index'))
        return render_template("login.html")

@app.route('/logout')
def logout():
    print(session)
    session.pop('nom_utilisateur', None)
    print(session)
    return redirect(url_for('login'))

@app.route("/compteur")
def compteur():
    if "compteur" not in session:
        session['compteur'] = 1
    else:
        session['compteur'] = session['compteur'] + 1
    print(session)
    nb_visites = session['compteur']
    return f"Vous avez visité cette page {nb_visites} fois"


@app.route("/traitement", methods=["POST", "GET"])
def traitement():
    if request.method == "POST":
        donnees = request.form
        nom = donnees.get('nom')
        mdp = donnees.get('mdp')
        if nom == 'admin' and mdp == '1234':
            return render_template("traitement.html", nom_utilisateur=nom)
        else:
            return render_template("traitement.html")
    else:
        return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_excel():
    excel_file = request.files['excel_file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_file.filename)
    excel_file.save(file_path)
    emails = request.form['emails'].split(',')
    attachments = request.files.getlist("attachments")
    try:
        df = pd.read_excel(file_path)

        # Vérification des colonnes nécessaires
        required_columns = ['Network', 'Status', 'Originator', 'Amount', 'Actual Amount']
        for col in required_columns:
            if col not in df.columns:
                return render_template('index.html', error=f"Colonne manquante : {col}")

        # Analyse des données
        decompte_des_reseaux = df['Network'].value_counts()
        decompte_des_status = df['Status'].value_counts()
        originator_amounts = df.groupby('Originator')['Amount'].sum()
        df['Fees'] = df['Amount'] - df['Actual Amount']
        originator_fees = df.groupby('Originator')['Fees'].sum()
        failed_transactions = df[df['Status'] == 'Failed']
        failed_counts = failed_transactions['Originator'].value_counts()

        # Générer les graphiques seulement si les données existent
        if not decompte_des_reseaux.empty:
            plt.figure(figsize=(10, 10))
            patches, texts, autotexts = plt.pie(decompte_des_reseaux, labels=decompte_des_reseaux.index, autopct='%1.1f%%', startangle=140)
            for text in autotexts:
                text.set_color('red')
            for text in texts:
                text.set_fontsize(14)
            plt.title('Répartition des transactions par réseau', fontsize=15, fontweight='bold')
            plt.savefig('static/pdf/Distribution_par_reseau_cammabert.png')
            plt.close()

        if not decompte_des_status.empty:
            plt.figure(figsize=(10, 10))
            patches, texts, autotexts = plt.pie(decompte_des_status, labels=decompte_des_status.index, autopct='%1.1f%%', startangle=140)
            for text in autotexts:
                text.set_color('red')
            for text in texts:
                text.set_fontsize(14)
            plt.title('Répartition des statuts des transactions', fontsize=15, fontweight='bold')
            plt.savefig('static/pdf/Distribution_des_statuts_cammabert.png')
            plt.close()

        if not originator_amounts.empty:
            plt.figure(figsize=(10, 6))
            originator_amounts.plot(kind='bar', color='skyblue')
            plt.title('Montants des transactions par origine')
            plt.xlabel('Origine')
            plt.ylabel('Montant')
            plt.savefig('static/pdf/Montants_par_origine.png')
            plt.close()

        if not originator_fees.empty:
            plt.figure(figsize=(10, 6))
            originator_fees.plot(kind='bar', color='orange')
            plt.title('Frais par origine')
            plt.xlabel('Origine')
            plt.ylabel('Frais')
            plt.savefig('static/pdf/Frais_par_origine.png')
            plt.close()

        if not failed_counts.empty:
            plt.figure(figsize=(10, 6))
            failed_counts.plot(kind='bar', color='red')
            plt.title('Échecs de transactions par origine')
            plt.xlabel('Origine')
            plt.ylabel('Nombre d\'échecs')
            plt.savefig('static/pdf/Echecs_par_origine.png')
            plt.close()

        # Création du fichier PDF
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 12)
                self.cell(0, 10, 'Rapport de l\'analyse des données de transactions', 0, 1, 'C')

            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

            def chapter_title(self, title):
                self.set_font('Arial', 'B', 12)
                self.cell(0, 10, title, 0, 1, 'L')
                self.ln(5)

            def chapter_body(self, body):
                self.set_font('Arial', '', 12)
                self.multi_cell(0, 10, body)
                self.ln()

            def add_image(self, image_path):
                self.image(image_path, w=150)
                self.ln()

        pdf = PDF()
        pdf.add_page()

        if not decompte_des_reseaux.empty:
            pdf.chapter_title('Répartition des transactions par réseau')
            pdf.add_image('static/pdf/Distribution_par_reseau_cammabert.png')
            pdf.chapter_body(decompte_des_reseaux.to_string())

        if not decompte_des_status.empty:
            pdf.chapter_title('Répartition des statuts des transactions')
            pdf.add_image('static/pdf/Distribution_des_statuts_cammabert.png')
            pdf.chapter_body(decompte_des_status.to_string())

        if not originator_amounts.empty:
            pdf.chapter_title('Montants des transactions par origine')
            pdf.add_image('static/pdf/Montants_par_origine.png')
            pdf.chapter_body(originator_amounts.to_string())

        if not originator_fees.empty:
            pdf.chapter_title('Frais par origine')
            pdf.add_image('static/pdf/Frais_par_origine.png')
            pdf.chapter_body(originator_fees.to_string())

        if not failed_counts.empty:
            pdf.chapter_title('Échecs de transactions par origine')
            pdf.add_image('static/pdf/Echecs_par_origine.png')
            pdf.chapter_body(failed_counts.to_string())

        pdf_output_path = os.path.join('static/pdf', 'rapport_analyse.pdf')
        pdf.output(pdf_output_path)

        # Envoi du fichier PDF par email
        try:
            with app.app_context():
                for email in emails:
                    email = email.strip()
                    if email:
                        msg = Message("Rapport d'analyse des transactions", recipients=[email])
                        msg.body = "Veuillez trouver ci-joint le rapport d'analyse des transactions."
                        with app.open_resource(pdf_output_path) as fp:
                            msg.attach("rapport_analyse.pdf", "application/pdf", fp.read())
                        for attachment in attachments:
                            if attachment:
                                attachment_path = os.path.join(app.config['UPLOAD_FOLDER'], attachment.filename)
                                attachment.save(attachment_path)
                                with app.open_resource(attachment_path) as fp:
                                    msg.attach(attachment.filename, attachment.content_type, fp.read())
                        mail.send(msg)
        except Exception as e:
            return render_template('index.html', error=f"Erreur lors de l'envoi de l'email : {e}")

        return render_template('index.html', pdf_url=pdf_output_path)

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)