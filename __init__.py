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

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional("ort", default="Åre"): cv.string,
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
    scan_interval = conf[CONF_SCAN_INTERVAL]

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

async def fetch_police_events(hass, location='Åre', events_limit=5):
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


