# Process Discovery using Alpha Algorithm

## Overview

This project implements **Process Discovery** using the **Alpha Algorithm**. The Alpha Algorithm is a foundational process mining technique used to derive a **Petri net** from an event log, capturing the underlying business process model.

## Features

- **Event Log Processing**: Parses event logs to extract unique activities and traces.
- **Alpha Algorithm Implementation**: Discovers the **causal** relationships between activities.
- **Petri Net Construction**: Generates a **Petri net** representation of the discovered process.
- **Graph Visualization**: Displays the extracted process model.

## Requirements

- Python 3.8+
- Required Libraries:
  - `numpy`
  - `pandas`
  - `networkx`
  - `matplotlib`
  - `pm4py` (for process mining utilities)

Install dependencies using:

```sh
pip install numpy pandas networkx matplotlib pm4py
```

## Usage

1. **Prepare Event Log**

   - Ensure the event log is in CSV format with at least two columns: `case_id` and `activity`.
   - Example format:
     | case\_id | activity | timestamp        |
     | -------- | -------- | ---------------- |
     | 1        | A        | 2024-03-09 10:00 |
     | 1        | B        | 2024-03-09 10:05 |
     | 1        | C        | 2024-03-09 10:10 |

2. **Run the Alpha Algorithm**

   ```sh
   python alpha_algorithm.py event_log.csv
   ```

3. **Visualize the Process Model**

   - The discovered **Petri net** will be saved as an image and displayed.

## Output

- **Petri Net Representation**: A graphical view of the discovered process.
- **Dependency Graph**: Shows activity transitions and their relations.


## References

- [Process Mining: Discovery, Conformance, and Enhancement of Business Processes - Wil van der Aalst](https://www.springer.com/gp/book/9783662565092)
- [PM4Py - Process Mining for Python](https://pm4py.fit.fraunhofer.de/)

