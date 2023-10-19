<h1 align="center"><img src="./data/icons/Sparkamek.svg" width="32" align="center" /> Sparkamek: Add Code to NSMBW with Ease</h1>
<p align="center">
  <a href="https://www.python.org/downloads/">
    <img alt="Python 3.11" src="https://img.shields.io/badge/Python-3.11-blue" />
  </a>
  <a href="https://doc.qt.io/qtforpython/index.html">
    <img alt="PySide 6" src="https://img.shields.io/badge/PySide-6.4.1-brightgreen" />
  </a>
  <a href="https://github.com/Synell/Sparkamek/blob/master/LICENSE">
    <img alt="License: LGPL" src="https://img.shields.io/badge/License-LGPL-green" target="_blank" />
  </a>
  <img alt="Platforms: Windows, Linux and MacOS" src="https://img.shields.io/badge/Platforms-Windows%20|%20Linux%20|%20MacOS-yellow" />
  <a href="https://www.buymeacoffee.com/synell">
    <img alt="Donate: Buy me a coffee" src="https://img.shields.io/badge/Donate-Buy%20Me%20a%20Coffee-orange" target="_blank" />
  </a>
  <a href="https://www.patreon.com/synel">
    <img alt="Donate: Patreon" src="https://img.shields.io/badge/Donate-Patreon-red" target="_blank" />
  </a>
</p>

----------------------------------------------------------------------

Sparkamek is an app for Windows, Linux and MacOS. Kamek is a tool that allows you to add custom code to New Super Mario Bros. Wii. Sparkamek allows you to create, edit and build Kamek projects with ease. Everything is done in a simple and easy to use GUI.


## Requirements

### Windows
- Windows 7 or later
- VC++ 2015 Redistributable

### Linux
- All Linux distributions supported by PySide6

### MacOS
- MacOS 10.14 (Mojave) or later


### Source Code
- Python 3.11 or later
  - Dependencies (use `pip install -r requirements.txt` in the project root folder to install them)


## Installation

### Windows, Linux and MacOS

<a href="https://github.com/Synell/Sparkamek/releases/latest">
  <img alt="Release: Latest" src="https://img.shields.io/badge/Release-Latest-00B4BE?style=for-the-badge" target="_blank" />
</a>

