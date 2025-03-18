import logging
import os
from datetime import date, timedelta

from dotenv import load_dotenv
from els_api import VisionMobileAPI


def main():
    logging.basicConfig(level=logging.INFO)
    my_landromat = restore_session(state_file="./.landry-state")

    # my_landromat.get_room_list(force_refresh=False)
    # print(my_landromat.get_room_list())

    # Get all slots for the next week
    book_days = my_landromat.get_booking_days(
        room_index=8,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=0),
    )
    for op in book_days:
        print(op)

    save_session(my_landromat)


# ---


def restore_session(state_file: str = "./.landry-state") -> VisionMobileAPI:
    logger = logging.getLogger(__name__)
    load_dotenv()
    # Caching: Check if a cache file exists, if so, restore it.
    # Otherwise, make a new one.
    if os.path.exists(state_file):
        logger.info("Found Cached instance! Restoring...")
        with open(state_file, "r") as file:
            session = VisionMobileAPI.fromJSON(i_json=file.read())
    else:
        logger.info("No cached instance found, making new one")
        session = VisionMobileAPI(
            domain=os.getenv("ELS_SITE"),
            username=os.getenv("ELS_USER"),
            password=os.getenv("ELS_PSWD"),
        )

    # Check if we're logged in or not, if we aren't: Log In!
    if session.check_login_status() is False:
        session.login()
    return session


def save_session(session: VisionMobileAPI, state_file: str = "./.landry-state"):
    # Save our session before exiting
    with open(state_file, "w") as file:
        file.write(session.toJSON())


if __name__ == "__main__":
    main()
