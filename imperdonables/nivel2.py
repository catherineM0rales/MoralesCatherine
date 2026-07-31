import arcade
import random
import configuracion

# --- CALIBRACIÓN DE PAREDES ---
OFFSET_X = 0.1
OFFSET_Y = 65.0  


def obtener_caja_objeto(obj, alto_mapa_px):
    if hasattr(obj, "shape") and isinstance(obj.shape, (list, tuple)) and len(obj.shape) > 0:
        s = obj.shape
        if isinstance(s[0], (list, tuple)):
            xs = [p[0] for p in s]
            ys = [p[1] for p in s]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            w = max_x - min_x
            h = max_y - min_y
            
            center_x = (min_x + (w / 2.0)) + OFFSET_X
            center_y_tiled = min_y + (h / 2.0)
            center_y = (alto_mapa_px - center_y_tiled) - OFFSET_Y
            return center_x, center_y, w, h

    x = float(getattr(obj, "x", 0.0))
    y = float(getattr(obj, "y", 0.0))
    w = float(getattr(obj, "width", 32.0))
    h = float(getattr(obj, "height", 32.0))
    
    center_x = (x + (w / 2.0)) + OFFSET_X
    center_y = (alto_mapa_px - y - (h / 2.0)) - OFFSET_Y
    return center_x, center_y, w, h


