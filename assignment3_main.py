from statistics import NormalDist
import unittest 
import matplotlib.pyplot as plt


class SignalDetection:
    def __init__(self, hits, misses, falseAlarm, correctRejections):
        lst = [hits, misses, falseAlarm, correctRejections]
        for item in lst:
            if int(item) < 0:
                raise ValueError("Number of trials cannot be negative.")
    
        self.hits = hits
        self.misses = misses
        self.falseAlarm = falseAlarm
        self.correctRejections = correctRejections
        self.hit_rate = hits / (hits + misses)
        self.false_alarm_rate = falseAlarm / (falseAlarm + correctRejections)
        self.z_h = NormalDist().inv_cdf(self.hit_rate)
        self.z_fa = NormalDist().inv_cdf(self.false_alarm_rate)

    def d_prime(self):
        d = self.z_h - self.z_fa
        return d

    def criterion(self):
        c = (-0.5) * (self.z_h + self.z_fa)
        return c



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
       sd.hits = 5
       sd.misses = 5
       sd.correctRejections = 5
       sd.falseAlarm = 5
       sd.hit_rate = 5
       sd.false_alarm_rate = 5
       sd.z_fa = 5
       sd.z_h = 5
       expected_c = SignalDetection(1, 2, 3, 1).criterion()
       obtained_c = sd.criterion()
       self.assertEqual(obtained_c, expected_c)



if __name__ == "__main__":
    unittest.main()
