from datetime import timedelta


MODE_NOOLITE = 'noolite'
MODE_NOOLITE_F = 'noolite-f'

MODES_NOOLITE = [MODE_NOOLITE, MODE_NOOLITE_F]

BATTERY_LEVEL_NORMAL = 100
BATTERY_LEVEL_LOW = 20
BATTERY_LEVEL_DISCHARGED = 0

DOMAIN = 'noolite'

CONF_CHANNEL = "channel"
CONF_MAX_CHANNEL_TO_SCAN = "max_ch_for_scan"
CONF_MODULE_ID = "module_id"
CONF_BROADCAST = "broadcast"

MEASUREMENT_PERCENTS = "%"

DEFAULT_PORT = '/dev/ttyUSB0'

_SCAN_INTERVAL = timedelta(seconds=60)

_TYPE_LIGHT = 'light'
_TYPE_DIMMER = 'dimmer'
_TYPE_RGB_LED = 'rgb_led'

_TYPE_TEMP = 'temp'
_TYPE_HUMI = 'humi'
_TYPE_ANALOG = 'analog'
_TYPE_REMOTE = 'remote'

_BATTERY_DATA_INTERVAL = 6 * 60 * 60
