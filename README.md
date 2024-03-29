# Microgreens Automation System

## Introduction
This project aims to automate a microgreens production system. It's designed to manage the schedule of the lights, irrigation, and fans to control the climate (humidity and temperature). The project will be developed in three main phases:

1. **Proof of Concept (PoC)**: In this phase, the focus will be on controlling a single light. The goal is to establish the basic architecture of the system and ensure that the components can communicate effectively. The system will allow manual control and scheduling of the light from a web interface.

2. **Full Application (without Machine Learning)**: In this phase, the system will be expanded to control multiple lights, irrigation, and fans. The user interface will be enhanced to manage these additional components and to display the current state of the system.

3. **Full Application (with Machine Learning)**: In the final phase, a machine learning model will be incorporated into the system. This model will analyze images from a camera to determine the age of the crops. The system will notify the user when the crops are ready for harvest.

## Architecture
The system will be built using Python, SQL, and Azure, with a Raspberry Pi acting as the hardware interface for the lights, irrigation, and fans. The backend will be structured into two main parts: an API for the database and an API for the Raspberry Pi. Communication between the Raspberry Pi and the backend server will be handled using MQTT.

Here's a rough diagram of how these components could interact:
```
Frontend App <--> Backend Server (Database API + Device API) <--> PostGreSQL Database
					    ^ 
					    |
					    v
				MQTT Broker <--> Raspberry Pi (Python script controlling GPIO)
```

In this architecture, the Device API part of the backend would interact with MQTT Broker instead of directly with the Raspberry Pi.