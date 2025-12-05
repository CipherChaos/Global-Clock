import os

from PyQt5.QtCore import QUrl

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from clock.config import ClockConfig


class AudioManager:
    """Manages audio playback for clock ticking sounds."""

    def __init__(self):
        self.sound_files = [os.path.abspath(f) for f in
                            ClockConfig.SOUND_FILES]
        self.current_sound_index = 0
        self.sound_enabled = True

        self.player = QMediaPlayer()
        self.player.setVolume(100)
        self.player.mediaStatusChanged.connect(self._on_media_status_changed)

    def play(self):
        """Play the current sound file."""
        try:
            audio_content = QMediaContent(
                QUrl.fromLocalFile(self.sound_files[self.current_sound_index])
            )
            self.player.setMedia(audio_content)
            if self.sound_enabled:
                self.player.play()
        except Exception as e:
            print(f"Error playing clock sound: {e}")

    def _on_media_status_changed(self, status):
        """Replay sound when it ends."""
        if status == QMediaPlayer.EndOfMedia:
            self.play()

    def switch_sound(self):
        """Switch to the next sound file."""
        self.current_sound_index = (self.current_sound_index + 1) % len(
            self.sound_files)
        self.play()

    def toggle(self):
        """Toggle sound on/off."""
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.player.play()
        else:
            self.player.stop()
        return self.sound_enabled
