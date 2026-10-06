[Index](../../../index.md) > [Event](../../Event.md) > [PointEvent](../PointEvent.md) > [ParameterEvent](#)
# ParameterEvent

**Display name:** Parameter event<br />
**DTMI:** dtmi:org:w3id:rec:ParameterEvent;1

---

## Child interfaces
* [DoubleValueParameter](DoubleValueParameter.md)
* [RelativeHumidityParameter](RelativeHumidityParameter.md)
* [TemperatureParameter](TemperatureParameter.md)
* [TimeSpanParameter](TimeSpanParameter.md)
* [VelocityParameter](VelocityParameter.md)
* [VolumeFlowRateParameter](VolumeFlowRateParameter.md)

---

## Relationships

|Name|Display name|Description|Multiplicity|Target|Properties|Writable|
|-|-|-|-|-|-|-|
|sourcePoint|**en**: source point|**en**: The brick:Point that has this parameter.|0-1|[Point](../../../Point/Point.md)||True|

---

## Properties

### Inherited Properties
* **[Event](../../Event.md):** customProperties, customTags, end, identifiers, name, start, timestamp

---

## Target Of
### General
* [Point](../../../Point/Point.md).isPointOf
* [Agent](../../../Agent/Agent.md).owns
* [Space](../../../Space/Space.md).isLocationOf
* [Equipment](../../../Asset/Equipment/Equipment.md).feeds
* [Equipment](../../../Asset/Equipment/Equipment.md).isFedBy
* [System](../../../Collection/System/System.md).includes
* [Architecture](../../../Space/Architecture/Architecture.md).isFedBy
* [Document](../../../Information/Document/Document.md).documentTopic
* [Document](../../../Information/Document/Document.md).url
* [Lease](../../Lease.md).leaseOf
* [PointOfInterest](../../../Information/PointOfInterest.md).objectOfInterest
* [Portfolio](../../../Collection/Portfolio.md).includes
* [ServiceObject](../../../Information/ServiceObject/ServiceObject.md).relatedTo
* [Meter](../../../Asset/Equipment/Meter/Meter.md).meters
