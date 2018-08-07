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

# Advise:

The complete script will generate graph that will makes Force Atlas I, II running kind of crazy with default parameters. It’s because the amplitude of edges weight (representing the number of µBTC ) can be very wide. To stabilize the layouts I can advise you to :

* (Force Atlas I) Put the property Maximum Displacement to 1 or lower (but not 0).
* (Force Atlas II ) Put the property Edge Influence Weight to  0.2 or lower (0 is possible here).
