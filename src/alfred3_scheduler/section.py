from alfred3.section import Section
from alfred3.admin import AdminAccess
from alfred3._helper import inherit_kwargs

from .page import ManageDateSlotsPage
from .page import AddDateSlotsPage
from .page import RegistrationPage
from .page import RegistrationInitiatedPage
from .page import ConfirmationPage
from .page import CancelPage


@inherit_kwargs
class SchedulerAdmin(Section):
    """
    Provides scheduler administration pages for alfred3's admin mode.

    Args:
        scheduler (alfred3_scheduler.Scheduler): A scheduler instance.
            Can be defined as a class attribute instead of an init 
            argument.
        {kwargs}
    """
    scheduler = None
    access_level = AdminAccess.LEVEL2

    def __init__(self, scheduler=None, **kwargs):
        if scheduler is not None:
            self.scheduler = scheduler
        if self.scheduler is None:
            raise ValueError("Must supply scheduler.")

        name = self.scheduler.admin
        super().__init__(name=name, **kwargs)

    def on_exp_access(self):
        # docstring inherited
        self += ManageDateSlotsPage(self.scheduler)
        self += AddDateSlotsPage(self.scheduler)


@inherit_kwargs
class SchedulerInterface(Section):
    """
    Provides a participant-facing scheduler interface.

    The interface displays an overview of available slots for participants
    and allows them to register.

    Args:
        scheduler (alfred3_scheduler.Scheduler): A scheduler instance.
            Can be defined as a class attribute instead of an init 
            argument.
        email (str): Participant email address. The SchedulerInterface
            expects that you have asked the participant for their
            email address on a previous page. You can provide it on init,
            as a class attribute, or access in :meth:`.on_exp_access`.
            Often, the latter option will be the easiest to use.
        {kwargs}

    """
    scheduler = None
    email: str = None

    def __init__(self, scheduler=None, email: str = None, **kwargs):
        if scheduler is not None:
            self.scheduler = scheduler
        if self.scheduler is None:
            raise ValueError("Must supply scheduler.")

        if email is not None:
            self.email = email

        name = self.scheduler.interface
        super().__init__(name=name, **kwargs)

    def showif(self) -> bool:
        return self.exp.urlargs.get("scheduler") == self.scheduler.name

    def on_exp_access(self):
        if self.should_be_shown:
            if self.email is None:
                raise ValueError("Must supply email.")
            self += RegistrationPage(self.scheduler)
            self += RegistrationInitiatedPage(self.scheduler)
            self += ConfirmationPage(self.scheduler)
            self += CancelPage(self.scheduler)
