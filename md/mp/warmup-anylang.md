---
title: 'Warmup — Text to PNG'
header-includes: |
    <style>div > dl > dt  { clear: right; }</style>
...

The goal of this warmup is to ensure you can make programs that read text files and produce PNG files
in the language of your choice
and have those run successfully on the submission server.
In theory this is a mix of copying code we provide,
copying examples from your language's official documentation,
and writing some basic file processing code such as you did in CS1 and CS2.
In practice it will likely mean working around a few setup challenges.

# Overview

You will submit at least three files:

-   A `Makefile` with (at least) two targets:
    `build`, which accepts no arguments,
    and `run`, which accepts a single input `file` argument.
    
    Running
    
    ````bash
    make build
    make run file=inputfilename.txt
    ````
    
    should execute your code on `inputfilename.txt`.

-  Code, in whatever language you prefer, including any necessary support libraries that `make build` cannot obtain.

You do *not* need to submit the example input or output files: just your code and the `Makefile`.

If all of your files are in the same directory, you can submit them as-is (but must submit all of them in one go; piecemeal uploads will not work).

If you need a specific directory structure, upload a `.zip` that contains those files.
The logic for handling submissions is

a. If you submitted a `Makefile` (and other files) directly, we use that
a. Otherwise if you submitted a tarball or zip archive, we extract that and
    i. If extracting it provides a `Makefile`, we use that
    i. Otherwise if extracting it created exactly one directory, we enter that and
        1. If there's a `Makefile` in that directory, we use that
        1. Otherwise, report an upload format error
    i. Otherwise, report an upload format error
a. Otherwise, report an upload format error

The input files your code will read are ASCII text files;
after processing an input file, your code will produce one or more RGBA PNG files.

# What to code

## Reading Input

Each run, your program will be given one command-line argument, which is the path to an input file.

Each input file will have a number of lines; each line will have a keyword first, followed by zero or more extra pieces of information separated by whitespace (some mix of `' '` and `'\t'`).
Lines should be read in order, first to last, because some lines refer to the lines above them.

Ignore blank lines and lines starting with anything other than a keyword you know.
Always strip leading and trailing space from a line before parsing it.

In this assignment input files might look like

    png 200 300 outfilename.png
    position 2   20 200  150 90  40 290
    ignore this line since "ignore" is not a keyword you know 
    likewise ignore this line, which also starts with an unknown keyword
    
    color 4  255 127 0 255  0 127 255 127  0 0 0 255
    drawPixels 2

You do not need to have error checking code.
For example, if a `png` keyword is not followed by exactly two positive integers and one string ending ".png", your code is welcome to break in any way you wish.

### Keywords

Each homework will define its own set of keywords.
For this warmup MP, these are:


png *width* *height* *filename*
:   Every file will begin with `png`
    
    `png` will be followed by two positive integers, *width* and *height*, and a *filename*.
    You should write a RGBA png image of the specified width and height (see [Image file creation]).
    You should write the file in the default directory.
    The initial color of every pixel in the image should be transparent black (0, 0, 0, 0).
    
    You may assume the filename contains only non-whitespace ASCII characters and already has the appropriate ".png" ending.

position 2 $x_0$ $y_0$ $x_1$ $y_1$ ...
:   Provides a buffer of pixel locations, giving 2 coordinates ($x$ and $y$) for each.
    
    You may assume that every $x$ has a $y$,
    that $0 \le x_i \lt \text{\it width}$,
    and that $0 \le y_i \lt \text{\it height}$.

color 4 $r_0$ $g_0$ $b_0$ $\alpha_0$ $r_1$ $g_1$ $b_1$ $\alpha_1$ ...
:   Provides a buffer of colors, giving 4 coordinates (red, green, blue, alpha) for each.
    
    You may assume that every red has a corresponding green, blue, and alpha
    and that all values are between 0 and 255, inclusive.

drawPixels *n*
:   Draws *n* pixels from the most-recently-provided buffers.

    You may assume that this only comes after a `position` and `color` keyword
    and that *n* is a positive integer that does not exceed the number of position and color coordinates provided in them.

# Get three files working

You should be able to pass all of the following.
All test input files, with their reference output files, can be downloaded [as a zip](files/anylang-files.zip)


