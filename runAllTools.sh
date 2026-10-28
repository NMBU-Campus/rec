#!/bin/bash

dotnet run --project ./Tools/DTDL2OAS --inputPath ./Source/DTDLv2/ --nuspecPath ./Metadata/RealEstateCore.Ontology.DTDLv2.nuspec --endpointsPath ./API/REST/Endpoints.csv --outputPath ./API/REST
# dotnet run --project ./Tools/DTDL2SHACL/   -i ./Source/DTDLv2   -o ./Source/SHACL/RealEstateCore.shacl.ttl   -n ./Source/SHACL/DtmiNamespaceMappings.csv
dotnet run --project ./Tools/DTDLValidator/  --recursive true --directory ./Source/DTDLv2/
dotnet run --project ./Tools/DTDLMerger/ ./Source/DTDLv2/ > ./RealEstateCore.DTDLv2.jsonld
dotnet run --project ./Tools/DTDL2MD/ -i ./RealEstateCore.DTDLv2.jsonld -o ./Doc/
