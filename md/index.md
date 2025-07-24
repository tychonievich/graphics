---
title: CS 418
subtitle: Interactive Computer Graphics
summary: |

  <center>
  `https://courses.grainger.illinois.edu/cs418`
  </center>
  
  <center>
  [Content](content.html)  
  [Quizzes](https://us.prairielearn.com/pl/course_instance/182443)  
  [MPs](mp/)  
  [Submit](https://cs418.cs.illinois.edu/sudmit/)  
  [Text](text/)  
  [Video](https://classtranscribe.illinois.edu/offering/c7e741f2-d482-496e-ba57-0285d39ccedb) 
  </center>
...

This offering of CS 418 "Interactive Computer Graphics" is being offered in a way designed specifically to cater to our online MCS program.
As such, both in-person and online students will be expected to consume course material in an asynchronous online form.
Office hours will also be held online, are optional, and will be the only synchronous component of the course.

<details class="note"><summary>About Coursera</summary>

Courses for the online MCS are generally offered via Coursera.
Content on Coursera for this course is entirely redundant to material on this page;
you never need to use Coursera unless you want to.

If you wish to connect via Coursera,
there's a several-step process for getting your enrollment copied from the campus records to Coursera.
In particular, there are emails generated the day after you enroll you need to read
and an "onboarding course" you have to complete on Coursera before CS 418 will show up.
See [this guide](https://ws.engr.illinois.edu/sitemanager/getfile.asp?id=3552) for more.

</details>


# Course operation

The course consists of the following components:

Pre-recorded lecture material
:   Available on the [course content site](content.html), these are mostly fairly dense videos; I regularly distilled 3 hours of class into 1 hour of video by removing the Q&A and other interactive content. Please make notes of questions as you watch them and post those questions on CampusWire. I may answer them there or record videos explaining the answers and post them as supplementary content.
    
Pre-written lecture notes
:   Available on the [course content site](content.html), these have roughly the same content as the videos, but often differ in level of detail.
    Some video content (such as coding demonstrations) have no corresponding notes.
    
    Please make notes of questions as you read them and post those questions on CampusWire. I may answer them there or write up longer explanations and post them as supplementary content.

Per-module retakable quizzes
:   Lecture material is split into modules, each with a quiz.
    These quizzes are intended primarily as a self-assessment of learning and may be retaken as often as desired.
    
    I understand that some students find quizzes annoying, but experience has shown me they they do help students find and fix gaps in understanding.
    
    These quizzes are administered on [PrairieLearn](https://us.prairielearn.com/pl/course_instance/182443).

Machine problems (MPs)
:   MPs are the primary driver of both learning and assessment.
    You will have a menu of MP options,
    with some "core" that you'll need to complete most of
    and more "elective" that you'll need to complete a selection from.
    There are also two warm-ups intended primarily to smooth the way for subsequent MPs.
    
    Machine problems are submitted on a custom course submission site that provides some limited automated feedback (mostly of the form "did it run on our server"); they are graded primarily by hand.

    Different MPs have different difficulty, with points allocated accordingly.
    See the [MP page](mp) for more.

No Final
:   This class has no final exam/quiz/project/assessment.
   


# Course content

Computer graphics studies how computers can create images.
Interactive computer graphics creates images quickly enough that a new image can be created in response to every user action.
In principle any image-creation algorithm could be interactive, given adequate hardware, but in practice it usually refers to a specific family of workflows involving the interaction of the CPU and GPU.
That family of workflows will be our primary topic in this class.

This course teaches the following in enough detail to implement them yourself:

- How 3D computer graphics works, including both rasterization and raytracing.
- How to use WebGL2, a popular GPU API, to create interactive 3D graphics.
- How to generate your own 3D geometry, render it, texture map it, move it, and move the camera around it, with all of the underlying math and algorithms. 
- How to basic graphical motion simulation and particle effects.

This course teaches various other topics at a lower level of detail, including:

- Shadow maps
- Deferred shading
- Keyframe animation and tweening
- Various fractals
- Various texture mapping techniques
- Physically-based rendering techniques
- Inverse kinematics
- Rigid-body, soft-body, and fluid dynamics

## Related topics

This course does not teach

- OpenGL, Direct3D, Metal, Vulkan
    - WebGL2 is related to them and will help you understand them too.
- Artistic content such as 3D modeling, animation, rigging, texture creation, light setups, etc.
    - [ARTS 340](https://courses.illinois.edu/schedule/terms/ARTS/340) is related to these topics, but hasn't been offered in some time.
    - Parkland College has a sequence of computer animation courses, including [a certficate program in 3D animation software](https://www.parkland.edu/Main/Academics/Departments/Business-Computer-Science-Technologies/Areas-of-Study/Computer-Science-Programs/Digital-Media/Curriculum).
    - The [UIUC chapter of SIGGRAPH](https://siggraph.acm.illinois.edu/) (part of the [ACM RSO](https://acm.illinois.edu/)) sometimes teaches Blender, a tool used for 3D modeling and animation
    - [CS 445](https://courses.illinois.edu/schedule/terms/CS/445) requires students to use Blender for one of the assignments.
- Allegro, Banshee, C4, CryEngine, Godot, Intrinsic, OGRE, SDL, Serious, Source, Torque, Unity, Unreal, UX3D, Xenko, XNA, ...
    - We discuss techniques used to build these tools, but not how to use them.
    - [CS 415](https://courses.illinois.edu/schedule/terms/CS/415) uses one of theses.
    - The [GameBuilders RSO](https://gamebuilders.acm.illinois.edu/) often uses these tools.
- Computer game design
    - [CS 415](https://courses.illinois.edu/schedule/terms/CS/415) teaches this, as do all [GSD courses](http://catalog.illinois.edu/courses-of-instruction/gsd/).
    - The [GameBuilders RSO](https://gamebuilders.acm.illinois.edu/) focuses on this.
- Computer vision
    - [CS 444](https://courses.illinois.edu/schedule/terms/CS/444) covers this topic
- 2D graphics
    - We'll mention some topics in passing, but  [CS 445](https://courses.illinois.edu/schedule/terms/CS/445) is more relevant
- Advanced raytracing, path tracing, importance sampling, and other movie-quality graphics content
    - [CS 419](https://courses.illinois.edu/schedule/terms/CS/419) teaches this, but is offered infrequently.

# Grading

My goal in this class is that you learn.
As it is an elective, I hope most of you are taking it for the same reason.
But I do have a duty to assign grades, so here's how we'll do it.

| Weight | Assessment |
|:------:|:-----------|
| 70%    | MPs        |
| 30%    | Quizzes    |

Numbers are converted to letters linearly with the A−/B+ cut-off at 90%
and the C−/D+ cutoff at 70%; more precisely

```js
const letter_grade = (percentage_earned) => {
    if (percentage_earned <= 60) return 'F'
    let letter = 'DCBA'[Math.floor(percentage_earned/10 - 6)]
    if (letter != 'A' && percentage_earned % 10 > 20/3) letter += '+'
    if (percentage_earned % 10 < 10/3) letter += '-'
    return letter
}
```

MP points come in two groups: core and elective.
Core MP components are mostly things that every graphics students should know,
with some additions that are prerequisite for many other tasks.
Elective MP components go beyond the minimum, and you'll get to pick and chose which ones you do.
The number of MP points of each type you will need,
together with a list of MPs,
can be found on the [MPs overview page](mp/)

# Collaboration

Collaboration includes

- Giving information to others, such as by tutoring, working together, or posting solutions online.
- Receiving information from others, such as from AI systems, websites, tutors, or other students.

My goal in this course is not to have you create working solutions (I already have working solutions, I wrote them before the course began) but rather to have you *learn* enough to be able to create your own working solutions.
As such, you may collaborate on MPs but must obey the following limitations on your collaboration:

- Do not collaborate on quizzes; limit your sources to course material, other pre-made content, and your own work.

- Quizzes have unlimited retakes. Please still think about each question rather than just randomly guessing.

- Type all code yourself; no copy-paste or AI-typed code from others.

- Design and understand all your code.

- If you use any source, pre-existing or dynamic, that was not provided by this course in writing code, cite that source in a comment in your code.


# Prerequisites

Listed prereqs in the course catalog are

CS 225 Data Structures
:   Needed for

    - Experience with C or C++. We won't use those languages, but GLSL which we will use is based on them.
    - Comfort with the idea of pointers, binary encoding of data, and memory.
    - At least three semester of programming experience.
        
    
A linear algebra class
:   Needed for

    - Familiarity with matrices and vectors. We'll use vectors to represent 3D points and matrices to transform them, and also use vectors to represent lists of properties of a point.
    
    We will discuss using large sparse matrices to represent systems of equations and variants of conjugate gradient to solve them. That is rarely usable at interactive speeds, so we won't talk about then in much detail in this class.


MATH 241 Calculus III
:   Needed for

    - Comfort with Euclidean space and the 3D vectors
    - experience thinking in 3D that multivariable calculus provides
    
    There is some calculus in graphics, but mostly as theoretic background for algorithms that do not themselves use the calculus. We'll not need any integral-solving or related by-hand calculus computations in this course.

Analysis of past student performance leads us to identify the following as optional but recommended prerequisites:

CS 340 Introduction to Computer Systems or CS 341 Systems Programming
:   CS 418 is a programming-heavy course, and these courses provide valuable extra training an experience with programming.
    
    We also deal with how the CPU and GPU interact, a topic made much easier if you have had prior computer systems training.

CS 357 Numerical Methods 1
:   This course involves considerable mathematical reasoning; taking CS 357 before it increases increase your experience with mathematically-based programming and is recommended.


# Course Staff

Instructor
:   ---------   -------------------------------------------------
    Name        Luther Tychonievich
    
    Office      2340 Siebel
    
    Phone       +1 217 333 8609
    
    Email       `luthert@...`\
                Include "418" or "graphics" in the subject line
    ---------   -------------------------------------------------

Assistants
:   TBD
    
    This is a smaller staff of assistants than I've had in the past.
    As such, there may be fewer help hours than you'd otherwise hope; if you generally use instructor or assistant help in most programming assignments, this course may not be ideal for you this semester.
    

CampusWire
:   By invitation only. I get daily roster change update digests and enter them into CampusWire when I do.

Office Hours
:   ---------   -----------------------------------------------------------------------------------
    Schedule    <iframe src="https://calendar.google.com/calendar/embed?height=600&wkst=1&bgcolor=%23ffffff&ctz=America%2FChicago&mode=WEEK&showCalendars=0&showTabs=1&showPrint=0&showTitle=1&title=CS%20418%20Office%20hours&src=Y19iZTA5MjdlYmRmZGYxZmM1YjZmOWY1M2M5YWVmOGM5YTQwOTY4OWQ1MzUyMTFhNzNlMTc2NDljMmQ3YTg5NTczQGdyb3VwLmNhbGVuZGFyLmdvb2dsZS5jb20&color=%23A79B8E" style="border-width:0" width="800" height="600" frameborder="0" scrolling="no"></iframe>
    
    Location    [Zoom](https://illinois.zoom.us/j/85360858537?pwd=WDGasda1vmfCb2KdUC0jBbk3aMROVk.1)
                meeting  853 6085 8537  passcode  418
    ---------   -----------------------------------------------------------------------------------

# Textbook

Readings are hosted for free on this site. There is no other textbook required.
