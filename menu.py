import arcade

from configuracion import *
from nombre import PantallaNombre


class Menu(arcade.View):

    def __init__(self):
        super().__init__()
        self.musica = arcade.load_sound("musica/menu.mp3")

        # ==================================================
        # OPCIONES DEL MENÚ
        # ==================================================
        # 0 = Jugar
        # 1 = Controles
        # 2 = Salir

        self.opcion = 0
        #pone play a la musica
        arcade.play_sound(self.musica, volume=0.25, loop=True)
        # ==================================================
        # CARGAR IMÁGENES DEL MENÚ
        # ==================================================

        self.fondo = arcade.load_texture(
            "imagenes/menu/menu.png"
        )

        self.logo = arcade.load_texture(
            "imagenes/menu/titulo.png"
        )

        self.jugar = arcade.load_texture(
            "imagenes/menu/jugar.png"
        )

        self.jugar_sel = arcade.load_texture(
            "imagenes/menu/jugar_seleccionado.png"
        )

        self.controles = arcade.load_texture(
            "imagenes/menu/controles.png"
        )

        self.controles_sel = arcade.load_texture(
            "imagenes/menu/controles_seleccionado.png"
        )

        self.salir = arcade.load_texture(
            "imagenes/menu/salir.png"
        )

        self.salir_sel = arcade.load_texture(
            "imagenes/menu/salir_seleccionado.png"
        )

        # ==================================================
        # IMAGEN PERSONALIZADA DE CONTROLES
        # ==================================================

        self.imagen_controles = arcade.load_texture(
            "imagenes/menu/controles_pantalla.png"
        )

        # Saber si estamos dentro de la pantalla de controles
        self.mostrando_controles = False

    # ==========================================================
    # DIBUJAR IMAGEN SIN DEFORMARLA
    # ==========================================================

    def dibujar_textura_ajustada(
        self,
        textura,
        x,
        y,
        ancho_max
    ):

        # Calculamos la escala usando el ancho original
        # de la imagen.

        escala = ancho_max / textura.width

        ancho = textura.width * escala
        alto = textura.height * escala

        # Dibujamos la imagen centrada.

        arcade.draw_texture_rect(
            textura,
            arcade.LBWH(
                x - ancho / 2,
                y - alto / 2,
                ancho,
                alto
            )
        )

    # ==========================================================
    # DIBUJAR MENÚ
    # ==========================================================

    def on_draw(self):

        self.clear()

        # ==================================================
        # FONDO DEL MENÚ
        # ==================================================

        arcade.draw_texture_rect(
            self.fondo,
            arcade.LBWH(
                0,
                0,
                ANCHO,
                ALTO
            )
        )

        # ==================================================
        # PANTALLA PERSONALIZADA DE CONTROLES
        # ==================================================

        if self.mostrando_controles:

            self.dibujar_textura_ajustada(
                self.imagen_controles,
                ANCHO // 2,
                ALTO // 2,
                ANCHO
            )

            return

        # ==================================================
        # LOGO
        # ==================================================

        self.dibujar_textura_ajustada(
            self.logo,
            ANCHO // 2,
            ALTO - 170,
            600
        )

        # ==================================================
        # BOTÓN JUGAR
        # ==================================================

        textura_jugar = (
            self.jugar_sel
            if self.opcion == 0
            else self.jugar
        )

        self.dibujar_textura_ajustada(
            textura_jugar,
            ANCHO // 2,
            350,
            240
        )

        # ==================================================
        # BOTÓN CONTROLES
        # ==================================================

        textura_controles = (
            self.controles_sel
            if self.opcion == 1
            else self.controles
        )

        self.dibujar_textura_ajustada(
            textura_controles,
            ANCHO // 2,
            245,
            270
        )

        # ==================================================
        # BOTÓN SALIR
        # ==================================================

        textura_salir = (
            self.salir_sel
            if self.opcion == 2
            else self.salir
        )

        self.dibujar_textura_ajustada(
            textura_salir,
            ANCHO // 2,
            140,
            240
        )

    # ==========================================================
    # CONTROLES DEL TECLADO
    # ==========================================================

    def on_key_press(self, key, modifiers):

        # ==================================================
        # SI ESTAMOS EN LA PANTALLA DE CONTROLES
        # ==================================================

        if self.mostrando_controles:

            if key == arcade.key.ENTER:

                self.mostrando_controles = False

            return

        # ==================================================
        # MOVER HACIA ARRIBA
        # ==================================================

        if key == arcade.key.UP:

            self.opcion -= 1

        # ==================================================
        # MOVER HACIA ABAJO
        # ==================================================

        elif key == arcade.key.DOWN:

            self.opcion += 1

        # Mantener la opción entre 0 y 2.

        self.opcion %= 3

        # ==================================================
        # ENTER
        # ==================================================

        if key == arcade.key.ENTER:

            # ----------------------------------------------
            # JUGAR
            # ----------------------------------------------

            if self.opcion == 0:

                pantalla_nombre = PantallaNombre()

                self.window.show_view(
                    pantalla_nombre
                )

            # ----------------------------------------------
            # CONTROLES
            # ----------------------------------------------

            elif self.opcion == 1:

                self.mostrando_controles = True

            # ----------------------------------------------
            # SALIR
            # ----------------------------------------------

            elif self.opcion == 2:

                arcade.exit()