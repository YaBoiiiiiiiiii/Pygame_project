import pygame 
import random 

pygame.init()
#Texture pour le menu principal#

menu_background = pygame.image.load('texture/background_special.png') 
police          = pygame.font.Font("police/mingliu.ttf", 50 )
texte_background = pygame.Surface((900,150))
texte_background_mini = pygame.Surface((300,150))

texture_menu = { 
"menu_background" : pygame.transform.scale((menu_background), (1600 , 900)) ,
    
"texte_demarer"    : police.render("Nouvelle partie" , True , "White"  ) ,
"texte_charger"    : police.render("Charger une partie" , True , "White")   ,
"texte_quitter"    : police.render("Quitter le jeu", True , "White") ,
"texte_niveau1"    : police.render("Niveau 1", True , "White") ,
"texte_niveau2"    : police.render("Niveau 2", True , "White") ,
"texte_niveau3"    : police.render("Niveau 3", True , "White") ,

    
"texte_background" : texte_background ,
"texte_background_mini" : texte_background_mini
}

#Texture pour le jeu#

sprite_joueur      = pygame.image.load("texture/honk_idle.png") 
sprite_joueur_saut = pygame.image.load("texture/honk_idle.png") 

sprite_joueur_buff      = pygame.image.load("texture/honk_boosted.png") 
sprite_joueur_saut_buff = pygame.image.load("texture/honk_boosted.png") 

sprite_enemy1      = pygame.image.load("texture/enemy_float.png") 
sprite_enemy2      = pygame.image.load("texture/enemy_troll.png") 
sprite_enemy3      = pygame.image.load("texture/enemy_troll3.png") 
sprite_enemy4      = pygame.image.load("texture/enemy_troll2.png")
sprite_panacea     = pygame.image.load("texture/item_panacea.png")
sprite_pv          = pygame.image.load("texture/item_pv.png")
feu                = pygame.image.load("texture/honk_fire.png")
sprite_juice       = pygame.image.load("texture/item_forbiddenjuice.png")

texture_jeu = { 
"sprite_joueur"          : pygame.transform.scale(sprite_joueur , (100,100)) ,
"sprite_joueur_saut"     : pygame.transform.scale(sprite_joueur_saut , (100,150)) ,  
"sprite_joueur_opp"      : pygame.transform.flip( (pygame.transform.scale(sprite_joueur , (100,100)) ) , 1 , 0) ,
"sprite_joueur_saut_opp" : pygame.transform.flip( (pygame.transform.scale(sprite_joueur , (100,150)) ) , 1 , 0),

"sprite_joueur_buff"          : pygame.transform.scale(sprite_joueur_buff , (100,100)) ,
"sprite_joueur_saut_buff"     : pygame.transform.scale(sprite_joueur_saut_buff , (100,150)) , 
"sprite_joueur_buff_opp"      : pygame.transform.flip( (pygame.transform.scale(sprite_joueur_buff , (100,100)) ) , 1 , 0) , 
"sprite_joueur_saut_buff_opp" : pygame.transform.flip ( (pygame.transform.scale(sprite_joueur_saut_buff , (100,150)) ), 1 ,0 ), 

"sprite_joueur_tir"     : pygame.transform.scale(pygame.image.load("texture/honk_minigun.png") , (150 ,50)) ,
"sprite_joueur_tir_opp" : pygame.transform.flip ( (pygame.transform.scale(pygame.image.load("texture/honk_minigun.png") , (150 ,50))), 1 ,0) ,

"sprite_enemy1"   : pygame.transform.scale(sprite_enemy1 , (100,100)) , 
"sprite_enemy2"   : pygame.transform.scale(sprite_enemy2 , (300,300)) ,
"sprite_enemy3"   : pygame.transform.scale(sprite_enemy3 , (100,500)) , 
"sprite_enemy4"   : pygame.transform.scale(sprite_enemy4 , (80 , 80)) ,
"sprite_enemy_special"   : pygame.transform.scale(sprite_enemy3 , (500 , 500)) ,
"sprite_panacea"  : pygame.transform.scale(sprite_panacea, (100,100) ),
"sprite_juice"    : pygame.transform.scale(sprite_juice  , (100,150) ),
"sprite_pv"  : pygame.transform.scale(sprite_pv, (100,100) ), 
"feu"        : pygame.transform.scale(feu , (125, 125))
}

