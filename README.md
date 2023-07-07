# Brewery_DT

Project contains the development of the tool for the Brewery DT and the research files and outputs from the MSc project  of Ander Lee. 

[[_TOC_]]

# Devices & System Setup
## Inkbird IBS-TH1
The MAC address of the sensor and the URL of the web server can be configured in:

`Implementation/RaspberryPi/monitoring/config.ini` 

by changing the corresponding fields:
```
[MAC]
Inkbird = <MAC in all caps, e.g., FF:FF:FF:FF:FF>
Tilt = <MAC in all caps, e.g., FF:FF:FF:FF:FF>

[URL]
Inkbird = <URL>
Tilt = <URL>
```
After that, go to directory `Implementation/RaspberryPi`

Execute the command:

```
python -m monitoring -t <seconds>
```

The `-t` flag sets the cycle time (in seconds) for each scan. The flag is optional. If not used, the default time is 60 seconds.

The program will scan for the BLE advertisement data and forward them to the pre-configured URL.

### Alternative method for Inkbird
Inkbird supports sending the monitoring data in two ways, through BLE packet advertisement or Generic ATTribute Profile (GATT) transaction. The latter is not recommended when BLE scanning is still on for other devices, because there is a [reported issue](https://forums.raspberrypi.com/viewtopic.php?f=28&t=268779&p=1631047#p1631047) regarding BLE scanning and peripheral connection taking place simultaneously.

To obtain the data through GATT, one can use handle `0x24` (depending on the actual model, could be `0x28` or `0x2D` instead, need to give a few trials) with the command below:

```shell
gatttool -b <MAC> --char-read --handle=<handle> 
```

The return value will be a seven bytes data:

- The first 2 bytes, little endian ordered, represent `uint16` temperature value / 100 
- The next 2 bytes, little endian ordered, represent `uint16` humidity value / 100 
- The 5th byte represents the probe type, `0` for internal, `1` for external 

## Tilt
The configuration of Tilt device is the same as Inkbird. First edit the `config.ini` file and then run the command:

```shell
python -m monitoring -t <seconds>
```

## Inkbird ITC-308-WIFI

## Kafka broker
Java 8+ must be installed, and `JAVA_HOME` should be set in the system environment variables in Windows. See this [tutorial](https://confluence.atlassian.com/doc/setting-the-java_home-variable-in-windows-8895.html) if not clear.

Download Kafka from the [official site](https://kafka.apache.org/downloads) and extract it.

Move the extracted folder to `C:\`, the local Kafka main directory should have the file path similar to `C:\kafka_x.xx` 

Copy the files `server.properties` and `zookeeper.properties` in `Implementation/Windows/commons/kafka/config` of this repository. 
Paste them in the `C:\kafka_x.xx\config` directory to overwrite the default files. 

After that, go back to the local Kafka main directory, run:

```
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
```

Open another terminal window, then run:

```
bin\windows\kafka-server-start.bat config\server.properties
```

The Kafka server should be now running. Next, create topics with the command:
```
bin\windows\kafka-topics.bat --create --topic <topic name> --bootstrap-server localhost:9092

```
List all the created topics with the command:
```
bin\windows\kafka-topics.bat --bootstrap-server=localhost:9092 --list
```

One can proceed to invoke the producers and consumers that perform write/read to the topics.

## Python Requirements
Install Python 3.8+ and `pip` in Windows. After that, go to `Implementation/Windows/commons` and run:

```bash
pip install -r requirements.txt
```

The required Python libraries for the frameworks will be installed.


# How to Use the Frameworks
## TwinOps
## ThingsBoard
## Ptolemy II


# Troubleshoot
- When running into Bluetooth errors on RaspberryPi, try the command: 
```shell
sudo hciconfig hci0 reset
```
- When statrting the Kafka server, if the following error message shows up:
> The system cannot find the path specified

It's probably because `JAVA_HOME` is invalid. One can check `JAVA_HOME` in the terminal by:
```
echo %JAVA_HOME%
```
