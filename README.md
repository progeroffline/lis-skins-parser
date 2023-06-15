
3. Prepare the JSON file:

- Create a JSON file with the desired skin data. Example format:

  ```json
  {
    "skins": [
      {
        "name": "Skin 1",
        "float": 0.123,
        "site_id": "ABC123",
        "min_price": 10.0,
        "max_price": 100.0
      },
      {
        "name": "Skin 2",
        "float": 0.456,
        "site_id": "DEF456",
        "min_price": 50.0,
        "max_price": 200.0
      },
      ...
    ]
  }
  ```

4. Configure and run the skin parser:

- Open the `parser.py` file and modify it as needed, specifying the paths to the HTML source and JSON file.
- Run the parser:

  ```
  python parser.py
  ```

- The parser will continuously monitor new skins and attempt to purchase any that match the criteria defined in the JSON file.

## Contributions

Contributions to the real-time skin parser and purchase repository are welcome. If you encounter any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.

## License

This repository is licensed under the [MIT License](LICENSE).
