"""Light platform for the EZVALO Infrared integration."""

from typing import Any, override

from homeassistant.components.light import ColorMode, LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_INFRARED_ENTITY_ID, EzvaloCommand
from .entity import EzvaloInfraredEntity

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the light platform from a config entry."""
    if not (infrared_entity_id := entry.data.get(CONF_INFRARED_ENTITY_ID)):
        return

    async_add_entities([EzvaloLight(entry, infrared_entity_id)])


class EzvaloLight(EzvaloInfraredEntity, LightEntity):
    """Representation of the EZVALO light."""

    # The EZVALO light sends only blind IR commands and reports no state back.
    _attr_assumed_state = True
    _attr_color_mode = ColorMode.ONOFF
    _attr_name = "EZVALO Light"
    _attr_supported_color_modes = {ColorMode.ONOFF}

    def __init__(self, entry: ConfigEntry, infrared_entity_id: str) -> None:
        """Initialize the EZVALO light."""
        super().__init__(entry, infrared_entity_id)
        self._attr_unique_id = f"{entry.entry_id}_light"
        # Optimistic local state: stays unknown until the first ON/OFF command
        # is sent, because the device never reports its real state back.
        self._attr_is_on: bool | None = None

    @override
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the EZVALO light on (ON = 0x03)."""
        await self._send_ezvalo_command(EzvaloCommand.ON)
        self._attr_is_on = True
        self.async_write_ha_state()

    @override
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the EZVALO light off (OFF = 0x98)."""
        await self._send_ezvalo_command(EzvaloCommand.OFF)
        self._attr_is_on = False
        self.async_write_ha_state()
