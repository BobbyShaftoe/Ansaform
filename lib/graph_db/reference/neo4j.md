
# Neo4j

https://neo4j.com/developer/graph-database/


Developer Guides Getting Started Getting Started What is a Graph Database? 

Intro to Graph DBs Video Series Concepts: RDBMS to Graph Concepts: 
NoSQL to Graph Getting Started Resources Neo4j Graph Platform Graph Platform Overview Neo4j Desktop Intro Neo4j Browser Intro… 

[Read more →](https://neo4j.com/developer/python/)
  

### **Developer Guides**

*   [Getting Started](/developer/get-started/)
*   [What is a Graph Database?](/developer/graph-database/)
*   [Intro to Graph DBs Video Series](/developer/intro-videos/)
*   [Concepts: RDBMS to Graph](/developer/graph-db-vs-rdbms/)
*   [Concepts: NoSQL to Graph](/developer/graph-db-vs-nosql/)
*   [Getting Started Resources](/developer/getting-started-resources/)


*   [Graph Platform Overview](/developer/graph-platform/)
*   [Neo4j Desktop Intro](/developer/neo4j-desktop/)
*   [Neo4j Browser Intro](/developer/neo4j-browser/)
*   [Neo4j ETL Tool](/developer/neo4j-etl/)
*   [Neo4j APOC Library](/developer/neo4j-apoc/)
*   [Neo4j Graph Algorithms](/developer/graph-algorithms/)
*   [Neo4j & GraphQL](/developer/graphql/)


*   [Cypher Overview](/developer/cypher/)
*   [Cypher Basics I](/developer/cypher-query-language/)
*   [Cypher Basics II](/developer/cypher-basics-ii/)
*   [Filtering Query Results](/developer/filtering-query-results/)
*   [Aggregation, Returns, & Functions](/developer/aggregation-returns-functions/)
*   [Cypher Style Guide](/developer/cypher-style-guide/)
*   [From SQL to Cypher](/developer/guide-sql-to-cypher/)
*   [User Defined Procedures & Functions](/developer/procedures-functions/)
*   [Tutorial: Build a Recommendation Engine](/developer/guide-build-a-recommendation-engine/)
*   [Cypher Resources](/developer/cypher-resources/)


*   [Graph Modeling Overview](/developer/data-modeling/)
*   [Graph Modeling Guidelines](/developer/guide-data-modeling/)
*   [Modeling: RDBMS to Graph](/developer/relational-to-graph-modeling/)
*   [Modeling Designs](/developer/modeling-designs/)
*   [Graph Modeling Tips](/developer/modeling-tips/)
*   [Interactive Graph Models](/developer/graphgist/)


*   [Import Overview](/developer/data-import/)
*   [Importing CSV](/developer/guide-import-csv/)
*   [Importing API Data](/developer/guide-import-json-rest-api/)
*   [Import: RDBMS to Graph](/developer/relational-to-graph-import/)
*   [Example: Northwind Dataset](/developer/guide-importing-data-and-etl/)
*   [How-To: Desktop CSV Import](/developer/desktop-csv-import/)
*   [Example Datasets](/developer/example-data/)


*   [Visualization Overview](/developer/graph-visualization/)
*   [Visualization Tools](/developer/tools-graph-visualization/)
*   [Other Visualizations](/developer/other-graph-visualizations/)


*   [Drivers Overview](/developer/language-guides/)
*   [Java](/developer/java/)
*   [Spring Framework](/developer/spring-data-neo4j/)
*   [.NET](/developer/dotnet/)
*   [JavaScript](/developer/javascript/)
*   [Python](/developer/python/)
*   [Go](/developer/go/)
*   [Ruby](/developer/ruby/)
*   [PHP](/developer/php/)


*   [Integrations Overview](/developer/integration/)
*   [Tools & Libs for Neo4j](/developer/ecosystem/)
*   [Apache Spark](/developer/apache-spark/)
*   [Elastic-Search](/developer/elastic-search/)
*   [MongoDB](/developer/mongodb/)
*   [Cassandra](/developer/cassandra/)


*   [Deployment Overview](/developer/in-production/)
*   [Performance Tuning](/developer/guide-performance-tuning/)
*   [Clustering Neo4j](/developer/guide-clustering-neo4j/)
*   [How-To: Run Neo4j in Docker](/developer/docker-run-neo4j/)
*   [Startups: Free Neo4j Enterprise](/startup-program/)
*   [Online Course: Neo4j Administration](/graphacademy/online-training/neo4j-administration/)


*   [Cloud Overview](/developer/guide-cloud-deployment/)
*   [Deploying to Amazon EC2](/developer/neo4j-cloud-aws-ec2-ami/)
*   [Deploying to Google Compute Engine](/developer/neo4j-google-cloud-launcher/)
*   [Deploying to Azure](/developer/neo4j-cloud-azure-cluster)
*   [Neo4j Cloud VMs](/developer/neo4j-cloud-vms)
*   [Orchestration Tools](/developer/guide-orchestration)
*   [Cloud Hosting Providers](/developer/neo4j-cloud-hosting-providers)


*   [Resource Overview](/developer/resources/)
*   [Getting Started Course](/graphacademy/online-course-getting-started/)
*   [Ruby / Rails Course](/developer/ruby-course/)
*   [Online Course: Neo4j Administration](/graphacademy/online-training/neo4j-administration/)
*   [Neo4j Documentation](/docs/)
*   [Developer Manual](/docs/developer-manual/current/)
*   [Java Developer Reference](/docs/java-reference/current/)
*   [Operations Manual](/docs/operations-manual/current/)
*   [Cypher Refcard](/docs/cypher-refcard/current/)


*   [Contributing Overview](/developer/contribute/)
*   [Help on Community Forums](https://community.neo4j.com/)
*   [Speaker Program: Share your Story](/speaker-program/)

[  
](http://community.neo4j.com)
[  
](http://twitter.com/neo4j)
[  
](http://youtube.com/neo4j)
[  
](https://meetup.com/Neo4j-Online-Meetup/)
[  
](https://github.com/neo4j/neo4j)
[  
](http://stackoverflow.com/questions/tagged/neo4j)
Want to Speak? [Get $ back.](/speaker-program/)

# Using Neo4j from Python

Goals
> This guide provides an overview of how to connecting to Neo4j from Python. While it is not comprehensive, it aims to introduce the available drivers and links to other relevant resources.

Prerequisites
*   You should be familiar with [graph database concepts](/developer/graph-database) and the property graph model.
*   You should have [installed Neo4j](/download) and made yourself familiar with our [Cypher Query language](/developer/cypher-query-language).
*   We also recommend installing and becoming familiar with both [pip](https://pip.pypa.io/) and [virtualenv](https://virtualenv.pypa.io/) before working on a Python project.
Intermediate
* * *


![python logo](//s3.amazonaws.com/dev.assets.neo4j.com/wp-content/uploads/python-logo.png)

Neo4j can be installed on any system and then accessed via its binary and HTTP APIs.
You can use the official binary driver for Python (neo4j-python-driver) or connect via HTTP with any of our community drivers.

The Neo4j Python driver is **officially supported** by Neo4j and connects to the database using the binary protocol. It aims to be minimal, while being idiomatic to Python.

Support for Python 2 will be removed in the upcoming 2.0 release of the driver.

```
pip install neo4j
```



### neo4j-driver
##### 1.7.1

The Neo4j Team, [Nigel Small](https://twitter.com/technige)

[Package](https://pypi.python.org/pypi/neo4j)
[Neo4j Online Community](https://community.neo4j.com/c/drivers-stacks/python)

[Docs](http://neo4j.com/docs/developer-manual/current/drivers/)
[API](https://neo4j.com/docs/api/python-driver/current/)
[Source](https://github.com/neo4j/neo4j-python-driver)



### The Example Project

The Neo4j example project is a small, one page webapp for the movies database built into the Neo4j tutorial. The front-end page is the same for all drivers: movie search, movie details, and a graph visualization of actors and movies. Each backend implementation shows you how to connect to Neo4j from each of the different languages and drivers.
You can learn more about our small, consistent example project across many different language drivers [here](../example-project). You will find the implementations for all drivers as [individual GitHub repositories](https://github.com/neo4j-examples?q=movies), which you can clone and deploy directly.


The drivers below have been thankfully contributed by the Neo4j community. Many of these are fully featured and well maintained. But we don’t take any responsibility for their fitness for use with the most recent versions of Neo4j.

For anyone working with [Python](https://www.python.org/), the Neo4j community have contributed a range of driver options. These range from lightweight to comprehensive driver packages as well as libraries designed for use with web frameworks such as [Django](https://www.djangoproject.com/).
While Python 3 is preferred, some drivers still support Python 2, please check with the individual project if you need it.
While we do not provide a specific web framework recommendation, both the lightweight [Flask](http://flask.pocoo.org/) and the more comprehensive [Django](https://www.djangoproject.com/) frameworks are known to work well.
Many Pythonistas have invested a lot of time and love to develop these libraries, so if you use them, please provide feedback to the authors and help us improve.

Py2neo is a client library and comprehensive toolkit for working with Neo4j from within Python applications and from the command line. It has been carefully designed to be easy and intuitive to use.
  
Author
[Nigel Small](https://twitter.com/technige)

Package
[https://pypi.python.org/pypi/py2neo](https://pypi.python.org/pypi/py2neo)

Source
[https://github.com/nigelsmall/py2neo](https://github.com/nigelsmall/py2neo)

Example
[https://github.com/neo4j-examples/movies-python-py2neo](https://github.com/neo4j-examples/movies-python-py2neo)

### Docs

[http://py2neo.org/](http://py2neo.org/)

Python
2.7 / 3.4+

Protocols
Bolt, Http

### Installation

```
pip install py2neo
Example
from py2neo import Graph
graph = Graph()
tx = graph.begin()
for name in ["Alice", "Bob", "Carol"]:
    tx.append("CREATE (person:Person {name:{name}}) RETURN person", name=name)
alice, bob, carol = [result.one for result in tx.commit()]
```


## Neomodel

An Object Graph Mapper built on top of the Neo4j python driver. Familiar Django style node definitions with a powerful query API, thread safe and full transaction support. A Django plugin [django_nemodel](https://github.com/neo4j-contrib/django-neomodel) is also available.
  
Author
Athanasios Anastasiou and Robin Edwards

Package
[https://pypi.python.org/pypi/neomodel](https://pypi.python.org/pypi/neomodel)

Source
[http://github.com/neo4j-contrib/neomodel](http://github.com/neo4j-contrib/neomodel)

Docs
[http://neomodel.readthedocs.org/](http://neomodel.readthedocs.org/)

Python
2.7 / 3.3+

Protocols
Bolt

