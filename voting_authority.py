
import os
import random


from config import *

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def modinv(a, m):  
    g, x, y = egcd(a, m)
    if g != 1:
        
        return -1
    else:
        return x % m

def lcm(x, y):
    
    if x > y:
        greater = x
    else:
        greater = y
    LCM = 0
    while(True):
        if((greater % x == 0) and (greater % y == 0)):
            LCM = greater
            break
        greater += 1

    return LCM

def gcd(x, y):
   
    return abs(x * y) / lcm(x, y)


def isPrime(n):
    
    if (n <= 1):
        return False
    if (n <= 3):
        return True
  
    if (n % 2 == 0 or n % 3 == 0):
        return False
    i = 5
    while(i * i <= n):
        if (n % i == 0 or n % (i + 2) == 0):
            return False
        i = i + 6
    return True


def generate2Prime(a=0, b=100):
   
    n1 = 0
    n2 = 0
    primes = [i for i in range(a, b) if isPrime(i)]
    if len(primes) >= 2:
        n1 = random.choice(primes)
        primes.remove(n1)
        n2 = random.choice(primes)
    return n1, n2

def print_candidate_result(data):
   
    max_count = max(data)
    max_occurences = data.count(max_count)
    if max_occurences ==  1:
        print("Candidate " + str(data.index(max_count)+ 1) + " win this election with " + str(max_count) + " votes!")
    else:
        print("This election results in a draw between " + str(max_occurences) + " candidates, each of whom have " + str(max_count) + " votes!")



def generate_data():
   
    inp_test = input(
        "Do you want to test paillier encryption key? 1 for yes, other value for no: ")
    allValueFound = False
    n, g, L, k, meu, p, q = 0, 0, 0, 0, 0, 0, 0
    # Loop until all values is found
    while not allValueFound:
        p, q = generate2Prime(prime_lowerbound, prime_upperbound)
       
        while gcd(p*q, (p-1)*(q-1)) != 1:
            print("Regenerating p and q!")
            p, q = generate2Prime(prime_lowerbound, prime_upperbound)
        n = p*q
        
        g = random.randrange(1, n**2 + 1)
        L = lcm((p-1), (q-1))
        u = pow(g, L, n*n)
        k = int((u-1)/n)
        meu = int(modinv(k, n))
        if meu == -1:
            print("Redoing the generation! Modular inverse not found!")
        elif n < minimum_n_value:
            print("n is too small! Do not satisfy n >=", str(minimum_n_value),  "(larger than", str(number_of_bits* number_of_candidates) ,"bits binary)!")
        else:
            allValueFound = True
 
    file_public = open("public.txt", "w")
    file_public.write(str(n) + " " + str(g))
    file_public.close()
    file_private = open("private.txt", "w")
    file_private.write(str(n) + " " + str(L) + " " + str(meu))
    file_private.close()
    print("-------------------------------------------------")
    print("Private key file and public key file is generated")
    print("-------------------------------------------------")
    
    file_voter = open("voter.txt", "w")
    for i in range(1, voter + 1):
        file_voter.write("Voter" + str(i) + " " + str(i) + " " + "0 -1\n")
    file_voter.close()
    print("Voter information file is generated")
    print("There are a total of " + str(voter) +
          " voters (Voter1 to Voter" + str(voter) + ")!")
    print("-------------------------------------------------")
    
    with open('vote_status.txt', 'w') as writer:
        writer.write("0")
    
    if os.path.exists("encrypted_vote.txt"):
        os.remove("encrypted_vote.txt")
    if os.path.exists("homomorphic_vote.txt"):
        os.remove("homomorphic_vote.txt")
    print("All system file has been reinitialized!")
    print("-------------------------------------------------")
    
    print("The value of 'p' and 'q' is: ", str(p), ",", str(q))
    print("The value of 'n' is: "+str(n))
    print("The Public-Key (n,g) := ("+str(n)+", "+str(g)+")")
    print("The value of 'Lambda' is: "+str(L))
    print("The value of k is := "+str(k))
    print("The value of 'Meu' is := "+str(meu))
    print("Private-Key (Lambda,Meu) := ("+str(L)+", "+str(meu)+")")
   
    if inp_test == "1":
        print("-------------------- Testing --------------------")
        m_str = input(
            "Enter the value of Message 'm' (as Integer), m < " + str(n) + ": ")
        m = int(m_str)
        r_str = input("Enter the value of 'r' (as Integer): ")
        r = int(r_str)
        C = int(((g**m)*(r**n)) % (n*n))
        print("Ciphertext, C := "+str(C))
        u1 = pow(C, L, n*n)
        L_of_u1 = int((u1-1)/n)
        M = int((L_of_u1 * meu) % n)
        print("Extracted Message, M := " + str(M))


def decrypt_homomorphic():
    
    
    if not os.path.isfile('private.txt'):
        print("No private key found! Please run election data generation in this program!")
        return
    if not os.path.isfile('homomorphic_vote.txt'):
        print("No homomorphic encrypted data found! Please run homomorphic_server.py if voting has ended!")
        return
   
    with open("homomorphic_vote.txt", "r") as reader:
        c_homomorphic = int(reader.readline())
    with open("private.txt", "r") as reader:
        data = reader.readline().strip().split(" ")
        n, L, meu = int(data[0]), int(data[1]), int(data[2])
   
    u1 = pow(c_homomorphic, L, n*n)
    L_of_u1 = int((u1-1)/n)
    M = int((L_of_u1 * meu) % n)
    
    data_M = str(bin(M))[2:].zfill(number_of_candidates * number_of_bits)
    print("Extracted Homomorphic Message: M := " + str(M))
    print("Convert to binary:", data_M)

    vote_count_candidates = [int(data_M[i:i+number_of_bits], 2) for i in range(0, len(data_M), number_of_bits)][::-1]
    print("Vote count array for candidates (candidate 1 to candidate", str(number_of_candidates) + "):" ,str(vote_count_candidates))
 
    print_candidate_result(vote_count_candidates)

if __name__ == "__main__":
    print("Python File for Voting Authority")
    inp = input(
        "Enter 1 for data and paillier key generation, 2 for decrypting the homomorphic value from server for final result: ")
    if inp == "1":
        generate_data()
    elif inp == "2":
        decrypt_homomorphic()
    else:
        print("wrong input!")
