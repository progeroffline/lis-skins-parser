# Real-Time Skin Parser and Purchase

This repository contains a real-time skin parser that monitors and checks for new skins. It compares the characteristics of the skins, such as float value, skin name, site ID, and minimum/maximum price, with a JSON file. If there is a match, the parser automatically purchases the skin.

## Features

- Real-time monitoring: The parser continuously scans for new skins as they become available.
- Comparison with JSON file: The characteristics of each skin are compared with the data stored in a JSON file.
- Match detection: If there is a match based on float value, skin name, site ID, or price range, the parser identifies it.
- Automated skin purchase: When a match is found, the parser initiates the purchase process for the corresponding skin.

## Usage

To use the skin parser and purchase functionality, follow these steps:

1. Clone the repository:

```
git clone https://github.com/ProgerOffline/lis-skins-parser/
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Prepare the JSON file:

- Create a JSON file with the desired skin data. Example format:

  ```json
  {"items": [
      {
          "name": "MAG-7 | Insomnia",
          "price_max": 0.5
      },
      {
          "name": "M4A4 | Urban DDPAT (Field-Tested)",
          "price_max": 0.4,
          "stickers": [
              ["mousesports | Berlin 2019"],
              ["Tyloo | Berlin 2019"]
          ]
      },
      {
          "name": "M4A4 | Urban DDPAT (Field-Tested)",
          "price_max": 0.4,
          "phases": [
              {"seeds": [293, 292]}
          ]
      },
      {
          "name": "StatTrak™ Five-SeveN | Nightshade (Minimal Wear)",
          "price_max": 6,
          "float_min": 0.0743,
          "float_max": 0.0745
      }
      ...
  ]}
  ```

4. Configure and run the skin parser:

- Open the `app.py` file and modify it as needed, specifying the paths to the HTML source and JSON file.
- Run the parser:

  ```
  python app.py
  ```

- The parser will continuously monitor new skins and attempt to purchase any that match the criteria defined in the JSON file.

## Contributions

Contributions to the real-time skin parser and purchase repository are welcome. If you encounter any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.

## License

This repository is licensed under the [MIT License](LICENSE).
