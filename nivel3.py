import arcade
import math
import random

import configuracion

from entidades import Player, VillanoPrincipal


# ============================================================
# CONFIGURACIÓN DEL MAPA
# ============================================================

ANCHO_MAPA = 1536
ALTO_MAPA = 1024


# ============================================================
# PROYECTIL DEL VILLANO
# ============================================================

class PoderVillano(arcade.SpriteSolidColor):

    def __init__(self, x, y, jugador_x, jugador_y):

        super().__init__(
            width=18,
            height=18,
            color=(150, 90, 220)
        )

        self.center_x = x
        self.center_y = y

        dx = jugador_x - x
        dy = jugador_y - y

        distancia = math.sqrt(dx * dx + dy * dy)

        if distancia == 0:
            distancia = 1

        self.direccion_x = dx / distancia
        self.direccion_y = dy / distancia

        self.velocidad = 4.5

    def update(self, delta_time=1 / 60):

        self.center_x += self.direccion_x * self.velocidad
        self.center_y += self.direccion_y * self.velocidad

        if (
            self.center_x < -50
            or self.center_x > ANCHO_MAPA + 50
            or self.center_y < -50
            or self.center_y > ALTO_MAPA + 50
        ):
            self.remove_from_sprite_lists()


# ============================================================
# LLAVE
# ============================================================

class Llave(arcade.Sprite):

    def __init__(self, x, y):

        super().__init__(
            "imagenes/objetos/llave_nivel3.png",
            scale=0.15
        )

        self.center_x = x
        self.center_y = y


# ============================================================
# PUERTA
# ============================================================

class Puerta(arcade.Sprite):

    def __init__(self, x, y):

        super().__init__(
            "imagenes/objetos/puerta_nivel3.png",
            scale=0.15
        )

        self.center_x = x
        self.center_y = y


# ============================================================
# PARED
# ============================================================

class Pared(arcade.Sprite):

    def __init__(self, x, y, ancho, alto):

        super().__init__(
            "imagenes/objetos/paredes.png"
        )

        self.center_x = x
        self.center_y = y

        self.width = ancho
        self.height = alto


# ============================================================
# NIVEL 3
# ============================================================

