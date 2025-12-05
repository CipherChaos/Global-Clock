import os
import sys

from PyQt5.QtGui import QColor


from pathlib import Path

def resource_path(relative_path):
    base_path = Path(__file__).resolve().parent
    return (base_path / relative_path).as_posix()



class ClockConfig:
    """Centralized configuration for the clock application."""

    # Window settings
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080
    WINDOW_TITLE = "Global Clock"

    # Animation settings
    FPS = 60

    # Sound files
    SOUND_FILES = [
        resource_path("medias/sounds/Ticking-1.mp3"),
        resource_path("medias/sounds/Ticking-2.mp3"),
        resource_path("medias/sounds/Ticking-3.mp3"),
    ]

    # Time zones grouped by continent
    TIME_ZONES_BY_CONTINENT = {
        "Europe": {
            "London": "Europe/London",
            "Paris": "Europe/Paris",
            "Berlin": "Europe/Berlin",
            "Rome": "Europe/Rome",
            "Moscow": "Europe/Moscow",
            "Athens": "Europe/Athens"
        },
        "Asia": {
            "Tokyo": "Asia/Tokyo",
            "Dubai": "Asia/Dubai",
            "Shanghai": "Asia/Shanghai",
            "Mumbai": "Asia/Kolkata",
            "Seoul": "Asia/Seoul",
            "Bangkok": "Asia/Bangkok",
            "Tehran": "Asia/Tehran"
        },
        "North America": {
            "New York": "America/New_York",
            "Toronto": "America/Toronto",
            "Mexico City": "America/Mexico_City"
        },
        "Australia": {
            "Sydney": "Australia/Sydney"
        }
    }

    TIME_ZONES = {}
    for continent in TIME_ZONES_BY_CONTINENT.values():
        TIME_ZONES.update(continent)

    # Background images
    CITY_IMAGES = {
        "London": resource_path("medias/backgrounds/London-clock-tower.jpg"),
        "New York": resource_path("medias/backgrounds/New-York.jpg"),
        "Paris": resource_path("medias/backgrounds/Paris.jpg"),
        "Tokyo": resource_path("medias/backgrounds/Tokyo.jpg"),
        "Sydney": resource_path("medias/backgrounds/Sydney.jpg"),
        "Berlin": resource_path("medias/backgrounds/Berlin.jpg"),
        "Dubai": resource_path("medias/backgrounds/Dubai.jpg"),
        "Rome": resource_path("medias/backgrounds/Rome.jpg"),
        "Moscow": resource_path("medias/backgrounds/Moscow.jpg"),
        "Shanghai": resource_path("medias/backgrounds/Shanghai.jpg"),
        "Mumbai": resource_path("medias/backgrounds/Mumbai.jpg"),
        "Toronto": resource_path("medias/backgrounds/Toronto.jpg"),
        "Mexico City": resource_path("medias/backgrounds/Mexico-city.jpg"),
        "Seoul": resource_path("medias/backgrounds/Seoul.jpg"),
        "Bangkok": resource_path("medias/backgrounds/Bangkok.jpg"),
        "Athens": resource_path("medias/backgrounds/Athens.jpg"),
        "Tehran": resource_path("medias/backgrounds/Tehran.jpg")
    }

    # Analog clock styles
    ANALOG_STYLES = {
        "Billiard": resource_path(
            "medias/analog_styles/Billiard-modified.png"),
        "Blue-neon": resource_path(
            "medias/analog_styles/Blue-neon-modified.png"),
        "Modern-pilot": resource_path(
            "medias/analog_styles/Modern-Pilot-modified.png"),
        "Omega": resource_path(
            "medias/analog_styles/Omega-Black-Gold-modified.png"),
        "Porsche": resource_path(
            "medias/analog_styles/Porsche-modified.png"),
        "Purple-mystery": resource_path(
            "medias/analog_styles/Purple-Mystery-modified.png"),
        "Purple-mystery-2": resource_path(
            "medias/analog_styles/Purple-Mystery-modified-2.png"),
        "Rings": resource_path("medias/analog_styles/Rings-modified.png"),
        "Rolex": resource_path("medias/analog_styles/Rolex-modified-1.png"),
        "Rolex2": resource_path("medias/analog_styles/Rolex-modified-2.png"),
        "Rolex3": resource_path("medias/analog_styles/Rolex-modified-3.png"),
        "Sun": resource_path("medias/analog_styles/Sun-modified.png"),
        "Tux": resource_path("medias/analog_styles/Tux-modified.png"),
        "Yalda": resource_path("medias/analog_styles/Yalda-modified.png"),
        "Simple_farsi": resource_path(
            "medias/analog_styles/Simple-Farsi-modified.png")
    }

    # Digital clock styles
    DIGITAL_STYLES = {
        "Aqua": resource_path("medias/digital_styles/Aqua-digital.png"),
        "Coca": resource_path("medias/digital_styles/Coca-digital.png"),
        "Emerald": resource_path(
            "medias/digital_styles/Emerald-digital.png"),
        "Gem": resource_path("medias/digital_styles/Gem-digital.png"),
        "Ocean": resource_path("medias/digital_styles/Ocean-digital.png"),
        "Red-cobalt": resource_path(
            "medias/digital_styles/Red-cobalt-digital.png"),
        "Wooden": resource_path("medias/digital_styles/Wooden-digital.png")
    }

    # Colors
    HOUR_HAND_COLOR = QColor(100, 149, 237)  # Cornflower Blue
    MINUTE_HAND_COLOR = QColor(112, 128, 144)  # Slate Gray
    SECOND_HAND_COLOR = QColor(240, 128, 128)  # Light pink
