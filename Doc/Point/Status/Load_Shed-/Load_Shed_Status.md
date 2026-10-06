[Index](../../../index.md) > [Point](../../Point.md) > [Status](../Status.md) > [Load_Shed_Status](#)
# Load_Shed_Status

Indicates if a load shedding policy is in effect


**Display name:** Load Shed Status<br />
**DTMI:** dtmi:org:brickschema:schema:Brick:Load_Shed_Status;1

---

## Child interfaces
* [Differential_Pressure_Load_Shed_Status](Differential_Pressure-/Differential_Pressure_Load_Shed_Status.md)
* [Entering_Hot_Water_Temperature_Load_Shed_Status](Entering_Hot_Water_Temperature-/Entering_Hot_Water_Temperature_Load_Shed_Status.md)
* [Leaving_Hot_Water_Temperature_Load_Shed_Status](Leaving_Hot_Water_Temperature-/Leaving_Hot_Water_Temperature_Load_Shed_Status.md)

---

## Components

|Name|Display name|Description|Schema|
|-|-|-|-|
|lastKnownValue|**en**: last known value||[BooleanValueStatus](../../../Event/Point-/StatusEvent/BooleanValueStatus.md)|

---

## Relationships

### Inherited Relationships
* **[Point](../../Point.md):** isPointOf

---

## Properties

### Inherited Properties
* **[Point](../../Point.md):** aggregate, customProperties, customTags, hasQuantity, hasSubstance, identifiers, name

---

## Target Of
### General
* [Portfolio](../../../Collection/Portfolio.md).includes
* [PointOfInterest](../../../Information/PointOfInterest.md).objectOfInterest
* [Agent](../../../Agent/Agent.md).owns
* [Space](../../../Space/Space.md).isLocationOf
* [Lease](../../../Event/Lease.md).leaseOf
* [Point](../../Point.md).isPointOf
* [Document](../../../Information/Document/Document.md).documentTopic
* [Document](../../../Information/Document/Document.md).url
* [ServiceObject](../../../Information/ServiceObject/ServiceObject.md).relatedTo
* [Architecture](../../../Space/Architecture/Architecture.md).isFedBy
* [System](../../../Collection/System/System.md).includes
* [Equipment](../../../Asset/Equipment/Equipment.md).feeds
* [Equipment](../../../Asset/Equipment/Equipment.md).isFedBy
* [Meter](../../../Asset/Equipment/Meter/Meter.md).meters
### Inherited
* [ActuationEvent](../../../Event/Point-/ActuationEvent.md).targetPoint
* [Architecture](../../../Space/Architecture/Architecture.md).hasPoint
* [Asset](../../../Asset/Asset.md).hasPoint
* [ExceptionEvent](../../../Event/Point-/ExceptionEvent.md).sourcePoint
* [ObservationEvent](../../../Event/Point-/ObservationEvent/ObservationEvent.md).sourcePoint
* [ParameterEvent](../../../Event/Point-/ParameterEvent/ParameterEvent.md).sourcePoint
* [ServiceObject](../../../Information/ServiceObject/ServiceObject.md).producedBy
* [SetpointEvent](../../../Event/Point-/SetpointEvent/SetpointEvent.md).sourcePoint
* [StatusEvent](../../../Event/Point-/StatusEvent/StatusEvent.md).sourcePoint
