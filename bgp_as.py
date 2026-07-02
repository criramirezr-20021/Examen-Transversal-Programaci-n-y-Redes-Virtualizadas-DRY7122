as_number = int(input("Ingrese el número de AS de BGP: "))

if 64512 <= as_number <= 65534 or 4200000000 <= as_number <= 4294967294:
    print("El AS ingresado es privado.")
elif 1 <= as_number <= 4294967294:
    print("El AS ingresado es público.")
else:
    print("Número de AS no válido.")
