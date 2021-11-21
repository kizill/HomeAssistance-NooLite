from .const import *

from threading import Timer

from homeassistant.helpers.entity import ToggleEntity, Entity
from typing import Optional

from homeassistant.const import CONF_NAME, CONF_MODE, ATTR_BATTERY_LEVEL
from homeassistant.const import STATE_UNKNOWN


class NooLiteGenericModule(ToggleEntity):

    @staticmethod
    def _module_mode(config):
        from NooLite_F import ModuleMode

        mode = config[CONF_MODE].lower()

        if mode == MODE_NOOLITE:
            module_mode = ModuleMode.NOOLITE
        else:
            module_mode = ModuleMode.NOOLITE_F

        return module_mode


    def __init__(self, config, device):
        self._device = device
        self._name = config[CONF_NAME]
        self._mode = NooLiteGenericModule._module_mode(config)
        self._broadcast = config[CONF_BROADCAST]
        self._module_id = config[CONF_MODULE_ID] if config[CONF_MODULE_ID] >= 0 else None
        self._channel = config[CONF_CHANNEL] if config[CONF_CHANNEL] >= 0 else None
        assert self._channel is None or self._module_id is None, "Either module_id or channel should be None"
        assert self._channel is not None or self._module_id is not None, "Either module_id or channel should be not None"
        self._state = STATE_UNKNOWN
        self._level = 0.0

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def is_on(self) -> bool:
        return self._state

    @property
    def assumed_state(self) -> bool:
        from NooLite_F import ModuleMode
        return self._mode == ModuleMode.NOOLITE

    def turn_on(self, **kwargs):
        responses = self._device.on(None, self._channel, self._broadcast, self._mode)
        if self.assumed_state:
            self._state = True
        else:
            self._update_state_from(responses)

    def turn_off(self, **kwargs):
        responses = self._device.off(None, self._channel, self._broadcast, self._mode)
        if self.assumed_state:
            self._state = False
        else:
            self._update_state_from(responses)

    def toggle(self, **kwargs) -> None:
        responses = self._device.switch(None, self._channel, self._broadcast, self._mode)
        if self.assumed_state:
            self._state = not self._state
        else:
            self._update_state_from(responses)

    def update(self):
        if not self.assumed_state:
            responses = self._device.read_state(None, self._channel, self._broadcast, self._mode)
            self._update_state_from(responses)

    def _is_module_on(self, module_state) -> bool:
        from NooLite_F import ModuleState
        return module_state.state == ModuleState.ON or module_state.state == ModuleState.TEMPORARY_ON

    def _update_state_from(self, responses):
        state = False
        level = 0.0
        for (result, info, module_state) in responses:
            if result and module_state is not None and self._is_module_on(module_state):
                state = True
                level = max(module_state.brightness, level)
        self._state = state
        self._level = level


class NooLiteGenericSensor(Entity):
    def __init__(self, config, device, battery_timeout):
        self._device = device
        self._name = config[CONF_NAME]
        self._channel = config[CONF_CHANNEL]
        self._state = None
        self._battery = None
        self._battery_timer = None
        self._battery_timeout = battery_timeout

    def action_detected(self):
        if self._battery_timer is None:
            self.normal_battery()

    def low_battery(self):
        self._battery = BATTERY_LEVEL_LOW
        self._start_battery_timer()
        self.schedule_update_ha_state()

    def normal_battery(self):
        if self._battery_timer is not None:
            self._battery_timer.cancel()
            self._battery_timer = None
        self._battery = BATTERY_LEVEL_NORMAL
        self.schedule_update_ha_state()

    def _start_battery_timer(self):
        if self._battery_timer is not None:
            self._battery_timer.cancel()
        self._battery_timer = Timer(self._battery_timeout, self._on_battery_timer)
        self._battery_timer.start()

    def _on_battery_timer(self):
        self._battery_timer = None
        self.on_battery_timeout()

    def on_battery_timeout(self):
        self._battery = BATTERY_LEVEL_DISCHARGED
        self._state = None
        self.schedule_update_ha_state()

    @property
    def battery(self):
        return self._battery

    @property
    def name(self):
        return self._name

    @property
    def should_poll(self):
        return False

    @property
    def state_attributes(self):
        attr = {
            ATTR_BATTERY_LEVEL: self._battery
        }
        return attr

    def update(self):
        pass
