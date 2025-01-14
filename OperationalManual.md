# Creating a Virtual Environment for Python Projects

Follow these steps to create a virtual environment named `project_name` in the `src` folder for Python coding practices:

1. **Navigate to the Project Directory**
    ```sh
    cd /path/to/your/project/src
    ```

2. **Create the Virtual Environment**
    ```sh
    python3 -m venv project_name
    ```

3. **Activate the Virtual Environment**
    - On macOS and Linux:
        ```sh
        source project_name/bin/activate
        ```
    - On Windows:
        ```sh
        project_name\Scripts\activate
        ```

4. **Install Required Packages**
    ```sh
    pip install -r requirements.txt
    ```

5. **Deactivate the Virtual Environment**
    ```sh
    deactivate
    ```

6. **Add `project_name` to `.gitignore`**
    ```sh
    echo "src/project_name/" >> .gitignore
    ```

By following these steps, you will have a dedicated virtual environment for your Python project, ensuring that dependencies are managed and isolated.