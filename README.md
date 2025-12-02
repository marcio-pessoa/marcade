# MArcade

Márcio's Arcade games

## Changes

All notable changes to this project will be documented in this [Change log](CHANGELOG.yaml).

## Installing

### Cloning

``` sh
git clone https://github.com/marcio-pessoa/marcade.git
```

### Installing SO dependencies

On Ubuntu:

``` sh
sudo apt install portaudio19-dev python3-all-dev
```

On Mac:

``` sh
brew install portaudio
```

### Installing required Python modules

``` sh
cd marcade

pip3 install -r requirements.txt
```

## Usage

To start a random game:

``` sh
./marcade.py
```

To start a game (ie: Invasion):

``` sh
./marcade.py invasion
```

For help:

``` sh
./marcade.py -h
```

## Games available

### Invasion

Based on memorable Space Invaders

[![Invasion](Screenshots/invasion.png)](Documents/invasion.md)

### Pongue

Based on classic Pong

[![Pongue](Screenshots/pongue.png)](Documents/pongue.md)

### Rocks

Based on amazing Asteroids

[![Rocks](Screenshots/rocks.png)](Documents/rocks.md)

### Serpent

Based on the fun Snake

[![Rocks](Screenshots/serpent.png)](Documents/serpent.md)

### 2048

Based on the addictive 2048

[![2048](Screenshots/2048.png)](Documents/2048.md)

## Contributing

Changes and improvements are more than welcome! Feel free to fork and open a pull request. Please make your changes in a specific branch and request to pull into `main`! If you can, please make sure the game fully works before sending the Pull Request, as that will help speed up the process.


Make sure your contribution meets the [Functionality and Code Quality Criteria](#functionality-and-code-quality-criteria).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Functionality and Code Quality Criteria

Make sure every development contribution meets the following functionality and code quality criteria.

Pylint:

```sh
pylint $(find . -name "*.py")
```

Flake8:

```sh
flake8 . --count --statistics
```

pytest:

```sh
./run_tests.sh
```

Bandit:

```sh
bandit --recursive marcade.py src games
```

## License

Licensed under the [GPLv2](LICENSE).

## Donations

I made this in my spare time, and it's hosted on GitHub, but if you enjoyed the game and feel like buying me coffee, you can donate at GitHub at [GitHub Sponsors](https://github.com/sponsors/marcio-pessoa) or my PayPal: <marcio.pessoa@gmail.com>. Thank you very much!
