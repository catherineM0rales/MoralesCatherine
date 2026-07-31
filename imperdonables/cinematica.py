import arcade

import configuracion
from camino_rosas import CaminoRosas

# ==========================================
# CONFIGURACIÓN
# ==========================================

VELOCIDAD_TEXTO = 2

# ==========================================
# CLASE CINEMÁTICA
# ==========================================

class Cinematica(arcade.View):

    def __init__(self):

        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)

        self.fuente = "Arial"

        # Escena actual
        self.escena_actual = 0

        # Diálogo actual dentro de la escena
        self.dialogo_actual = 0

        # Máquina de escribir
        self.texto_mostrado = ""
        self.indice_letra = 0
        self.texto_completo = False
        self.contador = 0

        # -----------------------------------
        # ESCENAS
        # -----------------------------------

        self.escenas = [

            {
                "imagen": arcade.load_texture("imagenes/cinematica/escena1.png"),
                "sonido": None,
                "dialogos": [

                    {
                        "personaje": "Narrador",
                        "texto": "En un bosque tranquilo, lleno de vida y color, los niños jugaban felices a las escondidas."
                    },

                    {
                        "personaje": "Narrador",
                        "texto": "Pero aun en un lugar tan lindo como este, no todo es lo que parece."
                    }

                ]
            },

            {
                "imagen": arcade.load_texture("imagenes/cinematica/escena2.png"),
                "sonido": None,
                "dialogos": [

                    {
                        "personaje": "Narrador",
                        "texto": "Todos conocían el bosque y sabían dónde esconderse."
                    },

                    {
                        "personaje": "Narrador",
                        "texto": "Todos... menos nuestro querido protagonista."
                    }

                ]
            },

            {
                "imagen": arcade.load_texture("imagenes/cinematica/escena3.png"),
                "sonido": None,
                "dialogos": [

                    {
                        "personaje": "Chico",
                        "texto": "¿Por qué estás siguiéndome? Ve a esconderte en otro lugar."
                    }

                ]
            },

            {
                "imagen": arcade.load_texture("imagenes/cinematica/escena4.png"),
                "sonido": None,
                "dialogos": [

                    {
                        "personaje": configuracion.NOMBRE_JUGADOR,
                        "texto": "Es que... no sé a dónde ir."
                    },

                    {
                        "personaje": configuracion.NOMBRE_JUGADOR,
                        "texto": "¿Dónde podría esconderme?"
                    }

                ]
            },

            {
                "imagen": arcade.load_texture("imagenes/cinematica/escena5.png"),
                "sonido": None,
                "dialogos": [

                    {
                        "personaje": "Chico",
                        "texto": "No lo sé. Ve a la cueva que está cerca de aquí. Nadie va a encontrarte."
                    }


                ]
            },

            {
                "imagen": arcade.load_texture("imagenes/cinematica/escena4.png"),
                "sonido": None,
                "dialogos": [

                    {
                        "personaje": configuracion.NOMBRE_JUGADOR,
                        "texto": "¿Una cueva?"
                    },

                    {
                        "personaje": configuracion.NOMBRE_JUGADOR,
                        "texto": "Mmm... suena a una buena idea, aunque da un poco de miedo."
                    },

                    {
                        "personaje": configuracion.NOMBRE_JUGADOR,
                        "texto": "Pero iré."
                    }

                ]
            },
            

            {
                "imagen": arcade.load_texture("imagenes/cinematica/escena6.png"),
                "sonido": None,
                "dialogos": []
            },

            {
                "imagen": arcade.load_texture("imagenes/cinematica/escena7.png"),
                "sonido": None,
                "dialogos": []
            },

            {
                "imagen": arcade.load_texture("imagenes/cinematica/escena8.png"),
                "sonido": None,
                "dialogos": [

                    {
                        "personaje": configuracion.NOMBRE_JUGADOR,
                        "texto": "Está... muy oscuro..."
                    }

                ]
            },

            {
                "imagen": arcade.load_texture("imagenes/cinematica/escena9.png"),
                "sonido": None,
                "dialogos": []
            },

            {
                "imagen": arcade.load_texture("imagenes/cinematica/escena10.png"),
                "sonido": None,
                "dialogos": [

                    {
                        "personaje": configuracion.NOMBRE_JUGADOR,
                        "texto": "¡AHH!"
                    }

                ]
            },

            {
                "imagen": arcade.load_texture("imagenes/cinematica/escena11.png"),
                "sonido": None,
                "dialogos": [

                    {
                        "personaje": configuracion.NOMBRE_JUGADOR,
                        "texto": "Ouch..."
                    }

                ]
            },

            {
                "imagen": arcade.load_texture("imagenes/cinematica/escena12.png"),
                "sonido": None,
                "dialogos": [

                    {
                        "personaje": configuracion.NOMBRE_JUGADOR,
                        "texto": "!!!"
                    }

                ]
            },

            {
                "imagen": arcade.load_texture("imagenes/cinematica/escena13.png"),
                "sonido": None,
                "dialogos": [

                    {
                        "personaje": configuracion.NOMBRE_JUGADOR,
                        "texto": "¿Dónde estoy?"
                    }

                ]
            }

        ]

        if self.escenas[0]["sonido"]:
            arcade.play_sound(self.escenas[0]["sonido"])
        # ==========================================
    # ACTUALIZAR LA CINEMÁTICA
    # ==========================================

    # ==========================================
