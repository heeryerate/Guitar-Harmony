class Interval():
    """
    The interval class.

    The notes are to be parsed in th following way:
    * the quality, (m, M, p, A, d)
    * the number. (1 to 8) [Compound intervals will be supported]

    For example, 'd8', 'P1', 'A5' are valid intervals. 'P3', '5' are not.
    """
    def __init__(self, interval = 'P1'):
        try:
            self.semitones = {'P1': 0, 'A1':1, 'd2':0, 'm2':1, 'M2':2, 'A2':3,
                              'd3':3, 'm3':3, 'M3':4, 'A3':5, 'd4':4, 'P4':5,
                              'A4':6, 'd5':6, 'P5':7, 'A5':8, 'd6':7, 'm6':8,
                              'M6':9, 'A6':10,'d7':9, 'm7':10, 'M7':11, 'A7':12,
                              'd8':11, 'P8':12}
            self.semitone = self.semitones[interval]
        except:
            raise Exception('Could not parse the interval.')
        self.number = int(interval[1])
    def all_intervals(self):
        return self.semitones.keys()

