# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""





import classes as func
import fonctions as stp
import random
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for
UPLOAD_FOLDER = "C:/Users/arizz/Documents/Master/python/alex/static/uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def connect_database(database_path):
    return sqlite3.connect(database_path)

@app.route("/")
def default():
    return redirect("index")

@app.route("/hi")
def greeting():
    return "Hello world"

@app.route("/hello")
def hello():
    return render_template("test.html")

@app.route("/connexion")
def connexion():
    # filename to form database 
    return "On test"
   
    
    #return render_template("connected.html")

@app.route("/form", methods=['GET', 'POST'])
def formulaire():
    if request.method=="POST":
        username=request.form["pseudo"]
        password=request.form["pass"]
        if username == "alex" and password== "alex":
            return redirect(url_for("connexion"))
    return render_template("login.html")




@app.route("/index")
def index():
    return render_template("index.html")



#page qui montre toutes les prisons
@app.route("/Touteslesprisons")
def Touteslesprisons():
    prisons=func.Prison.getAllPrisons()
    return render_template("Touteslesprisons.html",prisons=prisons)

#page d'information sur prisonnier
@app.route("/ConsultPrisonner", methods=['GET','POST'])
def ConsultPrisonner():
    if request.method=="GET":
        id_prisonnier=request.args.get('id', default="", type=str)
        prisonner=func.Prisonnier.getPrisonner(id_prisonnier)
        peine=func.Peine.getPeineFromUserID(id_prisonnier)
        print('Limage est'+str(prisonner.image))
        return render_template("prisonnerInformation.html", id_prisonnier=id_prisonnier,prisonner=prisonner, peine=peine )

    

@app.route("/Touslesprisonniers", methods=['GET', 'POST'])
def Touslesprisonniers():
    
    #Pour le résultat du filtre
    if request.method=="GET":
        prisons=func.Prison.getAllPrisons()
         
        nom_ville=request.args.get('prisonFilter', default="", type=str)
        #return nom_ville
        if(nom_ville != ""):
         #   return nom_ville
            filteredPrisonners=func.Prisonnier.getPrisonnersFilteredByPrison(nom_ville)
            #print(vars(filteredPrisonners))
            return render_template("Touslesprisonniers.html", prisonniers=filteredPrisonners, prisons=prisons)
        else:

            #prisons=func.Prison.getAllPrisons()

            prisonniers=func.Prisonnier.getAllPrisonners()

            return render_template("Touslesprisonniers.html", prisonniers=prisonniers, prisons=prisons)



#ajouter un prisonnier depuis un formulaire:
@app.route("/ajoutPrisonnier", methods=['GET', 'POST'])
def ajoutPrisonnier():
    if request.method == "POST":
        prenom = request.form['prenom']
        nom = request.form['nom']
        birthday=request.form['birthday']
        type_de_peine = request.form['type_de_peine']
        collaborateur = bool(request.form.get('collaborateur', False))
        prison_id = int(request.form['prison_id'])
        ##On ajoute l'image
        print(request.files)
        nombre=random.randint(0,4684113)
            # Obtient le fichier téléchargé depuis la requête
        uploaded_img = request.files['file']

            # Vérifie si le nom du fichier est valide (évite les injections)
        if uploaded_img.filename != '':
                # Déplace le fichier téléchargé dans le dossier UPLOAD_FOLDER
            img_filename = os.path.join(app.config['UPLOAD_FOLDER'], f"{nombre}.jpg")
            uploaded_img.save(img_filename)
        prisonnier = func.Prisonnier(prenom, nom, birthday, type_de_peine, collaborateur, prison_id, nombre)
        
        prisonnier.ajoute_prisonnier()

        #func.ajoute_prisonnier( prenom, nom, type_de_peine, collaborateur, prison_id)

    return render_template("AjoutPrisonnier.html")


app.run(debug=True)