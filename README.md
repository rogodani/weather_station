# **Weather monitor**

## **Hardware**
- Weather station: https://www.sparkfun.com/products/15901
- RapbarryPi Zero W
- 4,7 K resistor
- 2 x RJ11 connector
- MCP3008 ADC

## **Software**
- PostgreSQL
- pgAdmin

## **Instalation**
#### **PostgreSQL**
- Enable SSH on the Raspberry Pi

`sudo apt install postgresql postgresql-contrib libpq-dev`

- Check the Postgres cluster status. If the cluster is down check the log file

`pg_lsclusters`

- Access the Postgres user

 `sudo su postgres`
 
- Configure PostgreSQL

```bash
psql                                    # access psql
SHOW hba_file;                          # get the pg_hba.conf file
\q                                      # exit psql
exit                                    # exit postgres user
sudo find / -name "postgresql.conf"     # find the location of postgresql.conf
```
- If you want to access Postress froma  differente machine add in pg_hba.conf (24 value is to cover a range of IP addresses on the network)

`host all all 192.168.100.2/24 trust`

- The postgresql.conf file must be edited so it can listen for addresses. Add in postgresql.conf `listen_addresses = '*'`. For extra security you can hard code a list of IPs.
- Restart PostgreSQL

`sudo service postgresql restart`