"""Select platform for the EZVALO Infrared integration."""

from typing import override

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import (
    COLOR_TEMPERATURE_COMMANDS,
    COLOR_TEMPERATURES,
    CONF_INFRARED_ENTITY_ID,
    OPERATING_MODE_COMMANDS,
    OPERATING_MODES,
)
from .entity import EzvaloInfraredEntity

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the select platform from a config entry."""
    if not (infrared_entity_id := entry.data.get(CONF_INFRARED_ENTITY_ID)):
        return

    async_add_entities(
        [
            EzvaloOperatingModeSelect(entry, infrared_entity_id),
            EzvaloColorTemperatureSelect(entry, infrared_entity_id),
        ]
    )


class EzvaloOperatingModeSelect(EzvaloInfraredEntity, SelectEntity):
    """Operating mode of the EZVALO light: Always On / Day Motion / Night Motion.

    Selecting "Always On" transmits 0x03, the same key as the light's ON
    command, so it also switches the light on.
    """

    _attr_name = "EZVALO Operating Mode"
    _attr_options = OPERATING_MODES
    _attr_current_option: str | None = None

    def __init__(self, entry: ConfigEntry, infrared_entity_id: str) -> None:
        """Initialize the operating mode select entity."""
        super().__init__(entry, infrared_entity_id)
        self._attr_unique_id = f"{entry.entry_id}_operating_mode"

    @override
    async def async_select_option(self, option: str) -> None:
        """Send the IR command for the selected operating mode."""
        await self._send_ezvalo_command(OPERATING_MODE_COMMANDS[option])
        self._attr_current_option = option
        self.async_write_ha_state()


class EzvaloColorTemperatureSelect(EzvaloInfraredEntity, SelectEntity):
    """Color temperature of the EZVALO light: Cool / Neutral / Warm."""

    _attr_name = "EZVALO Color Temperature"
    _attr_options = COLOR_TEMPERATURES
    _attr_current_option: str | None = None

    def __init__(self, entry: ConfigEntry, infrared_entity_id: str) -> None:
        """Initialize the color temperature select entity."""
        super().__init__(entry, infrared_entity_id)
        self._attr_unique_id = f"{entry.entry_id}_color_temperature"

    @override
    async def async_select_option(self, option: str) -> None:
        """Send the IR command for the selected color temperature."""
        await self._send_ezvalo_command(COLOR_TEMPERATURE_COMMANDS[option])
        self._attr_current_option = option
        self.async_write_ha_state()
