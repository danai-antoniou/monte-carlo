import numpy as np
import scipy.stats as st
import math
import matplotlib.pyplot as plt
# TODO parallelise - this is embarrassingly parallel


class MonteCarlo:

    def __init__(self, test_sample, control_sample, permutations, plot=False, confidence_interval=0.99,
                 asymptotic_ci=False):
        self.test_sample = test_sample
        self.control_sample = control_sample
        self.permutations = permutations
        self.plot = plot
        self.asymptotic_ci = asymptotic_ci
        self.confidence_interval = confidence_interval
        self.Z = np.concatenate((self.control_sample, self.test_sample), axis=0)
        self.n = len(self.control_sample)
        self.m = len(self.test_sample)
        self.N = self.n + self.m
        self.T_obs = abs(np.mean(self.Z[:self.n] - np.mean(self.Z[self.n:])))
        # The two variables below are for Wilcoxon
        self.ranks = st.rankdata(self.Z, method='average')  # break ties with average
        self.w_obs = sum(self.ranks[self.n:])

    @staticmethod
    def _asymptotic_ci(p, permutations, confidence_level):
        alpha = 1 - confidence_level
        alpha2 = 0.5 * alpha
        z = st.norm.ppf(1-alpha2)
        se = math.sqrt(p * (1 - p) / permutations)
        lower_cl = p - z * se
        lower_cl = float("{0:.3f}".format(lower_cl))
        upper_cl = p + z * se
        upper_cl = float("{0:.3f}".format(upper_cl))
        return [lower_cl, upper_cl]

    @staticmethod
    def _wilson_ci(p, permutations, confidence_level):
        alpha = 1 - confidence_level
        alpha2 = 0.5 * alpha
        z = st.norm.ppf(1 - alpha2)
        tmp_lower = (2 * permutations * p + z**2 - (z * math.sqrt(z**2-1/permutations+4*p*(1-p)+(4*p-2))+1)) / \
                    (2*(permutations+z**2))
        tmp_upper = (2 * permutations * p + z**2 + (z * math.sqrt(z**2 - 1/permutations + 4*p*(1-p)-(4*p-2))+1)) / \
                    (2*(permutations+z**2))
        lower_cl = np.max([0, tmp_lower])
        upper_cl = np.min([1, tmp_upper])
        return [lower_cl, upper_cl]

    def permutation(self):
        T_permutation = []
        for i in range(self.permutations):
            Z_permutation = np.random.choice(self.Z, size=self.N, replace=False)
            tmp_T = np.mean(Z_permutation[:self.n]) - np.mean(Z_permutation[self.n:])
            T_permutation.append(tmp_T)
        p_value = np.mean(abs(np.array(T_permutation)) > self.T_obs)
        if self.asymptotic_ci:
            confint = MonteCarlo._asymptotic_ci(p=p_value, permutations=self.permutations,
                                                confidence_level=self.confidence_interval)
        else:
            confint = MonteCarlo._wilson_ci(p=p_value, permutations=self.permutations,
                                            confidence_level=self.confidence_interval)
        sided_p_values = {'one_sided_p_value_less': (1-p_value / 2),
                          'one_sided_p_value_greater': p_value / 2,
                          'two_sided_p_value': p_value,
                          'two_sided_confidence_interval': confint}

        if self.plot:
            fig, ax = plt.subplots(figsize=(12, 12))
            ax.hist(T_permutation)
            ax.set_title('Histogram of permutation distribution')
            ax.axvline(x=self.T_obs, color='r', linestyle='dashed', linewidth=2)
            plt.xlabel('Permuted T-value', fontsize=13)
            plt.ylabel('Frequency', fontsize=13)
            plt.show()
        return sided_p_values

    def wilcoxon_permutation(self):
        rank_seq = np.linspace(1, self.N, num=self.N)
        w_rand = []
        for i in range(self.permutations):
            w_tmp = sum(np.random.choice(rank_seq, size=self.m, replace=False))
            w_rand.append(w_tmp)
        prob_smaller = np.mean(self.w_obs <= w_rand)
        prob_larger = np.mean(self.w_obs >= w_rand)
        p_value = 2 * np.min([prob_smaller, prob_larger])
        if self.asymptotic_ci:
            confint = MonteCarlo._asymptotic_ci(p=p_value, permutations=self.permutations,
                                                confidence_level=self.confidence_interval)
        else:
            confint = MonteCarlo._wilson_ci(p=p_value, permutations=self.permutations,
                                            confidence_level=self.confidence_interval)
        sided_p_values = {'one_sided_p_value_less': prob_smaller,
                          'one_sided_p_value_greater': prob_larger,
                          'two_sided_p_value': p_value,
                          'two_sided_confidence_interval': confint}
        if self.plot:
            fig, ax = plt.subplots(figsize=(12, 12))
            ax.hist(w_rand)
            ax.set_title('Histogram of simulated rank distribution')
            ax.axvline(x=self.w_obs, color='r', linestyle='dashed', linewidth=2)
            plt.xlabel('Simulated W', fontsize=13)
            plt.ylabel('Frequency', fontsize=13)
            plt.show()
        return sided_p_values

    def normal_approximation_wilcoxon(self):
        # E(W) under null that samples of test and control come from same distribution
        expectation = self.m * (self.m + self.n + 1) / 2
        # V(W) under null that samples of test and control come from same distribution
        variance = self.n * self.m * (self.m + self.n + 1) / 12
        # Added the +.5 below as a continuity correction
        p_value = 2 * st.norm.cdf(-abs((self.w_obs + 0.5 - expectation) / math.sqrt(variance)))
        if self.asymptotic_ci:
            confint = MonteCarlo._asymptotic_ci(p=p_value, permutations=self.permutations,
                                                confidence_level=self.confidence_interval)
        else:
            confint = MonteCarlo._wilson_ci(p=p_value, permutations=self.permutations,
                                            confidence_level=self.confidence_interval)
        sided_p_values = {'one_sided_p_value': p_value / 2,
                          'two_sided_p_value': p_value,
                          'two_sided_confidence_interval': confint}
        return sided_p_values