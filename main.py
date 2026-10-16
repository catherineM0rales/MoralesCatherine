import arcade

from configuracion import ANCHO, ALTO, TITULO
from nivel4 import Nivel4


def main():
    ventana = arcade.Window(ANCHO, ALTO, TITULO)
    ventana.show_view(Nivel4())
    arcade.run()


if __name__ == "__main__":
    main()