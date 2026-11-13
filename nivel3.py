
import arcade
import math
import random

import configuracion
from entidades import Player, VillanoPrincipal, Proyectil as PoderVillano


# ============================================================
# CONFIGURACIÓN DEL MAPA
# ============================================================

ANCHO_MAPA = 1536
ALTO_MAPA = 1024


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

        self.llave = Llave(768, 500)

        self.llaves = arcade.SpriteList()
        self.llaves.append(self.llave)

        # ======================================================
        # PUERTA
        # ======================================================

        self.puerta = Puerta(768, 930)

        self.puertas = arcade.SpriteList()
        self.puertas.append(self.puerta)

        # ======================================================
        # VILLANOS
        # ======================================================

        self.crear_villanos()

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

                ancho = random.randint(100, 220)
                alto = random.randint(60, 110)

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

        # 0 = SIGUIENTE NIVEL
        # 1 = VOLVER AL MENÚ

        self.opcion_final = 0

        # ======================================================
        # MOVIMIENTO
        # ======================================================

        self.arriba = False
        self.abajo = False
        self.izquierda = False
        self.derecha = False

        # ======================================================
        # CÁMARA DEL MAPA
        # ======================================================

        self.camera = arcade.Camera2D()

        self.camera.zoom = 0.75

        self.camera.position = (
            ANCHO_MAPA / 2,
            ALTO_MAPA / 2
        )

        # ======================================================
        # NUEVA CÁMARA DE INTERFAZ
        # ======================================================

        self.gui_camera = arcade.Camera2D()

        self.gui_camera.zoom = 1

        self.gui_camera.position = (
            configuracion.ANCHO / 2,
            configuracion.ALTO / 2
        )

    # ============================================================
    # CREAR VILLANOS
    # ============================================================

    def crear_villanos(self):

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

        self.villanos.append(villano_izquierda)
        self.villanos.append(villano_derecha)

    # ============================================================
    # COLISIÓN CON PARED
    # ============================================================

    def choca_con_pared(self, x, y):

        for pared in self.paredes:

            izquierda = pared.center_x - pared.width / 2
            derecha = pared.center_x + pared.width / 2

            abajo = pared.center_y - pared.height / 2
            arriba = pared.center_y + pared.height / 2

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

            self.jugador.update_animation(0, 0)
            return

        distancia = math.sqrt(dx * dx + dy * dy)

        dx /= distancia
        dy /= distancia

        velocidad = configuracion.VELOCIDAD_JUGADOR

        nuevo_x = self.jugador.center_x + dx * velocidad
        nuevo_y = self.jugador.center_y + dy * velocidad

        # COLISIÓN HORIZONTAL

        if not self.choca_con_pared(
            nuevo_x,
            self.jugador.center_y
        ):

            self.jugador.center_x = nuevo_x

        # COLISIÓN VERTICAL

        if not self.choca_con_pared(
            self.jugador.center_x,
            nuevo_y
        ):

            self.jugador.center_y = nuevo_y

        # LÍMITES DEL MAPA

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

        self.jugador.update_animation(dx, dy)

    # ============================================================
    # ACTUALIZAR
    # ============================================================

    def on_update(self, delta_time):

        if not self.juego_empezado:
            return

        if self.nivel_completado:
            return

        # JUGADOR

        self.mover_jugador()

        # VILLANOS

        for villano in self.villanos:

            villano.actualizar(
                self.jugador,
                self.paredes,
                delta_time
            )

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

                    self.proyectiles.append(proyectil)

        # ======================================================
        # CONTACTO DIRECTO CON LOS VILLANOS
        # ======================================================

        if arcade.check_for_collision_with_list(
            self.jugador,
            self.villanos
        ):

            self.reiniciar_nivel()
            return

        # ======================================================
        # PROYECTILES
        # ======================================================

        self.proyectiles.update()

        # PROYECTILES CONTRA JUGADOR

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

        # PROYECTILES CONTRA PAREDES

        for proyectil in list(self.proyectiles):

            if self.choca_con_pared(
                proyectil.center_x,
                proyectil.center_y
            ):

                proyectil.remove_from_sprite_lists()

        # ======================================================
        # RECOGER LLAVE
        # ======================================================

        if not self.tiene_llave:

            if arcade.check_for_collision(
                self.jugador,
                self.llave
            ):

                self.tiene_llave = True
                self.llave.remove_from_sprite_lists()

        # ======================================================
        # PUERTA
        # ======================================================

        if self.tiene_llave:

            if arcade.check_for_collision(
                self.jugador,
                self.puerta
            ):

                self.nivel_completado = True
                self.opcion_final = 0

    # ============================================================
    # TECLAS PRESIONADAS
    # ============================================================

    def on_key_press(self, key, modifiers):

        # ======================================================
        # PANTALLA DE NIVEL COMPLETADO
        # ======================================================

        if self.nivel_completado:

            if key == arcade.key.UP:

                self.opcion_final = 0

            elif key == arcade.key.DOWN:

                self.opcion_final = 1

            elif key == arcade.key.ENTER:

                if self.opcion_final == 0:

                    import nivel4

                    self.window.show_view(
                        nivel4.Nivel4()
                    )

                elif self.opcion_final == 1:

                    import menu

                    self.window.show_view(
                        menu.Menu()
                    )

            return

        # ======================================================
        # ENTER PARA COMENZAR
        # ======================================================

        if key == arcade.key.ENTER:

            if not self.juego_empezado:

                self.juego_empezado = True
                return

        # ======================================================
        # MOVIMIENTO
        # ======================================================

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

        # JUGADOR

        self.jugador.center_x = 768
        self.jugador.center_y = 100

        # ESTADOS

        self.vida = 5
        self.tiene_llave = False
        self.juego_empezado = False
        self.nivel_completado = False

        self.opcion_final = 0

        self.arriba = False
        self.abajo = False
        self.izquierda = False
        self.derecha = False

        # LLAVE

        self.llaves = arcade.SpriteList()

        self.llave = Llave(768, 500)
        self.llaves.append(self.llave)

        # PUERTA

        self.puertas = arcade.SpriteList()

        self.puerta = Puerta(768, 930)
        self.puertas.append(self.puerta)

        # VILLANOS

        self.crear_villanos()

        # PROYECTILES

        self.proyectiles = arcade.SpriteList()

        # CÁMARA DEL MAPA

        self.camera.zoom = 0.75

        self.camera.position = (
            ANCHO_MAPA / 2,
            ALTO_MAPA / 2
        )

        # CÁMARA DE INTERFAZ

        self.gui_camera.position = (
            configuracion.ANCHO / 2,
            configuracion.ALTO / 2
        )

    # ============================================================
    # DIBUJAR
    # ============================================================

    def on_draw(self):

        self.clear()

        # ======================================================
        # DIBUJAR EL MUNDO CON LA CÁMARA DEL MAPA
        # ======================================================

        self.camera.use()

        # FONDO

        arcade.draw_texture_rect(
            self.fondo,
            arcade.LBWH(
                0,
                0,
                ANCHO_MAPA,
                ALTO_MAPA
            )
        )

        # PAREDES

        self.paredes.draw()

        # LLAVE

        self.llaves.draw()

        # PUERTA

        self.puertas.draw()

        # VILLANOS

        self.villanos.draw()

        # PROYECTILES

        self.proyectiles.draw()

        # JUGADOR

        self.jugadores.draw()

        # ======================================================
        # HUD
        # ======================================================

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

        # ======================================================
        # CUADRO DE INFORMACIÓN INICIAL
        # ======================================================

        if not self.juego_empezado:

            arcade.draw_lbwh_rectangle_filled(
                368,
                315,
                800,
                400,
                (20, 15, 30, 235)
            )

            arcade.draw_lbwh_rectangle_outline(
                368,
                315,
                800,
                400,
                arcade.color.WHITE,
                4
            )

            arcade.draw_text(
                "NIVEL 3",
                ANCHO_MAPA / 2,
                625,
                arcade.color.WHITE,
                42,
                anchor_x="center"
            )

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

            arcade.draw_text(
                "Usá las flechas para moverte.",
                ANCHO_MAPA / 2,
                405,
                arcade.color.WHITE,
                20,
                anchor_x="center"
            )

            arcade.draw_text(
                "Presioná ENTER para comenzar",
                ANCHO_MAPA / 2,
                350,
                arcade.color.YELLOW,
                22,
                anchor_x="center"
            )

        # ======================================================
        # PANTALLA DE NIVEL COMPLETADO
        # ======================================================

        if self.nivel_completado:

            # CAMBIAR A LA CÁMARA DE INTERFAZ

            self.gui_camera.position = (
                configuracion.ANCHO / 2,
                configuracion.ALTO / 2
            )

            self.gui_camera.use()

            # FONDO OSCURO: CUBRE TODA LA VENTANA

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                configuracion.ALTO,
                (0, 0, 0, 220)
            )

            # VENTANA CENTRAL

            arcade.draw_lrbt_rectangle_filled(
                250,
                configuracion.ANCHO - 250,
                180,
                configuracion.ALTO - 180,
                (25, 25, 35)
            )

            # BORDE DORADO

            arcade.draw_lrbt_rectangle_outline(
                250,
                configuracion.ANCHO - 250,
                180,
                configuracion.ALTO - 180,
                arcade.color.GOLD,
                3
            )

            # TÍTULO

            arcade.draw_text(
                "NIVEL COMPLETADO",
                configuracion.ANCHO / 2,
                550,
                arcade.color.GOLD,
                36,
                bold=True,
                anchor_x="center"
            )

            # PREGUNTA

            arcade.draw_text(
                "¿Qué querés hacer?",
                configuracion.ANCHO / 2,
                470,
                arcade.color.WHITE,
                24,
                anchor_x="center"
            )

            # SIGUIENTE NIVEL

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

            # VOLVER AL MENÚ

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

            # INDICACIONES

            arcade.draw_text(
                "↑ ↓  Seleccionar     ENTER  Confirmar",
                configuracion.ANCHO / 2,
                220,
                arcade.color.LIGHT_GRAY,
                17,
                anchor_x="center"
            )
