import json
import os

from dotenv import load_dotenv
from zeep import Client, xsd


class VisionMobileAPI:
    def __init__(self, domain, username, password, loginguid=None, room_list=None):
        self.domain = domain
        self.username = username
        self.password = password
        self.client = Client(self.get_wsdl_url())
        self.api = self.client.service
        self.loginguid = loginguid
        self.room_list = room_list

    def toJSON(self):
        return json.dumps(
            {
                "domain": self.domain,
                "username": self.username,
                "password": self.password,
                "loginguid": self.loginguid,
                "room_list": self.room_list,
            }
        )

    def fromJSON(i_json: json):
        data = json.loads(i_json)
        return VisionMobileAPI(
            domain=data["domain"],
            username=data["username"],
            password=data["password"],
            loginguid=data["loginguid"],
            room_list=data["room_list"],
        )

    def login(self):
        # Check if already have a login GUID
        if self.loginguid is not None:
            # If so, check if if's still valid
            if self.check_login_status():
                print("Already have a valid login UUID")
                return

        print("Logging in...")
        self.loginguid = self.api.Login(
            username=xsd.AnyObject(xsd.String(), self.username),
            Password=xsd.AnyObject(xsd.String(), self.password),
            timeout=30,
        )
        return self.loginguid

    def check_login_status(self):
        req: str = self.api.GetUserData(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )
        if req is None:
            return False
        status: int = req[0]
        if status == -1:
            return False

        return True

    def get_room_list(self, force_refresh=False):
        if self.room_list is not None and force_refresh is False:
            return self.room_list
        choices = self.client.service.GetUserData(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )[1]["Units"]["MobileUnit"][0]["PreChoises"]["MobilePreChoise"]
        self.room_list = dict()
        for alternative in choices:
            self.room_list[alternative["Index"]] = alternative["Name"]
        return self.room_list

    def get_api_url(self):
        return f"https://{self.domain}/booking/Api/Mobile/VisionMobile.asmx"

    def get_wsdl_url(self):
        return f"{self.get_api_url()}?WSDL"


def main():
    load_dotenv()

    my_landromat: VisionMobileAPI | None = None

    # Caching: Check if a cache file exists, if so, restore it.
    # Otherwise, make a new one.
    CACHE_FILE = "./.landry-state"
    if os.path.exists(CACHE_FILE):
        print("Found Cached instance! Restoring...")
        with open(CACHE_FILE, "r") as file:
            my_landromat = VisionMobileAPI.fromJSON(i_json=file.read())
    else:
        print("No cached instance found, making new one")
        my_landromat = VisionMobileAPI(
            domain=os.getenv("ELS_SITE"),
            username=os.getenv("ELS_USER"),
            password=os.getenv("ELS_PSWD"),
        )

    # Check if we're logged in or not, if we aren't: Log In!
    if my_landromat.check_login_status() is False:
        my_landromat.login()

    # Do the stuff now:
    print(f"Are we logged in: {my_landromat.check_login_status()}")

    my_landromat.get_room_list(force_refresh=False)
    print(my_landromat.get_room_list())

    print(
        my_landromat.api.SetBookPrechoises(
            loginguid=xsd.AnyObject(xsd.String(), my_landromat.loginguid),
            prechoiseindex=xsd.AnyObject(xsd.String(), "8"),
        )
    )

    print(
        my_landromat.api.GetBookingCalendarDays(
            loginguid=xsd.AnyObject(xsd.String(), my_landromat.loginguid),
            startDate=xsd.AnyObject(xsd.String(), "2025-01-24"),
            endDate=xsd.AnyObject(xsd.String(), "2025-01-30"),
        )
    )

    # Save our session
    with open(CACHE_FILE, "w") as file:
        file.write(my_landromat.toJSON())


if __name__ == "__main__":
    main()
