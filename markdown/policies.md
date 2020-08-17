---
title: Policies
...

> "A syllabus is just a list of words they don&rsquo;t know yet."
> <div>---Seth Reichelson</div>

# Course objectives

At the end of this course you will be able to do two broad classes of things:
first, you will learn to write algorithms that create images from models;
second, you will learn to effectively understand the capabilities, limitations and vocabulary that underly common graphical libraries.
In addition to these two core classes of learning objectives
we will explore a few more specialized topics,
some of which you will be able to select.

In part because of the ability you will have to influence course topics,
this document is very much open to being adjusted as the semester progresses.

# Logistics

## Meetings

> "The pain of parting is nothing to the joy of meeting again." 
> <div>---Charles Dickens</div>

This course will be taught online.
It will be delivered synchronously so that you can interact with me, asking questions and the like;
it will also be recorded for later viewing.
Grades will never be associated with synchronous presence.

I've requested a classroom we can use to display visual phenomena that do not capture well via camera.
I have not yet heard if such a classroom will be provided.
If it is, use of it will be scheduled, limited to small numbers at a time, and optional.

There is no lab or discussion session.
I do not schedule review sessions or the like outside of usual class time.

## Tasks

> "Some college cell, Where muzzing quizzes mutter monkish schemes."
> <div>---William Roberts</div>

You will be asked to write and turn in four or five programs:

#. a basic 2D rasterizer

#. a basic 3D rasterizer

#. a basic raytracer

#. (probably) a basic WebGL program

#. an additional program based on the latter part of the course

Additionally, quizzes will be administered online frequently.
There will be a final quiz, which I traditionally administered in-person;
I have not yet determined how to adjust that for remote delivery.

## Contact

> "I heard a sound; I turned around; I turned around to face the thing that made the sound."
> <div>---They Might Be Giants</div>

We are likely to use Discord as the primary communication medium in this course.
Details will appear here once determined.

## Readings

> "When you read books your eyeballs wither away leaving the bare sockets"
> <div>---Yang Wanli</div>

Reading materials will be selected from various web pages, articles, and the like. There is no course textbook.
Readings may be roughly categorized into two kinds.

-   Conceptual readings will provide background and understanding of course concepts, 
	including both how algorithms work at a high level
	and why they are designed as they are.
	Conceptual readings are important to the course,
	should be read prior to class meetings,
	and may be used as the source material for quizzes.
	I anticipate conceptual readings will occupy in the neighborhood of 2 hours per week, varying by individual and by week.

-	Reference readings are more applied <q>how-to</q> kinds of material
	that I believe will assist you in completing the coding assignments.

## Coding

> "If you really want to understand something, the best way is to try and explain it to someone else. That forces you to sort it out in your own mind. And the more slow and dim-witted your pupil, the more you have to break things down into more and more simple ideas. And that’s really the essence of programming. By the time you’ve sorted out a complicated idea into little steps that even a stupid machine can deal with, you’ve certainly learned something about it yourself."
> <div>---Douglas Adams</div>

Most assignments will be supported in any language you chose to use.
In the past I have supported C++, C#, D, Java, Kotlin, Python, and Rust.
You may switch languages as often as you wish.
If you want another language added, let me know.

One assignment will explore low-level 3D graphics library use,
probably either WebGL in Javascript
or Vulkan in C++.
Assuming that plan does not change, we'll have a tutorial on the necessary bits of those languages in class prior to the assignment.

Estimating how long it will take someone to complete a coding assignment
is always difficult.
The target difficulty is 5–10 hours of focused effort each week.

# Grading

> "I find that I go up and down, and back and forth as well;<br/> I move so freely left and right, it seems quite dull to tell.<br/> I also can move later; I move hours every day;<br/> But moving former stumps me hard; I cannot find a way.<br/> Of eight directions on the test, I fear that I've missed one;<br/> And eighty-se'en percent is just a B‍‍, which is not fun.<br/> I think I'm good at motion; I'm a farily agile bloke;<br/> Perhaps the standard grading scale is just a nasty joke."
> <div>--Luther Tychonievich</div>

