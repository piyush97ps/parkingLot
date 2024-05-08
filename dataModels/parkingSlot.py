from typing import List

from parking_lot.dataModels.customDataType import ParkingSpotType


class ParkingSpot:

    def __init__(self, parkingID: str, spotType: ParkingSpotType, parkingName: str,
                 parkingLevel: int, isReserved: bool = False,
                 preAssignedMemberID: str = "") -> None:
        """ParkingSpot.

        Args:
            spotTypes (list): Type are like car, bike, truck
            parkingNumber (str): Parking Number for parking spot
            parkingLevel (int): Parking Level for Parking spot
            isReserved (bool, optional): if the parking spot is reserved or not
            preAssignedMemberID (str, optional): is Parking Spot is reserved
                                                 and if yes then to whom.
        """
        self.parkingID = parkingID
        self.parkingSpotType: ParkingSpotType = spotType
        self.name: str = parkingName
        self.parkingLevel: int = parkingLevel
        self.isReserved: bool = isReserved
        self.preAssignedMemberID: str = preAssignedMemberID
        self.isAlloted: bool = False
        self.vehicleNumber: str = ""

    def isParkingSpotAlloted(self) -> bool:
        return self.isAlloted

    def allotParkingSpot(self) -> bool:
        self.isAlloted = True
        return self.isAlloted

    def unAlotParkingSpot(self) -> bool:
        self.isAlloted = False
        return self.isAlloted

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
