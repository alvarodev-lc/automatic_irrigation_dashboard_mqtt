#define MQTTCLIENT_QOS2 1

#include <memory.h>
#include <memory>
#include <thread>
#include "MQTTClient.h"
#ifdef HW
//#include <beaglebone_pruio.h>
//#include <beaglebone_pruio_pins.h>
#endif
#define DEFAULT_STACK_SIZE -1
#define PUBLISH_TIME 2
#include <fstream>
#include "linux/linux.cpp"
#include <unistd.h>
int arrivedcount = 0;

bool nodeActivated = true;
int water = 0;
int Qos = 0;
char topicTemp[30]="";
char topicHum[30]="";
char topicStatus[30]="";
char topicWater[30]="";
char topicQoS[30]="";
class Node {

public:
    int id;
    float temp;
    float humidity;
    bool nodeEnabled;
    Node(int idNodo, std::shared_ptr <IPStack> ipstack,std::shared_ptr<MQTT::Client<IPStack, Countdown>> client):id(idNodo), m_ipstack(ipstack), m_client(client),nodeEnabled(true){};
    float GetTemperature();
    float GetHumidity();
    void UpdateSensors();
    void InitTopics();
    void PublishTopics(const char* topic,float value);
    void Connect();
    void Disconnect();
#ifdef HW
    void HardwareInit();
#endif
private:
    std::shared_ptr <IPStack> m_ipstack;
    std::shared_ptr<MQTT::Client<IPStack, Countdown>> m_client;
};
void CallbackStatus(MQTT::MessageData& md)
{
    MQTT::Message &message = md.message;

#ifdef DEBUG2
    printf("Message %d arrived: qos %d, retained %d, dup %d, packetid %d\n", 
		++arrivedcount, message.qos, message.retained, message.dup, message.id);
    printf("Topic Status updated:  %.*s\n", (int)message.payloadlen, (char*)message.payload);
#endif    
    int val = atoi((char*)message.payload);
    ( val == 0) ?nodeActivated=false:nodeActivated=true;
}


void CallbackWater(MQTT::MessageData& md)
{
    MQTT::Message &message = md.message;

#ifdef DEBUG2
    printf("Message %d arrived: qos %d, retained %d, dup %d, packetid %d\n", 
		++arrivedcount, message.qos, message.retained, message.dup, message.id);
    printf("Topic water updated:  %.*s\n", (int)message.payloadlen, (char*)message.payload);
#endif    
    int val = atoi((char*)message.payload);
    ( val == 0) ?water=false:water=true;
}

void CallbackQoS(MQTT::MessageData& md)
{
    MQTT::Message &message = md.message;
#ifdef DEBUG2
    printf("Message %d arrived: qos %d, retained %d, dup %d, packetid %d\n", 
		++arrivedcount, message.qos, message.retained, message.dup, message.id);
    printf("Topic Qos updated:  %.*s\n", (int)message.payloadlen, (char*)message.payload);
#endif    
    Qos = atoi((char*)message.payload);
}

void Node::Connect()
{
    float version = 0.3;
    const char* topic = "temperature";
    printf("Version is %f\n", version);
    const char* broker_ip = "192.168.7.1";
    int port = 1883;
    printf("Node %d connecting to %s:%d\n",id, broker_ip,port);
    int rc = m_ipstack->connect(broker_ip, port);
	if (rc != 0)
	    printf("rc from TCP connect is %d\n", rc);
 
#ifdef DEBUG2
    printf("Node %d connecting\n", id);
#endif
    MQTTPacket_connectData data = MQTTPacket_connectData_initializer;       
    data.MQTTVersion = 3;
    data.clientID.cstring = (char*)"mbed-icraggs";

    rc = m_client->connect(data);
	if (rc != 0)
	    printf("rc from MQTT connect is %d\n", rc);
#ifdef DEBUG2
    printf("Node %d connected\n",id);
#endif

    sprintf(topicStatus, "sensor/%d/status",id);
    sprintf(topicWater, "sensor/%d/water",id);
    sprintf(topicQoS, "sensor/%d/QoS",id);
    rc = m_client->subscribe(topicStatus, MQTT::QOS2, CallbackStatus);
    if (rc != 0)
        printf("Error subscribing in topic status is %d\n", rc);
#ifdef SUBS
    
    rc = m_client->subscribe(topicWater, MQTT::QOS2, CallbackWater);
    if (rc != 0)
        printf("Error subscribing in topic water is %d\n", rc);
    
    rc = m_client->subscribe(topicQoS, MQTT::QOS2, CallbackQoS);
    if (rc != 0)
        printf("Error subscribing in topic QoS is %d\n", rc);
#endif
}
void Node::UpdateSensors()
{
#ifdef HW
    FILE *cmd=popen("cat /sys/devices/ocp.3/helper.12/AIN4", "r");
    char result[24]={0x0};
    while (fgets(result, sizeof(result), cmd) !=NULL);
    pclose(cmd);
    temp = ((atoi(result)/2.0)/10.0);
#else
    temp = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/3.3));      
    humidity = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/3.3));      
