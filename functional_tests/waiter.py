from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time


# Modify WebDriverWait's 'until' function to return the last exception it intercepted
class JoWaiter(WebDriverWait):
    def until(self, method, message=''):
        """Calls the method provided with the driver as an argument until the \
        return value is not False."""
        exception = None  # Diff with super

        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(self._driver)
                if value:
                    return value
            except self._ignored_exceptions as exc:
                exception = exc  # Diff with super
            time.sleep(self._poll)
            if time.time() > end_time:
                break
        if exception:  # Diff with super
            raise exception  # Diff with super
        raise TimeoutException(message)
