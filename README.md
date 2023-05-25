# Debrief Server

Flask app to serve F1 season and Race details along with images comparing driver lap times and more.
Some responses will be taken directly from [Ergast](http://ergast.com/mrd/), while the images with telemetry 
data will be processed from the [FastF1](https://docs.fastf1.dev/index.html) python library.

## API Reference

#### Get Race Schedule

```http
  GET /race-schedule/<year>
```

| Parameter | Type  | Description                                 |
|:----------|:------|:--------------------------------------------|
| `year`    | `int` | Year for desired race schedule.             |

#### Get Line Graph Image for Fastest Laps

```http
  GET /fastest-laps/line-graph
```

| Parameter | Type        | Description                                                                     |
|:----------|:------------|:--------------------------------------------------------------------------------|
| `x`       | `string`    | Field for x-axis: `Speed`, `RPM`, `nGear`, `Throttle`, `Brake`, `DRS`.          |
| `y`       | `string`    | Field for y-axis: `Speed`, `RPM`, `nGear`, `Throttle`, `Brake`, `DRS`.          |
| `gp`      | `string`    | Name of the circuit.                                                            |
| `year`    | `int`       | Year of the F1 Season.                                                          |
| `drivers` | `list[str]` | Comma-separated(,) list of drivers to compare. Use driver code in block letters |

## Contributing

Contributions are always welcome!

See [`contributing.md`](contributing.md) for ways to get started.


## License

[MIT](LICENSE)


## Authors

- [@cybercoder-naj](https://www.github.com/cybercoder-naj)