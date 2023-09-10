import random 
import math
import json

class KeyGen():
    def __init__(self):
        self.n = None
        self.phi = self.get_phi(10000,15000)
        self.e =  self.get_public()
        gcd, self.d, y = self.euclid_extended(self.e, self.phi)
        self.write_to_json()
    
    def write_to_json(self):
        public = {"e": self.e, "n" : self.n}
        with open("public.json", "w") as f:
            json.dump(public,f )
        
        private = {"d" : self.d}
        with open("private.json", "w") as f:
            json.dump(private,f)

    
    def is_prime(self, number):
        if number < 2:
            return False
        for i in range(2,number//2+1):
            if number%i == 0:
                return False
        return True
    
    def generate_prime(self, min_v, max_v):
        p  = random.randint(min_v, max_v)
        while not self.is_prime(p):
            p = random.randint(min_v, max_v)
        return p
    
    def euclid_extended(self,e, phi):
        if e == 0 :
            return phi,0,1     
        gcd,x1,y1 = self.euclid_extended(phi%e, e)
        d = y1 - (phi//e) * x1
        y = x1
        return gcd, d, y
  
    
    def get_phi(self, min, max):
        p1 = self.generate_prime(min,max)
        p2 = self.generate_prime(min,max)
        self.n = p1*p2
        return (p1-1)*(p2-1)
        

    def get_public(self):
        e = random.randint(3, self.phi-1)
        while math.gcd(e,self.phi) != 1:
            e = random.randint(3, self.phi-1)
        return e
