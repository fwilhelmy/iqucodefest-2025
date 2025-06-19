# Beginner's Guide: Setting Up Your Coding Environment & Troubleshooting

Welcome! Starting a new coding project or exercise can be exciting, but sometimes technical setup issues can be frustrating. This guide aims to help you navigate common hurdles so you can focus on learning and coding.

> **Tip:** For a quick summary, jump to the [Quick Reference: Key Setup Steps & Troubleshooting](#quick-reference-key-setup-steps--troubleshooting) at the end.

---

## Table of Contents

- [Beginner's Guide: Setting Up Your Coding Environment \& Troubleshooting](#beginners-guide-setting-up-your-coding-environment--troubleshooting)
  - [Table of Contents](#table-of-contents)
  - [1. Getting the Project Code (from GitHub)](#1-getting-the-project-code-from-github)
    - [Option 0: Download as a ZIP File](#option-0-download-as-a-zip-file)
    - [Option A: GitHub Desktop (Recommended for Beginners)](#option-a-github-desktop-recommended-for-beginners)
      - [Method 1: From the GitHub Repository Page (Easiest)](#method-1-from-the-github-repository-page-easiest)
      - [Method 2: Manually within GitHub Desktop (If the browser option doesn't work or you have the URL copied)](#method-2-manually-within-github-desktop-if-the-browser-option-doesnt-work-or-you-have-the-url-copied)
    - [Option B: Using the Command Line (Git Bash, Terminal, PowerShell)](#option-b-using-the-command-line-git-bash-terminal-powershell)
    - [Option C: Using your IDE (VS Code or PyCharm)](#option-c-using-your-ide-vs-code-or-pycharm)
    - [Option D: Using Google Colab](#option-d-using-google-colab)
  - [2. Understanding \& Using Virtual Environments](#2-understanding--using-virtual-environments)
    - [Method 1: Command Line](#method-1-command-line)
    - [Method 2: VS Code](#method-2-vs-code)
      - [**A. Creating a New Virtual Environment in VS Code**](#a-creating-a-new-virtual-environment-in-vs-code)
      - [**B. Selecting an existing virtual environment in VS Code**](#b-selecting-an-existing-virtual-environment-in-vs-code)
    - [Method 3: PyCharm](#method-3-pycharm)
    - [Common pitfall: wrong environment active](#common-pitfall-wrong-environment-active)
  - [3. Working with project files \& imports](#3-working-with-project-files--imports)
  - [4. Dealing with package version issues](#4-dealing-with-package-version-issues)
    - [Understanding `requirements.txt`](#understanding-requirementstxt)
    - [Solving version conflicts](#solving-version-conflicts)
  - [Using Jupyter Notebook/Lab with Your Virtual Environment (Shell \& IDEs)](#using-jupyter-notebooklab-with-your-virtual-environment-shell--ides)
    - [1. Install Jupyter and `ipykernel` in your virtual environment](#1-install-jupyter-and-ipykernel-in-your-virtual-environment)
    - [2. Using Jupyter Notebooks from the terminal](#2-using-jupyter-notebooks-from-the-terminal)
    - [3. Using Jupyter Notebooks Inside IDEs](#3-using-jupyter-notebooks-inside-ides)
    - [4. Verify Your Setup (in a Notebook Cell)](#4-verify-your-setup-in-a-notebook-cell)
  - [5. General troubleshooting \& FAQ](#5-general-troubleshooting--faq)
  - [Quick Reference: Key Setup Steps \& Troubleshooting](#quick-reference-key-setup-steps--troubleshooting)

---


## 1. Getting the Project Code (from GitHub)

Most projects and exercises will be hosted on GitHub. You need to get a copy of this code onto your computer. This is called "cloning" a repository.

### Option 0: Download as a ZIP File

If you just want to run the code locally and don't need updates or version control:
1. Go to the GitHub repository page.
2. Click the green "▼ Code" button, then "Download ZIP".
3. Extract the ZIP file to your computer.


### Option A: GitHub Desktop (Recommended for Beginners)

1.  **Install GitHub Desktop:** If you haven't already, download and install it from [desktop.github.com](https://desktop.github.com/). Make sure it's set up and you're logged into your GitHub account within the application if prompted.

#### Method 1: From the GitHub Repository Page (Easiest)
1.  Navigate to the GitHub repository page in your web browser (e.g., `https://github.com/some-user/their-cool-project`).
2.  Click the green "▼ Code" button.
3.  In the dropdown menu, you should see a tab for "Local". Under this tab, look for an "Open with GitHub Desktop" option. Click it.
    *   Your web browser might show a pop-up asking for permission to open GitHub Desktop. Allow it.
4.  GitHub Desktop should open automatically. The repository URL will likely be pre-filled.
5.  **Continue in GitHub Desktop:**
    *   GitHub Desktop will now show you the repository to be cloned.
    *   It will suggest a "Local Path" on your computer where the project folder will be created (e.g., `C:\Users\YourName\Documents\GitHub\their-cool-project`). You can change this if you prefer a different location.
    *   Verify the details and click the "Clone" button.
    *   Wait for the files to download. Once done, the project is on your computer!

#### Method 2: Manually within GitHub Desktop (If the browser option doesn't work or you have the URL copied)
1.  Open the GitHub Desktop application on your computer.
2.  If this is your first time or you don't have any repositories, you might see a "Clone a repository from the Internet..." option directly. Otherwise, go to "File" > "Clone repository...".
3.  In the "Clone a repository" dialog:
    *   Select the "URL" tab.
    *   Paste the GitHub repository link (e.g., `https://github.com/some-user/their-cool-project.git`). You can get this link from the repository's page by clicking the green "▼ Code" button and copying the HTTPS URL.
    *   Choose a "Local Path" on your computer where you want to save the project.
    *   Click the "Clone" button.

### Option B: Using the Command Line (Git Bash, Terminal, PowerShell)
1.  **Install Git:** If you don't have Git, download and install it from [git-scm.com](https://git-scm.com/downloads). During installation, accept the default options.
2.  **Open your terminal:**
    *   Windows: Git Bash (installed with Git), Command Prompt, or PowerShell.
    *   macOS/Linux: Terminal.
3.  **Navigate to where you want to store the project:**
    ```bash
    cd path/to/your/projects_folder
    ```
4.  **Clone the repository:**
    ```bash
    git clone https://github.com/user/project.git
    ```
    Replace the URL with the actual project URL. This will create a new folder named `project` (or whatever the repository is called).
5.  **Navigate into the project folder:**
    ```bash
    cd project
    ```

### Option C: Using your IDE (VS Code or PyCharm)

**VS Code:**
- Open Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`).
- Type `Git: Clone`, paste the repo URL, choose a folder, and open the project.

**PyCharm:**
- On the Welcome screen, click "Clone Repository" or "File" > "Project from Version Control".
- Paste the repo URL, choose a directory, and click "Clone".

---

### Option D: Using Google Colab

Google Colab is a convenient way to run Python notebooks in your browser without local setup. Here’s how to work with a project from GitHub:

**1. Open the Main Notebook from GitHub:**

*   Go to [Google Colab](https://colab.research.google.com/).
*   In the welcome pop-up or via `File > Open notebook...`, select the **GitHub** tab.
*   Paste the URL of the GitHub repository (or the direct URL to the `.ipynb` file).
*   Select the main `.ipynb` notebook file for the project and open it.


**2. Make Project Files Accessible (Clone & Set Path):**

If your opened notebook needs to import other Python files (`.py` scripts) or use data files from the *same* GitHub repository, you need to make the entire repository available.

*   **In a code cell at the top of your Colab notebook, run the following:**

    First, clone the repository (if you haven't already or if you opened the notebook directly and need other files):
    ```python
    # Replace with the actual GitHub repository URL
    !git clone https://github.com/your-username/your-repository-name.git 
    ```
    This command downloads the repository into a folder (e.g., `your-repository-name`) in your Colab session.

    Next, add this folder to Python's import path:
    ```python
    import sys
    import os

    # Replace 'your-repository-name' with the name of the folder created by git clone
    repository_folder_name = 'your-repository-name' 
    project_path = os.path.join('/content/', repository_folder_name)

    if project_path not in sys.path:
        sys.path.insert(0, project_path)
        print(f"Added {project_path} to sys.path")
    ```
    Now, your notebook can import Python files from the cloned repository.

**3. Install Required Packages:**

Projects often depend on specific Python packages. These are usually listed in a `requirements.txt` file or provided as a list.

*   **If there's a `requirements.txt` file in the repository:**
    After cloning (Step 2), navigate into the repository's directory (if needed) and install the packages using `pip`. Add a new code cell and run:
    ```python
    # Replace 'your-repository-name' with the actual folder name
    %cd /content/your-repository-name 
    !pip install -r requirements.txt
    ```
    The `%cd` command changes the current directory. Then `!pip install -r requirements.txt` installs all packages listed in that file.

*   **If you have a list of packages to install:**
    In a new code cell, run:
    ```python
    !pip install package1 package2 another-package
    ```
    Replace `package1`, `package2`, etc., with the actual names of the packages you need to install.

**4. Saving Your Work:**

When you make changes in Colab, you're working on a temporary copy.

*   **To save your notebook:**
    *   **To Google Drive (Recommended for your own copies):** `File > Save a copy in Drive`
    *   **To GitHub (If you want to suggest changes or save to your fork):** `File > Save a copy to GitHub`. You'll need to authorize Colab with GitHub.

**Important Notes for Colab Users:**

*   **Temporary Environment:** Files in Colab (like the cloned repository and installed packages) are temporary and will be gone when your session ends. You'll need to re-run the `!git clone`, `sys.path`, and `!pip install` cells each time you start a new session.
*   **Always Save:** Make sure to save your important notebook changes to Google Drive or GitHub before closing Colab.

---
**(Optional: Advanced Colab Topics / Further Information)**

*   **Working with Private Repositories:** To open notebooks from private GitHub repositories, in the "Open notebook" dialog (GitHub tab), check "Include private repos" and authorize Colab.
*   **Persistent Storage with Google Drive:** For projects requiring more persistent storage (e.g., large datasets, saving intermediate results beyond the notebook), you can mount your Google Drive:
    ```python
    from google.colab import drive
    drive.mount('/content/drive')
    # You can then access files at /content/drive/MyDrive/
    ```
*   For more details on Colab's GitHub integration, see Google's official [Colab GitHub Demo Notebook](https://colab.research.google.com/github/googlecolab/colabtools/blob/master/notebooks/colab-github-demo.ipynb).

---

## 2. Understanding & Using Virtual Environments

When working on Python projects, it's crucial to use virtual environments.

**Why Use Virtual Environments?**
- **Isolation:** Each project can have its own set of dependencies (packages like `numpy`, `qiskit`, `pandas`) without interfering with other projects or your system's global Python installation.
- **Version Control:** Project A might need `numpy` version 1.20, while Project B needs `numpy` 1.25. Virtual environments keep these separate.
- **Reproducibility:** You can easily recreate the same environment on another machine or for a teammate using a `requirements.txt` file.

We'll primarily use `venv`, which comes built-in with Python 3.3+.

It's best practice to create a virtual environment inside your project folder.  
This keeps your project's dependencies isolated and avoids conflicts with other projects or your system Python.

You can create and manage virtual environments in several ways:
- **Method 1:** Using the command line (works everywhere, helps you understand what's happening)
- **Method 2:** Using VS Code (integrated and convenient if you use this editor)
- **Method 3:** Using PyCharm (integrated and convenient if you use this editor)

Below, you'll find instructions for each method.  
*If you use an IDE like VS Code or PyCharm, you can create and manage virtual environments directly from within the IDE—see the next sections for details.*

### Method 1: Command Line

1. **Navigate to your project folder:**
   ```bash
   cd path/to/your/project
   ```
2. **Create the virtual environment:**
   ```bash
   python -m venv venv
   # or, if needed:
   python3 -m venv venv
   ```
3. **Activate the environment:**
   - Windows (Command Prompt/PowerShell):  
     `.\venv\Scripts\activate`
   - Windows (Git Bash):  
     `source venv/Scripts/activate`
   - macOS/Linux:  
     `source venv/bin/activate`
4. **Install packages:**
   ```bash
   pip install -r requirements.txt
   # or
   pip install package_name
   ```
5. **Deactivate when done:**  
   `deactivate`


### Method 2: VS Code

VS Code makes it easy to work with Python virtual environments. Here’s how to set up and use them for your project:

#### **A. Creating a New Virtual Environment in VS Code**

1. **Open your project folder in VS Code**  
   Go to "File" > "Open Folder..." and select your project folder.  
   *This step is crucial so VS Code understands your project's context and can manage environments correctly.*

2. **Open the Command Palette**  
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS).

3. **Create the environment**  
   - Type `Python: Create Environment` and select it from the list.
   - When prompted, choose **Venv** as the environment type.
   - Next, select the Python interpreter you want to use as a base (usually your global Python installation or another version you have installed).

4. **VS Code will create the environment**  
   - A new folder (usually called `.venv`) will appear in your project folder.
   - VS Code will usually offer to select this new environment for your workspace automatically.

5. **Automatic package installation**  
   - If your project folder contains a `requirements.txt`, `pyproject.toml`, or `environment.yml` file, VS Code will offer to install the necessary packages for you.
   - It will also add a `.gitignore` file to help prevent you from accidentally committing the virtual environment to source control.

For more details, see the [official VS Code documentation `creating-environments`](https://code.visualstudio.com/docs/python/environments#_creating-environments).


#### **B. Selecting an existing virtual environment in VS Code**

If you already have a virtual environment and want to use it:

1. **Open the Command Palette**  
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS).

2. **Select the interpreter**  
   - Type `Python: Select Interpreter` and select it.
   - You’ll see a list of available Python interpreters and environments.
   - If you don’t see your environment, choose "Enter interpreter path..." and browse to the Python executable inside your venv (e.g., `./venv/bin/python` or `.\venv\Scripts\python.exe`).

3. **Verify the selection**  
   - After selecting, check the **bottom-left corner of the VS Code status bar**. It should now show the path to the Python interpreter inside your chosen virtual environment.
   - This means VS Code will use this environment for running Python code, linting, debugging, and in its integrated terminal (which should auto-activate the venv).

For more details, see the [official VS Code documentation `workingwith python interpreters`](https://code.visualstudio.com/docs/python/environments#_working-with-python-interpreters)


### Method 3: PyCharm

PyCharm makes it easy to manage Python interpreters and virtual environments for your projects. Here’s how you can set up and use them:

**1. Choosing or Creating a Python Interpreter**

- **For an existing project:**  
  - On Windows and Linux: Go to `File | Settings | Project: <project name> | Python Interpreter`
  - On macOS: Go to `PyCharm | Settings | Project: <project name> | Python Interpreter`
- **For new projects (default interpreter):**  
  - On any OS: Go to `File | New Projects Setup | Settings for New Projects`

Here, you can either select an existing interpreter from the list or click "New interpreter" to create a new one. After making your choice, click OK to save the changes.

**Tip:** The Python Interpreter selector is also available on the status bar at the bottom of PyCharm. This is the quickest way to switch between interpreters.


**2. Creating a Virtual Environment from Project Requirements**

If your project folder contains a `requirements.txt` or `setup.py` file, you can let PyCharm set up the environment for you:

- Open your project folder in PyCharm (`File | Open` and select the folder).
- If no virtual environment exists yet, PyCharm will suggest creating one automatically.
- PyCharm will use the requirements file to install all necessary packages for you.

For more details, see the [official PyCharm guide on creating virtual environments](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#env-requirements).



**3. Managing Packages and Dependencies**

- You can manage packages and dependencies directly in PyCharm’s interface, or by editing the `requirements.txt` file.
- For more info, see [Managing dependencies in PyCharm](https://www.jetbrains.com/help/pycharm/managing-dependencies.html).


**4. Installing Packages with pip in PyCharm**

- Open the terminal in PyCharm (from the left sidebar).
- You can install a single package, multiple packages, or all packages from a requirements file:
  ```bash
  pip install package_name
  pip install package1 package2
  pip install -r requirements.txt
  ```


### Common pitfall: wrong environment active

*This is the most common source of confusing errors for beginners!*

**Problem:**  
You created `venv_A` for project A and installed packages. Later, you open a new terminal, forget to activate `venv_A`, and try to run your code. Python uses the global environment (or `venv_B` from another project if that was last active), and you get `ModuleNotFoundError` because the packages aren't there.

**How to avoid & check:**

1. **Always activate your environment:**  
   Before running `pip install` or your Python scripts from the terminal, make sure the correct virtual environment is active. Look for `(venv)` or your custom environment name in the terminal prompt.

2. **Check your IDE:**  
   - **VS Code:** Look at the bottom-left status bar for the Python interpreter path.  
   - **PyCharm:** Go to "Settings" > "Python Interpreter" and check the selected interpreter. 
   If the interpreter path does not point inside your project folder (or the path of your virtual environment), you are not using the correct environment.

1. **Test which Python/pip is being used:**  
   In an active terminal, run:
   ```bash
   # On macOS/Linux
   which python
   which pip

   # On Windows
   where python
   where pip
   ```
   The paths should point *inside* your project's `venv` folder.

   Or, in Python:
   ```python
   import sys
   print(sys.executable) # Path to Python interpreter
   print(sys.path)       # List of paths Python searches for modules
   ```
   `sys.executable` should point to the Python within your venv.

---

## 3. Working with project files & imports

**Problem:** You have `main.py` and `helper.py` in the same directory. `main.py` has `import helper`. You open *only* `main.py` in VS Code (or another editor) and run it. You get `ModuleNotFoundError: No module named 'helper'`, even though `helper.py` is right there!

**The solution: open the entire project folder**

Python looks for modules in specific places (defined in `sys.path`). When you run a script, the directory containing the script is usually added to `sys.path`. However, if an IDE isn't aware of the "project" context, it might not set up the paths correctly, **especially if you only open a single file instead of the whole project directory**.

---

## 4. Dealing with package version issues

**Problem:** You install packages, but they conflict, or you need a specific version.

### Understanding `requirements.txt`
Many projects include a `requirements.txt` file. This file lists the necessary packages and often their specific versions, like:
```
numpy==1.20.3
pandas>=1.0.0,<2.0.0
qiskit==0.45.0
matplotlib
```
*   `==1.20.3`: Exactly this version.
*   `>=1.0.0`: Version 1.0.0 or newer.
*   `,<2.0.0`: And older than version 2.0.0.
*   `matplotlib`: Any version (usually the latest).

**Always install from `requirements.txt` if provided (after activating your venv):**
```bash
pip install -r requirements.txt
```
This helps ensure everyone is using a compatible set of packages.

### Solving version conflicts
**Symptom:** Errors during `pip install`, or runtime errors mentioning version incompatibilities.

1.  **Fresh Virtual Environment:** The best first step is often to delete your current `venv` folder, create a new one, activate it, and try `pip install -r requirements.txt` again.
2.  **Install all at once:** If you're installing multiple packages manually, do it in one command:
    ```bash
    pip install packageA packageB packageC
    ```
    This allows `pip`'s dependency resolver to try and find compatible versions for all of them simultaneously.
3.  **Check for problematic packages:**
    *   `pip check`: This command can sometimes identify broken dependencies.
4.  **Uninstall and reinstall specific versions:**
    If you know `packageX` is causing issues and needs to be, say, version 1.5:
    ```bash
    pip uninstall packageX
    pip install packageX==1.5
    ```
5.  **Look at error messages:** `pip` usually gives clues about which packages have conflicting requirements. You might need to adjust versions in `requirements.txt` (if you control it) or find a set of versions that work together. ***This can sometimes be trial and error.***

----

## Using Jupyter Notebook/Lab with Your Virtual Environment (Shell & IDEs)

When working with Jupyter Notebooks (`.ipynb` files), it's essential that the notebook uses the Python environment and packages from your project's virtual environment. This is true whether you launch Jupyter from the terminal or use it inside an IDE like VS Code or PyCharm.

**Core Principle:**  
The Jupyter kernel (the engine that runs your Python code in the notebook) must be associated with your project's virtual environment, where your specific packages (like `numpy`, `qiskit`, `pandas`, etc.) are installed.


### 1. Install Jupyter and `ipykernel` in your virtual environment

Even if you have Jupyter or Python extensions installed globally or in your IDE, you **must** install `ipykernel` (and usually `notebook` or `jupyterlab`) *inside* your project's active virtual environment.

**Steps:**
1. **Activate your project's virtual environment** (in the terminal).
2. **Install Jupyter and ipykernel:**
    ```bash
    pip install notebook ipykernel
    ```
    - `notebook`: Installs the classic Jupyter Notebook interface.
    - `ipykernel`: Lets this Python environment be used as a "kernel" by Jupyter.

    *If you prefer JupyterLab:*
    ```bash
    pip install jupyterlab ipykernel
    ```
    > *Tip: Add `notebook`/`jupyterlab` and `ipykernel` to your `requirements.txt` so they're always installed with your environment.*


### 2. Using Jupyter Notebooks from the terminal

This is the traditional way to run Jupyter.

1. **Activate your virtual environment** in the terminal.
2. **Navigate to your project folder:**
    ```bash
    cd path/to/your/project
    ```
3. **Start Jupyter:**
    - For classic Notebook: `jupyter notebook`
    - For JupyterLab: `jupyter lab`
    - This will open Jupyter in your web browser.

**Selecting the correct Kernel:**
- **New Notebook:** Choose your kernel from the "New" dropdown or Launcher.
- **Existing Notebook:** Go to "Kernel" > "Change kernel" and select your environment.


### 3. Using Jupyter Notebooks Inside IDEs

IDEs like VS Code and PyCharm Professional have built-in Jupyter support.  
**Important:** Make sure your IDE is set to use your project's virtual environment as the Python interpreter, and that this environment has `ipykernel` installed.  
If `ipykernel` is missing, the notebook will not run or the correct kernel will not appear in the selection list.


### 4. Verify Your Setup (in a Notebook Cell)

To check which Python environment your notebook is using, run this in a notebook cell:
```python
import sys
print("Python Executable:", sys.executable)
print("\nSys Path:")
for path in sys.path:
    print(path)
```
- The `Python Executable` should point *inside* your project's virtual environment.


---

## 5. General troubleshooting & FAQ


**Q: My terminal says `'python'` or `'pip'` or `'git'` is not recognized / command not found.**  
**A:**  
This means the program is either not installed, or its location is not added to your system's PATH environment variable.

- **Solution:**
    - Ensure you have installed Python (from [python.org](https://python.org), check "Add Python to PATH" during installation) and/or Git (from [git-scm.com](https://git-scm.com)).
    - Try reinstalling and make sure the "Add to PATH" option is selected.
    - You might need to restart your terminal or even your computer for PATH changes to take effect.


**Q: I installed a package, but Python says `ModuleNotFoundError`.**  
**A:**  
This is almost always one of these:

1. **Wrong environment active:**  
   You installed the package in `venv_A` but are trying to run your script using `venv_B` or the global Python.
   - **Fix:** Activate the correct virtual environment in your terminal. Ensure your IDE is using that environment's interpreter (see section 2).
2. **Typo in package name:**  
   For example, `import pands` instead of `import pandas`.
3. **You didn't actually install it:**  
   The `pip install` command might have failed. Check its output for errors.


**Q: What's the difference between `venv` and `conda`?**  
**A:**  

- **`venv`:** Manages Python packages for Python environments. It's built into Python.
- **`conda`:** A more general-purpose package and environment manager. It can manage Python packages, Python versions themselves, and even non-Python software (like C++ libraries). Often used in data science (Anaconda/Miniconda distribution).
- **Recommendation:**  
  If your course/project uses `venv` and `pip`, stick to that. If it specifies `conda`, use `conda`. They achieve similar goals for Python package isolation but work differently. Mixing them can be problematic if you're not careful.


**Q: My IDE (VS Code/PyCharm) is slow or behaving strangely.**  
**A:**  

- Ensure you have the official Python extension (for VS Code) installed and up-to-date.
- Try closing and reopening the IDE.
- Restart your computer.
- Check if the IDE is indexing files (often a progress bar in the status area). Wait for it to finish.
- Ensure you have enough RAM and CPU resources available.


**Q: `pip install` is failing due to network issues/firewall.**  
**A:**  
This can happen in corporate or university networks.

- You might need to configure `pip` to use a proxy server. Search for "pip configure proxy".
- Try a different network if possible to confirm it's a network issue.
- Download the package's `.whl` (wheel) file manually from [PyPI](https://pypi.org/) and install it with:
  ```bash
  pip install path/to/package_file.whl
  ```


**Q: How do I create/update a `requirements.txt` file?**  
**A:**  
Once you have your virtual environment active and all packages installed, run:
```bash
pip freeze > requirements.txt
```
This will save all installed packages (and their exact versions) in the current environment to `requirements.txt`.


**Q: `ModuleNotFoundError` in Notebook (but package is in venv):**  
**A:**  

- **Cause:** The notebook is *not* using the kernel from your intended virtual environment.
- **Shell Fix:** Select the correct kernel in the web UI.
- **VS Code Fix:** Select the correct kernel/interpreter in VS Code.
- **PyCharm Fix:** Ensure the Project Interpreter is correctly set to your venv.


**Q: Kernel Not Found / IDE can't start Jupyter:**  
**A:**  

- **Cause:** `ipykernel` (and possibly `notebook` or `jupyterlab`) is not installed *in the Python environment the IDE is trying to use*.
- **Fix:** Ensure their installation for the virtual environment your IDE is pointed to.

---

## Quick Reference: Key Setup Steps & Troubleshooting

**1. Get the Code:**  
- **GitHub Desktop:** "Code" > "Open with GitHub Desktop"
- **Terminal:** `git clone <URL>`
- **IDE:** Use the "Clone" feature
- **Google Colab:** Go to [colab.research.google.com](https://colab.research.google.com/) > "File" > "Open notebook" > "GitHub" tab > paste repository URL

**2. Set Up Your Virtual Environment:**  
- **Create:** `python -m venv venv`
- **Activate:**  
  - Windows: `.\venv\Scripts\activate`
  - Mac/Linux: `source venv/bin/activate`
- **Install packages:**  
  - All at once: `pip install -r requirements.txt`
  - Single: `pip install package_name`
- **Deactivate:** `deactivate` (when done)

**3. Ensure Your IDE Uses the Right Environment:**  
- **VS Code:** Check the status bar for the Python interpreter path.
- **PyCharm:** Check "Settings" > "Python Interpreter".

**4. Check Your Python Environment:**  
- In terminal:  
  - macOS/Linux: `which python` and `which pip`
  - Windows: `where python` and `where pip`
  - Paths should point inside your project's `venv` folder.
- In Python:
  ```python
  import sys
  print(sys.executable)
  print(sys.path)
  ```

**5. Jupyter Notebooks:**  
- **Install in venv:**  
  `pip install notebook ipykernel`  
  *(or `pip install jupyterlab ipykernel` for JupyterLab)*
- **Start Jupyter:**  
  - Terminal: `jupyter notebook` or `jupyter lab`
  - IDE: Make sure the interpreter is set to your venv and `ipykernel` is installed.
- **Select the correct kernel** in the Jupyter interface or IDE.

**6. Google Colab (No Local Setup):**  
- **Clone repo:** `!git clone https://github.com/your-username/your-repo.git`
- **Add to path:**
  ```python
  import sys, os
  sys.path.insert(0, '/content/your-repo-name')
  ```
- **Install packages:** `!pip install -r requirements.txt` or `!pip install package_name`
- **Save work:** "File" > "Save a copy in Drive" (files are temporary otherwise)

**7. Common Pitfalls:**  
- **Import errors:** Always open the entire project folder in your IDE, not just a single file.
- **Wrong environment:** Activate the correct venv before running code or installing packages.
- **Package version issues:** Use `requirements.txt` and install all dependencies at once.
- **Jupyter kernel not found:** Ensure `ipykernel` is installed in your venv and selected as the kernel.
- **Colab session ends:** Re-run clone, path, and install commands each new session.

**8. Troubleshooting:**  
- **Read error messages carefully.**
- **Google the error message**—someone else has had the same issue!
- **If stuck:** Delete your venv, recreate it, and reinstall packages.
- **Colab issues:** Check that repository is public or authorize private repo access.

---

**Remember:**  
- Error messages often tell you exactly what's wrong  
- Google error messages—someone else has had the same issue  
- Be patient—setup can be tricky, but once done, you're ready to code!

Good luck, and happy coding!


---

*Guide written by `ibra` ibrahim Chegrane, Algolab IQ, 2025.*