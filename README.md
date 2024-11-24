# Workflow Scheduling Coursework

### About
This program is designed to find a schedule the execution of a serverless workflow DAG on a single machine. 

---
### Pre-installation

In order to run the program, you'll need to install python virtual environment. You can follow the following steps:

1. **Clone this GitHub Repository to your local machine:**
    ```sh
    git clone git@github.com:Will-JacKnight/Scheduling.git
    ```

2. **Navigate to the root directory of this project:**
    ```sh
    cd /path/to/this/project
    ```

3.	**Create a virtual environment:**
    ```sh
    python3 -m venv venv
    ```
    This creates a virtual environment in a folder named venv within your project directory. You can name it something else if you prefer.

4.	**Activate the virtual environment:**
    * On Windows:
        ```sh
        venv\Scripts\activate
        ```
    * On macOS or Linux:
        ```sh
        source venv/bin/activate
        ```

5.	**Install the required pre-requisites:**
    ```sh
    pip install -r requirements.txt
    ```

---
### User Instruction
To test with the this program, if all prerequisites are installed properly, simply run the 'src/main.py' file and results for both algorithms will display on the CLI.

1. Intermediate scheduling results display control
Turn off the partial schedule results display by setting the value of `printEachIteration` to `False`, which is set to `True` by default.

2. Modify parameters for Tabu Search
Vary different values of K (maximum number of iterations), L (Tabu List length) and gamma (tolerance) by assigning different values in `find_schedule` parameter list.


---
### Other useful information about this codebase
 - This program is designed to be scalable, where DAG structure and algorithms are defined as modular classes, both of them can be swapped easily.
 - The details of jobs are stored in the "data/data.xlsx", while the precedence relationship of jobs (DAG) is defined in "main.py" as an edge variable, for easy implementation.
 - Both LCL and Tabu Search algorithms are defined as single classes in "src/algorithm.py", where you will find switching algorithms fairly easy.

---
 ### Credits
This project is developed by Wang, Jiankai and Huang, Yile.
Special thanks to Casale, Giuliano and Paccagnan, Dario.
