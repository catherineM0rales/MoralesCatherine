import arcade
import configuracion
from nivel1 import Nivel1

class CaminoRosas(arcade.View):
    def __init__(self):
        super().__init__()
        
        # 1. Cargar Fondo
        self.fondo = arcade.load_texture("imagenes/mapas/camino.png")
        
        # 2. Cargar Texturas del Protagonista
        self.textura_quieto = arcade.load_texture("imagenes/personajes/protagonista/quieto.png")
        self.textura_caminar1 = arcade.load_texture("imagenes/personajes/protagonista/caminar1.png")
        self.textura_caminar2 = arcade.load_texture("imagenes/personajes/protagonista/caminar2.png")

        # Sprite del Jugador
        self.jugador_sprite = arcade.Sprite(self.textura_quieto, scale=0.2)

        # Sprite del Papel / Dibujo (provisional si no tenés imagen)
        try:
            self.papel_sprite = arcade.Sprite("imagenes/objetos/dibujo.png", scale=0.10)
        except Exception:
            self.papel_sprite = None

        # Posición del jugador (Empieza a la izquierda)
        self.jugador_x = 60
        self.jugador_y = configuracion.ALTO // 2
        self.velocidad = 3.5

        # Control de Animación
        self.contador_animacion = 0
        self.frame_animacion = 0

        # Control de teclas
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Sistema de Bucle de Camino (Tramo 1 y Tramo 2)
        self.tramo_actual = 1
        self.dibujo_encontrado = False
        self.leyendo_nota = False

        # Límites del camino (Paredes invisibles)
        self.limite_arriba = configuracion.ALTO // 2 + 60
        self.limite_abajo = configuracion.ALTO // 2 - 60

    def on_draw(self):
        self.clear()
        
        # Dibujar Fondo
        arcade.draw_texture_rect(
            self.fondo,
            arcade.LBWH(0, 0, configuracion.ANCHO, configuracion.ALTO)
        )

        # Dibujar el Dibujo/Papel SOLO en el Tramo 2 si no se recogió
        if self.tramo_actual == 2 and not self.dibujo_encontrado:
            pos_papel_x = configuracion.ANCHO // 2 + 100
            pos_papel_y = configuracion.ALTO // 2
            
            if self.papel_sprite:
                self.papel_sprite.center_x = pos_papel_x
                self.papel_sprite.center_y = pos_papel_y
                arcade.draw_sprite(self.papel_sprite)
            else:
                arcade.draw_rect_filled(
                    arcade.XYWH(pos_papel_x, pos_papel_y, 25, 25),
                    arcade.color.WHITE
                )

        # Dibujar Jugador (Forma compatible con Arcade 3.0+)
        self.jugador_sprite.center_x = self.jugador_x
        self.jugador_sprite.center_y = self.jugador_y
        arcade.draw_sprite(self.jugador_sprite)

        # Cuadro de Texto de la historia
        if self.leyendo_nota:
            # Caja de fondo oscura para el diálogo
            arcade.draw_rect_filled(
                arcade.XYWH(configuracion.ANCHO // 2, 85, configuracion.ANCHO, 170),
                (0, 0, 0, 200)
            )
            arcade.draw_text(
                "Encontraste un fragmento de un dibujo...",
                40, 130, arcade.color.YELLOW, 20, bold=True
            )
            arcade.draw_text(
                "\"De cuando no tenía miedo a equivocarme.\"",
                40, 50, arcade.color.WHITE, 18, width=configuracion.ANCHO - 80, multiline=True
            )
            arcade.draw_text(
                "▶ Presiona ESPACIO para continuar",
                configuracion.ANCHO - 300, 15, arcade.color.LIGHT_GRAY, 14
            )

    def on_update(self, delta_time):
        if self.leyendo_nota:
            self.jugador_sprite.texture = self.textura_quieto
            return

        # 1. Movimiento y animación
        se_mueve = False

        if self.left_pressed:
            self.jugador_x -= self.velocidad
            se_mueve = True
        if self.right_pressed:
            self.jugador_x += self.velocidad
            se_mueve = True
        if self.up_pressed:
            self.jugador_y += self.velocidad
            se_mueve = True
        if self.down_pressed:
            self.jugador_y -= self.velocidad
            se_mueve = True

        # Lógica de animación paso a paso
        if se_mueve:
            self.contador_animacion += 1
            if self.contador_animacion >= 10:  # Cambia de paso cada 10 frames
                self.contador_animacion = 0
                self.frame_animacion = 1 - self.frame_animacion  # Alterna entre 0 y 1
                
                if self.frame_animacion == 0:
                    self.jugador_sprite.texture = self.textura_caminar1
                else:
                    self.jugador_sprite.texture = self.textura_caminar2
        else:
            self.jugador_sprite.texture = self.textura_quieto

        # 2. Paredes / Límites del mapa
        self.jugador_y = max(self.limite_abajo, min(self.jugador_y, self.limite_arriba))
        self.jugador_x = max(30, self.jugador_x)

        # 3. Lógica del Bucle del Camino
        if self.jugador_x >= configuracion.ANCHO - 30 and self.tramo_actual == 1:
            self.tramo_actual = 2
            self.jugador_x = 40  # Vuelve a la izquierda para simular el avance continuo

        # Detectar interacción con el dibujo en el Tramo 2
        if self.tramo_actual == 2 and not self.dibujo_encontrado:
            pos_papel_x = configuracion.ANCHO // 2 + 100
            if abs(self.jugador_x - pos_papel_x) < 35 and abs(self.jugador_y - (configuracion.ALTO // 2)) < 35:
                self.dibujo_encontrado = True
                self.leyendo_nota = True

        # 4. Salida al Nivel 1
        if self.jugador_x >= configuracion.ANCHO - 30 and self.tramo_actual == 2 and self.dibujo_encontrado:
            self.window.show_view(Nivel1())

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and self.leyendo_nota:
            self.leyendo_nota = False

        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True
        elif key in (arcade.key.UP, arcade.key.W):
            self.up_pressed = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = True

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False
        elif key in (arcade.key.UP, arcade.key.W):
            self.up_pressed = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = False