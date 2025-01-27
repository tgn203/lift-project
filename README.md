# Elevator Simulator

This project simulates an elevator system that moves up and down, transporting passengers between floors. The default configuration includes 10 floors and 1 elevator, but users can specify the number of floors and elevators through a configuration file.

## Project Structure

```
elevator-simulator
├── src
│   ├── main.py          # Entry point of the application
│   ├── elevator.py      # Elevator class for managing movement and passengers
│   ├── building.py      # Building class for managing floors and elevators
│   ├── passenger.py     # Passenger class representing individuals in the system
│   ├── config
│   │   └── settings.py  # Configuration settings for the simulation
│   └── algorithms
│       └── __init__.py  # Package for future elevator algorithms
├── config.json          # Configuration file for floors and elevators
├── requirements.txt     # List of dependencies for the project
└── README.md            # Documentation for the project
```

## Getting Started

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd elevator-simulator
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Configure the simulation:**
   Edit the `config.json` file to specify the number of floors and elevators.

4. **Run the simulation:**
   ```
   python src/main.py
   ```

## Future Development

This project is designed to allow for the implementation of various elevator algorithms. Future updates will include additional features and optimizations based on algorithm performance comparisons.