 #!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import numpy.linalg as alg
import matplotlib.pyplot as plt
import pygame

'''

# Initialisation de Pygame
pygame.init()
'''
# Paramètres de la fenêtre
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Billard de Sinaï")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
'''
# Temps
clock = pygame.time.Clock()
FPS = 60

# Paramètres du billard de Sinaï

# Paramètres des billes
ball_radius = 1
initial_pos = np.array([530.0, 430.0])  # Position initiale des billes
initial_speed = 2.0  # Vitesse initiale des billes

num_balls = 500  # Nombre de billes

# Générer des directions aléatoires pour chaque bille
balls = []
for _ in range(num_balls):
    # Générer un angle aléatoire en radians
    angle = np.random.uniform(0, 2 * np.pi)
    # Convertir l'angle en un vecteur de direction
    ball_vel = initial_speed * np.array([np.cos(angle), np.sin(angle)])
    balls.append({
        'pos': initial_pos.copy(),
        'vel': ball_vel
    })

# Paramètres des obstacles
obstacle_radius = 10
grid_size = 40  # Distance entre les obstacles dans le réseau
obstacles = []  # Liste pour stocker les positions des obstacles

# Créer un réseau carré d'obstacles
for x in range(obstacle_radius, WIDTH, grid_size):
    for y in range(obstacle_radius, HEIGHT, grid_size):
        obstacles.append(np.array([x, y]))


def reflect(ball_pos, ball_vel, obstacle_pos, obstacle_radius):
    # Vérifier la collision avec l'obstacle circulaire
    delta_pos = ball_pos - obstacle_pos
    distance = np.linalg.norm(delta_pos)
    
    if distance <= obstacle_radius + ball_radius:
        # Normaliser le vecteur entre la bille et l'obstacle
        normal = delta_pos / distance
        # Calcul de la réflexion en renversant la composante normale de la vitesse
        ball_vel -= 2 * np.dot(ball_vel, normal) * normal
    
    return ball_vel

# cas non magnétique

def update_ball(balls, obstacles, obstacle_radius):
    for ball in balls:
        ball['pos'] += ball['vel']  # Mettre à jour la position de chaque bille

        # Gestion des collisions avec les bords de la fenêtre
        if ball['pos'][0] - ball_radius <= 0 or ball['pos'][0] + ball_radius >= WIDTH:
            ball['vel'][0] = -ball['vel'][0]  # Inverser la vitesse en x
            ball['pos'][0] = np.clip(ball['pos'][0], ball_radius, WIDTH - ball_radius)  # Garder la bille à l'intérieur des bords

        if ball['pos'][1] - ball_radius <= 0 or ball['pos'][1] + ball_radius >= HEIGHT:
            ball['vel'][1] = -ball['vel'][1]  # Inverser la vitesse en y
            ball['pos'][1] = np.clip(ball['pos'][1], ball_radius, HEIGHT - ball_radius)  # Garder la bille à l'intérieur des bords

        # Gestion des collisions avec les obstacles circulaires
        for obstacle_pos in obstacles:
            delta_pos = ball['pos'] - obstacle_pos
            distance = np.linalg.norm(delta_pos)

            if distance <= obstacle_radius + ball_radius:
                # Collision détectée avec l'obstacle
                normal = delta_pos / distance
                new_vel = ball['vel'] - 2 * np.dot(ball['vel'], normal) * normal
                # Vérifier si la réflexion change suffisamment la direction
                if not np.allclose(ball['vel'], new_vel, atol=1e-3):
                    ball['vel'] = new_vel
                else:
                    break  # Éviter la réflexion continue

    return balls



##### Boucle principale


# Boucle principale 1
t=0
meand = []
T = []
running = True
while running:
    total_distance = 0
    t+=1
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mise à jour de la position et de la vitesse de chaque bille

    balls = update_ball(balls, obstacles, obstacle_radius)

    # Dessin des obstacles
    for obstacle_pos in obstacles:
        pygame.draw.circle(screen, BLACK, obstacle_pos.astype(int), obstacle_radius )
    
    # Dessin des billes
    for ball in balls:
        pygame.draw.circle(screen, RED, ball['pos'].astype(int), ball_radius)
        
    for ball in balls: 
        distance_to_initial = alg.norm(ball['pos'] - initial_pos)
        total_distance += distance_to_initial  # Ajouter cette distance à la somme totale

    # Rafraîchissement de l'écran
    pygame.display.flip()

    # Limiter les FPS
    clock.tick(FPS)
    
    meand.append(total_distance / len(balls))
    T.append(t)
    
    

    
    if t >= 500: 
        running = False

pygame.quit()


### Validation du modèle diffusif 

plt.plot(T, meand, marker='o')  # 'o' pour afficher des marqueurs sur les points

# Ajouter des titres et des labels
plt.title("Eloignement moyen en fonction du temps : noB")
plt.xlabel("temps (tics)")
plt.ylabel("distance moyenne du point de départ")

# Afficher la grille
plt.grid()

# Afficher le graphique
plt.show()


meandcarre = []
for i in meand:
    meandcarre.append(i*i)
    
coefficients = np.polyfit(T, meandcarre, 1)
slope = coefficients[0]  # Coefficient directeur
intercept = coefficients[1]  # Ordonnée à l'origine

# Calculer la droite d'ajustement
y_fit = np.polyval(coefficients, T)
plt.scatter(T,meandcarre, color='blue', label='Données')
plt.plot(T, y_fit, color='red', label=f'Ajustement linéaire (pente={slope:.2f})')
    
plt.plot(T, meandcarre, marker='o')  # 'o' pour afficher des marqueurs sur les points

# Ajouter des titres et des labels
plt.title("Eloignement quadratique moyen en fonction du temps : noB")
plt.xlabel("temps (tics)")
plt.ylabel("distance moyenne du point de départ")

# Afficher la grille
plt.grid()

# Afficher le graphique
plt.show()

print(f"Le coefficient directeur (pente) est : {slope}")



### ajout d'un champs magnétique :

#champs magnétique
Bz = 0.3 # dans les faits c'est (q*B)/m

   
def update_balls_with_magnetic_field(balls, obstacles, obstacle_radius, Bz):
    total_distance = 0  # Somme des distances entre positions actuelles et initiales

    for ball in balls:
        # Calcul de la force magnétique
        # La force magnétique est perpendiculaire à la vitesse et agit dans le plan XY
        magnetic_force_x = ball['vel'][1] * Bz  # Force en X
        magnetic_force_y = -ball['vel'][0] * Bz  # Force en Y

        # Mettre à jour la vitesse de la bille avec la force magnétique
        ball['vel'][0] += magnetic_force_x
        ball['vel'][1] += magnetic_force_y
        ball['vel'] = (initial_speed*ball['vel'])/np.sqrt( (ball['vel'][0])**2 +(ball['vel'][1])**2)

        # Mettre à jour la position de chaque bille
        ball['pos'] += ball['vel']

        # Gestion des collisions avec les bords de la fenêtre
        if ball['pos'][0] - ball_radius <= 0 or ball['pos'][0] + ball_radius >= WIDTH:
            ball['vel'][0] = -ball['vel'][0]  # Inverser la vitesse en x
            ball['pos'][0] = np.clip(ball['pos'][0], ball_radius, WIDTH - ball_radius)  # Garder la bille à l'intérieur des bords

        if ball['pos'][1] - ball_radius <= 0 or ball['pos'][1] + ball_radius >= HEIGHT:
            ball['vel'][1] = -ball['vel'][1]  # Inverser la vitesse en y
            ball['pos'][1] = np.clip(ball['pos'][1], ball_radius, HEIGHT - ball_radius)  # Garder la bille à l'intérieur des bords

        # Gestion des collisions avec les obstacles circulaires
        for obstacle_pos in obstacles:
            delta_pos = ball['pos'] - obstacle_pos
            distance = np.linalg.norm(delta_pos)

            if distance <= obstacle_radius + ball_radius:
                # Collision détectée avec l'obstacle
                normal = delta_pos / distance
                new_vel = ball['vel'] - 2 * np.dot(ball['vel'], normal) * normal
                ball['vel'] = new_vel

                # Ajuste la position de la bille pour éviter qu'elle ne reste coincée dans l'obstacle
                overlap = (obstacle_radius + ball_radius) - distance
                ball['pos'] += normal * overlap  # Pousse la bille hors de l'obstacle

        # Calcul de la distance entre la position actuelle et la position initiale
        distance_to_initial = alg.norm(ball['pos'] - initial_pos)
        total_distance += distance_to_initial  # Ajouter cette distance à la somme totale

    # Calcul de la distance moyenne
    average_distance = total_distance / len(balls)
    return balls




# Boucle principale 2

#initialisation  

pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Billard de Sinaï")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Temps
clock = pygame.time.Clock()
FPS = 60


# Paramètres du billard de Sinaï

# Paramètres des billes
ball_radius = 1
initial_pos = np.array([560.0, 430.0])  # Position initiale des billes
initial_speed = 2.0  # Vitesse initiale des billes

num_balls = 800  # Nombre de billes

# Générer des directions aléatoires pour chaque bille
balls = []
for _ in range(num_balls):
    # Générer un angle aléatoire en radians
    angle = np.random.uniform(0, 2 * np.pi)
    # Convertir l'angle en un vecteur de direction
    ball_vel = initial_speed * np.array([np.cos(angle), np.sin(angle)])
    balls.append({
        'pos': initial_pos.copy(),
        'vel': ball_vel
    })




#lancement 
t=0
meand = []
T = []
running = True
while running:
    total_distance=0
    t+=1
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mise à jour de la position et de la vitesse de chaque bille

    balls = update_balls_with_magnetic_field(balls, obstacles, obstacle_radius,Bz)

    # Dessin des obstacles
    for obstacle_pos in obstacles:
        pygame.draw.circle(screen, BLACK, obstacle_pos.astype(int), obstacle_radius, 2)
    
    # Dessin des billes
    for ball in balls:
        pygame.draw.circle(screen, RED, ball['pos'].astype(int), ball_radius)
        
    for ball in balls: 
        distance_to_initial = alg.norm(ball['pos'] - initial_pos)
        total_distance += distance_to_initial  # Ajouter cette distance à la somme totale

    # Rafraîchissement de l'écran
    pygame.display.flip()

    # Limiter les FPS
    clock.tick(FPS)
    
    meand.append(total_distance / len(balls))
    T.append(t)
    

       

pygame.quit()


### Validation du modèle diffusif 

plt.plot(T, meand, marker='o')  # 'o' pour afficher des marqueurs sur les points

# Ajouter des titres et des labels
plt.title("Eloignement moyen en fonction du temps : B")
plt.xlabel("temps (tics)")
plt.ylabel("distance moyenne du point de départ")

# Afficher la grille
plt.grid()

# Afficher le graphique
plt.show()


meandcarre = []
for i in meand:
    meandcarre.append(i*i)
    
coefficients = np.polyfit(T, meandcarre, 1)
slope = coefficients[0]  # Coefficient directeur
intercept = coefficients[1]  # Ordonnée à l'origine

# Calculer la droite d'ajustement
y_fit = np.polyval(coefficients, T)
plt.scatter(T,meandcarre, color='blue', label='Données')
plt.plot(T, y_fit, color='red', label=f'Ajustement linéaire (pente={slope:.2f})')
    
plt.plot(T, meandcarre, marker='o')  # 'o' pour afficher des marqueurs sur les points

# Ajouter des titres et des labels
plt.title("Eloignement quadratique moyen en fonction du temps : B")
plt.xlabel("temps (tics)")
plt.ylabel("distance moyenne du point de départ")

# Afficher la grille
plt.grid()

# Afficher le graphique
plt.show()

print(f"Le coefficient directeur (pente) est : {slope}")


'''
'''
def rk4_step(masses, dt, obstacles, obstacle_radius, ball_radius):
    
    def compute_acceleration(masses):
         # Accélération (Newton's second law: F = ma)
         F_total = calculate_forces(masses, obstacles, obstacle_radius, ball_radius)
         return F_total 
    
    # RK4 coefficients pour la position et la vitesse
    k1_v = dt * compute_acceleration(ball)
    k1_x = dt 
    
    k2_v = dt * compute_acceleration({'pos': masses['pos'] + 0.5 * k1_x, 'vel': masses['vel'] + 0.5 * k1_v})
    k2_x = dt * (ball['vel'] + 0.5 * k1_v)
    
    k3_v = dt * compute_acceleration({'pos': masses['pos'] + 0.5 * k2_x, 'vel': masses['vel'] + 0.5 * k2_v})
    k3_x = dt * (ball['vel'] + 0.5 * k2_v)
    
    k4_v = dt * compute_acceleration({'pos': masses['pos'] + k3_x, 'vel': masses['vel'] + k3_v})
    k4_x = dt * (ball['vel'] + k3_v)
    
    # Mise à jour des positions et vitesses
    ball['vel'] += (k1_v + 2*k2_v + 2*k3_v + k4_v) / 6
    ball['pos'] += (k1_x + 2*k2_x + 2*k3_x + k4_x) / 6
    
    return masses

'''

