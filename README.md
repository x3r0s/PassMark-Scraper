# passmark-scraper

PassMark (<https://cpubenchmark.net/cpu_list.php>) parser

## Installation

1. Clone this project repository:

  ```bash
  [git clone <https://github.com/x3r0s/passmark-scraper.git>](https://github.com/x3r0s/PassMark-Scraper.git)
  ```

2. Navigate to the project folder:

  ```bash
  cd passmark-scraper
  ```

3. Install the required packages:
  
  ```bash
  pip install -r requirements.txt
  ```

## Usage

Run the main script:

```bash
python main.py
```

You will be prompted with the following options:

```plaintext
Choose a format to save the CPU data:
1: CSV
2: JSON
3: SQL
4: ALL

Enter the number corresponding to your choice:
```

The data will be saved in the `./data` directory according to your selected option.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
