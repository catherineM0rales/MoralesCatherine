import arcade
import configuracion
from entidades import Player
import nivel2


# ============================================================
# CONFIGURACIÓN DEL MAPA
# ============================================================

ANCHO_MAPA = 1536
ALTO_MAPA = 1024

# El protagonista pasa al Nivel 2 al llegar
# aproximadamente a donde estaba el villano central.
SALIDA_X = 1430

# Margen de las colisiones exteriores.
MARGEN_MAPA = 30


# ============================================================
# ENEMIGO: GUARDIA
# ============================================================

class Guardia(arcade.Sprite):

    def __init__(
        self,
        x,
        y,
        limite_arriba,
        limite_abajo,
        velocidad=1.5
    ):

        super().__init__(
            "imagenes/personajes/enemigos/guardia.png",
            scale=0.08
        )

        self.center_x = x
        self.center_y = y

        self.limite_arriba = limite_arriba
        self.limite_abajo = limite_abajo

        self.velocidad = velocidad

        # Cada guardia tiene su propia dirección.
        self.direccion = 1

    def patrullar(self):

        self.center_y += self.velocidad * self.direccion

        if self.center_y >= self.limite_arriba:

            self.center_y = self.limite_arriba
            self.direccion = -1

        elif self.center_y <= self.limite_abajo:

            self.center_y = self.limite_abajo
            self.direccion = 1


# ============================================================
# VILLANO PRINCIPAL
# ============================================================

class VillanoInseguridad(arcade.Sprite):

    def __init__(self, x, y):

        super().__init__(
            "imagenes/personajes/enemigos/enemigo1.png",
            scale=0.15
        )

        self.center_x = x
        self.center_y = y


# ============================================================
# FRAGMENTOS DEL DIBUJO
# ============================================================

class FragmentoDibujo(arcade.Sprite):

    def __init__(self, x, y):

        super().__init__(
            "imagenes/objetos/dibujo.png",
            scale=0.10
        )

        self.center_x = x
        self.center_y = y


# ============================================================
# NIVEL 1
# ============================================================

