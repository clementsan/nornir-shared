'''
Created on Mar 5, 2013

@author: u0490822
'''
import unittest

from nornir_shared.histogram import *


class Test(unittest.TestCase):

    def testHistogram8bppMinVals(self):

        minVal = 64
        maxVal = 191
        numBins = 128

        hist = Histogram.Init(minVal=minVal, maxVal=maxVal, numBins=None, binVals=None)
        self.assertEqual(hist.NumBins, numBins)
        self.assertEqual(hist.MaxValue, maxVal)
        self.assertEqual(hist.MinValue, minVal)
        self.assertEqual(len(hist.Bins), numBins)
        self.assertEqual(hist.BinWidth, 1)

        hist = Histogram.Init(minVal=minVal, maxVal=maxVal, numBins=numBins, binVals=None)
        self.assertEqual(hist.NumBins, numBins)
        self.assertEqual(hist.MaxValue, maxVal)
        self.assertEqual(hist.MinValue, minVal)
        self.assertEqual(len(hist.Bins), numBins)
        self.assertEqual(hist.BinWidth, 1)

        binVals = [10] * numBins
        hist = Histogram.Init(minVal=minVal, maxVal=maxVal, numBins=numBins, binVals=binVals)
        self.assertEqual(hist.NumBins, numBins)
        self.assertEqual(hist.MaxValue, maxVal)
        self.assertEqual(hist.MinValue, minVal)
        self.assertEqual(len(hist.Bins), numBins)
        self.assertEqual(hist.Bins, binVals)
        self.assertEqual(hist.BinWidth, 1)

        # Test cutoff values
        [MinCutoff, MaxCutoff] = hist.AutoLevel(0.0, 0.0)
        # Should be equal to min and max values
        self.assertEqual(MinCutoff, minVal)
        self.assertEqual(MaxCutoff, maxVal)

        median = hist.Median()
        self.assertEqual(median, (maxVal + minVal) / 2.0)

        mean = hist.Mean()
        self.assertEqual(mean, (maxVal + minVal) / 2.0)

        peak = hist.PeakValue()
        self.assertEqual(peak, (maxVal + minVal) / 2.0)

        minCutoff = 128
        maxCutoff = 160
        median = hist.Median(minVal=minCutoff, maxVal=maxCutoff)
        self.assertEqual(median, (maxCutoff + minCutoff) / 2.0)

        mean = hist.Mean(minVal=minCutoff, maxVal=maxCutoff)
        self.assertEqual(mean, (maxCutoff + minCutoff) / 2.0)

        peak = hist.PeakValue(minVal=minCutoff, maxVal=maxCutoff)
        self.assertEqual(peak, (maxCutoff + minCutoff) / 2.0)

    def testHistogram8bpp(self):
        '''Test histogram code with typical 8 bit per pixel numbers'''

        minVal = 0
        maxVal = 255
        numBins = 256

        hist = Histogram.Init(minVal=minVal, maxVal=maxVal, numBins=None, binVals=None)
        self.assertEqual(hist.NumBins, numBins)
        self.assertEqual(hist.MaxValue, maxVal)
        self.assertEqual(hist.MinValue, minVal)
        self.assertEqual(len(hist.Bins), numBins)
        self.assertEqual(hist.BinWidth, 1)

        hist = Histogram.Init(minVal=minVal, maxVal=maxVal, numBins=numBins, binVals=None)
        self.assertEqual(hist.NumBins, numBins)
        self.assertEqual(hist.MaxValue, maxVal)
        self.assertEqual(hist.MinValue, minVal)
        self.assertEqual(len(hist.Bins), numBins)
        self.assertEqual(hist.BinWidth, 1)

        binVals = range(1, numBins + 1)
        hist = Histogram.Init(minVal=minVal, maxVal=maxVal, numBins=numBins, binVals=binVals)
        self.assertEqual(hist.NumBins, numBins)
        self.assertEqual(hist.MaxValue, maxVal)
        self.assertEqual(hist.MinValue, minVal)
        self.assertEqual(len(hist.Bins), numBins)
        self.assertEqual(hist.Bins, binVals)
        self.assertEqual(hist.BinWidth, 1)

        # Test cutoff values
        [MinCutoff, MaxCutoff] = hist.AutoLevel(0.0, 0.0)
        # Should be equal to min and max values
        self.assertEqual(MinCutoff, minVal)
        self.assertEqual(MaxCutoff, maxVal)

        NumSamples = sum(binVals)
        # A value of 256 / NumSamples should produce

        [MinCutoff, MaxCutoff] = hist.AutoLevel(1.0 / NumSamples, 256.0 / NumSamples)
        self.assertEqual(MinCutoff, 1)
        self.assertEqual(MaxCutoff, 254)

        [MinCutoff, MaxCutoff] = hist.AutoLevel(None, None)
        self.assertEqual(MinCutoff, 0)
        self.assertEqual(MaxCutoff, 255)

        # This should be a pixel intensity of 100 and 200.
        MinCutoff = float(sum(range(1, 101)))
        HighCutoff = float(sum(range(202, 257)))
        [MinCutoff, MaxCutoff] = hist.AutoLevel(MinCutoff / NumSamples, HighCutoff / NumSamples)
        self.assertEqual(MinCutoff, 100)
        self.assertEqual(MaxCutoff, 200)

        # This should be a pixel intensity of 100.5 and 199.5.
        MinCutoff = float(sum(range(1, 101))) + 101.0 / 2.0
        HighCutoff = float(sum(range(202, 257))) + 201.0 / 2.0
        [MinCutoff, MaxCutoff] = hist.AutoLevel(MinCutoff / NumSamples, HighCutoff / NumSamples)
        self.assertEqual(MinCutoff, 100.5)
        self.assertEqual(MaxCutoff, 199.5)

        # Test a histogram that does not start at zero
        binVals = [10] * 10
        hist = Histogram.Init(minVal=100, maxVal=200, numBins=None, binVals=binVals)
        [MinCutoff, MaxCutoff] = hist.AutoLevel(0.0, 0.0)
        self.assertEqual(MinCutoff, 100)
        self.assertEqual(MaxCutoff, 200)

        [MinCutoff, MaxCutoff] = hist.AutoLevel(0.333, 0.333)
        MinCutoff = round(MinCutoff, 0)
        MaxCutoff = round(MaxCutoff, 0)
        self.assertEqual(MinCutoff, 134)
        self.assertEqual(MaxCutoff, 166)

        # Make a histogram with empty bins on either end.  Test that 0% and None parameters work
        binVals = [0] * 4
        binVals.extend([10] * 8)
        binVals.extend([0] * 4)

        # This should return the first non-zero bin
        hist = Histogram.Init(minVal=minVal, maxVal=maxVal, numBins=None, binVals=binVals)
        [MinCutoff, MaxCutoff] = hist.AutoLevel(0.0, 0.0)
        self.assertEqual(MinCutoff, 64)
        self.assertEqual(MaxCutoff, 191)

        mean = hist.Mean()
        self.assertEqual(mean, 128.0)

        gamma = hist.GammaAtValue(191)
        gamma = round(gamma, 1)
        self.assertEqual(gamma, 0.4)

        gamma = hist.GammaAtValue(63)
        gamma = round(gamma, 1)
        self.assertEqual(gamma, 2)

        binVals = [10] * 16
        hist = Histogram.Init(minVal=minVal, maxVal=maxVal, numBins=None, binVals=binVals)
        gamma = hist.GammaAtValue(128, 64, 255)
        gamma = round(gamma, 3)
        self.assertEqual(gamma, 1.577)

    def testHistogram16bpp(self):
        '''Test histogram code with typical 8 bit per pixel numbers'''

        minVal = 0
        maxVal = (1 << 16) - 1
        numBins = 1024
        ExpectedBinWidth = 64.0

        hist = Histogram.Init(minVal=minVal, maxVal=maxVal, numBins=numBins, binVals=None)
        self.assertEqual(hist.NumBins, numBins)
        self.assertEqual(hist.MaxValue, maxVal)
        self.assertEqual(hist.MinValue, minVal)
        self.assertEqual(len(hist.Bins), numBins)
        self.assertEqual(hist.BinWidth, ExpectedBinWidth)

        binVals = range(1, numBins + 1)
        hist = Histogram.Init(minVal=minVal, maxVal=maxVal, numBins=numBins, binVals=binVals)
        self.assertEqual(hist.NumBins, numBins)
        self.assertEqual(hist.MaxValue, maxVal)
        self.assertEqual(hist.MinValue, minVal)
        self.assertEqual(len(hist.Bins), numBins)
        self.assertEqual(hist.Bins, binVals)
        self.assertEqual(hist.BinWidth, ExpectedBinWidth)

        # Test cutoff values
        [MinCutoff, MaxCutoff] = hist.AutoLevel(0.0, 0.0)
        # Should be equal to min and max values
        self.assertEqual(MinCutoff, minVal)
        self.assertEqual(MaxCutoff, maxVal)

        NumSamples = float(sum(binVals))
        # A value of 256 / NumSamples should produce

        [MinCutoff, MaxCutoff] = hist.AutoLevel(1.0 / NumSamples, numBins / NumSamples)
        self.assertEqual(MinCutoff, 1.0 * ExpectedBinWidth)
        self.assertEqual(MaxCutoff, maxVal - ExpectedBinWidth)

        [MinCutoff, MaxCutoff] = hist.AutoLevel(None, None)
        self.assertEqual(MinCutoff, 0)
        self.assertEqual(MaxCutoff, maxVal)

        binCount = 10
        binVals = [binCount] * numBins
        NumSamples = float(sum(binVals))
        hist = Histogram.Init(minVal=minVal, maxVal=maxVal, numBins=numBins, binVals=binVals)

        # This should be a pixel intensity of 100 and 200.
        CutoffPercent = (binCount / 2.0) / NumSamples
        [MinCutoff, MaxCutoff] = hist.AutoLevel(CutoffPercent, CutoffPercent)
        self.assertEqual(MinCutoff, ExpectedBinWidth / 2.0)
        self.assertEqual(MaxCutoff, maxVal - (ExpectedBinWidth / 2.0))

        # This should be a pixel intensity of 100 and 200.
        CutoffPercent = (binCount * 3 / 2.0) / NumSamples
        [MinCutoff, MaxCutoff] = hist.AutoLevel(CutoffPercent, CutoffPercent)
        self.assertEqual(MinCutoff, 3 * ExpectedBinWidth / 2)
        self.assertEqual(MaxCutoff, maxVal - (3 * ExpectedBinWidth / 2.0))

        [MinCutoff, MaxCutoff] = hist.AutoLevel(0.25, 0.25)
        self.assertEqual(MinCutoff, (maxVal + 1) / 4.0)
        self.assertEqual(MaxCutoff, int(3 * maxVal / 4.0))

    def testHistogramAdd(self):
        '''Test histogram code with typical 8 bit per pixel numbers'''

        minVal = 0
        maxVal = (1 << 16) - 1
        numBins = 1024
        ExpectedBinWidth = 64.0

        hist = Histogram.Init(minVal=minVal, maxVal=maxVal, numBins=numBins, binVals=None)
        self.assertEqual(hist.NumBins, numBins)
        self.assertEqual(hist.MaxValue, maxVal)
        self.assertEqual(hist.MinValue, minVal)
        self.assertEqual(len(hist.Bins), numBins)
        self.assertEqual(hist.BinWidth, ExpectedBinWidth)

        inputVals = list(map(lambda x: (x * ExpectedBinWidth) - 1, range(1, numBins + 1)))

        for i in range(0, len(inputVals)):
            inputVals.extend([inputVals[i]] * i)

        binVals = list(range(1, numBins + 1))
        hist = Histogram.Init(minVal=minVal, maxVal=maxVal, numBins=numBins)
        hist.Add(inputVals)

        self.assertEqual(hist.NumBins, numBins)
        self.assertEqual(hist.MaxValue, maxVal)
        self.assertEqual(hist.MinValue, minVal)
        self.assertEqual(len(hist.Bins), numBins)

        for iBin in range(0, len(hist.Bins)):
            self.assertEqual(hist.Bins[iBin], binVals[iBin], "Bins do not match bins passed to constructor")
        # self.assertEqual(hist.Bins, binVals)
        self.assertEqual(hist.BinWidth, ExpectedBinWidth)

        # Test cutoff values
        [MinCutoff, MaxCutoff] = hist.AutoLevel(0.0, 0.0)
        # Should be equal to min and max values
        self.assertEqual(MinCutoff, minVal)
        self.assertEqual(MaxCutoff, maxVal)

        NumSamples = float(sum(binVals))
        # A value of 256 / NumSamples should produce

        [MinCutoff, MaxCutoff] = hist.AutoLevel(1.0 / NumSamples, numBins / NumSamples)
        self.assertEqual(MinCutoff, 1.0 * ExpectedBinWidth)
        self.assertEqual(MaxCutoff, maxVal - ExpectedBinWidth)

        [MinCutoff, MaxCutoff] = hist.AutoLevel(None, None)
        self.assertEqual(MinCutoff, 0)
        self.assertEqual(MaxCutoff, maxVal)


#     def testHugeAdd(self):
#         '''Wrote to compare performance, OK to disable'''
#         minVal = 0
#         maxVal = (1 << 16) - 1
#         numBins = 200
#         ExpectedBinWidth = 64.0
#
#         inputVals = map(lambda x : (x * ExpectedBinWidth) - 1, range(1, numBins + 1))
#
#         inputVals = inputVals * int(1.0 / (float(len(inputVals)) / 67108864.0))
#
#         print "Num values: " + str(len(inputVals))
#
#         hist = Histogram.Init(minVal=minVal, maxVal=maxVal, numBins=numBins)
#         hist.Add(inputVals)

if __name__ == "__main__":
    # import syssys.argv = ['', 'Test.testName']
    unittest.main()
