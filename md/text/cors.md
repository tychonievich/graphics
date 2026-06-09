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
But many local webservers encourage browsers to cache files,
meaning that edits you make to files will seem not to have happened.

We have multiple possible solutions, using different local server tools.

<ul><li>
<details><summary>Python</summary>

Make a file `webserver.py` with the following contents:

```py
import http.server
import socketserver

PORT = 8080

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Send headers to prevent the browser from caching anything
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

# Allow restarting the server immediately without "Address already in use" errors
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), NoCacheHTTPRequestHandler) as httpd:
    print(self_address := f"Server running at http://localhost:{PORT}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
```

Run `python webserver.py` (or `python3` or `py3` or whatever your Python executable is called)
from the directory containing your HTML file, and then open <http://localhost:8080>

</details></li>

<li><details><summary>Node, full developer control</summary>

Run `npx http-server -c-1` 
from the directory containing your HTML file, and then open <http://localhost:8080>.

</details></li>

<li><details><summary>Node, more features</summary>

Run `npx live-server` 
from the directory containing your HTML file, and then open <http://localhost:8080>.

This inserts JavaScript into your HTML files to automatically reload the page when a file is edited.
That can be convenient, but can also be confusing to debug if you try to trace everything the page is doing.

</details></li>

<li><details><summary>VS Code extension </summary>

Install the "Live server" extension by Ritwick Dey in VS Code and use its "Go Live" button.
This inserts JavaScript into your HTML files to automatically reload the page when a file is edited.
That can be convenient, but can also be confusing to debug if you try to trace everything the page is doing.

</details></li></ul>

If you want to use a server that lacks a cache disable feature, you can also bypass caching in either of two ways:

- If you run your code with your browser's developer tools open (F12)
    and in those tools' Networks tab check the "Disable Cache" button,
    then your browser will ignore all caches while the developer tools are open.

- For `fetch` calls, use `fetch(myFileName, {cache:"no-store"})`{.js} to bypass the cache.
    For `<script>` tags, they can be forcibly reloaded in a platform-specific way:
    
    - Most OSes and browsers: Ctrl+F5 or Ctrl+Shift+R or Ctrl+(refresh button)
    - MacOS and most browsers: Cmd+Shift+R or Shift+(refresh button)
    - MacOS and Safari: Cmd+Shift+E followed by Cmd+R


# Servers might not share images

Servers can be configured to refuse JavaScript-based requests to load files.
For example, the images on the <https://illinois.edu> homepage are set up this way;
if you try to load them as a texture map of the like you'll get a CORS error.

Because this is a configuration setting of the server, you can't directly bypass it.
Instead, you'll have to work around it, e.g. by loading the image in the HTML (instead of JavaScript) of your page or downloading a local copy of the image.
