// To compile this file, run the following:
//   g++ cimg_example.cpp -lpng -lX11 -lpthread -o myprogram.exe
//
// Note that you will need CImg.h, which can be downloaded from
// http://cimg.sourceforge.net.

// Note that -lX11 is only necessary on linux (other OSs may need to include
// other libraries for the CImg<T>.display() function to work, see
// http://cimg.sourceforge.net for documentation).

// This define tells cimg to include functions for writing png files
// Similarly, we could use '#define cimg_use_jpeg' to include jpeg-writing
// support.
// However, when we do this, we must link against libpng (and/or
// libjpeg). To do this, add a '-lpng' or '-ljpeg' to the gcc command.
#define cimg_use_png
#include "CImg.h"

using namespace cimg_library;

int main(int argc, char** argv) {
    int width = 512;
    int height = 512;
    int depth = 1;
    int spectrum = 4;

    // Create an image where each pixel is represented as a 32-bit int.
    // We could also use CImg<float> to define an image of 32-bit floats.
    // Notice that CImg represents 4d images, but for most purposes, we
    // will use a depth of 1.
    CImg<unsigned char> myImage(width, height, depth, spectrum);

    // Set all pixels to 0
    myImage = 0;

    // Loop over the "spectrum" of the image (red = 0, green = 1, blue = 2, alpha = 3)
    for (int c = 0; c < myImage.spectrum(); c++) {
        int x = myImage.width() / 2;
        int y = myImage.height() / 2;
        int d = 0;
        myImage(x, y, d, c) = c % 256; // some random intensity
    }

    // Display the image...
    // myImage.display();

    myImage.save_png("output.png");

    return 0;
}

