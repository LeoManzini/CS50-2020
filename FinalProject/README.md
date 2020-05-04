    My project is a simple but useful extension for google chrome, where you can quickly format text. The project is in version "1.5" able to future updates
and allows you to type text and convert it to Upper, Lower or make it Bold.
    It consists of an icon and when you click on it, a small box appears with a field to enter the text to be formatted three buttons appear with it:
the Upper button that turns all text into capital letters, the Lower button that turns all text into lowercase letters and the Bold button that turn the text into bold.
    To make it work, you need to enter at chrome://extensions and enable the developer function, drag the folder with all its contents into that tab, and it's ready to use.
    Inside the folder has 3 files: index.html, manifest.json and script.js. The html file has the function of displaying the body of the plugin, the field to type, the buttons and
their respective unique identifier (identity or id). The main purpose of the manifest file is to provide information about the web application. It is a JSON file that
contains information such as application name, author, icons and description. This information is used to install the application on the device's home page. The manifest file is
responsible for an installable web application.
    The javascript file is responsible for giving functionality to the application, the script.js contains an event listener which means that when an event occurs
(in this case a click on a button identified by the id) an event will fire and a different functionality will happen for each button clicked. The typed text is assigned to a
variable called text (for convenience) and depending on the button clicked it calls the corresponding function and transforms the text that appears below the buttons (div with id result).
