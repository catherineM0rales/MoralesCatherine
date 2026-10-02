import arcade
import math


# ============================================================
# JUGADOR
# ============================================================

class Player(arcade.Sprite):

    def __init__(self):

        super().__init__(
            "imagenes/personajes/protagonista/quieto.png",
            scale=0.15
        )

        # ========================================================
        # TEXTURAS DEL JUGADOR
        # ========================================================

        self.tex_quieto = self.texture

        self.tex_caminar1 = arcade.load_texture(
            "imagenes/personajes/protagonista/caminar1.png"
        )

        self.tex_caminar2 = arcade.load_texture(
            "imagenes/personajes/protagonista/caminar2.png"
        )

        # ========================================================
        # ANIMACIÓN
        # ========================================================

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


# ============================================================
# VILLANO PERSEGUIDOR
# ============================================================

class VillanoPerseguidor(arcade.Sprite):

    def __init__(
        self,
        x,
        y,
        imagen,
        velocidad=2,
        rango_vision=900,
        espera_disparo=1.0
    ):

        super().__init__(
            imagen,
            scale=0.12
        )

        self.center_x = x
        self.center_y = y

        # ========================================================
        # MOVIMIENTO
        # ========================================================

        self.velocidad = velocidad

        # ========================================================
        # VISIÓN
        # ========================================================

        self.rango_vision = rango_vision

        # ========================================================
        # DISPARO
        # ========================================================

        self.tiempo_disparo = 0
        self.espera_disparo = espera_disparo
        self.contador_ataques = 0

        # ========================================================
        # ESTADO
        # ========================================================

        # IMPORTANTE:
        # Ahora el villano está activo desde que aparece.
        self.activo = True

        # ========================================================
        # COLISIÓN
        # ========================================================

        self.radio_colision = 10

    # ============================================================
    # CALCULAR DISTANCIA
    # ============================================================

    def calcular_distancia(self, jugador):

        dx = jugador.center_x - self.center_x
        dy = jugador.center_y - self.center_y

        return math.sqrt(
            dx * dx +
            dy * dy
        )

    # ============================================================
    # ¿PUEDE VER AL JUGADOR?
    # ============================================================

    def puede_ver_jugador(
        self,
        jugador,
        paredes=None
    ):

        distancia = self.calcular_distancia(
            jugador
        )

        # Está demasiado lejos
        if distancia > self.rango_vision:

            return False

        # Si no hay paredes, lo ve directamente
        if paredes is None:

            return True

        # ========================================================
        # COMPROBAR SI UNA PARED BLOQUEA LA VISIÓN
        # ========================================================

        pasos = max(
            1,
            int(distancia / 10)
        )

        for i in range(1, pasos + 1):

            porcentaje = i / pasos

            x = (
                self.center_x
                + (
                    jugador.center_x
                    - self.center_x
                ) * porcentaje
            )

            y = (
                self.center_y
                + (
                    jugador.center_y
                    - self.center_y
                ) * porcentaje
            )

            if self.choca_con_paredes(
                x,
                y,
                paredes
            ):

                return False

        return True

    # ============================================================
    # COLISIÓN CON PAREDES
    # ============================================================

    def choca_con_paredes(
        self,
        x,
        y,
        paredes
    ):

        radio = self.radio_colision

        for pared in paredes:

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

            punto_x = max(
                izquierda,
                min(x, derecha)
            )

            punto_y = max(
                abajo,
                min(y, arriba)
            )

            distancia_x = x - punto_x
            distancia_y = y - punto_y

            if (
                distancia_x * distancia_x
                + distancia_y * distancia_y
                < radio * radio
            ):

                return True

        return False

    # ============================================================
    # POSICIÓN LIBRE
    # ============================================================

    def posicion_libre(
        self,
        x,
        y,
        paredes,
        ancho_mapa=1536,
        alto_mapa=1024
    ):

        if x < 40:
            return False

        if x > ancho_mapa - 40:
            return False

        if y < 40:
            return False

        if y > alto_mapa - 40:
            return False

        return not self.choca_con_paredes(
            x,
            y,
            paredes
        )

    # ============================================================
    # PERSEGUIR AL JUGADOR
    # ============================================================

    def intentar_movimiento(
        self,
        jugador,
        paredes=None,
        ancho_mapa=1536,
        alto_mapa=1024
    ):

        dx = jugador.center_x - self.center_x
        dy = jugador.center_y - self.center_y

        distancia = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distancia <= 1:

            return

        # ========================================================
        # DIRECCIÓN NORMALIZADA
        # ========================================================

        dir_x = dx / distancia
        dir_y = dy / distancia

        # ========================================================
        # SI NO HAY PAREDES
        # ========================================================

        if paredes is None:

            nuevo_x = (
                self.center_x
                + dir_x * self.velocidad
            )

            nuevo_y = (
                self.center_y
                + dir_y * self.velocidad
            )

            self.center_x = nuevo_x
            self.center_y = nuevo_y

            return

        # ========================================================
        # DIRECCIONES PARA RODEAR PAREDES
        # ========================================================

        angulos = [
            0,
            -15, 15,
            -30, 30,
            -45, 45,
            -60, 60,
            -75, 75,
            -90, 90,
            -120, 120,
            -150, 150,
            180
        ]

        candidatos = []

        for angulo in angulos:

            radianes = math.radians(
                angulo
            )

            nuevo_x_dir = (
                dir_x * math.cos(radianes)
                - dir_y * math.sin(radianes)
            )

            nuevo_y_dir = (
                dir_x * math.sin(radianes)
                + dir_y * math.cos(radianes)
            )

            nuevo_x = (
                self.center_x
                + nuevo_x_dir * self.velocidad
            )

            nuevo_y = (
                self.center_y
                + nuevo_y_dir * self.velocidad
            )

            # ====================================================
            # ¿ESTÁ LIBRE?
            # ====================================================

            if self.posicion_libre(
                nuevo_x,
                nuevo_y,
                paredes,
                ancho_mapa,
                alto_mapa
            ):

                distancia_nueva = math.sqrt(
                    (
                        jugador.center_x
                        - nuevo_x
                    ) ** 2
                    +
                    (
                        jugador.center_y
                        - nuevo_y
                    ) ** 2
                )

                penalizacion = (
                    abs(angulo) * 0.15
                )

                puntuacion = (
                    distancia_nueva
                    + penalizacion
                )

                candidatos.append(
                    (
                        puntuacion,
                        nuevo_x,
                        nuevo_y
                    )
                )

        # ========================================================
        # ELEGIR EL MEJOR MOVIMIENTO
        # ========================================================

        if candidatos:

            candidatos.sort(
                key=lambda candidato: candidato[0]
            )

            _, mejor_x, mejor_y = candidatos[0]

            self.center_x = mejor_x
            self.center_y = mejor_y

    # ============================================================
    # ACTUALIZAR VILLANO
    # ============================================================

    def actualizar(
        self,
        jugador,
        paredes=None,
        delta_time=1 / 60,
        ancho_mapa=1536,
        alto_mapa=1024
    ):

        # Si por algún motivo está desactivado,
        # no se mueve.
        if not self.activo:

            return

        # ========================================================
        # PERSEGUIR
        # ========================================================

        self.intentar_movimiento(
            jugador,
            paredes,
            ancho_mapa,
            alto_mapa
        )

        # ========================================================
        # TIEMPO DE DISPARO
        # ========================================================

        self.tiempo_disparo += delta_time

    # ============================================================
    # ¿PUEDE DISPARAR?
    # ============================================================

    def puede_disparar(self):

        if (
            self.tiempo_disparo
            >= self.espera_disparo
        ):

            self.tiempo_disparo = 0

            self.contador_ataques += 1

            return True

        return False


