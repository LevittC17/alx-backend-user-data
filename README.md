# 0x01. Basic authentication
*Back-end
*Authentification

## Background Context
In this project, you will learn what the authentication process means and implement a **Basic Authentication** on a simple API.
In this industry, you should not implement your own Basic authentication system and use a module or framework that doing it for you (like in Python-Flask): [Flask-HTTPAuth](https://flask-httpauth.readthedocs.io/en/latest/). Here, for the learning purpose, we will walk through each step of this mechanism to understand it by doing.

![Auth](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/medias/2020/5/6ccb363443a8f301bc2bc38d7a08e9650117de7c.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20231108%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231108T093254Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=40c3d755a07c7170b800845a7c8a75e37c2814e41a28f8072bc5c07d3eb4ef96)


## Resources
**Read or watch**
   [REST API Authentication Mechanisms](https://www.youtube.com/watch?v=501dpx2IjGY)
   [Base64 in Python](https://docs.python.org/3.7/library/base64.html)
   [HTTP header Authorization](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization)
   [Flask](https://palletsprojects.com/p/flask/)
   [Base64 - concept](https://en.wikipedia.org/wiki/Base64)


# Learning Objectives
At the end of this project, you are expected to be able to explain to anyone, without the help of Google:

### General
   - What authentication means
   - What Base64 is
   - How to encode a string in Base64
   - What Basic authentication means
   - How to send the Authorization header

# Requirements

### Python Scripts
   - All your files will be interpreted/compiled on Ubuntu 18.04 LTS using `python3` (version 3.7)
   - All your files should end with a new line
   - The first line of all your files should be exactly `#!/usr/bin/env python3`
   - A `README.md` file, at the root of the folder of the project, is mandatory
   - Your code should use the `pycodestyle` style (version 2.5)
   - All your files must be executable
   - The length of your files will be tested using `wc`
   - All your modules should have a documentation (`python3 -c 'print(__import__("my_module").__doc__)'`)
   - All your classes should have a documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`)
   - All your functions (inside and outside a class) should have a documentation (`python3 -c 'print(__import__("my_module").my_function.__doc__)'` and `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`)
   - A documentation is not a simple word, it’s a real sentence explaining what’s the purpose of the module, class or method (the length of it will be verified)
