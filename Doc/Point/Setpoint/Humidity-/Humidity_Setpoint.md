[Index](../../../index.md) > [Point](../../Point.md) > [Setpoint](../Setpoint.md) > [Humidity_Setpoint](#)
# Humidity_Setpoint

Sets humidity


**Display name:** Humidity Setpoint<br />
**DTMI:** dtmi:org:brickschema:schema:Brick:Humidity_Setpoint;1

---

## Child interfaces
* [Building_Air_Humidity_Setpoint](Building_Air-.md)
* [Bypass_Air_Humidity_Setpoint](Bypass_Air-.md)
* [Discharge_Air_Humidity_Setpoint](Discharge_Air-.md)
* [Exhaust_Air_Humidity_Setpoint](Exhaust_Air-.md)
* [Mixed_Air_Humidity_Setpoint](Mixed_Air-.md)
* [Occupied_Humidity_Setpoint](Occupied-.md)
* [Outside_Air_Humidity_Setpoint](Outside_Air-.md)
* [Return_Air_Humidity_Setpoint](Return_Air-.md)
* [Supply_Air_Humidity_Setpoint](Supply_Air-.md)
* [Unoccupied_Humidity_Setpoint](Unoccupied-.md)
* [Zone_Air_Humidity_Setpoint](Zone_Air-.md)

---

## Components

|Name|Display name|Description|Schema|
|-|-|-|-|
|lastKnownValue|**en**: last known value||[RelativeHumidityObservation](../../../Event/Point-/ObservationEvent/RelativeHumidityObservation.md)|

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