# ============================================================
# VILLANO PRINCIPAL
# ============================================================

class VillanoPrincipal(VillanoPerseguidor):

    def __init__(
        self,
        x,
        y,
        imagen="imagenes/personajes/enemigos/villano.png",
        velocidad=1.35,
        rango_vision=2000,
        espera_disparo=1.15
    ):

        super().__init__(
            x,
            y,
            imagen,
            velocidad=velocidad,
            rango_vision=rango_vision,
            espera_disparo=espera_disparo
        )

        self.vida_maxima = 5
        self.vida = self.vida_maxima

        # IMPORTANTE:
        # También queda activo explícitamente.
        self.activo = True


# ============================================================
# RECUERDO
# ============================================================

class Recuerdo(arcade.Sprite):

    def __init__(
        self,
        x,
        y
    ):

        super().__init__(
            "imagenes/objetos/recuerdo.png",
            scale=0.10
        )

        self.center_x = x
        self.center_y = y


# ============================================================
# PROYECTIL
# ============================================================

class Proyectil(arcade.SpriteSolidColor):

    def __init__(
        self,
        x,
        y,
        objetivo_x,
        objetivo_y
    ):

        super().__init__(
            width=18,
            height=18,
            color=(150, 90, 220)
        )

        self.center_x = x
        self.center_y = y

        self.velocidad = 4.5

        dx = objetivo_x - x
        dy = objetivo_y - y

        distancia = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distancia == 0:

            self.dx = 0
            self.dy = 0

        else:

            self.dx = dx / distancia
            self.dy = dy / distancia

    def mover(self):

        self.center_x += (
            self.dx * self.velocidad
        )

        self.center_y += (
            self.dy * self.velocidad
        )