### Ajout des phonons 



# Constantes physiques
num_masses = 40  # Nombre de masses par dimension
mass_spacing = 40  # Espacement entre les masses
k = 10 # Constante de ressort
L0 = mass_spacing  # Longueur à vide du ressort
time_step = 10**(-4)  # Pas de temps
box_size = 1800  # Taille de la boîte
mu = 0

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((box_size, box_size))
pygame.display.set_caption("Système Masse-Ressort")
clock = pygame.time.Clock()

# Initialisation des masses
masses = []
for i in range(num_masses):
    for j in range(num_masses):
        pos = np.array([i * mass_spacing + 10, j * mass_spacing + 10], dtype=np.float64)
        if j!=0 and j!= num_masses-1 and i != 0 and i != num_masses-1:
            masses.append({'pos': pos + 3*np.random.uniform(-1, 1, 2), 'vel': np.array([0,0], dtype=np.float64)})#''', charge': e'''
        else :
            masses.append({'pos': pos , 'vel': np.array([0,0], dtype=np.float64)})
    
        


# Fonction pour trouver les voisins adjacents
def find_adjacent_neighbors(idx):
    neighbors = []
    row = idx // num_masses
    col = idx % num_masses
    
    # Vérification des voisins dans les quatre directions
    if row > 0:  # Voisin du haut
        neighbors.append(idx - num_masses)
    if row < num_masses - 1:  # Voisin du bas
        neighbors.append(idx + num_masses)
    if col > 0:  # Voisin de gauche
        neighbors.append(idx - 1)
    if col < num_masses - 1:  # Voisin de droite
        neighbors.append(idx + 1)
    
    return neighbors

