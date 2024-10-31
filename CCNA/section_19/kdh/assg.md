### Enable RIPv2 on every router. Ensure all networks except 203.0.113.0/24 are advertised. Do not perform any summarisation.
`router rip`
`version 2`
`no auto-summary`
`network 10.0.0.0`

### Verify all networks are in the router's routing tables.
`sh ip route`

### Verify that routing is working by checking that PC1 has connectivity to РС3.
`ping 10.1.2.10`

### Ensure that all routers have a route to the 203.0.113.0/24 network. Internal routes must not advertised to the Service Provider at 203.0.113.2.
`router rip`
`passive-interface f1/1`
`network 203.0.113.0`

### Verify that all routers have a path to the 203.0.113.0/24 network.
`sh ip route`

### Configure a default static route on R4 to the Internet via the service provider at 203.0.113.2
`ip route 0.0.0.0 0.0.0.0 203.0.113.2`

### Ensure that all other routers learn via RIP how to reach the Internet.
`router rip`
`deefault-information originate`

### Verify all routers have a route to the Internet.
`sh ip route`

### Enable EIGRP AS 100 on every router. Ensure all networks except  203.0.113.0/24 are advertised in EIGRP.
`router eigrp 100`
`network 10.0.0.0`

### Verify the routers have formed adjacencies with each other.
`sh ip eigrp neighbors`

### Which routing protocol (RIP or EIGRP) do you expect routes to the  10.x.x.x networks to be learned from in the routing tables?
AD값때문에 eigrp

### Do you expect to see any routes from the other routing protocol in the routing tables?
static 경로 추가한거땜에 RIP가 남아있네

### View the routing tables to verify your answers.
`sh ip route`