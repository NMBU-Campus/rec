[Index](../../../../index.md) > [Point](../../../Point.md) > [Setpoint](../../Setpoint.md) > [Flow_Setpoint](../Flow_Setpoint.md) > [Water_Flow_Setpoint](#)
# Water_Flow_Setpoint

Sets the target flow rate of water


**Display name:** Water Flow Setpoint<br />
**DTMI:** dtmi:org:brickschema:schema:Brick:Water_Flow_Setpoint;1

---

## Child interfaces
* [Bypass_Water_Flow_Setpoint](Bypass-.md)
* [Chilled_Water_Flow_Setpoint](Chilled-/Chilled_Water_Flow_Setpoint.md)
* [Condenser_Water_Flow_Setpoint](Condenser-.md)
* [Entering_Water_Flow_Setpoint](Entering-.md)
* [Hot_Water_Flow_Setpoint](Hot-/Hot_Water_Flow_Setpoint.md)
* [Leaving_Water_Flow_Setpoint](Leaving-.md)

---

## Components

### Inherited Components
* **[Flow_Setpoint](../Flow_Setpoint.md):** lastKnownValue

---

## Relationships

### Inherited Relationships
* **[Point](../../../Point.md):** isPointOf

---

## Properties

### Inherited Properties
* **[Point](../../../Point.md):** aggregate, customProperties, customTags, hasQuantity, hasSubstance, identifiers, name

---

## Target Of
### General
* [Portfolio](../../../../Collection/Portfolio.md).includes
* [PointOfInterest](../../../../Information/PointOfInterest.md).objectOfInterest
* [Agent](../../../../Agent/Agent.md).owns
* [Space](../../../../Space/Space.md).isLocationOf
* [Lease](../../../../Event/Lease.md).leaseOf
* [Point](../../../Point.md).isPointOf
* [Document](../../../../Information/Document/Document.md).documentTopic
* [Document](../../../../Information/Document/Document.md).url
* [ServiceObject](../../../../Information/ServiceObject/ServiceObject.md).relatedTo
* [Architecture](../../../../Space/Architecture/Architecture.md).isFedBy
* [System](../../../../Collection/System/System.md).includes
* [Equipment](../../../../Asset/Equipment/Equipment.md).feeds
* [Equipment](../../../../Asset/Equipment/Equipment.md).isFedBy
* [Meter](../../../../Asset/Equipment/Meter/Meter.md).meters
### Inherited
* [ActuationEvent](../../../../Event/Point-/ActuationEvent.md).targetPoint
* [Architecture](../../../../Space/Architecture/Architecture.md).hasPoint
* [Asset](../../../../Asset/Asset.md).hasPoint
* [ExceptionEvent](../../../../Event/Point-/ExceptionEvent.md).sourcePoint
* [ObservationEvent](../../../../Event/Point-/ObservationEvent/ObservationEvent.md).sourcePoint
* [ParameterEvent](../../../../Event/Point-/ParameterEvent/ParameterEvent.md).sourcePoint
* [ServiceObject](../../../../Information/ServiceObject/ServiceObject.md).producedBy
* [SetpointEvent](../../../../Event/Point-/SetpointEvent/SetpointEvent.md).sourcePoint
* [StatusEvent](../../../../Event/Point-/StatusEvent/StatusEvent.md).sourcePoint
