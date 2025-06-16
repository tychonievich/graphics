---
title: Parts of JavaScript We'll Use
summary: Assuming you know Java or C++ and are comfortable learning a language from examples on your own.
...

<style>body { line-height: 150%; }</style>

This is *not* a [full description of JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript). Rather, it is the most important things to know for the JavaScript we'll use, assuming you know Java or C++ already.

# Browser console

We'll run JavaScript as part of web pages.
In that context, JavaScript's primary way of communicating with the user is by modifying something called the <abbr title="Document Object Model">DOM</abbr>, a hierarchy of objects describing the visible contents of the webpage.
We'll use it for that, but during development we want some kind of more direct programmer-centric display.

That programmer-centric display can be found in the "console", which is hidden by default in most browsers. There are two versions of it too: one that just shows output and one that also allows you to directly interact with the webpage through JavaScript.

The common keyboard shortcuts for opening the console include

- F12
- Ctrl+Shift+J
- Ctrl+Shift+K
- Cmd+Opt+J
- Ctrl+Alt+I

It's generally also available from a menu item under a name like "console", "JavaScript console", "browser console", "developer tools", or "web inspector".
It might open in a view with several tabs, only one of which is the console.

If you're in the right console, you should be able to type an expression like `2 + 3` and see the result (`5`).

## Displaying in the console

If you type code in the console, you'll see its result immediately.
If you put code in an HTML or JavaScript file or inside a function, you won't.

There is a global variable named `console` that has methods for putting information into the console.
There are five such methods, each with a different display mode.

Example invocation      Displays as
--------------------    -----------------------
`console.error(0)`{.js} an error icon with redish background; also shows call stack
`console.warn(0)`{.js}  a caution icon with yellowish background; may show call stack, depends on browser
`console.log(0)`{.js}   no icon, no background
`console.info(0)`{.js}  an info icon or no icon, no background
`console.debug(0)`{.js} no icon or background

Consoles also let you pick which kind of messages you want to see, ranging from only errors to all five levels.

All of the console functions are variadic, accepting as many arguments as you wish; for example

```js
console.log("text, number, array", 3+1+4+1+5, [3,1,4,1,5])
```

# Semicolon Insertion

