
Airline Reservation System
=========
|python| |react| |django| |license| 

Disclaimer
----------
This "Airline Reservation System" is just an unprofessional project which was made by a total beginner for the sake of learning. 

It has no real world use.

And please be patient because my system runs slowly. 




Description
----------
As its name suggests, this system allows airlines to display information about upcoming flights to the public, and provides a flight reservation customer service.

From now on I'll be referring to this "Airline Reservation System" as "ARS" for short.





Quickstart
----------
There are 3 ways to use this system, and I'll start from giving instructions on how to use this system from the most to least recommended way.



1 - MOST RECOMMENDED WAY TO USE THIS SYSTEM | DOCKER IMAGE UI :

Steps:

1. Install Docker.

2. Run your docker daemon.

3. Pull my image, it's called "ars-web" : https://hub.docker.com/r/minus0plus/ars-web.

.. code-block::

    $ docker pull minus0plus/ars-web


4. Run it, either via the Docker Desktop app, or via the terminal like so: "docker run -dp <insert your chosen unoccupied port number>:3000 --name <insert your chosen container name> ars-web:latest". Example:

.. code-block::

    $ docker run -dp 3002:3000 --name ars-example-container minus0plus/ars-web:latest


* Why is it the most recommended way? - Because my deployed react frontend has all sorts of silly bugs, and its appearance is inconsistent with browser changes.

* What is this image for? - This image is only for my system's react frontend UI. (The django backend is deployed separately on azure).





2 - WILL WORK WITH OCCASIONAL HICCUPS ...PROBABLY. | FIREBASE HOST UI :

Steps:

1. Connect to the internet.

2. Open a browser, preferably Firefox (it looks its best there).

3. Go to: https://sky-seat-saver.web.app.

* What do you mean by 'hiccups'? - Don't refresh the buy_ticket page. The navbar even disappeared once seemingly randomly. It looks even worse there than it does locally. There are probably many more bugs which I haven't had the displeasure nor time to discover yet.





3 - IF YOU REALLY HATE YOURSELF | AZURE HOST API :

Steps:

1. Connect to the internet.

2. Open a browser, preferably Firefox.

3. Go to: https://ars-api.azurewebsites.net/api/.

* Why the hate? - I haven't even tried using the whole system via APIs only. I only ever directly used each API once or twice, immediately after writing it. The APIs were pretty much built for internal system use only, or in other words, to be used by the react UI behind the scenes. Also, this too, for some cursed reason, looks worse in deployment. All the APIs were under one title locally, but there it's all separated into ugly sub-titles. Oh and my 'id_id' variable name blunder is in full display there.





Testing
----------
I started by writing relatively a lot of tests. In hindsight, I really shouldn't have done it. 

And that's because I mostly ended up using only a small portion of that stuff. Unfortunately, I haven't had the time to test all the parts that I ended up using. 

Most of it was only tested manually by a very sleepy me. Not very reliable, I know, and my final grade will surely know it too.

I didn't even write a postman collection.

So glad and so sad simultaneously that my future self will never have an access to a time machine.






Useful
----------
Generate DATA quickly (just some websites that I found):

* https://www.prepostseo.com/tool/fake-address-generator

* https://randommer.io/Phone

* https://www.creditcardvalidator.org/generator



Some pre-made USERS (Registered = users that have an existing instance in their designated role's table) :

[ Please use them only to view the UI from their respective perspective. Don't do any create/update/delete with them. Create your own users for that. ]


* ADMINS:


   (Registered)

   Cat

   Murka1234


   (Not Registered)

   Elina

   Lock1234



* CUSTOMERS:


   (Registered)

   RockyRecklessRaccoon

   Yeah666YOLO


   (Not Registered)

   GhostlyNapstablook

   Ghost1234



* AIRLINES:


   (Registered)

   Surpass_Icarus

   AndstillfailH4


   (Not Registered)

   NotAFlyingButter

   Serious1y








.. |python| image:: https://img.shields.io/badge/python-3.11-blue.svg
   :target: https://www.python.org/downloads/release/python-3110/

.. |react| image:: https://img.shields.io/badge/React-18-blue.svg
   :target: https://react.dev/learn/

.. |django| image:: https://img.shields.io/badge/Django-4.2-blue.svg
   :target: https://docs.djangoproject.com/en/4.2/

.. |license| image:: https://img.shields.io/badge/license-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/quick-guide-gplv3.html

