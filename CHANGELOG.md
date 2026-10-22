# Changelog

## 3.0.0

- Rename the motion firmware layout and YAML example from `airquality-motion` to `motion`.
- Replace duplicated per-firmware YAML examples with one root `secrets-template.yaml`; remove the `examples/` directory.

- Generate only shared credential/connection `secrets.h` for every model; remove firmware layout selection, hardware schemas, and simulator generation. Leave fixed `config.h` files untouched and ignore legacy hardware YAML fields. Update examples and regression coverage.

- Add `water-level` layout and YAML example with configurable input GPIO (default 17) and active-high polarity (default true), plus rendering, validation, and CLI tests.
- Rename the layout/example to `airquality-airpressure` and remove the obsolete Grove air-quality GPIO from motion configuration.
- Rename the barometer layout and example to `co2-airpressure` for the combined SCD43/BME688 firmware.
- Add the ADS1115 `ph` firmware layout, YAML example, and configurable calibration-button GPIO (default 17).
- Remove the obsolete DHT data-pin configuration from `lux-temp-hum`, which now uses the I2C SHT45 sensor on the shared SDA/SCL pins.
- Rename the `dht-light` firmware layout and example to `lux-temp-hum`.
- Generate project-specific GPIO definitions, including I2C SDA/SCL, for all six Arduino firmwares and the ESP-IDF MCP9600 simulator.
- Add optional `--firmware` selection while preserving `--model` as the device identity and retaining legacy YAML defaults.
- Validate GPIO values and require positive thermostat cooling rise-check durations.
- Add firmware YAML examples and automated CLI/rendering regression tests in CI.
- Include both Jinja2 header templates in built packages so the installed CLI can render configurations.