from application.login import ApplicationLogin
from application.identify_person import ApplicationIdentifyPerson
from application.rtc import ApplicationRtc

class Application:
    def __init__(
        self,
        login: ApplicationLogin,
        identify_person: ApplicationIdentifyPerson,
        rtc: ApplicationRtc
    ):
        self.login = login
        self.identify_person = identify_person
        self.rtc = rtc

    def startup(self):
        self.identify_person.startup()

    def shutdown(self):
        self.identify_person.shutdown()
