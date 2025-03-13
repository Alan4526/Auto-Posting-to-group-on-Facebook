# Auto-Posting-to-group-on-Facebook

This bot works based on python selenium.
OS: Windows & MacOS

How to run it?

===========================
|||||| SETTING UP
===========================

1. Download the delivered ZIP file and copy all the files inside that ZIP file into a new folder.

2. Download and install Python 3.X and PIP if not already installed. Usually, newer MacOS versions have these packages installed by default. (https://www.python.org/downloads/)

3. Then open Terminal on your Mac (or Command Prompt on Windows). Type this command (and press ENTER key) to install the required libraries.

pip3 install -r requirements.txt

4. The setting up part is now complete.

===========================
|||||| USAGE
===========================

1. The file, named 'Config.txt', contains the settings of this script. Open that file using a text editor and change settings accordingly. Default settings are already there.

2. Input the links of all the groups you would like to auto-post into 'Groups.txt' file. Sample links are already there.

3. If you would like to upload photos, copy all the photos to 'Images' folder. It supports both 'png' and 'jpg' image formats.

4. Then, set the caption of your new post via 'Caption.txt' file.

5. To run your new automated script, open your Terminal (Command Prompt) and type these two commands. Make sure to replace the "path/to/your/folder/" with the correct path according to your script's folder.

python3 main.py

3. It will load a new Chrome session. Simply, log into your Facebook account using that browser and press ENTER key on terminal.

4. Then it will automatically perform the automation. You will see the status in the terminal.

===========================

Let me know if you need further support in setting up. We also offer remote desktop support through TeamViewer.

Thank you!

It saves chrome information like cookie to chromeProfile folder, so once you log in, you don't have to login again.