# Fonction pour calculer les forces entre les masses
def calculate_forces(k):
    forces = []
    for i in range(len(masses)):
        net_force = np.array([0.0, 0.0], dtype=np.float64)
        neighbors = find_adjacent_neighbors(i)
        for j in neighbors:
            # Calcul de la force entre la masse i et son voisin j
            displacement = masses[j]['pos'] - masses[i]['pos']
            distance = np.linalg.norm(displacement)
            speed = masses[j]['vel'] - masses[i]['vel']
            if distance > 0:  # Évite la division par zéro
                force_magnitude = k * (distance - L0)
                force_direction = (displacement / distance)
                net_force += (force_magnitude * force_direction + mu* speed)
        forces.append(net_force)
    return forces



# Fonction de mise à jour des positions des masses
def update_positions(forces):
    for i in range(len(masses)):
        r = i // num_masses
        c = i % num_masses
        if c!=0 and c!= num_masses-1 and r != 0 and r != num_masses-1:
            # Mise à jour de la vitesse et de la position
            masses[i]['vel'] += forces[i] * time_step
            masses[i]['pos'] += masses[i]['vel'] * time_step

        # Gestion des collisions avec les murs
        masses[i]['pos'] = np.clip(masses[i]['pos'], 0, box_size)  # Assurer que les positions restent dans la boîte

        # Inverser la vitesse si la masse touche les murs
        if masses[i]['pos'][0] <= 0 or masses[i]['pos'][0] >= box_size:
            masses[i]['vel'][0] *= -1
        if masses[i]['pos'][1] <= 0 or masses[i]['pos'][1] >= box_size:
            masses[i]['vel'][1] *= -1


