# ==========================================================
# CONFIGURACIÓN DE LA VENTANA
# ==========================================================

ANCHO = 1200
ALTO = 800
TITULO = "imperdonables"

# ==========================================================
# TAMAÑO DEL MAPA DEL NIVEL 1
# ==========================================================

ANCHO_MAPA = 1800
ALTO_MAPA = 1000


# ==========================================================
# VELOCIDAD DEL JUGADOR
# ==========================================================

VELOCIDAD_JUGADOR = 5


# ==========================================================
# NOMBRE DEL JUGADOR (se asigna en PantallaNombre)
# ==========================================================

NOMBRE_JUGADOR = ""


# ==========================================================
# MÚSICA
# ==========================================================

_musica_actual = None
_player_actual = None


def reproducir_musica(ruta, volumen=0.5):
    """Reproduce música de fondo. Si el archivo no existe, no hace nada."""
    global _musica_actual, _player_actual
    try:
        import arcade
        if _player_actual is not None:
            try:
                _player_actual.pause()
            except Exception:
                pass
            _player_actual = None

        sonido = arcade.load_sound(ruta)  #carga el sonido 
        _player_actual = arcade.play_sound(sonido, volume=volumen, loop=True) #reproduce el sonido 
        _musica_actual = ruta
    except Exception:
        pass  # El archivo de audio no existe o hay un error: ignorar silenciosamente


def detener_musica():
    """Detiene la música actual si está sonando."""
    global _player_actual
    if _player_actual is not None:
        try:
            import arcade
            arcade.stop_sound(_player_actual)
        except Exception:
            pass
        _player_actual = None