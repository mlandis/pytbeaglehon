#! /usr/bin/env python
# Copyright (c) 2010-2011 by Mark T. Holder
# (see bottom of file)

"unit tests datatyp internals"
import unittest
from pytbeaglehon import get_logger
_LOG = get_logger(__name__)

from pytbeaglehon.tests.util import *
# pylint: disable-msg=C0111,W0401,W0611,W0212
from pytbeaglehon.parameter import MutableFloatParameter
from pytbeaglehon.disc_state_cont_time_model import JukesCantorModel, DNAType, RevDiscStateContTimeModel, Kimura2ParameterModel, HKY85Model

from pytbeaglehon.like_calc_environ import minimal_LCE

from pytbeaglehon.tree_scorer import create_toggle_partial_tree_scorer

class ModelTest(unittest.TestCase):
    def test_simplest(self):
        m = HKY85Model(kappa=2.0, state_freq=[.25, 0.25, 0.25, 0.25])
        m.kappa.is_mutable = True
        m.kappa = 6.122449
        m.state_freq.is_mutable = True
        m.state_freq = (0.3, 0.25, 0.2, 0.25)
#         #NEXUS
#         begin data;    dimensions ntax = 4 nchar = 16;    format datatype = dna; matrix
#         t1 AAAACCCCGGGGTTTT
#         t2 AAAACCCCGGGGTTTT
#         t3 ACGTACGTACGTACGT
#         t4 ACGTACGTACGTACGT
#         ; end;
#         begin paup;    set storebr;    lset nst = 2 trat=3 basefreq = ( .3  .25  .2) userbr; end;
#         begin trees; tree o = [&U] (t1:0.0, t2:0.0,(t3:0.0,t4:0.0):0.01); end;
#         begin paup ;     lscore /sitelik ;   lsc / tr = 2.45 ;   quit; end;

        t1_2_data = tuple([0]*4 + [1]*4 + [2]*4 + [3]*4)
        t3_4_data = tuple([0, 1, 2, 3] * 4)
        data = (t1_2_data, t1_2_data, t3_4_data, t3_4_data)
        
        tree = TreeForTesting(newick='((1:0.0, 2:0.0):0.0,(3:0.0,4:0.0):0.01)')
        scorer = create_toggle_partial_tree_scorer(model_list=[m], data=data, tree=tree)
        lnL = scorer()
        self.assertAlmostEqual(lnL, -95.53419, places=4)
        scorer.accept()
        _LOG.debug("About to change kappa")
        m.kappa.value = 5.0
        lnL = scorer()
        self.assertAlmostEqual(lnL, -94.57203, places=4)

def additional_tests():
    "returns all tests in this file as suite"
    return unittest.TestLoader().loadTestsFromTestCase(ModelTest)

# pylint: disable-msg=C0103
def getTestSuite():
    """Alias to the additional_tests().  This is unittest-style.
    `additional_tests` is used by setuptools.
    """
    return additional_tests()

if __name__ == "__main__":
    unittest.main()
    print "SKIPPING TESTS!!!"



##############################################################################
##  pytbeaglehon phylogenetic likelihood caluclations using beaglelib.
##
##  Copyright 2010 Mark T. Holder
##  All rights reserved.
##
##  See "LICENSE.txt" for terms and conditions of usage.
##
##############################################################################
