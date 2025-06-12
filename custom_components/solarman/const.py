from datetime import timedelta as td

DOMAIN = "solarman"

IP_BROADCAST = "<broadcast>"
IP_ANY = "0.0.0.0"

PORT_ANY = 0

DISCOVERY_PORT = 48899
DISCOVERY_TIMEOUT = .5
DISCOVERY_MESSAGE = ["WIFIKIT-214028-READ".encode(), "HF-A11ASSISTHREAD".encode()]

COMPONENTS_DIRECTORY = "custom_components"

LOOKUP_DIRECTORY = "inverter_definitions"
LOOKUP_DIRECTORY_PATH = f"{COMPONENTS_DIRECTORY}/{DOMAIN}/{LOOKUP_DIRECTORY}/"

CONF_HOST = "host"
CONF_PORT = "port"
CONF_TRANSPORT = "transport"
CONF_LOOKUP_FILE = "lookup_file"
CONF_ADDITIONAL_OPTIONS = "additional_options"
CONF_MB_SLAVE_ID = "mb_slave_id"

OLD_ = { "name": "name", "serial": "inverter_serial", "sn": "serial", "sn": "sn", CONF_HOST: "inverter_host", CONF_PORT: "inverter_port" }

SUGGESTED_VALUE = "suggested_value"
UPDATE_INTERVAL = "update_interval"
IS_SINGLE_CODE = "is_single_code"
REGISTERS_CODE = "registers_code"
REGISTERS_MIN_SPAN = "registers_min_span"
REGISTERS_MAX_SIZE = "registers_max_size"
DIGITS = "digits"

DEFAULT_ = {
    "name": "",
    CONF_MB_SLAVE_ID: 1,
    UPDATE_INTERVAL: 15,
    IS_SINGLE_CODE: False,
    REGISTERS_CODE: 0x03,
    REGISTERS_MIN_SPAN: 25,
    REGISTERS_MAX_SIZE: 125,
    DIGITS: 6
}

PARAM_ = { }

TIMINGS_INTERVAL = 5
TIMINGS_INTERVAL_SCALE = 1
TIMINGS_UPDATE_INTERVAL = td(seconds = TIMINGS_INTERVAL * TIMINGS_INTERVAL_SCALE)

REQUEST_UPDATE_INTERVAL = UPDATE_INTERVAL
REQUEST_MIN_SPAN = "min_span"
REQUEST_MAX_SIZE = "max_size"
REQUEST_CODE = "code"
REQUEST_CODE_ALT = "mb_functioncode"
REQUEST_START = "start"
REQUEST_END = "end"
REQUEST_COUNT = "count"

SERVICES_PARAM_DEVICE = "device"
SERVICES_PARAM_ADDRESS = "address"
SERVICES_PARAM_COUNT = "count"
SERVICES_PARAM_VALUE = "value"
SERVICES_PARAM_VALUES = "values"

SERVICE_READ_HOLDING_REGISTERS = "read_holding_registers"
SERVICE_READ_INPUT_REGISTERS = "read_input_registers"
SERVICE_WRITE_SINGLE_REGISTER = "write_single_register"
SERVICE_WRITE_MULTIPLE_REGISTERS = "write_multiple_registers"

SERVICES_PARAM_REGISTER = "register"
SERVICES_PARAM_QUANTITY = "quantity"

DATETIME_FORMAT = "%y/%m/%d %H:%M:%S"
TIME_FORMAT = "%H:%M"