[Index](../../../index.md) > [Event](../../Event.md) > [PointEvent](../PointEvent.md) > [ObservationEvent](ObservationEvent.md) > [DateTimeObservation](#)
# DateTimeObservation

**Display name:** DateTime observation<br />
**DTMI:** dtmi:org:w3id:rec:DateTimeObservation;1

---

## Relationships

### Inherited Relationships
* **[ObservationEvent](ObservationEvent.md):** sourcePoint

---

## Properties

|Name|Display name|Description|Schema|Writable|
|-|-|-|-|-|
|observedDateTime|**en**: Observed date time|**en**: Observed date time for observation or setpoint.|dateTime|True|
### Inherited Properties
* **[Event](../../Event.md):** customProperties, customTags, end, identifiers, name, start, timestamp

---

## Target Of
### General
* [Point](../../../Point/Point.md).isPointOf
* [Root](../../../Root/Root.md).containsTwin
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
