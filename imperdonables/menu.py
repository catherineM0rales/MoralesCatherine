import arcade

from configuracion import *
from nombre import PantallaNombre

class Menu(arcade.View):

    def __init__(self):
        super().__init__()

        self.opcion = 0

        

        # Cargar imágenes
        self.fondo = arcade.load_texture("imagenes/menu/menu.png")
        self.logo = arcade.load_texture("imagenes/menu/titulo.png")

        self.jugar = arcade.load_texture("imagenes/menu/jugar.png")
        self.jugar_sel = arcade.load_texture("imagenes/menu/jugar_seleccionado.png")

        self.salir = arcade.load_texture("imagenes/menu/salir.png")
        self.salir_sel = arcade.load_texture("imagenes/menu/salir_seleccionado.png")

    def on_draw(self):

        self.clear()

        # ==========================
        # Fondo
        # ==========================
        arcade.draw_texture_rect(
            self.fondo,
            arcade.LBWH(
                0,
                0,
                ANCHO,
                ALTO
            )
        )

        # ==========================
        # Logo
        # ==========================
        arcade.draw_texture_rect(
            self.logo,
            arcade.LBWH(
                ANCHO // 2 - 320,
                ALTO - 340,
                850,
                230
            )
        )

        
        # ==========================
        # Botón Jugar
        # ==========================

        if self.opcion == 0:
            textura = self.jugar_sel
        else:
            textura = self.jugar

        arcade.draw_texture_rect(
            textura,
            arcade.LBWH(
                ANCHO // 2 - 140,
                225,
                360,
                120
            )
        )

        # ==========================
        # Botón Salir
        # ==========================

        if self.opcion == 1:
            textura = self.salir_sel
        else:
            textura = self.salir

        arcade.draw_texture_rect(
            textura,
            arcade.LBWH(
                ANCHO // 2 - 140,
                105,
                360,
                120
            )
        )
    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            self.opcion -= 1

        elif key == arcade.key.DOWN:
            self.opcion += 1

        self.opcion %= 2

        if key == arcade.key.ENTER:

            if self.opcion == 0:

                pantalla_nombre = PantallaNombre()
                self.window.show_view(pantalla_nombre)

            elif self.opcion == 1:

                arcade.exit()