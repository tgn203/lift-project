# Elevator Simulator

This project simulates an elevator system that moves up and down, transporting passengers between floors. Users can specify the number of floors and elevators through a configuration file that can be generated.

## Project Structure

```
lift-project/
├── src/
│   ├── frontend.py     # Entry point of the application
│   ├── inputread.py    # Loads configuration from files
│   ├── config.json     # JSON file for configuration (this could also be a .txt)
│   └── algs/
│       ├── ed_algorithm.py     # Ed's algorithm
│       ├── max_algorithm.py    # Max's algorithm
│       ├── scan.py             # Scan algorithm
│       └── look.py             # Look algorithm
├── static/
│   ├── images/             # Images for webpages
│   ├── scripts/            # JavaScript for each webpage
│   │   ├── animation.js
│   │   ├── config.js
│   │   ├── index.js
│   │   └── script.js       # Common scripts
│   ├── styles/             # Styling for each webpage
│   │   ├── animation.css
│   │   ├── config.css
│   │   ├── index.css
│   │   ├── style.css       # Common styles
│   │   └── variables.css   # Common styling variables
│   └── favicon.ico         # Webpage favicon
├── templates/          # HTML templates used by Flask
│   ├── algorithm.html
│   ├── animation.html
│   ├── config.html
│   └── index.html
├── tests/              # Code for generating, running and comparing tests
│   ├── test_code/
│   ├── test_data/
│   ├── test_results/
│   └── testcourse.xlsx     # Excel document for test comparisons
├── docs/
│   ├── psuedocode/     # Psuedocode for individual algorithms
│   │   ├── ed_code
│   │   ├── max_code
│   │   └── nick_code
│   └── spec/
│       ├── graph.png   # Ed's algorithm
│       ├── spec.latex  # LaTeX file to generate PDF
│       └── spec.pdf    # Submitted PDF
├── requirements.txt    # List of dependencies for the project
└── README.md           # Documentation for the project
```

## Getting Started

1. **Clone the repository:**
   ```
   git clone https://github.com/tgn203/lift-project.git
   cd lift-project/
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Configure the simulation:**
   - Edit or create the `src/config.json` file to specify the number of floors and elevators.
   - Use `python src/config_generator.py` to automatically create a random config.

4. **Run the simulation:**
   ```
   python src/frontend.py
   ```
