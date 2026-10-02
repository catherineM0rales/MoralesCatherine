import arcade

from configuracion import *
from nombre import PantallaNombre


class Menu(arcade.View):

    def __init__(self):
        super().__init__()

        self.opcion = 0

        # ============================================================
        # CÁMARA DEL MENÚ
        # ============================================================

        self.camera = arcade.Camera2D()
        self.camera.position = (ANCHO / 2, ALTO / 2)
        self.camera.zoom = 1

        # ============================================================
        # IMÁGENES DEL MENÚ
        # ============================================================

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

        self.niveles = arcade.load_texture(
            "imagenes/menu/niveles.png"
        )

        self.niveles_sel = arcade.load_texture(
            "imagenes/menu/niveles_seleccionado.png"
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

        self.imagen_controles = arcade.load_texture(
            "imagenes/menu/controles_pantalla.png"
        )

        # ============================================================
        # ESTADOS DEL MENÚ
        # ============================================================

        self.mostrando_controles = False
        self.mostrando_niveles = False
        self.nivel_opcion = 0

    # ================================================================
    # DIBUJAR TEXTURA AJUSTADA
    # ================================================================

    def dibujar_textura_ajustada(
        self,
        textura,
        x,
        y,
        ancho_max
    ):
        escala = ancho_max / textura.width

        ancho = textura.width * escala
        alto = textura.height * escala

        arcade.draw_texture_rect(
            textura,
            arcade.LBWH(
                x - ancho / 2,
                y - alto / 2,
                ancho,
                alto
            )
        )

    # ================================================================
    # DIBUJAR MENÚ
    # ================================================================

    def on_draw(self):

        self.clear()

        # ============================================================
        # RESTABLECER LA CÁMARA
        # ============================================================

        self.camera.position = (
            ANCHO / 2,
            ALTO / 2
        )

        self.camera.zoom = 1

        self.camera.use()

        # ============================================================
        # FONDO
        # ============================================================

        arcade.draw_texture_rect(
            self.fondo,
            arcade.LBWH(
                0,
                0,
                ANCHO,
                ALTO
            )
        )

        # ============================================================
        # PANTALLA DE SELECCIÓN DE NIVELES
        # ============================================================

        if self.mostrando_niveles:

            arcade.draw_lrbt_rectangle_filled(
                200,
                ANCHO - 200,
                100,
                ALTO - 100,
                (0, 0, 0, 210)
            )

            arcade.draw_text(
                "SELECCIONAR NIVEL",
                ANCHO // 2,
                ALTO - 180,
                arcade.color.WHITE,
                38,
                anchor_x="center"
            )

            # NIVEL 1
            color_nivel1 = (
                arcade.color.YELLOW
                if self.nivel_opcion == 0
                else arcade.color.WHITE
            )

            arcade.draw_text(
                "NIVEL 1",
                ANCHO // 2,
                470,
                color_nivel1,
                30,
                anchor_x="center"
            )

            # NIVEL 2
            color_nivel2 = (
                arcade.color.YELLOW
                if self.nivel_opcion == 1
                else arcade.color.WHITE
            )

            arcade.draw_text(
                "NIVEL 2",
                ANCHO // 2,
                390,
                color_nivel2,
                30,
                anchor_x="center"
            )

            # NIVEL 3
            color_nivel3 = (
                arcade.color.YELLOW
                if self.nivel_opcion == 2
                else arcade.color.WHITE
            )

            arcade.draw_text(
                "NIVEL 3",
                ANCHO // 2,
                310,
                color_nivel3,
                30,
                anchor_x="center"
            )

            # VOLVER
            color_volver = (
                arcade.color.YELLOW
                if self.nivel_opcion == 3
                else arcade.color.WHITE
            )

            arcade.draw_text(
                "VOLVER",
                ANCHO // 2,
                210,
                color_volver,
                26,
                anchor_x="center"
            )

            arcade.draw_text(
                "↑ ↓  Seleccionar     ENTER  Entrar     ESC  Volver",
                ANCHO // 2,
                135,
                arcade.color.LIGHT_GRAY,
                18,
                anchor_x="center"
            )

            return

        # ============================================================
        # PANTALLA DE CONTROLES
        # ============================================================

        if self.mostrando_controles:

            self.dibujar_textura_ajustada(
                self.imagen_controles,
                ANCHO // 2,
                ALTO // 2,
                ANCHO
            )

            arcade.draw_text(
                "ESC  Volver",
                ANCHO // 2,
                25,
                arcade.color.WHITE,
                18,
                anchor_x="center"
            )

            return

        # ============================================================
        # LOGO
        # ============================================================

        self.dibujar_textura_ajustada(
            self.logo,
            ANCHO // 2,
            ALTO - 150,
            600
        )

        # ============================================================
        # JUGAR
        # ============================================================

        textura_jugar = (
            self.jugar_sel
            if self.opcion == 0
            else self.jugar
        )

        self.dibujar_textura_ajustada(
            textura_jugar,
            ANCHO // 2,
            390,
            240
        )

        # ============================================================
        # NIVELES
        # ============================================================

        textura_niveles = (
            self.niveles_sel
            if self.opcion == 1
            else self.niveles
        )

        self.dibujar_textura_ajustada(
            textura_niveles,
            ANCHO // 2,
            320,
            240
        )

        # ============================================================
        # CONTROLES
        # ============================================================

        textura_controles = (
            self.controles_sel
            if self.opcion == 2
            else self.controles
        )

        self.dibujar_textura_ajustada(
            textura_controles,
            ANCHO // 2,
            230,
            270
        )

        # ============================================================
        # SALIR
        # ============================================================

        textura_salir = (
            self.salir_sel
            if self.opcion == 3
            else self.salir
        )

        self.dibujar_textura_ajustada(
            textura_salir,
            ANCHO // 2,
            140,
            240
        )

    # ================================================================
    # TECLAS
    # ================================================================

    def on_key_press(self, key, modifiers):

        # ============================================================
        # SELECCIÓN DE NIVELES
        # ============================================================

        if self.mostrando_niveles:

            if key == arcade.key.UP:

                self.nivel_opcion -= 1
                self.nivel_opcion %= 4

            elif key == arcade.key.DOWN:

                self.nivel_opcion += 1
                self.nivel_opcion %= 4

            elif key == arcade.key.ENTER:

                # NIVEL 1
                if self.nivel_opcion == 0:

                    import nivel1

                    self.window.show_view(
                        nivel1.Nivel1()
                    )

                # NIVEL 2
                elif self.nivel_opcion == 1:

                    import nivel2

                    self.window.show_view(
                        nivel2.Nivel2()
                    )

                # NIVEL 3
                elif self.nivel_opcion == 2:

                    import nivel3

                    self.window.show_view(
                        nivel3.Nivel3()
                    )

                # VOLVER
                elif self.nivel_opcion == 3:

                    self.mostrando_niveles = False
                    self.opcion = 0

            elif key == arcade.key.ESCAPE:

                self.mostrando_niveles = False
                self.opcion = 0

            return

        # ============================================================
        # CONTROLES
        # ============================================================

        if self.mostrando_controles:

            if key == arcade.key.ENTER:
                self.mostrando_controles = False

            elif key == arcade.key.ESCAPE:
                self.mostrando_controles = False

            return

        # ============================================================
        # MENÚ PRINCIPAL
        # ============================================================

        if key == arcade.key.UP:

            self.opcion -= 1

        elif key == arcade.key.DOWN:

            self.opcion += 1

        self.opcion %= 4

        # ============================================================
        # ENTER
        # ============================================================

        if key == arcade.key.ENTER:

            # JUGAR
            if self.opcion == 0:

                pantalla_nombre = PantallaNombre()

                self.window.show_view(
                    pantalla_nombre
                )

            # NIVELES
            elif self.opcion == 1:

                self.mostrando_niveles = True
                self.nivel_opcion = 0

            # CONTROLES
            elif self.opcion == 2:

                self.mostrando_controles = True

            # SALIR
            elif self.opcion == 3:

                arcade.exit()