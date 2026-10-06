[Index](../../../index.md) > [Point](../../Point.md) > [Parameter](../Parameter.md) > [Limit](#)
# Limit

A parameter that places an upper or lower bound on the range of permitted values of another point


**Display name:** Limit<br />
**DTMI:** dtmi:org:brickschema:schema:Brick:Limit;1

---

## Child interfaces
* [Air_Flow_Setpoint_Limit](Air_Flow_Setpoint-/Air_Flow_Setpoint_Limit.md)
* [Close_Limit](Close-.md)
* [Current_Limit](Current-.md)
* [Differential_Pressure_Setpoint_Limit](Differential_Pressure_Setpoint-/Differential_Pressure_Setpoint_Limit.md)
* [Fresh_Air_Setpoint_Limit](Fresh_Air_Setpoint-/Fresh_Air_Setpoint_Limit.md)
* [Max_Limit](Max-.md)
* [Min_Limit](Min-.md)
* [Position_Limit](Position-/Position_Limit.md)
* [Speed_Setpoint_Limit](Speed_Setpoint-/Speed_Setpoint_Limit.md)
* [Static_Pressure_Setpoint_Limit](Static_Pressure_Setpoint-/Static_Pressure_Setpoint_Limit.md)
* [Ventilation_Air_Flow_Ratio_Limit](Ventilation_Air_Flow_Ratio-.md)

---

## Components

|Name|Display name|Description|Schema|
|-|-|-|-|
|lastKnownValue|**en**: last known value||[DoubleValueParameter](../../../Event/Point-/ParameterEvent/DoubleValueParameter.md)|

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
