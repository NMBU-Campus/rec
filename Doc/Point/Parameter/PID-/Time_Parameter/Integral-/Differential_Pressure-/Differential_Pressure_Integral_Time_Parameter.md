[Index](../../../../../../index.md) > [Point](../../../../../Point.md) > [Parameter](../../../../Parameter.md) > [PID_Parameter](../../../PID_Parameter.md) > [Time_Parameter](../../Time_Parameter.md) > [Integral_Time_Parameter](../Integral_Time_Parameter.md) > [Differential_Pressure_Integral_Time_Parameter](#)
# Differential_Pressure_Integral_Time_Parameter

**Display name:** Differential Pressure Integral Time Parameter<br />
**DTMI:** dtmi:org:brickschema:schema:Brick:Differential_Pressure_Integral_Time_Parameter;1

---

## Child interfaces
* [Chilled_Water_Differential_Pressure_Integral_Time_Parameter](Chilled_Water-.md)
* [Entering_Water_Differential_Pressure_Integral_Time_Parameter](Entering_Water-.md)
* [Hot_Water_Differential_Pressure_Integral_Time_Parameter](Hot_Water-.md)
* [Leaving_Water_Differential_Pressure_Integral_Time_Parameter](Leaving_Water-.md)

---

## Components

### Inherited Components
* **[PID_Parameter](../../../PID_Parameter.md):** lastKnownValue

---

## Relationships

### Inherited Relationships
* **[Point](../../../../../Point.md):** isPointOf

---

## Properties

### Inherited Properties
* **[Point](../../../../../Point.md):** aggregate, customProperties, customTags, hasQuantity, hasSubstance, identifiers, name

---

## Target Of
### General
* [Portfolio](../../../../../../Collection/Portfolio.md).includes
* [PointOfInterest](../../../../../../Information/PointOfInterest.md).objectOfInterest
* [Agent](../../../../../../Agent/Agent.md).owns
* [Space](../../../../../../Space/Space.md).isLocationOf
* [Lease](../../../../../../Event/Lease.md).leaseOf
* [Point](../../../../../Point.md).isPointOf
* [Document](../../../../../../Information/Document/Document.md).documentTopic
* [Document](../../../../../../Information/Document/Document.md).url
* [ServiceObject](../../../../../../Information/ServiceObject/ServiceObject.md).relatedTo
* [Architecture](../../../../../../Space/Architecture/Architecture.md).isFedBy
* [System](../../../../../../Collection/System/System.md).includes
* [Equipment](../../../../../../Asset/Equipment/Equipment.md).feeds
* [Equipment](../../../../../../Asset/Equipment/Equipment.md).isFedBy
* [Meter](../../../../../../Asset/Equipment/Meter/Meter.md).meters
### Inherited
* [ActuationEvent](../../../../../../Event/Point-/ActuationEvent.md).targetPoint
* [Architecture](../../../../../../Space/Architecture/Architecture.md).hasPoint
* [Asset](../../../../../../Asset/Asset.md).hasPoint
* [ExceptionEvent](../../../../../../Event/Point-/ExceptionEvent.md).sourcePoint
* [ObservationEvent](../../../../../../Event/Point-/ObservationEvent/ObservationEvent.md).sourcePoint
* [ParameterEvent](../../../../../../Event/Point-/ParameterEvent/ParameterEvent.md).sourcePoint
* [ServiceObject](../../../../../../Information/ServiceObject/ServiceObject.md).producedBy
* [SetpointEvent](../../../../../../Event/Point-/SetpointEvent/SetpointEvent.md).sourcePoint
* [StatusEvent](../../../../../../Event/Point-/StatusEvent/StatusEvent.md).sourcePoint
