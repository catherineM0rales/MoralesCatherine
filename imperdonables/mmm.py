import arcade

ANCHO = 800
ALTO = 600
TITULO = "Imperdonables"


class MenuView(arcade.View):

    def __init__(self):
        super().__init__()

        # Fondo del menú
        self.fondo = arcade.load_texture(
            "sprites/menufondo.png"
        )

        # Logo del juego
        self.logo = arcade.load_texture(
            "sprites/logofinal_menu.png"
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

        # Dibujar fondo
        arcade.draw_lrwh_rectangle_textured(
            0,
            0,
            ANCHO,
            ALTO,
            self.fondo
        )

        # Dibujar logo
        arcade.draw_lrwh_rectangle_textured(
            100,   # posición X
            330,   # posición Y
            600,   # ancho
            200,   # alto
            self.logo
        )

        # Opciones del menú
        arcade.draw_text(
            "Presiona ENTER para jugar",
            100,
            200,
            arcade.color.WHITE,
            24
        )