# Paramètres des billes
ball_radius = 1
initial_pos = np.array([830.0, 750.0])  # Position initiale des billes
initial_speed = 10**(4)  # Vitesse initiale des billes

num_balls = 300  # Nombre de billes

# Générer des directions aléatoires pour chaque bille
balls = []
angle=4898
anglee = angle + 1e-6
ball_vel1 = initial_speed * np.array([np.cos(angle), np.sin(angle)])
balls.append({
    'pos': initial_pos.copy(),
    'vel': ball_vel1
    })
ball_vel2 = initial_speed * np.array([np.cos(anglee), np.sin(anglee)])
balls.append({
    'pos': initial_pos.copy(),
    'vel': ball_vel2
    })

'''for _ in range(num_balls):
    # Générer un angle aléatoire en radians
    angle = np.random.uniform(0, 2 * np.pi)
    # Convertir l'angle en un vecteur de direction
    ball_vel = initial_speed * np.array([np.cos(angle), np.sin(angle)])
    balls.append({
        'pos': initial_pos.copy(),
        'vel': ball_vel
    })
'''

#'charge': -e



#update de la position de la bille 
def update_ball(balls, obstacles, obstacle_radius):
    for ball in balls:
        
 
        
 
        
    
       
        ball['pos'] += ball['vel']  * time_step # Mettre à jour la position de chaque bille

   # Gestion des collisions avec les bords de la fenêtre
        if ball['pos'][0] - ball_radius <= 0 or ball['pos'][0] + ball_radius >= WIDTH:
            ball['vel'][0] = -ball['vel'][0]  # Inverser la vitesse en x
            ball['pos'][0] = np.clip(ball['pos'][0], ball_radius, WIDTH - ball_radius)  # Garder la bille à l'intérieur des bords

        if ball['pos'][1] - ball_radius <= 0 or ball['pos'][1] + ball_radius >= HEIGHT:
            ball['vel'][1] = -ball['vel'][1]  # Inverser la vitesse en y
            ball['pos'][1] = np.clip(ball['pos'][1], ball_radius, HEIGHT - ball_radius)  # Garder la bille à l'intérieur des bords

        # Gestion des collisions avec les obstacles circulaires
        for obstacle in obstacles:
            delta_pos = ball['pos'] - obstacle['pos']
            distance = np.linalg.norm(delta_pos)

            if distance <= obstacle_radius + ball_radius:
                # Collision détectée avec l'obstacle
                normal = delta_pos / distance

                # Influence de la vitesse de l'obstacle sur la réflexion
                relative_velocity = ball['vel'] - obstacle['vel']  # Vitesse relative entre la bille et l'obstacle
                new_vel = relative_velocity - 2 * np.dot(relative_velocity, normal) * normal
                new_vel += obstacle['vel']  # Ajouter la vitesse de l'obstacle à la nouvelle vitesse

                # Vérifier si la réflexion change suffisamment la direction
                if not np.allclose(ball['vel'], new_vel, atol=1e-3):
                    ball['vel'] = new_vel
                else:
                    break  # Éviter la réflexion continue

    return balls






