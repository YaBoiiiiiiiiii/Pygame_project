#Note#
#Cette partie gere les logiques du jeu , le gros bout du code se trouvera ici.
#Ne s'occupe que des actions DANS le jeu (donc ne s'occupe pas des systemes de sauvegarde et des graphiques, ainsi que les menus.)
#Ici sera traite : Les classes entite, control, joueur

# Information suplementaire :
# - Les enemies vivants ignorent les rebords , sauf ceux des cartes 

import fichier


import numpy as np
import random


#-------------------#
#-Fonction generale-#
#-------------------#

def detect_active_entite(e): #Renvoie les entites se trouvant sur la meme carte que le joueur , renvoie une list de Active_entite.
    control = e 
    active = control.player.coord.macro
    entite = control.entite
    res = []
    for e in entite : 
        if (e.macro.x == active.x  and e.macro.y == active.y) or ( e.base.espece == 2 and e.pv < 666 ): 
            res.append(e) 

    return res 

#-----------#
#-Coordonne-#
#-----------#

class Coordonne() : 
    def __init__(self,x,y,macrox = None , macroy = None) : 
        self.x     = x
        self.y     = y
        if macrox != None : #On a juste besoin d'en verifier une seule; si une seule est fausse alors l'autre est aussi forcement fausse. 
            self.macro = Coordonne(macrox , macroy)
        else : 
            self.macro = None 

#-------#
#-Carte-#
#-------#

class Carte() : 
    def __init__(self , carte ): #carte = numpy array 
        self.carte         = carte #list, matrice 2 dimensionels, chaque case represente une carte. Chaque carte contient les coordonnees, puis dimensions des cubes qui servent de bloc dans la carte.
        macrox , macroy  = len(carte)-1 , len(carte[0])-1
        self.macro = Coordonne(macrox , macroy) 
        
                
#--------#
#-Joueur-#
#--------#

def toucher(cible,souris) : #joueur : Joueur() , cible : Active_entite , souris_x : int , souris_y : int . Fonction qui trace une droite joueur-curseur et voit si la cible s'y trouve dessus.
    if cible.coord.x <= souris.x + 75 and cible.coord.x >= souris.x - 75 and cible.coord.y <= souris.y + 75 and cible.coord.y >= souris.y - 75 :
       return True 
    return False 

def detect_block_en_dessous(e) :
    control = e
    active = control.map.carte[control.player.coord.macro.x ][ control.player.coord.macro.y]
    for e in active : #navigue a travers les blocs 
        if e[1] - control.player.coord.y < 50 and control.player.coord.y < e[1] and control.player.coord.x < e[0] + e[2] and control.player.coord.x > e[0] : #Hauteur standard d'un block : 20 ; 
            return True
    return False

def detect_block_en_dessous_aggressive(e) : #Meme principe que le dernier mais detecte les blocs encore plus bas , donc plus "aggressive"
    control = e
    active = control.map.carte[control.player.coord.macro.x ][ control.player.coord.macro.y]
    for e in active : #navigue a travers les blocs 
        if e[1] - control.player.coord.y < 80 and control.player.coord.y < e[1] and control.player.coord.x < e[0] + e[2] and control.player.coord.x > e[0] : #Hauteur standard d'un block : 20 ; 
            return True
    return False

def detect_block_en_dessous_aggressive_ultra(e) : #Encore plus aggressive que le dernier 
    control = e
    active = control.map.carte[control.player.coord.macro.x ][ control.player.coord.macro.y]
    for e in active : #navigue a travers les blocs 
        if e[1] - control.player.coord.y < 250 and control.player.coord.y < e[1] and control.player.coord.x < e[0] + e[2] and control.player.coord.x > e[0] : #Hauteur standard d'un block : 20 ; 
            return True
    return False   

def detect_block_droite(e):
    control = e
    active = control.map.carte[control.player.coord.macro.x ][control.player.coord.macro.y]
    for e in active : #navigue a travers les blocs 
        resultat = e[0] - control.player.coord.x
        if resultat < 50 and resultat > 0 and control.player.coord.y < e[1] + e[3] and control.player.coord.y > e[1] : 
            return True
    return False

