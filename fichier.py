import numpy as np
import random 
import logique 
import json 


def to_list_entite(elem) : #Transforme en classe dictionaire les entites de classe Active_entite. Ranger sous une classe dictionaire est plus rapide pour la bibliotheque json.
    retour = [ ]
    
    for e in elem : 
        retour.append([
            [e.base.anime , e.base.espece , e.base.interaction , e.base.aoe.x , e.base.aoe.y] ,
            e.coord.x ,
            e.coord.y ,
            e.macro.x , 
            e.macro.y , 
            e.pv , 
            e.texture 
        ])

    return retour 

def to_obj_entite (e) : #Transforme un dictionaire definissant une entite du jeu en une classe Active_entite
    retour = [] 
    for elem in e : 
        retour.append( 
        logique.Active_Entite ( 
            logique.Base_Entite( 
                elem[0][0] ,
                elem[0][2] , 
                elem[0][3] , 
                elem[0][4] ,
                elem[0][1]
                               ), 
            elem[1],
            elem[2],
            elem[3],
            elem[4],
            elem[6], 
            elem[5],
                               )
        )
    return retour 

def charger() : #Extrait les sauvegardes contenue dans le fichier txt a l'aide de json. 
    control = [ ]
    with open("sauvegarde.txt") as sv : 
        data = json.load(sv)
    control.append( data["coord"] )  
    control.append( data["pv"]    ) 
    control.append( data["time"]  ) 
    control.append( data["map"]   ) 
    control.append( to_obj_entite(data["entite"]) )
    control.append(data["niveau"])
    return control 

def sauvegarder(e) : #Sauvegarde la progression du joueur dans une classe Dictionaire, puis balance le dictionaire dans un fichier txt a l'aide de json. e , obj Control ; prend en argument la variable control. 
    control = e 
    with open("sauvegarde.txt","w") as sv : 
        data = {
            "map"    : control.map.carte       ,
            "entite" : to_list_entite(control.entite) ,
            "coord"  : [control.player.coord.x      ,
                       control.player.coord.y       , 
                       control.player.coord.macro.x ,
                       control.player.coord.macro.y ] ,
            "pv"     : control.player.pv              ,
            "time"   : control.player.time            ,
            "niveau" : control.niveau               ,
            }
        json.dump(data , sv )

def nouvelle_partie_1() :  #Met en place les parametres pour pouvoir commencer une nouvelle partie. Donne une nouvelle valeur a la variable control . 
    nv1 = [ ]

    for x in range (5) : 
        nv1.append( [ ] ) 
        for y in range (5) : 
            nv1[x].append([ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ])
  

    for x in range (len(nv1)-1) :  
            nv1[x][0][0] = [0 , 700 , 1600 , 200]   
            nv1[len(nv1)-1 - x][1][0] = [0 , 700 , 1600 , 200] 
            nv1[x][2][0] = [0 , 700 , 1600 , 200]  

    nv1[0][3][0] = [400 , 450 , 800 , 200] 
    nv1[2][3][0] = [400 , 450 , 800 , 200] 
    nv1[4][3][0] = [400 , 450 , 800 , 200] 

    for x in range ( len(nv1) ) : 
        for e in range(4) : 
            nv1[x][4][e] = [ random.randint(750 , 1000) , random.randint(300 , 600) , random.randint(250 , 499) , random.randint ( 200 , 299 ) ] 

    for x in range ( len(nv1) ) : 
        for y in range (len(nv1[0]) - 1) : 
            for e in range (3) : 
                nv1[x][y][1 + e] = [ random.randint(1 , 1000) , random.randint(100 , 700) , random.randint(1 , 499) , random.randint ( 1 , 199 ) ] 

           
          

    rdd = (800 , 450 , 0 , 0) #Coordonnes de depart du joueur 
    enemie = []               #Liste contenant les entites du niveau. 
    
    for i in range(80) : 
        enemie.append( logique.Active_Entite(logique.Base_Entite(1    ,
                       ["pv",-3],40,40,0),random.randint(1 , 1560)  , 
                       random.randint(1 , 860) , random.randint(0 , 4), 
                       random.randint(0 , 4) , "sprite_enemy1" , 60 ) ) 
    for i in range(5)  : 
        enemie.append( logique.Active_Entite(logique.Base_Entite(1    ,
                       ["pv",-6],40,40,0), 800                     , 
                       450 , random.randint(1 , 4)                    , 
                       random.randint(2 , 4) , "sprite_enemy2" , 400)) 
    enemie.append( logique.Active_Entite(logique.Base_Entite( 0       ,
                       ["time",600],100,100),800, 350, 1 , 2 
                       ,"sprite_panacea" , 10000000 ) ) 
    for i in range (3) : 
        enemie.append ( logique.Active_Entite(logique.Base_Entite( 0,
                       ["pv",30],100,100),800,350, random.randint(0 , 4) , 
                       random.randint(0 , 4) , "sprite_pv" , 10000000 ) ) 
    

    return rdd ,enemie , nv1 , 1