# Boucle principale
t=0
meand = []
meanv = []
T = []
Lya =[]
K = [100000,500000,1000000,2000000,5000000,7000000,10000000]
running = True
bille = True
for k in K: 
    bille = True
    Moy=[]
    while bille:
        running = True
        t=0
        T = []
        meand = []
        meanv = []
        balls = []
        angle=43*np.random.uniform(-1, 1)
        anglee = angle + 1e-6
        ball_vel1 = initial_speed * np.array([np.cos(angle), np.sin(angle)])
        balls.append({
            'pos': initial_pos.copy(),
            'vel': ball_vel1
            })
        ball_vel2 = initial_speed * np.array([np.cos(anglee), np.sin(anglee)])
        balls.append({
            'pos': initial_pos.copy(),
            'vel': ball_vel2
            })
    
        while running:
            total_distance = []
            t+=1
            screen.fill(WHITE)
            
            #Dessin des masses
            for mass in masses:
                pygame.draw.circle(screen, BLACK, mass['pos'].astype(int), 10)
        
            # Calcul des forces et mise à jour des positions
            forces = calculate_forces(k)
            update_positions(forces)
            
            # Mise à jour de la position et de la vitesse de chaque bille
        
            balls = update_ball(balls, masses, 10)
        
        
            
            # Dessin des billes
            for ball in balls:
                pygame.draw.circle(screen, RED, ball['pos'].astype(int), ball_radius)
                
            for ball in balls: 
                distance_to_initial = ball['pos'] - initial_pos
                total_distance.append(distance_to_initial) 
                #total_vel += alg.norm(ball['vel'])   # Ajouter cette distance à la somme totale
        
        
            pygame.display.flip()
            clock.tick(60)
        
            # Quitter la simulation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    bille = False
                    
            if len(Moy) >= 10 : 
                bille = False
                    
        
            
            meand.append(alg.norm(total_distance[1] - total_distance[0]))
            T.append(t)
            
                
            if t >= 600: 
                running = False
    
    
        LY=[]
        LYnorm=[]
        for i in range(len(meand)-1):
            LY.append(np.log(meand[i+1]/meand[i]))
            LYnorm.append(np.log(meand[i]))
        
        lammda = 1/t*sum(LY)
        print(lammda)
    
        ### Validation du modèle diffusif 
        
        plt.plot(T, meand, marker='o')  # 'o' pour afficher des marqueurs sur les points
        
        # Ajouter des titres et des labels
        plt.title("Eloignement moyen en fonction du temps : phonons")
        plt.xlabel("temps (tics)")
        plt.ylabel("distance moyenne du point de départ")
        
        # Afficher la grille
        plt.grid()
        
        # Afficher le graphique
        plt.show()
        T.pop()
            
        plt.plot(T, LYnorm, marker='o')  # 'o' pour afficher des marqueurs sur les points
        
        # Ajouter des titres et des labels
        plt.title("Eloignement moyen en fonction du temps : phonons")
        plt.xlabel("temps (tics)")
        plt.ylabel("distance moyenne du point de départ")
     
        coefficients = np.polyfit(T, LYnorm, 1)
        slope = coefficients[0]  # Coefficient directeur
        intercept = coefficients[1]  # Ordonnée à l'origine
    
        # Calculer la droite d'ajustement
        y_fit = np.polyval(coefficients, T)
        plt.scatter(T,LYnorm, color='blue', label='Données')
        plt.plot(T, y_fit, color='red', label=f'Ajustement linéaire (pente={slope:.2f})')
        ### Validation du modèle diffusif 
    
              
        # Afficher la grille
        plt.grid()
        
        # Afficher le graphique
        plt.show() 
        print(f"Le coefficient directeur (pente) est : {slope}")
    #    if alg.norm((lammda-slope)/lammda) <= 0.1:
        Moy.append(lammda)
            
    
    
    
    print(f"En moyenne, l'exposant de Lyapunov est ' : {np.mean(Moy)}")
    Lya.append(np.mean(Moy))
