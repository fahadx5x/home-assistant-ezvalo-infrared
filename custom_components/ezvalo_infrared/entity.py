"""Base entity for the EZVALO Infrared integration.

Every entity of this integration sends Extended NEC commands through an
``infrared`` emitter entity, so every entity inherits from
``InfraredEmitterConsumerEntity`` (which tracks emitter availability and owns
the ``_send_command`` helper) and stores the chosen emitter in
``self._infrared_emitter_entity_id``.
"""

from infrared_protocols.commands.nec import NECCommand

from homeassistant.components.infrared import InfraredEmitterConsumerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from .const import (
    DEVICE_NAME,
    DOMAIN,
    EZVALO_ADDRESS,
    EZVALO_MODULATION,
    MANUFACTURER,
    MODEL,
)


class EzvaloInfraredEntity(InfraredEmitterConsumerEntity):
    """Base entity for all EZVALO Infrared entities."""

    # Entity names are set explicitly on each entity (EZVALO Light,
    # EZVALO Operating Mode, ...), so no device-name prefix is used.
    _attr_has_entity_name = False

    def __init__(self, entry: ConfigEntry, infrared_entity_id: str) -> None:
        """Initialize the EZVALO Infrared entity."""
        self._entry = entry
        self._infrared_emitter_entity_id = infrared_entity_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=DEVICE_NAME,
            manufacturer=MANUFACTURER,
            model=MODEL,
        )

    async def _send_ezvalo_command(self, command: int) -> None:
        """Send one confirmed EZVALO command through the infrared emitter."""
        await self._send_command(
            NECCommand(
                address=EZVALO_ADDRESS,
                command=command,
                modulation=EZVALO_MODULATION,
            )
        )
