class Topic(object):

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key, value in dictionary.iteritems():
                setattr(self, key, value)
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
