
#!/bin/bash

cd SciGraph
cd SciGraph-core
mvn exec:java -Dexec.mainClass="io.scigraph.owlapi.loader.BatchOwlLoader" -Dexec.args="-c ../exampleGraph.yaml"
cd ../SciGraph-services
mvn exec:java -Dexec.mainClass="io.scigraph.services.MainApplication" -Dexec.args="server ../exampleServices.yaml"
