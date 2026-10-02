import arcade
import configuracion
from entidades import Player
import nivel2


ANCHO_MAPA = 1536
ALTO_MAPA = 1024

SALIDA_X = 1430
MARGEN_MAPA = 30


# *==========================================================*
# *GUARDIA*
# *==========================================================*
class Guardia(arcade.Sprite):

    def __init__(self, x, y):

        super().__init__(
            "imagenes/personajes/enemigos/guardia.png",
            scale=0.15
        )

        self.center_x = x
        self.center_y = y

        self.velocidad = 1.5


# *==========================================================*
# *VILLANO DE INSEGURIDAD*
# *==========================================================*
class VillanoInseguridad(arcade.Sprite):

    def __init__(self, x, y):

        super().__init__(
            "imagenes/personajes/enemigos/villano.png",
            scale=0.15
        )

        self.center_x = x
        self.center_y = y

        self.velocidad = 1.2


# *==========================================================*
# *FRAGMENTO DE DIBUJO*
# *==========================================================*
class FragmentoDibujo(arcade.Sprite):

    def __init__(self, x, y):

        super().__init__(
            "imagenes/objetos/dibujo.png",
            scale=0.10
        )

        self.center_x = x
        self.center_y = y


# *==========================================================*
# *NIVEL 1*
# *==========================================================*
class Nivel1(arcade.View):

    def __init__(self):

        super().__init__()

        # *==================================================*
        # *MAPA*
        # *==================================================*

        self.mapa = arcade.load_texture(
            "imagenes/mapas/nivel_inseguridad.png"
        )

        # *==================================================*
        # *CÁMARAS*
        # *==================================================*

        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        # *==================================================*
        # *JUGADOR*
        # *==================================================*

        self.player = Player()

        self.player.center_x = 90
        self.player.center_y = 540

        self.velocidad = configuracion.VELOCIDAD_JUGADOR

        # *==================================================*
        # *GUARDIAS*
        # *==================================================*

        self.guardias = arcade.SpriteList()

        posiciones_guardias = [
            (400, 700),
            (400, 400),
            (700, 700),
            (700, 400),
            (1000, 700),
            (1000, 400),
            (1250, 700),
            (1250, 400)
        ]

        for x, y in posiciones_guardias:

            guardia = Guardia(x, y)

            self.guardias.append(guardia)

        # *==================================================*
        # *VILLANO*
        # *==================================================*

        self.villano = VillanoInseguridad(
            1430,
            540
        )

        # *==================================================*
        # *FRAGMENTOS*
        # *==================================================*

        self.fragmentos = arcade.SpriteList()

        posiciones_fragmentos = [
            (280, 780),
            (520, 350),
            (760, 760),
            (1010, 420),
            (1260, 760)
        ]

        for x, y in posiciones_fragmentos:

            fragmento = FragmentoDibujo(x, y)

            self.fragmentos.append(fragmento)

        # *==================================================*
        # *TECLAS*
        # *==================================================*

        self.teclas = set()

        # *==================================================*
        # *ESTADO DEL NIVEL*
        # *==================================================*

        self.fase = "caminar"

        self.tiempo = 0

        self.tiempo_camara = 0

        self.tiempo_mensaje = 0

        # *==================================================*
        # *PANTALLA DE NIVEL COMPLETADO*
        # *==================================================*

        # *0 = Siguiente nivel*
        # *1 = Volver al menú*

        self.opcion_final = 0

        # *==================================================*
        # *FRAGMENTOS RECOGIDOS*
        # *==================================================*

        self.fragmentos_recogidos = 0

        # *==================================================*
        # *OSCURECIMIENTO*
        # *==================================================*

        self.opacidad = 0

        self.fase_oscura = False

        # *==================================================*
        # *FASE DE INICIO*
        # *==================================================*

        self.tiempo_inicio = 0

    # *==========================================================*
    # *ACTUALIZAR*
    # *==========================================================*
    def on_update(self, delta_time):

        # *==================================================*
        # *SI EL NIVEL YA TERMINÓ*
        # *==================================================*

        if self.fase == "completado":
            return

        # *==================================================*
        # *ACTUALIZAR TIEMPOS*
        # *==================================================*

        self.tiempo += delta_time

        # *==================================================*
        # *FASE DE CAMINAR*
        # *==================================================*

        if self.fase == "caminar":

            self.tiempo_inicio += delta_time

            if self.tiempo_inicio >= 2:

                self.fase = "camara"

            return

        # *==================================================*
        # *FASE DE CÁMARA*
        # *==================================================*

        if self.fase == "camara":

            self.tiempo_camara += delta_time

            self.camera.position = (
                self.player.center_x,
                self.player.center_y
            )

            if self.tiempo_camara >= 3:

                self.fase = "espera_camara"

            return

        # *==================================================*
        # *ESPERA DE CÁMARA*
        # *==================================================*

        if self.fase == "espera_camara":

            if self.tiempo >= 5:

                self.fase = "regreso"

            return

        # *==================================================*
        # *REGRESO*
        # *==================================================*

        if self.fase == "regreso":

            self.tiempo_camara -= delta_time

            if self.tiempo_camara <= 0:

                self.fase = "instrucciones"

            return

        # *==================================================*
        # *INSTRUCCIONES*
        # *==================================================*

        if self.fase == "instrucciones":

            return

        # *==================================================*
        # *JUGANDO*
        # *==================================================*

        if self.fase != "jugando":

            return

        # *==================================================*
        # *MOVIMIENTO*
        # *==================================================*

        dx = 0
        dy = 0

        if arcade.key.W in self.teclas:
            dy += 1

        if arcade.key.S in self.teclas:
            dy -= 1

        if arcade.key.A in self.teclas:
            dx -= 1

        if arcade.key.D in self.teclas:
            dx += 1

        if arcade.key.UP in self.teclas:
            dy += 1

        if arcade.key.DOWN in self.teclas:
            dy -= 1

        if arcade.key.LEFT in self.teclas:
            dx -= 1

        if arcade.key.RIGHT in self.teclas:
            dx += 1

        # *==================================================*
        # *NORMALIZAR MOVIMIENTO*
        # *==================================================*

        if dx != 0 and dy != 0:

            velocidad_movimiento = self.velocidad / 1.414

        else:

            velocidad_movimiento = self.velocidad

        # *==================================================*
        # *MOVER JUGADOR*
        # *==================================================*

        self.player.center_x += (
            dx * velocidad_movimiento
        )

        self.player.center_y += (
            dy * velocidad_movimiento
        )

        # *==================================================*
        # *LIMITES DEL MAPA*
        # *==================================================*

        if self.player.center_x < MARGEN_MAPA:

            self.player.center_x = MARGEN_MAPA

        if self.player.center_x > ANCHO_MAPA - MARGEN_MAPA:

            self.player.center_x = (
                ANCHO_MAPA - MARGEN_MAPA
            )

        if self.player.center_y < MARGEN_MAPA:

            self.player.center_y = MARGEN_MAPA

        if self.player.center_y > ALTO_MAPA - MARGEN_MAPA:

            self.player.center_y = (
                ALTO_MAPA - MARGEN_MAPA
            )

        # *==================================================*
        # *ANIMACIÓN DEL JUGADOR*
        # *==================================================*

        self.player.update_animation(
            dx,
            dy
        )

        # *==================================================*
        # *ACTUALIZAR CÁMARA*
        # *==================================================*

        self.camera.position = (
            self.player.center_x,
            self.player.center_y
        )

        # *==================================================*
        # *RECOGER FRAGMENTOS*
        # *==================================================*

        for fragmento in list(self.fragmentos):

            if arcade.check_for_collision(
                self.player,
                fragmento
            ):

                fragmento.remove_from_sprite_lists()

                self.fragmentos_recogidos += 1

        # *==================================================*
        # *OSCURECIMIENTO*
        # *==================================================*

        if self.fase_oscura:

            self.opacidad += 5

            if self.opacidad >= 180:

                self.opacidad = 180

        else:

            self.opacidad -= 5

            if self.opacidad <= 0:

                self.opacidad = 0

        # *==================================================*
        # *SALIDA*
        # *==================================================*

        if self.player.center_x >= SALIDA_X:

            # *------------------------------------------------*
            # *SI TODAVÍA FALTAN FRAGMENTOS*
            # *------------------------------------------------*

            if self.fragmentos_recogidos < 5:

                self.player.center_x = SALIDA_X - 20

                return

            # *------------------------------------------------*
            # *SI YA TIENE LOS 5 FRAGMENTOS*
            # *------------------------------------------------*

            self.teclas.clear()

            self.fase = "completado"

            self.opcion_final = 0

            return

    # *==========================================================*
    # *PRESIONAR TECLA*
    # *==========================================================*
    def on_key_press(self, key, modifiers):

        # *==================================================*
        # *PANTALLA DE NIVEL COMPLETADO*
        # *==================================================*

        if self.fase == "completado":

            # *----------------------------------------------*
            # *SELECCIONAR SIGUIENTE NIVEL*
            # *----------------------------------------------*

            if key == arcade.key.UP:

                self.opcion_final = 0

            # *----------------------------------------------*
            # *SELECCIONAR MENÚ*
            # *----------------------------------------------*

            elif key == arcade.key.DOWN:

                self.opcion_final = 1

            # *----------------------------------------------*
            # *ENTER*
            # *----------------------------------------------*

            elif key == arcade.key.ENTER:

                # *------------------------------------------*
                # *SIGUIENTE NIVEL*
                # *------------------------------------------*

                if self.opcion_final == 0:

                    self.window.show_view(
                        nivel2.Nivel2()
                    )

                # *------------------------------------------*
                # *VOLVER AL MENÚ*
                # *------------------------------------------*

                else:

                    from menu import Menu

                    self.window.show_view(
                        Menu()
                    )

            return

        # *==================================================*
        # *INSTRUCCIONES*
        # *==================================================*

        if self.fase == "instrucciones":

            if key == arcade.key.ENTER:

                self.fase = "jugando"

            return

        # *==================================================*
        # *TECLAS PRESIONADAS*
        # *==================================================*

        self.teclas.add(key)

    # *==========================================================*
    # *SOLTAR TECLA*
    # *==========================================================*
    def on_key_release(self, key, modifiers):

        if key in self.teclas:

            self.teclas.remove(key)

    # *==========================================================*
    # *DIBUJAR*
    # *==========================================================*
    def on_draw(self):

        self.clear()

        # *==================================================*
        # *CÁMARA DEL MAPA*
        # *==================================================*

        self.camera.use()

        # *==================================================*
        # *MAPA*
        # *==================================================*

        arcade.draw_texture_rect(
            self.mapa,
            arcade.LBWH(
                0,
                0,
                ANCHO_MAPA,
                ALTO_MAPA
            )
        )

        # *==================================================*
        # *FRAGMENTOS*
        # *==================================================*

        self.fragmentos.draw()

        # *==================================================*
        # *GUARDIAS*
        # *==================================================*

        self.guardias.draw()

        # *==================================================*
        # *VILLANO*
        # *==================================================*

        self.villano.draw()

        # *==================================================*
        # *JUGADOR*
        # *==================================================*

        self.player.draw()

        # *==================================================*
        # *OSCURECIMIENTO*
        # *==================================================*

        if self.opacidad > 0:

            arcade.draw_lrbt_rectangle_filled(
                self.player.center_x - configuracion.ANCHO / 2,
                self.player.center_x + configuracion.ANCHO / 2,
                self.player.center_y - configuracion.ALTO / 2,
                self.player.center_y + configuracion.ALTO / 2,
                (0, 0, 0, self.opacidad)
            )

        # *==================================================*
        # *CÁMARA DE INTERFAZ*
        # *==================================================*

        self.gui_camera.use()

        # *==================================================*
        # *HUD*
        # *==================================================*

        arcade.draw_text(
            f"Fragmentos: {self.fragmentos_recogidos}/5",
            25,
            configuracion.ALTO - 45,
            arcade.color.WHITE,
            22
        )

        # *==================================================*
        # *INSTRUCCIONES*
        # *==================================================*

        if self.fase == "instrucciones":

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                configuracion.ALTO,
                (0, 0, 0, 190)
            )

            arcade.draw_text(
                "NIVEL 1",
                configuracion.ANCHO / 2,
                540,
                arcade.color.WHITE,
                40,
                bold=True,
                anchor_x="center"
            )

            arcade.draw_text(
                "Encontrá los fragmentos del dibujo.",
                configuracion.ANCHO / 2,
                470,
                arcade.color.WHITE,
                24,
                anchor_x="center"
            )

            arcade.draw_text(
                "Movete con WASD o las flechas.",
                configuracion.ANCHO / 2,
                420,
                arcade.color.LIGHT_GRAY,
                20,
                anchor_x="center"
            )

            arcade.draw_text(
                "Presioná ENTER para comenzar.",
                configuracion.ANCHO / 2,
                340,
                arcade.color.YELLOW,
                22,
                anchor_x="center"
            )

            return

        # *==================================================*
        # *PANTALLA DE NIVEL COMPLETADO*
        # *==================================================*

        if self.fase == "completado":

            # *----------------------------------------------*
            # *FONDO OSCURO*
            # *----------------------------------------------*

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                configuracion.ALTO,
                (0, 0, 0, 220)
            )

            # *----------------------------------------------*
            # *VENTANA*
            # *----------------------------------------------*

            arcade.draw_lrbt_rectangle_filled(
                250,
                configuracion.ANCHO - 250,
                180,
                configuracion.ALTO - 180,
                (25, 25, 35)
            )

            # *----------------------------------------------*
            # *BORDE*
            # *----------------------------------------------*

            arcade.draw_lrbt_rectangle_outline(
                250,
                configuracion.ANCHO - 250,
                180,
                configuracion.ALTO - 180,
                arcade.color.GOLD,
                3
            )

            # *----------------------------------------------*
            # *TÍTULO*
            # *----------------------------------------------*

            arcade.draw_text(
                "NIVEL COMPLETADO",
                configuracion.ANCHO / 2,
                550,
                arcade.color.GOLD,
                36,
                bold=True,
                anchor_x="center"
            )

            # *----------------------------------------------*
            # *PREGUNTA*
            # *----------------------------------------------*

            arcade.draw_text(
                "¿Qué querés hacer?",
                configuracion.ANCHO / 2,
                470,
                arcade.color.WHITE,
                24,
                anchor_x="center"
            )

            # *----------------------------------------------*
            # *SIGUIENTE NIVEL*
            # *----------------------------------------------*

            color_siguiente = (
                arcade.color.YELLOW
                if self.opcion_final == 0
                else arcade.color.WHITE
            )

            arcade.draw_text(
                "[ SIGUIENTE NIVEL ]",
                configuracion.ANCHO / 2,
                370,
                color_siguiente,
                25,
                bold=True,
                anchor_x="center"
            )

            # *----------------------------------------------*
            # *VOLVER AL MENÚ*
            # *----------------------------------------------*

            color_menu = (
                arcade.color.YELLOW
                if self.opcion_final == 1
                else arcade.color.WHITE
            )

            arcade.draw_text(
                "[ VOLVER AL MENÚ ]",
                configuracion.ANCHO / 2,
                290,
                color_menu,
                25,
                bold=True,
                anchor_x="center"
            )

            # *----------------------------------------------*
            # *AYUDA*
            # *----------------------------------------------*

            arcade.draw_text(
                "↑ ↓  Seleccionar     ENTER  Confirmar",
                configuracion.ANCHO / 2,
                220,
                arcade.color.LIGHT_GRAY,
                17,
                anchor_x="center"
            )

            return