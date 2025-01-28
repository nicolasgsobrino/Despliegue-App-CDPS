import os
import subprocess
import sys

def install_dependencies():
    """
    Instala las dependencias necesarias para la aplicación.
    """
    print("Instalando dependencias...")
    subprocess.run(["sudo", "apt", "update"], check=True)
    subprocess.run(["sudo", "apt", "upgrade", "-y"], check=True)
    subprocess.run(["sudo", "apt", "install", "-y", "python3", "python3-pip", "git"], check=True)
    subprocess.run(["pip3", "install", "requests<2.25", "urllib3<1.25", "chardet<4"], check=True)
    clone_repository()
    subprocess.run(["pip3", "install", "-r", "bookinfo/src/productpage/requirements.txt"], check=True)

def clone_repository():
    """
    Clona el repositorio de la aplicación desde GitHub.
    """
    print("Clonando el repositorio de la aplicación...")
    subprocess.run(["git", "clone", "https://github.com/CDPS-ETSIT/practica_creativa2.git"], check=True)
    os.chdir("practica_creativa2")

def modify_application_title():
    """
    Modifica el título de la aplicación para incluir el nombre del grupo desde la variable de entorno.
    """
    with open("bookinfo/src/productpage/templates/productpage.html", "r") as file:
        content = file.read()
    content = content.replace("BookInfo Sample", os.environ.get("GROUP_NUM", "Default Group"))
    with open("bookinfo/src/productpage/templates/productpage.html", "w") as file:
        file.write(content)

def configure_application(group_num, port):
    """
    Configura la aplicación para usar el nombre del grupo y puerto especificado.
    """
    os.environ['GROUP_NUM'] = str(group_num)
    modify_application_title()
    print(f"Configurando la aplicación con el grupo {group_num} y puerto {port}...")
    subprocess.run(["nohup", "python3", "bookinfo/src/productpage/productpage_monolith.py", str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def delete_application():
    """
    Detiene la aplicación y elimina los archivos relacionados.
    """
    print("Eliminando la aplicación...")
    subprocess.run(["rm", "-rf", "practica_creativa2"])
    print("Aplicación eliminada correctamente.")

def deploy_application(group_num, port):
    """
    Despliega la aplicación en la máquina virtual.
    """
    install_dependencies()
    configure_application(group_num, port)
    print(f"Aplicación desplegada en http://<ip-publica>:{port}/productpage")

def main():
    """
    Punto de entrada principal del script. Maneja las opciones de despliegue y eliminación.
    """
    group_num = os.environ.get("GROUP_NUM", "14")
    port = os.environ.get("APP_PORT", "9080")

    if len(sys.argv) == 1:
        deploy_application(group_num, port)
    elif len(sys.argv) == 2 and sys.argv[1] == "delete":
        delete_application()
    else:
        print("Uso: python3 script.py [delete]")
        sys.exit(1)

if __name__ == "__main__":
    main()