[warmup-simple.txt](files/warmup-simple.txt)
:   This file's contents are

        png 5 8 simple.png
        position 2 0 1 1 2 2 3 3 4 4 5 3 3 2 4
        color 4 255 255 255 255 127 255 255 255 170 170 255 255 255 255 255 255 200 120 3 255 0 0 0 255 0 0 0 255
        drawPixels 7

    and it should produce this image file: <img src="files/warmup-simple.png" style="height:1em;"/>.

    That's so small it's almost impossible to see, so let's zoom in and put a striped background behind the image so you can tell the difference between transparent and white:

    <img style="width:5em" class="demo" src="files/warmup-simple.png"/>

[warmup-messy1.txt](files/warmup-messy1.txt)
:   This file's contents are

        png 5 8 messy1.png
        color 4   127 255 255 127   170 170 255 255   200 120 3 255   0 0 0 191   255 255 255 255
        nothing here 23425 56
        position 2   1   2             2   3             4   5         2 4           1   1             3 6
        drawPixels 4

    and it should produce this image file: <img style="width:5em" class="demo" src="files/warmup-messy1.png"/>

[warmup-messy2.txt](files/warmup-messy2.txt)
:   This file's contents are

        png 8 8 messy2.png
        color 4 127 255 255 127 170 170 255 255 200 120 3 255 0 0 0 191 255 255 255 255
        position 2 1 2 2 3 4 5 0 0 2 4
        drawPixels 5
        position 2 0 0 0 7 7 7 7 0 6 1
        drawPixels 5

    and it should produce this image file: <img style="width:8em" class="demo" src="files/warmup-messy2.png"/>

# Submission and Feedback

