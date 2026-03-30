[Index](../index.md) > [Root](#)
# Root

A generic base interface that can target any twin type, or be extended by other interfaces to constrain which twin types may be targeted by the relationship


**Display name:** Root<br />
**DTMI:** dtmi:org:nmbu:Root;1

---

## Relationships

|Name|Display name|Description|Multiplicity|Target|Properties|Writable|
|-|-|-|-|-|-|-|
|containsTwin|**en**: containsTwin||0-Infinity|||True|

---

## Target Of
### General
* [Point](../Point/Point.md).isPointOf
* [Root](#).containsTwin
* [Agent](../Agent/Agent.md).owns
* [Space](../Space/Space.md).isLocationOf
* [Equipment](../Asset/Equipment/Equipment.md).feeds
* [Equipment](../Asset/Equipment/Equipment.md).isFedBy
* [System](../Collection/System/System.md).includes
* [Architecture](../Space/Architecture/Architecture.md).isFedBy
* [Document](../Information/Document/Document.md).documentTopic
* [Document](../Information/Document/Document.md).url
* [Lease](../Event/Lease.md).leaseOf
* [PointOfInterest](../Information/PointOfInterest.md).objectOfInterest
* [Portfolio](../Collection/Portfolio.md).includes
* [ServiceObject](../Information/ServiceObject/ServiceObject.md).relatedTo
* [Meter](../Asset/Equipment/Meter/Meter.md).meters
