# HackersWeek

Website of UMA Hackers Week, a CS event that takes place in University of Málaga (Spain), created in 2014 by https://github.com/baenafrancisco and the ETSI Informática Student Council.

This is an update of https://github.com/ConsejoInfUMA/UHW, rewritten in order to enhance the architecture of the site to implement better analytic features, a better control of the site, RESTful capabilities and a responsive front-end.

Original designs made by https://github.com/fdezfuentes.
Backend development by https://github.com/baenafrancisco.

Thanks to @YouWoTMA for attendance monitoring search!

## In Spanish, motherfucker!

###¿Por qué una web en Python? ¿Qué clase de magia negra es esta?

Tranquilo, quizá no estés acostumbrado a desarrollar en Django, pero ni te rayes… haciendo un mini tutorial de (approx.) una hora de duración, podrás hacer CUALQUIER CAMBIO que se te ocurra a la web. Además, la mayoría del código está hiper-bien documentado… y si tienes algún problema sólo tienes que mensajear a @baenafrancisco y el tío muy felizmente comentará línea por línea lo que quieras.

Antes de rendirte con algo… pregúntame al menos una vez!. Como me dijo una profesora china una vez (Jing Lu)…

![Attitude is everything!](http://i0.wp.com/prefer.co.nz/wp-content/uploads/2013/07/Attitude.jpg?fit=737%2C99999)

###¿Cómo edito algo en esto? [cambios sin persistencia]

Lo primero que tienes que hacer es clonar el proyecto en tu ordenador con GIT. Si no sabes a qué me refiero, busca arriba el botón «descargar ZIP» y descárgate el ZIP. Si no, abre un terminal y escribe la siguiente línea:

	```
	git clone https://github.com/ConsejoInfUMA/HackersWeek.git
	```

Una vez instalado esto, necesitas que un par de cositas estén instaladas en tu ordenador… en concreto, python (2.5+) y pip. Comprobar que están instalados es tan fácil como ir a una consola, escribir «python» y ver que no te da error. Igual con pip. Si ves que alguno te da error, busca en Google: «Cómo instalar [python/pip] en [tu sistema operativo]». Si tienes dudas, @baenafrancisco.

En este punto, python y pip ya estarán instalados en nuestro ordenador… Python es lo que va a interpretar nuestro código en nuestro sistema, y pip es un gestor de librerías de Python (para hacer la web, necesitamos algunas librerías que le dan a Python superpoderes).

En concreto, nos hacen falta dos librerías de Pyhton: django y django-allauth. Por suerte, hay un archivo que se llama «requirements.txt» que podemos darle a pip para que las instale automáticamente. Podemos hacer esto ejecutando el siguiente comando desde el directorio donde hayamos clonado el repositorio de GitHub (la carpeta HackersWeek):

Linux/Mac:

	```
	sudo pip install -r requirements.txt
	```

Windows:

	```
	pip install -r requirements.txt
	```

Si quieres hacer cambios en la portada de la web, el CSS, etc… no es extrictamente necesario utilizar el motor de persistencia (las bases de datos). Ya podrías ejecutar el proyecto django y ver (únicamente la portada) con el siguiente comando:

	```
	./manage.py runserver
	```

o

	```
	python manage.py runserver
	```

(Si no te funciona la primera sintaxis, usa la segunda siempre que veas ./)

Eso ejecutará un servidor de pruebas al que podrás acceder desde el navegador en la dirección http://127.0.0.1:8000/. Puedes parar este servidor en cualquier momento pulsando Ctrl+c en tu terminal. (Mandando una SIGINT, cosa que entenderás si has dado SO :P)

###Necesito editar cosas de STAFF/Login/etc… [cambios con persistencia]

Para todo esto, necesitas configurar una base de datos de pruebas. En principio, es tan fácil como introducir tres comandos más y no debería hacer falta que tengas instalado nada más en tu ordenador, aunque si tienes algún fallo contacta conmigo y edito esta guía. Los siguientes comandos harán que tu aplicación tenga acceso a una base de datos. (Asegurate )
 
1. El siguiente comando busca las descripciones de las clases que componen la base de datos y crea el SQL necesario para generar las tablas. 

	```
	./manage.py makemigrations
	```


2. Lo siguiente que hace falta es ejecutar ese SQL. Para ello, hay que escribir el siguiente comando:

	```
	./manage.py migrate
	```

3. Por último, si es la primera vez que creas la base de datos, hace falta crear el primer usuario del sistema (superusuario). Para ello, ejecuta el siguiente comando:


	```
	./manage.py syncdb
	```

	Te va a preguntar en Inglés si quieres crear un superusuario. Contesta «yes», e introduce los datos: usuario, email, contraseña, repite contraseña.

4. Una vez actualizado todo y creado el superusuario, vamos a probar que funciona todo. Vuelve a ejecutar el servidor de pruebas:

	```
	./manage.py runserver
	```

	Y loguéate en la web de administración: http://127.0.0.1:8000/admin/

5. La web de Hackers Week usa login con Facebook. Para eso tiene instalada una extensión que controla todo esto automáticamente (django-allauth); pero para que todo funcione hace falta configurarlo inicialmente. Si cerrases sesión e intentases loguearte en la web, te daría un error del tipo «Provider Facebook not configured». Para evitar este error, simplemente hay que ir a la web de administración (http://127.0.0.1:8000/admin/), hacer clic en Social applications (bajo el apartado Social Accounts), Añadir Social Application (arriba a la derecha), escoger Facebook en el proveedor e inventarse el resto de datos en negrita. Atención: esto evitará que aparezca el problema en nuestro servidor local, pero no permitirá que podamos loguearnos con Facecbook desde el mismo. Como el login con Facebook está perfectamente testeado y funciona, no te va a hacer falta usar el real. Si hay algún problema en la web original, añade un Issue en GitHub y etiquétame (@baenafrancisco).

Una vez configurado todo esto, la web local debería funcionar con casi todas las funcionalidades de la web original (menos las analíticas de Google y el login con Facebook).

###Okie dokie, todo fuma perfe… ¿cómo toco el código?

Te recomiendo que, antes de intentar toquetear nada aquí, primero te informes de CÓMO hacerlo siguiendo el siguiente tutorial (a mi me llevó una horita, más o menos): https://docs.djangoproject.com/en/1.7/intro/tutorial01/. No obstante, si quieres cambiar un color en CSS, una imagen o whatever, puedes hacerlo en los archivos HTML/CSS y no necesitas saber nada más de Django que instalarlo y poder previsualizar los archivos.

Voy a subdividir este apartado en tres subsecciones (de mayor a menor probabilidad):

####Cómo editar CSS/HTML o añadir archivos

Los archivos CSS e imágenes están en /static/css/ o /static/img. Puedes editarlo intentando comentar lo que hagas.

Los archivos HTML se subdividen en tres:

	- Archivos generales: se encuentran en el directorio /templates/. Ahí está la base (header y footer) y todo lo que tenga que ver con login.
	- Web pública: todo está bajo /www/templates. Heredan de "base.html" en /templates/ para añadir el header y footer.
	- Web de staff: todo está bajo /staff/templates/.

Para cargar un archivo estático dentro del HTML (imagen, CSS, javascript) hay que meterlo en la carpeta /static y referenciarlo dentro del código con la siguiente etiqueta:


	```
	{% static '/ruta/al/archivo.jpg' %}
	```


###Errores típicos/FAQ

1. **Cuando ejecuto runserver, me dice que el puerto está en uso:** puedes cambiar el puerto donde se ejecuta el servidor añadiéndolo detrás de runserver. El próximo ejemplo sería para ejecutar el servidor en el 8081. Para más info, visita: https://docs.djangoproject.com/en/1.7/ref/django-admin/#runserver-port-or-address-port

	```
	./manage.py runserver 8081
	```

2. **Me sale un error del tipo «table xxxxxx doesn't exist»:** necesitas seguir el tutorial bajo el título "Necesito editar cosas de STAFF/Login/etc… [cambios con persistencia]"

3. **Todo funciona bien (puedo hasta loguearme en la web /admin/ pero me dice algo de «Provider not configured»):** mira el punto 5 de "Necesito editar cosas de STAFF/Login/etc… [cambios con persistencia]"

