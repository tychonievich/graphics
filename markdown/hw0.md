---
title: 'HW0: Getting Started'
...

# Overview

This assignment is really more about making sure you are ready for those that follow than it is an actual assignment. 
It is *dramatically* easier than HW1.

## Logistics

Unlike other assignments

- all parts are required
- no extra credit is possible
- avoid plagarism, but feel free to grab code from any source as long as you cite it
- you are encouraged to submit it in each language you think you might want to use

This assignment is due the second week of class (i.e., 4 Sep or thereabouts) but earlier = better.

## How we submit

You will submit, for each assignment:

1. A `Makefile` with (at least) two targets:
    `build`, which accepts no arguments,
    and `run`, which accepts a single input `file` argument.
    
    Running
    
    ````bash
    make build
    make run file=inputfilename.txt
    ````
    
    should execute your code on `inputfilename.txt`.

2. Your code, including any necessary support libraries

3. A file named `implemented.txt` that contains the names of the reference input files you believe your code handles, one per line

If all of your files are in the same directory, you can submit them as-is (but must submit all of them in one go; piecemeal uploads will not work).

If you need a specific directory structure, upload a `.zip` or `.tar` that contains those files.
The logic for handling submissions is

a. If you submitted a `Makefile` directly, we use that
a. Otherwise if you submitted a tarball or zip archive, we extract that and
    i. If extracting it provides a `Makefile`, we use that
    i. Otherwise if extracting it created exactly one directory, we enter that and
        1. If there's a `Makefile` in that directory, we use that
        1. Otherwise, report an upload format error

The input files your code will read are ASCII text files;
after processing an input file, your code will produce one or more RGBA PNG files.

For your own testing sanity,
you will also want to be able to turn sets of PNG files into an video file
and to compare pixel differences between two PNG files.
This writeup describes how to set those up, but we will not directly test these functionality, neither in this nor in subsequent homeworks.

# What to code

## Reading Input

Each file will have a number of lines; each line will have a keyword first, followed by zero or more extra pieces of information separated by whitespace (some mix of `' '` and `'\t'`).
Lines should be read in order, first to last, because some lines refer to the lines above them.

Ignore blank lines and lines starting with anything other than a keyword you know.
Always strip leading and trailing space from a line before parsing it.

In this assignment input files might look like

    png 200 300 outfilename.png
    xy 10 20

    xyrgb 50 50   255 127 0
    ignore this line since "ignore" is not a keyword you know 
    likewise ignore this line, which also starts with an unknown keyword
    xyc     150   250 #ff00ee

You do not need to have error checking code.
For example, if a `png` keyword is not followed by exactly two positive integers and one string ending ".png", your code is welcome to break in any way you wish.

### Keywords

Each homework will define its own set of keywords.
For HW0, these are:


png *width* *height* *filename*
:   Every file will begin with either `png` or `pngs`
    
    `png` will be followed by two positive integers, *width* and *height*, and a *filename*.
    You should write a RGBA png image of the specified width and height (see [Image file creation]).
    You should write the file in the default directory.
    The initial color of every pixel in the image should be transparent black (0, 0, 0, 0).
    
    You may assume the filename contains only non-whitespace ASCII characters and already has the appropriate ".png" ending.

pngs *width* *height* *filename* *frames*
:   Every file will begin with either `png` or `pngs`
    
    `pngs` will be followed by two positive integers, *width* and *height*; a base *filename*; and a number of *frames* to generate.
    Your should write *frames* distinct RGBA png images of the specified width and height in the default directory.
    Each should be named *filename* followed by a 3-digit number between 000 and *frames* with a `.png` ending.
    
    <div class="example">
    If an input file begins `pngs 20 30 whatnot 12`
    your program will create twelve separate PNG files:
    `whatnot000.png`, `whatnot001.png`, ... `whatnot011.png`.
    </div>
    
    The initial color of every pixel in the image should be transparent black (0, 0, 0, 0).
    
    You may assume the filename contains only non-whitespace ASCII characters.

frame *t*
:   `frame` commands will only appear in files beginning `pngs`, not files beginning `png`.
    They specify that the subsequent commands should be applied to the given frame *t*,
    which will be an integer between 0 and the number of frames given on the `pngs` line.
    
    `frame` lines will be given in increasing order: `frame 3` will never appear after `frame 4`.
    Some frames may be skipped, meaning that image should remain its initial color.
    If drawing commands appear before the first `frame`, they apply to frame 0.