JavaScript uses a syntax inspired by Java, which in turn uses a syntax inspired by C++.
It has a very different semantic model, though, so some parts like type names just get discarded entirely.
It also has something that Java and C++ could have done but didn't:
[automatic semicolon insertion](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar#automatic_semicolon_insertion).

Formally, JavaScript requires semicolons at the end of statements.
Practically, it can almost always figure out where you needed one and add it for you---not by modifying your file, just by pretending you put a semicolon there.

Developers who come to JavaScript from semicolon-requiring languages like Java and Perl tend to include semicolons.
Developers who come to JavaScript from non-semicolon languages like Python and LISP tend to omit semicolons.
I regularly use both semicolon and non-semicolon languages, so my examples might be inconsistent in whether I add semicolons or not.

# Types and Variables

JavaScript is dynamically typed.
That means that the type information is stored with the value, not the variable,
and thus that the same variable can store multiple different types.

```js
x = 3   // x becomes the number `3`
x += 2  // x becomes the number `5`
x = "3" // x becomes the string `"3"`
x += 2  // x becomes the string `"32"`
```

Every value is an object (in the object-oriented sense; JavaScript also uses the word "object" to mean something like a hash map), even those that are primitives in other languages

```js
(2/3).toFixed(3) // the string `"0.667"`
true.constructor // the function that creates Boolean values
```

Variables can be declared using either `var` or `let`.
[`let`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let) creates a variable scoped to the current block (i.e., it will vanish at the closing `}`).
[`var`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/var) creates a variable in scoped to the current function.

```js
let a = null, b = null, c = null, d = null
function f() {
    let a = 1
    var b = 2
    if (true) {
        let c = 3
        var d = 4
        console.log(a,b,c,d) // shows `1 2 3 4`
    }
    console.log(a,b,c,d) // shows `1 2 null 4`
}
f()
console.log(a,b,c,d) // shows `null null null null`
```

Used outside of a function, `var` declares a variable and also puts them into the special "`window`" object.
We can access and modify global variables inside a function using `window.variableName = value`{.js}.[^nuance1]
`let` does not put its variables in the `window` object.

[^nuance1]:
    It is *almost* the case that `window.x` and global-scope `var x` are the same thing.
    The exception occurs in the no-redeclarations rule:
    
    - You can declare `var x` at most once in the global scope,
    but it's OK if that one time happens after `window.x` already exists.
    - You can't have both `let x` and `var x` in the same scope, but you can have a `let x` in the global scope and a separate `window.x`. If you do, `x` will resolve to the `let x`, not the `window.x`.


When you use a variable, JavaScript looks for it in the current scope, then every containing scope, and then in the `window` object, stopping when it finds it.
If it does not find it, it might do one of two things:

- If you are writing to the variable *in strict mode*
    you'll get a reference error.
- If you are writing to the variable and *not* in strict mode
    JavaScript acts like you had used `var` to declare it instead.

Strict mode can be entered by putting the exact statement `'use strict';` *before any other statement* in your file or function.
In most browsers, the console is never in strict mode.

`const` also exists and acts like `let` except it prevents subsequent assignments from changing the value stored in the variable.

# Functions, objects, and so on

Functions can be defined in JavaScript in several ways:

- `function add(x,y) { return x + y }`{.js} -- defines `add` as a function in the same scope that `var add` would.
- `add = function(x,y) { return x + y }`{.js} -- defines a function like any other literal and assigns it to a variable.
- `add = (x,y) => { return x + y }`{.js} -- defines a function like any other literal and assigns it to a variable.
- `add = (x,y) => x + y`{.js} -- defines a function that only has one statement in its body like any other literal and assigns it to a variable.

Technically the functions defined with `function` and those defined with `=>` have some differences, notably when it comes to how they handle the `this` keyword, but we won't need to know those differences for our purposes.


JavaScript has two kinds of "nothing":
`null`{.js}, which you have to set explicitly, and `undefined`{.js},
which is used to indicate something was missing (e.g. `window.qwertyuiop`{.js} is `undefined`{.js}, not `null`{.js}).

There are two kinds of comparison in JavaScript.
The `==` operator checks that values match, and the `===` operator checks that values and types both match.
Notably, numbers and strings can be `==` each other,

```js
3 == "3.0"  // true
3 === "3.0" // false
undefined == null // true
undefined === null // false
```

JavaScript has a built-in dict/map type called "objects", written with braces: `{"one":1, "two":2}`{.js}. Regardless of their type, keys are converted to strings before they are used; values are left as-is.
The usual bracket operator `x[y]`{.js} also has a shorthand version for compile-time-known string-valued keys: `x["thing"]`{.js} and `x.thing`{.js} are synonyms. 

You can use `[]` and `.` on any value type; however, numbers, Booleans, and strings ignore any assignments using these operators.

JavaScript has a built-in list type, written with brackets: `[3,1,4,1,5]`{.js}.
Called "arrays", these are just a special type of "object", meaning you can also treat them like dict/map types, though doing so might result in some unexpected behaviors if they conflict with how the array expects to use its fields.

There is [*much* more to know about objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_Objects),
including [prototypes](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/Object_prototypes), [constructors](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/constructor), polymorphism, method resolution, [the `this` keyword](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this), [calling](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/call) vs [applying](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/apply) methods, [better `Map` objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map), and so on.
We won't need any of that for this course.

# Asynchronous single-threaded code

JavaScript wants to be responsive and have few errors.
Threads tend to result in programmer errors.
Letting code wait for something like a network or file system to return makes things unresponsive.
JavaScript's solution is to have only one thread^[[Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers) allow more, but we won't use them]
and have any code that would normally wait instead return immediately with no results.
These return-before-they're-really-done functions are called "asynchronous".

Code that returns without a result begs the question, how do we get the results?
Unfortunately for us, the answer is "it depends on when the delayed-result function was added to JavaScript".

## Events

JavaScript has a robust event system.
Type a key, press a button or move the mouse and an event is created.
You can request to be informed of events, providing a JavaScript function to be called on each one.
Events are associated with a triggering object and an event name,
so for example to be informed when the mouse is moved while pointing at a button
you'd tell the button object to inform you of [mousemove](https://developer.mozilla.org/en-US/docs/Web/API/Element/mousemove_event) events.

Early asynchronous methods in JavaScript return an object that generates its own events,
such as the [XMLHttpRequest](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest)'s `load`, `error`, and `readystatechange` events.

One we'll use often is the [`window` object's `load` event](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event) which tells us that all the bits and pieces of a webpage are ready for use
and we can start hooking up user input with display canvases without worrying that one or more of the involved components is missing.

