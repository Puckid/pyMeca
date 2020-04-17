# pyMeca
Standalone python library for mechanical design

# Philosophy
Mechanical design is missing a proper open source alternative. Even closed source paid solution often doesn't offer all the feature I would want. Also another issue I want to consider is the overcomplication and over dependencies. My goal is to have a minimal solution that allows to design 3d parts.

## Flexibility of input
It is necessary to have flexibility of input to satisfy most people and to smooth development process. Most users of cad softwares are used to UI so it should be considered.
The idea is to be able to use the interactive, meaning it needs some ways to export and save progress. This would kind of automatically allows to write scripts. You could share scripts or export compiled version which won't be obfuscated but would simply be a list volumes, shapes, contour, points and such. So the compiled version could be directly converted by an interpreter to a viewable 3d version or some stl file.
Also, enabling an interactive mode would make straight forward the implementation of a ui, buttons would simply directly call the same function one would call in the interactive mode.

## Everything is text
Everything should be text based files understandable by humans. This should also applied to compiled files (even if those are more robot like). This would enable easy version control and collaborative work. The goal is to allow the same workflow used in programming using Git.

## Everything is open
It goes together with the previous point, the ultimate goal of this library is to give user an true open source way to generate and share mechanical parts. Open source philosophy evolved in the right direction for the software world, it is necessary that this paradigm shift occurs in mechanical design. Sadly, no descent infrastructure allows that at the moment. Most shared parts are simply in stl format which is definitely not intended for further modification. Let's change that.

## Evolutive
Start minimal, allow user to expand functionality. It must be easy to create modules to expand features.


# Convention
## Coding style
This project applies to [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html). Especially, apply the point 2.1 : Run pylint ! Expecting a result of 10.00 for all files.

## Unit Test
Every single function of modules and packages are required to be tested in unit tests.
Use 'unittest' module for automatic testing.