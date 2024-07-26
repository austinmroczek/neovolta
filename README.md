# WARNING
[!CAUTION]
The NeoVolta custom integration for HACS is broken and not maintained. Instead use the [SolarMan MQTT Add-on](https://github.com/austinmroczek/addon-solarman-mqtt).  

# NeoVolta

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

_Integration to integrate [NeoVolta](https://www.neovolta.com) solar home batteries with [Home Assistant](https://www.home-assistant.io)._

## This is a work in progress
**You are likely to encounter errors and missing functionality.**

So far this integration has only been tested on one battery in one configuration.

Battery | Network | Tested
-- | -- | --
NV14 | Wired | Yes
NV14 | Wifi | No
NV24 | Wired | No
NV24 | Wifi | No

Please report [issues](https://github.com/austinmroczek/neovolta/issues).

## Platforms

This integration will set up the following platforms. While many of the measurements are clearly of a particular type (voltage, frequency, etc) we do not have a full mapping to specific items shown in the Solarman app, so some items are named "TBD" or "Voltage1" until we know what they are.

Platform | Type | Description
-- | -- | --
`sensor` | Battery | Current percentage of overall battery, or battery pack that is available.
`sensor` | Total Energy | Various measurements of total energy in kiloWatt hours.
`sensor` | Frequency | Frequency in Hertz
`sensor` | Voltage | Current voltage of various components.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `neovolta`.
1. Download _all_ the files from the `custom_components/neovolta/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "NeoVolta"

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[neovolta]: https://github.com/austinmroczek/neovolta
[commits-shield]: https://img.shields.io/github/commit-activity/y/austinmroczek/neovolta.svg?style=for-the-badge
[commits]: https://github.com/austinmroczek/neovolta/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/austinmroczek/neovolta.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Austin%20Mroczek%20%40austinmroczek-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/austinmroczek/neovolta.svg?style=for-the-badge
[releases]: https://github.com/austinmroczek/neovolta/releases
