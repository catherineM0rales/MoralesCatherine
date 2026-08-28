import arcade
import math
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

class Proyectil(arcade.SpriteSolidColor):

    def __init__(self, x, y, jugador_x, jugador_y):

        super().__init__(
            width=18,
            height=18,
            color=(150, 90, 220)
        )

        self.center_x = x
        self.center_y = y

        # Dirección hacia el jugador
        dx = jugador_x - x
        dy = jugador_y - y

        distancia = math.sqrt(
            dx ** 2 + dy ** 2
        )

        if distancia == 0:
            distancia = 1

        self.direccion_x = dx / distancia
        self.direccion_y = dy / distancia

        # Velocidad
        self.velocidad = 4.5

    def mover(self):

        self.center_x += (
            self.direccion_x *
            self.velocidad
        )

        self.center_y += (
            self.direccion_y *
            self.velocidad
        )


# ============================================================
# RECUERDO
# ============================================================

class Recuerdo(arcade.Sprite):

    def __init__(self, x, y):

        super().__init__(
            "imagenes/objetos/recuerdo.png",
            scale=0.10
        )

        self.center_x = x
        self.center_y = y


# ============================================================
# NIVEL 2
# ============================================================

class Nivel2(arcade.View):

    def __init__(self):

        super().__init__()

        # ====================================================
        # MAPA
        # ====================================================

        self.mapa = arcade.load_texture(
            "imagenes/mapas/nivel2.png"
        )

        # ====================================================
        # CÁMARAS
        # ====================================================

        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        # ====================================================
        # CÁMARA FIJA
        # ====================================================

        zoom_x = (
            configuracion.ANCHO /
            ANCHO_MAPA
        )

        zoom_y = (
            configuracion.ALTO /
            ALTO_MAPA
        )

        self.zoom_mapa = (
            min(zoom_x, zoom_y) * 0.95
        )

        self.camera.zoom = self.zoom_mapa

        self.camera.position = (
            ANCHO_MAPA / 2,
            ALTO_MAPA / 2
        )

        # ====================================================
        # JUGADOR
        # ====================================================

        self.player = Player()

        self.player.center_x = 90
        self.player.center_y = 570

        self.player_list = arcade.SpriteList()
        self.player_list.append(
            self.player
        )

        # ====================================================
        # VIDA
        # ====================================================

        self.vida_maxima = 5
        self.vida = self.vida_maxima

        self.invulnerable = False
        self.tiempo_invulnerable = 0
        self.parpadeo_daño = 0

        # ====================================================
        # MOVIMIENTO
        # ====================================================

        self.teclas = set()

        # ====================================================
        # VILLANO
        # ====================================================

        self.villano = VillanoPrincipal(
            1420,
            570
        )

        self.villano.velocidad = 1.35

        self.villano_list = arcade.SpriteList()
        self.villano_list.append(
            self.villano
        )

        # ====================================================
        # PROYECTILES
        # ====================================================

        self.proyectiles = arcade.SpriteList()

        self.tiempo_disparo = 0
        self.intervalo_disparo = 1.15

        # ====================================================
        # RECUERDOS
        # ====================================================

        self.recuerdos = arcade.SpriteList()

        posiciones_recuerdos = [
            (330, 820),
            (620, 300),
            (850, 760),
            (1120, 330),
            (1260, 800)
        ]

        for x, y in posiciones_recuerdos:

            recuerdo = Recuerdo(
                x,
                y
            )

            self.recuerdos.append(
                recuerdo
            )

        self.total_recuerdos = len(
            self.recuerdos
        )

        # ====================================================
        # PUERTA / SALIDA
        # ====================================================

        # La puerta está en el centro
        # de la pared superior.

        self.salida_x_min = 690
        self.salida_x_max = 846

        self.salida_y_min = 900
        self.salida_y_max = 1024

        # ====================================================
        # ESTADOS DEL NIVEL
        # ====================================================

        self.fase = "presentacion"

        self.tiempo_fase = 0

        self.mostrar_instrucciones = False

        # ====================================================
        # PANTALLAS FINALES
        # ====================================================

        self.mostrando_felicitacion = False
        self.mostrando_pregunta = False
        self.mostrando_final = False

        self.final_ganado = False

        # ====================================================
        # MENSAJES
        # ====================================================

        self.mensaje = ""
        self.tiempo_mensaje = 0

    # ========================================================
    # MOVIMIENTO DEL JUGADOR
    # ========================================================

    def mover_jugador(self):

        velocidad = (
            configuracion.VELOCIDAD_JUGADOR
        )

        dx = 0
        dy = 0

        # WASD

        if arcade.key.W in self.teclas:
            dy += velocidad

        if arcade.key.S in self.teclas:
            dy -= velocidad

        if arcade.key.A in self.teclas:
            dx -= velocidad

        if arcade.key.D in self.teclas:
            dx += velocidad

        # FLECHAS

        if arcade.key.UP in self.teclas:
            dy += velocidad

        if arcade.key.DOWN in self.teclas:
            dy -= velocidad

        if arcade.key.LEFT in self.teclas:
            dx -= velocidad

        if arcade.key.RIGHT in self.teclas:
            dx += velocidad

        # Movimiento horizontal

        self.player.center_x += dx

        if self.player.left < 35:
            self.player.left = 35

        if self.player.right > ANCHO_MAPA - 35:
            self.player.right = (
                ANCHO_MAPA - 35
            )

        # Movimiento vertical

        self.player.center_y += dy

        if self.player.bottom < 35:
            self.player.bottom = 35

        if self.player.top > ALTO_MAPA - 35:
            self.player.top = (
                ALTO_MAPA - 35
            )

        # Animación

        self.player.update_animation(
            dx,
            dy
        )

    # ========================================================
    # DISPARAR PROYECTIL
    # ========================================================

    def disparar_proyectil(self):

        proyectil = Proyectil(
            self.villano.center_x,
            self.villano.center_y,
            self.player.center_x,
            self.player.center_y
        )

        self.proyectiles.append(
            proyectil
        )

    # ========================================================
    # ACTUALIZAR PROYECTILES
    # ========================================================

    def actualizar_proyectiles(
        self,
        delta_time
    ):

        self.tiempo_disparo += delta_time

        # Disparo

        if (
            self.tiempo_disparo
            >= self.intervalo_disparo
        ):

            self.disparar_proyectil()

            self.tiempo_disparo = 0

        # Movimiento

        for proyectil in self.proyectiles:

            proyectil.mover()

            # Eliminar si sale del mapa

            if (
                proyectil.center_x < 0
                or
                proyectil.center_x > ANCHO_MAPA
                or
                proyectil.center_y < 0
                or
                proyectil.center_y > ALTO_MAPA
            ):

                proyectil.remove_from_sprite_lists()

        # Colisión con jugador

        if not self.invulnerable:

            proyectiles_tocados = (
                arcade.check_for_collision_with_list(
                    self.player,
                    self.proyectiles
                )
            )

            if len(proyectiles_tocados) > 0:

                for proyectil in proyectiles_tocados:

                    proyectil.remove_from_sprite_lists()

                self.recibir_daño()

    # ========================================================
    # RECIBIR DAÑO
    # ========================================================

    def recibir_daño(self):

        self.vida -= 1

        self.invulnerable = True
        self.tiempo_invulnerable = 0

        self.parpadeo_daño = 0.30

        self.mensaje = "¡Cuidado!"
        self.tiempo_mensaje = 1.0

        # Si pierde toda la vida

        if self.vida <= 0:

            self.reiniciar_nivel()

    # ========================================================
    # REINICIAR NIVEL
    # ========================================================

    def reiniciar_nivel(self):

        self.player.center_x = 90
        self.player.center_y = 570

        self.villano.center_x = 1420
        self.villano.center_y = 570

        self.vida = self.vida_maxima

        self.invulnerable = False
        self.tiempo_invulnerable = 0
        self.parpadeo_daño = 0

        self.proyectiles.clear()
        self.teclas.clear()

        self.tiempo_disparo = 0

        self.mensaje = (
            "¡Debes intentarlo nuevamente!"
        )

        self.tiempo_mensaje = 2.0

        # Recrear recuerdos

        self.recuerdos.clear()

        posiciones_recuerdos = [
            (330, 820),
            (620, 300),
            (850, 760),
            (1120, 330),
            (1260, 800)
        ]

        for x, y in posiciones_recuerdos:

            self.recuerdos.append(
                Recuerdo(x, y)
            )

    # ========================================================
    # ACTUALIZAR INVULNERABILIDAD
    # ========================================================

    def actualizar_invulnerabilidad(
        self,
        delta_time
    ):

        if self.invulnerable:

            self.tiempo_invulnerable += (
                delta_time
            )

            if (
                self.tiempo_invulnerable
                >= 0.8
            ):

                self.invulnerable = False
                self.tiempo_invulnerable = 0

        if self.parpadeo_daño > 0:

            self.parpadeo_daño -= (
                delta_time
            )

    # ========================================================
    # ACTUALIZAR CÁMARA
    # ========================================================

    def actualizar_camara(self):

        self.camera.position = (
            ANCHO_MAPA / 2,
            ALTO_MAPA / 2
        )

        self.camera.zoom = self.zoom_mapa

    # ========================================================
    # ACTUALIZACIÓN
    # ========================================================

    def on_update(
        self,
        delta_time
    ):

        self.tiempo_fase += delta_time

        # ====================================================
        # PRESENTACIÓN
        # ====================================================

        if self.fase == "presentacion":

            self.actualizar_camara()

            if self.tiempo_fase >= 3.5:

                self.fase = "instrucciones"

                self.tiempo_fase = 0

                self.mostrar_instrucciones = True

            return

        # ====================================================
        # INSTRUCCIONES
        # ====================================================

        if self.fase == "instrucciones":

            self.actualizar_camara()

            return

        # ====================================================
        # FELICITACIÓN
        # ====================================================

        if self.fase == "felicitacion":

            self.actualizar_camara()

            return

        # ====================================================
        # PREGUNTA
        # ====================================================

        if self.fase == "pregunta":

            self.actualizar_camara()

            return

        # ====================================================
        # FINAL
        # ====================================================

        if self.fase == "final":

            self.actualizar_camara()

            return

        # ====================================================
        # JUEGO
        # ====================================================

        if self.fase != "jugando":

            return

        # ====================================================
        # MOVIMIENTO
        # ====================================================

        self.mover_jugador()

        # ====================================================
        # PERSECUCIÓN DEL VILLANO
        # ====================================================

        self.villano.perseguir(
            self.player.center_x,
            self.player.center_y
        )

        # ====================================================
        # PROYECTILES
        # ====================================================

        self.actualizar_proyectiles(
            delta_time
        )

        # ====================================================
        # INVULNERABILIDAD
        # ====================================================

        self.actualizar_invulnerabilidad(
            delta_time
        )

        # ====================================================
        # COLISIÓN DIRECTA CON VILLANO
        # ====================================================

        if arcade.check_for_collision(
            self.player,
            self.villano
        ):

            self.reiniciar_nivel()

            return

        # ====================================================
        # RECOGER RECUERDOS
        # ====================================================

        recuerdos_tocados = (
            arcade.check_for_collision_with_list(
                self.player,
                self.recuerdos
            )
        )

        for recuerdo in recuerdos_tocados:

            recuerdo.remove_from_sprite_lists()

            self.mensaje = (
                "Has recuperado un recuerdo."
            )

            self.tiempo_mensaje = 1.5

        # ====================================================
        # PUERTA / SALIDA
        # ====================================================

        if (
            self.salida_x_min
            <= self.player.center_x
            <= self.salida_x_max
            and
            self.salida_y_min
            <= self.player.center_y
            <= self.salida_y_max
        ):

            # Faltan recuerdos

            if len(self.recuerdos) > 0:

                self.mensaje = (
                    "Necesitas todos tus recuerdos "
                    "para poder salir."
                )

                self.tiempo_mensaje = 2.0

            # Tiene todos los recuerdos

            else:

                self.teclas.clear()

                self.mostrando_felicitacion = True

                self.fase = "felicitacion"

                self.tiempo_fase = 0

                return

        # ====================================================
        # MENSAJE
        # ====================================================

        if self.tiempo_mensaje > 0:

            self.tiempo_mensaje -= (
                delta_time
            )

        # ====================================================
        # CÁMARA
        # ====================================================

        self.actualizar_camara()

    # ========================================================
    # TECLAS
    # ========================================================

    def on_key_press(
        self,
        key,
        modifiers
    ):

        # ====================================================
        # INSTRUCCIONES
        # ====================================================

        if self.fase == "instrucciones":

            if key == arcade.key.ENTER:

                self.mostrar_instrucciones = False

                self.fase = "jugando"

                self.tiempo_fase = 0

            return

        # ====================================================
        # FELICITACIÓN
        # ====================================================

        if self.fase == "felicitacion":

            if key == arcade.key.ENTER:

                self.mostrando_felicitacion = False

                self.mostrando_pregunta = True

                self.fase = "pregunta"

                self.tiempo_fase = 0

            return

        # ====================================================
        # PREGUNTA
        # ====================================================

        if self.fase == "pregunta":

            # Respuesta B = correcta

            if key == arcade.key.B:

                self.final_ganado = True

                self.mostrando_pregunta = False

                self.mostrando_final = True

                self.fase = "final"

                self.tiempo_fase = 0

            # Respuesta A = incorrecta

            elif key == arcade.key.A:

                self.final_ganado = False

                self.mostrando_pregunta = False

                self.mostrando_final = True

                self.fase = "final"

                self.tiempo_fase = 0

            return

        # ====================================================
        # FINAL
        # ====================================================

        if self.fase == "final":

            if key == arcade.key.ENTER:

                arcade.exit()

            return

        # ====================================================
        # JUEGO
        # ====================================================

        if self.fase != "jugando":

            return

        self.teclas.add(key)

    # ========================================================
    # SOLTAR TECLAS
    # ========================================================

    def on_key_release(
        self,
        key,
        modifiers
    ):

        self.teclas.discard(key)

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
        # RECUERDOS
        # ====================================================

        self.recuerdos.draw()

        # ====================================================
        # PROYECTILES
        # ====================================================

        self.proyectiles.draw()

        # ====================================================
        # VILLANO
        # ====================================================

        self.villano_list.draw()

        # ====================================================
        # JUGADOR
        # ====================================================

        if self.parpadeo_daño <= 0:

            self.player_list.draw()

        else:

            if (
                int(
                    self.parpadeo_daño * 20
                ) % 2 == 0
            ):

                self.player_list.draw()

        # ====================================================
        # INTERFAZ
        # ====================================================

        self.gui_camera.use()

        # ====================================================
        # INSTRUCCIONES
        # ====================================================

        if self.mostrar_instrucciones:

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                configuracion.ALTO,
                (0, 0, 0, 200)
            )

            margen_x = 120
            margen_y = 100

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

            arcade.draw_text(
                "NIVEL 2",
                centro_x,
                570,
                arcade.color.GOLD,
                36,
                bold=True,
                anchor_x="center"
            )

            arcade.draw_text(
                "RECUPERA TUS RECUERDOS",
                centro_x,
                515,
                arcade.color.WHITE,
                22,
                bold=True,
                anchor_x="center"
            )

            arcade.draw_text(
                "Encuentra todos los recuerdos",
                centro_x,
                425,
                arcade.color.WHITE,
                21,
                anchor_x="center"
            )

            arcade.draw_text(
                "que están dispersos por el mapa.",
                centro_x,
                390,
                arcade.color.WHITE,
                21,
                anchor_x="center"
            )

            arcade.draw_text(
                "El villano te perseguirá",
                centro_x,
                330,
                arcade.color.WHITE,
                21,
                anchor_x="center"
            )

            arcade.draw_text(
                "y lanzará proyectiles hacia ti.",
                centro_x,
                295,
                arcade.color.WHITE,
                21,
                anchor_x="center"
            )

            arcade.draw_text(
                "Esquiva los proyectiles para no perder vida.",
                centro_x,
                245,
                arcade.color.WHITE,
                19,
                anchor_x="center"
            )

            arcade.draw_text(
                "WASD / FLECHAS: Moverse",
                centro_x,
                185,
                arcade.color.GOLD,
                20,
                bold=True,
                anchor_x="center"
            )

            arcade.draw_text(
                "Presiona ENTER para comenzar",
                centro_x,
                135,
                arcade.color.YELLOW,
                19,
                bold=True,
                anchor_x="center"
            )

            return

        # ====================================================
        # HUD
        # ====================================================

        # VIDA

        arcade.draw_text(
            "VIDA",
            25,
            configuracion.ALTO - 42,
            arcade.color.WHITE,
            18,
            bold=True
        )

        for i in range(
            self.vida_maxima
        ):

            if i < self.vida:

                texto = "♥"
                color = arcade.color.RED

            else:

                texto = "♡"
                color = arcade.color.GRAY

            arcade.draw_text(
                texto,
                85 + i * 30,
                configuracion.ALTO - 47,
                color,
                25,
                bold=True
            )

        # ====================================================
        # RECUERDOS
        # ====================================================

        arcade.draw_text(
            f"Recuerdos: {len(self.recuerdos)}"
            f"/{self.total_recuerdos}",
            configuracion.ANCHO - 250,
            configuracion.ALTO - 42,
            arcade.color.WHITE,
            18,
            bold=True
        )

        # ====================================================
        # MENSAJE
        # ====================================================

        if self.tiempo_mensaje > 0:

            arcade.draw_text(
                self.mensaje,
                configuracion.ANCHO / 2,
                configuracion.ALTO - 70,
                arcade.color.YELLOW,
                18,
                bold=True,
                anchor_x="center"
            )

        # ====================================================
        # FELICITACIÓN
        # ====================================================

        if self.mostrando_felicitacion:

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                configuracion.ALTO,
                (0, 0, 0, 190)
            )

            arcade.draw_lrbt_rectangle_filled(
                180,
                configuracion.ANCHO - 180,
                140,
                configuracion.ALTO - 140,
                (35, 35, 45)
            )

            arcade.draw_lrbt_rectangle_outline(
                180,
                configuracion.ANCHO - 180,
                140,
                configuracion.ALTO - 140,
                arcade.color.GOLD,
                4
            )

            centro_x = (
                configuracion.ANCHO / 2
            )

            arcade.draw_text(
                "¡FELICIDADES!",
                centro_x,
                500,
                arcade.color.GOLD,
                34,
                bold=True,
                anchor_x="center"
            )

            arcade.draw_text(
                "Has recuperado todos tus recuerdos.",
                centro_x,
                415,
                arcade.color.WHITE,
                23,
                anchor_x="center"
            )

            arcade.draw_text(
                "Enfrentar los miedos, pedir ayuda",
                centro_x,
                355,
                arcade.color.WHITE,
                21,
                anchor_x="center"
            )

            arcade.draw_text(
                "y seguir adelante siempre vale la pena.",
                centro_x,
                320,
                arcade.color.WHITE,
                21,
                anchor_x="center"
            )

            arcade.draw_text(
                "Ahora pondrás a prueba lo aprendido.",
                centro_x,
                250,
                arcade.color.GOLD,
                21,
                bold=True,
                anchor_x="center"
            )

            arcade.draw_text(
                "Presiona ENTER para continuar",
                centro_x,
                180,
                arcade.color.YELLOW,
                20,
                bold=True,
                anchor_x="center"
            )

        # ====================================================
        # PREGUNTA
        # ====================================================

        elif self.mostrando_pregunta:

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                configuracion.ALTO,
                (0, 0, 0, 200)
            )

            arcade.draw_lrbt_rectangle_filled(
                180,
                configuracion.ANCHO - 180,
                140,
                configuracion.ALTO - 140,
                (35, 35, 45)
            )

            arcade.draw_lrbt_rectangle_outline(
                180,
                configuracion.ANCHO - 180,
                140,
                configuracion.ALTO - 140,
                arcade.color.GOLD,
                4
            )

            centro_x = (
                configuracion.ANCHO / 2
            )

            arcade.draw_text(
                "RESPONDE LA SIGUIENTE PREGUNTA",
                centro_x,
                500,
                arcade.color.GOLD,
                28,
                bold=True,
                anchor_x="center"
            )

            arcade.draw_text(
                "¿Qué debería hacer una persona si siente",
                centro_x,
                415,
                arcade.color.WHITE,
                21,
                bold=True,
                anchor_x="center"
            )

            arcade.draw_text(
                "tristeza o ansiedad durante mucho tiempo?",
                centro_x,
                380,
                arcade.color.WHITE,
                21,
                bold=True,
                anchor_x="center"
            )

            arcade.draw_text(
                "A) Guardárselo para sí mismo.",
                centro_x,
                285,
                arcade.color.RED,
                21,
                anchor_x="center"
            )

            arcade.draw_text(
                "B) Hablar con alguien de confianza y buscar ayuda.",
                centro_x,
                225,
                arcade.color.GREEN,
                21,
                anchor_x="center"
            )

            arcade.draw_text(
                "Presiona A o B",
                centro_x,
                155,
                arcade.color.YELLOW,
                20,
                bold=True,
                anchor_x="center"
            )

        # ====================================================
        # FINAL
        # ====================================================

        elif self.mostrando_final:

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                configuracion.ALTO,
                (0, 0, 0, 210)
            )

            arcade.draw_lrbt_rectangle_filled(
                180,
                configuracion.ANCHO - 180,
                140,
                configuracion.ALTO - 140,
                (35, 35, 45)
            )

            arcade.draw_lrbt_rectangle_outline(
                180,
                configuracion.ANCHO - 180,
                140,
                configuracion.ALTO - 140,
                arcade.color.GOLD,
                4
            )

            centro_x = (
                configuracion.ANCHO / 2
            )

            # =================================================
            # FINAL BUENO
            # =================================================

            if self.final_ganado:

                arcade.draw_text(
                    "¡FELICIDADES!",
                    centro_x,
                    470,
                    arcade.color.GOLD,
                    34,
                    bold=True,
                    anchor_x="center"
                )

                arcade.draw_text(
                    "Elegiste la respuesta correcta.",
                    centro_x,
                    395,
                    arcade.color.WHITE,
                    22,
                    anchor_x="center"
                )

                arcade.draw_text(
                    "Hablar con alguien de confianza",
                    centro_x,
                    340,
                    arcade.color.WHITE,
                    21,
                    anchor_x="center"
                )

                arcade.draw_text(
                    "y buscar ayuda puede marcar la diferencia.",
                    centro_x,
                    305,
                    arcade.color.WHITE,
                    21,
                    anchor_x="center"
                )

                arcade.draw_text(
                    "Has logrado escapar de la oscuridad.",
                    centro_x,
                    245,
                    arcade.color.GOLD,
                    21,
                    bold=True,
                    anchor_x="center"
                )

            # =================================================
            # FINAL INCORRECTO
            # =================================================

            else:

                arcade.draw_text(
                    "FIN DEL JUEGO",
                    centro_x,
                    470,
                    arcade.color.RED,
                    34,
                    bold=True,
                    anchor_x="center"
                )

                arcade.draw_text(
                    "Esa no era la mejor decisión.",
                    centro_x,
                    395,
                    arcade.color.WHITE,
                    22,
                    anchor_x="center"
                )

                arcade.draw_text(
                    "Guardar lo que sentimos para nosotros",
                    centro_x,
                    340,
                    arcade.color.WHITE,
                    21,
                    anchor_x="center"
                )

                arcade.draw_text(
                    "puede hacer que sea más difícil enfrentarlo.",
                    centro_x,
                    305,
                    arcade.color.WHITE,
                    21,
                    anchor_x="center"
                )

                arcade.draw_text(
                    "No tienes por qué enfrentarlo en soledad.",
                    centro_x,
                    245,
                    arcade.color.GOLD,
                    21,
                    bold=True,
                    anchor_x="center"
                )

            arcade.draw_text(
                "Presiona ENTER para salir",
                centro_x,
                175,
                arcade.color.YELLOW,
                20,
                bold=True,
                anchor_x="center"
            )