# Aiven Kafka Quickstart with Polygon.io Websocket

### A demonstration on streaming cryptocurrency data in realtime with Aiven services.

#### In this demonstration, we will show how to stream cryptocurrency quotes in real-time from the polygon.io websocket. With this stream, we will then structure the json data to reflect only the spread for the given instrument, which is the difference between the bid and ask price. We will then convert the timestamp to a string with the date in “ISO 8601” format for better readability. 

#### Next, we will gather analytics on the health of our data stream by using Aiven’s services integrations to store telemetry data in an InfluxDB timeseries database, and then visualize these metrics on a Grafana dashboard. 

#### The technologies used in this tutorial include: 

#### Kafka - an open source streaming data store that acts as a messaging queue with producer and consumer classes

#### InfluxDB - an open source time series database used mainly for IoT sensor data and real-time analytics

#### Grafana - an open source analytics and visualization web application that provides charts, graphs and alerts

### 1. Start the Kafka Broker through the Aiven Services Menu

##### ![alt text](https://github.com/Ryan-Ray-Martin/aivan_crypto_stream/blob/main/images/Screen%20Shot%202021-07-20%20at%207.04.04%20PM.png)

#### Aiven simplifies the task of spinning up a Kafka cluster by providing an intuitive menu to create new services that can either integrate or stand alone. For now, we will create a new service and select Kafka 2.7 to start a broker that will allow communication between the producers and consumers of our cryptocurrency data stream. We will then choose our preferred cloud provider, region, and then service plan. 

##### ![alt text](https://github.com/Ryan-Ray-Martin/aivan_crypto_stream/blob/main/images/Screen%20Shot%202021-07-20%20at%207.04.36%20PM.png)

#### Once the service begins running, we can create a kafka topic that will allow us to organize and segment our data stream. Here we will call our topic: “crypto-topic.” 

##### ![alt text](https://github.com/Ryan-Ray-Martin/aivan_crypto_stream/blob/main/images/Screen%20Shot%202021-07-20%20at%207.12.20%20PM.png)

### 2. Use Websocket Client from Polygon to Create Kafka Producer

#### By referencing a provided websocket client class from polygon.io, we can implement a custom websocket class to stream cryptocurrency data in real-time. But first, we must create our producer with the correct attributes that will allow our local machine to communicate with the kafka broker in the cloud. 

##### ![alt text](https://github.com/Ryan-Ray-Martin/aivan_crypto_stream/blob/main/images/Screen%20Shot%202021-07-20%20at%207.15.02%20PM.png)

#### We find these attributes in the “overview” page in our Kafka services in Aiven. We use the “service URI” as our bootstrap server, and then handle our security protocol with the downloaded SSL files. The value serializer is modified with a lambda function to encode our json data for later formatting. We set “acks” to zero so that the producer will not wait for any acknowledgment from the server and send records immediately. The “batch size” is set to zero in order to reduce throughput and conserve memory. 

##### ![alt text](https://github.com/Ryan-Ray-Martin/aivan_crypto_stream/blob/main/images/Screen%20Shot%202021-07-20%20at%207.15.22%20PM.png)

#### In the custom process message function, we parse the quotes from the websocket data stream in json format to structure the data for our use case. We accomplish this by instantiating a new json object called “crypto_data”, then we change the values of our original message, adding these new values to our json object. We sink “crypto_data” to our kafka topic to use later for the consumer.

#### BEFORE:

#### {'ev': 'XQ', 'pair': 'BTC-USD', 'lp': 0, 'ls': 0, 'bp': 29603.82, 'bs': 0.0006127, 'ap': 29603.83, 'as': 4.16595782, 't': 1626828416892, 'x': 1, 'r': 1626828416899}

#### AFTER: 

#### {"timestamp": "2021-07-20 18:45:58.389", "symbol": "BTC-USD", "spread": 0.00999999999839929}

### 3. Implement a Consumer Class to Fetch Our Event Data

#### In this class, we simply pull the event data from the kafka topic that we created in the producer class. 

#### Similarly to the producer, we have to declare a number of attributes related to our Aiven service. Firstly, we insert our topic name in quotes, then set the offset to “latest”, in order to automatically reset to the most recent instance of data in our topic. We, again, fill in our SSL protocol information. 

##### ![alt text](https://github.com/Ryan-Ray-Martin/aivan_crypto_stream/blob/main/images/Screen%20Shot%202021-07-20%20at%209.26.09%20PM.png)

#### Next, we loop through our consumer object to view the current spread of Bitcoin, formatted in our json object. With this data stream, one could create many useful applications for visualization. One could even use this data stream to train, deploy, and then serve a machine learning model to execute trades in the cryptocurrency market.

##### ![alt text](https://github.com/Ryan-Ray-Martin/aivan_crypto_stream/blob/main/images/Screen%20Shot%202021-07-20%20at%206.46.21%20PM.png)

### 4. Utilize Service Integrations to Visualize Telemetry Data

##### ![alt_text](https://github.com/Ryan-Ray-Martin/aivan_crypto_stream/blob/main/images/Screen%20Shot%202021-07-20%20at%208.24.12%20PM.png)

#### To gather telemetry data, we will use the Aiven service integration option to visualize the health of our kafka broker and data stream. On the kafka service overview menu, we will click “manage integrations” and then choose the metrics to automatically send metrics to either InfluxDB or postgres. This will create a new InfluxDB service with telemetric data from the kafka broker. 

##### ![alt_text](https://github.com/Ryan-Ray-Martin/aivan_crypto_stream/blob/main/images/Screen%20Shot%202021-07-20%20at%208.31.37%20PM.png)

#### Then, to visualize these metrics, we will go to the services menu, selecting our InfluxDB service. Next, we will go to the InfluxDB service overview menu and choose “manage integrations” again. We will now select the dashboard integration to automatically visualize the telemetry data that is stored in InfluxDB. All we have to do now is select the Grafana service, copy the password in “connection information”, and go to the service URI to login to Grafana. 

#### ![alt_text](https://github.com/Ryan-Ray-Martin/aivan_crypto_stream/blob/main/images/Screen%20Shot%202021-07-20%20at%208.33.18%20PM.png)

#### Under Grafana’s general tab, we will be able to view metric from our Kafka service. 

#### ![alt_text](https://github.com/Ryan-Ray-Martin/aivan_crypto_stream/blob/main/images/Screen%20Shot%202021-07-20%20at%208.34.08%20PM.png)

