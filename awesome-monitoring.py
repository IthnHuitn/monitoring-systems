#!/usr/bin/env python3
"""
Скрипт для сбора системных метрик и записи их в JSON-лог.
Запускается каждую минуту через cron.
"""

import json
import os
import time
from datetime import datetime


def get_cpu_usage():
    """Получает загрузку CPU из /proc/stat"""
    try:
        with open('/proc/stat', 'r') as f:
            first_line = f.readline().strip()
        
        # Разбираем первую строку (cpu total)
        fields = first_line.split()
        if fields[0] != 'cpu':
            return None
        
        # Рассчитываем загрузку по разнице между вызовами
        cpu_stats_file = '/tmp/cpu_stats.json'
        
        # Текущие значения
        user, nice, system, idle = map(int, fields[1:5])
        total = user + nice + system + idle
        idle_time = idle
        total_time = total
        
        # Если есть предыдущие значения, вычисляем процент
        if os.path.exists(cpu_stats_file):
            with open(cpu_stats_file, 'r') as f:
                prev = json.load(f)
            
            total_diff = total_time - prev['total_time']
            idle_diff = idle_time - prev['idle_time']
            
            if total_diff > 0:
                cpu_percent = 100.0 * (total_diff - idle_diff) / total_diff
            else:
                cpu_percent = 0.0
        else:
            cpu_percent = 0.0
        
        # Сохраняем текущие значения для следующего замера
        with open(cpu_stats_file, 'w') as f:
            json.dump({'total_time': total_time, 'idle_time': idle_time}, f)
        
        return round(cpu_percent, 2)
    
    except Exception as e:
        print(f"Error getting CPU usage: {e}")
        return None


def get_memory_usage():
    """Получает информацию о памяти из /proc/meminfo"""
    try:
        meminfo = {}
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = int(parts[1].strip().split()[0])
                    meminfo[key] = value
        
        total = meminfo.get('MemTotal', 0)
        available = meminfo.get('MemAvailable', 0)
        used = total - available
        percent_used = (used / total * 100) if total > 0 else 0
        
        return {
            'total_kb': total,
            'used_kb': used,
            'available_kb': available,
            'percent_used': round(percent_used, 2)
        }
    
    except Exception as e:
        print(f"Error getting memory info: {e}")
        return None


def get_disk_usage():
    """Получает информацию о дисковом пространстве через statvfs"""
    try:
        stat = os.statvfs('/')
        
        total = stat.f_blocks * stat.f_frsize
        available = stat.f_bavail * stat.f_frsize
        used = total - available
        percent_used = (used / total * 100) if total > 0 else 0
        
        return {
            'total_bytes': total,
            'used_bytes': used,
            'available_bytes': available,
            'percent_used': round(percent_used, 2)
        }
    
    except Exception as e:
        print(f"Error getting disk usage: {e}")
        return None


def get_load_average():
    """Получает Load Average из /proc/loadavg"""
    try:
        with open('/proc/loadavg', 'r') as f:
            content = f.read().strip()
        
        parts = content.split()
        return {
            'load_1min': float(parts[0]),
            'load_5min': float(parts[1]),
            'load_15min': float(parts[2]),
            'running_tasks': int(parts[3].split('/')[0]),
            'total_tasks': int(parts[3].split('/')[1])
        }
    
    except Exception as e:
        print(f"Error getting load average: {e}")
        return None


def get_network_stats():
    """Получает сетевую статистику из /proc/net/dev"""
    try:
        # Файл для хранения предыдущих значений
        net_stats_file = '/tmp/net_stats.json'
        
        current_stats = {}
        with open('/proc/net/dev', 'r') as f:
            # Пропускаем первые две строки (заголовки)
            lines = f.readlines()[2:]
            
            for line in lines:
                parts = line.strip().split()
                interface = parts[0].rstrip(':')
                
                # Пропускаем lo интерфейс
                if interface == 'lo':
                    continue
                
                rx_bytes = int(parts[1])
                tx_bytes = int(parts[9])
                
                current_stats[interface] = {
                    'rx_bytes': rx_bytes,
                    'tx_bytes': tx_bytes
                }
        
        # Рассчитываем скорость передачи
        if os.path.exists(net_stats_file):
            with open(net_stats_file, 'r') as f:
                prev_stats = json.load(f)
            
            total_rx_rate = 0
            total_tx_rate = 0
            
            for iface, stats in current_stats.items():
                if iface in prev_stats:
                    # Разница за минуту (скрипт запускается раз в минуту)
                    rx_diff = stats['rx_bytes'] - prev_stats[iface]['rx_bytes']
                    tx_diff = stats['tx_bytes'] - prev_stats[iface]['tx_bytes']
                    total_rx_rate += rx_diff
                    total_tx_rate += tx_diff
            
            net_info = {
                'rx_bytes_per_sec': round(total_rx_rate / 60, 2),
                'tx_bytes_per_sec': round(total_tx_rate / 60, 2),
                'rx_kbps': round(total_rx_rate / 60 / 1024, 2),
                'tx_kbps': round(total_tx_rate / 60 / 1024, 2)
            }
        else:
            net_info = {
                'rx_bytes_per_sec': 0,
                'tx_bytes_per_sec': 0,
                'rx_kbps': 0,
                'tx_kbps': 0
            }
        
        # Сохраняем текущие значения
        with open(net_stats_file, 'w') as f:
            json.dump(current_stats, f)
        
        return net_info
    
    except Exception as e:
        print(f"Error getting network stats: {e}")
        return None


def collect_metrics():
    """Собирает все метрики и возвращает их в виде словаря"""
    timestamp = int(time.time())
    
    metrics = {
        'timestamp': timestamp,
        'datetime': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
        'cpu_percent': get_cpu_usage(),
        'memory': get_memory_usage(),
        'disk': get_disk_usage(),
        'load_average': get_load_average(),
        'network': get_network_stats()
    }
    
    return metrics


def write_metrics_to_log(metrics):
    """Записывает метрики в лог-файл"""
    log_dir = '/var/log'
    log_file = datetime.now().strftime('%y-%m-%d') + '-awesome-monitoring.log'
    log_path = os.path.join(log_dir, log_file)
    
    # Создаём директорию, если её нет
    os.makedirs(log_dir, exist_ok=True)
    
    # Записываем JSON-строку в файл
    try:
        with open(log_path, 'a') as f:
            json.dump(metrics, f)
            f.write('\n')
        print(f"Metrics written to {log_path}")
    except PermissionError:
        # Если нет прав на запись в /var/log, пишем в текущую директорию
        fallback_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), log_file)
        with open(fallback_path, 'a') as f:
            json.dump(metrics, f)
            f.write('\n')
        print(f"Metrics written to {fallback_path} (fallback location)")


def main():
    """Основная функция"""
    print(f"Collecting metrics at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    metrics = collect_metrics()
    write_metrics_to_log(metrics)
    print("Metrics collection completed successfully")


if __name__ == '__main__':
    main()