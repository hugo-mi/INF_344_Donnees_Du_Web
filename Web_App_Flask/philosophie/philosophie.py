#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash
from getpage import getPage

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', message="Bienvenue sur le jeu Tous les chemins mènent à la philosophie")

# Si vous définissez de nouvelles routes, faites-le ici

# Question 3 et Question 9
@app.route('/new-game', methods=['POST'])
def new_game():
    '''
    DESCRIPTION
        Initialise la partie de jeu
    RETOURNE
        Retourne la page "/game" qui contient les règles du jeu de la partie
    '''
    
    # Récupération du titre de la page entrée dans la formulaire du template "index.html" pour le lancement de la partie
    titre_page = request.form["start"]
    session['article'] = titre_page
    
    # Initialisation du score au lancement de la partie
    session['score'] = 0
    
    return redirect('/game')

# Question 4 et Question 5
@app.route('/game', methods=['GET'])
def game():
    '''
    DESCRIPTION
        Déroulement de la partie de jeu (Moteur de jeu)
    RETOURNE
        Le template de la page "/game.html" qui est l'interface du jeu
    '''
    
    # Recupération du titre de page entré par l'utilisateur dans le formulaire
    titre_page = session['article']
    
    # Récupération de la page à afficher
    session['title'], session['content_html'] = getPage(titre_page)
    
    # Si la page saisie par l'utilisateur dès le début de la partie n'existe pas
    # alors on informe l'utilisateur que la page est introuvable et qu'il doit retenter sa chance
    if (session['title'] is None) and (session["score"] == 0):
        flash("Dommage, c'est perdu !", "flash_box_error")
        flash("La page demandée est introuvable", "flash_box_warning")
        flash("Votre score est : " + str(session['score']), "flash_box_info")
        flash("Retentez votre chance en saisissant une page qui existe vraiment !")
        return redirect('/')
    
    # Si la page choisie par l'utilisateur ne contient aucun lien 
    # alors on l'informe qu'il vient de perdre
    if len(session['content_html']) == 0:
        flash("Dommage, c'est perdu !", "flash_box_error")
        flash("La page demandée ne contient aucun lien URL", "flash_box_warning")
        flash("Votre score est : " + str(session['score']), "flash_box_info")
        flash("Retentez votre chance !")
        return redirect('/')
    
    # Si l'utilisateur choisi de saisir la page Philosophie dès le début du jeu 
    # alors on informe l'utilisateur qu'il enfreint les règles et qu'il vient de perdre la partie
    if (session["title"] == "Philosophie") and (session["score"] == 0):
        flash("Dommage, c'est perdu ! Vous avez enfreint les règles du jeu !", "flash_box_error")
        flash("Vous ne pouvez pas accéder dès le début à la page *Philosophie*", "flash_box_warning")
        flash("Votre score est : " + str(session['score']), "flash_box_info")
        flash("Retentez votre chance en saisissant une autre page que la page *Philosophie* !")
        return redirect('/')        

    
    return render_template("game.html")

# Question 7 et Question 8 et Question 9
@app.route('/move', methods=['POST'])
def move():
    """
    DESCRIPTION
        récupère la page où l'utilisateur souhaite 
        se rendre et redirige vers cette page en y affichant
        les liens internes valides de cette dernière
    RETOURNE
        La page de destination avec ses liens internes valides

    """
    # Récupération du titre de la page de destination entrée par l'utilisateur
    titre_page = request.form["destination"]
    session['article'] = titre_page
    
    # On incrémente le score à chaque changement de page
    session['score'] = session['score'] + 1
    
    # Victoire : Affichage d'une notification dès que la page "Philosophie" est atteinte
    if titre_page == "Philosophie":
        flash("C'est gagné ! Vous avez atteint la page page *Philosophie*", "flash_box_succes")
        flash("Votre score est : " + str(session['score']), "flash_box_info")
        return redirect("/")
    
    # On vérifie que l'utilisateur entre bien un URL valide parmis les différentes URL possible qui lui sont utilisés
    # L'idée est de bloquer l'utilisateur si ce dernier tente de tricher en jouant sur plusieurs onglets 
    # ou en soumettant manuellement des requêtes POST pour dont les entrées sont impossibles (pas contenu dans la liste des liens proposés).
    if (titre_page not in session['content_html']):
        flash("Dommage, c'est perdu !", "flash_box_error")
        flash("Votre score est : " + str(session['score']), "flash_box_info")
        flash("Vous essayez de tricher. Soit en jouant sur plusieurs onglets, soit en envoyant des requêtes POST non permises", 'flash_box_warning')
        flash("Ne tentez plus de tricher à la prochaine partie", 'flash_box_warning')
        flash("Retentez votre chance")
        return redirect('/') 
    
    return redirect('/game')

if __name__ == '__main__':
    app.run(debug=True)

