import os
import sys

# Definir función para desplegar los recursos
def deploy():
    print("Desplegando los microservicios en Kubernetes...")
    os.system("kubectl apply -f productpage.yaml")
    os.system("kubectl apply -f details.yaml")
    os.system("kubectl apply -f ratings.yaml")
    os.system("kubectl apply -f reviews-v1-deployment.yaml")
    os.system("kubectl apply -f reviews-v2-deployment.yaml")
    os.system("kubectl apply -f reviews-v3-deployment.yaml")
    os.system("kubectl apply -f reviews-svc.yaml")

    print("Verificando el estado de los pods...")
    os.system("kubectl get pods")

# Definir función para eliminar los recursos
def delete():
    print("Eliminando todos los microservicios de Kubernetes...")
    os.system("kubectl delete -f productpage.yaml")
    os.system("kubectl delete -f details.yaml")
    os.system("kubectl delete -f ratings.yaml")
    os.system("kubectl delete -f reviews-v1.yaml")
    os.system("kubectl delete -f reviews-v2-.yaml")
    os.system("kubectl delete -f reviews-v3-.yaml")
    os.system("kubectl delete -f productpage-svc.yaml")
    os.system("kubectl delete -f reviews-svc.yaml")

    print("Verificando que todos los recursos han sido eliminados...")
    os.system("kubectl get all")

# Función principal
if len(sys.argv) != 2:
    print("Uso: python deploy_k8s.py [deploy|delete]")
    sys.exit(1)

command = sys.argv[1].lower()

if command == "deploy":
    deploy()
elif command == "delete":
    delete()
else:
    print("Comando no reconocido. Usa 'deploy' para desplegar o 'delete' para eliminar.")
    sys.exit(1)
