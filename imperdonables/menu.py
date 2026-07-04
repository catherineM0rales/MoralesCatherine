import arcade

from configuracion import *
from nombre import PantallaNombre

class Menu(arcade.View):

    def __init__(self):

        super().__init__()

        self.opcion = 0

        self.opciones = [

            "JUGAR",

            "SALIR"

        ]

    def on_draw(self):

        self.clear()

        arcade.draw_text(

            TITULO,

            ANCHO / 2,

            600,

            arcade.color.WHITE,

            40,

            anchor_x="center"

        )

        for i, opcion in enumerate(self.opciones):

            texto = opcion

            if i == self.opcion:

                texto = "> " + texto

            arcade.draw_text(

                texto,

                ANCHO / 2,

                420 - i * 60,

                arcade.color.WHITE,

                24,

                anchor_x="center"

            )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:

            self.opcion -= 1

        elif key == arcade.key.DOWN:

            self.opcion += 1

        self.opcion %= len(self.opciones)

        if key == arcade.key.ENTER:

            if self.opcion == 0:

                pantalla_nombre = PantallaNombre()
                self.window.show_view(pantalla_nombre)

            elif self.opcion == 1:

                arcade.exit()