# ACTUALIZAR LA CINEMÁTICA
# ==========================================

    def on_update(self, delta_time):

        escena = self.escenas[self.escena_actual]

    # Si la escena no tiene diálogos, no hay texto que escribir
        if len(escena["dialogos"]) == 0:
            return

        dialogo = escena["dialogos"][self.dialogo_actual]["texto"]

    # Si el texto todavía no terminó de escribirse
        if not self.texto_completo:

            self.contador += 1

            if self.contador >= VELOCIDAD_TEXTO:

                self.contador = 0

                if self.indice_letra < len(dialogo):

                    self.indice_letra += 1
                    self.texto_mostrado = dialogo[:self.indice_letra]

                # Más adelante acá podremos reproducir
                # el sonido de escritura.

                else:

                    self.texto_completo = True
        # ==========================================
    # DIBUJAR
    # ==========================================

    def on_draw(self):

        self.clear()

        escena = self.escenas[self.escena_actual]

        # ------------------------
        # Imagen de fondo
        # ------------------------

        arcade.draw_texture_rect(
            escena["imagen"],
            arcade.LBWH(
                0,
                0,
                configuracion.ANCHO,
                configuracion.ALTO
            )
        )

        # ------------------------
        # Caja del diálogo
        # ------------------------

        if len(escena["dialogos"]) > 0:

            arcade.draw_lrbt_rectangle_filled(
                0,
                configuracion.ANCHO,
                0,
                170,
                (0, 0, 0, 180)
            )

            personaje = escena["dialogos"][self.dialogo_actual]["personaje"]

            arcade.draw_text(
                personaje,
                40,
                130,
                arcade.color.YELLOW,
                24,
                bold=True,
                font_name=self.fuente
            )

            arcade.draw_text(
                self.texto_mostrado,
                40,
                50,
                arcade.color.WHITE,
                22,
                width=configuracion.ANCHO - 80,
                multiline=True,
                font_name=self.fuente
            )

            if self.texto_completo:

                arcade.draw_text(
                    "▶ Haz clic para continuar",
                    configuracion.ANCHO - 250,
                    15,
                    arcade.color.LIGHT_GRAY,
                    18
                )

        else:

            arcade.draw_text(
                "▶ Haz clic para continuar",
                configuracion.ANCHO - 250,
                15,
                arcade.color.WHITE,
                18
            )
        # ==========================================
    # CLIC DEL MOUSE
    # ==========================================

    def on_mouse_press(self, x, y, button, modifiers):

        escena = self.escenas[self.escena_actual]

        # ---------------------------------------
        # Si la escena tiene diálogos
        # ---------------------------------------

        if len(escena["dialogos"]) > 0:

            dialogo = escena["dialogos"][self.dialogo_actual]["texto"]

            # Si el texto todavía se está escribiendo,
            # mostrarlo completo.
            if not self.texto_completo:

                self.texto_mostrado = dialogo
                self.indice_letra = len(dialogo)
                self.texto_completo = True
                return

            # Pasar al siguiente diálogo
            self.dialogo_actual += 1

            # Si todavía quedan diálogos en esta escena
            if self.dialogo_actual < len(escena["dialogos"]):

                self.texto_mostrado = ""
                self.indice_letra = 0
                self.texto_completo = False
                self.contador = 0
                return

        # ---------------------------------------
        # Pasar a la siguiente escena
        # ---------------------------------------

        self.escena_actual += 1
        self.dialogo_actual = 0

        # ¿Terminó la cinemática?
        if self.escena_actual >= len(self.escenas):

            self.window.show_view(CaminoRosas())
            return

        # Reiniciar la máquina de escribir
        self.texto_mostrado = ""
        self.indice_letra = 0
        self.texto_completo = False
        self.contador = 0

        # Reproducir sonido de la nueva escena
        sonido = self.escenas[self.escena_actual]["sonido"]

        if sonido:
            arcade.play_sound(sonido)