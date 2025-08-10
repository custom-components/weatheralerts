"""Constants for weatheralerts integration."""

DOMAIN = "weatheralerts"
VERSION = "2025.7.0"

# Configuration keys
CONF_ZONE = "zone"
CONF_COUNTY = "county"
CONF_ZONE_NAME = "zone_name"
CONF_NAME = "name"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"
CONF_ENTITY_NAME = "entity_name"
CONF_MARINE_ZONES = "marine_zones"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_API_TIMEOUT = "api_timeout"
CONF_DEDUPLICATE_ALERTS = "deduplicate_alerts"

# Icon config keys for options flow
CONF_EVENT_ICONS = "event_icons"
CONF_DEFAULT_ICON = "default_icon"

# API endpoints
ALERTS_API = "https://api.weather.gov/alerts/active?zone={}"
ZONE_API = "https://api.weather.gov/zones/public/{}"
COUNTY_API = "https://api.weather.gov/zones/county/{}"
POINTS_API = "https://api.weather.gov/points/{},{}"
MARINE_API = "https://api.weather.gov/zones/marine/{}"

# HTTP headers for API requests
HEADERS = {
    "accept": "application/json",
    "user-agent": f"HomeAssistant_weatheralerts/{VERSION}",
}

# Valid NWS code regex for all alert zone/county/marine codes (e.g. WIZ013, WIC087, LMZ043)
NWS_CODE_REGEX = r"^(A[KLMNRSZ]|C[AOT]|D[CE]|F[LM]|G[AMU]|I[ADLN]|K[SY]|L[ACEHMOS]|M[ADEHINOPST]|N[CDEHJMVY]|O[HKR]|P[AHKMRSWZ]|S[CDL]|T[NX]|UT|V[AIT]|W[AIVY]|[HR]I)[CZ]\d{3}$"

# Defaults for update_interval and timeout options (in seconds)
DEFAULT_UPDATE_INTERVAL = 90
DEFAULT_API_TIMEOUT = 20
MIN_UPDATE_INTERVAL = 30
MAX_UPDATE_INTERVAL = 600
MIN_API_TIMEOUT = 10
MAX_API_TIMEOUT = 60
TIMEOUT_BUFFER = 5  # Minimum difference between update interval and timeout
DEFAULT_DEDUPLICATE_ALERTS = False

# Default icon for unknown/other event types
DEFAULT_EVENT_ICON = "hass:alert-rhombus"

