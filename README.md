# Gephi Bitcoin Stream script
Simple script that connects to `blockchain.info` and stream the result as graph into gephi.

Done quickly 5 years ago, reshaped to make it works with recent version of python and gephi.

# Install & Usage

* Download or Clone project
* `pip install -r req.txt`  to install dependencies
* Open Gephi, create a new project and Start the master server in the Streaming plugin.
* `python complete.py` Create a graph by representing in addresses, out addresses and transactions as node and relationship in addresses-[]-> transaction and transaction-[]-> out addresses.
* `python simple.py` : Same as before , but it will only represent in / out addresses as node and relationship in addresses-[]->out addresses.
* Watch your gephi and have fun
