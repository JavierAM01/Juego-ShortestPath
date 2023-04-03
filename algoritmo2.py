import pygame

# colores
NEGRO = (0,0,0)
GRIS = (50,50,50)
AMARILLO = (255,255,0)
VERDE = (9, 217, 12)
MORADO = (150,25,200)

#variables
COLOR_PUNTOS1 = AMARILLO 
COLOR_PUNTOS2 = NEGRO 
COLOR_HISTORIAL = GRIS
COLOR_ADYACENCIA = VERDE
COLOR_CAMINO = MORADO 
COLOR_PARED = (200,200,200)

NX = 50
NY = 50
DIM = 15
ANCHURA = NX*DIM
ALTURA = NY*DIM


# inicio del juego
pygame.init()
paredes = []
pos_inicial, pos_final = [0,0], [(NX-1)*DIM, (NY-1)*DIM]


play_surface = pygame.display.set_mode((ANCHURA, ALTURA))
pygame.display.set_caption("Find the sortest path. Creado por: Javier Abollado")

font = pygame.font.Font(None, 30)
FPS = pygame.time.Clock()


def actualizar_screen(fps, historial = [], adyacencias = []):
    play_surface.fill(NEGRO)

    for pos in paredes:
        pygame.draw.rect(play_surface, COLOR_PARED, pygame.Rect(pos[0], pos[1], DIM, DIM))
        
    for i in range(NY+1):
        pygame.draw.rect(play_surface, GRIS, pygame.Rect(0, i*DIM-1, ANCHURA, 2))
    for i in range(NY+1):
        pygame.draw.rect(play_surface, GRIS, pygame.Rect(i*DIM-1, 0, 2, ALTURA))

    for pos in historial:
        pygame.draw.rect(play_surface, COLOR_HISTORIAL, pygame.Rect(pos[0], pos[1], DIM, DIM))
    for pos in adyacencias:
        pygame.draw.rect(play_surface, COLOR_ADYACENCIA, pygame.Rect(pos[0], pos[1], DIM, DIM))

    pygame.draw.rect(play_surface, COLOR_PUNTOS1, pygame.Rect(pos_inicial[0], pos_inicial[1], DIM, DIM))
    pygame.draw.rect(play_surface, COLOR_PUNTOS2, pygame.Rect(pos_inicial[0] + DIM/4+ DIM/16, pos_inicial[1] + DIM/4+ DIM/16, DIM/2, DIM/2))
    pygame.draw.rect(play_surface, COLOR_PUNTOS1, pygame.Rect(pos_final[0], pos_final[1], DIM, DIM))
    pygame.draw.rect(play_surface, COLOR_PUNTOS2, pygame.Rect(pos_final[0] + DIM/4+ DIM/16, pos_final[1] + DIM/4+ DIM/16, DIM/2, DIM/2))
        
    FPS.tick(fps)



