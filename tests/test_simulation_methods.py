from model.simulation_methods import MonteCarlo
import numpy as np

control = np.array([34, 45, 49, 55, 58, 59, 61, 62, 86])
test = np.array([5, 8, 18, 24, 60, 84, 96])
permutations = 10000


def test_permutation():
    eval = MonteCarlo(test_sample=test, control_sample=control, permutations=permutations, plot=False).permutation()
    assert eval['two_sided_p_value'] <= .35
    assert eval['two_sided_p_value'] >= .25


def test_wilcoxon_permutation():
    eval = MonteCarlo(test, control, permutations, False, confidence_interval=.99).wilcoxon_permutation()
    assert eval['two_sided_p_value'] <= .45
    assert eval['two_sided_p_value'] >= .35


def test_normal_approximation_wilcoxon():
    eval = MonteCarlo(test, control, permutations).normal_approximation_wilcoxon()
    rounded_p_value = float("{0:.7f}".format(eval['two_sided_p_value']))
    assert rounded_p_value == 0.3971011


def test_confidence_interval():
    eval = MonteCarlo(test_sample=test, control_sample=control, permutations=permutations, plot=False,
                      confidence_interval=.99).permutation()
    assert eval['two_sided_confidence_interval'] >= [.28]
    assert eval['two_sided_confidence_interval'] <= [.32]


def test_wilcoxon_confidence_interval():
    eval = MonteCarlo(test, control, permutations, False, confidence_interval=.99).wilcoxon_permutation()
    assert eval['two_sided_confidence_interval'] >= [.39]
    assert eval['two_sided_confidence_interval'] <= [.44]
