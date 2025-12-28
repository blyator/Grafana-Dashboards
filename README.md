# <img src="https://wp-cdn.pi-hole.net/wp-content/uploads/2016/12/Vortex-R.png" width="36" height="36"> Pi-hole DNS and Linux Monitoring

<p align="center">
  <img src="screenshots/pihole.png" width="50%" />
  <img src="screenshots/pihole2.png" width="50%" />
  <img src="screenshots/pihole1.png" width="50%" />
  <img src="screenshots/system.png" width="50%" />
</p>

> **Pi-hole Live Dashboard:** [https://serverdashboard.qzz.io](https://serverdashboard.qzz.io/d/edknpuskjzw1sc/)  
> **System Health Dashboard:** [https://serverdashboard.qzz.io/metrics](https://serverdashboard.qzz.io/d/edknpuskjzw1sc/)

### Network Security & Infrastructure Reliability

This repo shows how I monitor my demo home lab's Pi-hole ad-block and DNS on a Linux server. I'm using Prometheus and Grafana to track DNS queries and system stats (CPU, RAM, Disk) in real-time, with Nginx handling SSL to keep the dashboard secure.

---

## Project Overview

I built this setup to improve my overall internet experience, which had become increasingly unusable without an effective ad-blocker.This provides network-wide ad-blocking and tracker protection via Pi-hole DNS. By acting as the primary DNS sinkhole for my entire network, it strips away advertisements at the DNS level before they ever reach any of my devices, significantly improving my internet experience.

I also integrated system monitoring alongside Pi-hole statistics. Now I can easily tell how effectively Pi-hole is filtering traffic while also monitoring the health and stability of the server at a glance all from the dashboard. It is so easy to manage the system and quickly spot any issues without having to query anything.
## The Stack
- **DNS Sinkhole:** Pi-hole
- **Reverse Proxy:** Nginx (SSL/TLS Termination)
- **Metrics Collection:** Prometheus
- **Exporters:**
  - `pihole-exporter` - DNS stats
  - `node_exporter` - System stats
- **Visualization:** Grafana
- **Alerting:** Alertmanager - Via Telegram

---

##  Dashboard Insights

### 1. [Pi-hole DNS Performance](https://serverdashboard.qzz.io/d/edknpuskjzw1sc/)
Real-time monitoring of DNS traffic and filtering efficiency. Key metrics tracked include:
- **Network Summary:** Total Queries, Active Clients and Domains on Blocklist.
- **Filtering Impact:** Tracking of Blocked Queries and total Ads Blocked.
- **Query Status:** Breakdown of Cache hits.
- **Upstream Performance:** Monitoring of Upstream DNS Response Times.

<blockquote>
  <a href="https://serverdashboard.qzz.io/d/edknpuskjzw1sc/">
    <img src="screenshots/pihole.png" width="30%" alt="Pi-hole DNS Dashboard">
  </a>
</blockquote>

### 2. [System Health](https://serverdashboard.qzz.io/d/rYdddlPWk/)
Keeps track of the server's resources to prevent issues:
- **CPU Load:** Breakdown of System vs. User load.
- **Memory Usage:** RAM usage and swap tracking.
- **Disk Usage:** Real-time capacity monitoring.

<blockquote>
  <a href="https://serverdashboard.qzz.io/d/rYdddlPWk/">
    <img src="screenshots/system.png" width="30%" alt="System Health Dashboard">
  </a>
</blockquote>

---

##  Alerting Policies

I also set up alerts to ping me on **Telegram** if the server gets overloaded.

| Metric | Threshold | Duration | Notification Channel |
| :--- | :--- | :--- | :--- |
| **High CPU Usage** | > 80% | > 2 Minutes |  Telegram |
| **High RAM Usage** | > 80% | > 2 Minutes |  Telegram |
| **Low Disk Space** | > 90% | - |  Telegram |

*The 2-minute delay ensures I don't get annoyed by random quick spikes.*

---

### Architecture

This system uses a standard Prometheus pull-based architecture, securely exposed via Nginx.

```mermaid
graph TD
    User -- HTTPS --> Nginx -- Proxy --> Grafana
    Pi-hole -- Stats --> Prometheus -- Query --> Grafana
    Prometheus -- Alerts --> Telegram
```

- **Pi-hole**: Core DNS ad-blocker.
- **Prometheus**: Time-series database that scrapes metrics from the server.
- **Grafana**: Visualization layer for building real-time dashboards.
- **Exporters**: `node_exporter` (System stats) and `pihole_exporter` (DNS stats).
- **Security**: **Nginx** handles SSL/TLS termination for secure remote access.
- **Alerting**: Alertmanager integration for **Telegram** notifications.

---


##  Deployment and Setup

To get this monitoring stack running, you'll need three main apps installed. I recommend using **Docker** for all of them to keep things simple.

### 1. Install the Core Apps
Ensure you have these three services up and running:
- **[Pi-hole](https://pi-hole.net/)**: Your network's ad-blocker and DNS server.
- **[Prometheus](https://prometheus.io/)**: The database that collects and stores metrics.
- **[Grafana](https://grafana.com/oss/grafana/)**: The dashboard tool used to visualize all the data.

### 2. Set Up the Exporters
Exporters take data from your apps and hand it over to Prometheus.
- **Node Exporter**: Install this on your server port `9100` to track system health like CPU, RAM and Disk usage.
- **Pi-hole Exporter**: I use the [bazmonk/pihole6_exporter](https://github.com/bazmonk/pihole6_exporter) on port `9617`. You'll need to provide your Pi-hole API token so it can read your DNS stats.

### 3. Connect Prometheus to Exporters
Update your `prometheus.yml` file to tell it where to find the data. Add these lines under `scrape_configs`:
```yaml
- job_name: 'node'
  static_configs:
    - targets: ['localhost:9100']

- job_name: 'pihole'
  static_configs:
    - targets: ['localhost:9617']
```

### 4. Import the Dashboards
1. Open Grafana, go to **Dashboards > Import**.
2. **For Pi-hole**: Upload the `pihole-stats.json` file included in this repository.
3. **For System Health**: I recommend using the [Node Exporter Full](https://grafana.com/grafana/dashboards/1860-node-exporter-full/) dashboard.
### 5. Secure with Nginx 
Finally, use **Nginx** as a reverse proxy to handle SSL (HTTPS). This keeps your connection secure when you access it outside of your network.



---



## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.
