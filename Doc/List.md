[Index](index.md) > [List](#)
# List

A list of twins


**Display name:** List<br />
**DTMI:** dtmi:org:w3id:rec:List;1

---

## Relationships

|Name|Display name|Description|Multiplicity|Target|Properties|Writable|
|-|-|-|-|-|-|-|
|includes|**en**: includes||0-Infinity|||True|

---

## Properties

|Name|Display name|Description|Schema|Writable|
|-|-|-|-|-|
|customProperties|**en**: Custom Properties||map (string->map (string->string))|True|
|customTags|**en**: Custom Tags||map (string->boolean)|True|
|identifiers|**en**: Identifiers||map (string->string)|True|
|name|**en**: name||string|True|

---

## Target Of
### General
* [Point](Point/Point.md).isPointOf
* [Agent](Agent/Agent.md).owns
* [List](#).includes
* [Space](Space/Space.md).isLocationOf
* [Equipment](Asset/Equipment/Equipment.md).feeds
* [Equipment](Asset/Equipment/Equipment.md).isFedBy
* [System](Collection/System/System.md).includes
* [Architecture](Space/Architecture/Architecture.md).isFedBy
* [Document](Information/Document/Document.md).documentTopic
* [Document](Information/Document/Document.md).url
* [Lease](Event/Lease.md).leaseOf
* [PointOfInterest](Information/PointOfInterest.md).objectOfInterest
* [Portfolio](Collection/Portfolio.md).includes
* [ServiceObject](Information/ServiceObject/ServiceObject.md).relatedTo
* [Meter](Asset/Equipment/Meter/Meter.md).meters
