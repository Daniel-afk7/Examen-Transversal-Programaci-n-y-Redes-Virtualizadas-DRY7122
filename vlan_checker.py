# vlan_checker.py
def verificar_vlan():
    try:
        vlan = int(input("Ingrese el número de VLAN: "))
        
        if 1 <= vlan <= 1005:
            print(f"La VLAN {vlan} corresponde al rango NORMAL.")
        elif 1006 <= vlan <= 4094:
            print(f"La VLAN {vlan} corresponde al rango EXTENDIDO.")
        else:
            print(f"La VLAN {vlan} no es válida. El rango válido es 1-4094.")
    
    except ValueError:
        print("Error: Por favor ingrese un número válido.")

if __name__ == "__main__":
    verificar_vlan()