def detect_block_gauche(e): #Detecte si il y a un mur vers la direction ou on se dirige
    control = e
    active = control.map.carte[control.player.coord.macro.x ][ control.player.coord.macro.y]
    for e in active : #navigue a travers les blocs 
        resultat = control.player.coord.x - (e[0] + e[2])
        if resultat < 50 and resultat > 0 and control.player.coord.y < e[1] + e[3] and control.player.coord.y > e[1] : 
            return True
    return False 

class Joueur() : 
    def __init__(self , coord , pv = 100 , time = False ) : #Entite speciale controle par le joueur ; coord est delivre sous forme (x,y)
        self.coord     = Coordonne(coord[0],coord[1],coord[2],coord[3]) #macro est un int : designe la position du joueur sur la macromap.
        self.pv        = pv
        self.speed     = 20
        self.jump = 0 #Permet de calculer la distance de saut : A chaque saut on incremente de 20, pour jump>0 on continue a ascendre, en soustrayant 1 a chaque frame. Sinon on descend
        self.time      = False  #Les bonuses de vitesses octrues par les entites non-intelligente sont temporaires : time mesure ce temps. #1sec = 30 alors 10sec = 300
    
    def check_carte (self,control) : 
        if self.coord.x > 1600 : 
            if self.coord.macro.x < control.map.macro.x : 
                self.coord.x = 1 
                self.coord.macro.x += 1 
            else : 
                self.coord.x = 1599 
        elif self.coord.x < 0 : 
            if self.coord.macro.x > 0 :
                self.coord.x = 1599 
                self.coord.macro.x -= 1 
            else : 
                self.coord.x = 1
        if self.coord.y < 0 :
            if self.coord.macro.y > 0 : 
                self.coord.y = 899
                self.coord.macro.y -= 1
        elif self.coord.y > 900 :
            if self.coord.macro.y < control.map.macro.y : 
                self.coord.y = 1
                self.coord.macro.y += 1
            else : 
                self.pv = 0 
        

    def mouvement(self, ui,control) :
        if ui == "MOVEUP"  : #bouger en haut 
            if self.jump == 0 and detect_block_en_dessous(control) : #on peut sauter
                self.jump = 19
                self.coord.y -= 23 

        elif ui == "MOVELEFT" : #bouger a gauche  
            if detect_block_gauche(control) == False :
                self.coord.x -= self.speed

        elif ui == "MOVERIGHT" : #bouger a droite
            if detect_block_droite(control) == False : 
                self.coord.x += self.speed 
    
    def momentum(self,e ) :
        detection = detect_block_en_dessous(e)
        if self.jump == False and detection == False : #On devrait normalement donc tomber.
            self.coord.y += 23 
        elif self.jump > 0 : 
            self.coord.y -= 23
            self.jump -= 1 
    
    def tirer(self, souris,scan) : #Fonction pour voir si le joueur a frappe une entite , scan = list d'Active entite , donne les donnees des entites qui se trouvent dans la meme carte que le joueur  
        res = []
        #detecte les entites se trouvant sur la meme carte que le joueur (car le joueur ne peux que taper les entites dans la meme carte)
        for cible in scan : 
            if  toucher(cible,souris) == True : #Verifie si on touche une entite avec le tir
                res.append((cible , 3))  #Cible obj:Active_entite , Degat int (30 fps => 60 degats par seconde)
        return res

    def timer_vitesse(self):
        if self.time > 0 : 
            self.speed = 60
            self.time -=1 
        else : 
            self.speed = 20
#--------#
#-Entite-#
#--------#

def detect_regard(entite , e) : #Renvoie les coordonnees du joueur si il est a porte de vue d'un monstre
    control = e
    joueur = control.player.coord
    if abs(entite.coord.x - joueur.x) < 1100 and abs(entite.coord.y - joueur.y) < 700 : 
        return joueur.x , joueur.y
    return False

def detect_regard_speciale(entite , e) : #Renvoie les coordonnees du joueur si il est a porte de vue d'un monstre
    control = e
    joueur = control.player.coord
    if abs(entite.coord.y - joueur.y) < 900 and abs(entite.coord.x - joueur.x)<100 : 
        return joueur.x , joueur.y
    return False

