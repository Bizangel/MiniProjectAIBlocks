
from PIL import Image, ImageFont, ImageDraw, ImageEnhance


class MundoBloques:
    def __init__(self, estado_inicial, target):
        # Pos de cada Caja por indice Sample
        # 0 top, 2 tocando el piso
        # 0 left - 2 right
        # [(2,1),(2,0),(1,1)] estado ref imagen
        self.estado_inicial = estado_inicial
        self.target = target

    def acciones_aplicables(self, estado):

        pass

    def transicion(self, estado, accion):
        pass

    def test_objetivo(self):
        # is target or not
        pass

    def costo(self):
        return 1

    def PintarEstado(self):

        source_img = Image.new("RGBA", (200, 200))
        draw = ImageDraw.Draw(source_img)
        draw.rectangle(((0, 00), (100, 100)), fill="black")
        draw.text((20, 70), "something123",
                  font=ImageFont.truetype("font_path123"))

        source_img.save(out_file, "JPEG")


if __name__ == "__main__":
    print("read")
