# EZVALO Infrared for Home Assistant

Unofficial Home Assistant custom integration for compatible EZVALO infrared motion lights.

It uses Home Assistant's native **Infrared** framework and sends the original remote-control commands through a compatible `infrared.*` emitter.

> [!IMPORTANT]
> This project is unofficial and is not affiliated with, endorsed by, or supported by EZVALO.

## Features

The integration exposes:

- Light power: **On / Off**
- Operating mode:
  - Always On
  - Day Motion
  - Night Motion
- Color temperature:
  - Cool
  - Neutral
  - Warm
- Brightness Up
- Brightness Down
- Timers:
  - 15 minutes
  - 30 minutes
  - 60 minutes
  - 90 minutes
  - 120 minutes
  - Cancel Timer

## Requirements

- Home Assistant **2026.8.0 or newer**
- A compatible Home Assistant `infrared.*` emitter
- An EZVALO light using the supported infrared protocol

This integration was developed and tested with Home Assistant's native Infrared framework.

## Installation

### HACS

Until the repository is available in the default HACS catalog:

1. Open **HACS**
2. Open the menu in the top-right corner
3. Select **Custom repositories**
4. Add:

   `https://github.com/fahadx5x/home-assistant-ezvalo-infrared`

5. Select **Integration**
6. Install **EZVALO Infrared**
7. Restart Home Assistant

### Manual installation

Copy:

`custom_components/ezvalo_infrared`

to:

`<config>/custom_components/ezvalo_infrared`

Then restart Home Assistant.

## Configuration

1. Go to **Settings → Devices & services**
2. Select **Add Integration**
3. Search for **EZVALO Infrared**
4. Select the infrared emitter that can reach your EZVALO light

No YAML configuration is required.

## Infrared protocol

The supported remote was captured and decoded as:

- Protocol: **Extended NEC**
- Address: `0x7386`
- Carrier frequency: **38 kHz**

Confirmed command bytes:

| Function | Command |
| --- | --- |
| On | `0x03` |
| Off | `0x98` |
| Day Motion | `0xA2` |
| Night Motion | `0xE2` |
| Brightness Down | `0x90` |
| Brightness Up | `0xE0` |
| Cool | `0xD0` |
| Neutral | `0x50` |
| Warm | `0x78` |
| Timer 15 | `0x10` |
| Timer 30 | `0x38` |
| Timer 60 | `0x5A` |
| Timer 90 | `0x42` |
| Timer 120 | `0x4A` |
| Cancel Timer | `0x52` |

## State behavior

Infrared communication is one-way.

The EZVALO light does not report its current state back to Home Assistant, so the integration uses **assumed/optimistic state**. If the physical remote is used outside Home Assistant, the displayed state can differ from the actual light state.

Brightness is intentionally exposed as **Up / Down buttons** instead of a percentage because the remote protocol does not provide absolute brightness feedback.

## Supported hardware

Support is based on the infrared protocol above rather than only the product name.

Other EZVALO models may use different infrared codes and are not guaranteed to work.

## Issues

If you find a compatible or incompatible EZVALO model, or encounter a problem, please open an issue:

https://github.com/fahadx5x/home-assistant-ezvalo-infrared/issues

## License

MIT License.
