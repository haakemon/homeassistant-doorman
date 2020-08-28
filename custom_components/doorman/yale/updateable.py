from datetime import datetime, timedelta

from custom_components.doorman.yale.expireable import Expireable
from custom_components.doorman.yale.exceptions import UpdateException

class Updateable(Expireable):
    def __init__(self, data, time_valid, tries=3):
        super().__init__(data, time_valid=time_valid)

        self._tries = tries

    @property
    def is_up_to_date(self):
        if self.is_active:
            return True
        else:
            return False

    """
    Update container with new data
    Returns: new data if sucsessfull, else returns None
    """
    def update(self):
        raise NotImplementedError("Update function is not implemented")

    def try_updates(self):
        exceptions = ""
        for i in range(self._tries):
            try:
                data = self.update()
                if data is not None:
                    self._data = data
                    self.set_timestamp(None)
                    return
            except UpdateException as error:
                exceptions += str(error) + ", "
        raise UpdateException(f"Data update failed due to: {exceptions}")

    """Returns the data.
    If the data has expired, the data will be updated
    Raises exception if update fails"""

    @property
    def data(self):
        if self.is_up_to_date is False:
            self.try_updates()

        return self._data
