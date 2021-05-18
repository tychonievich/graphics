---
title: Computer Graphics
...

<img id="icon" class="face" src="files/redchair0.png"/>
<script type="text/javascript">
var icon = document.getElementById("icon");
icon.setAttribute("src", "files/redchair"+Math.floor(Math.random()*6)+".png");
</script>

# Meetings

Course meetings are Mondays and Wednesdays 2–3:15 (eastern time).
A room has not yet been assigned to this course.

Office hours have not yet been selected for this course.

# Overview 

This course explores the algorithms, data structures, 
and techniques used to cause computers to generate visual outputs.
It is not a course about 3D modeling, animation or other content-creation topics
but rather about the computational aspects of turning that content
into images.

The first half of this course will be the basic topics
that every computer graphics course should cover:
the core algorithms and techniques for creating images from models.
The second half will have more flexibility,
going into more detail on a topic such as model representation,
visual-quality physics simulation, high-dimensional visualization,
or advanced topics in real-time or realistic 3D graphics.
Details of second-half curriculum will be based in part on student input.

# A note about getting help

This course is taught on a sporadic basis and generally lacks experienced TAs.
It was taught a year ago, so we might have more TAs than usual this semester, but I cannot yet guarantee that.
Additionally, we commonly have half a dozen different languages being used by students to write assignments.
The course involves a lot of coding and often has a large enrollment.

Ergo, you should expect to have little if any assistance debugging your code.
I'll be able to help with graphics questions (e.g., "that horizontal banding on your image means your DDA implementation is rounding wrong") but likely that is all.

If you are uncomfortable about the idea of working with minimal support, you should probably select a different course that uses a single programming language and has full TA staffing.

# Is this the right class?

--------------------------------------  ---------------------------------------
I have not yet finished CS 2150/DSA1    No. We'll need its coverage of data structures
                                        and the experience if provides in self-guided development.

I have not yet finished CS 4102/DSA2    Maybe; the assignments won't use these much, 
                                        but the concepts will be discussed often in class.

I want to write code                    Yes! Lots of that here! Most students will
                                        submit code containing more than 2,500 
                                        original statements (lines vary by language).

I want to design special effects        Yes, we'll talk about lots of them!

I want to make movies                   Movies are made mostly by artists, 
                                        actors, and technicians. We will talk
                                        about how to make the software CG 
                                        artists use...

I want to make games                    [CS 4730](https://cs4730.cs.virginia.edu/) is a better fit.
                                        We will talk some about how game engines 
                                        draw things on the screen.

I want to learn OpenGL, Direct3D,       We'll skim some of these, but not a
Metal, Vulkan, ...                      deep dive.

I want to learn Allegro, Banshee,       We may discuss how they are built, but not
C4, CryEngine, Intrinsic, OGRE, SDL,    how to use them.
Serious, Source, Torque, Unity, Unreal,
UX3D, Xenko, XNA, ...

I want to learn Maya, 3DS Max,          Not a topic of this class, sorry.
Blender, Rhino, Wings, A:M, ZBrush,     Try [Arch 5420](https://www.arch.virginia.edu/arch5420)
Nendo, XSI, SketchUp, ...               or [Arch 5422](https://www.arch.virginia.edu/arch5422).

I'm not very technical, this sounds     The technology of art is quite
artsy                                   technical. Sorry.

I'm interested in computer vision       Not part of this course.
                                        Computer vision is sometimes offered as a CS 4501.

I didn't do well in calculus            That's fine; we need the ideas, but
                                        not the techniques.

I don't know what calculus is           [Fixable with a bit of reading](https://en.wikipedia.org/wiki/Integral).

I'm not very good with vectors          Vectors are important. We'll help, but
                                        you'll want to brush up on your own.

I'm intrigued by numerical stability    We don't have proper courses on these
and computational geometry              topics from the programmer's perspective,
                                        but this class will whet your appetite.
--------------------------------------  ---------------------------------------

