import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
largeur_fenetre = 800
hauteur_fenetre = 600
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Jeu de Course avec Menu et Rejouer")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
GRIS = (128, 128, 128)


# Classe Voiture
class Voiture:
    def __init__(self, x, y, vitesse, direction):
        self.largeur = 50
        self.hauteur = 100
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.direction = direction  # 1 pour descendre, -1 pour monter
        self.rect = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

    def deplacer(self):
        self.y += self.vitesse * self.direction
        self.rect.y = self.y

    def dessiner(self, fenetre):
        pygame.draw.rect(fenetre, ROUGE, self.rect)


# Fonction pour afficher du texte
def afficher_textes(message, taille, couleur, x, y):
    police = pygame.font.SysFont(None, taille)
    texte = police.render(message, True, couleur)
    fenetre.blit(texte, (x, y))


# Fonction pour afficher un bouton
def afficher_bouton(message, taille, couleur, x, y, largeur, hauteur, survol=False):
    police = pygame.font.SysFont(None, taille)
    texte = police.render(message, True, couleur)
    rect_bouton = pygame.Rect(x, y, largeur, hauteur)
    if survol:
        pygame.draw.rect(fenetre, GRIS, rect_bouton)
    else:
        pygame.draw.rect(fenetre, BLANC, rect_bouton)
    fenetre.blit(texte, (x + (largeur - texte.get_width()) // 2, y + (hauteur - texte.get_height()) // 2))
    return rect_bouton


# Fonction du menu principal
def menu_principal():
    en_menu = True
    while en_menu:
        fenetre.fill(NOIR)
        souris_x, souris_y = pygame.mouse.get_pos()

        # Titre du jeu
        afficher_textes("Jeu de Course", 64, BLANC, largeur_fenetre // 2 - 200, hauteur_fenetre // 2 - 200)

        # Bouton "Démarrer le Jeu"
        bouton_start = afficher_bouton("Démarrer le Jeu", 40, NOIR, largeur_fenetre // 2 - 150,
                                       hauteur_fenetre // 2 - 50, 300, 60, survol=False)

        # Bouton "Quitter"
        bouton_quit = afficher_bouton("Quitter", 40, NOIR, largeur_fenetre // 2 - 150, hauteur_fenetre // 2 + 30, 300,
                                      60, survol=False)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                # Changer la couleur du bouton si la souris le survole
                if bouton_start.collidepoint(event.pos):
                    afficher_bouton("Démarrer le Jeu", 40, NOIR, largeur_fenetre // 2 - 150, hauteur_fenetre // 2 - 50,
                                    300, 60, survol=True)
                else:
                    afficher_bouton("Démarrer le Jeu", 40, NOIR, largeur_fenetre // 2 - 150, hauteur_fenetre // 2 - 50,
                                    300, 60, survol=False)

                if bouton_quit.collidepoint(event.pos):
                    afficher_bouton("Quitter", 40, NOIR, largeur_fenetre // 2 - 150, hauteur_fenetre // 2 + 30, 300, 60,
                                    survol=True)
                else:
                    afficher_bouton("Quitter", 40, NOIR, largeur_fenetre // 2 - 150, hauteur_fenetre // 2 + 30, 300, 60,
                                    survol=False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_start.collidepoint(event.pos):
                    en_menu = False  # Quitter le menu et démarrer le jeu
                elif bouton_quit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


# Fonction principale du jeu
def lancer_jeu():
    clock = pygame.time.Clock()
    FPS = 60

    # Position de la voiture du joueur
    voiture_joueur_x = largeur_fenetre // 2 - 25
    voiture_joueur_y = hauteur_fenetre - 150
    voiture_joueur = Voiture(voiture_joueur_x, voiture_joueur_y, 0, 0)

    # Liste des voitures ennemies
    voitures_ennemies = []
    fréquence_apparition = 60  # Apparition toutes les 1 seconde (60 FPS)
    compteur_apparition = 0

    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            # Gestion des touches
            touches = pygame.key.get_pressed()
            if touches[pygame.K_LEFT] and voiture_joueur.x > 0:
                voiture_joueur.x -= 5
            if touches[pygame.K_RIGHT] and voiture_joueur.x < largeur_fenetre - voiture_joueur.largeur:
                voiture_joueur.x += 5
            if touches[pygame.K_UP] and voiture_joueur.y > 0:
                voiture_joueur.y -= 5
            if touches[pygame.K_DOWN] and voiture_joueur.y < hauteur_fenetre - voiture_joueur.hauteur:
                voiture_joueur.y += 5
            voiture_joueur.rect.x = voiture_joueur.x
            voiture_joueur.rect.y = voiture_joueur.y

            # Apparition des voitures ennemies
            compteur_apparition += 1
            if compteur_apparition >= fréquence_apparition:
                compteur_apparition = 0
                # Décider aléatoirement de la direction
                direction = random.choice([1, -1])
                if direction == 1:
                    x = random.randint(0, largeur_fenetre - 50)
                    y = -100
                else:
                    x = random.randint(0, largeur_fenetre - 50)
                    y = hauteur_fenetre
                vitesse = random.randint(3, 7)
                voiture = Voiture(x, y, vitesse, direction)
                voitures_ennemies.append(voiture)

            # Déplacer les voitures ennemies
            for voiture in voitures_ennemies[:]:
                voiture.deplacer()
                # Supprimer les voitures qui sortent de l'écran
                if voiture.direction == 1 and voiture.y > hauteur_fenetre:
                    voitures_ennemies.remove(voiture)
                    score += 1
                elif voiture.direction == -1 and voiture.y < -voiture.hauteur:
                    voitures_ennemies.remove(voiture)
                    score += 1
                # Vérifier les collisions
                if voiture.rect.colliderect(voiture_joueur.rect):
                    game_over = True

            # Dessiner
            fenetre.fill(NOIR)

            # Dessiner la route (simple ligne au milieu)
            pygame.draw.rect(fenetre, BLANC, (largeur_fenetre // 2 - 2, 0, 4, hauteur_fenetre))

            # Dessiner la voiture du joueur
            voiture_joueur.dessiner(fenetre)

            # Dessiner les voitures ennemies
            for voiture in voitures_ennemies:
                voiture.dessiner(fenetre)

            # Afficher le score
            afficher_textes(f"Score: {score}", 30, BLANC, 10, 10)

        else:
            # Afficher l'écran Game Over
            fenetre.fill(NOIR)
            afficher_textes("Game Over", 64, ROUGE, largeur_fenetre // 2 - 180, hauteur_fenetre // 2 - 100)
            afficher_textes(f"Score Final: {score}", 40, BLANC, largeur_fenetre // 2 - 130, hauteur_fenetre // 2)
            afficher_textes("Appuyez sur R pour rejouer ou Échap pour quitter", 30, BLANC, largeur_fenetre // 2 - 300,
                            hauteur_fenetre // 2 + 60)

            # Gestion des entrées après le Game Over
            touches = pygame.key.get_pressed()
            if touches[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            if touches[pygame.K_r]:
                # Réinitialiser les variables du jeu
                lancer_jeu()

        pygame.display.flip()
        clock.tick(FPS)


# Fonction principale
def main():
    while True:
        menu_principal()
        lancer_jeu()


if __name__ == "__main__":
    main()
