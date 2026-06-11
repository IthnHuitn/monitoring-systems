# Домашнее задание к занятию "`Средство визуализации Grafana`" - `Ефимов Вячеслав`

---


### Задание 1

![grafana1-1](https://github.com/IthnHuitn/monitoring-systems/blob/grafana/screens/grafana1-1.png)


---

### Задание 2

1. Утилизация CPU (в процентах, 100 - idle)
```promql
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

2. CPU LA 1/5/15 (Load Average) 
```promql
node_load1
node_load5
node_load15
```

3. Количество свободной оперативной памяти (в гигабайтах)
```promql
node_memory_MemFree_bytes / 1024 / 1024 / 1024
```

4. Количество места на файловой системе (свободное место в байтах)
```promql
node_filesystem_free_bytes{mountpoint="/"}
```

![grafana2-1](https://github.com/IthnHuitn/monitoring-systems/blob/grafana/screens/grafana2-1.png)


---

### Задание 3

![grafana3-1](https://github.com/IthnHuitn/monitoring-systems/blob/grafana/screens/grafana3-1.png)
![grafana3-2](https://github.com/IthnHuitn/monitoring-systems/blob/grafana/screens/telega_bot.jpg)
![grafana3-3](https://github.com/IthnHuitn/monitoring-systems/blob/grafana/screens/grafana3-2.png)
![grafana3-4](https://github.com/IthnHuitn/monitoring-systems/blob/grafana/screens/telega_bot2.jpg)

---

### Задание 4

[JSON_model](https://github.com/IthnHuitn/monitoring-systems/blob/grafana/dashboard_model.json)