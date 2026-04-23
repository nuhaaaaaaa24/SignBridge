# SignBridge - Real-Time Sign Language Detection and Translation
SignBridge is a video calling application intended to aid with translating Sri Lankan Sign Language into text. It consists of a conventional two-person video call interface combined with a deep learning model that captures the camera feed and displays a text transcript in real time. 

The application is developed with Flask, HTML, CSS and JavaScript. The deep learning model is developed with Python, TensorFlow and TensorFlow.js.

The demo for this application can be viewed at https://signbridge-pzm3.onrender.com/ 

## How to run this application locally
To run this on a local development server, you will need to set the environment variables defined in config.py.

If you do not know how to do this, contact me for assistance.

<b>1) Clone the repository to your local drive:</b>

```
git clone https://github.com/nuhaaaaaaa24/SignBridge.git
```

<b>2) Navigate to the folder you just created:</b>

```
cd your/path/here/SignBridge
```

<b>3) Create a Python virtual environment.</b>

In your terminal, run the following command:

```
python3 -m venv venv
```

<b>4) Activate the virtual environment</b>

On Windows Command Prompt, run the following:

```
venv\Scripts\activate
```

On Windows PowerShell, run the following:

```
venv\Scripts\Activate.ps1
```

On MacOS, run the following:

```
source venv/bin/activate
```

On Linux, run the following:

```
source venv/bin/activate
```

<b>5) Install the required dependencies</b>

Run ONE of the following commands: 

```
pip install -r requirements.txt
```
or
```
python3 -m pip install -r requirements.txt
```

<b>6) Run the development server with the following command:</b>

```
python signbridge.py
```

## Changelog - Version 0.3.14
* Added bearer tokens so at registration the tokens are generated for each user
* Removed the 'View owned rooms' button in profile because it clutters the UI and we are not really implementing joining back or viewing messages.
* Migration added for User Tokens


## Documentation
This application uses Sphinx for documentation - please visit https://www.sphinx-doc.org/en/master/usage/quickstart.html for help.

Use `cd docs` followed by `build html` to build the documentation on your machine.

Please note that the documentation is currently UNFINISHED!

## todo

* let users switch mic and cam off if needed
* fix error.html or just delete it atp
* fix call room
* add model toggle
* add gradcam heatmaps
* polish ui
* add http 403 error

## Academic Supervision
This application was guided and supervised by Ann Roshanie Appuhamy as part of undergraduate coursework.