pygame.quit()
 plt.plot(K, Lya, marker='o')  # 'o' pour afficher des marqueurs sur les points
 
 # Ajouter des titres et des labels
 plt.title("Lya en fonction de k")
 plt.xlabel("temps (tics)")
 plt.ylabel("distance moyenne du point de départ")
 
 # Afficher la grille
 plt.grid()
 
 # Afficher le graphique
 plt.show()



'''LY=[]
for i in range(len(meand)-1):
    LY.append(np.log(meand[i+1]/meand[i]))

lammda = 1/t*sum(LY)
print(lammda)

### Validation du modèle diffusif 

plt.plot(T, meand, marker='o')  # 'o' pour afficher des marqueurs sur les points

# Ajouter des titres et des labels
plt.title("Eloignement moyen en fonction du temps : phonons")
plt.xlabel("temps (tics)")
plt.ylabel("distance moyenne du point de départ")

# Afficher la grille
plt.grid()

# Afficher le graphique
plt.show()
'''
'''
meandcarre = []
for i in meand:
    meandcarre.append(i*i)
    
coefficients = np.polyfit(T, meandcarre, 1)
slope = coefficients[0]  # Coefficient directeur
intercept = coefficients[1]  # Ordonnée à l'origine

# Calculer la droite d'ajustement
y_fit = np.polyval(coefficients, T)
plt.scatter(T,meandcarre, color='blue', label='Données')
plt.plot(T, y_fit, color='red', label=f'Ajustement linéaire (pente={slope:.2f})')
### Validation du modèle diffusif 

    
plt.plot(T, meandcarre, marker='o')  # 'o' pour afficher des marqueurs sur les points

# Ajouter des titres et des labels
plt.title("Eloignement quadratique moyen en fonction du temps : phonons")
plt.xlabel("temps (tics)")
plt.ylabel("distance moyenne du point de départ")

# Afficher la grille
plt.grid()

# Afficher le graphique
plt.show()

print(f"Le coefficient directeur (pente) est : {slope}")



### Paire de Cooper 
'''











