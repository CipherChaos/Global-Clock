from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve

from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QFrame, \
    QGraphicsOpacityEffect


class HorizontalSubMenu(QFrame):
    """A horizontal submenu that appears to the right of a parent widget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Setup layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(2)

        # Styling
        self.setStyleSheet("""
            HorizontalSubMenu {
                background-color: rgba(40, 40, 40, 240);
                border: 1px solid rgba(100, 149, 237, 180);
                border-radius: 8px;
                padding: 5px;
            }
        """)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(0)
        self.setGraphicsEffect(self.opacity_effect)

        self.opacity_animation = QPropertyAnimation(self.opacity_effect,
                                                    b"opacity")
        self.opacity_animation.setDuration(200)
        self.opacity_animation.setEasingCurve(QEasingCurve.InOutQuad)

    def show_menu(self, parent_widget):
        """Show the submenu positioned to the right of the parent widget."""
        if not parent_widget:
            return

        global_pos = parent_widget.mapToGlobal(parent_widget.rect().topRight())

        self.move(global_pos.x() + 5, global_pos.y())

        self.opacity_animation.stop()
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)
        self.opacity_animation.start()

        self.show()

    def hide_menu(self):
        """Hide the submenu with animation."""
        self.opacity_animation.stop()
        self.opacity_animation.setStartValue(1)
        self.opacity_animation.setEndValue(0)
        self.opacity_animation.start()

        QTimer.singleShot(200, self.hide)

    def add_item(self, text, callback):
        btn = QPushButton(text)
        btn.setFixedHeight(35)
        btn.setMinimumWidth(150)
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(30, 30, 30, 210);
                color: white;
                border: none;
                padding: 6px 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: rgba(50, 50, 50, 230);
            }
            QPushButton:pressed {
                background-color: rgba(20, 20, 20, 240);
            }
            """)

        btn.clicked.connect(lambda checked=False, t=text: callback(t))
        self.layout.addWidget(btn)
        return btn
