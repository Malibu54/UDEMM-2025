class Problema1:
    def reverse(self, n: int) -> int:
    
        if n < 10:
            return n
        
        ultimo_digito = n % 10
        
        resto = n // 10
        longitud_resto = len(str(resto))
        
        
        return ultimo_digito * (10 ** longitud_resto) + self.reverse(resto)