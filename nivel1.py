
import arcade
import configuracion
from entidades import Player
import nivel2

ANCHO_MAPA = 1536
ALTO_MAPA = 1024
SALIDA_X = 1430
MARGEN_MAPA = 30

POSICION_INICIAL_JUGADOR = (90, 540)

POSICIONES_FRAGMENTOS = [
    (280, 780),
    (520, 350),
    (760, 760),
    (1010, 420),
    (1260, 760)
]


class Guardia(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__(
            "imagenes/personajes/enemigos/guardia.png",
            scale=0.12
        )

        self.center_x = x
        self.center_y = y

        self.limite_superior = y + 75
        self.limite_inferior = y - 75

        self.velocidad = 42
        self.direccion_y = 1


class FragmentoDibujo(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__(
            "imagenes/objetos/dibujo.png",
            scale=0.10
        )

        self.center_x = x
        self.center_y = y


class Nivel1(arcade.View):

    def __init__(self):
        super().__init__()

        # MAPA
        self.mapa = arcade.load_texture(
            "imagenes/mapas/nivel_inseguridad.png"
        )

        # CÁMARAS
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        # JUGADOR
        self.player = Player()

        self.jugadores = arcade.SpriteList()
        self.jugadores.append(self.player)

        self.player.center_x = POSICION_INICIAL_JUGADOR[0]
        self.player.center_y = POSICION_INICIAL_JUGADOR[1]

        self.velocidad = configuracion.VELOCIDAD_JUGADOR

        # GUARDIAS
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

        for indice, (x, y) in enumerate(posiciones_guardias):
            guardia = Guardia(x, y)

            guardia.velocidad = 34 + (indice % 4) * 9

            guardia.direccion_y = (
                1 if indice % 2 == 0 else -1
            )

            self.guardias.append(guardia)

        # FRAGMENTOS
        self.fragmentos = arcade.SpriteList()
        self.crear_fragmentos()

        self.fragmentos_recogidos = 0

        # TECLAS
        self.teclas = set()

        # INTRODUCCIÓN DE CÁMARA
        self.fase = "camara_intro"

        self.tiempo = 0
        self.tiempo_camara = 0

        self.duracion_recorrido_camara = 4.5

        self.camara_inicio_x = configuracion.ANCHO / 2

        self.camara_final_x = (
            ANCHO_MAPA - configuracion.ANCHO / 2
        )

        self.camera.position = (
            self.camara_inicio_x,
            ALTO_MAPA / 2
        )

        self.tiempo_mensaje = 0

        # PANTALLA FINAL
        self.opcion_final = 0

        # OSCURECIMIENTO
        self.opacidad = 0
        self.fase_oscura = False
        self.tiempo_inicio = 0

        # TRANSICIÓN NEGRA AL RECOGER LOS CINCO FRAGMENTOS
        self.transicion_activa = False
        self.tiempo_transicion = 0
        self.duracion_transicion = 1.0
        self.enemigos_eliminados = False

    # CREAR FRAGMENTOS
    def crear_fragmentos(self):

        self.fragmentos = arcade.SpriteList()

        for x, y in POSICIONES_FRAGMENTOS:
            fragmento = FragmentoDibujo(x, y)
            self.fragmentos.append(fragmento)

    # REINICIAR JUGADOR Y FRAGMENTOS
    def reiniciar_por_contacto(self):

        self.player.center_x = POSICION_INICIAL_JUGADOR[0]
        self.player.center_y = POSICION_INICIAL_JUGADOR[1]

        self.crear_fragmentos()
        self.fragmentos_recogidos = 0

        self.teclas.clear()

        self.camera.position = (
            self.player.center_x,
            self.player.center_y
        )

    # ACTUALIZAR MOVIMIENTO DE ENEMIGOS
    def actualizar_enemigos(self, delta_time):

        for enemigo in self.guardias:

            enemigo.center_y += (
                enemigo.velocidad *
                enemigo.direccion_y *
                delta_time
            )

            if enemigo.center_y >= enemigo.limite_superior:

                enemigo.center_y = enemigo.limite_superior
                enemigo.direccion_y = -1

            elif enemigo.center_y <= enemigo.limite_inferior:

                enemigo.center_y = enemigo.limite_inferior
                enemigo.direccion_y = 1

    # ACTUALIZAR
    def on_update(self, delta_time):

        if self.fase == "completado":
            return

        self.tiempo += delta_time

        # TRANSICIÓN NEGRA
        if self.transicion_activa:

            self.tiempo_transicion += delta_time
            mitad = self.duracion_transicion / 2

            # Primera mitad: la pantalla se apaga.
            if self.tiempo_transicion <= mitad:

                self.opacidad = min(
                    255,
                    int(255 * self.tiempo_transicion / mitad)
                )

            # Segunda mitad: desaparecen los guardias
            # y la pantalla vuelve a iluminarse.
            else:

                if not self.enemigos_eliminados:

                    self.guardias = arcade.SpriteList()
                    self.enemigos_eliminados = True

                progreso_vuelta = (
                    self.tiempo_transicion - mitad
                ) / mitad

                self.opacidad = max(
                    0,
                    int(255 * (1 - progreso_vuelta))
                )

            if self.tiempo_transicion >= self.duracion_transicion:

                self.opacidad = 0
                self.transicion_activa = False
                self.teclas.clear()

            return

        # RECORRIDO PANORÁMICO DE CÁMARA
        if self.fase == "camara_intro":

            self.tiempo_camara += delta_time

            progreso = min(
                self.tiempo_camara /
                self.duracion_recorrido_camara,
                1
            )

            progreso_suave = (
                progreso * progreso * (3 - 2 * progreso)
            )

            x_camara = self.camara_inicio_x + (
                self.camara_final_x - self.camara_inicio_x
            ) * progreso_suave

            self.camera.position = (
                x_camara,
                ALTO_MAPA / 2
            )

            if progreso >= 1:

                self.fase = "regreso_camara"
                self.tiempo_camara = 0

            return

        # REGRESO DE CÁMARA
        if self.fase == "regreso_camara":

            self.tiempo_camara += delta_time

            duracion_regreso = 1.0

            progreso = min(
                self.tiempo_camara / duracion_regreso,
                1
            )

            progreso_suave = (
                progreso * progreso * (3 - 2 * progreso)
            )

            destino_x = max(
                configuracion.ANCHO / 2,
                min(
                    ANCHO_MAPA - configuracion.ANCHO / 2,
                    self.player.center_x
                )
            )

            x_camara = self.camara_final_x + (
                destino_x - self.camara_final_x
            ) * progreso_suave

            self.camera.position = (
                x_camara,
                self.player.center_y
            )

            if progreso >= 1:

                self.camera.position = (
                    destino_x,
                    self.player.center_y
                )

                self.fase = "instrucciones"

            return

        # INSTRUCCIONES
        if self.fase == "instrucciones":
            return

        if self.fase != "jugando":
            return

        # MOVIMIENTO DE ENEMIGOS
        self.actualizar_enemigos(delta_time)

        # MOVIMIENTO DEL JUGADOR
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

        # Normalizar movimiento diagonal.
        if dx != 0 and dy != 0:
            velocidad_movimiento = self.velocidad / 1.414
        else:
            velocidad_movimiento = self.velocidad

        # Mover al jugador.
        self.player.center_x += (
            dx * velocidad_movimiento
        )

        self.player.center_y += (
            dy * velocidad_movimiento
        )

        # LÍMITES DEL MAPA
        self.player.center_x = max(
            MARGEN_MAPA,
            min(
                ANCHO_MAPA - MARGEN_MAPA,
                self.player.center_x
            )
        )

        self.player.center_y = max(
            MARGEN_MAPA,
            min(
                ALTO_MAPA - MARGEN_MAPA,
                self.player.center_y
            )
        )

        # COLISIONES CON GUARDIAS
        contacto = any(
            arcade.check_for_collision(self.player, enemigo)
            for enemigo in self.guardias
        )

        if contacto:

            self.reiniciar_por_contacto()
            self.player.update_animation(0, 0)

            return

        # ANIMACIÓN DEL JUGADOR
        self.player.update_animation(dx, dy)

        # ACTUALIZAR CÁMARA
        self.camera.position = (
            self.player.center_x,
            self.player.center_y
        )

        # RECOGER FRAGMENTOS
        for fragmento in list(self.fragmentos):

            if arcade.check_for_collision(
                self.player,
                fragmento
            ):

                fragmento.remove_from_sprite_lists()
                self.fragmentos_recogidos += 1

        # AL CONSEGUIR LOS CINCO FRAGMENTOS, INICIAR EL APAGÓN.
        if (
            self.fragmentos_recogidos == 5
            and not self.enemigos_eliminados
            and not self.transicion_activa
        ):

            self.transicion_activa = True
            self.tiempo_transicion = 0
            self.opacidad = 0
            self.teclas.clear()

            return

        # OSCURECIMIENTO ANTERIOR
        if self.fase_oscura:

            self.opacidad += 5

            if self.opacidad >= 180:
                self.opacidad = 180

        else:

            self.opacidad -= 5

            if self.opacidad <= 0:
                self.opacidad = 0

        # SALIDA
        if self.player.center_x >= SALIDA_X:

            if self.fragmentos_recogidos < 5:

                self.player.center_x = SALIDA_X - 20
                return

            self.teclas.clear()

            self.fase = "completado"
            self.opcion_final = 0

            return

    # PRESIONAR TECLA
    def on_key_press(self, key, modifiers):

        # PANTALLA DE NIVEL COMPLETADO
        if self.fase == "completado":

            if key == arcade.key.UP:
                self.opcion_final = 0

            elif key == arcade.key.DOWN:
                self.opcion_final = 1

            elif key == arcade.key.ENTER:

                if self.opcion_final == 0:

                    self.window.show_view(
                        nivel2.Nivel2()
                    )

                else:

                    from menu import Menu

                    self.window.show_view(
                        Menu()
                    )

            return

        # INSTRUCCIONES
        if self.fase == "instrucciones":

            if key == arcade.key.ENTER:
                self.fase = "jugando"

            return

        if self.transicion_activa:
            return

        self.teclas.add(key)

    # SOLTAR TECLA
    def on_key_release(self, key, modifiers):

        if key in self.teclas:
            self.teclas.remove(key)

    # DIBUJAR
    def on_draw(self):

        self.clear()

        # CÁMARA DEL MAPA
        self.camera.use()

        # MAPA
        arcade.draw_texture_rect(
            self.mapa,
            arcade.LBWH(
                0,
                0,
                ANCHO_MAPA,
                ALTO_MAPA
            )
        )

        # FRAGMENTOS
        self.fragmentos.draw()

        # GUARDIAS
        self.guardias.draw()

        # JUGADOR
        self.jugadores.draw()

        # CÁMARA DE INTERFAZ
        self.gui_camera.use()

        # HUD
        arcade.draw_text(
            f"Fragmentos: {self.fragmentos_recogidos}/5",
            25,
            configuracion.ALTO - 45,
            arcade.color.WHITE,
            22
        )

        # DESTELLO NEGRO SOBRE TODA LA PANTALLA
        if self.transicion_activa or self.opacidad > 0:

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                configuracion.ALTO,
                (0, 0, 0, self.opacidad)
            )

        # PRESENTACIÓN DE CÁMARA
        if (
            self.fase == "camara_intro"
            or self.fase == "regreso_camara"
        ):

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                configuracion.ALTO,
                (0, 0, 0, 65)
            )

            arcade.draw_text(
                "LOS IMPERDONABLES",
                configuracion.ANCHO / 2,
                90,
                arcade.color.WHITE,
                25,
                bold=True,
                anchor_x="center"
            )

        # INSTRUCCIONES
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

        # PANTALLA DE NIVEL COMPLETADO
        if self.fase == "completado":

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                configuracion.ALTO,
                (0, 0, 0, 220)
            )

            arcade.draw_lrbt_rectangle_filled(
                250,
                configuracion.ANCHO - 250,
                180,
                configuracion.ALTO - 180,
                (25, 25, 35)
            )

            arcade.draw_lrbt_rectangle_outline(
                250,
                configuracion.ANCHO - 250,
                180,
                configuracion.ALTO - 180,
                arcade.color.GOLD,
                3
            )

            arcade.draw_text(
                "NIVEL COMPLETADO",
                configuracion.ANCHO / 2,
                550,
                arcade.color.GOLD,
                36,
                bold=True,
                anchor_x="center"
            )

            arcade.draw_text(
                "¿Qué querés hacer?",
                configuracion.ANCHO / 2,
                470,
                arcade.color.WHITE,
                24,
                anchor_x="center"
            )

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

            arcade.draw_text(
                "↑ ↓  Seleccionar     ENTER  Confirmar",
                configuracion.ANCHO / 2,
                220,
                arcade.color.LIGHT_GRAY,
                17,
                anchor_x="center"
            )

            return
