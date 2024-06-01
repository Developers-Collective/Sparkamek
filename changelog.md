# [07e87f08] - 2024-06-01

## New
- Kamek build copy settings -> allows you to choose if the build folder should be cleaned after copying the files (Feature #14)
- What's new dialog -> shows the changes of the current version
- NSMBW Reggie module now supports extended sprites (Feature #21)
- NSMBW Reggie module now supports "Hex value", "Dynamic Block Values" and "Multi-dualbox" options

## Changes
- Author of a language is now shown in the language list
- Open / Edit Project dialog has been reworked to be more user friendly

## Technical Changes
- Folder structure changes -> Sparkamek now uses a more organized folder structure in order to add more platform and game supports in the future
- Changed the save data keys of NSMBW projects to be more explicit
- Improved the language warning system to find more issues

--------------------------------

# [07e8158b] - 2024-01-17

## New
- Address Converter -> allows you to convert addresses between regions (Feature #4 & Feature #5)
- Developer Mode -> allows you to see more technical information about Sparkamek (Feature #13)

## Changes
- Symbols list now accepts greater and less than filters for addresses (Feature #10)

## Improvement
- Language debug is now shown in the logs dialog; *needs developer mode* (Feature #13)

## Bug fix
- Fixed project.yaml not working when defines was empty
- Fixed ld error not shown properly (Issue #9)

## Crash fix
- Incomplete languages no longer crash Sparkamek (Issue #12)

--------------------------------

# [07e7e931] - 2024-11-10

## Improvement
- Added timing to compilation
- YAML errors support are more explicit
- version-nsmbw errors are more explicit
- CodeWarrior path errors are more explicit
- Chinese version support (Feature #5)
- Separated v1 and v2 for regions

## Bug fix
- Device pixel ratio affecting font size (Issue #4)
- No more need of the special gekko CodeWarrior

--------------------------------

# [07e7d4b4] - 2024-10-22

## Improvement
- Reggie sprite list is now filtered by numeric values (Issue #3)

## Bug fix
- Reggie spritedata can now be exported when containing float values (Issue #2)

--------------------------------

# [07e7d494] - 2023-10-19

## New
- First release of Sparkamek ! 🥳
