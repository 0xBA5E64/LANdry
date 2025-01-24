import json

from zeep import Client, xsd
from zeep import xsd as ZeepClient


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
        return super(
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


class VisionApiClient:
    def __init__(self, input: VisionMobileAPI):
        self.client = ZeepClient(input.get_api_url())
        self.loginguid = input.loginguid

    def ApiVersion(self, apiMin: str, apiMax: str, deviceType: str, appVersion: str):
        return self.client.service.ApiVersion(
            apiMin=xsd.AnyObject(xsd.String(), apiMin),
            apiMax=xsd.AnyObject(xsd.String(), apiMax),
            deviceType=xsd.AnyObject(xsd.String(), deviceType),
            appVersion=xsd.AnyObject(xsd.String(), appVersion),
        )

    def ConnectToUnit(
        self,
        unitindex: int,
    ):
        return self.client.service.ConnectToUnit(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid),
            unitindex=xsd.AnyObject(xsd.String(), unitindex),
        )

    def DelBookUserBookings(
        self,
        bookindex: int,
    ):
        return self.client.service.DelBookUserBookings(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid),
            bookindex=xsd.AnyObject(xsd.String(), bookindex),
        )

    def GetAllTerminalMessageLite(self):
        return self.client.service.GetAllTerminalMessageLite(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetBookMachineGroupTypes(self):
        return self.client.service.GetBookMachineGroupTypes(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetBookMachineGroupsCountersLeft(self):
        return self.client.service.GetBookMachineGroupsCountersLeft(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetBookMachineGroupsFree(self):
        return self.client.service.GetBookMachineGroupsFree(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetBookPrechoices(self):
        return self.client.service.GetBookPrechoices(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetBookRandomMachineGroup(self):
        return self.client.service.GetBookRandomMachineGroup(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetBookUnits(self):
        return self.client.service.GetBookUnits(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetBookUserBookingCount(self):
        return self.client.service.GetBookUserBookingCount(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetBookUserBookings(self):
        return self.client.service.GetBookUserBookings(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetBookUserInfo(self):
        return self.client.service.GetBookUserInfo(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetBookingCalendarDays(self, startDate: str, endDate: str):
        return self.client.service.GetBookUserInfo(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid),
            startDate=xsd.AnyObject(xsd.String(), startDate),
            endDate=xsd.AnyObject(xsd.String(), endDate),
        )

    def GetCardgroupNameBookMachineGroupsFree(self):
        return self.client.service.GetCardgroupNameBookMachineGroupsFree(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetInformetricUrl(self):
        return self.client.service.GetCardgroupNameBookMachineGroupsFree(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetMachineGroups(self):
        return self.client.service.GetCardgroupNameBookMachineGroupsFree(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetNextBookMachineGroups(self):
        return self.client.service.GetNextBookMachineGroups(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetOneTerminalMessageLite(self, messageId: int):
        return self.client.service.GetOneTerminalMessageLite(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid),
            messageId=xsd.AnyObject(xsd.String(), messageId),
        )

    def GetShowBooked(self):
        return self.client.service.GetShowBooked(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetSystemDate(self):
        return self.client.service.GetSystemDate(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetSystemName(self):
        return self.client.service.GetSystemName()

    def GetTerminalMessageImage(self, messageId: int, isHeaderImage: bool):
        return self.client.service.GetTerminalMessageImage(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid),
            messageId=xsd.AnyObject(xsd.String(), messageId),
            isHeaderImage=xsd.AnyObject(xsd.String(), isHeaderImage),
        )

    def GetUserBalance(self):
        return self.client.service.GetUserBalance(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetUserData(self):
        return self.client.service.GetUserData(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetWebAccess(self):
        return self.client.service.GetWebAccess(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def GetWebAppAddress(self):
        return self.client.service.GetWebAppAddress(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def Login(self, systemname: str, username: str, password: str, timeout: int):
        return self.client.service.Login(
            systemname=xsd.AnyObject(xsd.String(), systemname),
            username=xsd.AnyObject(xsd.String(), username),
            password=xsd.AnyObject(xsd.String(), password),
            timeout=xsd.AnyObject(xsd.String(), timeout),
        )

    def Logout(self):
        return self.client.service.Logout(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid)
        )

    def SetBookMachineGroup(self, machinegroupindex: str):
        return self.client.service.Logout(
            machinegroupindex=xsd.AnyObject(xsd.String(), machinegroupindex)
        )

    def SetBookMachineGroupTypes(self, typeindex: str):
        return self.client.service.SetBookMachineGroupTypes(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid),
            typeindex=xsd.AnyObject(xsd.String(), typeindex),
        )

    def SetBookPass(self, SystemDate: str, passindex: str):
        return self.client.service.SetBookMachineGroupTypes(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid),
            SystemDate=xsd.AnyObject(xsd.String(), SystemDate),
            passindex=xsd.AnyObject(xsd.String(), passindex),
        )

    def SetBookPrechoises(self, prechoiseindex: str):
        return self.client.service.Logout(
            loginguid=xsd.AnyObject(xsd.String(), self.loginguid),
            prechoiseindex=xsd.AnyObject(xsd.String(), prechoiseindex),
        )
