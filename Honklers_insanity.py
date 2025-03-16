
import pygame 
from sys import exit 

import logique 
import graphique

control = None  #Variable globale 

pygame.init()
ecran = pygame.display.set_mode((1600,900))
pygame.display.set_caption("Pygame project")
fps = pygame.time.Clock() #Limite l'ordinateur a ne pas depasser 30 boucles par secondes
ui = [] #list str ; traque les frappes du joueur pour chaque frame (=100/30 sec)

tir = pygame.mixer.Sound("bruitage/pewpew.wav")
tir_timer = 1
musique = pygame.mixer.Sound("bruitage/jingle.wav") 
musique_timer = 0
saut = pygame.mixer.Sound("bruitage/saut.wav")

graphique_niveau3_timer = 180 #Permet de changer les textures du niveau toutes les 3 secondes. 

while True : 

    if musique_timer <= 0 : 
        musique_timer = 3600 
        musique.play() 
    elif musique_timer > 0 : 
        musique_timer -= 1 


    for e in pygame.event.get() :  # Enregistre dans la list ui les frappes du joueur. 
        if e.type == pygame.QUIT : 
            pygame.quit()
            exit()
    clavier  = pygame.key.get_pressed()   
    if clavier[pygame.K_SPACE] : 
              ui.append("MOVEUP")
              if isinstance(control, logique.Control) : 
                  if logique.detect_block_en_dessous_aggressive (control) : #Le son du jeu ne semble pas toujours marcher a cause de la maniere dont fonctionne la logique du jeu , meme fonction mais plus "aggressive"
                      saut.play()

    if clavier[pygame.K_a] : 
              ui.append("MOVELEFT")
    if clavier[pygame.K_d] : 
              ui.append("MOVERIGHT")
    if clavier[pygame.K_ESCAPE] : 
              ui.append("ESC") 
    if clavier[pygame.K_COMMA] : 
              ui.append("`") 
    if clavier[pygame.K_0] : 
              ui.append("0")

    if isinstance(control, logique.Control): #  Affiche les graphiques du jeu. Verifie si control est un objet de class Control , si oui on est en jeu alors on apelle la fonction jeu()
        scan = logique.detect_active_entite(control) # Retourne les proprietes des entites se trouvant dans la meme "carte" que le joueur. 
        retour = graphique.jeu(scan,control, graphique_niveau3_timer)          
        for e in retour : # e designe les surfaces pygame a afficher 
           ecran.blit(e[0],e[1])    #e[0] = proprietes de la surface ; e[1] = coordonnees ou la surface sera affiche. 
    elif control == None :  #Si control est egale a None , cela veut dire qu'on est dans le menu. On apelle la fonction menu()
        retour = graphique.menu()
        for e in retour : 
           ecran.blit(e[0],e[1])   

    graphique_niveau3_timer -= 1 
    if graphique_niveau3_timer <= 0 :
        graphique_niveau3_timer = 180

    if isinstance(control , logique.Control) : #  Met a jour le jeu selon la list ui, ou selon les proprietes des elements varies qui les obligent a se mettre a jour tout seul tout le temps.
        control.inserer(ui , pygame.mouse.get_pos())
        click = pygame.mouse.get_pressed()[0] 
        if click : 
            if tir_timer == 0 : 
                tir.play()
                tir_timer = 1
            else : 
                tir_timer -= 1
        i = control.activation(scan,click)
        control.activation_entite(scan) #On active les entites 
        if control.player.pv <= 0 : 
            control = None #Le joueur est mort donc on quitte vers le menu. 
        if i =="quit" : # Si le joueur a demande qu'on quitte le jeu, on quitte le jeu
            break  
        if i == "menu" : #Si le joueur a demander qu'on retourne au menu, control est egal a None
            control = None 
    
    elif control == None : #Si control est egal a None alors on est dans le menu; mettre a jour le menu.   
        control = logique.menu_principale(pygame.mouse.get_pressed()[0] , pygame.mouse.get_pos(),e)
        if control=="quit" :
            break 
    ui = []
    pygame.display.update()
    fps.tick(30)

print("Fin du jeu...")
pygame.quit() 
exit()