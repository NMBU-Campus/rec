[Index](../../../index.md) > [Point](../../Point.md) > [Command](../Command.md) > [Enable_Command](#)
# Enable_Command

Commands that enable functionality


**Display name:** Enable Command<br />
**DTMI:** dtmi:org:brickschema:schema:Brick:Enable_Command;1

---

## Child interfaces
* [Cooling_Enable_Command](Cooling-.md)
* [Enable_Differential_Enthalpy_Command](Enable_Differential_Enthalpy_Command.md)
* [Enable_Differential_Temperature_Command](Enable_Differential_Temperature_Command.md)
* [Enable_Fixed_Enthalpy_Command](Enable_Fixed_Enthalpy_Command.md)
* [Enable_Fixed_Temperature_Command](Enable_Fixed_Temperature_Command.md)
* [Heating_Enable_Command](Heating-.md)
* [Run_Enable_Command](Run-.md)
* [Stage_Enable_Command](Stage-.md)
* [System_Enable_Command](System-/System_Enable_Command.md)
* [VFD_Enable_Command](VFD-.md)

---

## Components

|Name|Display name|Description|Schema|
|-|-|-|-|
|lastKnownValue|**en**: last known value||[ActuationEvent](../../../Event/Point-/ActuationEvent.md)|

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
