"""Constants for the EZVALO Infrared integration."""

from enum import IntEnum

DOMAIN = "ezvalo_infrared"

CONF_INFRARED_ENTITY_ID = "infrared_entity_id"

# Protocol confirmed by capturing the physical EZVALO remote:
# Extended NEC, raw address bytes 0x86 0x73 -> 16-bit address 0x7386, 38 kHz.
EZVALO_ADDRESS = 0x7386
EZVALO_MODULATION = 38000

# Name of the single device that groups every entity of this integration.
DEVICE_NAME = "EZVALO Infrared Light"

MANUFACTURER = "EZVALO"
MODEL = "EZVALO motion light (Extended NEC 0x7386)"


class EzvaloCommand(IntEnum):
    """Confirmed EZVALO Extended NEC command bytes."""

    ON = 0x03
    OFF = 0x98

    DAY = 0xA2
    NIGHT = 0xE2

    BRIGHTNESS_DOWN = 0x90
    BRIGHTNESS_UP = 0xE0

    COOL = 0xD0
    NEUTRAL = 0x50
    WARM = 0x78

    TIMER_15 = 0x10
    TIMER_30 = 0x38
    TIMER_60 = 0x5A
    TIMER_90 = 0x42
    TIMER_120 = 0x4A
    TIMER_CANCEL = 0x52


# Operating mode select.
# NOTE: "Always On" transmits 0x03, the same key as the light's ON command,
# so selecting it also switches the light on. "Day Motion" / "Night Motion"
# only change the motion behaviour of the light.
OPERATING_MODES: list[str] = ["Always On", "Day Motion", "Night Motion"]

OPERATING_MODE_COMMANDS: dict[str, EzvaloCommand] = {
    "Always On": EzvaloCommand.ON,
    "Day Motion": EzvaloCommand.DAY,
    "Night Motion": EzvaloCommand.NIGHT,
}


# Color temperature select.
COLOR_TEMPERATURES: list[str] = ["Cool", "Neutral", "Warm"]

COLOR_TEMPERATURE_COMMANDS: dict[str, EzvaloCommand] = {
    "Cool": EzvaloCommand.COOL,
    "Neutral": EzvaloCommand.NEUTRAL,
    "Warm": EzvaloCommand.WARM,
}


# Buttons: unique id suffix -> (entity name, IR command).
BUTTONS: dict[str, tuple[str, EzvaloCommand]] = {
    "brightness_up": ("EZVALO Brightness Up", EzvaloCommand.BRIGHTNESS_UP),
    "brightness_down": ("EZVALO Brightness Down", EzvaloCommand.BRIGHTNESS_DOWN),
    "timer_15": ("EZVALO Timer 15", EzvaloCommand.TIMER_15),
    "timer_30": ("EZVALO Timer 30", EzvaloCommand.TIMER_30),
    "timer_60": ("EZVALO Timer 60", EzvaloCommand.TIMER_60),
    "timer_90": ("EZVALO Timer 90", EzvaloCommand.TIMER_90),
    "timer_120": ("EZVALO Timer 120", EzvaloCommand.TIMER_120),
    "timer_cancel": ("EZVALO Cancel Timer", EzvaloCommand.TIMER_CANCEL),
}
