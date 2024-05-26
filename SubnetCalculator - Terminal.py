#Code will take the input of a Host IP Address and Major Network Mask and will output the following:
#1. Major Network Address
#2. Major Network Broadcast Address
#3. CIDR Notation Major Network Address
#4. Number of Host Bits
#5. Number of Hosts
#6. Subnet Mask
#7. Number of Subnet Bits
#8. Number of Usable Subnets
#9. Number of Host Bits per Subnet
#10. Number of Usable Hosts per Subnet
#11. Subnet Address for this Host
#12. First Host IP Address for this Subnet
#13. Last Host IP Address for this Subnet
#14. Broadcast Address for this Subnet
def convertToBinary(x):
    # split the address into 4 octets
    octets = x.split(".")
    binaryOctets = []
    # convert each octet to binary
    for octet in octets:
        binaryOctets.append(bin(int(octet))[2:].zfill(8))
    # join the binary octets into a single binary string
    binaryString = ".".join(binaryOctets)
    return binaryString

def convertToDecimal(x):
    #split the binary address into 4 octets
    octets = x.split(".")
    decimalOctets = []
    #convert each octet to decimal
    for octet in octets:
        decimalOctets.append(str(int(octet, 2)))
    return ".".join(decimalOctets)

def bitwiseAND(xBinary, yBinary):
    octets1 = xBinary.split(".")
    octets2 = yBinary.split(".")  
    result = []
    for i in range(4):
        result.append(str(int(octets1[i], 2) & int(octets2[i], 2)))  # Perform bitwise AND on binary representations of octets
    return ".".join(result)  # Join the resulting octets into a single string separated by dots

def add_periods(string):
    return '.'.join(string[i:i+8] for i in range(0, len(string), 8)) # Split the binary string into octets of 8 bits

def flip_network_bits(xstring, numBits):
    xstring = xstring.replace(".", "")  # Remove the dots from the binary string
    # Find all sequences of zeros
    consecutive_ones = xstring[:-numBits]
    xstring = consecutive_ones + '1' * (32 - len(consecutive_ones))
    return add_periods(xstring)


#get input from user
hostIP = input("Enter Host IP Address: ")
majorMask = input("Enter Major Network Mask: ")

#convert IP Address and Major Network Mask to binary
hostBinary = convertToBinary(hostIP)
majorMaskBinary = convertToBinary(majorMask)

#calculate Major Network Address
majorNetAddress = bitwiseAND(hostBinary, majorMaskBinary)
print("Major Network Address: ", majorNetAddress)

#calculate Major Network Broadcast Address
print("Major Network Broadcast Address: ", convertToDecimal(flip_network_bits(convertToBinary(majorNetAddress), majorMaskBinary.count("0"))))

#calculate CIDR Notation Major Network Address
cidrNotation = majorNetAddress + "/" + str(majorMaskBinary.count("1"))
print("CIDR Notation Major Network Address: ", cidrNotation)

#calculate Number of Host Bits
print("Number of Host Bits: ", majorMaskBinary.count("0"))

#calculate Number of Hosts
numHosts = 2 ** majorMaskBinary.count("0") - 2
print("Number of Usable Hosts: ", numHosts)

#Get Subnet Mask
subnetMask = input("Enter Subnet Mask: ")
subnetMaskBinary = convertToBinary(subnetMask)

#calculate Number of Subnet Bits (by checking the differece in the change in host bits)
numSubnetBits = subnetMaskBinary.count("1") - majorMaskBinary.count("1")
print("Number of Subnet Bits: ", numSubnetBits)

# #calculate Number of Usable Subnets
repeat = True
while repeat:
    allZerosOption = input("Is the all 0's subnet usable? (Y/N): ")
    if allZerosOption.lower() in ["y", "yes"]:
        AllZeros = True
        repeat = False
    elif allZerosOption.lower() in ["n", "no"]:
        AllZeros = False
        repeat = False
    else:
        print("Invalid input")
        print("Enter Y or N:")

