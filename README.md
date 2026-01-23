# COM401-gradeAnalyser

A Python-based tool for analysing student grades and generating useful summaries.

This repository contains the **COM401-gradeAnalyser** project — a script designed to read student grade data from CSV or JSON files and produce reports or analysis based on course requirements.

---

## Features

- Parse student grades from CSV or JSON formats
- Analyse grade distributions and compute statistics
- Generate summary outputs for review or reporting
- Simple structure that is easy to extend or modify

---

## Installation

Ensure you have **Python 3.13 or higher** installed.

Clone the repository:

```bash
git clone https://github.com/Beast-Clutch/COM401-gradeAnalyser.git
cd COM401-gradeAnalyser
```

Install required dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

1. Place your grade data file (CSV or JSON) in the project directory.
2. Run the main script:

```bash
python main.py
```

3. View the output printed to the console or generated files.

Ensure the input file name matches what the script expects (e.g. `student_grades.csv` or `student_grades.json`).

---

## Project Structure

```text
.
├── .idea/                    # IDE configuration files
├── Notes/                    # Project notes and documentation
├── functions/                # Supporting Python modules
├── main.py                   # Main program entry point
├── requirements.txt          # Python dependencies
├── student_grades.csv        # Sample CSV input data
└── student_grades.json       # Sample JSON input data
```

---

## Example

```bash
python main.py
```

The program will analyse the grade data and output summary statistics.

---

## Contributing

Contributions are welcome.  
If you would like to improve this project, please fork the repository and submit a pull request.

---

## License

This project is released under the MIT License.

---

## Author

Created for the COM401 module.
