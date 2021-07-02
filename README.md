# MIT Trisemester-2 Mini-Project
**Bonjour**,
This Markdown file will help you learn,install and run the python application on flask web framework.

## Prerequisite
- [Python 3.7+](https://www.python.org/downloads/)
- [PIP 20.0+](https://bootstrap.pypa.io/get-pip.py)

## Installation
**Creating a Virtual environment:**<br/>
We create virtual environment in order to create a seperate box in your local machine. Whenever you run you flask application locally it will work from inside the box and will 
not mess with the  exisiting system and dependencies of other python projects.

**Create a virtual environment:**
```
virtualenv venv
```

**Activate virtual environment:**
```
venv\script\activate
```

<b><i> Please activate the virtual environment before installing python dependecies. </b></i>

<b>Requirements.txt</b> will have all the python dependencies and libraries to run the python flask application

<b>Installing the python dependencies: </b>
```
pip install -r requirements.txt
```

## Run the Python Application ##
Here comes the tricky part, particularly in this flask application, the code structure is based on <b>Blueprints</b> or <b>Factory Application Structure</b>
and that is the reason you see multiple python files all over the project.<br/>
To run the application we will run the following command:
```
python application.py
```
This command will create a package and run your application.<br/>
To open it in a browser go to this URL;
```
http://127.0.0.1:8000/user/index
```

Documentation link: <a href="https://github.com/madhavparikh99/MIT-TriSem2/tree/main/Documentation">Documentation Link</a>
