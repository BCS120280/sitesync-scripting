# MQTT Vanilla Transmission - Version 1.0.0

This resource is meant for everyone- who doesn't want to or can't implement Sparkplug protocol for MQTT messaging. 
By using Gateway Tag Change Events and Cirrus Link MQTT modules scripting options, it is possible to provide similar functionality as Transmission does. Multiple advantages of this module is not implemented in this resource such as history transmission, store and forward, buffering (pacing period). Instead, it provides flexibility in topic namespace and payload format.
For each captured tag change, one MQTT message is fired for each configured server with these parameters:

+ Topic is by default full tag path, but can be transformed by setting prefix and cut string
+ Payload format can be one of these:

+ Qualified value formatted as JSON string
+ Qualified value, comma separated
+ Influx line protocol (possible to subscribe by Telegraf and store values in this timeseries database)
+ Just value alone


+ Additionally timestamp format and quality representation can be configured
+ QoS can be configed globally of per each tag
+ Retain can be configed globally of per each tag

**More info in UDT, in each tags documentation, and in scripts docstrings.**

## Installation

### Custom Instructions

+ Make sure that you have installed the needed Cirrus Link module
+ Make sure that you have configured and connected server (MQTT Broker)
+ (Optional) Create new tag provider named: MQTT Vanilla Transmission
+ Import UDTs and tags
+ Import Project resources
+ In Ignition Designer navigate to tag: "[Your Tag Provider]Exchange/MQTT Vanilla Transmission/Example Instance/Config/General/Server List" and change the value in list to the server name, you configured in step 2
+ Enable transmission by setting tag: "[Your Tag Provider]Exchange/MQTT Vanilla Transmission/Example Instance/Config/General/Server List" to True.
+ Prepare some MQTT client and subscribe to relevant topic (in case of example, it will be: ignition/exchange/mqttVanillaTransmission/#)
+ Trigger tag change event by writing to the tag: "[MQTT Vanilla Transmission]Exchange/MQTT Vanilla Transmission/Example Writable Float 1"
+ MQTT client should receive message in configured format


### Common Instructions

**Project (.zip/.proj)**  
Project backup and restoring from a project backup is referred to as Project Export and Import. Projects are exported individually, and only include project-specific elements visible in the Project Browser in the Ignition Designer. They do not include Gateway resources, like database connections, Tag Providers, Tags, and images. The exported file (.zip or .proj) is used to restore / import a project.

.zip = Ignition 8+
.proj = Ignition 7+

There are two primary ways to export and import a project:

Gateway Webpage - exports and imports the entire project.
Designer -  exports and imports only those resources that are selected.

When you restore / import a project from an exported file in the Gateway Webpage, it will be merged into your existing Gateway.

The import is located in:
Ignition Gateway > Configuration > System > Projects > Import Project Link

If there is a naming collision, you have the option of renaming the project or overwriting the project. Project exports can also be restored / imported in the Designer. Once the Designer is opened you can choose File > Import from the menu. This will even allow you to select which parts of the project import you want to include and will merge them into the currently open project.

**Tags (.json/.xml/.csv)**  
Ignition can export and import Tag configurations to and from the JSON (JavaScript Object Notation) file format. You can import XML (Extensible Markup Language) or CSV (Comma Separated Value) file formats as well, but Ignition will convert them to JSON format. Tag exports are imported in the Designer. Once the Designer is opened you can click on the import button in the Tag Browser panel.

### Requirements

**Modules**

+ MQTT Transmission
+ MQTT Engine

**Other**

+ Knowledge of MQTT protocol
+ Knowledge of Cirrus Link MQTT modules

## Release Notes
Initial release

## Authors and Acknowledgment
Built for the [Ignition Exchange](https://inductiveautomation.com/exchange) by Daniel Schmidt

## Support
View [MQTT Vanilla Transmission](https://inductiveautomation.com/exchange/2670) for more information, and other [versions](https://inductiveautomation.com/exchange/2670/versions)

## License
+ [MIT](https://choosealicense.com/licenses/mit/)
+ [Terms & Conditions](https://inductiveautomation.com/exchange/terms)
+ [Acceptable Use](https://inductiveautomation.com/exchange/use)
