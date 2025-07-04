def main():
    integrantes = [
        {"nombre": "Daniel", "apellido": "Gallardo"},
        {"nombre": "Cristian", "apellido": "Sanhueza"},
        {"nombre": "Dylan", "apellido": "Garay"},
        
    ]
    
    print("Lista de integrantes del grupo:")
    for i, integrante in enumerate(integrantes, start=1):
        print(f"{i}. {integrante['nombre']} {integrante['apellido']}")

if __name__ == "__main__":
    main()