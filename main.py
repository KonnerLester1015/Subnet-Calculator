from pyscript import document

def convertToBinary(x):
    octets = x.split(".")
    binaryOctets = [bin(int(octet))[2:].zfill(8) for octet in octets]
    binaryString = ".".join(binaryOctets)
    return binaryString

def convertToDecimal(x):
    octets = x.split(".")
    decimalOctets = [str(int(octet, 2)) for octet in octets]
    return ".".join(decimalOctets)

def bitwiseAND(xBinary, yBinary):
    octets1 = xBinary.split(".")
    octets2 = yBinary.split(".")
    result = [str(int(octets1[i], 2) & int(octets2[i], 2)) for i in range(4)]
    return ".".join(result)

def add_periods(string):
    return '.'.join(string[i:i+8] for i in range(0, len(string), 8))

def flip_network_bits(xstring, numBits):
    xstring = xstring.replace(".", "")
    consecutive_ones = xstring[:-numBits]
    xstring = consecutive_ones + '1' * (32 - len(consecutive_ones))
    return add_periods(xstring)

def calculate_subnet_info(event):
    hostIP_input = document.querySelector("#hostIP")
    hostIP = hostIP_input.value
    
    majorMask_input = document.querySelector("#majorMask")
    majorMask = majorMask_input.value
    
    subnetMask_input = document.querySelector("#subnetMask")
    subnetMask = subnetMask_input.value

    nthSubnet_input = document.querySelector("#nthSubnet")
    nthSubnet = nthSubnet_input.value
    if nthSubnet == "2":
        nthSubnetInitial = "2nd"
    elif nthSubnet == "3":
        nthSubnetInitial = "3rd"
    else:
        nthSubnetInitial = nthSubnet + "th"
    nthSubnet = int(nthSubnet)

    allZeros = document.querySelector("#yes_allZero").checked
    allOnes = document.querySelector("#yes_allOnes").checked


    hostBinary = convertToBinary(hostIP)
    majorMaskBinary = convertToBinary(majorMask)
    subnetMaskBinary = convertToBinary(subnetMask)

    majorNetAddress = bitwiseAND(hostBinary, majorMaskBinary)
    majorNetAddress_output = "Major Network Address: " + majorNetAddress

    majorNetBroadcastAddress = flip_network_bits(convertToBinary(majorNetAddress), majorMaskBinary.count("0"))
    majorNetBroadcastAddressDecimal = convertToDecimal(majorNetBroadcastAddress)
    majorNetBroadcastAddress_output = "Major Network Broadcast Address: " + majorNetBroadcastAddressDecimal

    cidrNotation = majorNetAddress + "/" + str(majorMaskBinary.count("1"))
    cidrNotation_output = "CIDR Notation Major Network Address: " + cidrNotation

    numHostBits = majorMaskBinary.count("0")
    numHostBits_output = "Number of Host Bits: " + str(numHostBits)

    numHosts = 2 ** numHostBits - 2
    numHosts_output = "Number of Usable Hosts: " + str(numHosts)

    numSubnetBits = subnetMaskBinary.count("1") - majorMaskBinary.count("1")
    numSubnetBits_output = "\nNumber of Subnet Bits: " + str(numSubnetBits)

    if allZeros and allOnes:
        numSubnets = 2 ** numSubnetBits - 2
    elif allZeros or allOnes:
        numSubnets = 2 ** numSubnetBits - 1
    else:
        numSubnets = 2 ** numSubnetBits

    numSubnets_output = "Number of Usable Subnets: " + str(numSubnets)
    
    numHostBitsPerSubnet = subnetMaskBinary.count("0")
    numHostBitsPerSubnet_output = "Number of Host Bits per Subnet: " + str(numHostBitsPerSubnet)

    numUsableHostsPerSubnet = 2 ** numHostBitsPerSubnet - 2
    numUsableHostsPerSubnet_output = "Number of Usable Hosts per Subnet: " + str(numUsableHostsPerSubnet)

    subnetNetAddress = bitwiseAND(hostBinary, subnetMaskBinary)
    subnetNetAddress_output = "\nSubnet Address for this Host: " + subnetNetAddress

    subnetNetAddressBinary = convertToBinary(subnetNetAddress).replace(".", "")
    subnetNetAddressBinary = "1" + subnetNetAddressBinary
    firstHostAddress = str(int(subnetNetAddressBinary) + 1)
    firstHostAddress = add_periods(firstHostAddress[1:])
    firstHostAddress_output = "First Host IP Address for this Subnet: " + convertToDecimal(firstHostAddress)

    subnetBroadcastAddress = (convertToBinary(subnetNetAddress))[:-numHostBitsPerSubnet] + '1' * numHostBitsPerSubnet
    subnetBroadcastAddress_output = "Broadcast Address for this Subnet: " + convertToDecimal(subnetBroadcastAddress)

    subnetBroadcastAddress = subnetBroadcastAddress.replace(".", "")
    subnetBroadcastAddress = "1" + subnetBroadcastAddress
    lastHostAddress = str(int(subnetBroadcastAddress) - 1)
    lastHostAddress = add_periods(lastHostAddress[1:])
    lastHostAddress_output = "Last Host IP Address for this Subnet: " + convertToDecimal(lastHostAddress)

    if allZeros:
        nthSubnet = nthSubnet - 1
        
    nthSubnetNetAddress = convertToBinary(subnetNetAddress).replace(".", "")[:-numSubnetBits][:-numHostBitsPerSubnet]
    addressfill = numSubnetBits - len(bin(nthSubnet)[2:])
    nthSubnetNetAddress = nthSubnetNetAddress + '0' * addressfill + bin(nthSubnet)[2:]
    nthSubnetNetAddress = nthSubnetNetAddress + '0' * (32 - len(nthSubnetNetAddress))
    nthSubnetNetAddress_output = "\nNetwork Address of the " + nthSubnetInitial + " usable subnet: " + convertToDecimal(add_periods(nthSubnetNetAddress))

    nthSubnetBroadcastAddress = add_periods(nthSubnetNetAddress)[:-numHostBitsPerSubnet] + '1' * numHostBitsPerSubnet
    nthSubnetBroadcastAddress_output = "Broadcast Address of the  " + nthSubnetInitial + " usable subnet: " + convertToDecimal(nthSubnetBroadcastAddress)

    output = "\n".join([majorNetAddress_output, majorNetBroadcastAddress_output, cidrNotation_output, numHostBits_output, numHosts_output, numSubnetBits_output, numSubnets_output, numHostBitsPerSubnet_output, numUsableHostsPerSubnet_output, subnetNetAddress_output, firstHostAddress_output, subnetBroadcastAddress_output, lastHostAddress_output, nthSubnetNetAddress_output, nthSubnetBroadcastAddress_output])
    
    output_div = document.querySelector("#output")
    output_div.innerText = output