def algoritmo_busqueda():

    def invert(pos):
        return [int(pos[0]/DIM), int(pos[1]/DIM)]
    def convert(pos):
        return [pos[0]*DIM, pos[1]*DIM]

    def crear_direccion(pos):
        dif_x = invert(pos_final)[0] - pos[0]
        dif_y = invert(pos_final)[1] - pos[1]
        if dif_x > 0: negativo_x = False
        else: negativo_x = True
        if dif_y > 0: negativo_y = False
        else: negativo_y = True
        return [dif_x, dif_y, negativo_x, negativo_y]

    run = True
    longitud = 0

    distancias = [["i" for j in range(NX)] for i in range(NY)]
    distancias[invert(pos_inicial)[0]][invert(pos_inicial)[1]] = 0
    activos = [list(invert(pos_inicial))]
    historial = []
    adyacencias = []

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        temp = []

        for pos in activos:
            [dif_x, dif_y, negativo_x, negativo_y] = crear_direccion(pos)
            d = distancias[pos[0]][pos[1]] + 1

            def search(ady, longitud): # devuelve [si hay algún fallo, si seguimos investigando "run"]
                if convert(ady) not in paredes and ady[0] >= 0 and ady[0] < NX and ady[1] >= 0 and ady[1] < NY:
                        
                    movimiento_valido = False
                    if distancias[ady[0]][ady[1]] == "i": movimiento_valido = True
                    else: 
                        if distancias[ady[0]][ady[1]] > longitud: movimiento_valido = True
                        
                    if movimiento_valido:
                        if convert(ady) not in adyacencias: adyacencias.append(list(convert(ady)))
                        distancias[ady[0]][ady[1]] = longitud
                        if ady not in temp: 
                            temp.append(list(ady))
                        if convert(ady) not in historial: 
                            historial.append(list(convert(ady))) 
                        if ady == invert(pos_final): 
                            return [False, False]
                        return [True, True]
                return [False, True]

            # sigue todas las posiciones del eje horizontal posibles hasta: pos_final[0]
            if not negativo_x:
                for i in range(dif_x):
                    ady = [pos[0] + i+1, pos[1]]
                    result = search(ady, d+i)
                    run = result[1]
                    if not result[0]: break
            else: 
                for i in range(abs(dif_x)):
                    ady = [pos[0] - i-1, pos[1]]
                    result = search(ady, d+i)
                    run = result[1]
                    if not result[0]: break
            # sigue todas las posiciones del eje vertical posibles hasta: pos_final[1]
            if run:
                if not negativo_y:
                    for i in range(dif_y):
                        ady = [pos[0], pos[1] + i+1]
                        result = search(ady, d+i)
                        run = result[1]
                        if not result[0]: break
                else: 
                    for i in range(abs(dif_y)):
                        ady = [pos[0], pos[1] - i-1]
                        result = search(ady, d+i)
                        run = result[1]
                        if not result[0]: break
            # sgue investigando los adyacentes a los activos por si hay que retroceder para encontrar el camino
            if run:
                for ady in [[pos[0]+1, pos[1]], [pos[0], pos[1]+1], [pos[0]-1, pos[1]], [pos[0], pos[1]-1]]:
                    result = search(ady, d)
                    run = result[1]

            if not run: break

        if temp == []: run = False
        activos = temp

        # print(distancias, "\n"*20)

        actualizar_screen(5, historial, adyacencias)
        pygame.display.flip()
        adyacencias.clear()

    # backtracking para recuperar el camino
    def backtracking():
        d = distancias[invert(pos_final)[0]][invert(pos_final)[1]]
        camino = []
        pos = invert(pos_final)
        while d != 1:
            encontrado = False
            for ady in [[pos[0]+1, pos[1]], [pos[0], pos[1]+1], [pos[0]-1, pos[1]], [pos[0], pos[1]-1]]:
                if not encontrado and ady[0] >= 0 and ady[0] < NX and ady[1] >= 0 and ady[1] < NY:
                    if distancias[ady[0]][ady[1]] == d-1:
                        camino.insert(0, list(convert(ady)))
                        encontrado = True
                        pos = ady
            d -= 1

        # pintar el camino
        actualizar_screen(50, historial)
        for pos in camino:
            pygame.draw.rect(play_surface, COLOR_CAMINO, pygame.Rect(pos[0], pos[1], DIM, DIM))
        pygame.display.flip()
        pygame.time.wait(1000)

    if distancias[invert(pos_final)[0]][invert(pos_final)[1]] != "i":
        backtracking()


def main():

    run = True
    buscar = False
    pausa = False

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # poner y quitar muros
            if pygame.mouse.get_pressed()[0]: # right
                pos = pygame.mouse.get_pos()
                x, y = pos[0] // DIM, pos[1] // DIM
                x, y = DIM*x, DIM*y
                if [x,y] not in paredes: 
                    paredes.append(list([x, y]))

            if pygame.mouse.get_pressed()[2]: # left
                pos = pygame.mouse.get_pos()
                x, y = pos[0] // DIM, pos[1] // DIM
                x, y = DIM*x, DIM*y
                if [x,y] in paredes: 
                    paredes.remove(list([x, y]))

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    paredes.clear()

                if event.key == pygame.K_SPACE:
                    if pausa:
                        pausa = False
                    else:
                        algoritmo_busqueda()
                        pausa = True

        if not pausa:
            actualizar_screen(50)
            pygame.display.flip()


main()
pygame.quit()