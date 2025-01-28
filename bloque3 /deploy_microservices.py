import os
import sys

# Función para clonar el repositorio si no existe
def clone_repository():
    if not os.path.exists("practica_creativa2"):
        print("Clonando el repositorio de la práctica...")
        os.system("git clone https://github.com/CDPS-ETSIT/practica_creativa2.git")
    else:
        print("El repositorio ya existe. Saltando clonación.")

# Función para compilar el microservicio de Reviews
def build_reviews():
    print("Compilando el servicio Reviews...")
    os.chdir("practica_creativa2/bookinfo/src/reviews")
    os.system('docker run --rm -u root -v "$(pwd)":/home/gradle/project -w /home/gradle/project gradle:4.8.1 gradle clean build')
    os.chdir("../../../../")

# Función para construir todas las imágenes Docker
def build_images():
    print("Construyendo las imágenes Docker...")
    os.system("docker build -t productpage/14 -f Dockerfile.productpage .")
    os.system("docker build -t details/14 -f Dockerfile.details .")
    os.system("docker build -t ratings/14 -f Dockerfile.ratings .")
    os.system("docker build -t reviews/14 ./practica_creativa2/bookinfo/src/reviews/reviews-wlpcfg")

# Función para levantar la aplicación con Docker Compose
def start_application():
    print("Levantando la aplicación con Docker Compose...")
    os.system("docker-compose up --build -d")

# Función para detener los contenedores
def stop_application():
    print("Deteniendo la aplicación...")
    os.system("docker-compose down")

# Función para limpiar el entorno
def clean_application():
    print("Eliminando la aplicación y limpiando el entorno...")
    os.system("docker-compose down -v")
    os.system("sudo rm -rf practica_creativa2/")

# Función principal para manejar comandos desde CLI
def main():
    if len(sys.argv) < 2:
        print("Uso: python3 deploy_microservices.py [start|stop|delete]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "start":
        clone_repository()
        build_reviews()
        build_images()
        start_application()
    elif command == "stop":
        stop_application()
    elif command == "delete":
        clean_application()
    else:
        print("Comando no reconocido. Usa: start, stop, clean")

if __name__ == "__main__":
    main()
