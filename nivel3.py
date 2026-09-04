import arcade
import math
import random
import configuracion


class Nivel3(arcade.View):
    def __init__(self):
        super().__init__()

        # ---- Cámaras ----
        self.camera_sprites = arcade.Camera2D()
        self.camera_gui = arcade.Camera2D()

        # ---- Fondo del laberinto ----
        self.fondo = arcade.load_texture("imagenes/mapas/laberinto.png")

        # ---- Jugador ----
        self.jugador = arcade.Sprite("imagenes/personajes/protagonista/quieto.png", scale=0.15)
        self.lista_jugadores = arcade.SpriteList()
        self.lista_jugadores.append(self.jugador)

        self.textura_quieto = arcade.load_texture("imagenes/personajes/protagonista/quieto.png")
        self.textura_caminar1 = arcade.load_texture("imagenes/personajes/protagonista/caminar1.png")
        self.textura_caminar2 = arcade.load_texture("imagenes/personajes/protagonista/caminar2.png")
        self.jugador.texture = self.textura_quieto

        self.anim_timer = 0
        self.frame_animacion = 0
        self.posicion_inicial = (100, 360)
        self.jugador.center_x, self.jugador.center_y = self.posicion_inicial

        self.teclas = set()

        # ---- Enemigo patrullando diagonal ----
        self.enemigo = arcade.Sprite("imagenes/personajes/enemigos/enemigo1.png", scale=0.12)
        self.enemigo.center_x, self.enemigo.center_y = 800, 450
        self.lista_enemigos = arcade.SpriteList()
        self.lista_enemigos.append(self.enemigo)
        self.enemigo_dx = 1.5
        self.enemigo_dy = 1.0

        # ---- Puzzle: 5 fragmentos recogidos EN ORDEN ----
        self.siguiente_fragmento = 1
        self.total_fragmentos = 5
        self.fragmentos_recogidos = 0

        self.lista_fragmentos = arcade.SpriteList()
        self.datos_fragmentos = []

        posiciones = [
            (300, 550),    # Fragmento 1 - arriba izquierda
            (1050, 600),   # Fragmento 2 - arriba derecha
            (1100, 150),   # Fragmento 3 - abajo derecha
            (300, 150),    # Fragmento 4 - abajo izquierda
            (640, 360),    # Fragmento 5 - centro del mapa
        ]

        self.mensajes_fragmentos = [
            "1/5 — \"Recuerdo cuando todo era más simple...\"",
            "2/5 — \"Aprendí que pedir ayuda no es debilidad.\"",
            "3/5 — \"Cada paso cuenta, aunque sea pequeño.\"",
            "4/5 — \"No estoy solo en esto.\"",
            "5/5 — \"Soy más fuerte de lo que creía.\""
        ]

        for i, (px, py) in enumerate(posiciones):
            frag = arcade.Sprite("imagenes/objetos/recuerdo.png", scale=0.10)
            frag.center_x, frag.center_y = px, py
            frag.base_y = py
            frag.numero = i + 1
            self.lista_fragmentos.append(frag)
            self.datos_fragmentos.append(frag)

        # ---- Variables de estado ----
        self.tiempo_global = 0.0
        self.mensaje = ""
        self.tiempo_mensaje = 0.0
        self.shake_timer = 0.0

        # ---- Partículas ----
        self.particulas = []

        # ---- Estado del nivel ----
        self.fase = "instrucciones"   # instrucciones → jugando → final
        self.mostrando_final = False

        # ---- Fade in al entrar al nivel ----
        self.fade_alpha = 255.0   # Empieza negro, va bajando
        self.fade_velocidad = 180.0

        # ---- Paredes invisibles ----
        self.paredes = arcade.SpriteList()
        self.setup_paredes()

        self.physics_engine = arcade.PhysicsEngineSimple(self.jugador, self.paredes)

    # ----------------------------------------------------------
    def on_show_view(self):
        configuracion.reproducir_musica("audios/nivel3_misterio.mp3", 0.5)

    # ----------------------------------------------------------
    def setup_paredes(self):
        color_t = (0, 0, 0, 0)

        # Perímetro del mapa
        p = arcade.SpriteSolidColor(20, configuracion.ALTO, color_t)
        p.center_x, p.center_y = 10, configuracion.ALTO // 2
        self.paredes.append(p)

        p = arcade.SpriteSolidColor(20, configuracion.ALTO, color_t)
        p.center_x, p.center_y = configuracion.ANCHO - 10, configuracion.ALTO // 2
        self.paredes.append(p)

        p = arcade.SpriteSolidColor(configuracion.ANCHO, 20, color_t)
        p.center_x, p.center_y = configuracion.ANCHO // 2, 10
        self.paredes.append(p)

        # Obstáculos precisos del mapa TMX (convertidos a coordenadas Arcade)
        # TMX: Y-down 1216x896 → Arcade: Y-up 1200x800, con offset grupo (-139.4 en Y)
        obstaculos = [
            (  713.3, 762.3, 853.3,  26.1), (  141.1, 592.3, 254.5, 299.5),
            (  412.5, 658.1, 154.9,  45.9), (  673.3, 622.4,  56.1, 117.9),
            (  770.6, 595.7, 127.7,  41.9), (  806.3, 667.5,  50.7, 103.9),
            (  912.9, 589.3,  31.8, 171.5), ( 1015.9, 651.3, 149.5,  31.8),
            (  361.8, 475.3,  29.9, 313.9), (  690.8, 233.2,  29.9, 202.9),
            (  820.9, 229.1, 200.4,  27.1), (  909.1, 350.9,  29.9, 167.7),
            ( 1006.3, 398.2, 164.5,  46.0), ( 1058.6, 357.6,  59.8,  35.2),
            ( 1066.1, 547.0,  44.9, 132.6), ( 1021.2, 503.7,  32.9,  51.4),
            (  850.8, 491.6, 212.3,  27.1), (  807.4, 394.2,  41.9, 167.7),
            (  663.9, 449.6,  47.8, 127.2), (  740.1, 403.6,  92.7,  35.2),
            (  774.5, 344.1,  35.9,  67.6), (  463.5, 594.4,  53.8,  70.3),
            (  541.3, 579.5,  95.7,  40.6), (  566.7, 639.0,  44.9,  67.6),
            (  611.5, 659.3,  56.8,  27.1), (  565.2, 515.9,  53.8,  70.3),
            (  613.0, 498.3,  47.8,  24.4), (  438.1, 494.3, 110.6,  37.9),
            (  471.0, 441.5,  50.8,  67.6), (  550.2, 421.2, 101.7,  37.9),
            (  571.2, 350.9,  53.8, 102.8), (  653.4, 318.4, 110.6,  48.7),
            (  575.7, 206.1,  50.8,  94.7), (  637.0, 164.2,  53.8,  48.7),
            (  471.0, 165.5,  74.8,  35.2), (  527.8, 168.2,  32.9,  40.6),
            (  360.3, 208.8,  26.9, 127.2), (  447.1, 257.5, 104.7,  18.9),
            (  441.1, 340.0, 110.6,  32.5), (  463.5, 303.5,  53.8, 100.1),
            (  886.7, 145.2, 230.3,  32.5), ( 1058.6, 252.1, 161.5,  56.8),
            ( 1054.1, 202.1, 140.6,  27.1), (  997.3, 173.6,  32.9,  13.5),
            ( 1112.4, 149.3,  47.8,  67.6), (  163.0, 179.1, 248.2, 338.2),
            (  740.1,  39.7, 906.1,  54.1), ( 1172.3, 616.0,  47.8, 324.7),
            ( 1169.3, 221.0,  53.8, 259.7), (  979.4, 306.2,   9.0,  35.2)
        ]
        for cx, cy, w, h in obstaculos:
            obs = arcade.SpriteSolidColor(int(w), int(h), color_t)
            obs.center_x, obs.center_y = cx, cy
            self.paredes.append(obs)

    # ----------------------------------------------------------
    def on_key_press(self, key, mod):
        # Pantalla de instrucciones inicial
        if self.fase == "instrucciones":
            if key == arcade.key.ENTER:
                self.fase = "jugando"
                self.mensaje = "Recoge los fragmentos EN ORDEN: 1, 2, 3, 4, 5"
                self.tiempo_mensaje = 3.0
            return

        if self.mostrando_final:
            if key == arcade.key.ENTER:
                # Al terminar el Nivel 3, volver al menú principal
                from menu import Menu
                self.window.show_view(Menu())
            return

        self.teclas.add(key)

    def on_key_release(self, key, mod):
        self.teclas.discard(key)

    # ----------------------------------------------------------
    def on_update(self, delta_time):
        self.tiempo_global += delta_time

        # Fade in
        if self.fade_alpha > 0:
            self.fade_alpha -= self.fade_velocidad * delta_time
            if self.fade_alpha < 0:
                self.fade_alpha = 0

        # No actualizar juego durante instrucciones
        if self.fase == "instrucciones":
            return

        # Screen shake
        if self.shake_timer > 0:
            self.shake_timer -= delta_time
            sx = random.uniform(-12, 12)
            sy = random.uniform(-12, 12)
            self.camera_sprites.position = (configuracion.ANCHO / 2 + sx, configuracion.ALTO / 2 + sy)
        else:
            self.camera_sprites.position = (configuracion.ANCHO / 2, configuracion.ALTO / 2)

        if self.tiempo_mensaje > 0:
            self.tiempo_mensaje -= delta_time

        if self.mostrando_final:
            return

        # ---- Movimiento del jugador (WASD y flechas) ----
        dx = (arcade.key.D in self.teclas or arcade.key.RIGHT in self.teclas) \
           - (arcade.key.A in self.teclas or arcade.key.LEFT in self.teclas)
        dy = (arcade.key.W in self.teclas or arcade.key.UP in self.teclas) \
           - (arcade.key.S in self.teclas or arcade.key.DOWN in self.teclas)

        if dx != 0 or dy != 0:
            length = math.sqrt(dx**2 + dy**2)
            self.jugador.change_x = (dx / length) * configuracion.VELOCIDAD_JUGADOR
            self.jugador.change_y = (dy / length) * configuracion.VELOCIDAD_JUGADOR

            self.anim_timer += delta_time
            if self.anim_timer >= 0.15:
                self.anim_timer = 0
                self.jugador.texture = (
                    self.textura_caminar2 if self.frame_animacion == 0
                    else self.textura_caminar1
                )
                self.frame_animacion = 1 - self.frame_animacion
        else:
            self.jugador.change_x = 0
            self.jugador.change_y = 0
            self.jugador.texture = self.textura_quieto

        self.physics_engine.update()

        # ---- Enemigo patrullando en diagonal ----
        self.enemigo.center_x += self.enemigo_dx
        self.enemigo.center_y += self.enemigo_dy

        if self.enemigo.center_x < 50 or self.enemigo.center_x > configuracion.ANCHO - 50:
            self.enemigo_dx *= -1
        if self.enemigo.center_y < 50 or self.enemigo.center_y > configuracion.ALTO - 50:
            self.enemigo_dy *= -1

        # Colisión con enemigo → penalización (volver al inicio)
        if arcade.check_for_collision(self.jugador, self.enemigo):
            self.shake_timer = 0.4
            self.jugador.center_x, self.jugador.center_y = self.posicion_inicial
            self.teclas.clear()
            self.mensaje = "¡El guardián te atrapó! Volviste al inicio."
            self.tiempo_mensaje = 2.0

        # ---- Condición de victoria: salir por la derecha ----
        if self.fragmentos_recogidos >= self.total_fragmentos and self.jugador.center_x > 1150:
            self.mostrando_final = True
            self.fase = "final"
            self.teclas.clear()
            return

        # ---- Fragmentos flotantes ----
        for frag in self.lista_fragmentos:
            frag.center_y = frag.base_y + math.sin(self.tiempo_global * 4 + frag.center_x) * 5

        # ---- Actualizar Partículas ----
        for p in self.particulas[:]:
            p['radio'] += 60 * delta_time
            p['alpha'] -= 150 * delta_time
            if p['alpha'] <= 0:
                self.particulas.remove(p)

        # ---- Lógica del Puzzle: recoger en orden correcto ----
        tocados = arcade.check_for_collision_with_list(self.jugador, self.lista_fragmentos)
        for frag in tocados:
            if frag.numero == self.siguiente_fragmento:
                # Correcto
                self.particulas.append({
                    'x': frag.center_x, 'y': frag.center_y,
                    'radio': 10, 'alpha': 255
                })
                frag.remove_from_sprite_lists()
                self.fragmentos_recogidos += 1
                self.mensaje = self.mensajes_fragmentos[self.siguiente_fragmento - 1]
                self.tiempo_mensaje = 2.5
                self.siguiente_fragmento += 1

                if self.fragmentos_recogidos >= self.total_fragmentos:
                    self.mensaje = "¡Todos los fragmentos! Encuentra la salida → (derecha del mapa)"
                    self.tiempo_mensaje = 5.0
            else:
                # Incorrecto
                self.shake_timer = 0.4
                self.mensaje = f"¡Orden incorrecto! Busca primero el fragmento #{self.siguiente_fragmento}"
                self.tiempo_mensaje = 2.0
                self.jugador.center_x, self.jugador.center_y = self.posicion_inicial
                self.teclas.clear()

    # ----------------------------------------------------------
    def on_draw(self):
        self.clear()

        # ---- Cámara del mundo ----
        self.camera_sprites.use()

        # Fondo
        arcade.draw_texture_rect(
            self.fondo,
            arcade.LBWH(0, 0, configuracion.ANCHO, configuracion.ALTO)
        )

        if self.fase != "instrucciones":
            # Fragmentos
            self.lista_fragmentos.draw()

            # Números sobre cada fragmento
            for frag in self.lista_fragmentos:
                arcade.draw_circle_filled(frag.center_x, frag.center_y + 40, 18, (0, 0, 0, 200))
                color_num = arcade.color.LIME_GREEN if frag.numero == self.siguiente_fragmento else arcade.color.WHITE
                arcade.draw_text(
                    str(frag.numero),
                    frag.center_x, frag.center_y + 40,
                    color_num, 17, bold=True,
                    anchor_x="center", anchor_y="center"
                )

            # Flecha indicadora hacia el siguiente fragmento
            if self.siguiente_fragmento <= self.total_fragmentos and not self.mostrando_final:
                self._dibujar_flecha_indicadora()

            # Enemigo y Jugador
            self.lista_enemigos.draw()
            self.lista_jugadores.draw()

            # Partículas
            for p in self.particulas:
                arcade.draw_circle_outline(
                    p['x'], p['y'], p['radio'],
                    (255, 255, 100, int(max(0, p['alpha']))), 4
                )

        # ---- UI estática (no tiembla) ----
        self.camera_gui.use()

        # Fade in negro
        if self.fade_alpha > 0:
            arcade.draw_lrbt_rectangle_filled(
                0, configuracion.ANCHO,
                0, configuracion.ALTO,
                (0, 0, 0, int(self.fade_alpha))
            )

        # Pantalla de instrucciones
        if self.fase == "instrucciones":
            self._dibujar_instrucciones()
            return

        # HUD
        self._dibujar_hud()

        # Mensaje temporal
        if self.tiempo_mensaje > 0:
            arcade.draw_lrbt_rectangle_filled(
                0, configuracion.ANCHO, 25, 82, (0, 0, 0, 210)
            )
            arcade.draw_text(
                self.mensaje,
                0, 42,
                arcade.color.YELLOW, 21, bold=True,
                width=configuracion.ANCHO, align="center"
            )

        # Pantalla final
        if self.mostrando_final:
            self._dibujar_final()

    # ----------------------------------------------------------
    def _dibujar_instrucciones(self):
        """Pantalla de instrucciones del Nivel 3 (estilo nivel 1 y 2)."""
        arcade.draw_lrbt_rectangle_filled(
            0, configuracion.ANCHO, 0, configuracion.ALTO, (0, 0, 0, 210)
        )
        margen_x = 120
        margen_y = 80
        arcade.draw_lrbt_rectangle_filled(
            margen_x, configuracion.ANCHO - margen_x,
            margen_y, configuracion.ALTO - margen_y,
            (20, 20, 35)
        )
        arcade.draw_lrbt_rectangle_outline(
            margen_x, configuracion.ANCHO - margen_x,
            margen_y, configuracion.ALTO - margen_y,
            arcade.color.GOLD, 3
        )
        cx = configuracion.ANCHO / 2

        arcade.draw_text("NIVEL 3", cx, 590, arcade.color.GOLD, 38,
                         bold=True, anchor_x="center")
        arcade.draw_text("EL LABERINTO DE LA MEMORIA", cx, 535,
                         arcade.color.WHITE, 22, bold=True, anchor_x="center")

        arcade.draw_text("Recoge los 5 fragmentos de memoria", cx, 450,
                         arcade.color.WHITE, 20, anchor_x="center")
        arcade.draw_text("en el orden correcto: 1 → 2 → 3 → 4 → 5", cx, 415,
                         arcade.color.LIME_GREEN, 20, bold=True, anchor_x="center")

        arcade.draw_text("El fragmento que toca recoger brilla en verde.", cx, 355,
                         arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("Una flecha te guiará hacia él.", cx, 325,
                         arcade.color.WHITE, 18, anchor_x="center")

        arcade.draw_text("Evita al guardián — si te atrapa volvés al inicio.", cx, 265,
                         (255, 120, 120), 18, anchor_x="center")

        arcade.draw_text("Al recoger todo, escapa por la derecha del mapa.", cx, 215,
                         arcade.color.GOLD, 18, anchor_x="center")

        arcade.draw_text("WASD / FLECHAS: Moverse", cx, 165,
                         arcade.color.GOLD, 18, bold=True, anchor_x="center")
        arcade.draw_text("Presiona ENTER para comenzar", cx, 115,
                         arcade.color.YELLOW, 20, bold=True, anchor_x="center")

    # ----------------------------------------------------------
    def _dibujar_hud(self):
        """HUD superior con barra de progreso de fragmentos."""
        # Fondo HUD
        arcade.draw_lrbt_rectangle_filled(
            0, configuracion.ANCHO,
            configuracion.ALTO - 55, configuracion.ALTO,
            (0, 0, 0, 170)
        )

        # Texto izquierda
        arcade.draw_text(
            "FRAGMENTOS:", 18, configuracion.ALTO - 38,
            arcade.color.WHITE, 17, bold=True
        )

        # Íconos de fragmentos (rellenos = recogidos, vacíos = pendientes)
        for i in range(self.total_fragmentos):
            bx = 155 + i * 36
            by = configuracion.ALTO - 30
            recogido = i < self.fragmentos_recogidos
            color_circ = (100, 220, 100) if recogido else (80, 80, 90)
            arcade.draw_circle_filled(bx, by, 12, color_circ)
            arcade.draw_circle_outline(bx, by, 12, arcade.color.WHITE, 2)
            arcade.draw_text(
                str(i + 1), bx, by, arcade.color.WHITE,
                10, bold=True, anchor_x="center", anchor_y="center"
            )

        # Indicador del siguiente fragmento (derecha del HUD)
        if self.siguiente_fragmento <= self.total_fragmentos:
            arcade.draw_text(
                f"▶  Busca el #{self.siguiente_fragmento}",
                configuracion.ANCHO - 210, configuracion.ALTO - 38,
                arcade.color.LIME_GREEN, 18, bold=True
            )
        else:
            arcade.draw_text(
                "→ ¡Encuentra la salida!",
                configuracion.ANCHO - 260, configuracion.ALTO - 38,
                arcade.color.GOLD, 18, bold=True
            )

    # ----------------------------------------------------------
    def _dibujar_flecha_indicadora(self):
        """Dibuja una flecha animada apuntando al siguiente fragmento."""
        # Encontrar el sprite del fragmento siguiente
        objetivo = None
        for frag in self.lista_fragmentos:
            if frag.numero == self.siguiente_fragmento:
                objetivo = frag
                break

        if objetivo is None:
            return

        jx = self.jugador.center_x
        jy = self.jugador.center_y
        ox = objetivo.center_x
        oy = objetivo.center_y

        # Distancia al objetivo
        ddx = ox - jx
        ddy = oy - jy
        dist = math.sqrt(ddx**2 + ddy**2)

        if dist < 80:
            return   # Estamos muy cerca, no dibujar flecha

        # Normalizar dirección
        nx = ddx / dist
        ny = ddy / dist

        # Posición de la flecha (siempre a 55px del jugador)
        radio = 55
        ax = jx + nx * radio
        ay = jy + ny * radio

        # Punta de flecha (triángulo pequeño animado con pulso)
        pulso = 1.0 + 0.25 * math.sin(self.tiempo_global * 6)
        tam = 14 * pulso
        angulo = math.atan2(ny, nx)

        p1x = ax + math.cos(angulo) * tam
        p1y = ay + math.sin(angulo) * tam
        p2x = ax + math.cos(angulo + 2.4) * tam * 0.6
        p2y = ay + math.sin(angulo + 2.4) * tam * 0.6
        p3x = ax + math.cos(angulo - 2.4) * tam * 0.6
        p3y = ay + math.sin(angulo - 2.4) * tam * 0.6

        arcade.draw_triangle_filled(p1x, p1y, p2x, p2y, p3x, p3y, (100, 255, 120, 220))
        arcade.draw_triangle_outline(p1x, p1y, p2x, p2y, p3x, p3y, (0, 0, 0, 180), 2)

    # ----------------------------------------------------------
    def _dibujar_final(self):
        """Pantalla de fin del juego completo."""
        arcade.draw_lrbt_rectangle_filled(
            0, configuracion.ANCHO, 0, configuracion.ALTO, (0, 0, 0, 190)
        )
        arcade.draw_lrbt_rectangle_filled(
            150, configuracion.ANCHO - 150, 80, configuracion.ALTO - 80,
            (18, 18, 30)
        )
        arcade.draw_lrbt_rectangle_outline(
            150, configuracion.ANCHO - 150, 80, configuracion.ALTO - 80,
            arcade.color.GOLD, 3
        )

        cx = configuracion.ANCHO / 2

        arcade.draw_text(
            "★  JUEGO COMPLETADO  ★",
            cx, configuracion.ALTO - 130,
            arcade.color.GOLD, 34, bold=True,
            anchor_x="center"
        )

        arcade.draw_text(
            "Has reconstruido todos los fragmentos",
            cx, 520, arcade.color.WHITE, 21, anchor_x="center"
        )
        arcade.draw_text(
            "de tu memoria en el orden correcto.",
            cx, 488, arcade.color.WHITE, 21, anchor_x="center"
        )

        arcade.draw_text(
            "Cada recuerdo es una pieza de quien eres.",
            cx, 435, arcade.color.WHITE, 20, anchor_x="center"
        )
        arcade.draw_text(
            "No importa cuántas veces te pierdas,",
            cx, 405, arcade.color.WHITE, 20, anchor_x="center"
        )
        arcade.draw_text(
            "siempre podés volver a encontrarte.",
            cx, 375, arcade.color.WHITE, 20, anchor_x="center"
        )

        nombre = configuracion.NOMBRE_JUGADOR if configuracion.NOMBRE_JUGADOR else "Jugador"
        arcade.draw_text(
            f"Bien hecho, {nombre}. Has completado tu viaje.",
            cx, 315, arcade.color.GOLD, 22, bold=True, anchor_x="center"
        )

        arcade.draw_text(
            "Recuerda: pedir ayuda siempre es una señal de fortaleza.",
            cx, 255, (180, 230, 255), 18, anchor_x="center"
        )

        arcade.draw_lrbt_rectangle_filled(
            cx - 200, cx + 200, 140, 175, (40, 40, 60)
        )
        arcade.draw_lrbt_rectangle_outline(
            cx - 200, cx + 200, 140, 175, arcade.color.YELLOW, 2
        )
        arcade.draw_text(
            "ENTER — Volver al Menú",
            cx, 150, arcade.color.YELLOW, 19, bold=True, anchor_x="center"
        )