def detect_contact(zone , e) : #Renvoie si le joueur se trouve dans la zone de contact d'une entite
    control = e 
    joueur = control.player.coord
    if joueur.x < zone.coord.x + zone.base.aoe.x and joueur.x > - zone.base.aoe.x + zone.coord.x and joueur.y < zone.coord.y + zone.base.aoe.y and joueur.y > zone.coord.y - zone.base.aoe.y : 
        return True 
    return False

def suggest_detect_bord_x(pos , arg) : #Lorsqu'une entite se deplace, cette fonction s'assure qu'elle depasse pas les bordures des cartes, seulement sur les abscisse
    if pos + arg >= 1600 :  #pos : int coordonne sur l'axe x de l'entite  ;  arg : int donne la vitesse de l'entite en pixel/(100/30)secondes
        return (pos - arg*3)
    elif pos - arg <= 0 : 
        return (pos + arg*3)
    else : 
        return random.randint(pos-arg , pos + arg)

def suggest_detect_bord_y(pos , arg) : #Meme chose mais cette fois sur les ordonnees 
    if pos + arg >= 900 : 
        return (pos - arg*3)
    elif pos - arg <= 0 : 
        return (pos + arg*3)
    else : 
        return random.randint(pos-arg , pos + arg)

def speciale_escalade ( entite , control ) : #Permet une entite d'escalader pour atteindre le joueur  
    bloc_active = control.map.carte[entite.macro.x][entite.macro.y] 

    candidat_bloc = [ ] 

    for candidat in bloc_active : 
        if candidat[1] + candidat[3] > entite.coord.y - entite.base.aoe.y * 3 : 
            candidat_bloc.append(candidat) 

    for pres_du_joueur in candidat_bloc :
        operation_y = pres_du_joueur[1] - control.player.coord.y
        operation_x = pres_du_joueur[0] - control.player.coord.x   

        if operation_y < 460 and operation_y > 0 and operation_x < 230   : 
            candidat_bloc.pop( 0 )


    if len(candidat_bloc) == 0 : 
        return False

    maxi = candidat_bloc[0] 
    operation = ( maxi[0] + maxi[2] /2 ) - entite.coord.x

    for candidat in candidat_bloc : 
        if abs(( candidat[0] + candidat[2] /2 ) - entite.coord.x) < abs(operation) :
            maxi = candidat 

    if operation < -35 : 
        x = -35
    elif operation > 35 : 
        x = 35
    else : 
        x = operation 
    y = -8


    return x , y

def glissement(entite, i) : #entite , obj Active_entite : l'entite en question  ; i , int : detect_regard(self,e)
    x = i[0] - entite.coord.x 
    y = entite.coord.y - i[1]

    if x > 7  : #si le joueur est plus loins que 20 pixels : bouge pas plus de 20. 
        x = 7
    elif x < -7 : 
        x = -7

    if y > 7  : 
        y = - 7 
    elif y < -7 : 
        y = 7 

    return x , y 

def charge (entite , i) : #i , int : detect_regard(self,e)
    x = i[0] - entite.coord.x
    y = entite.coord.y - i[1] 

    if x < -16 : 
        x = -16
    elif x > 16 : 
        x = 16
    if y < 0 : 
        y = 20 
    else : 
        y = entite.coord.y
    
    return x , y

def charge_speciale(entite , i , e) : 

    x = i[0] 
    y = i[1] 

    entite_zone = entite.base.aoe  
    if y < entite.coord.y  : #Si le joueur se trouve en haut par rapport a l'entite 
        if  (entite.coord.y - 3.5*entite.base.aoe.y > y  or detect_block_en_dessous_aggressive_ultra(e)) and ( entite.coord.y - entite.base.aoe.y > y and detect_block_en_dessous_aggressive(e)): #Si le joueur se trouve TROP haut pour l'entite et que le joueur va se trouve sur un bloc : L'entite va s'apercevoir quil ne va pas l'attraper comme ca et va donc chercher une route alternative
            res = speciale_escalade( entite , e) 
            if res != False : 
                x = res[0] 
                y = res[1]
            else : 
                return False
        else : #Sinon, si le joueur est en l'air mais qu'il n'a pas de bloc sous lui : L'entite va s'apercevoir qu'il n'aura qu'a se mettre sous lui pour l'attraper.
            distance = x - entite.coord.x 
            if distance  < -35  : 
                x = -35 
            elif distance  > 35 : 
                x = 35
            else : 
                x = distance 
            y = 0
          
    elif y >= entite.coord.y  :  # Si l'entite se trouve en haut par rapport au joueur 
        y = 40

        if x - entite.coord. x< -35 : 
           x = -35 
        elif x - entite.coord.y  > 35 : 
           x = 35  

    return x , y

