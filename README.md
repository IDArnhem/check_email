## Before you run this
Before you try to run this script you will need [pyfirmata](https://pypi.python.org/pypi/pyFirmata) in your system, so that this python script can talk to your Arduino.

## Running the script
To run this script:
 * download it, store it somewhere in your desktop.
 * Open a terminal and type `cd <directory>` where `<directory` is the name of the directory/folder where your script is stored.
 1. Then type `python check.py`

## Stopping the script
Once the script is running press <kbd>Ctrl + C</kbd> to stop it.


## Troubleshooting

If you see an error like this one in the terminal:

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named babaloo
```

It means that a module (or library) called `babaloo` is missing from your system, the module `babaloo` of course, doesn't exist, it's just an example. You can install it using pip, like this:

```
$ sudo pip install babaloo
```

Where you have to replace the module name `babaloo` for the name of the module that you are actually missing.

The `sudo` command will ask for your password. `sudo` means **do** as **su**peruser.
