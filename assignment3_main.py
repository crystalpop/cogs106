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

    def plot_roc(self):
       x = [0, self.__hit_rate, 1]
       y = [0, self.__false_alarm_rate, 1]
       plt.plot(x, y, 'b')
       plt.plot(self.__hit_rate, self.__false_alarm_rate, 'bo')
       plt.xlabel("Hit rate")
       plt.ylabel("False alarm rate")
       plt.title("ROC curve")
       plt.show()
       
    def plot_std(self):
        x = np.arange(-4, 4, 0.01)
        #N
        plt.plot(x, norm.pdf(x, 0, 1), 'b', label = "N")
        #S
        plt.plot(x, norm.pdf(x, self.d_prime(), 1), 'r', label = "S")
        #C
        plt.axvline((self.d_prime()/2) + self.criterion(),color = 'black', linestyle = '--').set_label("C")
        #D
        plt.plot([self.d_prime(), 0], [0.4, 0.4], 'k', label = "D")

        plt.xlabel("Decision variable")
        plt.ylabel("Probability")
        plt.title("Signal Detection Theory")
        plt.legend()
        plt.show()

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

    def test_addition(self):
       sd = SignalDetection(1, 1, 2, 1) + SignalDetection(2, 1, 1, 3)
       expected = SignalDetection(3, 2, 3, 4).criterion()
       obtained = sd.criterion()
       # Compare calculated and expected criterion
       self.assertEqual(obtained, expected)

    def test_multiplication(self):
       sd = SignalDetection(1, 2, 3, 1) * 4
       expected = SignalDetection(4, 8, 12, 4).criterion()
       obtained = sd.criterion()
       # Compare calculated and expected criterion
       self.assertEqual(obtained, expected)

        

if __name__ == "__main__":
    unittest.main()
