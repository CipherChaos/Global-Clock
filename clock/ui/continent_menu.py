from PyQt5.QtCore import Qt, QTimer

from PyQt5.QtWidgets import QPushButton

from PyQt5.QtGui import QCursor

from clock.ui.submenu import HorizontalSubMenu


class ContinentMenuItem(QPushButton):
    """A continent menu item with horizontal submenu on hover."""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.submenu = None
        self.items = {}

        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(45)

        # Styling
        self.setStyleSheet("""

            QPushButton {
                background-color: rgba(60, 60, 60, 180);
                border: none;
                color: white;
                text-align: left;
                padding-left: 25px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 4px;
                margin: 2px 5px;
            }
            QPushButton:hover {
                background-color: rgba(100, 149, 237, 150);
            }
        """)

        # Timer for delayed hide
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self._on_hide_timer)

    def set_submenu_items(self, items_dict):
        """Set the items for the submenu."""
        self.items = items_dict

        # Create submenu
        self.submenu = HorizontalSubMenu(self.window())

        # Add items to submenu
        for city, timezone in items_dict.items():
            self.submenu.add_item(city, self._on_city_selected)

    def _on_city_selected(self, city):
        """Handle city selection."""
        self.submenu.hide_menu()
        if hasattr(self.window(), 'set_timezone'):
            self.window().set_timezone(city)

    def enterEvent(self, event):
        """Show submenu on hover."""
        super().enterEvent(event)
        self.hide_timer.stop()

        if self.submenu and self.items:
            self.submenu.show_menu(self)

    def leaveEvent(self, event):
        super().leaveEvent(event)

        if self.submenu and self.submenu.isVisible():
            submenu_geo = self.submenu.geometry()

            # Get current mouse position in global coordinates
            mouse_pos = QCursor.pos()

            if not submenu_geo.contains(mouse_pos):
                self.hide_timer.start(300)
        else:
            self.hide_timer.start(300)

    def _on_hide_timer(self):
        """Hide submenu when timer expires."""
        if self.submenu:
            self.submenu.hide_menu()

    def hide_submenu(self):
        """Force hide submenu."""
        if self.submenu:
            self.submenu.hide_menu()
