import arcade


# ==========================================================
# JUGADOR
# ==========================================================

class Player(arcade.Sprite):

    def __init__(self):

        super().__init__(
            "imagenes/personajes/protagonista/quieto.png",
            scale=0.15
        )

        # Texturas del jugador
        self.tex_quieto = self.texture

        self.tex_caminar1 = arcade.load_texture(
            "imagenes/personajes/protagonista/caminar1.png"
        )

        self.tex_caminar2 = arcade.load_texture(
            "imagenes/personajes/protagonista/caminar2.png"
        )

        # Variables de animación
        self.anim_timer = 0
        self.frame = 0

    def update_animation(self, dx, dy):

        # Si el jugador se está moviendo
        if dx != 0 or dy != 0:

            self.anim_timer += 1

            if self.anim_timer > 10:

                self.anim_timer = 0

                self.frame = 1 - self.frame

                if self.frame == 0:
                    self.texture = self.tex_caminar1
                else:
                    self.texture = self.tex_caminar2

        # Si está quieto
        else:

            self.texture = self.tex_quieto


# ==========================================================
# VILLANO PRINCIPAL
# ==========================================================

class VillanoPrincipal(arcade.Sprite):

    def __init__(self, x, y):

        super().__init__(
            "imagenes/personajes/enemigos/villano.png",
            scale=0.15
        )

        self.center_x = x
        self.center_y = y

        self.velocidad = 2

    def perseguir(self, jugador_x, jugador_y):

        if self.center_x < jugador_x:
            self.center_x += self.velocidad

        elif self.center_x > jugador_x:
            self.center_x -= self.velocidad

        if self.center_y < jugador_y:
            self.center_y += self.velocidad

        elif self.center_y > jugador_y:
            self.center_y -= self.velocidad