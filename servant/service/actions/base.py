class BaseAction(object):
    pass


class Action(BaseAction):

    def __call__(self, **kwargs):
        return self.run(**kwargs)