[Grading](http://www.cs.virginia.edu/tychonievich/blog/posts/244.html) is one of the aspects of a course that instructors enjoy even less than students. Still, we are stuck with them, so here goes.

Task | Weight | Comments
-----|--------|-----------------------------------------------------------------
Quizzes     | 25% | Acceptance of late submissions and/or dropping some scores will be implemented
Assignments | 50% | Approximately 10% each, but you'll have some point flexibility between them.  Extra credit in assignments will not transfer over to quizzes or final.
Final Quiz  | 25% | The intent is to make this a second try on the mid-semester quizzes' questions

Your final grade is computed based on the percentage of points you have earned and is designed to match the GPA value of each letter. For reasons I do not understand, that is not a linear scale: for example, `A-` &minus; `B+` = 0.4 grade points while `B+` &minus; `B` = 0.3 grade points. For reasons even farther from my ken, the most common grading scale I have seen is also not linear but differently spaced than the grade points. Following is a scale spaced like the grade point scale:



You get     if you score     Which is worth
----------  ------------    ----------------
A+          near the top           4.0
A           &ge; 93%               4.0
A&minus;    &ge; 90%               3.7
B+          &ge; 86%               3.3
B           &ge; 83%               3.0
B&minus;    &ge; 80%               2.7
C+          &ge; 76%               2.3
C           &ge; 73%               2.0
C&minus;    &ge; 70%               1.7
D+          &ge; 66%               1.3
D           &ge; 63%               1.0
D&minus;    &ge; 60%               0.7
F           otherwise              0.0


I do not round grades. 92.99999919% is not &ge; 93% and is thus an A&minus;, not an A.

I do not curve grades: if you all fail, you all fail; if you all ace, you all ace. However, rubrics for assignments are not linear: instead, I determine how well I expect a passing student to perform and assign a per-assignment rubric to match.

# Miscellanea

## Professionalism

Behave professionally.

Never abuse anyone, including the emotional abuse of blaming others for your mistakes.
Kindness is more important than correctness.

If we have TAs, let them be students when they are not on the clock as TAs.

## Honesty

We always hope everyone will behave honestly.
We know we all are tempted to do what we ought not;
if you do something you regret, the sooner you tell us the sooner (and more leniently) we can correct it.

### No plagiarism (nor anything like it)

If you consult resources other than course material in the performance of any course assessment (including quizzes and homeworks),
you **must** cite any and every source you consult in the comments of the quiz question or program file.
Talked to a friend, saw an interesting video, consulted a website, had a tutor?
Tell us!

### Obey collaboration limitations

Quizzes may not be done in groups or in consultation with any resource that did not exist prior to the quiz being posted.

Code must be written on your own.
Do not show or read your code to anyone other than course staff.
Do not seek out or view others' code, in or out of the class.

Remember: we don't care about your code or quizzes in and of themselves;
we know the answers and have reference implementations already.
What we care about is the changes that occur in your mind as you work on them.
Don't cheat yourself out of the gains these assessments are designed to provide.

### Consequences of Dishonesty

If we believe you have acted dishonestly, we will communicate this fact to you and propose a penalty.
If you have information we lack, please share that with us; we may thereafter change our belief and/or proposed penalty.

If we are not able to come to an agreement, or if the case is particularly egregious and beyond our comfort level handling in-course, we will instead refer the case to the University Honor System and abide by their findings.


## Personal accommodations

### Disability

If you qualify for accommodations from [the SDAC](http://studenthealth.virginia.edu/sdac), please let your professor know, preferably in a private conversation so we can discuss how your accommodations will interplay with the content delivery and assessment structure of this course.

### Religious observances

We fully support [the university's stance](https://eocr.virginia.edu/accommodations-religious-observance) on accommodating religious observances.
If such observances or other religious beliefs impact or are likely to impact your work this semester,
please let us know as soon as you are aware of this impact.

### Culture

All communication relies on shared context and understanding.
Because no member of our course staff has the same context and experience as you, it is likely we will inadvertently say and do things you find confusing or offensive. Please let us know if this happens! We will do our best to learn and adjust so we can become better and more welcoming communicators in the future, and to do what we can to fix any problems our mistakes caused.

### Life

Bad things happen.
People forget things and make mistakes.
Bad days coincide with due dates.
Students and their loved ones get sick.
Etc.

If you believe that circumstances warrant an change in deadline, a second chance, or some other accommodation in order to more accurately synchronize grade with knowledge, talk to your professor and we'll resolve the situation as best we can.
