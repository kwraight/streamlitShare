
class Question:
    def __init__(self, **kwargs):
        self.code = "NYS"
        self.text = "NYS"
        self.options = []
        self.index = float("NaN")
        self.points = float("NaN")
        self.__dict__.update(kwargs)

        allowed_keys = {'code', 'text', 'option', 'index', 'points'}
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
