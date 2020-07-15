from datetime import datetime, timedelta
import logging
logging.basicConfig(filename='tests/example.log', filemode='w', level=logging.DEBUG)


from custom_components.doorman.yale.expiration_wrapper import ExpirationWrapper

from custom_components.doorman.yale.exceptions import DataNotValidException, UpdateException


class UpdateWrapper:
    def __init__(
            self,
            data,
            tries=3,
            update_fn=None,
            access_fn=lambda x: x,
            update_cond_fn=lambda x: x is None):

        self._logger = logging.getLogger(__name__)
        self._data = data
        self._tries = tries
        self._update_fn = update_fn
        self._access_fn = access_fn
        self._update_cond_fn = update_cond_fn

    @property
    def need_update(self):
        if self._update_cond_fn == None:
            if self._data == None:
                return True
        else:
            try:
                return self._update_cond_fn(self._data)
            except Exception as error:
                self._logger.error(f"Could not establish if container needs update, {error}")

    """Update container with new data
    Returns: new data if sucsessfull, None if not"""
    def update(self):
        if self._update_fn == None:
            raise NotImplementedError("Update function is not implemented")

        self._logger.debug(f"Updating data, {datetime.now()}")
        try:
            self._data = self._update_fn()
        except Exception as error:
            raise UpdateException(f"Failed to update data due to {error}")

    """Returns the data.
    If the data has expired, the data will be updated
    Raises exception if update fails"""
    @property
    def data(self):
        self._logger.debug("Accessing data")

        for i in range(self._tries):
            if self.need_update():
                self.update()
            else:
                break

        try:
            if self.need_update() is False:
                return self._access_fn(self._data)
            else:
                raise UpdateException("Data condition not fullfilled")

        except Exception as error:
            self._logger.debug(f"Accessing data failed, error: {error}")

        self._logger.error("Container failed to update")
        raise UpdateException("Container failed to update")