#Texture specifique aux niveaux# 

#niveau 1#

niveau_1_texture = { 
"background"   : pygame.transform.scale(pygame.image.load('texture/niveau1/background_prime_niveau1.jpg')  , (1600,900)) , 
"background_spe" : pygame.transform.scale(pygame.image.load('texture/niveau1/background_special_buff_niveau1.jpg')  , (1600,900)) ,  
"forground"    : pygame.transform.scale(pygame.image.load("texture/niveau1/forground_niveau1.jpg"),(1600,900)) ,
"solid"          : pygame.image.load("texture/niveau1/bloc_niveau1.jpg") ,
"skybox"         : pygame.transform.scale(pygame.image.load("texture/niveau1/sky_niveau1.jpeg") , (1600,900)) ,
}

#niveau 2# 

niveau_2_texture = { 
"background"   : pygame.transform.scale(pygame.image.load('texture/niveau2/background_prime_niveau2.png')  , (1600,900)) , 
"background_spe" : pygame.transform.scale(pygame.image.load('texture/niveau2/background_special_buff_niveau2.jpg')  , (1600,900)) ,  
"forground"    : pygame.transform.scale(pygame.image.load("texture/niveau2/forground_niveau2.png"),(1600,900)) ,
"solid"          : pygame.image.load("texture/niveau2/bloc_niveau2.png") ,
"skybox"         : pygame.transform.scale(pygame.image.load("texture/niveau2/sky_niveau2.jpg") , (1600,900)) ,
}

#niveau 3#

niveau_3_texture = { 
"background1"   : pygame.transform.scale(pygame.image.load('texture/niveau3/background_prime_1_niveau3.jpg')  , (1600,900)) , 
"background2"   : pygame.transform.scale(pygame.image.load('texture/niveau3/background_prime_2_niveau3.jpg')  , (1600,900)) , 
"background_spe" : pygame.transform.scale(pygame.image.load('texture/niveau3/background_special_buff_niveau3.jpg')  , (1600,900)) ,  
"forground"    : pygame.transform.scale(pygame.image.load("texture/niveau3/forground_niveau3.png"),(1600,900)) ,
"solid"          : pygame.image.load("texture/niveau3/bloc_niveau3.png") ,
"skybox"         : pygame.transform.scale(pygame.image.load("texture/niveau3/sky_niveau3.jpg") , (1600,900)) ,
}



def menu () : #Fonction qui se charge de faire afficher le menu du jeu. Appeler si la variable control pointe qu'on est dans le menu
    global texture_menu 
    retour = [
        (texture_menu["menu_background"]  ,  ( 0 , 0 ))  ,
        
        (texture_menu["texte_background"] ,( 350 , 150 )),
        (texture_menu["texte_background"] ,( 350 , 300 )),
        (texture_menu["texte_background"] ,( 350 , 450 )),
        (texture_menu["texte_demarer"]    ,( 350 , 150 )),
        (texture_menu["texte_charger"]    ,( 350 , 300 )),
        (texture_menu["texte_quitter"]    ,( 350 , 450 )),

        (texture_menu["texte_background_mini"],( 350 , 600 )),
        (texture_menu["texte_niveau1"] , ( 350 , 600 )) , 
        (texture_menu["texte_background_mini"],( 650 , 600 )),
        (texture_menu["texte_niveau2"] , ( 650 , 600 )) , 
        (texture_menu["texte_background_mini"],( 950 , 600 )),
        (texture_menu["texte_niveau3"] , ( 950 , 600 )) , 
    
        ]
    return retour 

