import socket
import re
import time
#AF_INET for IPv4, SOCK_STREAM for TCP (as opposed to UDP).
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tell the socket what IP and port number to connect to (must be in two brackets because it needs a tuple).
clientsocket.connect(('ctf.mf.grsu.by', 9026))
clientsocket.bind(('ctf.mf.grsu.by', 9026))

def dosome(x,y,a,b,N):
    z1 = ( x**3 + a*x +b )%N
    z2 = pow(y,2,N)
    s = ( 3*(x**2) + a )/2*y 
    x2 = (s**2-2*x)%N
    y2 = ((s*(x-x2))-y)%N
    #print("rhs = ", z1, " lhs = ", z2 ,'\nAnswer')
    if x2 == 0.0 or y2 == 0.0:
        return None
    else:
        return str(int(x2)) + "," + str(int(y2)) + "\n"

#Recieve 1024 bytes of data.
k = 0
while True:
    
    data = clientsocket.recv(1024)
    
    if k >= 1:
        data = clientsocket.recv(1024)
        print(data)

    if len(data) < 10:
        print("less")
        print(data)
        break
    #print(data)
    if not data:
        break
    #time.sleep(2)
    #Split the recieved data by newlines (returns a list).

    data = data.decode().split('\n')
    j=0
    for i in data:
        print(j, " - ", i)
        j = j + 1
 
    # Input strings
    elliptic_curve_str = data[12]
    point_str = data[14]

    
    # Regex pattern to extract a and b
    curve_pattern = r"y\^2 = x\^3 \+ ([\d\.\-]+)\*x \+ ([\d\.\-]+)"
    curve_match = re.search(curve_pattern, elliptic_curve_str)
    
    a =0
    b = 0 
    field_size = 0
    p_x = 0
    p_y = 0

    if curve_match:
        a = curve_match.group(1)
        b = curve_match.group(2)
        #print(f"a: {a}, b: {b}")

    field_size_pattern = r"Finite Field of size (\d+)"
    field_size_match = re.search(field_size_pattern, elliptic_curve_str)

    if field_size_match:
        field_size = field_size_match.group(1)
        #print(f"Field Size: {field_size}")

    # Regex pattern to extract the coordinates of P
    point_pattern = r"P = \(\s*([\d\-]+)\s*,\s*([\d\-]+)\s*\)"
    point_match = re.search(point_pattern, point_str)

    if point_match:
        p_x = point_match.group(1)
        p_y = point_match.group(2)
        #print(f"P: ({p_x}, {p_y})")

    result=dosome(int(p_x),int(p_y),int(a),int(b),int(field_size))
    #print("result: ",result)
    time.sleep(1)
    #print(result.encode('utf-8'))
    #result = result + "\n"
    #print(result.encode('utf-8'))
    clientsocket.send(str(result).encode())
    data = clientsocket.recv(1024)
    print("Data:", data)
    time.sleep(1)

print("Here")