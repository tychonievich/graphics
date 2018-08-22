/**
 * A minimal 8- and 16-bit truecolor-with-alpha PNG writer based on the spec 
 * available at http://www.w3.org/TR/PNG
 * 
 * Standards: Intended to conform to ISO/IEC 15948:2003 (E)
 * 
 * Authors: Luther Tychonievich
 * 
 * Date: 2013-12-31
 * 
 * Copyright: Public Domain
 * 
 * License: use freely for any purpose; provided "as is" without any warranty 
 * of any kind, either express or implied, including, but not limited to, the 
 * implied warranties of merchantability and fitness for a particular purpose.
 * 
 * 
 * 
 * Suggested Use:
 * 
 * For most uses, the Img struct is all you'll need.
 * ----
 * auto im = Img!ubyte(width, height);    // creates an 8-bit RGBA PNG image
 * im[x, y] = [255, 0, 0, 255];           // sets a pixel to opaque red
 * im[x, y] = [1.0, 0.0, 0.0, 1.0];       // sets a pixel to opaque red
 * ubyte r = im[x, y].red;                // gets the red color, 255 in this case
 * ubyte r = im[x, y][0];                 // gets the red color, 255 in this case
 * size_t w = im.width, h = im.height;    // gets dimensions
 * im.save("filename.png");               // only .png supported
 * ----
 * 
 * The Img struct is mostly just convenience wrappers; the encode functions
 * and their dependencies do the actual work, and can be called directly if desired.
 * 
 */
module minipng;

import std.bitmanip;
import std.zlib;
static import std.math;


// CRC code adapted from http://www.w3.org/TR/PNG
uint crc_table[256];
bool crc_table_computed = false;
void make_crc_table() {
	foreach(n; 0..256) {
		uint c = n;
		foreach(k; 0..8)
			if ((c&1) != 0) c = 0xedb88320u ^ (c>>1);
			else c >>= 1;
		crc_table[n] = c;
	}
	crc_table_computed = true;
}
uint crc(ubyte[] buf) { 
	if (!crc_table_computed) make_crc_table();
	uint crc = uint.max;
	foreach(b; buf) crc = crc_table[(crc^b) & 0xff] ^ (crc>>>8);
	return ~crc;
}
// end CRC code


ubyte paeth(ubyte a, ubyte b, ubyte c) {
	int p = a+b-c;
	int pa = std.math.abs(p-a);
	int pb = std.math.abs(p-b);
	int pc = std.math.abs(p-c);
	if (pa<=pb && pa<=pc) return a;
	if (pb<=pc) return b;
	return c;
}

ubyte[] filter(ubyte[] row, int stride, ubyte[] above, int type, out uint heuristic) 
in {
	assert(row.length > 0, "must have a row to filter");
	assert(row.length % stride == 0, "row must be multiple of stride bytes long");
	assert(type >= 0 && type <= 4, "only 5 types are defined");
	assert(above.length == row.length || (above.length == 0 && type <= 1), "above row needed for filter type " ~ cast(char)('0'+type));
} body {
	heuristic = 0;
	switch(type) {
		case 0: // none
			foreach(b; row) heuristic += b;
			return row.dup;
		case 1: // sub
			ubyte[] ans = new ubyte[row.length];
			foreach(i; 0..stride) {
				ans[i] = row[i];
				heuristic += ans[i];
			}
			foreach(i; stride..row.length) {
				int diff = row[i] - row[i-stride];
				heuristic += std.math.abs(diff);
				ans[i] = cast(ubyte)(diff&0xff);
			}
			return ans;
		case 2: // up
			ubyte[] ans = new ubyte[row.length];
			foreach(i; 0..row.length) {
				int diff = row[i] - above[i];
				heuristic += std.math.abs(diff);
				ans[i] = cast(ubyte)(diff&0xff);
			}
			return ans;
		case 3: // average
			ubyte[] ans = new ubyte[row.length];
			foreach(i; 0..stride) {
				int av = above[i]>>1;
				int diff = row[i] - av;
				heuristic += std.math.abs(diff);
				ans[i] = cast(ubyte)(diff&0xff);
			}
			foreach(i; stride..row.length) {
				int av = (cast(int)(above[i]) + cast(int)(row[i-stride]))>>1;
				int diff = row[i] - av;
				heuristic += std.math.abs(diff);
				ans[i] = cast(ubyte)(diff&0xff);
			}
			return ans;
		case 4: // paeth
			ubyte[] ans = new ubyte[row.length];
			foreach(i; 0..stride) {
				ubyte p = paeth(0, above[i], 0);
				int diff = row[i] - p;
				heuristic += std.math.abs(diff);
				ans[i] = cast(ubyte)(diff&0xff);
			}
			foreach(i; stride..row.length) {
				ubyte p = paeth(row[i-stride], above[i], above[i-stride]);
				int diff = row[i] - p;
				heuristic += std.math.abs(diff);
				ans[i] = cast(ubyte)(diff&0xff);
			}
			return ans;
		default:
			assert(false, "unknown type");
	}
}




