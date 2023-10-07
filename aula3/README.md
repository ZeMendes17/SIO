# XSS and CORS

## Environment setup

After setting the app, installing the requirments, etc. We open the browser one in normal mode and
the other in incognito mode. The Admin will be in the normal and the attacker in the incognito.
We will know proceed into making a couple of attacks to the website.

Access the site in the URL **http://aula3:6543**

## Cross-Site Scripting

### Reflected XSS Attack

In this type of attack it is assumed that the attack is non-persistent. With this attack it becomes
possible to manipulate the browser Document Object Model (DOM) for a single user, or multiple which
access a page through the same specially crafted **URL** depicts a typical scenario.

#### How to do it in our Website:

Using the Blog Search bar, which searches directly using the website, we can pass:
```
<script>alert("You are under attack")</script>
```
Because we are passing a script tag, the site will interpert it as being part of the code and will
execute it (alert is not the best for attackers but shows well what happens).

URL generated: `http://aula3:6543/search?q=%3Cscript%3Ealert%28%22You+are+under+attack%22%29%3C%2Fscript%3E`

### Stored Xss Attack