def nouvelle_partie_2() :  
    nv2 = [ ]

    for x in range (2) : 
        nv2.append( [ ] ) 
        for y in range (66) : 
            nv2[x].append([ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ])

    nv2[0][0][0] = [ 650 , 550 ,300 , 300]
    nv2[1][0][0] = [ 650 , 550 ,300 , 300]

    nv2[0][65][0] =[1, 750 , 1600 , 150]
    nv2[1][65][0] =[1, 750 , 1600 , 150]

    rdd = (800 , 450 , 0 , 0) #Coordonnes de depart du joueur 
    enemie = []               #Liste contenant les entites du niveau. 
    
    for i in range (75) : 
        enemie.append( logique.Active_Entite(logique.Base_Entite(1    ,
                       ["pv",-3],30,100,0),random.randint(1 , 1560)  , 
                       random.randint(350 , 900) , random.randint(0 , 1), 
                       random.randint(1 , 9) , "sprite_enemy4" , 6 ) )        
    for i in range(591) : 
        enemie.append( logique.Active_Entite(logique.Base_Entite(1    ,
                       ["pv",-3],30,100,0),random.randint(1 , 1560)  , 
                       random.randint(350 , 900) , random.randint(0 , 1), 
                       random.randint(10 , 65) , "sprite_enemy4" , 6 ) ) 
    for i in range(6)  : 
        enemie.append( logique.Active_Entite(logique.Base_Entite(0    ,
                       ["time",600],100,100), 800                     , 
                       450 , random.randint(0 , 1)                    , 
                       random.randint(1 , 60) , "sprite_panacea" , 100000)) 
    for i in range (15) : 
        enemie.append ( logique.Active_Entite(logique.Base_Entite( 0,
                       ["pv",30],100,100),800,350, random.randint(0 , 1) , 
                       random.randint(1 , 65) , "sprite_pv" , 10000000 ) ) 
    

    return rdd ,enemie , nv2 , 2

def nouvelle_partie_3() :  
    nv3 = [ ]

    for x in range (10) : 
        nv3.append( [ ] ) 
        for y in range (33) : 
            nv3[x].append([ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]  ])

    rdd = (800 , 450 , 4 , 23) #Coordonnes de depart du joueur 
    enemie = []                #Liste contenant les entites du niveau. 
    
    for x in range (10) : 
        for y in range (33) : 
            nv3[x][y][0] = [0 , 750 , 1600 , 150]
    for y in range(33) : 
        resy = random.randint(1 , 9)
        nv3[resy][y][1] = [500 , 450 , 300 , 300] 
        nv3[resy][y][2] = [500 , 50 , 300 , 300] 
    for y in range (1 ,33) : 
        resz = random.randint(1 , 9)
        nv3[resz][y][3] = [500 , 450 , 100 , 100] 
    for x in range (10) : 
        nv3[x][24] = [ [0 , 750 , 1600 , 150], [0,0,0,0], [0,0,0,0], [0,0,0,0]  ] 
        nv3[x][23] = [ [0 , 750 , 1600 , 150], [0,0,0,0], [0,0,0,0], [0,0,0,0]  ] 

    nv3[0][24][1] =  [500 , 450 , 300 , 300] 
    nv3[0][24][2] =  [500 , 50 , 300 , 300] 
      
    nv3[5][23][1] =  [500 , 450 ,300 , 300] 
    nv3[6][23][2] =  [500 , 450 ,300 , 300]
    nv3[6][23][3] =  [500 , 50 ,300 , 300]
    nv3[4][23][3] =  [500 , 300 , 50, 50]

    enemie.append (   logique.Active_Entite(logique.Base_Entite(1    ,
                       ["pv",-2],225,125,2), 625  , 
                        525 , 5,  
                       23 , "sprite_enemy_special" , 666 ) )     

    return rdd ,enemie , nv3 , 3 
    

    
#150 , 150