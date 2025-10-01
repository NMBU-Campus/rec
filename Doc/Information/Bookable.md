[Index](../index.md) > [Information](Information.md) > [Bookable](#)
# Bookable

Description to be added when a Room can be booked. Bookable will include information about the booking source, and keys to find the correct resource within that system.


**Display name:** Bookable<br />
**DTMI:** dtmi:org:w3id:rec:Bookable;1

---

## Relationships

|Name|Display name|Description|Multiplicity|Target|Properties|Writable|
|-|-|-|-|-|-|-|
|isBookableOf|**en**: Bookable||0-Infinity|[Room](../Space/Architecture/Room/Room.md)||True|

---

## Properties

### Inherited Properties
* **[Information](Information.md):** customProperties, customTags, identifiers, name

---

## Target Of
### General
* [Point](../Point/Point.md).isPointOf
* [Agent](../Agent/Agent.md).owns
* [Space](../Space/Space.md).isLocationOf
* [Equipment](../Asset/Equipment/Equipment.md).feeds
* [Equipment](../Asset/Equipment/Equipment.md).isFedBy
* [System](../Collection/System/System.md).includes
* [Architecture](../Space/Architecture/Architecture.md).isFedBy
* [Document](Document/Document.md).documentTopic
* [Document](Document/Document.md).url
* [Lease](../Event/Lease.md).leaseOf
* [PointOfInterest](PointOfInterest.md).objectOfInterest
* [Portfolio](../Collection/Portfolio.md).includes
* [ServiceObject](ServiceObject/ServiceObject.md).relatedTo
* [Meter](../Asset/Equipment/Meter/Meter.md).meters
