---
title: MPs
summary: |

  <center>
  [Submit](https://cs418.cs.illinois.edu/submit/)    
  [WebGL2 Dialect](../text/dialect.html)
  </center>

...

# Overview

Each MP has a point value, representing some combination of its difficulty and importance;
and a category, either core or elective.

For full (100%) credit, you need to earn your credit-count enrollment times 10 core points and a like number of elective points.
Thus, if you are enrolled for 3 credits you need 30 core and 30 elective points;
if you are enrolled for 4 credits you need 40 core and 40 elective points.
Excess core points count as elective points
but excess elective points do not count as core points.
Earning fewer than that many points may result in a lower grade, as outlined in [the grading policy](../#grading).

:::aside
Why ×10?

The points on the assignments are my effort to estimate the hours I expect the median UIUC student will invest
in meaningful programming, assuming they've already invested significant time in understanding course content.
Given the [federal definition](https://www.ecfr.gov/current/title-34/part-600/section-600.2#p-600.2(Credit%20hour)) of 1 semester credit hour = 45 hours of total educational time
and assuming you use half^[
  I expect 50% on reading/viewing/discussing/reviewing, but for most of you not all up-front.
  Likely you'll put about 25% in up-front learning,
  another 25% in on-demand learning inspired by misunderstandings revealed when attempting an MP,
  and the remaining 50% in coding.
] of that with reading, viewing, quizzing, discussing, and reviewing content
that leaves about 20 hours per credit of programming time,
or 10 hours per credit of core MP and 10 hours per credit of elective MP.
:::

There are 42 core points available.

Core|MP        |Lang  |Notes
:--:|----------|------|---------------
  0 |[Any-language Warmup](warmup-anylang.html)|any|Prepares you to work on Rasterizer and Raytracer
  0 |[WebGL2 Warmup](warmup-webgl2.html)|WebGL2|Prepares you to work on other assignments
  8 |[Rasterizer](rasterizer.html)|any   |You code a partial implementation of what WebGL does
  2 |[Logo](logo.html)            |WebGL2|Basic motion
  4 |[Orbits](orbits.html)        |WebGL2|Scene graph
  8 |[Terrain](terrain.html)      |WebGL2|Generate and render geometry
  4 |[Flight](flight.html)        |WebGL2|Let the user move the camera
  4 |[Textures](textures.html)    |WebGL2|Basic texture maps
  8 |[Raytracer](raytracer.html)  |any   |Implement a basic raytracer
  4 |[Spheres](spheres.html)      |WebGL2|Simulate motion using simple physics

The Warmups help ensure that your code and our grading system understand one another.
After the warmups, the Rasterizer will help you understand WebGL2 and should be completed first,
followed by Logo.
Terrain is a prereq to both Flight and Textures.
Otherwise the order is not important, but we recommend the order listed here.

There are more than 80 elective points available; you only need 30 or 40 of them, depending on your credit enrollment.

|Elective|MP         |Lang  |Notes
|:------:|:------------------------------|------|---------------
|0--20   |[Rasterizer](rasterizer.html)  |any   |additions to the core *Rasterizer*
|2       |[Psychedelic](psychedelic.html)|WebGL2|visualize colorful time-varying functions
|2       |[GPU jitter](gpu-jitter.html)  |WebGL2|simple vertex shader added to *Logo*
|3       |[CPU jitter](cpu-jitter.html)  |WebGL2|simple dynamic positions added to *Logo*
|2       |[Lineograph](lineograph.html)  |WebGL2|keyboard motion without clearing
|2--4    |[OBJ loading](obj.html)        |WebGL2|load a common file format
|2--4    |[Parametric](parametric.html)  |WebGL2|generate spheres and toruses
|4       |[Subdivision](subdivision.html)|WebGL2|subdivide after *OBJ Loading*
|1       |[Cliffs](cliffs.html)          |WebGL2|variant of core *Terrain* styling
|2       |[Weathering](weathering.html)  |WebGL2|variant of core *Terrain* modeling
|3       |[Height map](height-map.html)  |WebGL2|variant of core *Terrain* styling
|4       |[Drive](drive.html)            |WebGL2|variant of core *Flight*
|1       |[Fog](fog.html)                |WebGL2|variant core *Flight* rendering
|0--26   |[Raytracer](raytracer.html)    |any   |additions to the core *Raytracer*
|4       |[Many spheres](many-spheres.html)|WebGL2|more efficient and versatile variant of core *Spheres*
|4       |[Goop](goop.html)              |WebGL2|smoothed particle hydrodynamics based on *Many spheres*

# Extensions

Deadlines have two purposes:
to help you manage your time
and to give us have enough time to grade your work.

Before a deadline comes due, you can extend it by going to the submission page and entering an extension request.
These are routinely granted without further review,
but too many extensions (especially near the end of the semester) can create a grading burden we can't handle and may result in some being rejected.
For that reason, please provide your rationale in the request.

The only notification of a successful extension request is a changed deadline on the submission page.
Rejected requests are communicated via campuswire DMs.


# Regrades

There are four types of regrade requests:

Grading errors
:   If we mis-graded your submission, let us know in a to-instructors post on campuswire and we'll address it.

Server errors
:   If your code works for you but not for us, let us know in a to-instructors post on campuswire.
    We'll investigate and may fix our server, ask you to fix your code, or explain why your code doesn't really work (the latter changing this to a different type of regrade).

Incorrect core MP
:   The core (parts of) MPs are selected because they represent content we want every student to master.
    If you lost core points during grading, you should
    
    1. Understand why they were lost (either by inspection or by visiting office hours)
    2. Fix your code
    3. Request (in a to-instructors post on campuswire) a chance to re-submit the assignment with the fixed core part

Fewer elective points than you wished
:   Our advice here is "focus on the upcoming assignment instead."
    Elective points are one big pool, so if you missed a point on one but do another point on the next it will come out at 100% in the end.
    There may be some special cases where we re-open an assignment to have elective points fixed, but we expect that to be rare.


# `Makefile`

Some MPs allow you to code in any language you want.
We support that by using [GNU Make](https://www.gnu.org/software/make/) as a build tool.
There are [many newer build tools out there](https://en.wikipedia.org/wiki/List_of_build_automation_software), but `make` remains the most widely deployed.

For these MPs, we execute your code as follows:

1. Enter the directory containing your code
2. Run `make build`
3. For each input file we want to test (for example `mp9xyzw.txt`),
    a. Copy the input file (`mp9xyzw.txt`) into the directory
    b. Run `make run file=mp9xyzw.txt` or the like
    c. Move the output file elsewhere, diff it against our expectations with ImageMagick, etc

The [first warmup](warmup-anylang.html) gives example `Makefile`s for many languages.
If you know about Makefiles you are welcome to make your own,
but for most students our example files can be used as-is.


If you don't have `make` on your computer, you can either install it or test without it.


## Installing `make`

Almost every OS
:   Either comes with `make` installed or allows installing it through the package manager under the name `make`
  
    This is true of at least Arch, Gentoo, Fedora, SUSE, CentOS, Nix, Guix, Debian, FreeBSD, OpenBSD, NetBSD, and Haiku;
    as well as their various re-skinned wrappers like Manjaro, Mint, Ubuntu, etc.

MacOS
:   Students have had success with each of the following (pick one):

    - install as part of the Apple developer tools.
      This might happen automatically or might require extra steps
      that vary from time to time as Apple changes its setup.
      If you have XCode but can't run `make` [search for "Command Line Tools" on developer.apple.com](https://ddg.gg/command line tools site:developer.apple.com).
    - install via [`brew install make`](https://formulae.brew.sh/formula/make#default)
    - install via [`port install gmake`](https://ports.macports.org/port/gmake/)
  
Windows
:   Students have had success with each of the following (pick one):

    - enable the [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install)
    - install via [`choco install make`](https://community.chocolatey.org/packages/make)
    - install via [`scoop install make`](https://scoop.sh/#/apps?id=c43ff861c0f1713336e5304d85334a29ffb86317)
    - install from [gnuwin32](https://gnuwin32.sourceforge.net/packages/make.htm)


## Testing without `make`

The `Makefile`s provided in the [first warmup](warmup-anylang.html)
have two lines they run.

The basic structure of a Makefile is

```makefile
rulename: optional dependencies
    code to execute
```

When we run `make rulename` it first looks for any rules named after dependencies and runs them;
then it runs the code.
While doing this it expands any names between `$(` and `)` with their definition;
notably, it expands `$(file)` with an input filename like `mp1req1.txt`.

:::example
Suppose a makefile contains

```makefile
run: program
	./program $(file)

program: main.cpp
	clang++ -O3 -I. main.cpp -o program
```

Then running `make run file=demo.txt`{.sh} will first `make program`{.sh};
because `main.cpp` is not a rule in the `Makefile` the dependency chain stops there;
it will jump to the command under `program:`{.makefile},
and then do the command under `run:`{.makefile}, for a final operation of

```sh
clang++ -O3 -I. main.cpp -o program
./program demo.txt
```

Thus running those two commands directly will test your code without needing `make`.
:::

:::example
Several example `Makefile`s have

```makefile
build:
	 
```

There's no dependencies and no commands, so running `make build` does nothing.
This is common for interpreted languages like Python.
:::


<script>document.querySelectorAll('pre.makefile').forEach(x => x.innerHTML = x.innerHTML.replace(/    /g,'\t'))</script>


# WebGL2 Dialect

Some MPs will require you to write in WebGL2.
We will impose a variety of limitations on these MPs beyond what the WebGL2 api and JavaScript and GLSL languages themselves imposes.

- No WebGL warnings.

  The only exception to this is WebGL-generated warnings responding to invalid user input,
  such as user-specified file names that do not exist on the server.

- Browser-agnostic.

  The V8 JavaScript engine (used by Chrome and Edge) applies some default values that can make certain kinds of erroneous code work when it is small but break when you add more to it.
  To avoid those cases, we will test on Firefox, LibreWolf, PaleMoon, or another Gecko-based browser, and we recommend that you do too.

- Various "do it this way" rules for things WebGL2 lets you do several ways.

  These serve two purposes.
  First, they help protect you from practices that we've notices tend to work at first but then lead to tricky-to-diagnose errors later on.
  Second, they help the course staff understand your code.
  
  We have a [separate page describing the specific rules](../text/dialect.html)
  and offer a [wrapWebGL2.js](../code/wrapWebGL2.js) script that checks these rules for you and generates warnings if they are violated.
