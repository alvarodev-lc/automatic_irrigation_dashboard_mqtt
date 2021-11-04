#define MQTTCLIENT_QOS2 1

#include <memory.h>
#include <memory>
#include <thread>
#include "MQTTClient.h"
//#include <beaglebone_pruio.h>
//#include <beaglebone_pruio_pins.h>
#define DEFAULT_STACK_SIZE -1
#include <fstream>
#include "linux/linux.cpp"
#include <unistd.h>
int arrivedcount = 0;

bool sensorActivated = true;
class TempSensor {

public:
    float temp;
    bool sensorEnabled;
    TempSensor(std::shared_ptr <IPStack> ipstack,std::shared_ptr<MQTT::Client<IPStack, Countdown>> client): m_ipstack(ipstack), m_client(client),sensorEnabled(true){};
    float GetTemperature();
    void UpdateTemperature();
    void PublishTemperature();
    void Connect();
    void Disconnect();
    void HardwareInit();
private:
    std::shared_ptr <IPStack> m_ipstack;
    std::shared_ptr<MQTT::Client<IPStack, Countdown>> m_client;
};
void CallbackSubscriber(MQTT::MessageData& md)
{
    MQTT::Message &message = md.message;

    printf("Message %d arrived: qos %d, retained %d, dup %d, packetid %d\n", 
		++arrivedcount, message.qos, message.retained, message.dup, message.id);
    printf("Payload %.*s\n", (int)message.payloadlen, (char*)message.payload);
    int val = atoi((char*)message.payload);
    ( val == 0) ?sensorActivated=false:sensorActivated=true;
}
void TempSensor::Connect()
{
    float version = 0.3;
    const char* topic = "temperature";
    printf("Version is %f\n", version);
    const char* broker_ip = "192.168.7.1";
    int port = 1883;
    printf("Connecting to %s:%d\n", broker_ip,port);
    int rc = m_ipstack->connect(broker_ip, port);
	if (rc != 0)
	    printf("rc from TCP connect is %d\n", rc);
 
    printf("MQTT connecting\n");
    MQTTPacket_connectData data = MQTTPacket_connectData_initializer;       
    data.MQTTVersion = 3;
    data.clientID.cstring = (char*)"mbed-icraggs";

    rc = m_client->connect(data);
	if (rc != 0)
	    printf("rc from MQTT connect is %d\n", rc);
    printf("MQTT connected\n");

    rc = m_client->subscribe("status", MQTT::QOS2, CallbackSubscriber);
    if (rc != 0)
        printf("rc from MQTT subscribe is %d\n", rc);
}
void TempSensor::UpdateTemperature()
{
/* To check with pruio library if needed 
    if(beaglebone_pruio_messages_are_available())
    {
        beaglebone_pruio_message message;
        beaglebone_pruio_read_message(&message);
        if(!message.is_gpio && message.adc_channel==1)
        { 
            printf("Temperature sensor in ADC channel 1 is %i \n", message.adc_channel, message.value);
        }
        else
        {
            printf("Analog pin %i changed to value %i \n", message.adc_channel, message.value);
        }
    }
    else
    {
        temp = static_cast <float> (rand()) / static_cast <float> (3.3);
        printf("No new analog data, generating randomly: temp = %f\n",temp);
    }
*/
    FILE *cmd=popen("cat /sys/devices/ocp.3/helper.12/AIN4", "r");
    char result[24]={0x0};
    while (fgets(result, sizeof(result), cmd) !=NULL);
    pclose(cmd);
    temp = ((atoi(result)/2.0)/10.0);
}

float TempSensor::GetTemperature()
{
    return temp;
}

void TempSensor::PublishTemperature()
{
    MQTT::Message message;
    const char* topic = "temperature";
    UpdateTemperature();
    float value = GetTemperature();
    printf("Sending temperature: %f\n", value);
    char buf[100];
    sprintf(buf,"%f\n",value);
    message.qos = MQTT::QOS2;
    message.retained = false;
    message.dup = false;
    message.payload = (void*)buf;
    message.payloadlen = strlen(buf)+1;
    int rc = m_client->publish(topic, message);
        if (rc != 0)
                printf("Error %d from sending message with temperature\n", rc);

}
void TempSensor::Disconnect()
{
    int rc = m_client->disconnect();
    if (rc != 0)
        printf("rc from disconnect was %d\n", rc);

    m_ipstack->disconnect();
}

void  TempSensor::HardwareInit()
{
/* To check with pruio lib if needed
    // Initialize library and hardware.
    beaglebone_pruio_start();
    beaglebone_pruio_init_adc_pin(1,12); 
*/
    
}

void CheckTemperature()
{
    std::shared_ptr<IPStack> ipstack1 = std::make_shared<IPStack>();
    std::shared_ptr<MQTT::Client<IPStack, Countdown>> client1 = std::make_shared<MQTT::Client<IPStack, Countdown>>(*ipstack1);
    TempSensor sensor1 = TempSensor(ipstack1,client1);
    sensor1.HardwareInit();
    sensor1.Connect();

    while(sensorActivated)
    {
        sensor1.UpdateTemperature();
        sensor1.PublishTemperature(); 
        sleep(2); 
    }
    sensor1.Disconnect();
    //beaglebone_pruio_stop();
}
int main(int argc, char* argv[])
{ 
    //std::shared_ptr<IPStack> ipstack1 = std::make_shared<IPStack>();
    //std::shared_ptr<MQTT::Client<IPStack, Countdown>> client1 = std::make_shared<MQTT::Client<IPStack, Countdown>>(*ipstack1);
    //TempSensor sensor1 = TempSensor(ipstack1,client1);
    //sensor1.Connect();
    CheckTemperature();
    //sensor1.UpdateTemperature();
    //sensor1.PublishTemperature();  
    
    //sensor1.Disconnect();
    return 0;
}

