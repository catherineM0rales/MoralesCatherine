import arcade
import configuracion


class Nivel1(arcade.View):

    def __init__(self):
        super().__init__()

        # Fondo del nivel
        self.fondo = arcade.load_texture("imagenes/mapas/nivel1.png")

        # Sprite del protagonista
        self.jugador = arcade.Sprite(
            "imagenes/personajes/protagonista/quieto.png",
            scale=0.15
            
        )
        self.lista_jugadores = arcade.SpriteList()
        self.lista_jugadores.append(self.jugador)
        self.textura_quieto = arcade.load_texture(
            "imagenes/personajes/protagonista/quieto.png"
        )

        self.textura_caminar1 = arcade.load_texture(
            "imagenes/personajes/protagonista/caminar1.png"
        )

        self.textura_caminar2 = arcade.load_texture(
            "imagenes/personajes/protagonista/caminar2.png"
        )
        # El jugador comienza usando el sprite quieto
        self.jugador.texture = self.textura_quieto

        # Variables para la animación
        self.contador_animacion = 0
        self.frame_animacion = 0
        # ==========================================
        # POSICIÓN INICIAL DEL JUGADOR
        # ==========================================

        self.posicion_inicial_jugador = (150, 120)

        self.jugador.center_x = self.posicion_inicial_jugador[0]
        self.jugador.center_y = self.posicion_inicial_jugador[1]

        # ==========================================
        # VILLANO
        # ==========================================

        self.villano = arcade.Sprite(
            "imagenes/personajes/villano.png",
            scale=0.15
        )

        # ==========================================
        # POSICIÓN INICIAL DEL VILLANO
        # ==========================================

        self.posicion_inicial_villano = (900, 500)

        self.villano.center_x = self.posicion_inicial_villano[0]
        self.villano.center_y = self.posicion_inicial_villano[1]

        self.lista_villanos = arcade.SpriteList()
        self.lista_villanos.append(self.villano)

        self.velocidad_villano = 2

        # Estado del jugador
        self.jugador_muerto = False
        # ==========================================
        # RECUERDOS (GEMAS)
        # ==========================================
        # Crear los recuerdos
        self.crear_recuerdos()

        # Contador de recuerdos
        self.recuerdos_conseguidos = 0

        # ==========================================
        # MENSAJE TEMPORAL
        # ==========================================

        self.mensaje = ""
        self.tiempo_mensaje = 0
        # ==========================================
        # PREGUNTA FINAL
        # ==========================================

        self.mostrando_pregunta = False
        self.mostrando_felicitacion = False
        self.mostrando_final = False
        self.final_ganado = False
        # ==========================================
        # SALIDA DEL NIVEL
        # ==========================================

        self.salida_x_min = 570
        self.salida_x_max = 710

        self.salida_y = 640

        # Movimiento
        self.velocidad_x = 0
        self.velocidad_y = 0

    def on_draw(self):

        self.clear()

        # Dibujar el mapa ocupando toda la ventana
        arcade.draw_texture_rect(
            self.fondo,
            arcade.LBWH(
                0,
                0,
                configuracion.ANCHO,
                configuracion.ALTO
            )
        )

        self.lista_jugadores.draw()
        self.lista_villanos.draw()
        self.lista_recuerdos.draw()

        arcade.draw_text(
            f"Recuerdos: {self.recuerdos_conseguidos}/3",
            20,
            configuracion.ALTO - 40,
            arcade.color.WHITE,
            20
        )
        if self.tiempo_mensaje > 0:

            arcade.draw_text(
                self.mensaje,
                350,
                670,
                arcade.color.YELLOW,
                24,
                bold=True
            )

        if self.mostrando_felicitacion:

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                configuracion.ALTO,
                (0, 0, 0, 150)
            )

            arcade.draw_lrbt_rectangle_filled(
                180,
                1100,
                140,
                580,
                (35, 35, 35)
            )

            arcade.draw_lrbt_rectangle_outline(
                180,
                1100,
                140,
                580,
                arcade.color.WHITE,
                4
            )

            arcade.draw_text(
                "¡Felicidades!",
                0,
                500,
                arcade.color.GOLD,
                34,
                bold=True,
                width=configuracion.ANCHO,
                align="center"
            )

            arcade.draw_text(
                "Has recuperado todos tus recuerdos.",
                300,
                410,
                arcade.color.WHITE,
                24
            )

            arcade.draw_text(
                "Eso demuestra que enfrentar los miedos,",
                250,
                360,
                arcade.color.WHITE,
                24
            )

            arcade.draw_text(
                "pedir ayuda y seguir adelante",
                310,
                320,
                arcade.color.WHITE,
                24
            )

            arcade.draw_text(
                "siempre vale la pena.",
                370,
                280,
                arcade.color.WHITE,
                24
            )

            arcade.draw_text(
                "Ahora pondrás a prueba lo aprendido.",
                0,
                240,
                arcade.color.GOLD,
                24,
                bold=True,
                width=configuracion.ANCHO,
                align="center"
            )

            arcade.draw_text(
                "Presiona ENTER para continuar",
                0,
                170,
                arcade.color.YELLOW,
                22,
                bold=True,
                width=configuracion.ANCHO,
                align="center"
            )
        # ==========================================
        # PREGUNTA EDUCATIVA
        # ==========================================

        # ==========================================
        # PREGUNTA EDUCATIVA
        # ==========================================

        if self.mostrando_pregunta:

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                configuracion.ALTO,
                (0, 0, 0, 150)
            )

            arcade.draw_lrbt_rectangle_filled(
                180,
                1100,
                140,
                580,
                (35, 35, 35)
            )

            arcade.draw_lrbt_rectangle_outline(
                180,
                1100,
                140,
                580,
                arcade.color.WHITE,
                4
            )

            arcade.draw_text(
                "Responde la siguiente pregunta",
                0,
                500,
                arcade.color.GOLD,
                30,
                bold=True,
                width=configuracion.ANCHO,
                align="center"
            )

            arcade.draw_text(
                "¿Qué debería hacer una persona",
                250,
                400,
                arcade.color.WHITE,
                24,
                bold=True
            )

            arcade.draw_text(
                "si siente tristeza o ansiedad",
                280,
                360,
                arcade.color.WHITE,
                24,
                bold=True
            )

            arcade.draw_text(
                "durante mucho tiempo?",
                340,
                320,
                arcade.color.WHITE,
                24,
                bold=True
            )
            arcade.draw_text(
                "A) Guardárselo para sí mismo.",
                300,
                260,
                arcade.color.RED,
                22
            )

            arcade.draw_text(
                "B) Hablar con alguien de confianza",
                300,
                200,
                arcade.color.GREEN,
                22
            )

            arcade.draw_text(
                "    y buscar ayuda.",
                330,
                170,
                arcade.color.GREEN,
                22
            )

            arcade.draw_text(
                "Presiona A o B",
                0,
                100,
                arcade.color.YELLOW,
                22,
                bold=True,
                width=configuracion.ANCHO,
                align="center"
            )
    def on_update(self, delta_time):
        # Si se está mostrando la pregunta, detener el juego
        if self.mostrando_pregunta:
            return

    # Movimiento
        self.jugador.center_x += self.velocidad_x
        self.jugador.center_y += self.velocidad_y

    # Si el jugador se está moviendo...
        if self.velocidad_x != 0 or self.velocidad_y != 0:

            self.contador_animacion += 1

        # Cambiar de sprite cada 10 actualizaciones
            if self.contador_animacion >= 10:

                self.contador_animacion = 0

                if self.frame_animacion == 0:
                    self.jugador.texture = self.textura_caminar1
                    self.frame_animacion = 1

                else:
                    self.jugador.texture = self.textura_caminar2
                    self.frame_animacion = 0

    # Si está quieto
        else:

            self.jugador.texture = self.textura_quieto
        # ==========================================
        # PERSECUCIÓN DEL VILLANO
        # ==========================================

        if self.villano.center_x < self.jugador.center_x:
            self.villano.center_x += self.velocidad_villano

        elif self.villano.center_x > self.jugador.center_x:
            self.villano.center_x -= self.velocidad_villano

        if self.villano.center_y < self.jugador.center_y:
            self.villano.center_y += self.velocidad_villano

        elif self.villano.center_y > self.jugador.center_y:
            self.villano.center_y -= self.velocidad_villano
        
        # ----------------------------------------
        # ¿EL VILLANO ATRAPÓ AL JUGADOR?
        # ----------------------------------------

        if arcade.check_for_collision(self.jugador, self.villano):

            self.jugador_muerto = True

            print("Has sido consumido por la oscuridad.")

            # Reiniciar posiciones
            self.jugador.center_x = self.posicion_inicial_jugador[0]
            self.jugador.center_y = self.posicion_inicial_jugador[1]

            self.villano.center_x = self.posicion_inicial_villano[0]
            self.villano.center_y = self.posicion_inicial_villano[1]

            self.jugador_muerto = False
            self.recuerdos_conseguidos = 0
            self.crear_recuerdos()

        # ==========================================
        # RECOGER RECUERDOS
        # ==========================================

        recuerdos = arcade.check_for_collision_with_list(
            self.jugador,
            self.lista_recuerdos
        )

        for recuerdo in recuerdos:

            recuerdo.remove_from_sprite_lists()

            self.recuerdos_conseguidos += 1

            self.mensaje = "Has recuperado un recuerdo."
            self.tiempo_mensaje = 120
        # ==========================================
        # COMPROBAR SI LLEGÓ A LA SALIDA
        # ==========================================

        if (
            self.salida_x_min <= self.jugador.center_x <= self.salida_x_max
            and self.jugador.center_y >= self.salida_y
        ):

            if self.recuerdos_conseguidos < 3:

                print("Necesito recuperar todos mis recuerdos.")

                # Lo alejamos un poco para que no imprima el mensaje miles de veces
                self.jugador.center_y = self.salida_y - 40

            else:

                self.mostrando_felicitacion = True

                self.velocidad_x = 0
                self.velocidad_y = 0
            # ==========================================
            # CONTADOR DEL MENSAJE
            # ==========================================

        if self.tiempo_mensaje > 0:
            self.tiempo_mensaje -= 1

    def on_key_press(self, key, modifiers):

        if self.mostrando_final:

            if key == arcade.key.ENTER:
                arcade.exit()

            return

        if self.mostrando_felicitacion:

            if key == arcade.key.ENTER:

                self.mostrando_felicitacion = False
                self.mostrando_pregunta = True

            return
        # ==========================================
        # RESPONDER LA PREGUNTA
        # ==========================================

        if self.mostrando_pregunta:

            if key == arcade.key.B:

                self.final_ganado = True
                self.mostrando_pregunta = False
                self.mostrando_final = True

            elif key == arcade.key.A:

                self.final_ganado = False
                self.mostrando_pregunta = False
                self.mostrando_final = True

            return
        
        if self.mostrando_final:

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                configuracion.ALTO,
                (0, 0, 0, 180)
            )

            arcade.draw_lrbt_rectangle_filled(
                180,
                1100,
                140,
                580,
                (35, 35, 35)
            )

            arcade.draw_lrbt_rectangle_outline(
                180,
                1100,
                140,
                580,
                arcade.color.WHITE,
                4
            )

            if self.final_ganado:

                arcade.draw_text(
                    "¡FELICIDADES!",
                    0,
                    470,
                    arcade.color.GOLD,
                    34,
                    bold=True,
                    width=configuracion.ANCHO,
                    align="center"
                )

                arcade.draw_text(
                    "Elegiste la respuesta correcta.\n\n"
                    "Hablar con alguien de confianza\n"
                    "y buscar ayuda puede marcar la diferencia.\n\n"
                    "Has logrado escapar de la oscuridad.",
                    250,
                    270,
                    arcade.color.WHITE,
                    24
                )

            else:

                arcade.draw_text(
                    "FIN DEL JUEGO",
                    0,
                    470,
                    arcade.color.RED,
                    34,
                    bold=True,
                    width=configuracion.ANCHO,
                    align="center"
                )

                arcade.draw_text(
                    "Guardar el sufrimiento para uno mismo\n"
                    "puede hacer que el problema empeore.\n\n"
                    "La oscuridad terminó consumiéndote.",
                    250,
                    290,
                    arcade.color.WHITE,
                    24
                )

            arcade.draw_text(
                "Presiona ENTER para salir",
                0,
                170,
                arcade.color.YELLOW,
                22,
                bold=True,
                width=configuracion.ANCHO,
                align="center"
            )
        
        velocidad = configuracion.VELOCIDAD_JUGADOR

        if key == arcade.key.W:
            self.velocidad_y = velocidad

        elif key == arcade.key.S:
            self.velocidad_y = -velocidad

        elif key == arcade.key.A:
            self.velocidad_x = -velocidad

        elif key == arcade.key.D:
            self.velocidad_x = velocidad

    def on_key_release(self, key, modifiers):

        if key in (arcade.key.W, arcade.key.S):
            self.velocidad_y = 0

        if key in (arcade.key.A, arcade.key.D):
            self.velocidad_x = 0

    def crear_recuerdos(self):

        self.lista_recuerdos = arcade.SpriteList()

        recuerdo1 = arcade.Sprite(
            "imagenes/objetos/recuerdo.png",
            scale=0.10
        )
        recuerdo1.center_x = 250
        recuerdo1.center_y = 500
        self.lista_recuerdos.append(recuerdo1)

        recuerdo2 = arcade.Sprite(
            "imagenes/objetos/recuerdo.png",
            scale=0.10
        )
        recuerdo2.center_x = 700
        recuerdo2.center_y = 300
        self.lista_recuerdos.append(recuerdo2)

        recuerdo3 = arcade.Sprite(
            "imagenes/objetos/recuerdo.png",
            scale=0.10
        )
        recuerdo3.center_x = 1100
        recuerdo3.center_y = 600
        self.lista_recuerdos.append(recuerdo3)

    def reiniciar_nivel(self):

        # Reiniciar jugador
        self.jugador.center_x = self.posicion_inicial_jugador[0]
        self.jugador.center_y = self.posicion_inicial_jugador[1]

        # Reiniciar villano
        self.villano.center_x = self.posicion_inicial_villano[0]
        self.villano.center_y = self.posicion_inicial_villano[1]

        # Reiniciar contador
        self.recuerdos_conseguidos = 0

        # Volver a crear los recuerdos
        self.crear_recuerdos()
