# Distintos despliegues de aplicaciones escalables. 

Nicolás García Sobrino nicolas.garciasobrino@alumnos.upm.es,
Santiago Rayán Castro , s.rayan@alumnos.upm.es
Javier de Ponte Hernando. j.deponteh@alumnos.upm.es

---
B1-GC-deploy_app (pip3 install "requests<2.25" "urllib3<1.25" "chardet<4")
B2-Local-deploy_docker
B3-GC-deploy_microservices
B4-VSCODE+cluster-deploy_k8s
---

# Bloque 1. Despliegue de la Aplicación Monolítica en VM de Google Cloud

Este documento detalla el proceso de desarrollo del script en Python para desplegar una aplicación monolítica en una máquina virtual pesada, conforme a los requisitos de la práctica creativa 2 utilizando Google Cloud como infraestructura de VM. 

El objetivo es desplegar una aplicación monolítica escrita en Python sobre una máquina virtual en Google Cloud Platform (GCP). La aplicación consiste en una página web que muestra información sobre libros y se ejecuta mediante el archivo `productpage_monolith.py`.

La instalación incluye:
- Clonación del repositorio con el código de la aplicación.
- Instalación de dependencias.
- Configuración del entorno.
- Despliegue y ejecución de la aplicación en la VM.

---

## **Estructura del Script**

El script desarrollado (`deploy_app.py`) realiza las siguientes funciones:

1. **`install_dependencies()`**: Instala paquetes esenciales como Python, Pip y Git.
2. **`clone_repository()`**: Clona el repositorio de la aplicación desde GitHub.
3. **`modify_application_title()`**: Modifica el título de la aplicación con el nombre del grupo.
4. **`configure_application(group_num, port)`**: Configura la aplicación con los valores especificados y la inicia.
5. **`delete_application()`**: Detiene la aplicación y elimina los archivos generados.
6. **`deploy_application(group_num, port)`**: Orquesta todo el proceso de instalación y despliegue.
7. **`main()`**: Controla la ejecución del script, permitiendo las opciones de despliegue y eliminación.

---

## **Uso del Script**

Para iniciar la aplicación en la máquina virtual, ejecutar:

```bash
python3 deploy_app.py
```

Esto realizará:
1. Instalación de dependencias.
2. Clonación del repositorio.
3. Configuración del entorno.
4. Despliegue de la aplicación.

La aplicación será accesible en la URL:

```
http://<IP PUBLICA VM>:9080/productpage
```

Para detener la aplicación y eliminar los archivos generados, ejecutar:

```bash
python3 deploy_monolith_vm.py delete
```

Este comando realiza:
- Finalización del proceso de la aplicación.
- Eliminación del repositorio clonado.

---

## **Configuración de Variables de Entorno**
El script permite personalizar la configuración a través de variables de entorno:

```bash
export GROUP_NUM=14
export APP_PORT=9080
```

Las variables disponibles son:
- `GROUP_NUM`: Número de grupo para personalizar el título de la aplicación.
- `APP_PORT`: Puerto en el que se ejecuta la aplicación.

---

## **Configuración de Firewall en GCP**
Para garantizar el acceso a la aplicación desde el exterior, es necesario crear una regla de firewall para permitir el puerto 9080 ajustada manualmente en Google Cloud
<img width="1285" alt="Captura de pantalla 2025-01-21 a las 18 35 25" src="https://github.com/user-attachments/assets/1825a7a3-7852-4c30-a222-cd7d48755f99" />

---

## **Consideraciones Finales**

La app se puede ejecutar en la propia maquina virtual de Google Cloud ejecutando el comando normal o ejecutando acompañado de un & para tener acceso posteriormente al terminal y poder ejecutar el comando delete de manera más limpia. (sin el & la consola se queda dentro de la ejecución y hay que hacer controlC para salir). 

---

# Bloque 2. Despliegue de Aplicación Monolítica usando Docker

Este documento proporciona una guía paso a paso para desplegar una aplicación monolítica utilizando Docker de forma automatizada mediante un script en Python.

El scrypt realiza todo, comprueba que docker este descargado, si no, lo instala, clona el repositorio, ejecuta los comando correspondientes y despliega la app en local. 

Tambien se puede desplegar en la VM de google cloud como hemos hecho en el bloque1 pero en este caso queríamos cambiar para ver otro enfoque. 

En el caso de desplegar en VM habría que subir los archivos y añadir una nueva regla del FW para que permita peticiones al puerto 5080. 

---

## **Descripción del Script**

El script automatiza las siguientes tareas:

