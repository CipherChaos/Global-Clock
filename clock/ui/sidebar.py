from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve

from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QFrame

from clock.ui.continent_menu import ContinentMenuItem


class SidebarPanel(QFrame):
    """Modern sidebar menu panel with proper collapse behavior."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_expanded = False
        self.collapsed_width = 60
        self.expanded_width = 280
        self.parent = parent
        self.continent_buttons = []

        self.setFixedWidth(self.collapsed_width)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 30, 230);
                border-right: 2px solid rgba(100, 149, 237, 150);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toggle button
        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.setFixedHeight(60)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(100, 149, 237, 200);
                border: none;
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(100, 149, 237, 255);
            }
        """)
        layout.addWidget(self.toggle_btn)

        self.menu_container = QWidget()
        self.menu_container.hide()
        self.menu_layout = QVBoxLayout(self.menu_container)
        self.menu_layout.setContentsMargins(0, 10, 0, 0)
        self.menu_layout.setSpacing(2)

        layout.addWidget(self.menu_container)

        layout.addStretch()

        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.animation2 = QPropertyAnimation(self, b"maximumWidth")
        self.animation2.setDuration(300)
        self.animation2.setEasingCurve(QEasingCurve.InOutQuad)

    def add_menu_item(self, icon, title):
        """Add a menu item to the sidebar."""
        item = QPushButton(f"{icon}  {title}")
        item.setFixedHeight(50)
        item.setStyleSheet("""
            QPushButton {
                background-color: rgba(50, 50, 50, 150);
                border: none;
                color: white;
                text-align: left;
                padding-left: 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(100, 149, 237, 200);
            }
        """)
        item.setCursor(Qt.PointingHandCursor)
        self.menu_layout.addWidget(item)
        return item

    def add_continent_menu(self, continent, cities):
        """Add a continent menu with horizontal submenu."""
        continent_btn = ContinentMenuItem(f"🗺  {continent}")
        continent_btn.set_submenu_items(cities)
        self.continent_buttons.append(continent_btn)
        return continent_btn

    def toggle_sidebar(self):
        """Toggle sidebar expansion with proper visibility handling."""
        if self.is_expanded:
            # Collapse
            self.animation.setStartValue(self.expanded_width)
            self.animation.setEndValue(self.collapsed_width)
            self.animation2.setStartValue(self.expanded_width)
            self.animation2.setEndValue(self.collapsed_width)
            self.toggle_btn.setText("☰")

            self.menu_container.hide()

            for btn in self.continent_buttons:
                btn.hide_submenu()

        else:

            self.animation.setStartValue(self.collapsed_width)
            self.animation.setEndValue(self.expanded_width)
            self.animation2.setStartValue(self.collapsed_width)
            self.animation2.setEndValue(self.expanded_width)
            self.toggle_btn.setText("✕")

            self.menu_container.show()

        self.animation.start()
        self.animation2.start()
        self.is_expanded = not self.is_expanded
