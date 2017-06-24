# Mining Twitter Data

This project aims to extract 1 million data from Twitter API, import the data into Neo4j, and use YCSB framework to test the performance of Neo4j.

Installation
----------------------

### Install the requirements
 
* Install the requirements using `pip install -r requirements.txt`.
    * Make sure you use Python 3.
* Run `mkdir private.py` and set the following keys (gain from Twitter API) in this file
	* CUSTOMER_KEY
	* CUSTOMER_SECRET
	* ACCESS_TOKEN
	* ACCESS_SECRET


Usage
-----------------------

* Run `twitter_streaming.py`
    * This will create 20 Json files in the `data` folder and each file has 5 housand records.
* Run `twitter_neo4j.py`
    * This will iterate all Json files in the `data` folder and execute cypher query to import data.
* Run `ASRL-YCSB\scriptst\Neo4j_workloads.bat`
    * This will run 3 workloads to test the performance of Neo4j and create logs in the `ASRL-YCSB\scriptst\logs` folder.
* Run `create_graph.py`
	* This will visualize the above log files.

