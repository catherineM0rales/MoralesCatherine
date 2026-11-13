
import arcade
import configuracion
import math

from entidades import Player


# ============================================================
# CONFIGURACIÓN
# ============================================================

ANCHO = configuracion.ANCHO
ALTO = configuracion.ALTO

ANCHO_MAPA = 1800
ALTO_MAPA = 1200

VELOCIDAD = configuracion.VELOCIDAD_JUGADOR

IMAGEN_TRES_CAMINOS = "imagenes/mapas/tres_caminos.jpg"
IMAGEN_CAMINO_CUEVAS = "imagenes/mapas/camino_cuevas.png"
IMAGEN_JUMPSCARE = "imagenes/mapas/jumpscare_nivel4.png"

IMAGEN_PARED_VERTICAL = "imagenes/objetos/paredvertical.png"
IMAGEN_PUERTA = "imagenes/objetos/puerta_nivel3.png"

IMAGEN_GUARDIAN = "imagenes/personajes/enemigos/guardian_nivel4.png"

ANCHO_CAMINO = 300
ANCHO_PARED = 170
ALTO_SEGMENTO = 200
INTRUSION_PARED = 28


# ============================================================
# NIVEL 4
# ============================================================

class Nivel4(arcade.View):

    def __init__(self):
        super().__init__()

        self.estado = "seleccion"

        self.camino_elegido = 0
        self.vidas = 5

        self.teclas = set()
        self.mensaje = ""
        self.tiempo_mensaje = 0

        # ----------------------------------------------------
        # IMÁGENES
        # ----------------------------------------------------

        self.fondo_seleccion = arcade.load_texture(
            IMAGEN_TRES_CAMINOS
        )

        self.textura_camino = arcade.load_texture(
            IMAGEN_CAMINO_CUEVAS
        )

        self.textura_pared_vertical = arcade.load_texture(
            IMAGEN_PARED_VERTICAL
        )

        self.textura_puerta = arcade.load_texture(
            IMAGEN_PUERTA
        )

        self.textura_jumpscare = arcade.load_texture(
            IMAGEN_JUMPSCARE
        )

        # ----------------------------------------------------
        # CÁMARAS
        # ----------------------------------------------------

        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        self.camera.position = (
            ANCHO_MAPA / 2,
            ALTO / 2
        )

        self.gui_camera.position = (
            ANCHO / 2,
            ALTO / 2
        )

        # ----------------------------------------------------
        # JUGADOR
        # ----------------------------------------------------

        self.jugador = Player()

        self.inicio_x = ANCHO_MAPA / 2
        self.inicio_y = 100
        self.final_y = ALTO_MAPA - 100

        self.jugador.center_x = self.inicio_x
        self.jugador.center_y = self.inicio_y

        self.jugadores = arcade.SpriteList()
        self.jugadores.append(self.jugador)

        # Límites invisibles del camino.

        self.limite_izquierdo = (
            self.inicio_x
            - ANCHO_CAMINO / 2
            + INTRUSION_PARED
        )

        self.limite_derecho = (
            self.inicio_x
            + ANCHO_CAMINO / 2
            - INTRUSION_PARED
        )

        # ----------------------------------------------------
        # PROGRESO
        # ----------------------------------------------------

        self.camino_1_completado = False
        self.camino_2_completado = False
        self.camino_3_completado = False

        # ----------------------------------------------------
        # PUERTA FALSA DEL CAMINO 2
        # ----------------------------------------------------

        self.puerta_falsa_y = 1080

        self.advertencia_y = 820

        self.advertencia_mostrada = False

        self.texto_advertencia = (
            "No... no entres ahí. "
            "Esa puerta no es la salida. "
            "¡No vayas hacia allá!"
        )

        # ----------------------------------------------------
        # GUARDIÁN DEL CAMINO 3
        # ----------------------------------------------------

        self.guardian_x = self.inicio_x
        self.guardian_y = 820

        self.puerta_y = 1080

        self.guardian = arcade.Sprite(
            IMAGEN_GUARDIAN,
            scale=0.22
        )

        self.guardian.center_x = self.guardian_x
        self.guardian.center_y = self.guardian_y

        self.guardian_sprites = arcade.SpriteList()
        self.guardian_sprites.append(self.guardian)

        self.guardian_activado = False
        self.guardian_resuelto = False

        self.respuesta_seleccionada = 0

        self.respuestas = [
            "Olvidar lo que pasó.",
            "Aceptar lo ocurrido y seguir adelante.",
            "Culpar a los demás."
        ]

        self.respuesta_correcta = 1

        # ----------------------------------------------------
        # SECUENCIA DE SORPRESA
        # ----------------------------------------------------

        self.tiempo_sorpresa = 0
        self.resultado_sorpresa = ""

    # ========================================================
    # DIBUJAR
    # ========================================================

    def on_draw(self):

        self.clear()

        # ----------------------------------------------------
        # SELECCIÓN DE CAMINOS
        # ----------------------------------------------------

        if self.estado == "seleccion":

            self.gui_camera.use()

            arcade.draw_texture_rect(
                self.fondo_seleccion,
                arcade.LBWH(0, 0, ANCHO, ALTO)
            )

            arcade.draw_text(
                "ELEGÍ TU CAMINO",
                ANCHO / 2,
                ALTO - 55,
                (235, 215, 255),
                28,
                anchor_x="center",
                bold=True
            )

            arcade.draw_text(
                "Hacé clic en uno de los tres túneles",
                ANCHO / 2,
                25,
                (230, 220, 240),
                16,
                anchor_x="center"
            )

            return

        # ----------------------------------------------------
        # DIÁLOGO DEL CAMINO 1
        # ----------------------------------------------------

        if self.estado == "dialogo_bucle":

            self.gui_camera.use()

            arcade.draw_rect_filled(
                arcade.LBWH(0, 0, ANCHO, ALTO),
                (12, 9, 20)
            )

            arcade.draw_rect_filled(
                arcade.LBWH(120, 260, ANCHO - 240, 180),
                (25, 20, 35)
            )

            arcade.draw_rect_outline(
                arcade.LBWH(120, 260, ANCHO - 240, 180),
                (170, 150, 195),
                2
            )

            arcade.draw_text(
                "PROTAGONISTA",
                ANCHO / 2,
                390,
                (210, 195, 235),
                17,
                anchor_x="center",
                bold=True
            )

            arcade.draw_text(
                "«¿Eh? Estoy aquí otra vez...»",
                ANCHO / 2,
                340,
                (245, 235, 250),
                22,
                anchor_x="center"
            )

            arcade.draw_text(
                "ENTER: continuar",
                ANCHO / 2,
                285,
                (190, 175, 210),
                15,
                anchor_x="center"
            )

            return

        # ----------------------------------------------------
        # VICTORIA
        # ----------------------------------------------------

        if self.estado == "victoria":

            self.gui_camera.use()

            arcade.draw_rect_filled(
                arcade.LBWH(0, 0, ANCHO, ALTO),
                (12, 9, 24)
            )

            arcade.draw_text(
                "LOGRASTE SALIR",
                ANCHO / 2,
                ALTO / 2 + 70,
                (230, 210, 255),
                36,
                anchor_x="center",
                bold=True
            )

            arcade.draw_text(
                "Incluso en la oscuridad, encontraste tu camino.",
                ANCHO / 2,
                ALTO / 2 + 15,
                (220, 210, 235),
                17,
                anchor_x="center"
            )

            arcade.draw_text(
                "ENTER: volver al menú",
                ANCHO / 2,
                ALTO / 2 - 65,
                (200, 180, 230),
                18,
                anchor_x="center"
            )

            return

        # ----------------------------------------------------
        # DERROTA
        # ----------------------------------------------------

        if self.estado == "derrota":

            self.gui_camera.use()

            arcade.draw_rect_filled(
                arcade.LBWH(0, 0, ANCHO, ALTO),
                (25, 4, 15)
            )

            arcade.draw_text(
                "TE EQUIVOCASTE DE PUERTA",
                ANCHO / 2,
                ALTO / 2 + 60,
                (255, 140, 175),
                28,
                anchor_x="center",
                bold=True
            )

            arcade.draw_text(
                "La oscuridad te impidió encontrar la salida.",
                ANCHO / 2,
                ALTO / 2 + 10,
                (235, 210, 225),
                17,
                anchor_x="center"
            )

            arcade.draw_text(
                "R: reintentar    ESC: volver al menú",
                ANCHO / 2,
                ALTO / 2 - 50,
                (235, 210, 225),
                17,
                anchor_x="center"
            )

            return

        # ----------------------------------------------------
        # JUMPSCARE
        # ----------------------------------------------------

        if self.estado == "sorpresa":

            self.gui_camera.use()

            arcade.draw_texture_rect(
                self.textura_jumpscare,
                arcade.LBWH(0, 0, ANCHO, ALTO)
            )

            return

        # ----------------------------------------------------
        # ESCENARIO DE LA CUEVA
        # ----------------------------------------------------

        self.camera.use()

        arcade.draw_texture_rect(
            self.textura_camino,
            arcade.LBWH(
                0,
                0,
                ANCHO_MAPA,
                ALTO_MAPA
            )
        )

        self.dibujar_paredes_bordes()

        # ----------------------------------------------------
        # CAMINO 2: PUERTA FALSA
        # ----------------------------------------------------

        if self.camino_elegido == 2:

            arcade.draw_texture_rect(
                self.textura_puerta,
                arcade.LBWH(
                    self.inicio_x - 45,
                    self.puerta_falsa_y - 55,
                    90,
                    110
                )
            )

        # ----------------------------------------------------
        # CAMINO 3: GUARDIÁN Y PUERTA VERDADERA
        # ----------------------------------------------------

        if self.camino_elegido == 3:

            self.guardian_sprites.draw()

            arcade.draw_texture_rect(
                self.textura_puerta,
                arcade.LBWH(
                    self.inicio_x - 45,
                    self.puerta_y - 55,
                    90,
                    110
                )
            )

        # ----------------------------------------------------
        # JUGADOR
        # ----------------------------------------------------

        self.jugadores.draw()

        # ----------------------------------------------------
        # INTERFAZ
        # ----------------------------------------------------

        self.gui_camera.use()

        arcade.draw_text(
            f"VIDAS: {self.vidas}",
            25,
            ALTO - 40,
            (255, 220, 240),
            20
        )

        arcade.draw_text(
            f"CAMINO {self.camino_elegido}",
            ANCHO / 2,
            ALTO - 40,
            (225, 205, 250),
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "WASD / FLECHAS: moverse",
            20,
            20,
            (220, 210, 235),
            14
        )

        if self.mensaje:

            arcade.draw_text(
                self.mensaje,
                ANCHO / 2,
                ALTO / 2 + 100,
                (255, 225, 245),
                18,
                anchor_x="center"
            )

        # ----------------------------------------------------
        # ADVERTENCIA DEL CAMINO 2
        # ----------------------------------------------------

        if self.estado == "advertencia_puerta":

            arcade.draw_rect_filled(
                arcade.LBWH(
                    40,
                    25,
                    ANCHO - 80,
                    150
                ),
                (12, 8, 20)
            )

            arcade.draw_rect_outline(
                arcade.LBWH(
                    40,
                    25,
                    ANCHO - 80,
                    150
                ),
                (170, 125, 155),
                2
            )

            arcade.draw_text(
                "VOZ DESCONOCIDA",
                ANCHO / 2,
                140,
                (210, 175, 205),
                17,
                anchor_x="center",
                bold=True
            )

            arcade.draw_text(
                self.texto_advertencia,
                ANCHO / 2,
                95,
                (245, 225, 240),
                16,
                anchor_x="center"
            )

            arcade.draw_text(
                "ENTER: continuar",
                ANCHO / 2,
                48,
                (190, 175, 210),
                14,
                anchor_x="center"
            )

        # ----------------------------------------------------
        # PREGUNTA DEL GUARDIÁN
        # ----------------------------------------------------

        if self.estado == "guardian_pregunta":

            arcade.draw_rect_filled(
                arcade.LBWH(
                    100,
                    100,
                    ANCHO - 200,
                    250
                ),
                (15, 10, 25)
            )

            arcade.draw_rect_outline(
                arcade.LBWH(
                    100,
                    100,
                    ANCHO - 200,
                    250
                ),
                (160, 135, 190),
                2
            )

            arcade.draw_text(
                "GUARDIÁN",
                ANCHO / 2,
                310,
                (230, 215, 255),
                23,
                anchor_x="center",
                bold=True
            )

            arcade.draw_text(
                "¿Qué significa realmente seguir adelante?",
                ANCHO / 2,
                270,
                (240, 230, 245),
                17,
                anchor_x="center"
            )

            for i, respuesta in enumerate(self.respuestas):

                color = (
                    (255, 220, 150)
                    if i == self.respuesta_seleccionada
                    else (215, 205, 225)
                )

                prefijo = (
                    "➤ "
                    if i == self.respuesta_seleccionada
                    else "   "
                )

                arcade.draw_text(
                    prefijo + respuesta,
                    155,
                    220 - i * 42,
                    color,
                    16
                )

            arcade.draw_text(
                "FLECHAS: elegir     ENTER: confirmar",
                ANCHO / 2,
                115,
                (190, 175, 210),
                14,
                anchor_x="center"
            )

    # ========================================================
    # PAREDES VISUALES
    # ========================================================

    def dibujar_paredes_bordes(self):

        borde_izquierdo = (
            self.inicio_x - ANCHO_CAMINO / 2
        )

        borde_derecho = (
            self.inicio_x + ANCHO_CAMINO / 2
        )

        centro_pared_izquierda = (
            borde_izquierdo
            - ANCHO_PARED / 2
            + INTRUSION_PARED
        )

        centro_pared_derecha = (
            borde_derecho
            + ANCHO_PARED / 2
            - INTRUSION_PARED
        )

        cantidad = int(
            ALTO_MAPA / ALTO_SEGMENTO
        ) + 2

        for i in range(cantidad):

            y = (
                i * ALTO_SEGMENTO
                + ALTO_SEGMENTO / 2
            )

            arcade.draw_texture_rect(
                self.textura_pared_vertical,
                arcade.LBWH(
                    centro_pared_izquierda - ANCHO_PARED / 2,
                    y - ALTO_SEGMENTO / 2,
                    ANCHO_PARED,
                    ALTO_SEGMENTO
                )
            )

            arcade.draw_texture_rect(
                self.textura_pared_vertical,
                arcade.LBWH(
                    centro_pared_derecha - ANCHO_PARED / 2,
                    y - ALTO_SEGMENTO / 2,
                    ANCHO_PARED,
                    ALTO_SEGMENTO
                )
            )

    # ========================================================
    # SELECCIÓN DE CAMINOS
    # ========================================================

    def on_mouse_press(self, x, y, button, modifiers):

        if self.estado != "seleccion":
            return

        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        if x < ANCHO / 3:
            self.elegir_camino(1)

        elif x < ANCHO * 2 / 3:
            self.elegir_camino(2)

        else:
            self.elegir_camino(3)

    def elegir_camino(self, numero):

        self.camino_elegido = numero
        self.estado = f"camino_{numero}"

        self.mensaje = ""
        self.tiempo_mensaje = 0

        self.teclas.clear()

        self.jugador.center_x = self.inicio_x
        self.jugador.center_y = self.inicio_y

        self.guardian_activado = False
        self.guardian_resuelto = False
        self.respuesta_seleccionada = 0

        self.advertencia_mostrada = False

        self.guardian.center_x = self.guardian_x
        self.guardian.center_y = self.guardian_y

        self.actualizar_camara()

    # ========================================================
    # CONTROLES
    # ========================================================

    def on_key_press(self, key, modifiers):

        if self.estado == "dialogo_bucle":

            if key == arcade.key.ENTER:
                self.estado = "seleccion"

            return

        if self.estado == "advertencia_puerta":

            if key == arcade.key.ENTER:
                self.estado = "camino_2"
                self.teclas.clear()

            return

        if self.estado == "victoria":

            if key == arcade.key.ENTER:
                self.volver_al_menu()

            return

        if self.estado == "derrota":

            if key == arcade.key.R:
                self.reintentar()

            elif key == arcade.key.ESCAPE:
                self.volver_al_menu()

            return

        if self.estado == "sorpresa":
            return

        if self.estado == "guardian_pregunta":

            if key == arcade.key.UP:

                self.respuesta_seleccionada = (
                    self.respuesta_seleccionada - 1
                ) % len(self.respuestas)

            elif key == arcade.key.DOWN:

                self.respuesta_seleccionada = (
                    self.respuesta_seleccionada + 1
                ) % len(self.respuestas)

            elif key == arcade.key.ENTER:

                self.comprobar_respuesta()

            return

        if key == arcade.key.ESCAPE:

            if self.estado.startswith("camino_"):

                self.estado = "seleccion"
                self.teclas.clear()

            return

        if key == arcade.key.R:

            self.reintentar()
            return

        self.teclas.add(key)

    def on_key_release(self, key, modifiers):

        self.teclas.discard(key)

    # ========================================================
    # INICIAR JUMPSCARE
    # ========================================================

    def iniciar_sorpresa(self, resultado):

        self.estado = "sorpresa"

        self.tiempo_sorpresa = 1.2

        self.resultado_sorpresa = resultado

        self.teclas.clear()

    # ========================================================
    # MOVIMIENTO DEL JUGADOR
    # ========================================================

    def mover_jugador(self, delta_time):

        dx = 0
        dy = 0

        if (
            arcade.key.LEFT in self.teclas
            or arcade.key.A in self.teclas
        ):
            dx -= 1

        if (
            arcade.key.RIGHT in self.teclas
            or arcade.key.D in self.teclas
        ):
            dx += 1

        if (
            arcade.key.UP in self.teclas
            or arcade.key.W in self.teclas
        ):
            dy += 1

        if (
            arcade.key.DOWN in self.teclas
            or arcade.key.S in self.teclas
        ):
            dy -= 1

        if dx != 0 and dy != 0:

            dx *= 0.7071
            dy *= 0.7071

        factor = delta_time * 60

        nuevo_x = (
            self.jugador.center_x
            + dx * VELOCIDAD * factor
        )

        nuevo_y = (
            self.jugador.center_y
            + dy * VELOCIDAD * factor
        )

        mitad_jugador = self.jugador.width / 2

        nuevo_x = max(
            self.limite_izquierdo + mitad_jugador,
            min(
                self.limite_derecho - mitad_jugador,
                nuevo_x
            )
        )

        nuevo_y = max(
            30,
            min(ALTO_MAPA - 30, nuevo_y)
        )

        self.jugador.center_x = nuevo_x
        self.jugador.center_y = nuevo_y

        if hasattr(self.jugador, "update_animation"):
            self.jugador.update_animation(dx, dy)

    # ========================================================
    # CÁMARA
    # ========================================================

    def actualizar_camara(self):

        centro_y = max(
            ALTO / 2,
            min(
                ALTO_MAPA - ALTO / 2,
                self.jugador.center_y
            )
        )

        self.camera.position = (
            self.jugador.center_x,
            centro_y
        )

    # ========================================================
    # GUARDIÁN
    # ========================================================

    def comprobar_respuesta(self):

        if self.respuesta_seleccionada == self.respuesta_correcta:

            self.guardian_resuelto = True
            self.estado = "camino_3"

            self.mensaje = "El guardián te permite continuar."
            self.tiempo_mensaje = 3

        else:

            self.iniciar_sorpresa("derrota")

    # ========================================================
    # ACTUALIZACIÓN DEL NIVEL
    # ========================================================

    def on_update(self, delta_time):

        if self.estado == "sorpresa":

            self.tiempo_sorpresa -= delta_time

            if self.tiempo_sorpresa <= 0:
                self.estado = self.resultado_sorpresa

            return

        if not self.estado.startswith("camino_"):
            return

        if self.estado == "guardian_pregunta":
            return

        if self.tiempo_mensaje > 0:

            self.tiempo_mensaje -= delta_time

            if self.tiempo_mensaje <= 0:
                self.mensaje = ""

        self.mover_jugador(delta_time)
        self.actualizar_camara()

        # ----------------------------------------------------
        # CAMINO 1
        # ----------------------------------------------------

        if self.camino_elegido == 1:

            if self.jugador.center_y >= self.final_y:

                self.camino_1_completado = True

                self.jugador.center_x = self.inicio_x
                self.jugador.center_y = self.inicio_y

                self.actualizar_camara()

                self.estado = "dialogo_bucle"
                self.teclas.clear()

                return

        # ----------------------------------------------------
        # CAMINO 2
        # ----------------------------------------------------

        elif self.camino_elegido == 2:

            if (
                self.jugador.center_y >= self.advertencia_y
                and not self.advertencia_mostrada
            ):

                self.advertencia_mostrada = True

                self.estado = "advertencia_puerta"
                self.teclas.clear()

                return

            if self.jugador.center_y >= self.puerta_falsa_y:

                self.camino_2_completado = True

                self.iniciar_sorpresa("derrota")

                return

        # ----------------------------------------------------
        # CAMINO 3
        # ----------------------------------------------------

        elif self.camino_elegido == 3:

            distancia_guardian = math.sqrt(
                (
                    self.jugador.center_x
                    - self.guardian_x
                ) ** 2
                +
                (
                    self.jugador.center_y
                    - self.guardian_y
                ) ** 2
            )

            if (
                distancia_guardian < 100
                and not self.guardian_resuelto
            ):

                self.estado = "guardian_pregunta"
                self.teclas.clear()

                return

            if (
                self.guardian_resuelto
                and self.jugador.center_y >= self.puerta_y
            ):

                self.camino_3_completado = True

                self.estado = "victoria"
                self.teclas.clear()

                return

    # ========================================================
    # REINTENTAR
    # ========================================================

    def reintentar(self):

        self.vidas = 5

        self.camino_1_completado = False
        self.camino_2_completado = False
        self.camino_3_completado = False

        self.estado = "seleccion"
        self.camino_elegido = 0

        self.mensaje = ""
        self.tiempo_mensaje = 0

        self.guardian_activado = False
        self.guardian_resuelto = False

        self.advertencia_mostrada = False

        self.teclas.clear()

        self.jugador.center_x = self.inicio_x
        self.jugador.center_y = self.inicio_y

        self.tiempo_sorpresa = 0
        self.resultado_sorpresa = ""

        self.actualizar_camara()

    # ========================================================
    # VOLVER AL MENÚ
    # ========================================================

    def volver_al_menu(self):

        from menu import Menu

        self.window.show_view(Menu())
