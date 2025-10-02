---
title: Perpetually Obsolete
summary: An observation about every introductory graphics course everywhere.
...

Question
:   How much of the content of this course is the latest and greatest?

Answer
:   None of it; we're mostly teaching a subset of 2008 technology, where the subset was picked in 2012 and wrapped in the API we'll use in 2017

Question
:   Why not the latest and greatest?

Answer
:   So many reasons...

# Hardware and Drivers

Suppose I decided to teach a course on the very latest technology available.
The problem is "available" is a relative term in graphics.
Unlike many other fields in computing, the latest interactive graphics techniques generally require hard investment:
cutting-edge graphics cards, latest operating systems, patched drivers, etc.
Of course, many courses require students to invest in textbooks or other supplies
and we could too,
but the latest tech for graphics dwarfs those expenses by a wide margin.

Instead, we're using a very widely available tech, WebGL2.
Part of its wide availability is achieved by its being based on old tech:
several years old when it was released[^age]
and released several years ago.
It is also based on a simple subset of available tech: tessellation, geometry, and compute shaders were common when WebGL2 was released but were not included in WebGL2 in part to make it smaller and easier to implement on resource-constrained platforms.

Thus, one reason we're teaching older tech is that it's the newest tech that we know you can all access.

[^age]:
    WebGL 2.0 was released in January 2017.
    
    OpenGL ES 3.2 had been out for a year and a half when WebGL 2.0 was released, but WebGL 2.0 was based on the then-five-year-old OpenGL ES 3.0 instead.
    
    OpenGL 4.3 was released the same day as OpenGL ES 3.0, but OpenGL ES 3.0 was based on the then-three-year-old OpenGL 3.0 instead.
    
    Vulkan was released a year before WebGL 2.0, but WebGL was still based on the then-twenty-five-year-old OpenGL line instead.
    
    Each of these not-the-latest decisions increased ease and likelihood of adoption,
    provide assurance that the underlying tech as robust in practice,
    and allowed user experience to guide what parts of the previous tech to include and what to exclude.
    
    WebGPU, a probable successor to WebGL based on Vulkan, is <time datetime="2025-06-01" title="June 2025">currently</time> in a usable but still developing state with [limited implementation](https://github.com/gpuweb/gpuweb/wiki/Implementation-Status) and several important [milestones still pending](https://github.com/gpuweb/gpuweb/milestones).
    At some point it will become a stable standard fully implemented by multiple web rendering engines.
    Once it is widely supported we expect the curriculum of this course to be updated to use it.
    
    

# Teachability

The latest and greatest advances are made by people deep in the current technology and described for other people deep in the space to consume.

Specs
:   The official specifications for each standard is a stand-alone document, but not good learning material.

Release guides
:   Sometimes when new releases are made they are accompanied by a collection of "what's new" documents
    and "here's something you can now do" demos
    which help people who knew the previous version
    learn the new version.

Tutorials
:   Tutorials help you get started without having to puzzle through official specs or re-tread decades of history.
    They typically are organized around a series of example programs with some explanation.
    They are a great way to learn how to operate, but they tend to get stale:
    when new features are added it takes significant work to go back through a tutorial and change all the examples to use it,
    and even when that work is done it often leads to code no professional would be proud of with archaic designs ported to use current tech.
    Many, though not all, tutorials also omit context, limiting learners' ability to go beyond the tutorials' scope
    and making future changes come as surprises.

Courses
:   Courses like this one are similar to tutorials
    but with more emphasis on context, principles, and explanations
    and less emphasis on current best practices.
    The hope is they provide greater forward flexibility and ability to go beyond what is directly covered.

There's a lag in each of these steps representing the additional cognitive effort needed to create the later items.
Specs are generally stable for several months before release guides are produced;
for more than a year before tutorials are created;
and for several years before courses are ready.
However, their duration of usefulness follows a similar trend:
old specs are rapidly obsolescent,
old release guides remain useful for a year or two,
old tutorials remain useful for several years,
and old courses can remain useful for decades^[I took computer graphics in college in 2004; roughly ⅔ of that content is still relevant in 2025.]

# Change

Computer graphics is fortunately still in a space with strong competition.
At the time of writing (2025) we have

- API competition (Vulkan, DX12, and Metal in the lead, others as well)
- Hardware competition (Nvidia, AMD, and Intel in the lead, others as well)
- Engine competition (Unreal Engine, Unity, Gdot, and CryEngine in the lead, *many* others as well)
- Application competition (far too many to list or tell what's in the lead)

This diversity of options may seem annoying for someone having to choose between similar-sounding options, but it fosters a rapid growth in technology at all levels. Without competition development tends towards the "safe" options, favoring keeping current customers over attracting new ones. But with competition every company has a vested interest in getting something new out that can give them an advantage over others, resulting in a much more rapid pace of development.

One result of this is that by the time you finish a multi-year development project (or multi-year degree program), odds are that even if you started working with the very latest tech available, something new has come along during the process and it is not longer the latest tech when you're done.

Perpetual obsolescence is one side effect of a healthy, thriving field.
