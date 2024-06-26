## Installation Guides

### Prerequisites

1. An SQL Database should already be running and contactable by this server through a certain URL.
2. Docker is needed to run the servers in production.
3. Preferably, the fingerprint processing server (FPS) is already running so that the machine learning server (MLS) can received fingerprint data from FPS and emit fingerprint to FPS.

### Steps

#### Development

1. Use a terminal, and clone this repository with the command <code>git clone https://github.com/lulus-on-time/machine-learning.git \<folder name></code>
2. Create a python virtual environment using this command <code>python3 -m venv venv</code>
3. Activate the virtual environment using one of these commands:
- On Windows: <code>venv\Scripts\activate</code>
- On macOS and Linux: <code>source venv/bin/activate</code>
4. Install all of the required packages and dependencies using this command <code>pip install -r requirements.txt</code>
5. Run <code>python app.py</code> to run the machine learning server.

#### Production

1. Use a terminal, and clone this repository with the command <code>git clone https://github.com/lulus-on-time/machine-learning.git \<folder name></code>
2. Create a python virtual environment using this command <code>python3 -m venv venv</code>
3. Activate the virtual environment using one of these commands:
- On Windows: <code>venv\Scripts\activate</code>
- On macOS and Linux: <code>source venv/bin/activate</code>
4. Modify the environment variables (<code>DATABASE_URI</code> and <code>SQLALCHEMY_DATABASE_URI</code>) in the docker file with the same value. Optional: edit the <code>LABEL</code> and <code>EXPOSE</code> according to your needs. The default exposed port is 5000.
5. Build the docker image with the command <code>docker build -t .</code> .

## Dataset Usage

There are 2 set of data available for use. All of them are available in the <code>data</code> folder. 
- The <code>29-04-2024</code> folder consists of 20 distinct locations (all classrooms, no corridors, and no other non-classrooms) collected from Gedung Baru Fasilkom UI. This data is used to select the optimal machine learning model (include training, validation, and testing phase).
- The <code>22-05-2024</code> folder consists of several locations collected from Gedung Baru Fasilkom UI (**5th, 6th, and 7th floor only**) . This data is used to train and test the model that is already deployed in machine learning server (MLS).

Note that each folder consists of several csv files. The files that are used for machine learning purposes are **Network.csv , Fingerprint.csv, and FingerprintDetail.csv**. All you need to do is to merge these 3 csv files. 

> For the full data processing, you can see it in the <code>models/call_model.py</code>, specifically in <code>build_df</code> function. All of the other csv files can be used in conjunction with the previously mentioned three csv files to further add more information for you own project.

