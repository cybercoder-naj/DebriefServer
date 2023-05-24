# Debrief Server

Flask app to serve F1 season and Race details along with images comparing driver lap times and more.
Some responses will be taken directly from [Ergast](http://ergast.com/mrd/), while the images with telemetry 
data will be processed from the [FastF1](https://docs.fastf1.dev/index.html) python library.

## API Reference

#### Get Race Schedule

```http
  GET /race-schedule/<year>
```

## Contributing

Contributions are always welcome!

See [`contributing.md`](contributing.md) for ways to get started.


## License

[MIT](LICENSE)


## Authors

- [@cybercoder-naj](https://www.github.com/cybercoder-naj)