from pyscript import document

def get_ordinal(n):
    if 11 <= (n % 100) <= 13:
        return "th"
    else:
        if n % 10 == 1:
            return "st"
        elif n % 10 == 2:
            return "nd"
        elif n % 10 == 3:
            return "rd"
        else:
            return "th"

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
    # Get the input values from the HTML elements
    hostIP_input = document.querySelector("#hostIP")
    hostIP = hostIP_input.value
    
    majorMask_input = document.querySelector("#majorMask")
    majorMask = majorMask_input.value
    
    subnetMask_input = document.querySelector("#subnetMask")
    subnetMask = subnetMask_input.value

    nthSubnet_input = document.querySelector("#nthSubnet")
    nthSubnet = nthSubnet_input.value
    nthSubnet = int(nthSubnet)
    nthSubnet_initial = nthSubnet

    allZeros = document.querySelector("#yes_allZero").checked
    allOnes = document.querySelector("#yes_allOnes").checked


    # Convert IP addresses to binary representation
    hostBinary = convertToBinary(hostIP)
    majorMaskBinary = convertToBinary(majorMask)
    subnetMaskBinary = convertToBinary(subnetMask)

    # Calculate major network address
    majorNetAddress = bitwiseAND(hostBinary, majorMaskBinary)
    majorNetAddress_output = "Major Network Address: " + majorNetAddress

    # Calculate major network broadcast address
    majorNetBroadcastAddress = flip_network_bits(convertToBinary(majorNetAddress), majorMaskBinary.count("0"))
    majorNetBroadcastAddressDecimal = convertToDecimal(majorNetBroadcastAddress)
    majorNetBroadcastAddress_output = "Major Network Broadcast Address: " + majorNetBroadcastAddressDecimal

    # Calculate CIDR notation for major network address
    cidrNotation = majorNetAddress + "/" + str(majorMaskBinary.count("1"))
    cidrNotation_output = "CIDR Notation Major Network Address: " + cidrNotation

    # Calculate the number of host bits
    numHostBits = majorMaskBinary.count("0")
    numHostBits_output = "Number of Host Bits: " + str(numHostBits)

    # Calculate the number of usable hosts
    numHosts = 2 ** numHostBits - 2
    numHosts_output = "Number of Usable Hosts: " + str(numHosts)

    # Calculate the number of subnet bits
    numSubnetBits = subnetMaskBinary.count("1") - majorMaskBinary.count("1")
    numSubnetBits_output = "\nNumber of Subnet Bits: " + str(numSubnetBits)

    # Calculate the number of usable subnets
    if allZeros and allOnes:
        numSubnets = 2 ** numSubnetBits - 2
    elif allZeros or allOnes:
        numSubnets = 2 ** numSubnetBits - 1
    else:
        numSubnets = 2 ** numSubnetBits

    numSubnets_output = "Number of Usable Subnets: " + str(numSubnets)
    
    # Calculate the number of host bits per subnet
    numHostBitsPerSubnet = subnetMaskBinary.count("0")
    numHostBitsPerSubnet_output = "Number of Host Bits per Subnet: " + str(numHostBitsPerSubnet)

    # Calculate the number of usable hosts per subnet
    numUsableHostsPerSubnet = 2 ** numHostBitsPerSubnet - 2
    numUsableHostsPerSubnet_output = "Number of Usable Hosts per Subnet: " + str(numUsableHostsPerSubnet)

    # Calculate the subnet address for the given host
    subnetNetAddress = bitwiseAND(hostBinary, subnetMaskBinary)
    subnetNetAddress_output = "\nSubnet Address for this Host: " + subnetNetAddress

    # Calculate the first host IP address for the subnet
    subnetNetAddressBinary = convertToBinary(subnetNetAddress).replace(".", "")
    subnetNetAddressBinary = "1" + subnetNetAddressBinary
    firstHostAddress = str(int(subnetNetAddressBinary) + 1)
    firstHostAddress = add_periods(firstHostAddress[1:])
    firstHostAddress_output = "First Host IP Address for this Subnet: " + convertToDecimal(firstHostAddress)

    # Calculate the broadcast address for the subnet
    subnetBroadcastAddress = (convertToBinary(subnetNetAddress))[:-numHostBitsPerSubnet] + '1' * numHostBitsPerSubnet
    subnetBroadcastAddress_output = "Broadcast Address for this Subnet: " + convertToDecimal(subnetBroadcastAddress)

    # Calculate the last host IP address for the subnet
    subnetBroadcastAddress = subnetBroadcastAddress.replace(".", "")
    subnetBroadcastAddress = "1" + subnetBroadcastAddress
    lastHostAddress = str(int(subnetBroadcastAddress) - 1)
    lastHostAddress = add_periods(lastHostAddress[1:])
    lastHostAddress_output = "Last Host IP Address for this Subnet: " + convertToDecimal(lastHostAddress)

    # Calculate the network address of the nth usable subnet
    if allZeros:
        nthSubnet = nthSubnet - 1
    
    nthSubnetSuffix = get_ordinal(int(nthSubnet_initial))
    nthSubnetNetAddress = convertToBinary(subnetNetAddress).replace(".", "")[:-numSubnetBits][:-numHostBitsPerSubnet]
    addressfill = numSubnetBits - len(bin(nthSubnet)[2:])
    nthSubnetNetAddress = nthSubnetNetAddress + '0' * addressfill + bin(nthSubnet)[2:]
    nthSubnetNetAddress = nthSubnetNetAddress + '0' * (32 - len(nthSubnetNetAddress))
    nthSubnetNetAddress_output = "\nNetwork Address of the " + str(nthSubnet_initial) + nthSubnetSuffix + " usable subnet: " + convertToDecimal(add_periods(nthSubnetNetAddress))

    # Calculate the broadcast address of the nth usable subnet
    nthSubnetBroadcastAddress = add_periods(nthSubnetNetAddress)[:-numHostBitsPerSubnet] + '1' * numHostBitsPerSubnet
    nthSubnetBroadcastAddress_output = "Broadcast Address of the  " + str(nthSubnet_initial) + nthSubnetSuffix + " usable subnet: " + convertToDecimal(nthSubnetBroadcastAddress)

    # Generate the output string
    output = "\n".join([majorNetAddress_output, majorNetBroadcastAddress_output, cidrNotation_output, numHostBits_output, numHosts_output, numSubnetBits_output, numSubnets_output, numHostBitsPerSubnet_output, numUsableHostsPerSubnet_output, subnetNetAddress_output, firstHostAddress_output, lastHostAddress_output, subnetBroadcastAddress_output, nthSubnetNetAddress_output, nthSubnetBroadcastAddress_output])
    
    # Update the output element in the HTML
    output_div = document.querySelector("#output")
    output_div.innerText = output
