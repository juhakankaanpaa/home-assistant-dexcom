"""Support for Dexcom sensors."""
from homeassistant.const import CONF_UNIT_OF_MEASUREMENT, CONF_USERNAME, STATE_UNKNOWN
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, GLUCOSE_TREND_ICON, GLUCOSE_VALUE_ICON, MG_DL


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Dexcom sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    username = config_entry.data[CONF_USERNAME]
    unit_of_measurement = config_entry.data[CONF_UNIT_OF_MEASUREMENT]
    sensors = []
    sensors.append(DexcomGlucoseTrendSensor(coordinator, username))
    sensors.append(DexcomGlucoseValueSensor(coordinator, username, unit_of_measurement))
    async_add_entities(sensors, False)


class DexcomGlucoseValueSensor(Entity):
    """Representation of a Dexcom glucose value sensor."""

    def __init__(self, coordinator, username, unit_of_measurement):
        """Initialize the sensor."""
        self._state = None
        self._unit_of_measurement = unit_of_measurement
        self._attribute_unit_of_measurement = (
            "mg_dl" if unit_of_measurement == MG_DL else "mmol_l"
        )
        self._coordinator = coordinator
        self._name = f"{DOMAIN}_{username}_glucose_value"
        self._unique_id = f"{username}-value"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon for the frontend."""
        return GLUCOSE_VALUE_ICON

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of the device."""
        return self._unit_of_measurement

    @property
    def state(self):
        """Return the state of the sensor."""
        return (
            getattr(self._coordinator.data, self._attribute_unit_of_measurement)
            if self._coordinator.data
            else STATE_UNKNOWN
        )

    @property
    def available(self):
        """Return True if entity is available."""
        return bool(self._coordinator.data)

    @property
    def should_poll(self):
        """Return False, updates are controlled via coordinator."""
        return False

    @property
    def unique_id(self):
        """Device unique id."""
        return self._unique_id

    async def async_update(self):
        """Get the latest state of the sensor."""
        await self._coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self._coordinator.async_add_listener(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """When entity will be removed from hass."""
        self._coordinator.async_remove_listener(self.async_write_ha_state)


class DexcomGlucoseTrendSensor(Entity):
    """Representation of a Dexcom glucose trend sensor."""

    def __init__(self, coordinator, username):
        """Initialize the sensor."""
        self._state = None
        self._coordinator = coordinator
        self._name = f"{DOMAIN}_{username}_glucose_trend"
        self._unique_id = f"{username}-trend"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon for the frontend."""
        return (
            GLUCOSE_TREND_ICON[self._coordinator.data.trend]
            if self._coordinator.data
            else GLUCOSE_TREND_ICON[0]
        )

    @property
    def state(self):
        """Return the state of the sensor."""
        return (
            self._coordinator.data.trend_description
            if self._coordinator.data
            else STATE_UNKNOWN
        )

    @property
    def available(self):
        """Return True if entity is available."""
        return bool(self._coordinator.data)

    @property
    def should_poll(self):
        """Return False, updates are controlled via coordinator."""
        return False

    @property
    def unique_id(self):
        """Device unique id."""
        return self._unique_id

    async def async_update(self):
        """Get the latest state of the sensor."""
        await self._coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self._coordinator.async_add_listener(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """When entity will be removed from hass."""
        self._coordinator.async_remove_listener(self.async_write_ha_state)
