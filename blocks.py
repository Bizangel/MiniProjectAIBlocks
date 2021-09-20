from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from numpy import source


class MundoBloques:
    Labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
    Colors = ["orange", "lightblue", "purple", "red", "yellow", "green", "gray", "teal", "lightsalmon", "limegreen", "tan", "gold", "navy"]

    def __init__(self, estado_inicial, target, tableroLength, tableroHeight):
        # Pos de cada Caja por indice Sample
        # 0 top, 2 tocando el piso
        # 0 left - 2 right
        # [(2,1),(2,0),(1,1)] estado ref imagen
        self.estado_inicial = estado_inicial
        self.target = target
        self.tableroLength = tableroLength
        self.tableroHeight = tableroHeight

    def acciones_aplicables(self, estado):
        # Cada acción esta simbolizada por una tupla (bloque, posicion)
        # Por ejemplo (1,2), consiste en mover el bloque de indice 1 (B) a la posición 2 en el piso

        # Considera el bloque que este más arriba
        # Tiene los indices de los bloques superiores, según posicion
        top_pos_blocks = []
        for pos in range(self.tableroLength):
            best_top_block = None
            for block_index in range(len(estado)):
                block = estado[block_index]
                if block[1] == pos:
                    if best_top_block is None:
                        best_top_block = block_index
                    else:
                        if (estado[best_top_block][0] > block[0]):  # not truly best block
                            best_top_block = block_index
            top_pos_blocks.append(best_top_block)

        # Every possible action, is moving a top block, to all different positions than itself
        poss_actions = []
        for block_index in top_pos_blocks:
            if block_index is not None:
                for pos in range(self.tableroLength):
                    if pos != estado[block_index][1]:
                        poss_actions.append((block_index, pos))
        return poss_actions

    def transicion(self, estado, accion):
        # Recibe accion de la forma (bloque, pos)
        # Mueve el bloque a la posición, retorna un nuevo estado
        block_index, pos = accion
        # encontrar el bloque más alto de esa posición
        topmostblock = float("inf")
        for block in estado:
            if block[1] == pos:
                if block[0] < topmostblock:
                    topmostblock = block[0]

        if topmostblock == float("inf"):
            # no blocks, place on floor
            blockheight = self.tableroHeight - 1
        else:
            blockheight = topmostblock - 1  # set atop block
        new_block = (blockheight, pos)
        new_state = []
        # Recreate state
        for index in range(len(estado)):
            if index == block_index:
                new_state.append(new_block)
            else:
                new_state.append(estado[index])  # just copy

        return new_state

    def test_objetivo(self, estado):
        return estado == self.target

    def costo(self, estado, accion):
        return 1

    def codigo(self, estado):
        buildstr = ''
        for i in range(len(estado)):
            buildstr += MundoBloques.Labels[i] + \
                "{0}-{1}|".format(estado[i][0], estado[i][1])
        return buildstr

    def PintarEstado(self, estado, filename=None):
        source_img = Image.new(
            "RGBA", (self.tableroLength*100, self.tableroHeight*100))

        def drawBlock(xtop, ytop, letter, color):
            draw = ImageDraw.Draw(source_img)
            draw.rectangle(
                ((xtop*100, ytop*100), (xtop*100+100, ytop*100+100)), fill=color)
            myfont = ImageFont.truetype(
                'Roboto-Regular.ttf', 50)
            draw.text((xtop*100+33, ytop*100+20), letter, font=myfont)

        for i in range(len(estado)):
            y, x = estado[i]
            color = MundoBloques.Colors[i]
            label = MundoBloques.Labels[i]
            drawBlock(x, y, label, color)

        if filename is not None:
            source_img.save(filename, "png")
        return source_img

    def PintarTransiciones(self, estadolist, filename=None):
        # Pinta todas los movimientos en una sola imagen, añadiendo el estado inicial
        canva = Image.new("RGBA", ((len(estadolist)+1)*self.tableroHeight *
                                   100 + (len(estadolist))*20, self.tableroHeight*100))
        canva.paste(self.PintarEstado(self.estado_inicial), (0, 0))
        draw = ImageDraw.Draw(canva)

        for i in range(1, len(estadolist)+1):
            estado = estadolist[i-1]
            canva.paste(self.PintarEstado(estado),
                        (i*self.tableroHeight*100 + 20*i, 0))
            draw.rectangle(
                ((100*i*self.tableroLength+(20*(i-1)), 0), (100*i*self.tableroLength+20+(20*(i-1)), 100*self.tableroHeight)), fill="black")

        if filename is not None:
            canva.save(filename, "png")
        return canva

    def PintarTransicionesGif(self, estadolist, filename, frameSeconds=1):
        images = [self.PintarEstado(estado) for estado in estadolist]
        start = (self.PintarEstado(self.estado_inicial))
        start.save(filename, save_all=True, append_images=images,
                   optimize=False, duration=frameSeconds*1000, loop=0)


if __name__ == "__main__":
    from busqueda import *
    prob = MundoBloques([(2, 1), (2, 0), (1, 1)], [(0, 2), (1, 2), (2, 2)])
    x = iterative_deepening_search(prob, l_max=5)
    nodos = find_path(x)
    estadolist = [nod.estado for nod in nodos]
    # prob.PintarTransiciones(estadolist, "transiciones.png")
    prob.PintarTransicionesGif(estadolist, "out.gif")

    # prob.PintarEstado(prob.estado_inicial, "mov0.png")
    # for i in range(len(moves)):
    #     prob.PintarEstado(moves[i].estado, "mov" + str(i+1) + ".png")

    s1 = prob.estado_inicial
    acciones = prob.acciones_aplicables(s1)
    s2 = prob.transicion(s1, acciones[3])
    acciones = prob.acciones_aplicables(s2)
    s3 = prob.transicion(s2, acciones[1])
    acciones = prob.acciones_aplicables(s3)
    s4 = prob.transicion(s3, acciones[1])   
    print(prob.test_objetivo(s4))
    prob.PintarEstado(s4)
