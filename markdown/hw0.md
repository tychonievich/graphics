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

This assignment is due the second week of class (i.e., 7 Sep or thereabouts) but earlier = better.

## Structure

This and the following three assignments all work as follows:

1. When run from the command line, the name of an input file will be provided
2. Each line of that file will provide space-separated information in an easy-to-parse format (split, trim, readline, slice, and string-to-number should be all you need)
3. The first (non-blank non-comment) line gives the name of an output image file to create
4. Your program creates that output image file

# Specifics

## Input file format

Each file will have a number of lines; each line will have a keyword first, followed by zero or more extra pieces of information separated by whitespace (some mix of `' '` and `'\t'`).
Lines should be read in order, first to last, because some lines refer to the lines above them.

Ignore blank lines and lines starting with anything other than a keyword you know.
Always strip leading and trailing space from a line before parsing it.

In this assignment input files might look like

    png 200 300 outfilename.png
    xy 10 20

    xyrgb 50 50   255 127 0
    ignore this line since "ignore" is not a keyword you know 
    likewise, ignore this line, which also starts with an unknown keyword
    xyc     150   250 #ff00ee

You do not need to have error checking code.
For example, if a `png` keyword is not followed by exactly two positive integers and one string ending ".png", your code is welcome to break in any way you wish.

## Image file creation

You will create an 8-bit RGBA PNG image with a specified width and height.

C/C++
:   You could use [libpng](http://libpng.org/pub/png/libpng.html), but you don't want to.
    I suggest the public-domain [miniz.c](https://code.google.com/archive/p/miniz/) header.
    I've posted [a stripped-down version](files/minizpng.h) and [an example interface](files/writepng.c) to it.

    Alternatively, a previous TAs suggested [CImg](http://cimg.sourceforge.net/) and an example file [cimg_example.cpp](files/cimg_example.cpp). I have not used CImg myself.

    If you find another library you like, let me know and I'll see if I can easily get it on my compiling test server.

    Remember, if you use a C-language header (like libpng or miniz) but are writing C++, you'll need to put an `extern "C" { ... }`{.c} block around the `#include`{.c}
    
    > The testing server currently runs clang 6.0.
    > gcc 8.2 is also installed and can be switched to if a version compatibility issue is identified.

C#
:   The relevant class is `System.Drawing.Bitmap`{.cs}, along with it's `setPixel`{.cs} and `save`{.cs} methods

    ````cs
    // ... set width, height, etc.
    Bitmap img = new Bitmap(width, height, PixelFormat.Format32bppArgb);
    img.SetPixel(x,y, Color.FromARGB(r,g,b,a));
    img.save("filename.png");
    ````

    > The testing server currently runs mono 5.14.

D
:   There are several image libraries in the D community; 
    [`imageformats`](http://code.dlang.org/packages/imageformats) works well.

    ````d
    import imageformats;
    void main() {
        // ... set width, height, etc.
        auto img = new ubyte[width*height*4];
        img[(x + y*width)*4 .. (x + y*width + 1)*4] = [r,g,b,a];
        write_png("filename.png", width, height, img, ColFmt.RGBA);
    }
    ````


    Before `imageformats` was a thing, I wrote [minipng.d](files/minipng.d) for my first version of this course.
    I doesn't have many options, but it is simple to use; see the header comments for other uses.

    ````d
    import minipng;
    void main() {
        // ... set width, height, etc.
        auto img = Img!ubyte(width, height);
        img[x,y] = [r,g,b,a];
        img.save("filename.png");
    }
    ````

    > The testing server currently runs rdmd 2.081.
    > dub, dmd, and ldc are also installed and can be switched to if a version compatibility issue is identified. 

Java
:   The relevant libraries are `BufferedImage`{.java}, `WritableRaster`{.java}, and `ImageIO`{.java}, all in the `javax.imageio`{.java} package. Do not use `java.awt.Graphics`{.java}.

    ````java
    // ... set width, height, etc.
    BufferedImage b = new BufferedImage(width, height, BufferedImage.TYPE_4BYTE_ABGR);
    WritableRaster wr = b.getRaster();
    int[] color = {r, g, b, a};
    wr.setPixel(x, y, color);
    ImageIO.write(b, "png", new File("filename.png"));
    ````
    
    > The testing server currently runs javac 1.10.

Python
:   The relevant library is [pillow](http://python-pillow.org/).
    To install, do `pip install pillow`{.bash} or `pip3 install pillow`{.bash} from the command line.
    
    The typical import is `from PIL import Image`{.python}.
    Do not use the `ImageDraw`{.python} module.
    
    ````python
    # ... set width, height, etc.
    img = Image.new("RGBA", (width, height), (0,0,0,0))
    
    # slow way:
    img.im.putpixel((x,y), (r,g,b,a))
    
    # not quote as slow way:
    putpixel = img.im.putpixel # do once only
    putpixel((x,y), (r,g,b,a)) # repeat as needed
    
    img.save("filename.png")
    ````
    
    > The testing server currently runs python 3.7.0.
    > pypy 3.5.3 is also installed and can be switched to if a version compatibility issue is identified. 

Want another language added?  Let me know so I can build my grading harness for it.


## Keywords

png *width* *height* *filename*
:   Every file will begin with a line `png` followed by two positive integers, *width* and *height*, and a *filename*.
    You should write a RGBA png image of the specified width and height (see [Image file creation]).
    You should write the file in the default directory.
    The initial color of every pixel in the image should be transparent black (0, 0, 0, 0).
    
    You may assume the filename contains only non-whitespace ASCII characters and already has the appropriate ".png" ending.
    
    You may assume that png will always be the first valid keyword in the file.

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


## Examples

Input file [hw0ex1.txt](files/hw0ex1.txt):

    png 5 8 hw0ex1.png
    xy 0 1
    xyrgb 1 2 127 255 255
    xyc 2 3 #aaaaff
    xy 3 4
    xyrgb 4 5 200 120 3
    xyrgb 3 3 0 0 0
    xyrgb 2 4 0 0 0

should produce this image file: <img src="files/hw0ex1.png" style="height:1em;"/>.
That's so small it's almost impossible to see, so let's zoom in and put a striped background behind the image so you can tell the difference between transparent and white:

<img style="width:5em" class="demo" src="files/hw0ex1.png"/>

# Submission and Feedback

The [submission site](https://kytos.cs.virginia.edu/graphics/) for this assignment (only)
will run automated tests and add information about their outcomes to the submission file list.
There may be a small delay before it is visible, as we queue each submission as it comes in.
Feel free to re-submit until you get positive status results.
Please refer questions to piazza or professor office hours.