def jeu (scan,e,timer_pour_niveau_3) : # scan = list obj d'Active entite, contient les donnees des entites se trouvant dans la meme carte que le joueur. Fonction qui se charge de faire afficher la partie de jeu , appeler si la variable control pointe qu'on est en plein jeu. 
    global texture_jeu 
    global police


    control = e 
    retour = [] 
    joueur = control.player 

    donnee = police.render ( (str (control.player.pv)) , True , "White" ) 

    if control.niveau == 1 : 
        global niveau_1_texture 
        niveau = niveau_1_texture
    elif control.niveau == 2 : 
        global niveau_2_texture 
        niveau = niveau_2_texture
    elif control.niveau == 3 : 
        global niveau_3_texture 
        niveau = niveau_3_texture 

    if joueur.time > 0 : #Charge les images en arrier plan
        retour.append((niveau["background_spe"], ( 0 , 0 )))
    elif control.player.coord.macro.y == control.map.macro.y : #Si on se trouve en bas du niveau  
        retour.append((niveau["forground"] , ( 0 , 0 ))) 
    elif control.player.coord.macro.y == 0 : 
        retour.append((niveau["skybox"] , ( 0 , 0 ) ))
    else : 
        if control.niveau != 3 : 
            retour.append(( niveau["background"] , ( 0 , 0 ))) 
        else : 
            if timer_pour_niveau_3 <= 90 : 
                retour.append((niveau["background1"] , ( 0 , 0 ))) 
            else :
                retour.append((niveau["background2"] , ( 0 , 0 )))

    if joueur.time > 0 : #Permet de determiner quelle image du joueur il faudrait charger selon certaine situation
        status = "sprite_joueur_buff" 
        status_saut = "sprite_joueur_saut_buff" 
        status_opp = "sprite_joueur_buff_opp"
        status_saut_opp = "sprite_joueur_saut_buff_opp"
    else : 
        status = "sprite_joueur"
        status_saut = "sprite_joueur_saut"
        status_opp = "sprite_joueur_opp"
        status_saut_opp = "sprite_joueur_saut_opp"    



    if joueur.jump > 0 : #on est en plein saut , alors charger une image differente
        if control.mouse.x > joueur.coord.x : 
            joueur_sprite = texture_jeu[status_saut],(joueur.coord.x - 50 , joueur.coord.y - 50 ) 
        else : 
            retour.append((texture_jeu[status_saut_opp],(joueur.coord.x - 50 , joueur.coord.y - 50 ))) 
    else : 
        if control.mouse.x > joueur.coord.x : 
            retour.append((texture_jeu[status],(joueur.coord.x - 50 , joueur.coord.y - 50 )))
        else : 
            retour.append((texture_jeu[status_opp],(joueur.coord.x - 50 , joueur.coord.y - 50 )))

    if control.fire == True : #Charge l'arme du joueur, si il tire
        if control.mouse.x > joueur.coord.x : 
            retour.append((texture_jeu["sprite_joueur_tir"] , (joueur.coord.x , joueur.coord.y)) )
        else : 
            retour.append((texture_jeu["sprite_joueur_tir_opp"] , (joueur.coord.x-125 , joueur.coord.y)) ) 

    joueur = control.player.coord.macro #Charge les soldies / blocs du jeu 
    for solid in control.map.carte[joueur.x][joueur.y] :
        block = pygame.transform.scale(niveau["solid"] , ( solid[2] , solid[3]))
        retour.append( (block , (solid[0] , solid[1])) )

    for ene in scan : #Charge les enemies 
       if ene.pv > 0 and not ene.base.espece == 2 : 
           retour.append((texture_jeu[ene.texture] , (ene.coord.x - ene.base.aoe.x / 2  , ene.coord.y - ene.base.aoe.y / 2 )) ) 
       elif ene.base.espece == 2 and ene.pv > 0 : 
           retour.append((texture_jeu[ene.texture] , (ene.coord.x - 225  , ene.coord.y - 225 )) )

    if control.fire : 
        retour.append(( texture_jeu["feu"] , (control.mouse.x-64 , control.mouse.y-64)))

    retour.append( (donnee , ( 100 , 100 ) ) )
    
    return retour 
