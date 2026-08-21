import arcade
import configuracion
import nivel2  

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.tex_quieto = arcade.load_texture("imagenes/personajes/protagonista/quieto.png")
        self.tex_caminar1 = arcade.load_texture("imagenes/personajes/protagonista/caminar1.png")
        self.tex_caminar2 = arcade.load_texture("imagenes/personajes/protagonista/caminar2.png")
        self.texture = self.tex_quieto
        self.scale = 0.15
        self.anim_timer = 0
        self.frame = 0

    def update_animation(self, dx, dy):
        if dx != 0 or dy != 0:
            self.anim_timer += 1
            if self.anim_timer > 10:
                self.anim_timer = 0
                self.frame = 1 - self.frame
                self.texture = self.tex_caminar1 if self.frame == 0 else self.tex_caminar2
        else:
            self.texture = self.tex_quieto

class Nivel1(arcade.View):
    def __init__(self):
        super().__init__()
        self.mapa = arcade.load_texture("imagenes/mapas/nivel_inseguridad.png")
        self.camera = arcade.Camera2D()
        self.camera.position = (600, 400)
        
        self.player = Player()
        self.player.center_x, self.player.center_y = 150, 400  
        
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        
        self.paredes = arcade.SpriteList()
        self.teclas = set()
        
        # Villano (Inseguridad) patrullando verticalmente
        self.enemigo_list = arcade.SpriteList()
        self.enemigo = arcade.Sprite("imagenes/personajes/enemigos/enemigo1.png", scale=0.15)
        self.enemigo.center_x, self.enemigo.center_y = 600, 400
        self.enemigo.change_y = 2  
        self.enemigo_list.append(self.enemigo)
        
        # Dibujos dispersados por el mapa 📄
        self.dibujo_list = arcade.SpriteList()
        posiciones_dibujos = [(400, 650), (950, 250), (1050, 650)]
        for px, py in posiciones_dibujos:
            dib = arcade.Sprite("imagenes/objetos/dibujo.png", scale=0.1)
            dib.center_x, dib.center_y = px, py
            self.dibujo_list.append(dib)
        
        # Diálogo inicial del villano
        self.mostrar_dialogo = True
        self.tiempo_dialogo = 0
        
        # Oscuridad 🌑
        self.nivel_opacidad = 0
        self.temporizador_ciclo = 0
        self.fase_oscura = False

        self.setup_colisiones()

    def setup_colisiones(self):
        color_transparente = (0, 0, 0, 0)
        
        # Paredes perimetrales con aberturas correctas para entrada y salida
        # Izquierda (dejando hueco para el túnel en y: 350 a 450)
        p_izq1 = arcade.SpriteSolidColor(20, 350, color_transparente)
        p_izq1.center_x, p_izq1.center_y = 10, 175
        self.paredes.append(p_izq1)
        
        p_izq2 = arcade.SpriteSolidColor(20, 350, color_transparente)
        p_izq2.center_x, p_izq2.center_y = 10, 625
        self.paredes.append(p_izq2)

        # Derecha (dejando hueco para la puerta en y: 380 a 520)
        p_der1 = arcade.SpriteSolidColor(20, 280, color_transparente)
        p_der1.center_x, p_der1.center_y = 1190, 140
        self.paredes.append(p_der1)
        
        p_der2 = arcade.SpriteSolidColor(20, 280, color_transparente)
        p_der2.center_x, p_der2.center_y = 1190, 660
        self.paredes.append(p_der2)

        # Abajo y Arriba completos
        p_abajo = arcade.SpriteSolidColor(1200, 20, color_transparente)
        p_abajo.center_x, p_abajo.center_y = 600, 10
        self.paredes.append(p_abajo)

        p_arriba = arcade.SpriteSolidColor(1200, 20, color_transparente)
        p_arriba.center_x, p_arriba.center_y = 600, 790
        self.paredes.append(p_arriba)

        # Obstáculos internos del mapa
        obstaculos_internos = [
            (350, 600, 100, 80),  
            (850, 600, 100, 80),  
            (600, 430, 90, 80),  
            (330, 220, 100, 80),  
            (870, 220, 100, 80)   
        ]
        for x, y, w, h in obstaculos_internos:
            obs = arcade.SpriteSolidColor(int(w), int(h), color_transparente)
            obs.center_x, obs.center_y = x, y
            self.paredes.append(obs)

    def on_key_press(self, key, mod): 
        self.teclas.add(key)
        
    def on_key_release(self, key, mod): 
        self.teclas.discard(key)

    def on_update(self, delta_time):
        dx = (arcade.key.D in self.teclas or arcade.key.RIGHT in self.teclas) - (arcade.key.A in self.teclas or arcade.key.LEFT in self.teclas)
        dy = (arcade.key.W in self.teclas or arcade.key.UP in self.teclas) - (arcade.key.S in self.teclas or arcade.key.DOWN in self.teclas)
        
        self.player.center_x += dx * configuracion.VELOCIDAD_JUGADOR
        if arcade.check_for_collision_with_list(self.player, self.paredes): 
            self.player.center_x -= dx * configuracion.VELOCIDAD_JUGADOR
            
        self.player.center_y += dy * configuracion.VELOCIDAD_JUGADOR
        if arcade.check_for_collision_with_list(self.player, self.paredes): 
            self.player.center_y -= dy * configuracion.VELOCIDAD_JUGADOR
            
        self.player.update_animation(dx, dy)

        # Patrullaje vertical del enemigo
        self.enemigo.center_y += self.enemigo.change_y
        if self.enemigo.center_y < 250 or self.enemigo.center_y > 600:
            self.enemigo.change_y *= -1

        # Control del diálogo inicial
        if self.mostrar_dialogo:
            self.tiempo_dialogo += delta_time
            if self.tiempo_dialogo > 5:
                self.mostrar_dialogo = False

        # Ciclo de oscuridad
        if not self.mostrar_dialogo:
            self.temporizador_ciclo += delta_time
            if self.temporizador_ciclo > 4:
                self.fase_oscura = True
                self.temporizador_ciclo = 0

            if self.fase_oscura:
                self.nivel_opacidad += 3
                if self.nivel_opacidad >= 235:
                    self.nivel_opacidad = 235
                    self.fase_oscura = False
            elif self.nivel_opacidad > 0:
                self.nivel_opacidad -= 1  

        # Recoger dibujos
        dibujos_tocados = arcade.check_for_collision_with_list(self.player, self.dibujo_list)
        for dibujo in dibujos_tocados:
            dibujo.remove_from_sprite_lists()

        # Condición de victoria: todos los dibujos recolectados Y cruzar la puerta de la derecha (y entre 380 y 520)
        if len(self.dibujo_list) == 0 and self.player.center_x >= 1170 and (380 <= self.player.center_y <= 520):
            self.window.show_view(nivel2.Nivel2())

    def on_draw(self):
        self.clear()
        self.camera.use()
        
        arcade.draw_texture_rect(self.mapa, arcade.rect.LBWH(0, 0, 1200, 800))
        
        self.player_list.draw()
        self.enemigo_list.draw()
        self.dibujo_list.draw()
        
        if self.mostrar_dialogo:
            arcade.draw_text("Inseguridad: Recolecta todos los trazos antes de que te consuma la oscuridad...", 
                             self.enemigo.center_x - 220, self.enemigo.center_y + 40, 
                             arcade.color.RED, 14, bold=True)
        
        if self.nivel_opacidad > 0:
            arcade.draw_lrbt_rectangle_filled(
                0, 1200, 0, 800,
                (0, 0, 0, self.nivel_opacidad)
            )