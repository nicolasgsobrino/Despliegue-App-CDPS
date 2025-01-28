import os
import subprocess
import platform
import sys

# Configuración
REPO_URL = "https://github.com/CDPS-ETSIT/practica_creativa2.git"
GROUP_NUM = "14"
IMAGE_NAME = f"product-page/{GROUP_NUM}"
CONTAINER_NAME = f"product-page-{GROUP_NUM}"
PORT = "5080"

def check_docker():
    """Verifica si Docker está instalado en el sistema."""
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(" Docker está instalado correctamente.")
        return True
    except FileNotFoundError:
        print(" Docker no está instalado en el sistema.")
        return False

def install_docker():
    """Intenta instalar Docker automáticamente en sistemas Linux."""
    if platform.system() == "Linux":
        print("⚙️  Instalando Docker en Linux...")
        subprocess.run(["sudo", "apt", "update"])
        subprocess.run(["sudo", "apt", "install", "-y", "docker.io"])
        print(" Docker ha sido instalado. Verifica la instalación ejecutando 'docker --version'.")
    else:
        print(" La instalación automática de Docker solo está disponible en Linux.")
        print("Por favor, instala Docker manualmente desde https://www.docker.com/get-started")
        sys.exit(1)

def clone_repository():
    """Clona el repositorio de la aplicación desde GitHub si no existe."""
    if not os.path.exists("practica_creativa2"):
        print("🔄 Clonando el repositorio desde GitHub...")
        subprocess.run(["git", "clone", REPO_URL])
    else:
        print("🔄 El repositorio ya existe. Actualizando...")
        os.chdir("practica_creativa2")
        subprocess.run(["git", "pull"])
        os.chdir("..")

def create_dockerfile():
    """Crea el Dockerfile necesario para el despliegue de la aplicación."""
    dockerfile_content = f"""
    FROM python:3.7.7-slim
    WORKDIR /app
    COPY bookinfo/src/productpage /app
    RUN pip install --upgrade urllib3 chardet requests
    RUN pip install --no-cache-dir -r /app/requirements.txt
    ENV GROUP_NUM={GROUP_NUM}
    EXPOSE {PORT}
    CMD ["sh", "-c", "sed -i 's|BookInfo Sample|Grupo {GROUP_NUM}|g' /app/templates/productpage.html && python3 /app/productpage_monolith.py {PORT}"]
    """
    with open("practica_creativa2/Dockerfile", "w") as f:
        f.write(dockerfile_content.strip())
    print(" Dockerfile creado correctamente.")


def build_image():
    """Construye la imagen Docker a partir del Dockerfile."""
    os.chdir("practica_creativa2")
    print(" Construyendo la imagen Docker...")
    subprocess.run(["docker", "build", "-t", IMAGE_NAME, "."])
    os.chdir("..")

def run_container():
    """Ejecuta el contenedor Docker con las configuraciones necesarias."""
    print(f" Ejecutando el contenedor {CONTAINER_NAME} en el puerto {PORT}...")
    subprocess.run([
        "docker", "run",
        "--name", CONTAINER_NAME,
        "-p", f"{PORT}:{PORT}",
        "-e", f"GROUP_NUM={GROUP_NUM}",
        "-d", IMAGE_NAME
    ])
    print(f" La aplicación está disponible en http://localhost:{PORT}/productpage")

def delete_container():
    """Detiene y elimina el contenedor de Docker."""
    print(f" Eliminando el contenedor {CONTAINER_NAME}...")
    subprocess.run(["docker", "stop", CONTAINER_NAME], stderr=subprocess.PIPE)
    subprocess.run(["docker", "rm", CONTAINER_NAME], stderr=subprocess.PIPE)
    subprocess.run(["rm", "-rf", "practica_creativa2"])
    print(" Contenedor y aplicación eliminados correctamente.")

def main():
    """Función principal para manejar las opciones del usuario."""
    if not check_docker():
        install_choice = input("¿Deseas instalar Docker? (s/n): ").strip().lower()
        if install_choice == 's':
            install_docker()
        else:
            print(" No se puede continuar sin Docker.")
            sys.exit(1)

    action = input("¿Qué deseas hacer? (deploy/delete): ").strip().lower()
    if action == "deploy":
        clone_repository()
        create_dockerfile()
        build_image()
        run_container()
    elif action == "delete":
        delete_container()
    else:
        print(" Opción no válida. Usa 'deploy' o 'delete'.")

if __name__ == "__main__":
    main()
