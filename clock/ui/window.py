import os
import pytz

from PyQt5.QtCore import Qt, QTimer, QUrl

from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QWidget, QMessageBox, QVBoxLayout

from PyQt5.QtGui import QDesktopServices

from clock.audio import AudioManager
from clock.render import ClockRenderer
from clock.ui import submenu, sidebar

from clock.utils import get_local_time, get_next_style

from clock.config import ClockConfig


class ClockWindow(QWidget):
    """Main clock window with fixed timezone updates."""

    timezone_expanded: False

    def __init__(self):
        super().__init__()

        self.audio_manager = AudioManager()
        self.renderer = ClockRenderer()
        self.sidebar = sidebar.SidebarPanel()
        self.display_submenu = submenu.HorizontalSubMenu()
        self.continent_container = QWidget()
        self.continent_layout = QVBoxLayout()
        self.timer = QTimer()

        self.is_digital = False
        self.show_clock = True
        self.selected_tz = pytz.timezone("Asia/Tehran")
        self.local_time = get_local_time("Asia/Tehran")

        # Default city
        self.current_city = "Tehran"

        # Initial graphics variables
        self.background_image = None
        self.cached_image = None
        self.cached_size = None
        self.sidebar.add_menu_item = None
        self.display_menu_btn = None
        self.timezone_menu_btn = None
        self.radius_map = {}

        # Initial audio variables
        self.audio_menu_btn = None
        self.audio_submenu = None

        # Initial info variables
        self.info_menu_btn = None
        self.info_submenu = None

        self.analog_styles = {k: QPixmap(v) for k, v in
                              ClockConfig.ANALOG_STYLES.items()}
        self.digital_styles = {k: QPixmap(v) for k, v in
                               ClockConfig.DIGITAL_STYLES.items()}

        self.current_style = self.analog_styles["Omega"]

        self.setup_ui()
        self.setup_timer()

        # Load initial background
        self.update_background("Tehran")

        self.audio_manager.play()

    def setup_ui(self):
        """Set up the main window UI."""
        self.setWindowTitle(ClockConfig.WINDOW_TITLE)
        self.setGeometry(100, 100, ClockConfig.WINDOW_WIDTH,
                         ClockConfig.WINDOW_HEIGHT)

        # Create sidebar
        self.sidebar = sidebar.SidebarPanel(self)
        self.sidebar.setGeometry(0, 0, 60, self.height())

        # Display menu with submenu
        self.display_menu_btn = self.sidebar.add_menu_item("🎨", "Display")
        self.display_submenu = submenu.HorizontalSubMenu(self)
        self.display_submenu.add_item("Toggle Clock Mode",
                                      self._toggle_mode_action)
        self.display_submenu.add_item("Change Clock Style",
                                      self._change_style_action)
        self.display_submenu.add_item("Toggle Clock Visibility",
                                      self._toggle_visibility_action)
        self.display_menu_btn.clicked.connect(self.show_display_menu)

        # Time Zone menu
        self.timezone_menu_btn = self.sidebar.add_menu_item("🌍", "Time Zone")
        self.timezone_expanded = False

        # Create a container widget for continents
        self.continent_container = QWidget()
        self.continent_layout = QVBoxLayout(self.continent_container)
        self.continent_layout.setContentsMargins(0, 0, 0, 0)
        self.continent_layout.setSpacing(2)
        self.sidebar.menu_layout.addWidget(self.continent_container)
        self.continent_container.hide()
        self.timezone_menu_btn.clicked.connect(self.toggle_timezone_menu)

        # Add continents to the container
        for continent, cities in ClockConfig.TIME_ZONES_BY_CONTINENT.items():
            continent_btn = self.sidebar.add_continent_menu(continent, cities)
            self.continent_layout.addWidget(continent_btn)
            self.sidebar.menu_layout.removeWidget(continent_btn)

        # Audio menu
        self.audio_menu_btn = self.sidebar.add_menu_item("🔊", "Audio")
        self.audio_submenu = submenu.HorizontalSubMenu(self)
        self.audio_submenu.add_item("Toggle Sound On/Off",
                                    self._toggle_sound_action)
        self.audio_submenu.add_item("Switch Sound Effect",
                                    self._switch_sound_action)
        self.audio_menu_btn.clicked.connect(self.show_audio_menu)

        # Info menu
        self.info_menu_btn = self.sidebar.add_menu_item("?", "Info")
        self.info_submenu = submenu.HorizontalSubMenu(self)
        self.info_submenu.add_item("About", self._show_about_action)
        self.info_submenu.add_item("Support", self._open_support_action)

        # Connect info menu button to show submenu
        self.info_menu_btn.clicked.connect(self.show_info_menu)

    def show_display_menu(self):
        """Show display submenu."""
        self.display_submenu.show_menu(self.display_menu_btn)

    def _toggle_mode_action(self, text):
        """Toggle between analog and digital mode."""
        self.display_submenu.hide_menu()
        self.toggle_clock_mode()

    def _change_style_action(self, text):
        """Change clock style."""
        self.display_submenu.hide_menu()
        self.change_clock_style()

    def _toggle_visibility_action(self, text):
        """Toggle clock visibility."""
        self.display_submenu.hide_menu()
        self.toggle_clock_visibility()

    def toggle_timezone_menu(self):
        """Toggle continent menu visibility."""
        self.timezone_expanded = not self.timezone_expanded

        if self.timezone_expanded:
            self.continent_container.show()

        else:
            self.continent_container.hide()
            for btn in self.sidebar.continent_buttons:
                btn.hide_submenu()

    def show_audio_menu(self):
        """Show audio submenu."""
        self.audio_submenu.show_menu(self.audio_menu_btn)

    def show_info_menu(self):
        """Show info submenu."""
        self.info_submenu.show_menu(self.info_menu_btn)

    def _toggle_sound_action(self, text):
        """Toggle sound and hide menu."""
        self.audio_manager.toggle()
        self.audio_submenu.hide_menu()

    def _switch_sound_action(self, text):
        """Switch sound and hide menu."""
        self.audio_submenu.hide_menu()
        self.switch_sound()

    def _show_about_action(self, text):
        """Show about dialog."""
        self.info_submenu.hide_menu()
        self.show_about()

    def _open_support_action(self, text):
        """Open support link."""
        self.info_submenu.hide_menu()
        self.open_support()

    def setup_timer(self):
        """Setup animation timer."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animation_loop)
        self.timer.start(int(1000 / ClockConfig.FPS))

    def toggle_clock_mode(self):
        """Toggle between digital and analog modes."""
        self.is_digital = not self.is_digital

        if self.is_digital:
            self.current_style = self.digital_styles["Aqua"]
        else:
            self.current_style = self.analog_styles["Omega"]

        self.update()

    def toggle_clock_visibility(self):
        """Toggle clock visibility."""
        self.show_clock = not self.show_clock
        self.update()

    def change_clock_style(self):
        """Change the current clock style."""
        if self.is_digital:
            self.current_style = get_next_style(self.current_style,
                                                self.digital_styles)
        else:
            self.current_style = get_next_style(self.current_style,
                                                self.analog_styles)
        self.update()

    def set_timezone(self, city):
        tz_name = ClockConfig.TIME_ZONES.get(city)

        self.selected_tz = pytz.timezone(tz_name)
        self.local_time = get_local_time(tz_name)
        self.current_city = city

        self.update_background(city)
        self.cached_size = None
        self.update()

    def update_background(self, city):
        """Update background image for the selected city."""
        try:
            image_path = ClockConfig.CITY_IMAGES.get(city)
            if image_path:
                if os.path.exists(image_path):
                    self.background_image = QPixmap(image_path)
                    self.cached_size = None
                else:

                    for key, path in ClockConfig.CITY_IMAGES.items():
                        if os.path.exists(path):
                            self.background_image = QPixmap(path)
                            self.cached_size = None
                            break
            else:
                print(f"No background image defined for city: {city}")
        except Exception as e:
            print(f"Error loading background image: {e}")

    def switch_sound(self):
        """Switch to next sound."""
        self.audio_manager.switch_sound()

    @staticmethod
    def open_support():
        """Open support link."""
        url = QUrl("https://github.com/CipherChaos")
        QDesktopServices.openUrl(url)

    def show_about(self):
        """Show about information."""
        QMessageBox.information(
            self,
            "About Global Clock",
            "Global Clock v2.0\n\n"
            "A beautiful world clock application with:\n"
            "• Multiple timezone support\n"
            "• Analog and Digital clock modes\n"
            "• Customizable clock styles\n"
            "• City backgrounds\n"
            "• Ticking sound effects\n\n"
            "Created with PyQt5"
        )

    def animation_loop(self):
        """Update time and trigger repaint."""
        self.local_time = get_local_time(self.selected_tz.zone)
        self.update()

    def resizeEvent(self, event):
        """Handle window resize."""
        super().resizeEvent(event)

        self.sidebar.setFixedHeight(self.height())

        # Update clock dimensions
        h_width = self.width() / 2
        h_height = self.height() / 2
        radius = h_height - 50

        self.radius_map = {
            "sec": radius - 100,
            "min": radius - 150,
            "hour": radius - 250,
            "digit": radius - 30
        }

        self.cached_size = None

    def paintEvent(self, event):
        """Paint the clock."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw background
        if self.background_image:
            if self.cached_size != self.size():
                self.cached_image = self.background_image.scaled(
                    self.width(), self.height(), Qt.KeepAspectRatioByExpanding
                )
                self.cached_size = self.size()

            if self.cached_image:
                painter.drawPixmap(0, 0, self.cached_image)

        # Draw clock
        if self.show_clock:
            if self.is_digital:
                self.renderer.draw_digital_clock(
                    painter, self.local_time, self.width(),
                    self.height(), self.current_style
                )
            else:
                # Draw clock face image
                if self.current_style:
                    size = min(self.width(), self.height()) * 0.8
                    x = self.width() / 2 - size / 2
                    y = self.height() / 2 - size / 2
                    painter.drawPixmap(int(x), int(y), int(size), int(size),
                                       self.current_style)

                # Draw clock face markers and hands
                self.renderer.draw_analog_clock(
                    painter, self.local_time, self.width(),
                    self.height(), self.radius_map
                )

    def eventFilter(self, obj, event):
        """Handle events for submenu mouse tracking."""
        if event.type() == event.Enter:
            if hasattr(obj, 'parent_menu'):
                obj.parent_menu.hide_timer.stop()
        elif event.type() == event.Leave:
            if hasattr(obj, 'parent_menu'):
                obj.parent_menu.hide_timer.start(300)
        return super().eventFilter(obj, event)
