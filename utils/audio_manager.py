import pygame
import os

AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'audio')
MUSIC_DIR = os.path.join(AUDIO_DIR, 'music')
SFX_DIR = os.path.join(AUDIO_DIR, 'sfx')


class AudioManager:
    """Singleton audio manager for music and sound effects with volume control."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        pygame.mixer.init()

        # Volume levels (0.0 - 1.0)
        self.music_volume = 0.5
        self.sfx_volume = 0.7

        # Pre-load sound effects
        self.sounds = {}
        sfx_map = {
            'click': 'freesound_crunchpixstudio-click-2-384920.mp3',
            'move': 'movepiece.mp3',
            'win': 'win.mp3',
            'lose': 'floraphonic-violin-lose-4-185125.mp3',
            'freeze': 'tanweraman-ice-freezing-445024.mp3',
            'undo': 'undo.mp3',
            'select': 'floraphonic-multi-pop-1-188165.mp3',
        }
        for key, filename in sfx_map.items():
            path = os.path.join(SFX_DIR, filename)
            if os.path.exists(path):
                try:
                    self.sounds[key] = pygame.mixer.Sound(path)
                except Exception:
                    pass

        # Apply initial volumes
        self._apply_sfx_volume()
        pygame.mixer.music.set_volume(self.music_volume)

    def _apply_sfx_volume(self):
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)

    def set_music_volume(self, vol):
        """Set music volume (0.0 - 1.0)"""
        self.music_volume = max(0.0, min(1.0, vol))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, vol):
        """Set SFX volume (0.0 - 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, vol))
        self._apply_sfx_volume()

    def play_music(self, filename=None, loops=-1):
        """Play background music. Loops=-1 means infinite loop."""
        if filename is None:
            filename = 'cyberwave-orchestra-adventure-game-fun-background-music-247661.mp3'
        path = os.path.join(MUSIC_DIR, filename)
        if os.path.exists(path):
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loops)
            except Exception:
                pass

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_sfx(self, name):
        """Play a sound effect by name."""
        if name in self.sounds and self.sfx_volume > 0:
            self.sounds[name].play()
