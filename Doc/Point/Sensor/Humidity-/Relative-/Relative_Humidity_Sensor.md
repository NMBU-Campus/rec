[Index](../../../../index.md) > [Point](../../../Point.md) > [Sensor](../../Sensor.md) > [Humidity_Sensor](../Humidity_Sensor.md) > [Relative_Humidity_Sensor](#)
# Relative_Humidity_Sensor

Measures the present state of absolute humidity relative to a maximum humidity given the same temperature


**Display name:** Relative Humidity Sensor<br />
**DTMI:** dtmi:org:brickschema:schema:Brick:Relative_Humidity_Sensor;1

---

## Child interfaces
* [Discharge_Air_Humidity_Sensor](Discharge_Air_Humidity_Sensor.md)
* [Exhaust_Air_Humidity_Sensor](Exhaust_Air_Humidity_Sensor.md)
* [Mixed_Air_Humidity_Sensor](Mixed_Air_Humidity_Sensor.md)
* [Outside_Air_Humidity_Sensor](Outside_Air_Humidity_Sensor.md)
* [Return_Air_Humidity_Sensor](Return_Air_Humidity_Sensor.md)
* [Supply_Air_Humidity_Sensor](Supply_Air_Humidity_Sensor.md)
* [Zone_Air_Humidity_Sensor](Zone_Air_Humidity_Sensor.md)

---

## Components

|Name|Display name|Description|Schema|
|-|-|-|-|
|lastKnownValue|**en**: last known value||[RelativeHumidityObservation](../../../../Event/Point-/ObservationEvent/RelativeHumidityObservation.md)|

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
