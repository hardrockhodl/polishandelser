from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

# Anpassa denna funktion för att passa din komponents konfigurationsmekanism
async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up PolisenEventSensor based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]['coordinator']

    # Skapa en sensor för varje händelse i koordinatorns data
    # Antag att koordinatorns data är en lista med händelser
    async_add_entities(
        PolisenEventSensor(coordinator, idx) for idx, _ in enumerate(coordinator.data)
    )

class PolisenEventSensor(CoordinatorEntity):
    """En sensor som visar information om en händelse från Polisen."""

    def __init__(self, coordinator, idx):
        """Initiera sensorn."""
        super().__init__(coordinator)
        self.idx = idx
        self._attr_name = f"Polisen Event {idx}"
        self._attr_unique_id = f"polisen_event_{idx}"

    @property
    def state(self):
        """Returnera tillståndet för sensorn. Används för att visa i UI."""
        event = self.coordinator.data[self.idx]
        return event.get('name', 'Okänd händelse')

    @property
    def extra_state_attributes(self):
        """Returnera ytterligare attribut för sensorn."""
        event = self.coordinator.data[self.idx]
        return {
            "summary": event.get('summary', 'Ingen sammanfattning tillgänglig'),
            # Lägg till fler attribut här om så önskas
        }

       
