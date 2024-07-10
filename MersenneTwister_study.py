class MersenneTwister:
    def __init__(self, seed):
        self.state = [0] * 624  # State array of 624 integers
        self.index = 0
        self.initialize_state(seed)
    
    def initialize_state(self, seed):
        self.state[0] = seed
        for i in range(1, 624):
            self.state[i] = (1812433253 * (self.state[i-1] ^ (self.state[i-1] >> 30)) + i) & 0xFFFFFFFF
    
    def twist(self):
        for i in range(624):
            y = (self.state[i] & 0x80000000) + (self.state[(i+1) % 624] & 0x7FFFFFFF)
            self.state[i] = self.state[(i + 397) % 624] ^ (y >> 1)
            if y % 2 != 0:
                self.state[i] ^= 0x9908B0DF
    
    def random_int(self):
        if self.index == 0:
            self.twist()
        
        y = self.state[self.index]
        y ^= (y >> 11)
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= (y >> 18)
        
        self.index = (self.index + 1) % 624
        return y
    
    def random(self):
        return self.random_int() / 0xFFFFFFFF

# Example usage
mt = MersenneTwister(seed=42)
print(mt.random())
print(mt.random())
print(mt.random())
