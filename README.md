# IoTImageRecognition
<p align="center">
  <img src="https://github.com/aaronbae/IoTImageRecognition/blob/master/other/results-table.PNG" width="700" title="IoT Image Classification Results">
</p>
Note that the project is aimed at deploying an image classification app to an edge device (in my case a raspberry pi). The computed results will send messages to the Azure IoT Hub and can be analyzed through its analytics service, Stream Analytics. Here are the steps that are involved in deploying the project:

1. Build the image through Docker or Visual Studio Code Extension for Azure Iot. This should create an image
2. Tag the image and upload it to a Azure Container Registry
3. Deploy the image from Azure IoT Hub or through Azure Cli (your terminal)
4. Start a BlobStorage and link it to the Stream Analytics service
5. View the messages received by the IoT Hub on the analytics service via query

Note that in total you will need these services:
1. Azure Container Registry
2. Azure IoT Hub
3. Azure Stream Analytics
4. Azure Storage Account

Note that all of these services have a free tier, but IoT Hub has a limitations on how many messages you can send per day. So be aware! Also, note that you will need to install these software:
1. Azure Cli on both your development machine and the edge node machine
2. Docker on your development machine
3. (optional) Visual Studio Code
4. (optional) Raspbian (OS for Raspberry Pi)

# Citation
We recognize that this project was largely a small modification project to the original EdgeBench Project. Here is a link to the original repository by Anirban Das and his team:
- Git: https://github.com/akaanirban/edgebench
- Paper: https://arxiv.org/pdf/1811.05948.pdf