repeat = True
while repeat:
    allOnesOption = input("Is the all 1's subnet usable? (Y/N): ")
    if allOnesOption.lower() in ["y", "yes"]:
        AllOnes = True
        repeat = False
    elif allOnesOption.lower() in ["n", "no"]:
        AllOnes = False
        repeat = False
    else:
        print("Invalid input")
        print("Enter Y or N:")
if AllZeros == True and AllOnes == True:
    numSubnets = 2 ** numSubnetBits - 2
elif AllZeros == True and AllOnes == False:
    numSubnets = 2 ** numSubnetBits - 1
elif AllZeros == False and AllOnes == True:
    numSubnets = 2 ** numSubnetBits - 1
else:
    numSubnets = 2 ** numSubnetBits

print("Number of Usable Subnets: ", numSubnets)

#calculate Number of Host Bits per Subnet
numHostBitsPerSubnet = subnetMaskBinary.count("0")
print("Number of Host Bits per Subnet: ", numHostBitsPerSubnet)

#calculate Number of Usable Hosts per Subnet
numUsableHostsPerSubnet = 2 ** numHostBitsPerSubnet - 2
print("Number of Usable Hosts per Subnet: ", numUsableHostsPerSubnet)

#calulate Subnet Address for this Host
subnetNetAddress = bitwiseAND(hostBinary, subnetMaskBinary)
print("Subnet Address for this Host: ", subnetNetAddress)

#calculate First Host IP Address for this Subnet
#this is done by converting the subnet address to binary, adding 1, then converting it back to decimal
subnetNetAddressBinary = convertToBinary(subnetNetAddress).replace(".", "")
subnetNetAddressBinary = "1" + subnetNetAddressBinary
firstHostAddress = str(int(subnetNetAddressBinary) + 1)
firstHostAddress = add_periods(firstHostAddress[1:])
print("First Host IP Address for this Subnet: ", convertToDecimal(firstHostAddress))

#calculate Broadcast IP Address for this Subnet'
#this is done by converting the subnet address to binary, removing the host bits, then adding 1's to the end
subnetBroadcastAddress = (convertToBinary(subnetNetAddress))[:-numHostBitsPerSubnet] + '1' * numHostBitsPerSubnet
print("Broadcast Address for this Subnet: ", convertToDecimal(subnetBroadcastAddress))

#calculate Last Host IP Address for this Subnet
#this is done by converting the Broadcast address to binary, subtracting 1, then converting it back to decimal
subnetBroadcastAddress = subnetBroadcastAddress.replace(".", "")
subnetBroadcastAddress = "1" + subnetBroadcastAddress
lastHostAddress = str(int(subnetBroadcastAddress) - 1)
lastHostAddress = add_periods(lastHostAddress[1:])
print("Last Host IP Address for this Subnet: ", convertToDecimal(lastHostAddress))

#get nth Number of Subnet
nthSubnet = int(input("Enter the nth Subnet:  "))
if AllZeros == True:
    nthSubnet = nthSubnet - 1

#calculate the nth Network Subnet Address
#this is done by removing the subnet bits and host bits, convert the nth subnet to binary, then adding the subnet bits and host bits
nthSubnetNetAddress = convertToBinary(subnetNetAddress).replace(".", "")[:-numSubnetBits][:-numHostBitsPerSubnet]
addressfill = numSubnetBits - len(bin(nthSubnet)[2:])
nthSubnetNetAddress = nthSubnetNetAddress + '0' * addressfill + bin(nthSubnet)[2:]
nthSubnetNetAddress = nthSubnetNetAddress + '0' * (32 - len(nthSubnetNetAddress))
print("Network Address of the nth usable subnet: ", convertToDecimal(add_periods(nthSubnetNetAddress)))

#calculate the nth Network Broadcast Address
#this is done by removing the host bits, then adding 1's to the end
nthSubnetBroadcastAddress = add_periods(nthSubnetNetAddress)[:-numHostBitsPerSubnet] + '1' * numHostBitsPerSubnet
print("Broadcast Address of the nth usable subnet: ", convertToDecimal(nthSubnetBroadcastAddress))