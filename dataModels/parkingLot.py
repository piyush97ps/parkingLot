from typing import List, Tuple
import copy

from dataModels.parkingSlot import ParkingSpot
from dataModels.parkingFloor import ParkingFloor
from dataModels.customDataType import ParkingSpotType


class ParkingLot:

    def __init__(self, uniqueId: str, name: str, totalLevel: int,
                 capacity: int, address: str, floors: List[str],
                 parkingFloors: List[ParkingFloor]):
        self.uniqueId: str = uniqueId
        self.name: str = name
        self.floors: List[str] = floors
        self.totalLevel: int = totalLevel
        self.capacity: int = capacity
        self.address: str = address
        self.parkingFloors: List[ParkingFloor] = parkingFloors

    def getParkingSpotAndFloor(self, vehicleNumber: str, vehicleType: ParkingSpotType
                               ) -> Tuple[ParkingSpot, ParkingFloor]:
        """AssignParkingSpot.

        Args:
            vehicleNumber (str): _description_
            vehicleType (ParkingSpotType): _description_

        Returns:
            ParkingSpot | None: _description_
        """
        for floor in self.parkingFloors:
            spot: ParkingSpot = floor.assignParkingSpot(
                vehicleNumber=vehicleNumber, vehicleType=vehicleType)
            if spot:
                print(f"Parking Floor: {floor.name}, Parking Spot: {spot.name}")
                break
        if not spot:
            print(f"Parking Not Available for vehicleNumber: {vehicleNumber}, vehicleType: {vehicleType}")

        return spot, floor

    def unassignedParkingSpot(self, parklingSpotId, vehicleNumber) -> bool:
        """unassignedParkingSpot.

        Args:
            vehicleNumber (str): _description_
            vehicleType (ParkingSpotType): _description_

        Returns:
            bool: _description_
        """
        spot = False
        for floor in self.parkingFloors:
            spot = floor.unassignParkingSpot(parkingSpotName=parklingSpotId,
                                             vehicleNumber=vehicleNumber)
            if spot:
                print("Parking Spot Unassigned Successfully!!")
                break
        if not spot:
            print("Parking Spot is already Unassigned Successfully!!")

        return spot
