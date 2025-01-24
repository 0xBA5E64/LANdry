import os

from dotenv import load_dotenv
from els_api import VisionMobileAPI
from zeep import xsd


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

    # Save our session before exiting
    with open(CACHE_FILE, "w") as file:
        file.write(my_landromat.toJSON())


if __name__ == "__main__":
    main()
