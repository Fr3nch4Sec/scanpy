# scanpy  

 Un outil python, pour scanner les ports réseaux.  🏄🏄  

Privilégier un environement virtuel, pour éviter les conflits de dépendances:  
 
  ``python <version> -m venv <virtual-environment-name>`` 

ou;

  ``uv venv``

puis;
  ``
  source .venv/bin/activate  
  uv pip install colorama==0.4.6  
  uv pip install tqdm==4.67.1  
   ``

  usage:  ``python3 scanpy.py -u <ip> -pS <port_start> -pE <port_end> -m [basic, advanced, concurrent] -b``       (Détection des services)  

  Exemple:  ``scanpy.py -u 127.0.0.1 -pS 1 -pE 1000 -m advanced -b  ``

  Exemple:  ``scanpy.py -u 127.0.0.1 -pS 1 -pE 1024 -m basic (Arguments par défault)  ``
 
