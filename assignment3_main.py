from statistics import NormalDist
import unittest 
import matplotlib.pyplot as plt


class SignalDetection:
    def __init__(self, hits, misses, falseAlarm, correctRejections):
        lst = [hits, misses, falseAlarm, correctRejections]
        for item in lst:
            if int(item) < 0:
                raise ValueError("Number of trials cannot be negative.")
    
        self.__hits = hits
        self.__misses = misses
        self.__falseAlarm = falseAlarm
        self.__correctRejections = correctRejections
        self.__hit_rate = self.__hits / (self.__hits + self.__misses)
        self.__false_alarm_rate = self.__falseAlarm / (self.__falseAlarm + self.__correctRejections)
        self.__z_h = NormalDist().inv_cdf(self.__hit_rate)
        self.__z_fa = NormalDist().inv_cdf(self.__false_alarm_rate)

    def d_prime(self):
        d = self.__z_h - self.__z_fa
        return d

    def criterion(self):
        c = (-0.5) * (self.__z_h + self.__z_fa)
        return c

    def __add__(self, other):
       return SignalDetection(self.__hits + other.__hits, self.__misses + other.__misses, self.__falseAlarm + other.__falseAlarm, self.__correctRejections + other.__correctRejections)

    def __mul__(self, scalar):
       return SignalDetection(self.__hits * scalar, self.__misses * scalar, self.__falseAlarm * scalar, self.__correctRejections * scalar)


class TestSignalDetection(unittest.TestCase):
    def test_d_prime_zero(self):
        sd   = SignalDetection(15, 5, 15, 5)
        expected = 0
        obtained = sd.d_prime()
        # Compare calculated and expected d-prime
        self.assertAlmostEqual(obtained, expected, places=6)

    def test_d_prime_nonzero(self):
        sd   = SignalDetection(15, 10, 15, 5)
        expected = -0.421142647060282
        obtained = sd.d_prime()
        # Compare calculated and expected d-prime
        self.assertAlmostEqual(obtained, expected, places=6)

    def test_criterion_zero(self):
        sd   = SignalDetection(5, 5, 5, 5)
        # Calculate expected criterion        
        expected = 0
        obtained = sd.criterion()
        # Compare calculated and expected criterion
        self.assertAlmostEqual(obtained, expected, places=6)

    def test_criterion_nonzero(self):
        sd   = SignalDetection(15, 10, 15, 5)
        # Calculate expected criterion        
        expected = -0.463918426665941
        obtained = sd.criterion()
        # Compare calculated and expected criterion
        self.assertAlmostEqual(obtained, expected, places=6)

    def test_corruption(self):
       sd = SignalDetection(1, 2, 3, 1)
       sd.__hits = 5
       sd.__misses = 5
       sd.__correctRejections = 5
       sd.__falseAlarm = 5
       sd.__hit_rate = 5
       sd.__false_alarm_rate = 5
       sd.__z_fa = 5
       sd.__z_h = 5
       expected_c = SignalDetection(1, 2, 3, 1).criterion()
       obtained_c = sd.criterion()
       self.assertEqual(obtained_c, expected_c)



if __name__ == "__main__":
    unittest.main()