#endif
}

float Node::GetTemperature()
{
    return temp;
}

float Node::GetHumidity()
{
    return humidity;
}

void Node::PublishTopics(const char* topic,float value)
{
    MQTT::Message message;
    UpdateSensors();
#ifdef DEBUG2
    printf("Sending topic %s: %.2f\n",topic, value);
#endif
    //char buf[100];
    char buf[2];
    sprintf(buf,"%f",value);
    message.qos = MQTT::QOS2;
    message.retained = false;
    message.dup = false;
    message.payload = (void*)buf;
    message.payloadlen = strlen(buf)+1;
    int rc = m_client->publish(topic, message);
        if (rc != 0)
                printf("Error %d from sending message with topic %s\n", rc,topic);

}
void Node::Disconnect()
{
    int rc = m_client->disconnect();
    if (rc != 0)
        printf("rc from disconnect was %d\n", rc);

    m_ipstack->disconnect();
}

#ifdef HW
void  Node::HardwareInit()
{
    // Initialize library and hardware.
    beaglebone_pruio_start();
    beaglebone_pruio_init_adc_pin(1,12); 
}
#endif

void Node::InitTopics()
{
    sprintf(topicTemp, "sensor/%d/temp",id);
    sprintf(topicHum, "sensor/%d/hum",id);
    //sprintf(topicStatus, "sensor/%d/status",id);
    //sprintf(topicWater, "sensor/%d/water",id);
    //sprintf(topicQoS, "sensor/%d/QoS",id);
#ifdef DEBUG2
    printf("%s\n",topicTemp);
    printf("%s\n",topicHum);
    //printf("%s\n",topicStatus);
    //printf("%s\n",topicWater);
    //printf("%s\n",topicQoS);
#endif
}


void NodeThread(const int nodeId)
{
    std::shared_ptr<IPStack> ipstack1 = std::make_shared<IPStack>();
    std::shared_ptr<MQTT::Client<IPStack, Countdown>> client1 = std::make_shared<MQTT::Client<IPStack, Countdown>>(*ipstack1);
    const int id = nodeId; 
    Node node = Node(id,ipstack1,client1);
#ifdef DEBUG2
    printf("Node %d is running\n",node.id);
#endif
#ifdef HW
    node.HardwareInit();
#endif
#ifdef DEBUG2
    printf("Node %d is configured\n",node.id);
#endif
    node.Connect();
#ifdef DEBUG2
    printf("Node %d is connected\n",node.id);
#endif
    node.InitTopics();
#ifdef DEBUG2
    printf("Node %d creating topics\n",node.id);
#endif
    while(1)
    {
#ifdef DEBUG2
        printf("nodeActivated: %d\n",nodeActivated);
#endif
        node.UpdateSensors();
        if(nodeActivated)
        //if(true)
        {
            //node.UpdateSensors();
            float value = node.GetTemperature();
            node.PublishTopics(topicTemp,value); 
            //node.PublishTopics("temperature",value); 
            value = node.GetHumidity();
            node.PublishTopics(topicHum,value); 
            //node.PublishTopics("humidity",value); 
            //sleep(PUBLISH_TIME); 
       }
       else
       {
           node.PublishTopics("sensor/alive",nodeActivated); 
#ifdef DEBUG2
           printf("Desconectado\n");
#endif
       }
       sleep(PUBLISH_TIME); 
    }
    node.Disconnect();
}
int main(int argc, char* argv[])
{ 
    NodeThread(argc);
    return 0;
}

