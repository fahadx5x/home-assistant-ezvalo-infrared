"""Config flow for the EZVALO Infrared integration."""

from typing import Any, override

import voluptuous as vol

from homeassistant.components.infrared import (
    DOMAIN as INFRARED_DOMAIN,
    async_get_emitters,
)
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import EntitySelector, EntitySelectorConfig

from .const import CONF_INFRARED_ENTITY_ID, DOMAIN


class EzvaloInfraredConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EZVALO Infrared."""

    VERSION = 1

    def _emitter_name(self, entity_id: str) -> str:
        """Return a human readable name for an infrared emitter entity."""
        if (entry := er.async_get(self.hass).async_get(entity_id)) is not None:
            return entry.name or entry.original_name or entity_id
        return entity_id

    def _emitter_schema(self, emitter_entity_ids: list[str]) -> vol.Schema:
        """Return the emitter selection schema."""
        return vol.Schema(
            {
                vol.Required(CONF_INFRARED_ENTITY_ID): EntitySelector(
                    EntitySelectorConfig(
                        domain=INFRARED_DOMAIN,
                        include_entities=emitter_entity_ids,
                    )
                )
            }
        )

    @override
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step: choose the infrared emitter."""
        emitter_entity_ids = async_get_emitters(self.hass)
        if not emitter_entity_ids:
            return self.async_abort(reason="no_emitters")

        errors: dict[str, str] = {}

        if user_input is not None:
            infrared_entity_id = user_input.get(CONF_INFRARED_ENTITY_ID)

            if infrared_entity_id in emitter_entity_ids:
                self._async_abort_entries_match(
                    {CONF_INFRARED_ENTITY_ID: infrared_entity_id}
                )
                return self.async_create_entry(
                    title=(
                        "EZVALO Infrared via "
                        f"{self._emitter_name(infrared_entity_id)}"
                    ),
                    data={CONF_INFRARED_ENTITY_ID: infrared_entity_id},
                )

            errors["base"] = "invalid_emitter"

        return self.async_show_form(
            step_id="user",
            data_schema=self._emitter_schema(emitter_entity_ids),
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle reconfiguration: change the infrared emitter."""
        entry = self._get_reconfigure_entry()

        emitter_entity_ids = async_get_emitters(self.hass)
        if not emitter_entity_ids:
            return self.async_abort(reason="no_emitters")

        errors: dict[str, str] = {}

        if user_input is not None:
            infrared_entity_id = user_input.get(CONF_INFRARED_ENTITY_ID)

            if infrared_entity_id in emitter_entity_ids:
                self._async_abort_entries_match(
                    {CONF_INFRARED_ENTITY_ID: infrared_entity_id}
                )
                return self.async_update_reload_and_abort(
                    entry,
                    title=(
                        "EZVALO Infrared via "
                        f"{self._emitter_name(infrared_entity_id)}"
                    ),
                    data={CONF_INFRARED_ENTITY_ID: infrared_entity_id},
                )

            errors["base"] = "invalid_emitter"

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self.add_suggested_values_to_schema(
                self._emitter_schema(emitter_entity_ids), entry.data
            ),
            errors=errors,
        )