1. **Verificación de Docker:** Comprueba si Docker está instalado.
2. **Instalación de Docker (opcional):** Instala Docker si no está disponible (solo en Linux). 
3. **Clonación del Repositorio:** Descarga la aplicación desde GitHub.
4. **Creación del Dockerfile:** Genera el Dockerfile para construir la imagen.
5. **Construcción de la Imagen Docker:** Construye la imagen de la aplicación.
6. **Ejecución del Contenedor:** Levanta la aplicación con la configuración correcta.
7. **Eliminación del Contenedor:** Permite borrar la aplicación desplegada.

---

## **Uso del Script**

1. Clona este repositorio o guarda el script Python en tu entorno.

2. Ejecuta el script:

    ```bash
    python3 deploy_docker.py
    ```

3. Selecciona la acción deseada:

    - Para desplegar la aplicación, escribe: `deploy`
    - Para eliminar la aplicación, escribe: `delete`

4. Una vez desplegado, accede a la aplicación a través de:

    ```
    http://localhost:5080
    ```

---

## **Descripción del Dockerfile Generado**

El Dockerfile generado por el script contiene los siguientes pasos:

```dockerfile
FROM python:3.7.7-slim
WORKDIR /app
COPY bookinfo/src/productpage /app
RUN pip install --upgrade urllib3 chardet requests
RUN pip install --no-cache-dir -r /app/requirements.txt
ENV GROUP_NUM=14
EXPOSE 5080
CMD ["sh", "-c", "sed -i 's|BookInfo Sample|Grupo ${GROUP_NUM}|g' /app/templates/productpage.html && python3 /app/productpage_monolith.py 5080"]
```

### **Explicación de las instrucciones:**

- `FROM python:3.7.7-slim`: Usa una imagen base ligera de Python.
- `WORKDIR /app`: Establece el directorio de trabajo dentro del contenedor.
- `COPY bookinfo/src/productpage /app`: Copia el código fuente de la aplicación.
- `RUN pip install`: Instala las dependencias necesarias.
- `ENV GROUP_NUM=14`: Establece una variable de entorno con el número del grupo.
- `EXPOSE 5080`: Expone el puerto en el contenedor.
- `CMD [...]`: Ejecuta la aplicación reemplazando el texto "BookInfo Sample" por "Grupo 14".

---

## **Funciones Principales del Script**

### `check_docker()`
Verifica si Docker está instalado en el sistema.

### `install_docker()`
Instala Docker en sistemas Linux si no está presente.

### `clone_repository()`
Clona el repositorio de la aplicación si no existe, o lo actualiza si ya está clonado.

### `create_dockerfile()`
Genera un Dockerfile para construir la imagen Docker.

### `build_image()`
Construye la imagen Docker a partir del Dockerfile generado.

### `run_container()`
Ejecuta un contenedor basado en la imagen creada.

### `delete_container()`
Elimina el contenedor desplegado y borra el repositorio.

### `main()`
Controla la ejecución del script según la acción elegida por el usuario.

<img width="1433" alt="Captura de pantalla 2025-01-22 a las 18 44 47" src="https://github.com/user-attachments/assets/23c041e4-4bd1-4dc0-a0a0-1ef6af777255" />

---

## **Eliminación del Contenedor**

Para detener y eliminar la aplicación de Docker, puedes ejecutar el script y elegir la opción `delete` o hacerlo manualmente con los siguientes comandos:

```bash
# Detener el contenedor
    docker stop product-page-14

# Eliminar el contenedor
    docker rm product-page-14

# Eliminar la imagen
    docker rmi product-page/14
```

---

## **Conclusión**

Este script proporciona una forma sencilla de automatizar el despliegue de una aplicación monolítica en Docker. Se encarga de todas las tareas necesarias, desde la instalación de dependencias hasta la ejecución de la aplicación en un contenedor accesible desde el navegador.



Tambien se puede ejecutar desde un terminal remoto utilizando ssh usuario@34.175.77.229 (ip externa) accediendo con la clave pública.

---

# **Bloque 3. Despliegue de la aplicación en microservicios**

Este proyecto despliega una aplicación basada en microservicios utilizando **Docker Compose**, segmentando los servicios de una aplicación monolítica para ejecutarlos de manera independiente.
Se suben todos los archivos a la maquina virtual de GoogleCloud para que no de errores de configuración y lo utilizamos para desplegar.

<img width="1012" alt="Captura de pantalla 2025-01-26 a las 20 01 28" src="https://github.com/user-attachments/assets/421f8f1b-ef12-4175-ab34-bd552e18327f" />

## **Estructura del proyecto**

