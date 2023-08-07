#!/bin/bash

echo "Starting the PlantUML picoserver."
java -jar /tmp/plantuml.jar -picoweb &
PLANTUML_PID=$!

echo -n "Waiting for picoserver to be up: "
retcode=1
while [ $retcode -ne 0 ]; do
    sleep 1
    wget http://127.0.0.1:8080 -T1 -O - 1>/dev/null 2>/dev/null; retcode=$?
done
echo "Picoserver is UP!"

hugo $@
exit_code=$?

echo "Cleaning up!"
kill $PLANTUML_PID

exit $exit_code