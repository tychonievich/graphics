---
title: Handling CORS errors
summary: A practical guide to running WebGL locally.
...

<style> summary > p { display: inline; } </style>

To improve security and reduce information leaks and spyware, HTTP (the protocol used to share most web resources) have a set of rules about "[cross-origin resource sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)".
For our purposes there are two broad ideas to consider here.

# `fetch` during development

If you run your page using the `file://` scheme, `fetch` and its friends are unlikely to work.
Instead, you'll need to run a local webserver.

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

2. Use the local server to view your files.

    For example, if your file is named `myfile.html`, in your browser go to one of the following:
    
    - <http://localhost:8000/myfile.html>
    - <http://127.0.0.1:8000/myfile.html>
    - <http://[::1]:8000/myfile.html>
    
    Depending on your OS and browser and which tool you used to start the server, it may be that only one of the above URLs works.

3. If needed, test in private/incognito mode and force-refresh

    Some combinations of operating system, browser, and server may result in excessive caching.
    This results in edits you make to local files not being visible in the browser: the old versions of the files are still served.
    
    For `fetch`, caching can be avoided by adding the `{cache:"no-store"}`{.js} configuration to the `fetch` call,
    as in `fetch(myFileName, {cache:"no-store"}).then(/*...*/)`{.js}.

    Opening the page in a private/incognito browser window bypasses most caching and may also assist in not caching files you've edited.

    If the browser still caches, there is a "forced reload" option that bypasses the cache;
    on Windows and most Linux installs this is achieved with Ctrl+F5; on MacOS Opt+R is more common.
    Holding Shift while pressing the reload button may also work.

# Servers might not share images

Servers can be configured to refuse JavaScript-based requests to load files.
For example, the images on the <https://illinois.edu> homepage are set up this way;
if you try to load them as a texture map of the like you'll get a CORS error.

Because this is a configuration setting of the server, you can't directly bypass it.
Instead, you'll have to work around it, e.g. by loading the image in the HTML of the page or copying the image to a directory you control.
