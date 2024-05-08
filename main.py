from typing import List, Tuple
import copy
import json

from parking_lot.dataModels.parkingSlot import ParkingSpot
from parking_lot.dataModels.parkingFloor import ParkingFloor
from parking_lot.dataModels.parkingLot import ParkingLot
from parking_lot.dataModels.customDataType import ParkingSpotType


class ParkPlus:

    def __init__(self):
        """__init__."""
        self.data = json.loads("./data.json")
        self.parkingLot = self.__loadParkingLot()

    def __loadParkingSpot(self, spotData: dict, parkingFloorName) -> ParkingSpot:
        spotID = spotData["spotData_ID"]
        level = spotData["LEVEL"]
        reserved = spotData["RESERVED"]
        spotType = spotData["spotData_TYPE"]
        reservedMemberID = spotData["RESERVED_MEMBER_ID"]

        return ParkingSpot(parkingID=spotID, spotType=spotType,
                           parkingName=parkingFloorName, parkingLevel=level,
                           isReserved=reserved,
                           preAssignedMemberID=reservedMemberID)

    def __loadParkingFloor(self, parkingFloorName: str, parkingSpots: dict, level: int) -> ParkingFloor:
        """__loadParkingFloor.

        Args:
            parkingFloor (str): _description_
            parkingSpots (dict): _description_

        Returns:
            List[ParkingFloor]: _description_
        """
        spots: List[ParkingSpot] = []

        for spot in parkingSpots:
            parkingSpot = self.__loadParkingSpot(spot, parkingFloorName)
            spots.append(parkingSpot)

        return ParkingFloor(name=parkingFloorName, level=level,
                            totalParkingSpot=len(spots),
                            parkingSpots=spots)

    def __loadParkingLot(self) -> ParkingLot:
        uniqueId = self.data["PARKING_LOT_ID"]
        name = self.data["NAME"]
        capacity = self.data["CAPACITY"]
        levels = self.data["LEVELS"]
        address = self.data["LOCATION"]
        floors = self.data["FLOORS"]
        parkingSpots = self.data["PARKING_SPOTS"]
        parkingFloors = []

        for level, floor in enumerate(floors):
            floorPackingSpots = parkingSpots[floor]
            packingFloor = self.__loadParkingFloor(floor, floorPackingSpots,
                                                   level)
            parkingFloors.append(packingFloor)

        parkingLot = ParkingLot(
            uniqueId=uniqueId,
            name=name,
            totalLevel=levels,
            capacity=capacity,
            address=address,
            floors=floors,
            parkingFloors=parkingFloors
        )

        return parkingLot


if __name__ == "__main__":
    pp = ParkPlus()
