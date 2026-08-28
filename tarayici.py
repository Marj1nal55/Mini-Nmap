import socket

hedef_ip = input("Ip adresini girin: ")
for port in range(0, 1025):

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sonuc = s.connect_ex((hedef_ip, port))

  if sonuc == 0:
    print(f"Port {port} açık")

  s.close()
print("Tarama bitti")
