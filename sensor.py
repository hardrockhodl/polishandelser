from homeassistant.helpers.entity import Entity
from .const import DOMAIN

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    # Använd `hass.data[DOMAIN]` för att komma åt konfigurationsdata
    ort = hass.data[DOMAIN]["ort"]
    antal_events = hass.data[DOMAIN]["antal_events"]

    # Skapa och lägg till dina sensorer. Exempel:
    async_add_entities([PolisenEventSensor(ort, antal_events)], True)

class PolisenEventSensor(Entity):
    """Exempelsensor för Polisens händelser."""

    def __init__(self, ort, antal_events):
        """Initialize the sensor."""
        self._ort = ort
        self._antal_events = antal_events
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Polisen Events"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        # Här skulle du hämta ny data baserat på `self._ort` och `self._antal_events`
        # och uppdatera `self._state` med den nya informationen.
        pass

       