- Download the latest release from the [releases page](https://github.com/Synell/Sparkamek/releases) and extract it to a folder of your choice.


## Customization

### Language

- You can customize the language of the app by adding a new file into the `/data/lang/` folder. The language must be a valid [JSON](https://en.wikipedia.org/wiki/JavaScript_Object_Notation) code. If the language is not supported, the app will default to English. Then, you can change the language in the settings menu.

  *See [this file](https://github.com/Synell/Sparkamek/blob/main/data/lang/english.json) for an example.*

### Theme

- You can customize the theme of the app by adding new files into the `/data/themes/` folder. The theme must be contain valid [JSON](https://en.wikipedia.org/wiki/JavaScript_Object_Notation) codes and valid [QSS](https://doc.qt.io/qt-6/stylesheet-reference.html) codes. If the theme is not supported, the app will default to the default theme. Then, you can change the theme in the settings menu.

  *See [this file](https://github.com/Synell/Sparkamek/blob/main/data/themes/neutron.json) and [this folder](https://github.com/Synell/Sparkamek/tree/main/data/themes/neutron) for an example.*


## Why Sparkamek?

### Kamek is a great tool, but...

Doing a lot of NSMBW modding, I found myself using Kamek a lot as it is used to compile the code. However, I found it very annoying to use as it for debugging for multiple reasons:
- No colors, so it's hard to read
- When using the fasthack option, it doesn't show the correct line number of the errors / warnings (it shows the line number of the fasthack instead, which is about 50 000 lines so good luck scrolling to the correct line, even with the search function)
- It doesn't show the file name of the errors / warnings
- No spacing, everything is cramped together
- When you have an error, it generates so much garbage that it's hard to find the error itself, because it's at the very top of the log

Okay, so if this didn't convince you, let me tell you a short story.

So one day I just wanted to test how much garbage the compiler gives, so I just remove a single `;` from a file called `boss.h`, and the rest of the code had no error. Now, if I compile this, we should in theory have a single error.

You know what, it threw me **1041 errors, in 24 different files**.
Like wtf, just for a single missing `;` ? And the worst part is that this represents 4 243 lines of garbage, and the correct error is at the very top of the log, under a lot of warnings, so good luck finding it on the command line with no color.

By the way, if you want to check the output for yourself, here it is, with all the warnings and the top of the log removed for your mental health: [error.log](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/files/error.log).

And here is the output of Sparkamek for the same error:
![Small output from Sparkamek](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/error-very-small.png)

Much better, right?


### So, what does Sparkamek do?

Sparkamek is a GUI for Kamek, so it does the same thing as Kamek, but with a lot of improvements. It also allows you to compile a custom loader for your game with improved features, like with the Kamek one.

You can also create and edit the Reggie Next (the level editor app) spritedata file with ease, which is use to create patches for the game.

And finally, you can also create and edit the Riivolution file with ease, which is used to create patches for the game.


## Usage

### First Start

When you start the app for the first time, you'll see this screen:
![No project opened screen](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/first-time.png)

Click on the `Open Project` button and follow the instructions to create a new project.

Once you have created a project, you'll have 1 to 4 tabs.

### Loader Tab

Here you can create and edit the loader for your game. The compiler has 2 modes: simple and complete.

The complete mode is the same as the base Loader one, meaning it has all the other stuff, but with colors, spacing and the correct line number for the errors / warnings whereas the simple mode is a lot more compact and only shows essential information.

![Simple compiler](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/loader-compiler-simple.png)


### Kamek Tab

#### Sprites and actors

Here you can check the sprites and actors that are in the game.

*Note that the sprites of this list are to take with a grain of salt, as they are not 100% accurate (because it requires putting the sprites replacement comment and using good profile names).*

![Sprites and actors](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/kamek-sprites-and-actors.png)

#### Compilers

Here you can compile the code for the game. The compiler has 2 modes: simple and complete.

The complete mode is the same as the base Kamek one, meaning it has all the other stuff, but with colors, spacing and the correct line number for the errors / warnings whereas the simple mode is a lot more compact and only shows essential information (and the only one true error instead of 1041 unrelated ones).

![Simple compiler](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/kamek-compiler-simple.png)

![Complete compiler](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/kamek-compiler-complete.png)

#### Symbols

Here you can check the symbols that are compiled, for debugging purposes.

![Sprites and actors](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/kamek-symbols.png)


### Reggie Next Tab

This tab is used to easily edit the `spritedata.xml` file, which is used to create sprite patches for the Reggie Next. You can also create a new `spritedata.xml` file from scratch.

![Reggie Next](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/reggie-next-all.png)

#### Sprites

Here you can check and select the sprites that are in the patch. You can load the sprites by pressing the `Load` button and save them by pressing the `Save` button.

![Sprites](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/reggie-next-sprites.png)

When selecting a sprite, you can see its information in the other panels.

#### Sprite Info

Here you can see the information of the selected sprite, as well as some useful buttons.

![Sprite Info](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/reggie-next-edit-sprite.png)

The buttons are:
- `Create a New Sprite`: Creates a new sprite with the default settings.
- `Delete Selected Sprite`: Deletes the selected sprite.
- `Import a Sprite`: Imports one or multiple sprites from a file.
- `Export Selected Sprite`: Exports the selected sprite to a file.
- `Reset`: Resets the settings of the selected sprite to the ones it had before editing it (selecting an other sprite sets the new reset state of the edited one).
- `Clear`: Clears the settings of the selected sprite.

![Sprite Info](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/reggie-next-edit-sprite-buttons.png)

The information are separated in 3 categories: `General Info`, `Dependencies` and `Settings`.

In the `General Info` category, you can see the name of the sprite, its sprite ID, its notes, and its supports.

![General Info](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/reggie-next-edit-sprite-general-info.png)

In the `Dependencies` category, you can see the dependencies of the sprite, which are the sprites that are required and / or suggested for the sprite to work.

![Dependencies](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/reggie-next-edit-sprite-dependencies.png)

In the `Settings` category, you can see the settings of the sprite, which are the settings that'll appear in Reggie Next when you select the sprite.

Here are the settings that you can have:
- `Dual Box / Radio Buttons`: A group of **two** settings that are exclusive to each other. You can only select one of them.
- `Entry Value`: A setting that has a raw number value.
- `Check Box`: A setting that can be enabled or disabled.
- `Drop Down List`: A group of settings that are exclusive to each other. You can only select one of them.
- `Value Selector from a File`: A group of **a lot** of settings that are exclusive to each other. You can only select one of them. A special window will open when you select this setting, allowing you to select the value. The values are loaded from a file. (*Note that Sparkamek doesn't support the editing of this files yet.*)

![Settings](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/reggie-next-edit-sprite-settings.png)

By clicking on one of the settings, you can edit it in the properties panel.

These settings are separated in 3 categories: `Nybbles`, `Required Nybble(s) / Required Value(s)` and `Other`.

The nybble settings are used to tell Reggie Next which nybble(s) should be affected by the setting. The `First Nybble` option is the first nybble that'll be affected by the setting, and the `Last Nybble` option is the last nybble that'll be affected by the setting. If you want to affect only one nybble, you can set the `First Nybble` and leave the `Last Nybble` to `None`. Because a nybble is 4 bits, you sometimes want to be more precise, like with a `Check Box` that only require one bit to work. In this case, you can set the `First Nybble Bit` and / or the `Last Nybble Bit` value(s). Note that you can easily check which nybble(s) and bit(s) are affected by the setting by looking at the sprite's current setting, in the bottom right corner of the widget.

![Settings](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/reggie-next-edit-sprite-settings-nybbles.png)

The `Other` category contains the other settings that are related to the type of widget you chose (e.g. `Dual Box / Radio Buttons` in the image below).

![Settings](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/reggie-next-edit-sprite-settings-other.png)

### Riivolution / Game Tab

This Riiivolution tab is used to easily edit the `riivolution.xml` file, which is used to create patches for the game. You can also create a new `riivolution.xml` file from scratch.

*Note that this section is a resume, more info can be found in the app itself.*

To load the riivolution file, you have to press the `Load` button. Then, you can edit the file and save it by pressing the `Save` button.

![Riivolution](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/riivolution-buttons.png)

Once you have loaded the file, you'll see planty of settings that you can edit.

#### General Info

Here you can edit the general information of the patch, like the root folder and the version of riivolution the patch should use.

![General Info](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/riivolution-general-info.png)

#### Game Properties

Here you can edit the game properties of the patch, like the game ID, the developper, the disc number and the disc version.

![Game Properties](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/riivolution-game-properties.png)

#### Regions

Here you can edit the regions of the patch. You can add, edit and delete regions.

![Regions](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/riivolution-regions.png)

![Regions](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/riivolution-region-properties.png)

#### Options

Here you can edit the options of the patch. You can add, edit and delete options.
Options are used to set which option should enable which patch. Note that options can enable multiple patches.

![Options](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/riivolution-options.png)

#### Patches

Here you can edit the different patches. You can add, edit and delete patches.

![Patches](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/riivolution-patches.png)
