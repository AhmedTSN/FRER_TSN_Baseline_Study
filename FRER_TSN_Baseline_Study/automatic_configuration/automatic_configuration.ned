
package src;

import inet.networks.base.TsnNetworkBase;
import inet.node.ethernet.EthernetLink;
import inet.node.tsn.TsnDevice;
import inet.node.tsn.TsnSwitch;
import inet.common.scenario.ScenarioManager;


module LocalTsnSwitch extends TsnSwitch
{
    @defaultStatistic("gateStateChanged:vector"; module="eth[0].macLayer.queue.gate[0]");
    @defaultStatistic("queueLength:vector"; module="eth[0].macLayer.queue");
    @defaultStatistic("packetDrop:vector"; module="eth[0].macLayer.queue");
}

network MergedFRERNetwork extends TsnNetworkBase
{
    submodules:
        scenarioManager: ScenarioManager {
            @display("p=100,142;is=s");
        }

        source: TsnDevice {
            @display("p=258,261");
        }

        s1: LocalTsnSwitch {
            @display("p=399,256");
        }

        s2a: LocalTsnSwitch {
            @display("p=607,90");
        }
        s3a: LocalTsnSwitch {
            @display("p=862,90");
        }

        s2b: LocalTsnSwitch {
            @display("p=607,249");
        }
        s3b: LocalTsnSwitch {
            @display("p=862,256");
        }

        s2c: LocalTsnSwitch {
            @display("p=607,375");
        }
        s3c: LocalTsnSwitch {
            @display("p=862,382");
        }

        destination: TsnDevice {
            @display("p=1085,261");
        }

    connections:

        source.ethg++ <--> EthernetLink <--> s1.ethg++;


        s1.ethg++ <--> EthernetLink <--> s2a.ethg++;
        s2a.ethg++ <--> EthernetLink <--> s3a.ethg++;
        s3a.ethg++ <--> EthernetLink <--> destination.ethg++;


        s1.ethg++ <--> EthernetLink <--> s2b.ethg++;
        s2b.ethg++ <--> EthernetLink <--> s3b.ethg++;
        s3b.ethg++ <--> EthernetLink <--> destination.ethg++;


        s1.ethg++ <--> EthernetLink <--> s2c.ethg++;
        s2c.ethg++ <--> EthernetLink <--> s3c.ethg++;
        s3c.ethg++ <--> EthernetLink <--> destination.ethg++;


        s2a.ethg++ <--> EthernetLink <--> s2b.ethg++;

        s3a.ethg++ <--> EthernetLink <--> s3b.ethg++;


}
