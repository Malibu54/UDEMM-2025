class Computadora:
    def __init__(self,hadd=None, memoria=None, gpu=None, cpu=None, motherboard=None):
        self.hdd = self.hdd
        self.memoria = memoria
        self.gpu = gpu
        self.cpu = cpu
        self.motherboard = motherboard

    def __str__(self):
        return(
            f"Computadora:\n"
            f"HDD:{self.hdd} GB\n"
            f"RAM:{self.memoria}\n"
            f"GPU:{self.gpu}\n"
            f"CPU:{self.cpu}\n"
            f"motherboard:{self.motherboard}\n"

        )
    
    class ComputadoraBuilder:
        def __init__(self):
            self.computadora = Computadora()
        
        def __init__(self,hdd):
            self._computadora.hdd = hdd
            return(self)
        
        def __init__(self,memoria):
            self._computadora.memoria = memoria
            return(self)
        
        def __init__(self,gpu):
            self._computadora.gpu = gpu
            return(self)
        
        def __init__(self,cpu):
            self._computadora.cpu = cpu
            return(self)
        
        def __init__(self,motherboard):
            self._computadora.motherboard = motherboard
            return(self)

    