This warmup is not graded by a human.
Rather, each time you submit your code to [submission site](https://cs418.cs.illinois.edu/submit/)
it will run automated tests and add information about their outcomes to that site.
There will be a delay of up to an hours before that information is visible.

Feel free to re-submit until you get positive status results.
Please refer questions to the campus forum or office hours.




# Tips

## Creating PNG files

You will create an 8-bit RGBA PNG image with a specified width and height.
The way to do this will vary by language.
You must use a technique that supports setting individual pixels to specific colors, not one with higher-level shape drawing functions (we'll write those functions ourselves).

Some optional parts of homeworks 2 and 3 will include reading image files too.
If you want to do those then, it might make sense to learn how now.

The following is example code to write PNGs taken from past semester's student submissions.
I don't claim they are optimal, but they did work.


<details><summary>C PNG Library</summary>

There are many image libraries for C, but students have had issues with most of the most popular ones.
We recommend using a light-weight wrapper around `libpng`:
`libpng` is by far the best-tested and most-rubust library but somewhat esoteric to use,
so we've created a 100-line wrapper [`uselibpng.c`](../files/uselibpng.c) and its header and documentation file  [`uselibpng.h`](../files/uselibpng.h) to give easy access to the most common use-cases.

```c
#include "uselibpng.h"

int main() {
  /* ... */
  image_t *img = new_image(width, height);
  /* ... */
  pixel_xy(img, x, y).red = /*...*/;
  pixel_xy(img, x, y).green = /*...*/;
  pixel_xy(img, x, y).blue = /*...*/;
  pixel_xy(img, x, y).alpha = /*...*/;
  /* ... */
  save_image(img, filename);
  free_image(img);
}
```

If you use `uselibpng.c`, you'll need to upload both it and its header with your code
and also compile with the `-lpng` library linker flag.

You may also use a different library (miniz and LodePNG have been used by past students) but if you do, expect to spend some programming time figuring out why the library doesn't always work in an intuitive way.

</details>


<details><summary>C++ PNG Library</summary>

There are many image libraries for C++, but students have had issues with most of the most popular ones.
We recommend using a light-weight wrapper around `libpng`:
`libpng` is by far the best-tested and most-rubust library but somewhat esoteric to use,
so we've created a 100-line wrapper [`uselibpng.c`](../files/uselibpng.c) and its header, documentation, and C++ wrapper file  [`uselibpng.h`](../files/uselibpng.h) to give easy access to the most common use-cases.

```cpp
#include "uselibpng.h"

int main() {
  /* ... */
  Image img = Image(width, height);
  /* ... */
  img[y][x].red = /*...*/;
  img[y][x].green = /*...*/;
  img[y][x].blue = /*...*/;
  img[y][x].alpha = /*...*/;
  /* ... */
  img.save(filename);
}
```

If you use `uselibpng.c`, you'll need to upload both it and its header with your code
and also compile with the `-lpng` library linker flag.

You may also use a different library (miniz, LodePNG, and CImg have been used by past students) but if you do, expect to spend some programming time figuring out why the library doesn't always work in an intuitive way.

</details>

<details><summary>C\# PNG Library</summary>

:::note
The testing server is running mono on Linux, not Microsoft's C# implementation. If you chose to use C#, you are responsible for ensuring it runs on Linux with mono.
:::

The relevant class is `System.Drawing.Bitmap`{.cs}.

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

<details><summary>Dart PNG Library</summary>

The relevant package is `image/image.dart`{.dart}.

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

<details><summary>Go PNG Library</summary>

The relevant package is `image`{.go}.

```go
import (
 "image/png"
 "image/color"
 "io"
)
func main() {
    // ...
    img := image.NewNRGBA(image.Rect(0, 0, width, height))
    // ...
    img.Set(x, y, color.NRGBA{red, green, blue, alpha})
    // ...
    w, err := os.Create(img.filename)
    png.Encode(w, img)
}
```
</details>

<details><summary>Haskell PNG Library</summary>

Students have reported success using [Phll](https://github.com/hywn/phll)

```haskell
import qualified Data.ByteString.Lazy as B
import Phll

pixels = flip map [0..width] $
         \x -> flip map [0..height] $
               \y -> (red, green, blue, alpha)

main = B.writeFile filename $ B.pack $ Phll.png_rgba pixels
```
</details>


<details><summary>Java PNG Library</summary>

The relevant libraries are `Color` from `java.awt`,
`BufferedImage`{.java} and `WritableRaster`{.java} from `java.awt.image`
and `ImageIO`{.java} from `javax.imageio`{.java} package.
Do not use `java.awt.Graphics`{.java}.

```java
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


<details><summary>Julia PNG Library</summary>

The relevant library is `Images`, which notably uses colors in a 0--1 color space, not 0--255.

```julia
using Images
# ...
raster = Array{ColorTypes.RGBA, 2}(undef, height, width)
fill!(raster, ColorTypes.RGBA(0,0,0,0))
# ...
raster[y,x] = ColorTypes.RGBA(red/255, green/255, blue/255, alpha/255)
# ...
save(filename, raster)
```
</details>


<details><summary>Python PNG Library</summary>

The relevant library is [pillow](http://python-pillow.org/).
To install, do `pip install pillow`{.bash} or `pip3 install pillow`{.bash} from the command line on your machine (not in your Makefile because we've pre-installed pillow, but not pip, on the testing server).
Do not use the `ImageDraw`{.python} module.

```python
from PIL import Image
# ...
image = Image.new("RGBA", (width, height), (0,0,0,0))
# ...
image.im.putpixel((x,y), (red, green, blue, alpha))
# ...
image.save(filename)
```
</details>    

<details><summary>Rust PNG Library</summary>

The relevant library is `image::RgbaImage` and `image:Rgba`.

```rust
use image::{Rgba,RgbaImage};
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


<details><summary>Typescript PNG Library</summary>

The relevant library is `jimp`.

```typescript
import Jimp from 'jimp';
const run = async () => {
    const image = new Jimp(width, height);
    // ...
    // make rgba a 32-bit integer of the form 0xRRGGBBAA
    image.setPixelColor(rgba, x, y);
    // ...
    await image.writeAsync(filename);
};
run().catch(console.error);
```
</details>    


<details><summary>Zig PNG Library</summary>

Thus far, students who have used zig have used its compatibility with C to use a [C] PNG library.
Zig is still in beta and is not recommended for those who are not interested in figuring out details like how to call a C library from zig themselves.

</details>

**Other**:
In earlier semesters we've also had students use D, Kotlin, Lua, and Scala.
In principle I am open to any language I can get to work on the testing server; just let me know what you'd like.


## Makefile

You will submit your code and a `Makefile`.
We will run your `Makefile` on a Linux server.
It is your responsibility to see that the `Makefile` and your code work in a Linux environment.
Following are *minimal* Makefiles you might use as a baseline.
We recommend using make's more advanced operations (separate `.o` targets, pattern rules, variables, etc) if you understand them.

Note that **`Makefile` indentation must be in tabs, not spaces** and that the file name must be exactly `Makefile` with no filename extension.

<details><summary>C Makefile</summary>
```makefile
.PHONEY: build, run

build: program

run: program
	./program $(file)

program: main.c uselibpng.c
	clang -O3 -I. main.c uselibpng.c -lpng -o program
```
</details>

<details><summary>C++ Makefile</summary>
```makefile
.PHONEY: build, run

build: program

run: program
	./program $(file)

program: main.cpp uselibpng.c
	clang++ -O3 -I. main.cpp uselibpng.c -lpng -o program
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

<details><summary>Go Makefile</summary>
```makefile
.PHONEY: build, run

build:
	go build -o bin/main main.go

run:
	./bin/main $(file)
```
</details>


<details><summary>Haskell Makefile</summary>
```makefile
.PHONEY: build, run

build:

run:
	runghc program.hs $(file)
```
</details>


<details><summary>Java Makefile</summary>
```makefile
.PHONEY: build, run

build: Program.class

run: Program.class
	java Program $(file)

Program.class: Program.java
	javac Program.java
```
</details>

<details><summary>Java Makefile with packages</summary>

If your code is in a package (as many IDEs will make it), you'll need a slightly more involved Makefile.

If the `.java` files contain `package some.name;` then they will be in some path `path/prefix/some/name`. Put the `Makefile` in `path/prefix/` as follows:

```makefile
SRC = $(wildcard some/name/*.java)
CLS = $(SRC:.java=.class)

.PHONEY: build, run

build: $(CLS)
    javac $(SRC)

run: $(CLS)
	java some.name.ClassWithMain $(file)
```

the `SRC` uses [the `wildcard` function](https://www.gnu.org/software/make/manual/html_node/Wildcard-Function.html) to find all Java files in that one package; if you use several packages, you will need to add additional wildcards there.

</details>


<details><summary>Julia Makefile</summary>
```makefile
.PHONEY: build, run

build:
	julia -e 'import Pkg; Pkg.add("Images")'

run:
	julia program.jl $(file)
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

Note: some students have seen cargo insert network access into the `cargo run` command,
but network access is not permitted during `make run` on the testing server.
`cargo build` will have created an executable in a path like `./target/debug/somename`
which can replace `cargo run` in the last line;
see <https://campuswire.com/c/GC178AE4D/feed/29> for how to use that.
</details>

<details><summary>Typescript Makefile</summary>
```makefile
.PHONEY: build, run

build:
	npm install && npm run build

run:
	npm start $(file)
```
</details>

<details><summary>Zig Makefile</summary>
```makefile
.PHONEY: build, run

build:
	zig build -Doptimize=ReleaseFast

run:
	zig-out/bin/program_name_from_buildzig $(file)
```
</details>


<script>document.querySelectorAll('pre.makefile').forEach(x => x.innerHTML = x.innerHTML.replace(/    /g,'\t'))</script>

## Image Comparison

Think your output looks like the reference output?
Maybe so, but "like" is a fuzzy idea and sometimes we'll hold you to a higher standard of similarity than your eye is trained to see.

Enter [ImageMagick](https://imagemagick.org/script/download.php).
ImageMagick is a collection of versatile command-line tools for manipulating images, including many forms of image comparison.

During grading, we use ImageMagick to create comparison images containing 

- your image, `student.png`
- the image we expect, `ref.png`
- an image that highlights any differences between them in red, `ae.png`
- an image that shows all color differences, `rawdiff.png`
- an image that magnifies color differences, `diff.png`

We create those images and stick them together into one large image to look at during grading using the following commands:

```bash
compare -fuzz 2% student.png ref.png ae.png
composite student.png ref.png -alpha off -compose difference rawdiff.png
convert rawdiff.png -level 0%,8% diff.png
convert +append ref.png student.png ae.png rawdiff.png diff.png look_at_this.png
```

Note that some tasks are permissive of some differences while others will be more strict.
For example, consider this image:

<figure>
<div style="display:grid; grid-template-columns: repeat(5, 1fr); width:100%">
<img style="grid-column-end: span 5; width:100%" class="demo" src="files/comparison.png"/>
<center>Reference</center><center>Student</center><center>Differing pixels</center><center>Subtraction</center><center>Brighter subtraction</center>
</div>
<figcaption>An example output image from ImageMagick</figcaption>
</figure>

The student image is similar to its reference image, but the outline is not the same (a few missing pixels along the left edge, touching in the middle) and there's visible horizontal banding in the color error.
If this input was meant to test shading and overlap, those would result in lost points.
It it were meant to measure positioning and perspective, they'd not be a concern.