class Nivel2(arcade.View):
    def __init__(self):
        super().__init__()

        # --- 1. CARGA DEL MAPA TILED ---
        nombre_mapa = "imagenes/mapas/laberinto.tmx"
        self.tile_map = arcade.load_tilemap(nombre_mapa, scaling=1.0)
        
        ancho_mapa_px = float(self.tile_map.width * self.tile_map.tile_width)
        alto_mapa_px = float(self.tile_map.height * self.tile_map.tile_height)
        
        self.escala_x = configuracion.ANCHO / ancho_mapa_px if ancho_mapa_px > 0 else 1.0
        self.escala_y = configuracion.ALTO / alto_mapa_px if alto_mapa_px > 0 else 1.0

        self.lista_paredes = arcade.SpriteList()
        
        objetos_tiled = self.tile_map.object_lists.get("Paredes", [])
        
        for obj in objetos_tiled:
            center_x_raw, center_y_raw, ancho_raw, alto_raw = obtener_caja_objeto(obj, alto_mapa_px)

            if ancho_raw <= 0: ancho_raw = 32.0
            if alto_raw <= 0: alto_raw = 32.0

            center_x = center_x_raw * self.escala_x
            center_y = center_y_raw * self.escala_y
            ancho_final = max(2, int(ancho_raw * self.escala_x))
            alto_final = max(2, int(alto_raw * self.escala_y))

            pared = arcade.SpriteSolidColor(ancho_final, alto_final, color=(255, 0, 0, 140))
            pared.center_x = center_x
            pared.center_y = center_y
            
            self.lista_paredes.append(pared)

        self.fondo_laberinto = arcade.load_texture("imagenes/mapas/laberinto.png")

        # --- 2. JUGADOR ---
        self.jugador_sprite = arcade.Sprite("imagenes/personajes/protagonista/quieto.png", scale=0.2)
        self.jugador_sprite.center_x = configuracion.ANCHO * 0.12
        self.jugador_sprite.center_y = configuracion.ALTO * 0.48

        self.lista_jugador = arcade.SpriteList()
        self.lista_jugador.append(self.jugador_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(self.jugador_sprite, self.lista_paredes)

        # Animaciones
        self.textura_quieto = arcade.load_texture("imagenes/personajes/protagonista/quieto.png")
        self.textura_caminar1 = arcade.load_texture("imagenes/personajes/protagonista/caminar1.png")
        self.textura_caminar2 = arcade.load_texture("imagenes/personajes/protagonista/caminar2.png")
        
        self.tiempo_animacion = 0
        self.velocidad = 3.2
        self.cambio_x = 0
        self.cambio_y = 0

        # --- 3. ENEMIGO Y DIBUJOS ---
        self.villano_sprite = arcade.Sprite("imagenes/personajes/enemigos/enemigo1.png", scale=0.2)
        self.villano_sprite.center_x = configuracion.ANCHO * 0.73
        self.villano_sprite.center_y = configuracion.ALTO * 0.72
        
        self.lista_enemigos = arcade.SpriteList()
        self.lista_enemigos.append(self.villano_sprite)

        self.lista_fragmentos = arcade.SpriteList()
        posiciones_fragmentos = [
            (configuracion.ANCHO * 0.34, configuracion.ALTO * 0.70),
            (configuracion.ANCHO * 0.34, configuracion.ALTO * 0.28),
            (configuracion.ANCHO * 0.58, configuracion.ALTO * 0.52),
            (configuracion.ANCHO * 0.56, configuracion.ALTO * 0.22),
        ]
        
        for pos_x, pos_y in posiciones_fragmentos:
            fragmento = arcade.Sprite("imagenes/objetos/dibujo.png", scale=0.2)
            fragmento.center_x = pos_x
            fragmento.center_y = pos_y
            self.lista_fragmentos.append(fragmento)

        self.salida_x = configuracion.ANCHO * 0.88
        self.salida_y = configuracion.ALTO * 0.20

        # --- 4. SISTEMA DE DIÁLOGOS Y ESTADOS ---
        self.estado = "INTRO_DIALOGO"
        self.opacidad_penumbra = 0
        self.tiempo_estado = 0
        self.shake_amount = 0.0

        self.cordura_max = 100.0
        self.cordura_actual = 100.0
        self.drenaje_cordura = 1.6

        self.dialogos_villano = [
            "Inseguridad: «¿Crees que puedes escapar juntando esos papeles?»",
            "Inseguridad: «Cada paso que das, la duda te consumirá más rápido...»",
            "Inseguridad: «No tienes lo necesario para salir de esta cueva.»"
        ]
        self.indice_dialogo = 0
        self.hablando_con_villano = False

        self.susurros = [
            "«¿Estás seguro de que este es el camino?»",
            "«Te vas a volver a equivocar...»",
            "«Inseguridad te acecha desde la penumbra...»",
            "«Nunca vas a juntar el dibujo completo.»"
        ]
        self.susurro_actual = ""
        self.timer_susurro = 0
        self.duracion_susurro = 0

        self.texto_titulo_hud = arcade.Text(
            "ESTABILIDAD MENTAL", 30, configuracion.ALTO - 45,
            arcade.color.WHITE, 10, bold=True
        )
        self.texto_restantes_hud = arcade.Text(
            f"Dibujos restantes: {len(self.lista_fragmentos)}", configuracion.ANCHO - 180, configuracion.ALTO - 35,
            arcade.color.GOLD, 11, bold=True
        )
        self.texto_dialogo = arcade.Text(
            "", configuracion.ANCHO / 2, 50,
            arcade.color.WHITE, 13, anchor_x="center"
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_update(self, delta_time: float):
        self.tiempo_estado += delta_time

        if self.shake_amount > 0:
            self.shake_amount = max(0.0, self.shake_amount - delta_time * 15.0)

        if self.estado == "INTRO_DIALOGO":
            if self.tiempo_estado > 3.0:
                self.estado = "APAGANDO"

        elif self.estado == "APAGANDO":
            if self.opacidad_penumbra < 190:
                self.opacidad_penumbra += 65 * delta_time
            else:
                self.opacidad_penumbra = 190
                self.estado = "JUGANDO"

        if self.estado in ("JUGANDO", "INTRO_DIALOGO", "APAGANDO") and not self.hablando_con_villano:
            self.jugador_sprite.change_x = self.cambio_x
            self.jugador_sprite.change_y = self.cambio_y

            self.physics_engine.update()

            if self.cambio_x != 0 or self.cambio_y != 0:
                self.tiempo_animacion += delta_time
                if int(self.tiempo_animacion * 6) % 2 == 0:
                    self.jugador_sprite.texture = self.textura_caminar1
                else:
                    self.jugador_sprite.texture = self.textura_caminar2
            else:
                # CORREGIDO: Se cambió 'textura_quiet' por 'textura_quieto'
                self.jugador_sprite.texture = self.textura_quieto
                self.tiempo_animacion = 0
        else:
            self.jugador_sprite.change_x = 0
            self.jugador_sprite.change_y = 0

        if self.estado == "JUGANDO":
            if not self.hablando_con_villano:
                self.cordura_actual -= self.drenaje_cordura * delta_time
                if self.cordura_actual <= 0:
                    self.cordura_actual = 0
                    self.estado = "COLAPSO"

            self.timer_susurro += delta_time
            if self.timer_susurro > random.uniform(6, 9):
                self.susurro_actual = random.choice(self.susurros)
                self.duracion_susurro = 3.0
                self.timer_susurro = 0
                self.cordura_actual -= 3

            if self.duracion_susurro > 0:
                self.duracion_susurro -= delta_time

            colisiones = arcade.check_for_collision_with_list(self.jugador_sprite, self.lista_fragmentos)
            for frag in colisiones:
                frag.remove_from_sprite_lists()
                self.cordura_actual = min(self.cordura_max, self.cordura_actual + 30)

            dist_salida = ((self.jugador_sprite.center_x - self.salida_x)**2 + 
                           (self.jugador_sprite.center_y - self.salida_y)**2)**0.5
            
            if dist_salida < 45 and len(self.lista_fragmentos) == 0:
                self.estado = "VICTORIA"

        self.texto_restantes_hud.text = f"Dibujos restantes: {len(self.lista_fragmentos)}"

    def on_draw(self):
        self.clear()

        offset_x = random.uniform(-self.shake_amount, self.shake_amount) if self.shake_amount > 0 else 0
        offset_y = random.uniform(-self.shake_amount, self.shake_amount) if self.shake_amount > 0 else 0

        arcade.draw_texture_rect(
            self.fondo_laberinto,
            arcade.LBWH(offset_x, offset_y, configuracion.ANCHO, configuracion.ALTO)
        )

        self.lista_paredes.draw()
        self.lista_enemigos.draw()
        self.lista_fragmentos.draw()
        self.lista_jugador.draw()

        if self.opacidad_penumbra > 0:
            arcade.draw_rect_filled(
                arcade.XYWH(configuracion.ANCHO / 2, configuracion.ALTO / 2, configuracion.ANCHO, configuracion.ALTO),
                color=(8, 10, 24, int(self.opacidad_penumbra))
            )

        self.dibujar_hud()

    def dibujar_hud(self):
        arcade.draw_rect_filled(
            arcade.XYWH(130, configuracion.ALTO - 25, 204, 20),
            color=arcade.color.DARK_GRAY
        )
        
        ancho_barra = max(0, (self.cordura_actual / self.cordura_max) * 200)
        color_barra = arcade.color.CORNFLOWER_BLUE if self.cordura_actual > 30 else arcade.color.CRIMSON

        arcade.draw_rect_filled(
            arcade.XYWH(30 + ancho_barra / 2, configuracion.ALTO - 25, ancho_barra, 16),
            color=color_barra
        )

        self.texto_titulo_hud.draw()
        self.texto_restantes_hud.draw()

        distancia_villano = arcade.get_distance_between_sprites(self.jugador_sprite, self.villano_sprite)

        if self.estado in ("INTRO_DIALOGO", "APAGANDO"):
            self.texto_dialogo.text = "Inseguridad: «Sientes que me ves... pero no puedes escapar de esta cueva.»"
            self.texto_dialogo.color = arcade.color.MEDIUM_PURPLE
            self.texto_dialogo.bold = True
            self.texto_dialogo.draw()

        elif self.hablando_con_villano:
            self.texto_dialogo.text = self.dialogos_villano[self.indice_dialogo] + "  [Presioná ESPACIO para avanzar]"
            self.texto_dialogo.color = arcade.color.LIGHT_RED_ORCHID
            self.texto_dialogo.bold = True
            self.texto_dialogo.draw()

        elif distancia_villano < 80 and self.estado == "JUGANDO":
            self.texto_dialogo.text = "Presioná [ESPACIO] para hablar con Inseguridad"
            self.texto_dialogo.color = arcade.color.GOLD
            self.texto_dialogo.bold = True
            self.texto_dialogo.draw()

        elif self.estado == "COLAPSO":
            self.texto_dialogo.text = "Inseguridad te ha consumido por completo... (Game Over)"
            self.texto_dialogo.color = arcade.color.DARK_RED
            self.texto_dialogo.bold = True
            self.texto_dialogo.draw()

        elif self.duracion_susurro > 0 and self.estado == "JUGANDO":
            self.texto_dialogo.text = self.susurro_actual
            self.texto_dialogo.color = arcade.color.LIGHT_GRAY
            self.texto_dialogo.bold = False
            self.texto_dialogo.draw()

        elif self.estado == "VICTORIA":
            self.texto_dialogo.text = "¡Juntaste todos los recuerdos y venciste tu Inseguridad!"
            self.texto_dialogo.color = arcade.color.PASTEL_GREEN
            self.texto_dialogo.bold = True
            self.texto_dialogo.draw()

    def on_key_press(self, key, modifiers):
        if self.estado == "COLAPSO":
            return

        if key == arcade.key.SPACE and self.estado == "JUGANDO":
            distancia_villano = arcade.get_distance_between_sprites(self.jugador_sprite, self.villano_sprite)
            if distancia_villano < 80:
                if not self.hablando_con_villano:
                    self.hablando_con_villano = True
                    self.indice_dialogo = 0
                else:
                    self.indice_dialogo += 1
                    if self.indice_dialogo >= len(self.dialogos_villano):
                        self.hablando_con_villano = False
                        self.indice_dialogo = 0

        if not self.hablando_con_villano:
            if key in (arcade.key.UP, arcade.key.W):
                self.cambio_y = self.velocidad
            elif key in (arcade.key.DOWN, arcade.key.S):
                self.cambio_y = -self.velocidad
            elif key in (arcade.key.LEFT, arcade.key.A):
                self.cambio_x = -self.velocidad
            elif key in (arcade.key.RIGHT, arcade.key.D):
                self.cambio_x = self.velocidad

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.W, arcade.key.DOWN, arcade.key.S):
            self.cambio_y = 0
        elif key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.cambio_x = 0