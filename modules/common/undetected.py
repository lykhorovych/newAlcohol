import undetected_chromedriver as uc


class RemoteService:
    SELENOID_HOST = '127.0.0.1'
    service_url = f'http://{SELENOID_HOST}:4444'  # If you use the driver container directly, remove `/wd/hub`.
    path = '/usr/bin/chromedriver'  # some existing fake path

    def start(self):
        pass

    def stop(self):
        pass


class UdChrome(uc.Chrome):

    def __init__(self, options):
        # Set your options here...
        options._session = self
        super().__init__(options=options, service=RemoteService(),
                         #browser_executable_path="/usr/bin/google-chrome",
                         # driver_executable_path="/usr/bin/chromedriver",
                         keep_alive=True)

        # Copy here what else you want from the uc.Chrome constructor...
        self._delay = 3
        self.options = options