class Base_Entite() :  #Permet de definir les proprietes immutables des entites. 
    def __init__(self , animate  , interaction ,aoex , aoey , espece = None ) : 
        self.anime = bool(animate) #0 : Non c'est une entite non intelligente , 1: Oui, elle possede une intelligence
        self.espece = espece # 0 : Enemie flottant , 1: Enemie pietaille  , 2 : speciale ; utile seulement si c'est anime.
        self.interaction = interaction # Quelle evenement se produit sur contact ?
        self.aoe = Coordonne(aoex , aoey) #Zonne d'effet de interaction, X:Y


class Active_Entite() : #Permet de placer les entites avec leurs proprietes de base dans le jeu ; les coordonnees ou les points de vie des entites varient ,donc elles ne peuvent etres fixes
    def __init__(self , base , x , y , macrox , macroy , texture , pv) : 
        self.base = base #Designe la classe Entite_base
        self.coord = Coordonne(x,y)
        self.macro = Coordonne(macrox , macroy) #Position de l'entite sur la carte macro
        self.pv = pv 
        self.texture = texture #str ; texture de l'entite. 

    def mouvement (self,e): # Fait deplacer les entites de maniere autonome 
        if self.base.anime == False : 
            pass
        if self.base.espece != 2 : 
            i = detect_regard(self , e) 
        else : 
            if self.pv > 665 : 
                i = detect_regard_speciale(self , e) 
                if i != False : 
                    self.pv = 665
            else : 
                joueur = e.player.coord 
                i = joueur.x , joueur.y

        if i == False and self.base.espece != 2 : #Si le monstre detecte pas le joueur et n'est pas un chasseur : bouge aleatoirement
            if self.base.espece : #Entite a pied
                self.coord.x = suggest_detect_bord_x(self.coord.x, 30)  
            else : 
                self.coord.x = suggest_detect_bord_x(self.coord.x,10)
                self.coord.y = suggest_detect_bord_y(self.coord.y,10)
        elif self.base.espece == 2 and i == False : 
            pass
        else : #Si l'entite detecte le joueur 
            if self.base.espece == 1 : 
                res = charge (self , i)
                self.coord.x += res[0]  
                self.coord.y += res[1]
            elif self.base.espece == 0  : 
                res= glissement(self , i)
                self.coord.x += res[0] 
                self.coord.y += res[1]
            else : 
                res = charge_speciale (self , i , e) 
                if res != False : 
                    self.coord.x += res[0] 
                    self.coord.y += res[1]


    def interaction(self,e) : #Retourne des resultats qui affecterons le joueur. Si il est dans la zone d'effet de l'entite. 
        if detect_contact(self,e) : 
            return (self.base.interaction)
        return None


#---------#
#-Control-#
#---------#


