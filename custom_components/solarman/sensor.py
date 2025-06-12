from __future__ import annotations

import logging

from typing import Any

from homeassistant.util import slugify
from homeassistant.core import HomeAssistant
from homeassistant.const import EntityCategory
from homeassistant.components.sensor import RestoreSensor, SensorEntity, SensorDeviceClass
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import *
from .common import *
from .services import *
from .entity import SolarmanConfigEntry, create_entity, SolarmanEntity

_LOGGER = logging.getLogger(__name__)

_PLATFORM = get_current_file_name(__name__)

def _create_entity(coordinator, description, options):
    if "persistent" in description:
        return SolarmanPersistentSensor(coordinator, description)

    if "restore" in description or "ensure_increasing" in description:
        return SolarmanRestoreSensor(coordinator, description)

    if "via_device" in description:
        return SolarmanNestedSensor(coordinator, description)

    return SolarmanSensor(coordinator, description)

async def async_setup_entry(_: HomeAssistant, config_entry: SolarmanConfigEntry, async_add_entities: AddEntitiesCallback) -> bool:
    _LOGGER.debug(f"async_setup_entry: {config_entry.options}")

    async_add_entities(create_entity(lambda x: _create_entity(config_entry.runtime_data, x, config_entry.options), d) for d in postprocess_descriptions(config_entry.runtime_data, _PLATFORM))

    async_add_entities([create_entity(lambda _: SolarmanIntervalSensor(config_entry.runtime_data), None)])

    return True

async def async_unload_entry(_: HomeAssistant, config_entry: SolarmanConfigEntry) -> bool:
    _LOGGER.debug(f"async_unload_entry: {config_entry.options}")

    return True

class SolarmanSensorEntity(SolarmanEntity, SensorEntity):
    def __init__(self, coordinator, sensor):
        super().__init__(coordinator, sensor)
        if "state_class" in sensor and (state_class := sensor["state_class"]):
            self._attr_state_class = state_class

class SolarmanIntervalSensor(SolarmanSensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator, {"key": "update_interval_sensor", "name": "Update Interval"})
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_native_unit_of_measurement = "s"
        self._attr_state_class = "duration"
        self._attr_icon = "mdi:update"
        self._attr_native_value = 0

    @property
    def available(self) -> bool:
        return self._attr_native_value is not None

    def update(self):
        self.set_state(self.coordinator.device.state.updated_interval.total_seconds())

class SolarmanSensor(SolarmanSensorEntity):
    def __init__(self, coordinator, sensor):
        super().__init__(coordinator, sensor)
        self._sensor_ensure_increasing = "ensure_increasing" in sensor

class SolarmanNestedSensor(SolarmanSensorEntity):
    def __init__(self, coordinator, sensor):
        super().__init__(coordinator, sensor)
        parent_device_info = self.coordinator.device.device_info.get(self.coordinator.device.config.config_entry.entry_id)
        device_serial_number, _ = self.coordinator.data[slugify(' '.join(filter(None, (sensor["group"], "serial", "number", "sensor"))))]
        if not device_serial_number in self.coordinator.device.device_info:
            self.coordinator.device.device_info[device_serial_number] = build_device_info(None, str(device_serial_number), None, None, None, parent_device_info["name"])
            self.coordinator.device.device_info[device_serial_number]["via_device"] = (DOMAIN, parent_device_info.get("serial_number", self.coordinator.device.config.config_entry.entry_id))
            self.coordinator.device.device_info[device_serial_number]["manufacturer"] = parent_device_info["manufacturer"]
            self.coordinator.device.device_info[device_serial_number]["model"] = None
        self._attr_device_info = self.coordinator.device.device_info[device_serial_number]
        self._attr_name.replace(f"{sensor["group"]} ", '')

class SolarmanRestoreSensor(SolarmanSensor, RestoreSensor):
    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()

        if (last_sensor_data := await self.async_get_last_sensor_data()) is not None:
            self._attr_native_value = last_sensor_data.native_value

    def set_state(self, state, value = None) -> bool:
        if self._sensor_ensure_increasing and self._attr_native_value is not None and state is not None and self._attr_native_value > state > 0:
            return False
        return super().set_state(state, value)

class SolarmanPersistentSensor(SolarmanRestoreSensor):
    @property
    def available(self) -> bool:
        return True
