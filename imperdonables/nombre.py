import arcade
import configuracion
from cinematica import Cinematica

class PantallaNombre(arcade.View):

    def __init__(self):
        super().__init__()

        self.nombre = ""

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "¿Cómo te llamás?",
            configuracion.ANCHO / 2,
            500,
            arcade.color.WHITE,
            32,
            anchor_x="center"
        )

        arcade.draw_text(
            self.nombre + "_",
            configuracion.ANCHO / 2,
            400,
            arcade.color.YELLOW,
            28,
            anchor_x="center"
        )

        arcade.draw_text(
            "Presioná ENTER para continuar",
            configuracion.ANCHO / 2,
            250,
            arcade.color.GRAY,
            18,
            anchor_x="center"
        )

    def on_text(self, texto):
        if len(self.nombre) < 15:
            self.nombre += texto

    def on_key_press(self, key, modifiers):

        if key == arcade.key.BACKSPACE:
            self.nombre = self.nombre[:-1]

        elif key == arcade.key.ENTER:

            if self.nombre.strip() != "":

                configuracion.NOMBRE_JUGADOR = self.nombre

                self.window.show_view(Cinematica())

                # Acá luego irá la cinemática