class Nivel3(arcade.View):

    def __init__(self):

        super().__init__()

        # ======================================================
        # FONDO
        # ======================================================

        self.fondo = arcade.load_texture(
            "imagenes/mapas/nivel3_fondo.png"
        )

        # ======================================================
        # JUGADOR
        # ======================================================

        self.jugador = Player()

        self.jugador.center_x = 768
        self.jugador.center_y = 100

        self.jugadores = arcade.SpriteList()
        self.jugadores.append(self.jugador)

        # ======================================================
        # LLAVE
        # ======================================================

        self.llave = Llave(
            768,
            500
        )

        self.llaves = arcade.SpriteList()
        self.llaves.append(self.llave)

        # ======================================================
        # PUERTA
        # ======================================================

        self.puerta = Puerta(
            768,
            930
        )

        self.puertas = arcade.SpriteList()
        self.puertas.append(self.puerta)

        # ======================================================
        # VILLANOS
        # ======================================================

        self.villanos = arcade.SpriteList()

        villano_izquierda = VillanoPrincipal(
            230,
            500,
            imagen="imagenes/personajes/enemigos/villano_nivel3.png",
            velocidad=3.5,
            rango_vision=2000,
            espera_disparo=0.6
        )

        villano_derecha = VillanoPrincipal(
            1300,
            500,
            imagen="imagenes/personajes/enemigos/villano_nivel3.png",
            velocidad=3.5,
            rango_vision=2000,
            espera_disparo=0.6
        )

        self.villanos.append(
            villano_izquierda
        )

        self.villanos.append(
            villano_derecha
        )

        # ======================================================
        # PROYECTILES
        # ======================================================

        self.proyectiles = arcade.SpriteList()

        # ======================================================
        # PAREDES
        # ======================================================

        self.paredes = arcade.SpriteList()

        random.seed(42)

        posiciones_evitar = [
            (768, 100),
            (768, 500),
            (768, 930),
            (230, 500),
            (1300, 500)
        ]

        for _ in range(10):

            while True:

                ancho = random.randint(
                    100,
                    220
                )

                alto = random.randint(
                    60,
                    110
                )

                x = random.randint(
                    ancho // 2 + 50,
                    ANCHO_MAPA - ancho // 2 - 50
                )

                y = random.randint(
                    alto // 2 + 50,
                    ALTO_MAPA - alto // 2 - 50
                )

                sirve = True

                for px, py in posiciones_evitar:

                    distancia = math.sqrt(
                        (x - px) ** 2 +
                        (y - py) ** 2
                    )

                    if distancia < 150:

                        sirve = False
                        break

                if sirve:
                    break

            pared = Pared(
                x,
                y,
                ancho,
                alto
            )

            self.paredes.append(pared)

        # ======================================================
        # VIDA
        # ======================================================

        self.vida = 5

        # ======================================================
        # ESTADOS
        # ======================================================

        self.tiene_llave = False

        self.juego_empezado = False

        self.nivel_completado = False

        # ======================================================
        # MOVIMIENTO
        # ======================================================

        self.arriba = False
        self.abajo = False
        self.izquierda = False
        self.derecha = False

        # ======================================================
        # CÁMARA FIJA
        # ======================================================

        self.camera = arcade.Camera2D()

        # El mapa completo entra en pantalla.
        self.camera.zoom = 0.75

        # La cámara queda SIEMPRE en el centro.
        self.camera.position = (
            ANCHO_MAPA / 2,
            ALTO_MAPA / 2
        )

    # ============================================================
    # COLISIÓN CON PARED
    # ============================================================

    def choca_con_pared(self, x, y):

        for pared in self.paredes:

            izquierda = (
                pared.center_x
                - pared.width / 2
            )

            derecha = (
                pared.center_x
                + pared.width / 2
            )

            abajo = (
                pared.center_y
                - pared.height / 2
            )

            arriba = (
                pared.center_y
                + pared.height / 2
            )

            if (
                x >= izquierda
                and x <= derecha
                and y >= abajo
                and y <= arriba
            ):

                return True

        return False

    # ============================================================
    # MOVIMIENTO DEL JUGADOR
    # ============================================================

    def mover_jugador(self):

        dx = 0
        dy = 0

        if self.arriba:
            dy += 1

        if self.abajo:
            dy -= 1

        if self.derecha:
            dx += 1

        if self.izquierda:
            dx -= 1

        if dx == 0 and dy == 0:

            self.jugador.update_animation(
                0,
                0
            )

            return

        # --------------------------------------------------------
        # NORMALIZAR DIAGONAL
        # --------------------------------------------------------

        distancia = math.sqrt(
            dx * dx +
            dy * dy
        )

        dx /= distancia
        dy /= distancia

        velocidad = (
            configuracion.VELOCIDAD_JUGADOR
        )

        nuevo_x = (
            self.jugador.center_x
            + dx * velocidad
        )

        nuevo_y = (
            self.jugador.center_y
            + dy * velocidad
        )

        # --------------------------------------------------------
        # COLISIÓN HORIZONTAL
        # --------------------------------------------------------

        if not self.choca_con_pared(
            nuevo_x,
            self.jugador.center_y
        ):

            self.jugador.center_x = nuevo_x

        # --------------------------------------------------------
        # COLISIÓN VERTICAL
        # --------------------------------------------------------

        if not self.choca_con_pared(
            self.jugador.center_x,
            nuevo_y
        ):

            self.jugador.center_y = nuevo_y

        # --------------------------------------------------------
        # LÍMITES DEL MAPA
        # --------------------------------------------------------

        margen_x = self.jugador.width / 2
        margen_y = self.jugador.height / 2

        self.jugador.center_x = max(
            margen_x,
            min(
                ANCHO_MAPA - margen_x,
                self.jugador.center_x
            )
        )

        self.jugador.center_y = max(
            margen_y,
            min(
                ALTO_MAPA - margen_y,
                self.jugador.center_y
            )
        )

        self.jugador.update_animation(
            dx,
            dy
        )

    # ============================================================
    # ACTUALIZAR
    # ============================================================

    def on_update(self, delta_time):

        # --------------------------------------------------------
        # SI TODAVÍA NO EMPEZÓ
        # --------------------------------------------------------

        if not self.juego_empezado:
            return

        # --------------------------------------------------------
        # SI TERMINÓ
        # --------------------------------------------------------

        if self.nivel_completado:
            return

        # ========================================================
        # JUGADOR
        # ========================================================

        self.mover_jugador()

        # ========================================================
        # VILLANOS
        # ========================================================

        for villano in self.villanos:

            # ----------------------------------------------------
            # IMPORTANTE:
            #
            # Antes estaba:
            #
            # if puede_ver_jugador:
            #     actualizar()
            #
            # Eso hacía que los villanos se quedaran quietos
            # cuando una pared bloqueaba la visión.
            #
            # Ahora SIEMPRE intentan seguir al jugador.
            #
            # Las paredes son tenidas en cuenta por
            # villano.actualizar().
            # ----------------------------------------------------

            villano.actualizar(
                self.jugador,
                self.paredes,
                delta_time
            )

            # ----------------------------------------------------
            # DISPARAR SOLAMENTE SI LO VE
            # ----------------------------------------------------

            if villano.puede_ver_jugador(
                self.jugador,
                self.paredes
            ):

                if villano.puede_disparar():

                    proyectil = PoderVillano(
                        villano.center_x,
                        villano.center_y,
                        self.jugador.center_x,
                        self.jugador.center_y
                    )

                    self.proyectiles.append(
                        proyectil
                    )

        # ========================================================
        # PROYECTILES
        # ========================================================

        self.proyectiles.update()

        # ========================================================
        # PROYECTILES CONTRA JUGADOR
        # ========================================================

        impactos = arcade.check_for_collision_with_list(
            self.jugador,
            self.proyectiles
        )

        for proyectil in impactos:

            proyectil.remove_from_sprite_lists()

            self.vida -= 1

            if self.vida <= 0:

                self.reiniciar_nivel()

                return

        # ========================================================
        # PROYECTILES CONTRA PAREDES
        # ========================================================

        for proyectil in list(
            self.proyectiles
        ):

            if self.choca_con_pared(
                proyectil.center_x,
                proyectil.center_y
            ):

                proyectil.remove_from_sprite_lists()

        # ========================================================
        # RECOGER LLAVE
        # ========================================================

        if not self.tiene_llave:

            if arcade.check_for_collision(
                self.jugador,
                self.llave
            ):

                self.tiene_llave = True

                self.llave.remove_from_sprite_lists()

        # ========================================================
        # PUERTA
        # ========================================================

        if self.tiene_llave:

            if arcade.check_for_collision(
                self.jugador,
                self.puerta
            ):

                self.nivel_completado = True

    # ============================================================
    # TECLAS PRESIONADAS
    # ============================================================

    def on_key_press(self, key, modifiers):

        # --------------------------------------------------------
        # ENTER
        # --------------------------------------------------------

        if key == arcade.key.ENTER:

            if not self.juego_empezado:

                self.juego_empezado = True

                return

            if self.nivel_completado:

                import menu

                self.window.show_view(
                    menu.Menu()
                )

                return

        # --------------------------------------------------------
        # MOVIMIENTO
        # --------------------------------------------------------

        if key == arcade.key.UP:

            self.arriba = True

        elif key == arcade.key.DOWN:

            self.abajo = True

        elif key == arcade.key.LEFT:

            self.izquierda = True

        elif key == arcade.key.RIGHT:

            self.derecha = True

    # ============================================================
    # TECLAS SOLTADAS
    # ============================================================

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP:

            self.arriba = False

        elif key == arcade.key.DOWN:

            self.abajo = False

        elif key == arcade.key.LEFT:

            self.izquierda = False

        elif key == arcade.key.RIGHT:

            self.derecha = False

    # ============================================================
    # REINICIAR NIVEL
    # ============================================================

    def reiniciar_nivel(self):

        # --------------------------------------------------------
        # JUGADOR
        # --------------------------------------------------------

        self.jugador.center_x = 768
        self.jugador.center_y = 100

        # --------------------------------------------------------
        # ESTADOS
        # --------------------------------------------------------

        self.vida = 5

        self.tiene_llave = False

        self.juego_empezado = False

        self.nivel_completado = False

        # --------------------------------------------------------
        # LLAVE
        # --------------------------------------------------------

        self.llaves = arcade.SpriteList()

        self.llave = Llave(
            768,
            500
        )

        self.llaves.append(
            self.llave
        )

        # --------------------------------------------------------
        # PUERTA
        # --------------------------------------------------------

        self.puertas = arcade.SpriteList()

        self.puerta = Puerta(
            768,
            930
        )

        self.puertas.append(
            self.puerta
        )

        # --------------------------------------------------------
        # VILLANOS
        # --------------------------------------------------------

        self.villanos = arcade.SpriteList()

        villano_izquierda = VillanoPrincipal(
            230,
            500,
            imagen="imagenes/personajes/enemigos/villano_nivel3.png",
            velocidad=3.5,
            rango_vision=2000,
            espera_disparo=0.6
        )

        villano_derecha = VillanoPrincipal(
            1300,
            500,
            imagen="imagenes/personajes/enemigos/villano_nivel3.png",
            velocidad=3.5,
            rango_vision=2000,
            espera_disparo=0.6
        )

        self.villanos.append(
            villano_izquierda
        )

        self.villanos.append(
            villano_derecha
        )

        # --------------------------------------------------------
        # PROYECTILES
        # --------------------------------------------------------

        self.proyectiles = arcade.SpriteList()

        # --------------------------------------------------------
        # CÁMARA
        # --------------------------------------------------------

        self.camera.zoom = 0.75

        self.camera.position = (
            ANCHO_MAPA / 2,
            ALTO_MAPA / 2
        )

    # ============================================================
    # DIBUJAR
    # ============================================================

    def on_draw(self):

        self.clear()

        # ========================================================
        # CÁMARA FIJA
        # ========================================================

        self.camera.use()

        # ========================================================
        # FONDO
        # ========================================================

        arcade.draw_texture_rect(
            self.fondo,
            arcade.LBWH(
                0,
                0,
                ANCHO_MAPA,
                ALTO_MAPA
            )
        )

        # ========================================================
        # PAREDES
        # ========================================================

        self.paredes.draw()

        # ========================================================
        # LLAVE
        # ========================================================

        self.llaves.draw()

        # ========================================================
        # PUERTA
        # ========================================================

        self.puertas.draw()

        # ========================================================
        # VILLANOS
        # ========================================================

        self.villanos.draw()

        # ========================================================
        # PROYECTILES
        # ========================================================

        self.proyectiles.draw()

        # ========================================================
        # JUGADOR
        # ========================================================

        self.jugadores.draw()

        # ========================================================
        # HUD
        # ========================================================

        arcade.draw_text(
            f"Vida: {self.vida}",
            40,
            950,
            arcade.color.WHITE,
            22
        )

        if self.tiene_llave:

            arcade.draw_text(
                "¡Tenés la llave!",
                40,
                915,
                arcade.color.YELLOW,
                20
            )

        else:

            arcade.draw_text(
                "Buscá la llave",
                40,
                915,
                arcade.color.WHITE,
                20
            )

        # ========================================================
        # CUADRO DE INFORMACIÓN INICIAL
        # ========================================================

        if not self.juego_empezado:

            # ----------------------------------------------------
            # Oscurecemos visualmente el centro
            # ----------------------------------------------------

            arcade.draw_lbwh_rectangle_filled(
                368,
                315,
                800,
                400,
                (20, 15, 30, 235)
            )

            # ----------------------------------------------------
            # Borde del cuadro
            # ----------------------------------------------------

            arcade.draw_lbwh_rectangle_outline(
                368,
                315,
                800,
                400,
                arcade.color.WHITE,
                4
            )

            # ----------------------------------------------------
            # TÍTULO
            # ----------------------------------------------------

            arcade.draw_text(
                "NIVEL 3",
                ANCHO_MAPA / 2,
                625,
                arcade.color.WHITE,
                42,
                anchor_x="center"
            )

            # ----------------------------------------------------
            # INFORMACIÓN
            # ----------------------------------------------------

            arcade.draw_text(
                "Dos enemigos te están buscando.",
                ANCHO_MAPA / 2,
                555,
                arcade.color.WHITE,
                24,
                anchor_x="center"
            )

            arcade.draw_text(
                "Conseguí la llave y llegá hasta la puerta.",
                ANCHO_MAPA / 2,
                510,
                arcade.color.WHITE,
                20,
                anchor_x="center"
            )

            arcade.draw_text(
                "Las paredes pueden ayudarte a cubrirte.",
                ANCHO_MAPA / 2,
                465,
                arcade.color.WHITE,
                20,
                anchor_x="center"
            )

            # ----------------------------------------------------
            # CONTROLES
            # ----------------------------------------------------

            arcade.draw_text(
                "Usá las flechas para moverte.",
                ANCHO_MAPA / 2,
                405,
                arcade.color.WHITE,
                20,
                anchor_x="center"
            )

            # ----------------------------------------------------
            # ENTER
            # ----------------------------------------------------

            arcade.draw_text(
                "Presioná ENTER para comenzar",
                ANCHO_MAPA / 2,
                350,
                arcade.color.YELLOW,
                22,
                anchor_x="center"
            )

        # ========================================================
        # NIVEL COMPLETADO
        # ========================================================

        if self.nivel_completado:

            arcade.draw_lbwh_rectangle_filled(
                368,
                380,
                800,
                260,
                (20, 15, 30, 240)
            )

            arcade.draw_lbwh_rectangle_outline(
                368,
                380,
                800,
                260,
                arcade.color.WHITE,
                4
            )

            arcade.draw_text(
                "¡NIVEL COMPLETADO!",
                ANCHO_MAPA / 2,
                530,
                arcade.color.WHITE,
                40,
                anchor_x="center"
            )

            arcade.draw_text(
                "Presioná ENTER para volver al menú",
                ANCHO_MAPA / 2,
                460,
                arcade.color.WHITE,
                20,
                anchor_x="center"
            )