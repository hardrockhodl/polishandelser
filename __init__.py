from datetime import timedelta
import voluptuous as vol
import aiohttp
import asyncio
import logging
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.const import CONF_SCAN_INTERVAL
from .const import DOMAIN
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

DOMAIN = "polishandelser"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional("ort", default="Stockholm"): cv.string,
                vol.Optional("antal_events", default=5): cv.positive_int,
                vol.Optional(CONF_SCAN_INTERVAL, default=3600): cv.positive_int,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Polisen Events component."""
    conf = config[DOMAIN]
    ort = conf["ort"]
    antal_events = conf["antal_events"]
    #The Swedish Police API can ban your IP if you poll more then every 10 seconds.
    scan_interval = conf[CONF_SCAN_INTERVAL]
    async def async_retrieve_events():
        """Hämta händelser från Polisens API."""
        try:
            events = await fetch_police_events(hass, ort, antal_events)
            return events
        except Exception as e:
            raise UpdateFailed(f"Error fetching events: {e}")

    coordinator = DataUpdateCoordinator(
        hass,
        logging.getLogger(__name__),
        name="polis_händelser",
        update_method=async_retrieve_events,
        update_interval=timedelta(seconds=scan_interval),
    )

    # Starta första uppdateringen manuellt
    await coordinator.async_refresh()

    hass.data[DOMAIN] = {
        "ort": ort,
        "antal_events": antal_events,
        "scan_interval": scan_interval,
    }

    # Lägg till kod här för att initiera din uppdateringslogik, exempelvis:
    async_track_time_interval(
        hass,
        lambda now: update_events(hass, ort, antal_events),
        timedelta(seconds=scan_interval),
    )

    return True

async def fetch_police_events(hass, location='Stockholm', events_limit=5):
    url = f"https://polisen.se/api/events?locationname={location}"
    session = async_get_clientsession(hass)
    try:
        async with session.get(url) as response:
            if response.status == 200:
                events = await response.json()
                return events[:events_limit]
            else:
                logging.error("Failed to fetch data from Polisen API")
                return []
    except Exception as e:
        logging.error(f"Error fetching data from Polisen API: {e}")
        return []

async def update_events(hass, ort, antal_events):
    """Hämta uppdateringar från Polisens API och uppdatera Home Assistant-entiteter."""
    events = await fetch_police_events(hass, ort, antal_events)
    if events:
        # Här kan du uppdatera dina Home Assistant-entiteter med den nya datan.
        pass
    else:
        logging.info("Inga händelser att visa.")

