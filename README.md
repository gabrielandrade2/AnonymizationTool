# AnonymizationTool

A simple Anonymization Tool for Japanese texts. 

It uses [Ginza](https://github.com/megagonlabs/ginza) POS tagging to identify potential `Proper Nouns` and replace those
with a `[ANON]` tag.

The method was specifically tunned to annonimize Japanese clinical texts, aiming to remove patient and doctor personal
information, such as names and addresses, and also institution (hopsital, clinic) names and locations.

## Execution

### Windows

A setup file is provided in the [Releases](https://github.com/gabrielandrade2/AnonymizationTool/releases/latest)
section.
This installer packs all required dependencies (including Python).
After installation, the program can be executed from the start menu or the desktop shortcut.

### The python way (Linux, Mac, Windows)

It can be executed in two main ways currently:

- Executing `gui.py` will initialize a gui to select files and define the parameters
- To run it in the console, `main.py` can be called, passing the proper parameters.

## Dependencies

- Python 3.10 or higher (It may work with older versions, but it was not tested)
- Spacy 3.4.4
- Ginza 5.1.2 (and ja-ginza module for Spacy)

## Generation of the executable / setup

The executable can be generated using [PyInstaller](https://www.pyinstaller.org/). \
The `AnonymizationTool.spec` file contains the configuration used for the generation of the executable.

The setup file was generated using [NSIS](https://nsis.sourceforge.io/Main_Page) and [NSIS Quick Setup Script Generator](https://nsis.sourceforge.io/NSIS_Quick_Setup_Script_Generator).

Note that all compilation and setup generation was done in a Windows 10 environment and some modification may be needed for it to work in other environments.