ubyte[] encode(I=ubyte, T)(T[4][][] img) 
if ((is(T == float) || is(T == double) || is(T == real)) && (is(I == ushort) || is(I == ubyte))) {
	I[4][][] simg = new I[4][][img.length];
	foreach(x ; 0..img.length) {
		simg[x] = new I[4][img[x].length];
		foreach(y ; 0 .. img[x].length) {
			foreach(c ; 0..4) {
				T val = img[x][y][c];
				simg[x][y][c] = val <= 0 ? 0 : val >= 1 ? I.max : cast(I)(I.max*val);
			}
		}
	}
	return encode(simg);
}

ubyte[] encode(T)(T[4][][] img) if (is(T == ushort) || is(T == ubyte)) 
in {
	assert(img.length > 0 && img[0].length > 0, "cannot encode a zero-pixel image");
	foreach(row; img) assert(row.length == img[0].length, "must be rectangular");
} body {
	
	ubyte[] ihdr = [0,0,0,13, 73,72,68,82, 0,0,0,0, 0,0,0,0, 8*T.sizeof, 6,0,0,0];
	ihdr[8..12] = nativeToBigEndian(cast(uint)(img.length)); // width
	ihdr[12..16] = nativeToBigEndian(cast(uint)(img[0].length)); // height
	
	// 4.5.3: scanline serialization, 7.2 scanlines
	ubyte[][] scanlines;
	ubyte stride;

	scanlines = new ubyte[][img[0].length];
	stride = T.sizeof*4;
	foreach(r; 0..img[0].length) {
		scanlines[r] = new ubyte[img.length*stride];
		foreach(c; 0..img.length) 
			foreach(i; 0..4)
				scanlines[r][c*stride+i*T.sizeof .. c*stride+(i+1)*T.sizeof] 
					= nativeToBigEndian(img[c][r][i])[];
	}

	// 4.5.4: filtering
	// per 12.8, using heuristic minimize sum(abs(row)) after filtering
	ubyte[] imagedata;
	uint[5] h;
	ubyte[][5] rows;
	// first row: only 0 or 1 are options (spec allows others, but never best)
	rows[0] = filter(scanlines[0], stride, null, 0, h[0]);
	rows[1] = filter(scanlines[0], stride, null, 1, h[1]);
	if (h[1] < h[0]) {
		imagedata ~= 1;
		imagedata ~= rows[1];
	} else {
		imagedata ~= 0;
		imagedata ~= rows[0];
	}
	foreach(line; 1..scanlines.length) {
		ubyte besti = 0;
		uint besth = uint.max;
		foreach(ubyte type; 0..5) {
			rows[type] = filter(scanlines[line], stride, scanlines[line-1], type, h[type]);
			if (h[type] < besth) { besti = type; besth = h[type]; }
		}
		imagedata ~= besti;
		imagedata ~= rows[besti];
	}
	

	// 4.5.5: compression
	ubyte[] compressed = cast(ubyte[])compress(imagedata, 6);
	
	// 4.5.6: chunking (ignored; leave it all in one chunk)
	
	// ===== 4.7, 5: datastream ===== //
	ubyte[] datastream = [137, 80, 78, 71, 13, 10, 26, 10]; // 5.2: signature
	
	// 11.2.2: IHDR chunk
	ihdr ~= nativeToBigEndian(crc(ihdr[4..$]));
	datastream ~= ihdr;
	
	// 11.2.4: IDAT
	ubyte[] idat = nativeToBigEndian(cast(uint)(compressed.length));
	idat ~= [73, 68, 65, 84];
	idat ~= compressed;
	idat ~= nativeToBigEndian(crc(idat[4..$]));
	datastream ~= idat;
	
	// 11.2.5: IEND
	ubyte[] iend = [0,0,0,0, 73,69,78,68, 174,66,96,130];
	datastream ~= iend;
	
	return datastream;
}

