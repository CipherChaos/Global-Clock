import math

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QFont, QColor, QPainterPath

from clock.config import ClockConfig
from clock.utils import deg_to_rad


class ClockRenderer:
    """Handles all clock rendering logic."""

    def __init__(self):
        self.clock_60 = {i: i * 6 for i in range(60)}

    def draw_analog_face(self, painter, width, height, radius_map):
        """Draw the analog clock face with markers."""
        painter.save()
        h_width = width / 2
        h_height = height / 2

        for digit, angle in self.clock_60.items():
            radius = 2
            if digit % 15 == 0:
                radius = 20
            elif digit % 5 == 0:
                radius = 8

            pos = self._get_clock_position(digit, angle, h_width, h_height,
                                           radius_map["digit"])
            painter.drawEllipse(pos, radius, radius)

        painter.restore()

    @staticmethod
    def draw_sword_hand(painter, color, angle, length, base_width,
                        tip_length, center_x, center_y):
        """Draw a modern sword-shaped clock hand."""
        painter.save()

        # Translate and rotate
        painter.translate(center_x, center_y)
        painter.rotate(angle - 180)

        path = QPainterPath()

        base_half = base_width / 2

        path.moveTo(-base_half, 0)
        path.lineTo(-base_half * 0.3, length - tip_length)
        path.lineTo(0, length)
        path.lineTo(base_half * 0.3, length - tip_length)
        path.lineTo(base_half, 0)

        path.closeSubpath()

        # Draw
        painter.setPen(QPen(color.darker(120), 1))
        painter.setBrush(QBrush(color))
        painter.drawPath(path)

        painter.setPen(QPen(color.lighter(130), 2))
        painter.drawLine(0, 0, 0, int(length * 0.7))

        painter.restore()

    def draw_analog_clock(self, painter, local_time, width, height,
                          radius_map):
        """Draw complete analog clock with sword-shaped hands."""
        painter.save()

        h_width = width / 2
        h_height = height / 2

        # Calculate angles
        hour = local_time.hour % 12
        hour_angle = hour * 30 + local_time.minute * 0.5
        minute_angle = local_time.minute * 6
        second_angle = local_time.second * 6

        # Draw hour hand (shortest, thickest)
        self.draw_sword_hand(
            painter,
            ClockConfig.HOUR_HAND_COLOR,
            hour_angle,
            radius_map["hour"],
            16,  # base width
            40,  # tip length
            h_width,
            h_height
        )

        # Draw minute hand (medium)
        self.draw_sword_hand(
            painter,
            ClockConfig.MINUTE_HAND_COLOR,
            minute_angle,
            radius_map["min"],
            12,  # base width
            50,  # tip length
            h_width,
            h_height
        )

        # Draw second hand (longest, thinnest)
        self.draw_sword_hand(
            painter,
            ClockConfig.SECOND_HAND_COLOR,
            second_angle,
            radius_map["sec"],
            6,  # base width
            30,  # tip length
            h_width,
            h_height
        )

        # Draw center circle
        painter.setBrush(QBrush(ClockConfig.HOUR_HAND_COLOR))
        painter.setPen(QPen(Qt.white, 2))
        painter.drawEllipse(QPointF(h_width, h_height), 8.0, 8.0)

        painter.restore()

    @staticmethod
    def draw_digital_clock(painter, local_time, width, height,
                           style_pixmap):
        """Draw digital clock display."""
        font = QFont("Arial", 100, QFont.Bold)
        font.setStyleHint(QFont.SansSerif)
        painter.setFont(font)

        time_str = local_time.strftime("%H:%M:%S")
        painter.setPen(QPen(Qt.white))

        pixmap = style_pixmap.scaled(600, 300, Qt.KeepAspectRatio)

        x = int(width / 2 - 300)
        y = int(height / 2 - 110)
        painter.drawPixmap(x, y, pixmap)

        # Draw time text
        painter.setPen(QPen(QColor(30, 30, 30), 5))
        painter.setBrush(Qt.transparent)

        text_x = x + (pixmap.width() - painter.fontMetrics().horizontalAdvance(
            time_str)) / 2
        text_y = y + (pixmap.height() + painter.fontMetrics().height()) / 2.5

        painter.drawText(int(text_x), int(text_y), time_str)

    @staticmethod
    def _get_clock_position(digit, angle, h_width, h_height, radius):
        """Calculate position on clock face."""
        angle_rad = deg_to_rad(angle - 90)
        x = h_width + radius * math.cos(angle_rad)
        y = h_height + radius * math.sin(angle_rad)
        return QPointF(x, y)
