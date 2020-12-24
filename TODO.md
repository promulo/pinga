# TODO

Many things that were intended for this first alpha version
of Pinga were unfortunately left out (I'm afraid my choice
of time to work on the project was rather unfortunate). The
original plan was to have both producer and consumer distributed
as .deb packages that would be automatically built as part of CI.
Additionally, both the aiven Kafka and aiven PostgreSQL
services would be created by Terraform but due to the
limitation of trial credits not being "transferable" onto
sub-accounts, that also had to be postponed.

Other TODO items are listed below.

### Some of the things that can be worked on

- Make check interval configurable (currently 5s)
- Make Kafka topic configurable (currently pinga-events)
- Automate PostgreSQL database creation
- More restricted networking and VPC configuration
- Terraform to output service URIs somewhere
  - CI to pull config values from the above during build
- Distribution of .snap, .deb, .rpm and Docker images
- Run producer and consumer as systemd services
- Handling of SIGKILL, SIGTERM, etc.
- Additional backends other than PG (InfluxDB? Mongo? Cassandra? M3?)
- Fine tuning of Kafka cluster
- More metrics and analytics
- Better logging
- Better README
