"""Button platform for the EZVALO Infrared integration."""

from typing import override

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import BUTTONS, CONF_INFRARED_ENTITY_ID, EzvaloCommand
from .entity import EzvaloInfraredEntity

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the button platform from a config entry."""
    if not (infrared_entity_id := entry.data.get(CONF_INFRARED_ENTITY_ID)):
        return

    async_add_entities(
        EzvaloButton(entry, infrared_entity_id, key, name, command)
        for key, (name, command) in BUTTONS.items()
    )


class EzvaloButton(EzvaloInfraredEntity, ButtonEntity):
    """Stateless EZVALO remote button."""

    def __init__(
        self,
        entry: ConfigEntry,
        infrared_entity_id: str,
        key: str,
        name: str,
        command: EzvaloCommand,
    ) -> None:
        """Initialize the EZVALO button."""
        super().__init__(entry, infrared_entity_id)
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_name = name
        self._command = command

    @override
    async def async_press(self) -> None:
        """Send the IR command of this button."""
        await self._send_ezvalo_command(self._command)
