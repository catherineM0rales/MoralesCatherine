import arcade
import configuracion
from entidades import Player, VillanoPrincipal, Proyectil

# ============================================================
# CONFIGURACIÓN DEL NIVEL 4
# ============================================================

ANCHO = configuracion.ANCHO
ALTO = configuracion.ALTO

ANCHO_MAPA = 1800
ALTO_MAPA = 1200
VELOCIDAD = configuracion.VELOCIDAD_JUGADOR

IMAGEN_TRES_CAMINOS = "imagenes/mapas/tres_caminos.jpg"
IMAGEN_PARED_VERTICAL = "imagenes/objetos/paredvertical.png"

# Ancho del camino y tamaño de los segmentos de pared.
# Las paredes son más grandes y quedan alineadas con el borde exterior
# del camino, sin invadir el espacio transitable.
ANCHO_CAMINO = 300
ANCHO_PARED = 170
ALTO_SEGMENTO = 200

# La pared se mete ligeramente hacia el camino para quedar visualmente
# montada sobre su borde. La colisión coincide con ese borde interior.
INTRUSION_PARED = 28


class Nivel4(arcade.View):
    def __init__(self):
        super().__init__()

        self.estado = "seleccion"
        self.camino_elegido = 0
        self.vidas = 5
        self.teclas = set()
        self.mensaje = ""

        self.fondo_seleccion = arcade.load_texture(IMAGEN_TRES_CAMINOS)
        self.textura_pared_vertical = arcade.load_texture(IMAGEN_PARED_VERTICAL)

        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        self.camera.position = (ANCHO_MAPA / 2, ALTO_MAPA / 2)
        self.gui_camera.position = (ANCHO / 2, ALTO / 2)

        self.jugador = Player()
        self.jugador.center_x = ANCHO_MAPA / 2
        self.jugador.center_y = 100

        self.jugadores = arcade.SpriteList()
        self.jugadores.append(self.jugador)

        self.camino_1_completado = False
        self.camino_2_completado = False
        self.camino_3_completado = False

        self.inicio_x = ANCHO_MAPA / 2
        self.inicio_y = 100
        self.final_y = ALTO_MAPA - 100

        # Límites invisibles de colisión para los bordes del túnel.
        self.limite_izquierdo = (
            self.inicio_x - ANCHO_CAMINO / 2 + INTRUSION_PARED
        )
        self.limite_derecho = (
            self.inicio_x + ANCHO_CAMINO / 2 - INTRUSION_PARED
        )

        # Villano y proyectiles del camino 2.
        self.villano = None
        self.villanos = arcade.SpriteList()
        self.proyectiles = arcade.SpriteList()
        self.tiempo_entre_danos = 0

    # ========================================================
    # DIBUJAR
    # ========================================================

    def on_draw(self):
        self.clear()

        if self.estado == "seleccion":
            self.gui_camera.use()
            arcade.draw_texture_rect(
                self.fondo_seleccion,
                arcade.LBWH(0, 0, ANCHO, ALTO),
            )
            arcade.draw_text(
                "ELEGÍ TU CAMINO",
                ANCHO / 2,
                ALTO - 55,
                (235, 215, 255),
                28,
                anchor_x="center",
                bold=True,
            )
            arcade.draw_text(
                "Hacé clic en uno de los tres túneles",
                ANCHO / 2,
                25,
                (230, 220, 240),
                16,
                anchor_x="center",
            )
            return

        if self.estado == "victoria":
            self.gui_camera.use()
            arcade.draw_rect_filled(
                arcade.LBWH(0, 0, ANCHO, ALTO),
                (12, 9, 24),
            )
            arcade.draw_text(
                "LOGRASTE SALIR",
                ANCHO / 2,
                ALTO / 2 + 70,
                (230, 210, 255),
                36,
                anchor_x="center",
                bold=True,
            )
            arcade.draw_text(
                "Incluso en la oscuridad, encontraste tu camino.",
                ANCHO / 2,
                ALTO / 2 + 15,
                (220, 210, 235),
                17,
                anchor_x="center",
            )
            arcade.draw_text(
                "ENTER: volver al menú",
                ANCHO / 2,
                ALTO / 2 - 65,
                (200, 180, 230),
                18,
                anchor_x="center",
            )
            return

        if self.estado == "derrota":
            self.gui_camera.use()
            arcade.draw_rect_filled(
                arcade.LBWH(0, 0, ANCHO, ALTO),
                (25, 4, 15),
            )
            arcade.draw_text(
                "TE EQUIVOCASTE DE PUERTA",
                ANCHO / 2,
                ALTO / 2 + 60,
                (255, 140, 175),
                28,
                anchor_x="center",
                bold=True,
            )
            arcade.draw_text(
                "R: reintentar    ESC: volver al menú",
                ANCHO / 2,
                ALTO / 2 - 20,
                (235, 210, 225),
                17,
                anchor_x="center",
            )
            return

        # Escenario provisional con las paredes solamente en los bordes.
        self.camera.use()
        arcade.draw_rect_filled(
            arcade.LBWH(0, 0, ANCHO_MAPA, ALTO_MAPA),
            (18, 13, 28),
        )
        arcade.draw_rect_filled(
            arcade.LBWH(
                self.inicio_x - ANCHO_CAMINO / 2,
                0,
                ANCHO_CAMINO,
                ALTO_MAPA,
            ),
            (48, 32, 58),
        )

        self.dibujar_paredes_bordes()

        # El villano aparece únicamente en el camino 2.
        if self.camino_elegido == 2:
            self.proyectiles.draw()
            self.villanos.draw()

        self.jugadores.draw()

        self.gui_camera.use()
        arcade.draw_text(
            f"VIDAS: {self.vidas}",
            25,
            ALTO - 40,
            (255, 220, 240),
            20,
        )
        arcade.draw_text(
            f"CAMINO {self.camino_elegido}",
            ANCHO / 2,
            ALTO - 40,
            (225, 205, 250),
            20,
            anchor_x="center",
        )
        arcade.draw_text(
            "WASD / FLECHAS: moverse     ESC: volver a elegir",
            20,
            20,
            (220, 210, 235),
            14,
        )
        if self.mensaje:
            arcade.draw_text(
                self.mensaje,
                ANCHO / 2,
                ALTO / 2,
                (255, 225, 245),
                20,
                anchor_x="center",
            )

    def dibujar_paredes_bordes(self):
        """Dibuja paredes verticales grandes, pegadas al borde del camino."""
        borde_izquierdo = self.inicio_x - ANCHO_CAMINO / 2
        borde_derecho = self.inicio_x + ANCHO_CAMINO / 2

        # El centro de cada pared queda fuera del camino para que su borde
        # interior coincida con la línea del borde transitable.
        centro_pared_izquierda = (
            borde_izquierdo - ANCHO_PARED / 2 + INTRUSION_PARED
        )
        centro_pared_derecha = (
            borde_derecho + ANCHO_PARED / 2 - INTRUSION_PARED
        )

        cantidad = int(ALTO_MAPA / ALTO_SEGMENTO) + 2
        for i in range(cantidad):
            y = i * ALTO_SEGMENTO + ALTO_SEGMENTO / 2

            # Un solo recurso: paredvertical.png, con segmentos grandes.
            arcade.draw_texture_rect(
                self.textura_pared_vertical,
                arcade.LBWH(
                    centro_pared_izquierda - ANCHO_PARED / 2,
                    y - ALTO_SEGMENTO / 2,
                    ANCHO_PARED,
                    ALTO_SEGMENTO,
                ),
            )
            arcade.draw_texture_rect(
                self.textura_pared_vertical,
                arcade.LBWH(
                    centro_pared_derecha - ANCHO_PARED / 2,
                    y - ALTO_SEGMENTO / 2,
                    ANCHO_PARED,
                    ALTO_SEGMENTO,
                ),
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
        self.teclas.clear()

        self.jugador.center_x = self.inicio_x
        self.jugador.center_y = self.inicio_y
        self.proyectiles.clear()
        self.villanos.clear()
        self.villano = None
        self.tiempo_entre_danos = 0

        if numero == 2:
            # Aparece más adelante, dentro del túnel, y dispara al jugador.
            self.villano = VillanoPrincipal(
                self.inicio_x,
                ALTO_MAPA - 220,
                velocidad=0,
                espera_disparo=1.4,
            )
            self.villanos.append(self.villano)

        self.actualizar_camara()

    # ========================================================
    # CONTROLES
    # ========================================================

    def on_key_press(self, key, modifiers):
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
    # MOVIMIENTO Y COLISIONES
    # ========================================================

    def mover_jugador(self, delta_time):
        dx = 0
        dy = 0

        if arcade.key.LEFT in self.teclas or arcade.key.A in self.teclas:
            dx -= 1
        if arcade.key.RIGHT in self.teclas or arcade.key.D in self.teclas:
            dx += 1
        if arcade.key.UP in self.teclas or arcade.key.W in self.teclas:
            dy += 1
        if arcade.key.DOWN in self.teclas or arcade.key.S in self.teclas:
            dy -= 1

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        factor = delta_time * 60
        nuevo_x = self.jugador.center_x + dx * VELOCIDAD * factor
        nuevo_y = self.jugador.center_y + dy * VELOCIDAD * factor

        # Colisión con el borde interior de las paredes.
        # El jugador permanece dentro del camino y no atraviesa las rocas.
        mitad_jugador = self.jugador.width / 2
        nuevo_x = max(
            self.limite_izquierdo + mitad_jugador,
            min(self.limite_derecho - mitad_jugador, nuevo_x),
        )
        nuevo_y = max(30, min(ALTO_MAPA - 30, nuevo_y))

        self.jugador.center_x = nuevo_x
        self.jugador.center_y = nuevo_y

        if hasattr(self.jugador, "update_animation"):
            self.jugador.update_animation(dx, dy)

    # ========================================================
    # CÁMARA
    # ========================================================

    def actualizar_camara(self):
        self.camera.position = (
            self.jugador.center_x,
            self.jugador.center_y,
        )

    # ========================================================
    # ACTUALIZACIÓN DEL NIVEL
    # ========================================================

    def on_update(self, delta_time):
        if not self.estado.startswith("camino_"):
            return

        self.mover_jugador(delta_time)
        self.actualizar_camara()

        if self.tiempo_entre_danos > 0:
            self.tiempo_entre_danos -= delta_time

        # Camino 2: el villano permanece en su posición y dispara proyectiles
        # violetas dirigidos hacia la posición actual del jugador.
        if self.camino_elegido == 2 and self.villano is not None:
            self.villano.tiempo_disparo += delta_time

            if self.villano.puede_disparar():
                proyectil = Proyectil(
                    self.villano.center_x,
                    self.villano.center_y,
                    self.jugador.center_x,
                    self.jugador.center_y,
                )
                self.proyectiles.append(proyectil)

            for proyectil in list(self.proyectiles):
                proyectil.mover()

                # Elimina proyectiles que salen del mapa.
                if (
                    proyectil.center_x < 0
                    or proyectil.center_x > ANCHO_MAPA
                    or proyectil.center_y < 0
                    or proyectil.center_y > ALTO_MAPA
                ):
                    proyectil.remove_from_sprite_lists()
                    continue

                # Un impacto quita una vida; el pequeño intervalo evita
                # perder varias vidas en el mismo instante.
                if (
                    self.tiempo_entre_danos <= 0
                    and arcade.check_for_collision(self.jugador, proyectil)
                ):
                    self.vidas -= 1
                    self.tiempo_entre_danos = 1.0
                    proyectil.remove_from_sprite_lists()
                    self.mensaje = "¡Te alcanzó un proyectil!"

                    if self.vidas <= 0:
                        self.estado = "derrota"
                        self.teclas.clear()
                        return
                elif arcade.check_for_collision(self.jugador, proyectil):
                    proyectil.remove_from_sprite_lists()



        # Camino 1: vuelve al selector al llegar al final.
        if self.camino_elegido == 1:
            if self.jugador.center_y >= self.final_y:
                self.camino_1_completado = True
                self.estado = "seleccion"
                self.teclas.clear()

        # El combate del camino 2 ya incluye al villano y sus disparos.
        # La espada y la posibilidad de derrotarlo se incorporarán después.
        elif self.camino_elegido == 2:
            pass
        elif self.camino_elegido == 3:
            pass

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
        self.teclas.clear()

    # ========================================================
    # VOLVER AL MENÚ
    # ========================================================

    def volver_al_menu(self):
        from menu import Menu
        self.window.show_view(Menu())