xy *x* *y*
:   Fill the pixel noted by the *x* and *y* coordinate to be opaque white (255, 255, 255, 255). 
    `xy 0 0` should fill the top left corner pixel.
    If the image is 200 wide and 300 tall, then `xy 199 299` would fill the bottom right pixel.
    
    You may assume *x* and *y* are integers within the image bounds.

xyrgb *x* *y* *r* *g* *b*
:   Fill the pixel noted by the *x* and *y* coordinate to have the specified color (*r*, *g*, *b*, 255).
    
    You may assume *r*, *g*, and *b* are integers between 0 and 255, inclusive.
    See the discussion of `xy` for comments on *x* and *y*.

xyc *x* *y* *hexColorString*
:   Fill the pixel noted by the *x* and *y* coordinate to have the specified color.
    The color is given in a web-standard 3-byte hex code: `#rrggbb`, where `rr` is a two-digit hexidecimal value for red, `gg` for green, and `bb` for blue.  Set the alpha to 255 (0xff)
    
    You may assume *hexColorString* is always a seven-character string of the appropriate format.
    See the discussion of `xy` for comments on *x* and *y*.

# Get two files working

You should be able to pass both of the following.
To get credit for them, make sure you put their names in your `implemented.txt` file, like

    hw0ex1.txt
    hw0ex2.txt

[hw0ex1.txt](files/hw0ex1.txt)
:   This file's contents are

        png 5 8 hw0ex1.png
        xy 0 1
        xyrgb 1 2 127 255 255
        xyc 2 3 #aaaaff
        xy 3 4
        xyrgb 4 5 200 120 3
        xyrgb 3 3 0 0 0
        xyrgb 2 4 0 0 0

    and it should produces this image file: <img src="files/hw0ex1.png" style="height:1em;"/>.

    That's so small it's almost impossible to see, so let's zoom in and put a striped background behind the image so you can tell the difference between transparent and white:

    <img style="width:5em" class="demo" src="files/hw0ex1.png"/>