```
Bloque_3/
│-- deploy_docker.py         # Script de automatización para despliegue
│-- Dockerfile.productpage   # Dockerfile para el servicio Product Page (Python)
│-- Dockerfile.details       # Dockerfile para el servicio Details (Ruby)
│-- Dockerfile.ratings       # Dockerfile para el servicio Ratings (NodeJS)
│-- docker-compose.yml       # Definición de los servicios con Docker Compose
│-- practica_creativa2/      # Repositorio clonado con los servicios
```

---

## **Microservicios incluidos**

La aplicación se ha dividido en los siguientes microservicios:

1. **Product Page** (Python): Página de inicio de la aplicación.
2. **Details** (Ruby): Muestra detalles adicionales de los productos.
3. **Reviews** (Java): Muestra reseñas de los productos en diferentes versiones.
4. **Ratings** (NodeJS): Proporciona la puntuación de los productos.

---

## **Despliegue en Google Cloud**

El despliegue de la aplicación se realiza en una máquina virtual de **Google Cloud Platform (GCP)**. Asegúrate de tener acceso a la VM y permisos para ejecutar Docker.

### **1. Acceder a la VM de Google Cloud**

Primero, inicia sesión en tu VM de Google Cloud usando SSH:

```bash
gcloud compute ssh <usuario>@<nombre-de-la-vm> --zone=<zona>
```

Ejemplo:

```bash
gcloud compute ssh nicolasgsobrino@bloque3-vm --zone=europe-west1-b
```

O subiendo los archivos desde local en el terminal de la maquina virtual con la opción (subir archivos).

---

## **Instalación y despliegue**

Para desplegar la aplicación en la VM de Google Cloud, utiliza el script `deploy_docker.py`, que permite gestionar todo el proceso de construcción y ejecución.

### **2. Requisitos previos**
Asegúrate de que la VM en Google Cloud tenga instalados los siguientes programas:

- **Docker**  
  ```bash
  sudo apt update && sudo apt install docker.io -y
  ```
- **Docker Compose**  
  ```bash
  sudo apt install docker-compose -y
  ```
- **Git**  
  ```bash
  sudo apt install git -y
  ```

---

## **Uso del script**

El script `deploy_docker.py` permite realizar las siguientes operaciones:

### **1. Construcción y despliegue de la aplicación**

```bash
python3 deploy_docker.py start
```

Este comando realiza los siguientes pasos:

- Clona el repositorio `practica_creativa2` si no existe.
- Compila el microservicio de **Reviews** utilizando Gradle.
- Construye las imágenes Docker para todos los microservicios.
- Levanta la aplicación usando **Docker Compose**.

---

### **2. Detener la aplicación**

```bash
python3 deploy_docker.py stop
```

Este comando detiene los contenedores sin eliminar los volúmenes de datos.

---

### **3. Eliminar la aplicación y limpiar el entorno**

```bash
python3 deploy_docker.py clean
```

Este comando realiza las siguientes acciones:

- Detiene los contenedores y elimina los volúmenes.
- Borra el repositorio clonado de la práctica.

---

## **Archivos importantes en el proyecto**

- **`Dockerfile.productpage`**  
  Construye la imagen del servicio Product Page utilizando Python.
  
- **`Dockerfile.details`**  
  Construye la imagen del servicio Details con Ruby.

- **`Dockerfile.ratings`**  
  Construye la imagen del servicio Ratings utilizando NodeJS.

- **`docker-compose.yml`**  
  Define la configuración de los contenedores y su comunicación entre sí.

---

## **Verificación del despliegue**

Una vez que la aplicación está en ejecución en la VM de Google Cloud, puedes acceder a la interfaz web de la aplicación mediante:

```
http://<IP-EXTERNA>:9080
```

Ejemplo (según nuestro despliegue):

```
http://34.175.221.139:9080
```

---

Aquí tienes el contenido para el archivo **README.md** del Bloque 4:

---

# **Despliegue de la aplicación en microservicios usando Kubernetes (Bloque 4)**

Este proyecto implementa el despliegue de una aplicación basada en microservicios utilizando **Kubernetes**, facilitando la orquestación y gestión de contenedores en un clúster de Google Kubernetes Engine (**GKE**).

---

## **Estructura del proyecto**

