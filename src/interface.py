import pylsl
import numpy
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis 

def init_lsl(stream_index):
    """init_lsl() - initialize an LSL stream containing EEG data
    @stream_type:  Should be "EEG" for EEG data.
    @stream_index: LSL supports multiple concurrent streams, this selects one.

    Returns: A stream inlet that can be read from.
    """
    streams = pylsl.resolve_stream('type', 'EEG')
    inlet   = pylsl.StreamInlet(streams[stream_index])
    return inlet

def read_lsl(inlet):
    """
    read_lsl() - reads a single sample from the LSL stream
    @inlet: The inlet from which to read the sample.

    Returns: A tuple with the timestamp integer, and sample (multiple variables in list form)
    """
    sample, time = inlet.pull_sample()
    return time, sample

def csv_to_nparray(cal_file):
    my_data = numpy.genfromtxt(cal_file, delimiter=',')
    end_index = my_data.shape[1]
    x = my_data[:, 1:end_index]
    y = my_data[:, 1]
    return x,y

def arr_to_feature(x):
   means_final = []
   i2=0
   j2=0
   for k in range(0,60):
	j=0
	while x[i2,0]==x[j2+j,0]:
		j=j+1	
	j2=j2+j+1	
        x2=x[i2:j2,0:6]
        means = numpy.mean(x2, axis = 1)
        first_row_mean = numpy.mean(x2[0,0:6])
        last_row_mean = numpy.mean(x2[j,0:6])
        means = numpy.mean(x2.compress([0,6], axis=-2), axis=-2)
        means = numpy.expand_dims(means, axis=-2)
        means_final.append([x[k],means])
	i2=j2

   print means
   return means_final
    
def butter_filter(x):
    pass

def get_classifier(x,y):
    clf = LinearDiscriminantAnalysis()
    clf.fit(x,y)
    return clf

def voting_matrix(x):
    return np.round(np.mean(x))

def classify_buf(lda_classifier, sample_buf):
    """
    classify_buf() - Takes the sample buffer, does EEG classification to determine game action.
    buf - The buffer containing relevant  EEG stream samples.

    Returns: ssvep_result controls game rotation and is 0/1/2 for left/none/right,
             mimg_result controls firing and is 0/1 for fire/don't fire
    """
    x = clf.predict(sample_buf)
    ssvep_result = voting_matrix(x)
    ssvep_result = 0
    return ssvep_result, 0

def gen_filter_vars(lowfreq, highfreq, fn, channels):
    b_low, a_low   = wyrm.processing.signal.butter(5, [highfreq / fn], btype='low')
    b_high, a_high = wyrm.processing.signal.butter(5, [lowfreq / fn], btype='high')
    zi_low         = wyrm.processing.lfilter_zi(b_low, a_low, channels)
    zi_high        = wyrm.processing.lfilter_zi(b_high, a_high, channels)
    return zi_low, zi_high