```js
window.addEventListener('load', event => {
    // get the gl object for our canvas, which we use to talk to the GPU
    // initiate any setup that depends on it
})
```

## Callbacks

Some functions don't return a value; instead, we pass in to them other functions they should call on success or failure.

The main example of these we'll use is the functions that request a delay, either for a fixed time window or until some event occurs.
If I want to do something, then wait for 20 milliseconds and do it again, and so on forever you might naively expect to write code like

    repeat forever:
        do something
        wait 20 milliseconds

but instead we'll write

```js
function repeatedly() {
    something(...)
    setTimeout(repeatedly, 20)
}
```

Here [`setTimeout`](https://developer.mozilla.org/en-US/docs/Web/API/setTimeout) accepts the name of a function to be called and how long to wait before calling it.
Thus, the `repeatedly` function invokes `something` and then requests that the `repeatedly` function be invoked again in 20ms.

Of particular interest to graphics is the [`requestAnimationFrame` function](https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame)
which will attempt to call its function at a frequency that matches your monitor's refresh rate.
A common model for a continuously changing animation will be

```js
function updateDisplay(milliseconds) {
    let secondsSincePageLoaded = milliseconds / 1000;
    // compute new positions of objects
    // clear the old content
    // draw the new conent
    requestAnimationFrame(updateDisplay)
}
```

If we instead only update the display in response to user input, we can save effort by only updating the display when needed with something like

```js
function userAction(event) {
    // compute new positions of objects
    requestAnimationFrame(updateDisplay)
}
function updateDisplay(milliseconds) {
    // clear the old content
    // draw the new conent
}
```

We don't call `updateDisplay` directly in `userAction` because user actions might arrive more often than the screen refresh can draw them.

## Promises

In 2017 JavaScript gained two new keywords: `async` and `await`,
and with them a new way of handling asynchronous functions.

- If a function is declared as `aync function` it returns an object called a [`Promise`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) before it is done executing.

- There are two ways of getting at the final return value of the function:
    
    - The `Promise`'s `then` function accepts a single-argument function which it calls with the result when ready.
        
        ````js
        fetch(url) // fetch is an async function
            .then((result)=>{ // `()=>{}` creates an anonymous function
                // ... // use the result here
            })
        ````
    
    - Inside an `async function` (and only there) you can use `await` to halt operation until a result is available.

        ````js
        let result = await fetch(url) // fetch is an async function
        // ... // use the result here
        ````

Using `async function` and `await` can lead to much cleaner code than other methods of handling asynchronicity, but `await` can only be used in other `async function`s so if we're not in an `async function` we'll use `then` callbacks instead.

# HTML

Web pages are usually written in Hyper-Text Markup Language (HTML).
HTML is not a full programming language, but it is complicated enough to be larger than we want to explore in full in this course.
It has also gone through various changes over its life, but in a mostly backwards-compatible way, meaning that there's generally several ways to do anything you might wish to do.

## Elements, Tags, and Attributes

Most text can be included in HTML as-is.

Angle brackets delimit **tags**.
An opening tag has an identifier following the opening angle bracket, called the *tag name*.
A closing tag has a slash and then the tag name.
An opening and closing tag pair with the same tag name form an **element**;
anything between the two is a child node of the element.

```html
This is just text
<p>we've now entered an element with tag name "p"</p>
and exited it again
```

Elements may have key-value pairs called **attributes** defined as part of their opening tag.
These consist of an identifier, an equals sign, and a value in quotes
with no intermediate spaces.

```html
<script type="text/javascript" deferred="deferred">
// here we have a script element of the text/javascript type
// it also has a deferred attribute
</script>
```

Some attributes can be given with no value

```html
<script type="text/javascript" deferred>
// same as above
</script>
```

and some types of elements are defined as never having children and hence not needing a closing tag

```html
Some text
<br>
Some more text, not part of a br element because br doesn't need closing
```

and some element types self-close when a new element type that can't be its child is encountered, and some can self-close with a trailing slash in the opning tag, and ... well, HTML has grown complicated over the years.

## Being polite

Every HTML file we write should have the following general structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>The name this tab should have in a browser</title>
    <script>let here = "we have in-line Javascript"</script>
    <script src="other-file.js"></script>
</head>
<body>
    <canvas id="mycanvas" width="500" height="500"></canvas>
</body>
</html>
```

- `<!DOCTYPE html>` lets browsers know we are writing HTML5, not some other version of HTML, and increases the chances they'll display our code correctly
- Except for the DOCTYPE, everything should be in an `html` element
- The `html` element should indicate the language any user-visible text is in to assist in language-specific functionality like hyphenation and screen reading.
- The `head` element must come before the `body` element and should have
    - a `meta` element identifying the character set you write the file in. The correct value here might depend on your text editor, operating system, and locale settings. UTF-8 is recommended if you have the option of changing it.
    - a `title` element to give the webpage a name to show on browser tabs, bookmarks, window title bars, etc
    - some JavaScript in `script` elements, either in-file or referencing a separate file
    - if you add CSS, it goes here too
- The `body` element should have anything that is visible to the user;
    we'll most often use a `canvas` element to display the results of 3D renders.

Note, *most* of these rules cane be bypassed *most* of the time;
browsers work very hard to figure out what you meant if you don't do what you were supposed to do.
Hence, these rules are arguably all rules of politeness rather than rules of necessity.

# Caching and CORS

Web browsers both want to let websites run code on your computer
and want to protect you from the worst kinds of code that might be run.
Servers want to provide some of their information to anyone who wants it,
but some of it they want to limit to use on their own sites.
Browsers want to be fast, only asking a server for information if they don't already have that information on hand.
The policies and practices inspire by these desires can sometimes make developing code in JavaScript more complicated than you'd expect.

## Use a local server

HTML files can be viewed directly from your local disk;
when so viewed, they have a URL beginning `file://`.
However, files viewed that way are less trusted by the browser than those served by a web server with the `http://` or `https://` schemes,
and operations like loading other files into the webpage's memory are unlikely to work.

Instead, you'll need to run a local webserver to test your code with.
This involves two parts:

1. Run a local webserver.
    You'll need to do this from the command line from directory that contains your HTML file.
    
    Pick one of the following:
    
    -  <details><summary>With Python 3</summary>
        
        ````sh
        python -m http.server
        ````
        
        </details>
    
    -   <details><summary>With Python 2</summary>
        
        ````sh
        python -m SimpleHTTPServer
        ````
        
        </details>

    -   <details><summary>With PHP</summary>
        
        ````sh
        php -S [::1]:8080
        ````
        
        </details>

    -   <details><summary>With Node.js</summary>
        Install once with `npm install -g httpserver`{.sh}.
        
        Once installed, run

        ````sh
        httpserver 8000 localhost
        ````
        
        </details>
    
    There are many other webservers you could use too; I assume if you have one of those you already know how to use it.

2. Use the local server to view your files.

    For example, if your file is named `myfile.html`, in your browser go to one of the following:
    
    - <http://localhost:8000/myfile.html>
    - <http://127.0.0.1:8000/myfile.html>
    - <http://[::1]:8000/myfile.html>
    
    Depending on your OS and browser and which tool you used to start the server, it may be that only one of the above URLs works.

If you don't do this, it is likely you'll get an error message in the console when using `fetch` or loading a texture image that includes the words CORS in it.

## Beware of Caching

To avoid re-requesting files often, caching is used in many places on most systems,
including in the browser, in the operating system, and in the various computers between you and the server.
Unfortunately, caching can cause a webpage you've edited to not re-load,
particularly if you have several files contributing to the page.

Because caching is handled in different ways be different tools, there's no one-size-fits-all solution, but a combination of the following generally works:

- Browsers have some kind of private window option: Google calls it Incognito, Microsoft calls it InPrivate, Mozilla and Apple call it Private. In this mode, caching is partially disabled, resulting in more reliable development.

- In addition to the usual reload/refresh option, browsers provide a "hard refresh"
    by holding Ctrl (Windows/Linux) or Shift (MacX) while pressing the refresh button
    or while typing the reload key sequence.

I had one student who didn't seem to have anything different in his setup than other students but who couldn't make those options work. For him, the only way to reload multi-file locally-developed webpages was to exit the browser entirely, stop and restart the local web server, and then open the browser anew.
Hopefully that won't be your experience, but if it is that process does seem to work.

## Not every image is available

When loading images in JavaScript,
some images won't load, instead giving a CORS-related error in the console.

Servers can be configured to refuse javascript-based requests to load files. For example, the images on the <https://illinois.edu> homepage are set up this way; if you try to load them as a texture map of the like you’ll get a CORS error.

Because this is a configuration setting of the server, you can’t directly bypass it. Instead you’ll have to work around it, e.g. by loading the image in the HTML of the page, copying the image to a directory you control, or using a different image.