```
Bloque_4/
│-- deploy_k8s.py                 # Script de automatización para despliegue en Kubernetes
│-- productpage-deployment.yaml    # Despliegue del servicio Product Page
│-- details-deployment.yaml        # Despliegue del servicio Details
│-- ratings-deployment.yaml        # Despliegue del servicio Ratings
│-- reviews-v1-deployment.yaml     # Despliegue de Reviews versión 1
│-- reviews-v2-deployment.yaml     # Despliegue de Reviews versión 2
│-- reviews-v3-deployment.yaml     # Despliegue de Reviews versión 3
│-- productpage-svc.yaml            # Configuración del servicio Product Page
│-- reviews-svc.yaml                 # Configuración del servicio Reviews
```

---

## **Microservicios incluidos**

La aplicación está compuesta por los siguientes microservicios:

1. **Product Page** (Python): Página de inicio de la aplicación.
2. **Details** (Ruby): Proporciona detalles adicionales de los productos.
3. **Reviews** (Java): Muestra reseñas de los productos en diferentes versiones.
4. **Ratings** (NodeJS): Proporciona la puntuación de los productos.

---

## **Despliegue en Google Kubernetes Engine (GKE)**

El despliegue de la aplicación se realiza en un clúster de **Google Kubernetes Engine (GKE)**. Para ello, se deben seguir los siguientes pasos.

---

## **Instalación y configuración en GKE**

### **1. Prerrequisitos**

Asegúrate de que tienes configuradas las herramientas necesarias en tu máquina virtual de Google Cloud:

- **Instalar Google Cloud SDK y herramientas de Kubernetes (kubectl):**

  ```bash
  sudo apt update
  sudo apt install google-cloud-sdk kubectl -y
  ```

- **Autenticarte en Google Cloud:**

  ```bash
  gcloud auth login
  gcloud config set project <tu-proyecto-id>
  ```

- **Crear un clúster de Kubernetes en GKE:**

  ```bash
  gcloud container clusters create bloque4-cluster --num-nodes=3 --zone=europe-west1-b
  ```

- **Conectar tu terminal con el clúster:**

  ```bash
  gcloud container clusters get-credentials bloque4-cluster --zone=europe-west1-b
  ```

---

## **Uso del script**

El script `deploy_k8s.py` permite gestionar el despliegue y eliminación de los microservicios en Kubernetes de manera sencilla.

### **1. Desplegar la aplicación**

```bash
python3 deploy_k8s.py deploy
```

Este comando realiza las siguientes tareas:

- Aplica los archivos YAML para crear los deployments de todos los microservicios.
- Crea los servicios correspondientes para permitir la comunicación entre los pods.
- Verifica el estado de los pods desplegados.

---

### **2. Eliminar la aplicación**

```bash
python3 deploy_k8s.py delete
```

Este comando realiza las siguientes acciones:

- Elimina los deployments y services creados.
- Verifica que no queden recursos activos en el clúster.

---

## **Verificación del despliegue**

1. **Comprobar el estado de los pods en Kubernetes:**

   ```bash
   kubectl get pods
   ```

   Todos los pods deben estar en estado `Running`.

2. **Verificar los servicios disponibles y su IP externa:**

   ```bash
   kubectl get svc
   ```

   Salida esperada:

   ```
   NAME            TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)          AGE
   productpage     LoadBalancer   34.118.239.140   34.175.25.80     9080:32070/TCP   5m
   reviews         ClusterIP      34.118.231.246   <none>           9083/TCP         5m
   ```

3. **Acceder a la aplicación web en el navegador:**  

   Utiliza la IP externa del servicio `productpage` para acceder a la aplicación:

   ```
   http://<IP asignada al productpage>:9080
   ```

---

## **Solución de problemas**

Si tienes problemas con el despliegue o la aplicación, prueba las siguientes soluciones:

1. **Verificar eventos del clúster para detectar errores:**  

   ```bash
   kubectl get events --sort-by=.metadata.creationTimestamp
   ```

2. **Revisar los logs de los pods individuales:**  

   ```bash
   kubectl logs deployment/productpage-v1
   ```

3. **Eliminar todos los recursos manualmente en caso de problemas:**  

   ```bash
   kubectl delete all --all
   ```

---

## **Escalado de la aplicación**

Puedes escalar los microservicios según las necesidades de carga con el siguiente comando:

```bash
kubectl scale deployment reviews-v1 --replicas=3
```

Esto creará más instancias del microservicio `reviews-v1`.

---

## **Monitoreo del clúster**

Para observar métricas de rendimiento del clúster, utiliza el siguiente comando:

```bash
kubectl top nodes
```

---

## **Notas adicionales**

- Asegúrate de que los puertos correctos están expuestos para el acceso externo.
- Si el balanceador de carga tarda en asignar una IP externa, espera unos minutos y verifica de nuevo con:

  ```bash
  kubectl get svc
  ```

