# ATTRIBUTE Plot

## Goal
The purpose of this analytic is to create an exploratory data analysis on the pandas Dataframe and return a html report. The analytic requires the Dataframe only.


## Usage: 
- Build the analytics container:
```
docker build -t kestrel-analytics-pandas-profiling .
```

- Command to trigger kestrel-analytics-pandas-profiling analytic
```
dns_conns = get network-traffic from file:///Users/dns_tunneling.json where [network-traffic:dst_port = 53]
APPLY docker://pandas-profiling on dns_conns

```
![screenshot](kestrel-analytics-pandas-profiling.png
)
  