class Control() : 
    def __init__ ( self , coord , entite , map_  , niveau , hp = 100 , time = 0 ) :       
        self.task      = [] #Pile qui suit les commandes a effectues, les commandes lance par le joueur lorsqu'il frappe sur une touche
        self.mouse     = Coordonne ( 0 , 0 )  #Suit la position de la souris.

        self.map       = Carte(map_)  #numpy array , type int : Carte contenant des plus petites cartes, chacune de longueur 1600*900 pixels
        self.player    = Joueur(coord, hp , time ) # coord : x , y , macrox , macroy
        self.entite    = entite     #liste de Active_entite :Contient les entites 
        self.fire      = False      #Indique si le joueur est en train de tirer, ne sert qu'a l'animation et au bruitage 
        self.niveau    = niveau #Traque le niveau actuel

    def inserer(self , ui, souris) :  #Inserer dans mouse et task les commandes et la position de la souris.
        for e in ui :  
           self.task.append(ui)
        self.mouse.x = souris[0] 
        self.mouse.y = souris[1]

    def activation (self,scan,click) : #Active le personnage joue par le joueur selon ses frappes de clavier/souris.
        mouvement = ["MOVEUP","MOVELEFT","MOVERIGHT"] 
        externel  = ["ESC","`","0"]
        self.player.momentum(self) # Celui-ci va faire chuter/ascendre le joueur selon l'etat de l'attribut jump 
        self.player.timer_vitesse()# Celui-ci va changer sa vitesse selon l'etat de l'attribut timer
        if click != False  : 
           self.fire = True
           res = self.player.tirer(self.mouse , scan )
           for e in res :
               e[0].pv -= e[1]
        elif click == False : 
           self.fire = False                
        for ui in self.task : 
            for mov in mouvement :
                for frappe in ui :
                    if frappe == mov : 
                        self.player.mouvement(frappe,self)
            for ex in externel :
                for frappe in ui : 
                    if frappe == ex : 
                         if frappe == "ESC" :
                             fichier.sauvegarder(self) 
                         elif frappe == "`" : 
                             return "menu"
                         elif frappe == "0" : 
                             return "quit"
        self.player.check_carte(self)
        self.task = []
    def activation_entite(self,scan) : #active les entites  , scan = list obj d'Active entite, contient les donnees des entites se trouvant dans la meme carte que le joueur.
        i = None                     #variable qui suit les interactions entites/joueur
        for e in scan : 
            if e.pv > 0  : #Si l'entite est vivante , c'est a dire actif alors l'activer.
                if e.base.anime != False  : 
                    e.mouvement(self)
                i = e.interaction(self) 
            if i != None : #Permet d'infliger au joueurs des changements si l'entite est en contact avec le joueur 
                if i[0] == "pv" : 
                    self.player.pv += i[1] 
                if i[0] == "time" : 
                    self.player.time += i[1]
                if e.base.anime == False : #Entite inactif => "meurt" une fois rentree en contact 
                    e.pv = 0



#-----------------#
#-Menu principale-#
#-----------------#


def menu_principale (click , souris,e ) : 
    control = e
    if click and souris[0] > 350 and souris[0] < 1250  and souris[1] > 150 and souris[1]<300 :   #On demarre une nouvelle partie. 
        retour  = fichier.nouvelle_partie_1() 
        control = Control(retour[0] , retour[1] , retour[2] , retour[3])
        print("Demarer la partie... ")
        return control
    elif click and souris[0] > 350  and souris[0] < 1250 and souris[1] > 300 and souris[1]<450 : #On charge la sauvegarde
        retour  = fichier.charger()
        control = Control(retour[0] , retour[4], retour[3] , retour[5] , retour [1] , retour[2] )
        print("Charger une sauvegarde...")
        return control 
    elif click and souris[0] > 350 and souris[0] < 1250 and souris[1] > 450 and souris[1]<600 : #On veut se casser de ce jeu naze et se coucher 
        print("Quitter le jeu...")
        return "quit"
    elif click and souris [0] > 350 and souris [0] < 650 and souris [1] > 600 and souris [1] < 750 : 
        retour  = fichier.nouvelle_partie_1() 
        control = Control(retour[0] , retour[1] , retour[2] , retour[3])
        print("Demarer la partie , niveau 1 ... ")
        return control 
    elif click and souris [0] > 650 and souris [0] < 950 and souris [1] > 600 and souris [1] < 750 : 
        retour  = fichier.nouvelle_partie_2() 
        control = Control(retour[0] , retour[1] , retour[2] , retour[3])
        print("Demarer la partie , niveau 2 ... ") 
        return control 
    elif click and souris [0] > 950 and souris [0] < 1250 and souris [1] > 600 and souris [1] < 750 : 
        retour  = fichier.nouvelle_partie_3()  
        control = Control(retour[0] , retour[1] , retour[2] , retour[3])
        print("Demarer la partie , niveau 3 ... ")    
        return control 