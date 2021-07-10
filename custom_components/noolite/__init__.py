"""
Support for NooLite.
"""
import logging

import voluptuous as vol
from homeassistant.const import CONF_PORT
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.helpers import config_validation as cv

from .base_devices import *
from .const import *


_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.string,
    }),
}, extra=vol.ALLOW_EXTRA)

PLATFORM_SCHEMA = vol.Schema({
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up the connection to the NooLite device."""

    from NooLite_F.MTRF64 import MTRF64Controller
    from serial import SerialException

    try:
        hass.data[DOMAIN] = MTRF64Controller(config[DOMAIN][CONF_PORT])
    except SerialException as exc:
        _LOGGER.error("Unable to open serial port for NooLite: %s", exc)
        return False
    except KeyError as exc:
        _LOGGER.error("Configuration for NooLite component doesn't found: %s", exc)
        return False

    for ch_id in range(11):
        try:
            from NooLite_F import ModuleMode
            responses = hass.data[DOMAIN].read_state(None, ch_id, False, ModuleMode.NOOLITE_F)
            _LOGGER.warning("Channel: %i state -> %s", ch_id, str(responses))
            responses = hass.data[DOMAIN].read_module_config(None, ch_id, False, ModuleMode.NOOLITE_F)
            _LOGGER.warning("Channel: %i config -> %s", ch_id, str(responses))
        except:
            _LOGGER.exception("Got exception while scanning noolite-f channels")

    def _release_noolite():
        hass.data[DOMAIN].release()

    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, _release_noolite)

    return True
