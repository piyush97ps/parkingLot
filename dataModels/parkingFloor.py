from typing import List
import copy

from dataModels.parkingSlot import ParkingSpot
from dataModels.customDataType import ParkingSpotType


class ParkingFloor:
    def __init__(self, name: str, level: int, totalParkingSpot: int,
                 parkingSpots: List[ParkingSpot]):
        self.name: str = name
        self.level: int = level
        self.totalParkingSpot: int = totalParkingSpot
        self.parkingSpots: dict[str, ParkingSpot] = {spot.parkingID: spot for spot in parkingSpots}
        self.spotMapping: dict = self.__initSpotMap()

    def __initSpotMap(self) -> dict:
        spotConfig = {
            "available": set(),
            "assignedParking": set(),
            "preReservedParking": {},
            "total": 0
        }
        spotMappingCount = {
            ParkingSpotType.car: spotConfig,
            ParkingSpotType.bike: copy.deepcopy(spotConfig),
            ParkingSpotType.truck: copy.deepcopy(spotConfig)
        }
        for spot in self.parkingSpots.values():
            spotConfig = spotMappingCount[spot.parkingSpotType]
            if spot.isReserved:
                if spot.preAssignedMemberID in spotConfig["preReservedParking"]:
                    spotConfig["preReservedParking"][spot.preAssignedMemberID].add(spot)
                else:
                    spotConfig["preReservedParking"][spot.preAssignedMemberID] = set(spot, )
            else:
                spotConfig["available"].add(spot)

            spotConfig["total"] += 1

        return spotMappingCount

    def getSpotMapping(self):
        return self.spotMapping

    def getAvailableSpotForType(self, spotType: ParkingSpotType) -> dict:
        return self.spotMapping[spotType]

    def assignParkingSpot(self, vehicleType: ParkingSpotType, vehicleNumber: str,
                          reservedMemberID: str = "") -> ParkingSpot:
        """AssignParkingSpot.
        Args:
            vehicleType (ParkingSpotType): _description_
            vehicleNumber (str): _description_

        Returns:
            ParkingSpot | None: _description_
        """
        availableSpots = None
        isReserved = False
        if reservedMemberID:
            preReservedParkingSpots = self.spotMapping.get(vehicleType, {}).get("preReservedParking")
            if reservedMemberID in preReservedParkingSpots:
                reservedSpots = self.spotMapping.get(vehicleType, {}).get("preReservedParking").get(reservedMemberID)
                availableSpots = set(filter(
                    lambda spot: (not spot.isAlloted and spot.parkingSpotType == vehicleType),
                    reservedSpots))
                isReserved = True
            else:
                print(f"No Spot Available for Resereved Memeber: {reservedMemberID}, Vehicle Type: {vehicleType}")
                availableSpots = self.spotMapping.get(vehicleType, {}).get("available")
        else:
            availableSpots = self.spotMapping.get(vehicleType, {}).get("available")

        if not availableSpots:
            print(f"No Spot Available for Vehicle Type: {vehicleType}")
            return None

        notAvailable = self.spotMapping.get(vehicleType, {}).get("assignedParking")

        selectedSpot: ParkingSpot = availableSpots.pop()
        if not isReserved:
            notAvailable.add(selectedSpot)

        selectedSpot.vehicleNumber = vehicleNumber
        selectedSpot.isAlloted = True

        return selectedSpot

    def unassignParkingSpot(self, parkingSpotName: str, vehicleNumber) -> bool:
        """UnassignParkingSpot.

        Args:
            parkingSpot (ParkingSpot): _description_

        Returns:
            bool: _description_
        """
        if parkingSpotName not in self.parkingSpots:
            print("Invalid Parking Spot Name or Doesn't Exist")
            return False

        spot: ParkingSpot = self.parkingSpots[parkingSpotName]

        if vehicleNumber != spot.vehicleNumber:
            print(f"Not Valid parkingSpot, entered vehicleNumber is different then the vehicleNumber to unassign the vehicleName: {spot.vehicleNumber}")
            return False

        spot.isAlloted = False
        spot.vehicleNumber = ""

        if spot.isReserved:
            return True

        spotMap = self.spotMapping[spot.parkingSpotType]
        availableSpot: set = spotMap.get("available")
        assignedParking: set = spotMap.get("assignedParking")

        if spot in availableSpot:
            availableSpot.remove(spot)
        elif spot not in assignedParking:
            assignedParking.add(spot)

        return True

    def __str__(self) -> str:
        return f"Parking Lot is: {self.spotMapping}, Floor: {self.name}, level: {self.level}"
