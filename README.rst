
Airline Reservation System
=========
|python| |react| |django| |license| 

Disclaimer
----------
This "Airline Reservation System" is just an unprofessional project which was made by a total beginner for the sake of learning. It has no real world use.

*** NO LONGER DEPLOYED!!! *** - Ignore the "Quickstart" section.

Feel free to try to make it work locally. Here're some TIPS for that:

* When you get field mismatch errors in dal, it's because in model._meta.get_fields, I changed 'reverse' to 'False'. (I made many such bad practices here, but now thanks to that I know better).

* If the initial data isn't enough for you, use "http://127.0.0.1:8000/admin/randomly_populate_all/" to automatically generate more.




Description
----------
As its name suggests, this system allows airlines to display information about upcoming flights to the public, and provides flight reservation customer service.

From now on I'll be referring to this "Airline Reservation System" as "ARS" for short.





Quickstart
----------
There are 3 ways to use this system, and I'll start from giving instructions on how to use this system from the most to least recommended way.



1 - DOCKER IMAGE UI :

Steps:

1. Install Docker.

2. Run your docker daemon.

3. Pull my image, it's called "sky-soar" : https://hub.docker.com/r/minus0plus/sky-soar.

.. code-block::

    $ docker pull minus0plus/sky-soar


4. Run it, either via the Docker Desktop app, or via the terminal like so: "docker run -dp <insert your chosen unoccupied port number>:3000 --name <insert your chosen container name> minus0plus/sky-soar:latest". Example:

.. code-block::

    $ docker run -dp 3002:3000 --name sky-soar-container minus0plus/sky-soar:latest


5. Wait a few minutes while it loads for the first time.





2 - FIREBASE HOST UI :

Steps:

1. Open a browser, preferably Firefox (it looks its best there).

2. Go to: https://sky-seat-saver.web.app.





3 - AZURE HOST API :

Steps:

1. Open a browser, preferably Firefox.

2. Go to: https://sky-soar.azurewebsites.net/api/.





Useful
----------
Generate fake valid DATA quickly (just some websites that I found):

* https://www.prepostseo.com/tool/fake-address-generator

* https://randommer.io/Phone

* https://www.creditcardvalidator.org/generator



Some premade USERS (Registered = users that have an existing instance in their designated role's table) :

[ Please use them only to view the UI from their respective perspective. ]


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

