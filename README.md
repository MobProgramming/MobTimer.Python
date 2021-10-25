# Mob Programming Timer – Python
# [Download Now](https://github.com/MobProgramming/MobTimer.Python/releases)
## How to install and basic use video
[![MobTimer Install and Tutorial Video](http://img.youtube.com/vi/GxMP8SI6v0k/0.jpg)](http://www.youtube.com/watch?v=GxMP8SI6v0k)
## What is Mob Programming?
All the brilliant people working on the same thing, at the same time, in the same space, and on the same computer. Find out more at the [Mob Programming site]( http://mobprogramming.org/).

## History
When we started mob programming we originally used a phone timer to time the rotation. The timer played some music and then we rotated, however as the problems we worked on became more difficult we noticed people were unwilling to give up the keyboard. We then did a retrospective and resolved to get a louder and more annoying timer. This worked great as the mob did not want to listen to this loud and annoying timer very long. We then quickly found out that no one else in the office wanted to hear it either. We needed a solution that was quiet, yet encouraged the developers at the keyboard to rotate without ignoring the rotation time. Here is where the mob programming timer was born. The first mob programming timer was written in dot net. We then quickly had people ask about multi-platform options which is now why the python version of the mob programming timer exists today.

# Typical Use
- Add mobber names to timer
- Have the user marked current driver sit at the keyboard
- Start the timer
- Screen will be blocked when timer runs out
- Switch the person at the keyboard to the new driver
- Repeat
- To stop timer mid-session, open the exe again

## Random Tips
Tips are maintained in the Tips folder. A random file is selected and a random line from the random file is displayed. To add or remove tips simply add or remove files and lines from files.

## Customizing the timer
The Mob timer can be customized by modifying MobTimer.cfg.

## Themes
To add a theme simply copy and existing theme. To use that theme, put the file name of the new theme in the theme attribute in the MobTimer.cfg

## Project Links
[Trello Kanban Board]( https://trello.com/b/THISIB9Q/mob-programming-timer-python)

## Build Windows Distributable
Run BuildMobTimer.py

# Todo
* Make a distributable version for Windows
* Choose if to use the trello link or use this list
* Create plugin infrastructure (to interface with Clockify, etc.)
* Type into the minutes and seconds
* Clicking [Add mobber] should redirect cursor to typing next name
* Flipping the order of next and driver
* Replace next with navigator
* Make a new setup for Mac
* Skipping someone on the timer screen should be a button not clicking the name
* Consolidate files into a dir for moving to the './dist' folder