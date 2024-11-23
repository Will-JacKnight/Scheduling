# Workflow Scheduling Coursework

### About
This program is designed to find a schedule the execution of a serverless workflow DAG on a single machine. 

---
### Pre-installation

In order to run the program, you'll need to install python virtual environment. You can follow the following steps:

1. **Navigate to the root directory of this project:**
    ```sh
    cd /path/to/this/project
    ```

2.	**Create a virtual environment:**
    ```sh
    python3 -m venv venv
    ```
    This creates a virtual environment in a folder named venv within your project directory. You can name it something else if you prefer.

3.	**Activate the virtual environment:**
    * On Windows:
        ```sh
        venv\Scripts\activate
        ```
    * On macOS or Linux:
        ```sh
        source venv/bin/activate
        ```

4.	**Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

---
### User Instruction
To manipulate with the algorithm, simply run the 'src/main.py' file. 

---
### Other useful information about this codebase
 - The structure of the DAG graph is stored in the data/ directory.
 - The data of nodes is imported in the graph.py class.
 - Algorithm is defined as a single class in src/algorithm.py, where you will find scaling the program fairly easy.
 - 

---
 ### Author
Wang, Jiankai  
Huang, Yile  
Special thanks to Casale, Giuliano and Paccagnan, Dario.