[hw0ex2.txt](files/hw0ex2.txt)
:   This file's contents are

        pngs 7 7 hw0ex2- 16
        frame 0
        xy 6 3
        frame 1
        xy 6 2
        frame 2
        xy 5 1
        frame 3
        xy 4 0
        frame 4
        xy 3 0
        frame 5
        xy 2 0
        frame 6
        xy 1 1
        frame 7
        xy 0 2
        frame 8
        xy 0 3
        frame 9
        xy 0 4
        frame 10
        xy 1 5
        frame 11
        xy 2 6
        frame 12
        xy 3 6
        frame 13
        xy 4 6
        frame 14
        xy 5 5
        frame 15
        xy 6 4

    and it should produce 16 images (`hw0ex2-000.png` through `hw0ex2-015.png`) that create this animation (rendered at 16fps; if you don't see animation please upgrade to a browser that [supports APNG](https://caniuse.com/apng)):

    <img style="width:5em" class="demo" src="files/hw0ex2.png"/>


# Submission and Feedback

The [submission site](https://kytos.cs.virginia.edu/graphics/) for this assignment (only)
will run automated tests and add information about their outcomes to the submission file list.
There may be a small delay before it is visible, as we queue each submission as it comes in.
Feel free to re-submit until you get positive status results.
Please refer questions to piazza or professor office hours.




# Tips

## Creating PNG files

You will create an 8-bit RGBA PNG image with a specified width and height.
The way to do this will vary by language.
You must use a technique that supports setting individual pixels to specific colors, not one with higher-level shape drawing functions (we'll write those functions ourselves).

Some optional parts of homeworks 2 and 3 will include reading image files too.
If you want to do those then, it might make sense to learn how now.

The following is example code to write PNGs taken from past semester's student submissions.
I don't claim they are optimal, but they did work.


### C
Students have used 
[miniz.c](https://code.google.com/archive/p/miniz/)
and [LodePNG](https://lodev.org/lodepng/).

<details><summary>An example using LodePNG:</summary>

```c
#include "lodepng.h"

int main(int argc, char *argv[]){
    /* ... */
	unsigned char *image = calloc(width * height * 4, sizeof(unsigned char));
    /* ... */
    image[((y * width) + x)*4 + 0] = red;
    image[((y * width) + x)*4 + 1] = green;
    image[((y * width) + x)*4 + 2] = blue;
    image[((y * width) + x)*4 + 3] = alpha;
    /* ... */
	lodepng_encode32_file(filename, image, width, height);
    free(image);
} 
```
</details>


<details><summary>An example using miniz</summary>

```c
#include "miniz.h"

int main(int argc, char *argv[]){
    /* ... */
	unsigned char *image = calloc(width * height * 4, sizeof(unsigned char));
    /* ... */
    image[((y * width) + x)*4 + 0] = red;
    image[((y * width) + x)*4 + 1] = green;
    image[((y * width) + x)*4 + 2] = blue;
    image[((y * width) + x)*4 + 3] = alpha;
    /* ... */
    size_t size;
    void* data = tdefl_write_image_to_png_file_in_memory((void*) image, width, height, 4, &size);
    FILE* out_file = fopen(filename, "wb");
    fwrite(data, 1, size, out_file);
    fclose(out_file);
    free(data);
    free(image);
} 
```
</details>



### C++
All methods that work for C also work for C++, and most students used one of those.
An OO interface is also available through [CImg](http://cimg.sourceforge.net/).

<details><summary>An example using CImg:</summary>

```c
#define cimg_use_png
#include "CImg.h"

int main(int argc, char *argv[]){
    /* ... */
	cimg_library::CImg<unsigned char> image(width, height, 1, 4);
    /* ... */
    image(x,y,0,0) = red;
    image(x,y,0,1) = green;
    image(x,y,0,2) = blue;
    image(x,y,0,3) = alpha;
    /* ... */
	image.save_png(filename.c_str());
} 
```
</details>

### C\#

:::note
The testing server is Linux and runs mono, not Microsoft's C# implementation. If you chose to use C#, you are responsible for ensuring it runs on Linux with mono.
:::

The relevant class is `System.Drawing.Bitmap`{.cs}.

<details><summary>An example</summary>
```cs
using System.Drawing;
class ClassName {
    static void Main(string[] args) {
        // ...
        Bitmap img = new Bitmap(width, height, PixelFormat.Format32bppArgb);
        // ...
        img.SetPixel(x,y, Color.FromARGB(red,green,blue,alpha));
        // ...
        img.save(filename);
    }
}
```
</details>

### Dart

The relevant package is `image/image.dart`{.dart}.

<details><summary>An example</summary>
```dart
import 'package:image/image.dart';
import 'dart:io';

void main(List<String> args) {
    // ...
    image = Image(width, height);
    // ...
    image.setPixelRgba(x, y, red, green, blue);
    // ...
    File(filename).writeBytesAsSync(encodePng(image));
}
```
</details>

### Java

The relevant libraries are `Color` from `java.awt`,
`BufferedImage`{.java} and `WritableRaster`{.java} from `java.awt.image`
and `ImageIO`{.java} from `javax.imageio`{.java} package.
Do not use `java.awt.Graphics`{.java}.

<details><summary>An example</summary>
```cs
import java.awt.Color;
import java.awt.image.BufferedImage;
import java.awt.image.WriteableRaster;
import javax.imageio.ImageIO;

class ClassName {
    public static void main(String[] args) {
        // ...
        BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_4BYTE_ABGR);
        WritableRaster raster = b.getRaster();
        // ...
        raster.SetPixel(x,y, new Color(red,green,blue,alpha));
        // ...
        ImageIO.write(image, "png", new File(filename));
    }
}
```
</details>

### Python

The relevant library is [pillow](http://python-pillow.org/).
To install, do `pip install pillow`{.bash} or `pip3 install pillow`{.bash} from the command line.
Do not use the `ImageDraw`{.python} module.

<details><summary>An example</summary>
```cs
from PIL import Image
# ...
image = Image.new("RGBA", (width, height), (0,0,0,0))
# ...
image.im.putpixel((x,y), (red, green, blue, alpha))
# ...
image.save(filename)
```
</details>    

### Rust

The relevant library is `std::io::RgbaImage` and `sts::io:Rgba`.

<details><summary>An example</summary>
```cs
use std::io::{BufRead, BufReader};
fn main() {
    // ...
    let mut image = RgbaImage::from_pixel(width, height, Rgba([0, 0, 0, 0]));
    // ...
    image.put_pixel(x, y, Rgba([red, green, blue, alpha]));
    // ...
    image.save(filename).unwrap();
}
```
</details>    

### Other

In earlier semesters we've had students use D, Go, Haskell, Kotlin, and Scala.
In principle I am open to any language I can get to work on the testing server; just let me know what you'd like.


## Makefile

You will submit your code and a `Makefile`.
We will run your `Makefile` on a Linux server.
It is your responsibility to see that the `Makefile` and your code work in a Linux environment.
Following are *minimal* Makefiles you might use as a baseline.
We recommend using make's more advanced operations (separate `.o` targets, pattern rules, variables, etc) if you understand them.

<details><summary>C Makefile</summary>
```makefile
.PHONEY: build, run

build: program

run: program
    ./program $(file)

program: main.c lodepng.c
    clang -O3 -I. main.c lodepng.c -o program
```
</details>

<details><summary>C++ Makefile</summary>
```makefile
.PHONEY: build, run

build: program

run: program
    ./program $(file)

program: main.cpp
    clang++ -O3 -I. main.cpp -o program
```
</details>

<details><summary>C# Makefile</summary>
```makefile
.PHONEY: build, run

build: program.exe

run: program.exe
    mono program.exe $(file)

program.exe: program.cs
    mcs -r:System.Drawing -pkg:gtk-sharp-2.0 program.cs
```
</details>

<details><summary>Dart Makefile</summary>
```makefile
.PHONEY: build, run

build:
    pub get

run:
    dart program.dart $(file)
```
</details>

<details><summary>Java Makefile</summary>
```makefile
.PHONEY: build, run

build: Program.class

run:
    java Program $(file)

Program.class: Program.java
    javac Program.java
```
</details>


<details><summary>Python Makefile</summary>
```makefile
.PHONEY: build, run

build:

run:
    python program.py $(file)
```
</details>

<details><summary>Rust Makefile</summary>
```makefile
.PHONEY: build, run

build:
    cargo build

run:
    cargo run $(file)
```
</details>


## Animations and Image Comparison

### Animation

Some image viewers will let you scroll through a set of images quickly enough to see animation. But in case yours doesn't...

Given a set of images created with `pngs 30 50 someprefix 80`,
you can create an animation from it using the extremely versatile tool [ffmpeg](https://ffmpeg.org/download.html).
Some example uses include

```bash
# make an APNG, good for small transparent animated images
ffmpeg -r 16 -i someprefix%03d.png -f apng -plays 0 loop.png
## -r 16                 16 fps; any number (even fractions) work
## -i someprefix%03.png  gives the input images
## -f apng               picks the output format
## -plays 0              repeat forever
## loop.png              output filename

# make an mp4 using default compression
ffmpeg -r 30 -i someprefix%03d.png loop.mp4

# make an animated gif (an older inferior version of APNG)
ffmpeg -r 12 -i someprefix%03d.png loop.gif
```

Ffmpeg can do a *lot* more than this; see [the docs](https://ffmpeg.org/documentation.html) if you are interested.

### Image Comparison

Think your output looks like the reference output?
Maybe so, but "like" is a fuzzy idea and sometimes we'll hold you to a higher standard of similarity than your eye is trained to see.

Enter [ImageMagick](https://imagemagick.org/script/download.php) (or its less popular but faster clone, [GraphicsMagick](http://www.graphicsmagick.org/download.html)).
ImageMagick is a collection of versatile command-line tools for manipulating images, including many forms of image comparison.

During grading, we use ImageMagick to create comparison images containing 

- your image, `student.png`
- the image we expect `ref.png`
- an image that highlights any differences between them in red, `ae.png`
- an image that shows all color differences, `rawdiff.png`
- an image that magnifies color differences, `diff.png`

We create those images and stick them together into one large image to look at during grading using the following commands:

```bash
compare -fuzz 2% student.png ref.png ae.png
composite student.png ref.png -compose difference rawdiff.png
convert rawdiff.png -level 0%,8% diff.png
convert +append ref.png student.png ae.png rawdiff.png diff.png look_at_this.png
```

Note that some tasks permissive of some differences while others will be more strict.
For example, this image:

<img style="width:100%" class="demo" src="files/comparison.png"/>

is similar to its reference image, but the outline is not the same (a few missing pixels along the left edge) and there's visible horizontal banding in the color error,
both of which would result in some point loss on this image.

