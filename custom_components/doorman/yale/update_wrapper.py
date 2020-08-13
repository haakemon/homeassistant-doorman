from datetime import datetime, timedelta
import logging
import copy

from custom_components.doorman.yale.expiration_wrapper import ExpirationWrapper
from custom_components.doorman.yale.exceptions import DataNotValidException, UpdateException

class UpdateWrapper:
    def __init__(
            self,
            data,
            tries=3,
            update_fn=None,
            access_fn=lambda x: x):  # update_cond_fn=lambda x: x is None

        self._logger = logging.getLogger(__name__)
        self._data = data
        self._tries = tries
        self._update_fn = update_fn
        self._sub_access_fn = access_fn
        # self._update_cond_fn = update_cond_fn

    @property
    def need_update(self):
        if self._data == None:
            return True

        if self._sub_access_fn(self._data) == None:
            return True
        else:
            return False

    """Update container with new data
    Returns: new data if sucsessfull, None if not"""
    def update(self):
        self._logger.debug(f"Updating data, {datetime.now()}")

        if self._update_fn == None:
            raise NotImplementedError("Update function is not implemented")

        try:
            self._data = self._update_fn()
        except Exception as error:
            raise UpdateException(f"Failed to update data due to {error}")

    def try_updates(self):
        exceptions = ""
        for i in range(self._tries):
            try:
                self.update()
                return
            except UpdateException as error:
                exceptions += str(error) + ", "
        raise UpdateException(f"Data update failed due to: {exceptions}")

    """Returns the data.
    If the data has expired, the data will be updated
    Raises exception if update fails"""
    @property
    def data(self):
        self._logger.debug("Accessing data")

        if self.need_update:
            self.try_updates()

        if self.need_update:
            self._logger.error("Container failed to update")
            raise UpdateException("Container failed to update")

        return self._sub_access_fn(self._data)