# Default mapping of alert "event" to icon (case preserved, but match case-insensitively)
DEFAULT_EVENT_ICONS = {
    '911 Telephone Outage Emergency': 'hass:phone-alert',
    'Administrative Message': 'hass:message-text',
    'Air Quality Alert': 'hass:blur',
    'Air Stagnation Advisory': 'hass:blur',
    'Arroyo And Small Stream Flood Advisory': 'hass:water-alert',
    'Ashfall Advisory': 'hass:cloud-alert',
    'Ashfall Warning': 'hass:cloud-alert',
    'Avalanche Advisory': 'hass:alert',
    'Avalanche Warning': 'hass:alert',
    'Avalanche Watch': 'hass:alert',
    'Beach Hazards Statement': 'hass:beach',
    'Blizzard Warning': 'hass:snowflake-alert',
    'Blizzard Watch': 'hass:snowflake-alert',
    'Blowing Dust Advisory': 'hass:blur',
    'Blowing Dust Warning': 'hass:blur',
    'Brisk Wind Advisory': 'hass:weather-windy',
    'Child Abduction Emergency': 'hass:human-male-child',
    'Civil Danger Warning': 'hass:image-filter-hdr',
    'Civil Emergency Message': 'hass:image-filter-hdr',
    'Coastal Flood Advisory': 'hass:waves',
    'Coastal Flood Statement': 'hass:waves',
    'Coastal Flood Warning': 'hass:waves',
    'Coastal Flood Watch': 'hass:waves',
    'Dense Fog Advisory': 'hass:weather-fog',
    'Dense Smoke Advisory': 'hass:smoke',
    'Dust Advisory': 'hass:blur',
    'Dust Storm Warning': 'hass:blur',
    'Earthquake Warning': 'hass:alert',
    'Evacuation - Immediate': 'hass:exit-run',
    'Excessive Heat Warning': 'hass:thermometer-plus',
    'Excessive Heat Watch': 'hass:thermometer-plus',
    'Extreme Cold Warning': 'hass:thermometer-minus',
    'Extreme Cold Watch': 'hass:thermometer-minus',
    'Extreme Fire Danger': 'hass:fire-alert',
    'Extreme Wind Warning': 'hass:weather-windy',
    'Fire Warning': 'hass:fire-alert',
    'Fire Weather Watch': 'hass:fire-alert',
    'Flash Flood Statement': 'hass:water-alert',
    'Flash Flood Warning': 'hass:water-alert',
    'Flash Flood Watch': 'hass:water-alert',
    'Flood Advisory': 'hass:water-alert',
    'Flood Statement': 'hass:water-alert',
    'Flood Warning': 'hass:water-alert',
    'Flood Watch': 'hass:water-alert',
    'Freeze Warning': 'hass:thermometer-minus',
    'Freeze Watch': 'hass:thermometer-minus',
    'Freezing Fog Advisory': 'hass:snowflake-alert',
    'Freezing Rain Advisory': 'hass:snowflake-alert',
    'Freezing Spray Advisory': 'hass:snowflake-alert',
    'Frost Advisory': 'hass:snowflake-alert',
    'Gale Warning': 'hass:weather-windy',
    'Gale Watch': 'hass:weather-windy',
    'Hard Freeze Warning': 'hass:thermometer-minus',
    'Hard Freeze Watch': 'hass:thermometer-minus',
    'Hazardous Materials Warning': 'hass:radioactive',
    'Hazardous Seas Warning': 'hass:sail-boat',
    'Hazardous Seas Watch': 'hass:sail-boat',
    'Hazardous Weather Outlook': 'hass:message-alert',
    'Heat Advisory': 'hass:thermometer-plus',
    'Heavy Freezing Spray Warning': 'hass:snowflake-alert',
    'Heavy Freezing Spray Watch': 'hass:snowflake-alert',
    'High Surf Advisory': 'hass:surfing',
    'High Surf Warning': 'hass:surfing',
    'High Wind Warning': 'hass:weather-windy',
    'High Wind Watch': 'hass:weather-windy',
    'Hurricane Force Wind Warning': 'hass:weather-hurricane',
    'Hurricane Force Wind Watch': 'hass:weather-hurricane',
    'Hurricane Local Statement': 'hass:weather-hurricane',
    'Hurricane Warning': 'hass:weather-hurricane',
    'Hurricane Watch': 'hass:weather-hurricane',
    'Hydrologic Advisory': 'hass:message-text',
    'Hydrologic Outlook': 'hass:message-text',
    'Ice Storm Warning': 'hass:snowflake-alert',
    'Lake Effect Snow Advisory': 'hass:snowflake-alert',
    'Lake Effect Snow Warning': 'hass:snowflake-alert',
    'Lake Effect Snow Watch': 'hass:snowflake-alert',
    'Lake Wind Advisory': 'hass:weather-windy',
    'Lakeshore Flood Advisory': 'hass:waves-arrow-up',
    'Lakeshore Flood Statement': 'hass:waves-arrow-up',
    'Lakeshore Flood Warning': 'hass:waves-arrow-up',
    'Lakeshore Flood Watch': 'hass:waves-arrow-up',
    'Law Enforcement Warning': 'hass:car-emergency',
    'Local Area Emergency': 'hass:alert',
    'Low Water Advisory': 'hass:wave',
    'Marine Weather Statement': 'hass:sail-boat',
    'Nuclear Power Plant Warning': 'hass:radioactive',
    'Radiological Hazard Warning': 'hass:biohazard',
    'Red Flag Warning': 'hass:fire-alert',
    'Rip Current Statement': 'hass:surfing',
    'Severe Thunderstorm Warning': 'hass:weather-lightning',
    'Severe Thunderstorm Watch': 'hass:weather-lightning',
    'Severe Weather Statement': 'hass:message-text',
    'Shelter In Place Warning': 'hass:account-box',
    'Short Term Forecast': 'hass:message-text',
    'Small Craft Advisory': 'hass:sail-boat',
    'Small Craft Advisory For Hazardous Seas': 'hass:sail-boat',
    'Small Craft Advisory For Rough Bar': 'hass:sail-boat',
    'Small Craft Advisory For Winds': 'hass:sail-boat',
    'Small Stream Flood Advisory': 'hass:water-alert',
    'Snow Squall Warning': 'hass:snowflake-alert',
    'Special Marine Warning': 'hass:sail-boat',
    'Special Weather Statement': 'hass:message-alert',
    'Storm Surge Warning': 'hass:waves-arrow-up',
    'Storm Surge Watch': 'hass:waves-arrow-up',
    'Storm Warning': 'hass:weather-lightning',
    'Storm Watch': 'hass:weather-lightning',
    'Test': 'hass:message-text',
    'Tornado Warning': 'hass:weather-tornado',
    'Tornado Watch': 'hass:weather-tornado',
    'Tropical Depression Local Statement': 'hass:weather-hurricane',
    'Tropical Storm Local Statement': 'hass:weather-hurricane',
    'Tropical Storm Warning': 'hass:weather-hurricane',
    'Tropical Storm Watch': 'hass:weather-hurricane',
    'Tsunami Advisory': 'hass:waves-arrow-up',
    'Tsunami Warning': 'hass:waves-arrow-up',
    'Tsunami Watch': 'hass:waves-arrow-up',
    'Typhoon Local Statement': 'hass:weather-hurricane',
    'Typhoon Warning': 'hass:weather-hurricane',
    'Typhoon Watch': 'hass:weather-hurricane',
    'Urban And Small Stream Flood Advisory': 'hass:home-flood',
    'Volcano Warning': 'hass:image-filter-hdr',
    'Wind Advisory': 'hass:weather-windy',
    'Wind Chill Advisory': 'hass:thermometer-minus',
    'Wind Chill Warning': 'hass:thermometer-minus',
    'Wind Chill Watch': 'hass:thermometer-minus',
    'Winter Storm Warning': 'hass:snowflake-alert',
    'Winter Storm Watch': 'hass:snowflake-alert',
    'Winter Weather Advisory': 'hass:snowflake-alert',
}
