# tuya-vacuum (porklabz fork)

> **Este é um fork mantido de [jaidenlabelle/tuya-vacuum](https://github.com/jaidenlabelle/tuya-vacuum).**
> O mantenedor original não está fazendo merge de Pull Requests há vários meses.
> Este fork aplica [jaidenlabelle/tuya-vacuum#7](https://github.com/jaidenlabelle/tuya-vacuum/pull/7)
> (fix de CI) e outras correções pendentes, para manter a lib instalável e a
> integração [tuya-vacuum-maps](https://github.com/porklabz/tuya-vacuum-maps)
> funcionando.

tuya-vacuum is a python library to view maps from Tuya robot vacuums.

## Installation
Instale direto deste fork via pip + git:

```bash
pip install "tuya-vacuum @ git+https://github.com/porklabz/tuya-vacuum-alternative.git@v0.1.9-1"
```

## Usage
```python
from tuya_vacuum import TuyaVacuum

# Create a new TuyaVacuum instance
vacuum = TuyaVacuum(
    origin="https://openapi.tuyaus.com",
    client_id="<Client ID>",
    client_secret="<Client Secret>",
    device_id="<Device ID>"
)

# Parse the map data
vacuum_map = vacuum.fetch_realtime_map()

# Save the map as an image
image = vacuum_map.to_image()
image.save("output.png")
```

## Compatability List

This is a list of all currently tested devices. Create a new [issue](https://github.com/porklabz/tuya-vacuum-alternative/issues) to add your device.

| Device                                                | Support                           |
| ----------------------------------------------------- | --------------------------------- |
| [Lefant M1](https://www.lefant.com/en-ca/products/m1) | <text style="color:lightgreen">Supported</text> |
| Kabum Robô Aspirador de Pó 700                        | <text style="color:lightgreen">Supported</text> |

## Special Thanks
- [Jaiden Labelle](https://github.com/jaidenlabelle) for the original `tuya-vacuum` library
- [Tuya Cloud Vacuum Map Extractor](https://github.com/oven-lab/tuya_cloud_map_extractor) by [@oven-lab](https://github.com/oven-lab)
