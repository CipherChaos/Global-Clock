import os
from PyQt5.QtCore import Qt, QElapsedTimer, QPointF
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont, QPixmap, QColor
from PyQt5.QtWidgets import QComboBox
import math
import pytz
from datetime import datetime
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget
from PyQt5.QtGui import QDesktopServices

def deg_to_rad(degrees):
    return degrees * (math.pi / 180)


def _get_next_style(current_style, style_dict):
    keys = list(style_dict.keys())
    current_index = keys.index(next(
        key for key, value in style_dict.items() if
        value == current_style))

    # Loop to find a non-duplicate style
    for i in range(1, len(keys) + 1):
        next_index = (current_index + i) % len(keys)
        if style_dict[keys[next_index]] != current_style:
            return style_dict[keys[next_index]]
    return current_style  # In case no change is found (fallback)


def _show_error_message(message):

    print(f"Error: {message}")  #


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.m_radiusMap = None
        self.RADIUS = None
        self.H_HEIGHT = None
        self.H_WIDTH = None
        self.setWindowTitle("Clock with Digital/Analog Toggle")
        self.setGeometry(100, 100, 1920, 1080)

        # Variables for the clock
        self.m_clock60 = {i: i * 6 for i in range(60)}

        # Settings
        self.m_timer = QTimer(self)
        self.m_timer.timeout.connect(self.animation_loop)
        self.m_timer.start(int(1000 / 60))
        self.m_elapsedTimer = QElapsedTimer()
        self.m_elapsedTimer.start()

        # Timer for animations

        self.m_hour = self.m_minute = self.m_second = 0
        self.is_digital = False
        self.show_clock = True

        # Sound settings
        self.sound_files = [
            os.path.abspath("./Medias/Sounds/Ticking-1.mp3"),
            os.path.abspath("./Medias/Sounds/Ticking-2.mp3"),
            os.path.abspath("./Medias/Sounds/Ticking-3.mp3")
        ]
        self.current_sound_index = 0
        self.sound_enabled = True

        # Sound player
        self.audio_player = QMediaPlayer()
        # Adjusting the volume to 100
        self.audio_player.setVolume(100)
        self.audio_player.mediaStatusChanged.connect(
            self.on_media_status_changed)

        # Button to switch the clock sound
        self.switch_sound_button = QPushButton("Switch the Clock Sound", self)
        self.switch_sound_button.clicked.connect(self.switch_clock_sound)
        self.switch_sound_button.move(800, 10)

        # Button to toggle sound on/off
        self.toggle_sound_button = QPushButton("Clock Sound (on)", self)
        self.toggle_sound_button.clicked.connect(self.toggle_clock_sound)
        self.toggle_sound_button.move(1100, 10)

        self.play_clock_sound()

        # Dictionary for images of different time zones
        self.city_images = {
            "London": "./Medias/Backgrounds/London-clock-tower.jpg",
            "New York": "./Medias/Backgrounds/New-York.jpg",
            "Paris": "./Medias/Backgrounds/Paris.jpg",
            "Tokyo": "./Medias/Backgrounds/Tokyo.jpg",
            "Sydney": "./Medias/Backgrounds/Sydney.jpg",
            "Berlin": "./Medias/Backgrounds/Berlin.jpg",
            "Dubai": "./Medias/Backgrounds/Dubai.jpg",
            "Rome": "./Medias/Backgrounds/Rome.jpg",
            "Moscow": "./Medias/Backgrounds/Moscow.jpg",
            "Shanghai": "./Medias/Backgrounds/Shanghai.jpg",
            "Mumbai": "./Medias/Backgrounds/Mumbai.jpg",
            "Toronto": "./Medias/Backgrounds/Toronto.jpg",
            "Mexico City": "./Medias/Backgrounds/Mexico-city.jpg",
            "Seoul": "./Medias/Backgrounds/Seoul.jpg",
            "Bangkok": "./Medias/Backgrounds/Bangkok.jpg",
            "Athens": "./Medias/Backgrounds/Athens.jpg",
            "Tehran": "./Medias/Backgrounds/Tehran.jpg"
        }

        self.background_image = QPixmap(self.city_images["Tehran"])
        self.cached_image = None
        self.cached_size = None

        # Dictionary for clock style images
        self.clock_images = {
            "Billiard" :QPixmap
                ("./Medias/Analog-Styles/Billiard-modified.png"),
            "Blue-neon" :QPixmap
                ("./Medias/Analog-Styles/Blue-neon-modified.png"),
            "Modern-pilot" :QPixmap
                ("./Medias/Analog-Styles/Modern-Pilot-modified.png"),
            "Omega": QPixmap(
                "./Medias/Analog-Styles/Omega-Black-Gold-modified.png"),
            "Porsche" :QPixmap("./Medias/Analog-Styles/Porsche-modified.png"),
            "Purple-mystery" :QPixmap
                ("./Medias/Analog-Styles/Purple-Mystery-modified.png"),
            "Purple-mystery-2": QPixmap(
                "./Medias/Analog-Styles/Purple-Mystery-modified-2.png"),

            "Rings": QPixmap("./Medias/Analog-Styles/Rings-modified.png"),
            "Rolex": QPixmap("./Medias/Analog-Styles/Rolex-modified-1.png"),
            "Rolex2": QPixmap("./Medias/Analog-Styles/Rolex-modified-2.png"),
            "Rolex3": QPixmap("./Medias/Analog-Styles/Rolex-modified-3.png"),
            "Sun" :QPixmap("./Medias/Analog-Styles/Sun-modified.png"),
            "Tux" :QPixmap("./Medias/Analog-Styles/Tux-modified.png"),
            "Yalda" :QPixmap("./Medias/Analog-Styles/Yalda-modified.png"),
            "Simple_farsi": QPixmap(
                "./Medias/Analog-Styles/Simple-Farsi-modified.png")

        }


        self.digital_style_image = {
            "Aqua" :QPixmap(
                "./Medias/Digital-Styles/Aqua-digital.png"),
            "Coca" :QPixmap("./Medias/Digital-Styles/Coca-digital.png"),
            "Emerald" :QPixmap("./Medias/Digital-Styles/Emerald-digital.png"),
            "Gem" :QPixmap("./Medias/Digital-Styles/Gem-digital.png"),
            "Ocean": QPixmap("./Medias/Digital-Styles/Ocean-digital.png"),
            "Red-cobalt" :QPixmap(
                "./Medias/Digital-Styles/Red-cobalt-digital.png"),
            "Wooden" :QPixmap("./Medias/Digital-Styles/Wooden-digital.png")
        }

        # Default image for digital style
        self.digital_default_style = self.digital_style_image["Aqua"]
        # Default image for analog style
        self.analog_default_style = self.clock_images["Omega"]
        self.current_style = self.analog_default_style

        # Button to toggle between digital and analog mode
        self.toggle_button = QPushButton("Switch to Digital", self)
        self.toggle_button.clicked.connect(self.toggle_clock)
        self.toggle_button.move(10, 10)

        # Button to change time zone
        self.time_zone_button = QPushButton("Time Zone", self)
        self.time_zone_button.clicked.connect(self.show_time_zone_menu)
        self.time_zone_button.move(150, 10)

        # Button to change clock style
        self.clock_style_button = QPushButton("Change Clock Style", self)
        self.clock_style_button.clicked.connect(self.change_clock_style)
        self.clock_style_button.move(650, 10)

        # ComboBox for time zone selection
        self.time_zones = [
            "London", "New York", "Paris", "Tokyo", "Sydney", "Berlin",
            "Dubai", "Rome", "Moscow", "Shanghai", "Mumbai", "Toronto",
            "Mexico City", "Seoul", "Bangkok", "Athens", "Tehran"
        ]
        self.time_zone_combo = QComboBox(self)
        self.time_zone_combo.addItems(self.time_zones)
        self.time_zone_combo.activated.connect(self.update_time_zone)
        self.time_zone_combo.move(300, 10)
        self.time_zone_combo.setVisible(False)

        # Button to show/hide the clock
        self.hide_clock_button = QPushButton("Hide the Clock", self)
        self.hide_clock_button.clicked.connect(self.toggle_show_clock)
        self.hide_clock_button.move(500, 10)

        self.selected_tz = pytz.timezone("Asia/Tehran")
        self.local_time = datetime.now(self.selected_tz)

        # Add the Support button
        self.support_button = QPushButton("Support", self)
        self.support_button.clicked.connect(self.open_github)
        self.support_button.move(1300, 10)  # Adjust the position as needed

    def open_github(self):
        # GitHub link
        github_url = "https://github.com/CipherChaos"  # alternative link
        try:
            url = QUrl(github_url)
            if not url.isValid():  # Link authorization
                raise ValueError("The URL is not valid.")
            QDesktopServices.openUrl(url)
        except ValueError as value_error:
            self.show_error_message(f"Invalid URL: {value_error}")
        except OSError as os_error:
            self.show_error_message(f"Failed to open URL: {os_error}")
        except Exception as error:
            self.show_error_message(f"An unexpected error occurred: {error}")
    def play_clock_sound(self):
        try:
            audio_content = QMediaContent(
                QUrl.fromLocalFile(self.sound_files[self.current_sound_index]))
            self.audio_player.setMedia(audio_content)
            if self.sound_enabled:
                self.audio_player.play()
        except Exception as error:
            print(f"Error playing clock sound: {error}")

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.play_clock_sound()  # Play the sound again if it has ended

    def switch_clock_sound(self):
        try:
            self.current_sound_index = (self.current_sound_index + 1) % len(
                self.sound_files)
            self.play_clock_sound()
        except Exception as error:
            print(f"Error switching clock sound: {error}")


    def toggle_clock_sound(self):
        # Toggle to on/off
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.audio_player.play()
            self.toggle_sound_button.setText("Clock Sound (on)")
        else:
            self.audio_player.stop()
            self.toggle_sound_button.setText("Clock Sound (off)")


    def show_time_zone_menu(self):
        self.time_zone_combo.setVisible(not self.time_zone_combo.isVisible())

    def update_time_zone(self):
        selected_zone = self.time_zone_combo.currentText()
        self.update_time_by_zone(selected_zone)
        self.update()

    def update_time_by_zone(self, zone_name):
        try:
            # Updating the time zone
            time_zones = {
                "London": "Europe/London",
                "New York": "America/New_York",
                "Paris": "Europe/Paris",
                "Tokyo": "Asia/Tokyo",
                "Sydney": "Australia/Sydney",
                "Berlin": "Europe/Berlin",
                "Dubai": "Asia/Dubai",
                "Rome": "Europe/Rome",
                "Moscow": "Europe/Moscow",
                "Shanghai": "Asia/Shanghai",
                "Mumbai": "Asia/Kolkata",
                "Toronto": "America/Toronto",
                "Mexico City": "America/Mexico_City",
                "Seoul": "Asia/Seoul",
                "Bangkok": "Asia/Bangkok",
                "Athens": "Europe/Athens",
                "Tehran": "Asia/Tehran"
            }
            tz_name = time_zones.get(zone_name, "Europe/London")
            self.selected_tz = pytz.timezone(tz_name)
            self.local_time = datetime.now(self.selected_tz)
            self.background_image = QPixmap(
                self.city_images.get(zone_name, "London-clock-tower.jpg"))
            # Updating the time zone by deleting the cache storage
            self.cached_size = None
        except KeyError as error:
            print(f"Invalid time zone key: {error}")
        except Exception as error:
            print(f"Error updating time zone: {error}")

    def toggle_clock(self):
        self.is_digital = not self.is_digital
        self.toggle_button.setText(
            "Switch to Analog" if self.is_digital else "Switch to Digital")

        if self.is_digital:
            # Default digital style
            self.current_style = self.digital_default_style
        else:
            # Default analog style
            self.current_style = self.analog_default_style

        self.update()

    def toggle_show_clock(self):
        self.show_clock = not self.show_clock
        self.hide_clock_button.setText(
            "Show the Clock" if not self.show_clock else "Hide the Clock")
        self.update()

    def change_clock_style(self):
        try:
            if self.is_digital:
                # Changing the clock style to digital mode
                self.current_style = _get_next_style(self.current_style,
                                                     self.digital_style_image)
            else:
                # Changing style to analog mode
                self.current_style = _get_next_style(self.current_style,
                                                     self.clock_images)

            # Update the clock style after change
            self.update()

        except ValueError as error:
            print(f"Error changing clock style: {error}")
        except Exception as error:
            print(f"Unexpected error in change_clock_style: {error}")

    def animation_loop(self):
        self.local_time = datetime.now(self.selected_tz)
        self.m_hour = self.local_time.hour
        self.m_minute = self.local_time.minute
        self.m_second = self.local_time.second
        self.update()

    def resizeEvent(self, event):
        self.H_WIDTH = self.width() / 2
        self.H_HEIGHT = self.height() / 2
        self.RADIUS = self.H_HEIGHT - 50
        self.m_radiusMap = {
            "sec": self.RADIUS - 100,
            "min": self.RADIUS - 150,
            "hour": self.RADIUS - 250,
            "digit": self.RADIUS - 30
        }
        self.cached_size = None

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)

        if self.cached_size != self.size():
            self.cached_image = self.background_image.scaled(
                self.width(), self.height(), Qt.KeepAspectRatioByExpanding)
            self.cached_size = self.size()

        if self.cached_image:
            qp.drawPixmap(0, 0, self.cached_image)

        if self.show_clock:

            # Only when it is not in digital mode.
            if self.current_style and not self.is_digital:

                omega_size = min(self.width(),
                                 # The size of the image relative to the size of the window.
                                 self.height()) * 0.8
                omega_pos = QPointF(self.H_WIDTH - omega_size / 2,
                                    self.H_HEIGHT - omega_size / 2)
                qp.drawPixmap(int(omega_pos.x()), int(omega_pos.y()),
                              int(omega_size), int(omega_size),
                              self.current_style)

            if self.is_digital:  # Only when it is digital
                self.draw_digital_clock(qp)
            else:
                self.draw_face(qp)
                self.drawclock(qp)

    def get_clock_pos(self, clock_hand_type, key):
        # Calculating the angle based on local time.
        if clock_hand_type == "hour":
            hour = self.local_time.hour % 12
            angle = (hour * 30 + self.local_time.minute * 0.5 - 90) % 360
        elif clock_hand_type == "min":
            angle = (self.local_time.minute * 6 - 90) % 360
        elif clock_hand_type == "sec":
            angle = (self.local_time.second * 6 - 90) % 360
        else:
            # Default value
            return QPointF(self.H_WIDTH, self.H_HEIGHT)

        x = self.H_WIDTH + self.m_radiusMap[key] * math.cos(deg_to_rad(angle))
        y = self.H_HEIGHT + self.m_radiusMap[key] * math.sin(deg_to_rad(angle))
        return QPointF(x, y)

    def draw_face(self, p):
        p.save()
        for digit, angle in self.m_clock60.items():
            radius = 2
            if digit % 15 == 0:
                radius = 20
            elif digit % 5 == 0:
                radius = 8
            p.setPen(QPen(Qt.white, 7.0))
            if radius == 2:
                p.setBrush(QBrush(Qt.white))
            p.drawEllipse(self.get_clock_pos(digit, "digit"), radius, radius)
        p.restore()

    def drawclock(self, p):
        p.save()

        # Definition of modern and minimal colors
        primary_color = QColor(100, 149, 237)  # Cornflower Blue
        secondary_color = QColor(112, 128, 144)  # Slate Gray
        accent_color = QColor(240, 128, 128)  # Light Coral

        # Drawing the clock hands (hour, minute, second)
        self.draw_clock_hand(p, primary_color, "hour", "hour", 6, 12)
        self.draw_clock_hand(p, secondary_color, "min", "min", 4, 10)
        self.draw_clock_hand(p, accent_color, "sec", "sec", 2, 8)

        # The center of clock
        p.setBrush(QBrush(primary_color))
        p.drawEllipse(QPointF(self.H_WIDTH, self.H_HEIGHT), 6.0, 6.0)

        p.restore()

    def draw_clock_hand(self, p, color, clock_hand_type, key, min_thickness,
                        max_thickness):
        angle_pos = self.get_clock_pos(clock_hand_type, key)
        pen = QPen(color, max_thickness)
        pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)

        # Thinner tip for the hands
        pen.setWidth(min_thickness)
        p.setBrush(QBrush(color))
        p.drawLine(QPointF(self.H_WIDTH, self.H_HEIGHT), angle_pos)

        # Adding a small circle to the tips of the hands to make them look better.
        tip_radius = max_thickness / 2
        p.drawEllipse(angle_pos, tip_radius, tip_radius)

    def draw_digital_clock(self, qp):
        font = QFont("Arial", 100, QFont.Bold)
        font.setStyleHint(QFont.SansSerif)
        qp.setFont(font)

        time_str = self.local_time.strftime("%H:%M:%S")
        qp.setPen(QPen(Qt.white))

        # Using the current style
        pixmap = self.current_style

        if isinstance(pixmap, QPixmap):
            pixmap = pixmap.scaled(600, 300, Qt.KeepAspectRatio)
        else:
            print("Error: Current style is not a valid QPixmap object")

        x = int(self.H_WIDTH - 300)
        y = int(self.H_HEIGHT - 110)
        qp.drawPixmap(x, y, pixmap)


        qp.setPen(QPen(QColor(30, 30, 30), 5))
        qp.setBrush(Qt.transparent)

        # Clock position in the center of pixmap
        text_x = x + (pixmap.width() - qp.fontMetrics().horizontalAdvance(
            time_str)) / 2
        text_y = y + (pixmap.height() + qp.fontMetrics().height()) / 2.5

        qp.drawText(int(text_x), int(text_y), time_str)

    def show_error_message(self, param):
        pass


if __name__ == "__main__":
    try:
        app = QApplication([])
        window = Window()
        window.show()
        app.exec()
    except Exception as applicatoin_error:
        print(f"Application encountered an error: {applicatoin_error}")