/** Not really necessary, but makes it easier to make a 2D array of colors.
 * 
 * Usage:
 * ----
 * auto img = Img!ubyte(width, height);
 * ubyte r = img[8,3][0]; // the red byte for pixel (8,3)
 * ubyte g = img[8,3].green; // the green byte for pixel (8,3)
 * img[x,y] = [255,127,0,255]; // sets pixel to opaque orange
 * img[x,y] = [1.0, 0.5, 0.0, 1.0]; // sets pixel to opaque orange
 * // note: there is no floating-point color reading, just setting
 * img.save("filename.png");
 * ----
 */
struct Img(T) {
	T[4][][] raster;
	this(uint w, uint h) {
		raster = new T[4][][w];
		foreach(x; 0..w) raster[x] = new T[4][h];
	}
	ref T red(uint x, uint y) { return raster[x][y][0]; }
	ref T green(uint x, uint y) { return raster[x][y][1]; }
	ref T blue(uint x, uint y) { return raster[x][y][2]; }
	ref T alpha(uint x, uint y) { return raster[x][y][3]; }
	pixel color(size_t x, size_t y) { 
		return pixel(&raster[x][y]); 
	}
	pixel opIndex(size_t x, size_t y) { return color(x,y); }
	void opIndexAssign(R)(auto ref R v, size_t x, size_t y) { color(x,y) = v; }
	struct pixel {
		import std.traits : isIntegral, isFloatingPoint;
		T[4]* data;
		private static T clip(R)(R i) if (isIntegral!R) { return cast(T)(i<0?0:i>T.max?T.max:i); }
		private static T clip(R)(R i) if (isFloatingPoint!R) { return clip(i*T.max); }
		
		ref T red() { return (*data)[0]; }
		ref T green() { return (*data)[1]; }
		ref T blue() { return (*data)[2]; }
		ref T alpha() { return (*data)[3]; }
		ref T opIndex(size_t i) { return (*data)[i]; }
		
		void red(R)(R i) { (*data)[0] = clip(i); }
		void green(R)(R i) { (*data)[1] = clip(i); }
		void blue(R)(R i) { (*data)[2] = clip(i); }
		void alpha(R)(R i) { (*data)[3] = clip(i); }
		void opIndexAssign(R)(R v, size_t i) { (*data)[i] = v; }
		
		void opAssign(R)(R[4] color...) { red = color[0]; green = color[1]; blue = color[2]; alpha = color[3]; }
		void opAssign(R)(R[3] color...) { red = color[0]; green = color[1]; blue = color[2]; alpha = T.max; }
		void opAssign(R)(R[] color...) { red = color[0]; green = color[1]; blue = color[2]; alpha = color.length > 3 ? color[3] : T.max; }
		void opAssign(R)(pixel color) if (is(R : pixel)) { (*data)[] = (*color.data)[]; }
	}
	
	size_t width() const { return raster.length; }
	size_t height() const { return raster[0].length; }
	
	void save(string path) {
		static import std.file;
		std.file.write(path, encode(raster));
	}
}