class Nivel1(arcade.View):

    def __init__(self):

        super().__init__()


        # ====================================================
        # MAPA
        # ====================================================

        self.mapa = arcade.load_texture(
            "imagenes/mapas/nivel_inseguridad.png"
        )


        # ====================================================
        # CÁMARAS
        # ====================================================

        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()


        # ====================================================
        # JUGADOR
        # ====================================================

        self.player = Player()

        # Posición inicial.
        # Un poco más arriba.
        self.player.center_x = 90
        self.player.center_y = 540

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)


        # ====================================================
        # TECLAS
        # ====================================================

        self.teclas = set()


        # ====================================================
        # VILLANO PRINCIPAL
        # ====================================================

        self.villano = VillanoInseguridad(
            1430,
            540
        )

        self.villano_list = arcade.SpriteList()
        self.villano_list.append(self.villano)


        # ====================================================
        # GUARDIAS
        # ====================================================

        self.guardias = arcade.SpriteList()


        # ----------------------------------------------------
        # PAR 1
        # ----------------------------------------------------

        self.guardias.append(
            Guardia(
                390,
                620,
                720,
                350,
                1.4
            )
        )

        self.guardias.append(
            Guardia(
                390,
                450,
                720,
                350,
                1.1
            )
        )


        # ----------------------------------------------------
        # PAR 2
        # ----------------------------------------------------

        self.guardias.append(
            Guardia(
                720,
                650,
                730,
                300,
                1.7
            )
        )

        self.guardias.append(
            Guardia(
                720,
                420,
                730,
                300,
                1.3
            )
        )


        # ----------------------------------------------------
        # PAR 3
        # ----------------------------------------------------

        self.guardias.append(
            Guardia(
                1060,
                630,
                750,
                350,
                1.5
            )
        )

        self.guardias.append(
            Guardia(
                1060,
                440,
                750,
                350,
                1.2
            )
        )


        # ----------------------------------------------------
        # PAR 4
        # ----------------------------------------------------

        self.guardias.append(
            Guardia(
                1270,
                600,
                700,
                280,
                1.8
            )
        )

        self.guardias.append(
            Guardia(
                1270,
                390,
                700,
                280,
                1.4
            )
        )


        # ====================================================
        # FRAGMENTOS
        # ====================================================

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


        # ====================================================
        # COLISIONES
        # ====================================================

        self.paredes = arcade.SpriteList()

        self.configurar_colisiones()


        # ====================================================
        # FASE DE INTRODUCCIÓN
        # ====================================================

        self.fase = "caminar"

        self.tiempo_fase = 0

        self.destino_intro_x = 230

        self.duracion_caminata = 2.8


        # ====================================================
        # CÁMARA DE INTRODUCCIÓN
        # ====================================================

        self.camera.position = (
            self.player.center_x + 250,
            self.player.center_y
        )


        # Objetivo de la cámara:
        # extremo derecho del mapa.

        self.camera_objetivo_x = (
            ANCHO_MAPA -
            configuracion.ANCHO / 2
        )

        self.camera_objetivo_y = (
            ALTO_MAPA / 2
        )


        # ====================================================
        # CARTEL
        # ====================================================

        self.mostrar_instrucciones = False


        # ====================================================
        # OSCURIDAD
        # ====================================================

        self.opacidad = 0

        self.oscuridad_tiempo = 0

        self.oscuridad_velocidad = 28

        self.oscuridad_maxima = 205

        self.oscuridad_subiendo = False

        self.oscuridad_activa = False


        # ====================================================
        # PARPADEO FINAL
        # ====================================================

        self.final_completado = False

        self.final_parpadeo = False

        self.final_opacidad = 0

        self.final_velocidad = 90


        # ====================================================
        # MENSAJES
        # ====================================================

        self.mensaje = ""

        self.tiempo_mensaje = 0


    # ========================================================
    # COLISIONES
    # ========================================================

    def crear_pared(
        self,
        x,
        y,
        ancho,
        alto
    ):

        pared = arcade.SpriteSolidColor(
            int(ancho),
            int(alto),
            (0, 0, 0, 0)
        )

        pared.center_x = x
        pared.center_y = y

        self.paredes.append(pared)


    def configurar_colisiones(self):

        grosor = 35


        # ----------------------------------------------------
        # BORDE IZQUIERDO
        # ----------------------------------------------------

        self.crear_pared(
            MARGEN_MAPA,
            ALTO_MAPA / 2,
            grosor,
            ALTO_MAPA
        )


        # ----------------------------------------------------
        # BORDE DERECHO
        # ----------------------------------------------------

        self.crear_pared(
            ANCHO_MAPA - MARGEN_MAPA,
            ALTO_MAPA / 2,
            grosor,
            ALTO_MAPA
        )


        # ----------------------------------------------------
        # BORDE SUPERIOR
        # ----------------------------------------------------

        self.crear_pared(
            ANCHO_MAPA / 2,
            ALTO_MAPA - MARGEN_MAPA,
            ANCHO_MAPA,
            grosor
        )


        # ----------------------------------------------------
        # BORDE INFERIOR
        # ----------------------------------------------------

        self.crear_pared(
            ANCHO_MAPA / 2,
            MARGEN_MAPA,
            ANCHO_MAPA,
            grosor
        )


    # ========================================================
    # TECLAS
    # ========================================================

    def on_key_press(
        self,
        key,
        modifiers
    ):

        # ----------------------------------------------------
        # CARTEL
        # ----------------------------------------------------

        if self.fase == "instrucciones":

            if key == arcade.key.ENTER:

                self.mostrar_instrucciones = False

                self.fase = "jugando"

                self.tiempo_fase = 0

                self.oscuridad_activa = True

                self.teclas.clear()

            return


        # ----------------------------------------------------
        # SI TODAVÍA NO ESTAMOS JUGANDO
        # ----------------------------------------------------

        if self.fase != "jugando":

            return


        self.teclas.add(key)


    def on_key_release(
        self,
        key,
        modifiers
    ):

        self.teclas.discard(key)


    # ========================================================
    # MOVIMIENTO DEL JUGADOR
    # ========================================================

    def mover_jugador(self):

        velocidad = configuracion.VELOCIDAD_JUGADOR

        dx = 0
        dy = 0


        # ----------------------------------------------------
        # WASD
        # ----------------------------------------------------

        if arcade.key.W in self.teclas:
            dy += velocidad

        if arcade.key.S in self.teclas:
            dy -= velocidad

        if arcade.key.A in self.teclas:
            dx -= velocidad

        if arcade.key.D in self.teclas:
            dx += velocidad


        # ----------------------------------------------------
        # FLECHAS
        # ----------------------------------------------------

        if arcade.key.UP in self.teclas:
            dy += velocidad

        if arcade.key.DOWN in self.teclas:
            dy -= velocidad

        if arcade.key.LEFT in self.teclas:
            dx -= velocidad

        if arcade.key.RIGHT in self.teclas:
            dx += velocidad


        # ----------------------------------------------------
        # MOVIMIENTO HORIZONTAL
        # ----------------------------------------------------

        self.player.center_x += dx

        if arcade.check_for_collision_with_list(
            self.player,
            self.paredes
        ):

            self.player.center_x -= dx


        # ----------------------------------------------------
        # MOVIMIENTO VERTICAL
        # ----------------------------------------------------

        self.player.center_y += dy

        if arcade.check_for_collision_with_list(
            self.player,
            self.paredes
        ):

            self.player.center_y -= dy


        # ----------------------------------------------------
        # ANIMACIÓN
        # ----------------------------------------------------

        self.player.update_animation(
            dx,
            dy
        )


    # ========================================================
    # CÁMARA
    # ========================================================

    def mover_camara_hacia(
        self,
        objetivo_x,
        objetivo_y,
        delta_time
    ):

        actual_x = self.camera.position[0]
        actual_y = self.camera.position[1]


        # Movimiento suave.
        # Un poco más rápido que antes.

        velocidad = 4.0


        nuevo_x = actual_x + (
            objetivo_x - actual_x
        ) * velocidad * delta_time


        nuevo_y = actual_y + (
            objetivo_y - actual_y
        ) * velocidad * delta_time


        # ----------------------------------------------------
        # LIMITES DE LA CÁMARA
        # ----------------------------------------------------

        mitad_ancho = configuracion.ANCHO / 2
        mitad_alto = configuracion.ALTO / 2


        nuevo_x = max(
            mitad_ancho,
            min(
                ANCHO_MAPA - mitad_ancho,
                nuevo_x
            )
        )


        nuevo_y = max(
            mitad_alto,
            min(
                ALTO_MAPA - mitad_alto,
                nuevo_y
            )
        )


        self.camera.position = (
            nuevo_x,
            nuevo_y
        )


    # ========================================================
    # OSCURIDAD
    # ========================================================

    def actualizar_oscuridad(
        self,
        delta_time
    ):

        if not self.oscuridad_activa:

            return


        self.oscuridad_tiempo += delta_time


        # ----------------------------------------------------
        # ESPERA
        # ----------------------------------------------------

        if not self.oscuridad_subiendo:

            if self.oscuridad_tiempo >= 4.5:

                self.oscuridad_subiendo = True

                self.oscuridad_tiempo = 0


        # ----------------------------------------------------
        # OSCURECER
        # ----------------------------------------------------

        else:

            self.opacidad += (
                self.oscuridad_velocidad *
                delta_time
            )


            if self.opacidad >= self.oscuridad_maxima:

                self.opacidad = self.oscuridad_maxima

                self.oscuridad_subiendo = False

                self.oscuridad_tiempo = 0


        # ----------------------------------------------------
        # ACLARAR
        # ----------------------------------------------------

        if (
            not self.oscuridad_subiendo
            and self.opacidad > 0
        ):

            self.opacidad -= (
                13 * delta_time
            )


            if self.opacidad < 0:

                self.opacidad = 0


    # ========================================================
    # ACTUALIZACIÓN
    # ========================================================

    def on_update(
        self,
        delta_time
    ):

        self.tiempo_fase += delta_time


        # ====================================================
        # 1. CAMINATA INICIAL
        # ====================================================

        if self.fase == "caminar":

            velocidad_intro = 45


            self.player.center_x += (
                velocidad_intro *
                delta_time
            )


            self.player.update_animation(
                velocidad_intro,
                0
            )


            # La cámara acompaña al protagonista.

            self.camera.position = (
                self.player.center_x + 250,
                self.player.center_y
            )


            if (
                self.player.center_x >=
                self.destino_intro_x
                or
                self.tiempo_fase >=
                self.duracion_caminata
            ):

                self.fase = "camara"

                self.tiempo_fase = 0

            return


        # ====================================================
        # 2. CÁMARA VA AL FINAL DEL MAPA
        # ====================================================

        if self.fase == "camara":

            self.mover_camara_hacia(
                self.camera_objetivo_x,
                self.camera_objetivo_y,
                delta_time
            )


            # Después de 3 segundos,
            # aseguramos que llegó.

            if self.tiempo_fase >= 3.0:

                self.camera.position = (
                    self.camera_objetivo_x,
                    self.camera_objetivo_y
                )

                self.fase = "espera_camara"

                self.tiempo_fase = 0

            return


        # ====================================================
        # 3. LA CÁMARA MUESTRA EL MAPA
        # ====================================================

        if self.fase == "espera_camara":

            self.camera.position = (
                self.camera_objetivo_x,
                self.camera_objetivo_y
            )


            # Tiempo mirando el mapa.

            if self.tiempo_fase >= 2.5:

                self.fase = "regreso"

                self.tiempo_fase = 0

            return


        # ====================================================
        # 4. CÁMARA REGRESA AL PROTAGONISTA
        # ====================================================

        if self.fase == "regreso":

            self.mover_camara_hacia(
                self.player.center_x,
                self.player.center_y,
                delta_time
            )


            # Después de 3 segundos,
            # terminamos el regreso.

            if self.tiempo_fase >= 3.0:

                self.camera.position = (
                    self.player.center_x,
                    self.player.center_y
                )


                # ACTIVAR CARTEL.

                self.fase = "instrucciones"

                self.mostrar_instrucciones = True

                self.tiempo_fase = 0

                self.teclas.clear()

            return


        # ====================================================
        # 5. CARTEL
        # ====================================================

        if self.fase == "instrucciones":

            self.mostrar_instrucciones = True

            self.teclas.clear()

            return


        # ====================================================
        # 6. JUEGO
        # ====================================================

        if self.fase != "jugando":

            return


        # ====================================================
        # MOVIMIENTO
        # ====================================================

        self.mover_jugador()


        # ====================================================
        # SALIDA DEL NIVEL
        # ====================================================

        # IMPORTANTE:
        #
        # El jugador pasa al Nivel 2 cuando alcanza
        # la posición horizontal del antiguo villano central.

        if self.player.center_x >= SALIDA_X:

            self.teclas.clear()

            self.window.show_view(
                nivel2.Nivel2()
            )

            return


        # ====================================================
        # GUARDIAS
        # ====================================================

        for guardia in self.guardias:

            guardia.patrullar()


        # ====================================================
        # COLISIÓN CON GUARDIAS
        # ====================================================

        guardias_tocados = (
            arcade.check_for_collision_with_list(
                self.player,
                self.guardias
            )
        )


        if len(guardias_tocados) > 0:

            self.reiniciar_posicion()


        # ====================================================
        # RECOGER FRAGMENTOS
        # ====================================================

        fragmentos_tocados = (
            arcade.check_for_collision_with_list(
                self.player,
                self.fragmentos
            )
        )


        for fragmento in fragmentos_tocados:

            fragmento.remove_from_sprite_lists()

            self.mensaje = (
                "Encontraste un fragmento del dibujo."
            )

            self.tiempo_mensaje = 2.0


        # ====================================================
        # MENSAJE
        # ====================================================

        if self.tiempo_mensaje > 0:

            self.tiempo_mensaje -= delta_time


        # ====================================================
        # CÁMARA NORMAL
        # ====================================================

        self.mover_camara_hacia(
            self.player.center_x,
            self.player.center_y,
            delta_time
        )


        # ====================================================
        # OSCURIDAD
        # ====================================================

        self.actualizar_oscuridad(
            delta_time
        )


        # ====================================================
        # PARPADEO FINAL
        # ====================================================

        # Los fragmentos todavía pueden activar
        # el efecto visual, pero NO controlan
        # el cambio de nivel.

        if (
            len(self.fragmentos) == 0
            and not self.final_parpadeo
            and not self.final_completado
        ):

            self.final_parpadeo = True

            self.final_opacidad = 0

            self.teclas.clear()


        # ----------------------------------------------------
        # SUBIR PARPADEO
        # ----------------------------------------------------

        if self.final_parpadeo:

            self.final_opacidad += (
                self.final_velocidad *
                delta_time
            )


            if self.final_opacidad >= 255:

                self.final_opacidad = 255

                self.guardias.clear()

                self.villano_list.clear()

                self.final_completado = True

                self.final_parpadeo = False

            return


        # ----------------------------------------------------
        # BAJAR PARPADEO
        # ----------------------------------------------------

        if self.final_completado:

            self.final_opacidad -= (
                self.final_velocidad *
                delta_time
            )


            if self.final_opacidad <= 0:

                self.final_opacidad = 0

                self.final_completado = False


    # ========================================================
    # REINICIAR POSICIÓN
    # ========================================================

    def reiniciar_posicion(self):

        self.player.center_x = 230

        self.player.center_y = 540

        self.teclas.clear()

        self.mensaje = (
            "¡Cuidado! Debes esquivar a los guardias."
        )

        self.tiempo_mensaje = 2.0


    # ========================================================
    # DIBUJAR
    # ========================================================

    def on_draw(self):

        self.clear()


        # ====================================================
        # CÁMARA DEL MUNDO
        # ====================================================

        self.camera.use()


        # ====================================================
        # MAPA
        # ====================================================

        arcade.draw_texture_rect(
            self.mapa,
            arcade.LBWH(
                0,
                0,
                ANCHO_MAPA,
                ALTO_MAPA
            )
        )


        # ====================================================
        # FRAGMENTOS
        # ====================================================

        self.fragmentos.draw()


        # ====================================================
        # GUARDIAS
        # ====================================================

        self.guardias.draw()


        # ====================================================
        # VILLANO
        # ====================================================

        self.villano_list.draw()


        # ====================================================
        # JUGADOR
        # ====================================================

        self.player_list.draw()


        # ====================================================
        # CARTEL DE INSTRUCCIONES
        # ====================================================

        if self.fase == "instrucciones":

            self.gui_camera.use()


            # ------------------------------------------------
            # FONDO OSCURO
            # ------------------------------------------------

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                configuracion.ALTO,
                (0, 0, 0, 200)
            )


            # ------------------------------------------------
            # CUADRO
            # ------------------------------------------------

            margen_x = 120
            margen_y = 120


            arcade.draw_lrbt_rectangle_filled(
                margen_x,
                configuracion.ANCHO - margen_x,
                margen_y,
                configuracion.ALTO - margen_y,
                (25, 25, 35)
            )


            arcade.draw_lrbt_rectangle_outline(
                margen_x,
                configuracion.ANCHO - margen_x,
                margen_y,
                configuracion.ALTO - margen_y,
                arcade.color.GOLD,
                3
            )


            centro_x = (
                configuracion.ANCHO / 2
            )


            # ------------------------------------------------
            # TÍTULO
            # ------------------------------------------------

            arcade.draw_text(
                "OBJETIVO",
                centro_x,
                570,
                arcade.color.GOLD,
                32,
                bold=True,
                anchor_x="center"
            )


            # ------------------------------------------------
            # TEXTO
            # ------------------------------------------------

            arcade.draw_text(
                "Encuentra todos los fragmentos",
                centro_x,
                475,
                arcade.color.WHITE,
                22,
                anchor_x="center"
            )


            arcade.draw_text(
                "del dibujo que están dispersos por el mapa.",
                centro_x,
                435,
                arcade.color.WHITE,
                22,
                anchor_x="center"
            )


            arcade.draw_text(
                "Evita a los guardias y llega hasta la salida.",
                centro_x,
                365,
                arcade.color.WHITE,
                22,
                anchor_x="center"
            )


            arcade.draw_text(
                "La oscuridad irá apareciendo poco a poco...",
                centro_x,
                300,
                arcade.color.WHITE,
                22,
                anchor_x="center"
            )


            arcade.draw_text(
                "Cuando tengas todos los fragmentos, podrás escapar.",
                centro_x,
                255,
                arcade.color.WHITE,
                20,
                anchor_x="center"
            )


            # ------------------------------------------------
            # CONTROLES
            # ------------------------------------------------

            arcade.draw_text(
                "WASD / FLECHAS: Moverse",
                centro_x,
                190,
                arcade.color.GOLD,
                20,
                bold=True,
                anchor_x="center"
            )


            # ------------------------------------------------
            # ENTER
            # ------------------------------------------------

            arcade.draw_text(
                "Presiona ENTER para comenzar",
                centro_x,
                145,
                arcade.color.YELLOW,
                19,
                bold=True,
                anchor_x="center"
            )


            # No dibujamos el HUD debajo del cartel.

            return


        # ====================================================
        # HUD
        # ====================================================

        self.gui_camera.use()


        # ----------------------------------------------------
        # CONTADOR
        # ----------------------------------------------------

        arcade.draw_text(
            f"Fragmentos: {len(self.fragmentos)}",
            25,
            configuracion.ALTO - 45,
            arcade.color.WHITE,
            20,
            bold=True
        )


        # ----------------------------------------------------
        # MENSAJE
        # ----------------------------------------------------

        if self.tiempo_mensaje > 0:

            arcade.draw_text(
                self.mensaje,
                configuracion.ANCHO / 2,
                configuracion.ALTO - 75,
                arcade.color.YELLOW,
                18,
                bold=True,
                anchor_x="center"
            )


        # ====================================================
        # OSCURIDAD NORMAL
        # ====================================================

        if self.opacidad > 0:

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                configuracion.ALTO,
                (
                    0,
                    0,
                    0,
                    int(self.opacidad)
                )
            )


        # ====================================================
        # PARPADEO FINAL
        # ====================================================

        if (
            self.final_parpadeo
            or self.final_completado
        ):

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                configuracion.ALTO,
                (
                    0,
                    0,
                    0,
                    int(self.final_opacidad)
                )
            )