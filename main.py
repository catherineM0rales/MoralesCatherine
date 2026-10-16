import arcade

from configuracion import *
from menu import Menu


def main():

    ventana = arcade.Window(
        ANCHO,
        ALTO,
        TITULO
    )

    menu = Menu()

    ventana.show_view(menu)

    arcade.run()


if _name_ == "_main_":
    main()