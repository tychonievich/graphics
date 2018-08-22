// Purposely disable a whole bunch of stuff this low-level example doesn't use.
#define MINIZ_NO_STDIO
#define MINIZ_NO_ARCHIVE_APIS
#define MINIZ_NO_TIME
#define MINIZ_NO_ZLIB_APIS
#include "minizpng.h"

#include <stdio.h>

typedef unsigned char uint8;
typedef unsigned short uint16;
typedef unsigned int uint;

typedef struct {
  uint8 r, g, b, a;
} rgba_t;

typedef struct {
  uint w,h;
  uint8 *img;
} img_t;

uint8 *red(img_t img, int x, int y) { return img.img + (4*(x+y*img.w) + 0); }
uint8 *green(img_t img, int x, int y) { return img.img + (4*(x+y*img.w) + 1); }
uint8 *blue(img_t img, int x, int y) { return img.img + (4*(x+y*img.w) + 2); }
uint8 *alpha(img_t img, int x, int y) { return img.img + (4*(x+y*img.w) + 3); }

img_t allocImage(uint w, uint h) {
  img_t ans;
  ans.w = w;
  ans.h = h;
  ans.img = (uint8 *)malloc(w*h*4);
  return ans;
}
void freeImage(img_t img) {
  if (img.img) {
    img.w = img.h = 0;
    free(img.img);
    img.img = NULL;
  }
}

void writeImage(img_t img, const char* fname) {
    size_t png_data_size = 0;
    void *pPNG_data = tdefl_write_image_to_png_file_in_memory(img.img, img.w, img.h, 4, &png_data_size);
    if (!pPNG_data)
      fprintf(stderr, "tdefl_write_image_to_png_file_in_memory() failed!\n");
    else
    {
      FILE *pFile = fopen(fname, "wb");
      fwrite(pPNG_data, 1, png_data_size, pFile);
      fclose(pFile);
      printf("Wrote %s\n", fname);
    }
    mz_free(pPNG_data);
}

