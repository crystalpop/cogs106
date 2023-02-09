import scipy.stats as stats

class SignalDetection:
    def __init__(self, hits, misses, falseAlarms, correctRejections):
        self.hits = int(hits)
        self.misses = int(misses)
        self.falseAlarms = int(falseAlarms)
        self.correctRejections = int(correctRejections)
        self.hit_rate = self.hits/(self.hits + self.misses)
        self.false_rate = self.falseAlarms/(self.falseAlarms + self.correctRejections)
        self.z_h = stats.norm.ppf(self.hit_rate)
        self.z_fa = stats.norm.ppf(self.false_rate)

    def d_prime(self):
        d = self.z_h - self.z_fa
        return d

    def criterion(self):
        c = (-0.5) * (self.z_h + self.z_fa)
        return c


