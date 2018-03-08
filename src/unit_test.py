import interface
import unittest
import matplotlib.pyplot as plt
import numpy

class TestBciData(unittest.TestCase):
    def test_calib_plot(self):
        """
        Plot the value of the O1 electrode over time, to see drift.
        """
        x,y = interface.csv_to_nparray("./cal_ssvep.csv")
        mag_vals  = x[:, 0].T
        plt.plot(mag_vals)
        plt.show()
        self.assertEqual(True, True)

     def test_lda(self):
         """
         Create the standard LDA classification graph for the calibration dataset.
         """
         x,y = interface.csv_to_nparray("./cal_ssvep.csv")

if __name__ == '__main__':
    unittest.main()
