from brian import *
from .hrtf import *
from ..prefs import get_samplerate

__all__ = ['ITDDatabase']

speed_of_sound_in_air = 343.2*metre/second

class ITDDatabase(HRTFDatabase):
    '''
    Database for creating HRTFSet with artificial interaural time-differences
    
    Initialisation keywords:
    
    ``n``, ``azim_max``, ``diameter``
        Specify the ITDs for two ears separated by distance ``diameter`` with
        no head. ITDs corresponding to ``n`` angles equally spaced between
        ``-azim_max`` and ``azim_max`` are used. The default diameter is that
        which gives the maximum ITD as 650 microseconds. The ITDs are computed
        with the formula ``diameter*sin(azim)/speed_of_sound_in_air``.
    ``itd``
        Instead of specifying the keywords above, just give the ITDs directly.
        
    To get the HRTFSet, the simplest thing to do is just::
    
        hrtfset = ITDDatabase(13).load_subject()
        
    The generated ITDs can be returned using the ``itd`` attribute of the
    :class:`ITDDatabase` object.
    '''
    def __init__(self, n=None, azim_max=pi/2,
                 diameter=speed_of_sound_in_air*650*usecond,
                 itd=None, samplerate=None):
        if itd is None:
            azim = linspace(-azim_max, azim_max, n)
            itd = diameter*sin(azim)/speed_of_sound_in_air
            coords = make_coordinates(azim=azim, itd=itd)
        else:
            coords = make_coordinates(itd=itd)
        self.itd = itd
        samplerate = self.samplerate = get_samplerate(samplerate)
        dmax = amax(abs(itd))/2
        dl = array(rint((itd/2+dmax)*samplerate), dtype=int)
        dr = array(rint((-itd/2+dmax)*samplerate), dtype=int)
        idxmax = max(amax(dl), amax(dr))
        data = zeros((2, len(itd), idxmax+1))
        data[0, arange(len(itd)), dl] = 1
        data[1, arange(len(itd)), dr] = 1
        self.hrtfset = HRTFSet(data, samplerate, coords)
        self.hrtfset.name = 'ITDDatabaseSubject'
        self.subjects = ['0']

    def load_subject(self, subject='0'):
        return self.hrtfset