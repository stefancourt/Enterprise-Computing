## 👥 Authors

- [@stefancourt](https://github.com/stefancourt)

## 🌐 Overview

An application that uses shell scripts to make changes to an sqlite database by adding deleting and changing information within the database to mimic that of a spreadsheet. There is laboratory material present in the folder as well as an sc folder which contains the main executable file along with the tests that are used to create and make changes to the database. This also contains firebase compatibility however my firebase database has since been deleted. if wanting to use a firebase database change *lines 8 and 10* respectively in the *sc.py-file*. This application was created using MacOS and so all scripts are for MacOS systems.

## 📦 Requirements

The following libraries and packages are required to run the application. These are downloaded within the virtual environment.

- [Flask](https://flask.palletsprojects.com/en/)
- [requests](https://pypi.org/project/requests/)

## 🌲 Project Structure

Any (item) means multiple files of type item

```plaintext
Quickhull-Algorithm/
├── laboratory1/
│   └── (Lab1-Contents)
├── laboratory2/
│   └── (Lab2-Contents)
├── laboratory3/
│   └── (Lab3-Contents)
├── laboratory4/
│   └── (Lab4-Contents)
├── sc/
│   ├── body
│   ├── cells.db
│   ├── test10.sh
│   └── sc.py
├── LICENSE
└── README.md
```

## 🌱 Configuring the Virtual Environment

1. Make sure that [Python 3.6.8](https://www.python.org/downloads) is installed on the device
2. Navigate to the **root directory**.

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install requests
python3 -m pip install flask
```

## 🚀 Running the Application

To run the application run the following script:

```bash
source venv/bin/activate
cd sc
# For Sqlite
python3 sc.py -r sqlite
# For Firebase
python3 sc.py -r firebase
```

1. Open a seperate terminal
2. Navigate to the **/sc directory**
3. Execute the following commands

```bash
chmod +x test10.sh
./test10.sh
```

You should then see all tests pass which are shell scripts changing items within the spreadsheet.
To ensure the application runs properly you should delete the database you can do this by navigating to the **/sc directory** and running:

```bash
rm -rf cells.db
```

## 📝 License

This project is licensed under the GNU GENERAL PUBLIC LICENSE