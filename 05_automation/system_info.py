#!/usr/bin/env python3
"""
System Information - Comprehensive System Information Gathering Script

This script collects detailed system information including:
- Hardware specifications (CPU, Memory, Disk)
- Operating system details
- Network configuration
- Process information
- Performance metrics
- Security status

Author: Python Automation Examples
Date: 2025
"""

import platform
import psutil
import socket
import subprocess
import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse
import logging
import sys
import os


class SystemInfo:
    """
    A comprehensive system information collector.
    
    This class provides methods to gather various types of system information
    and export the data in different formats.
    """
    
    def __init__(self):
        """Initialize the SystemInfo collector."""
        self._setup_logging()
        self.info_cache = {}
    
    def _setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def get_basic_info(self) -> Dict[str, Any]:
        """
        Get basic system information.
        
        Returns:
            Dict containing basic system information
        """
        try:
            info = {
                'hostname': socket.gethostname(),
                'platform': platform.platform(),
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'architecture': platform.architecture(),
                'python_version': platform.python_version(),
                'python_implementation': platform.python_implementation(),
                'timestamp': datetime.now().isoformat(),
                'uptime': self._get_uptime()
            }
            
            self.logger.info("Basic system information collected")
            return info
            
        except Exception as e:
            self.logger.error(f"Error collecting basic info: {str(e)}")
            return {}
    
    def get_hardware_info(self) -> Dict[str, Any]:
        """
        Get hardware information.
        
        Returns:
            Dict containing hardware specifications
        """
        try:
            # CPU Information
            cpu_info = {
                'physical_cores': psutil.cpu_count(logical=False),
                'logical_cores': psutil.cpu_count(logical=True),
                'max_frequency': f"{psutil.cpu_freq().max:.2f} MHz" if psutil.cpu_freq() else "N/A",
                'min_frequency': f"{psutil.cpu_freq().min:.2f} MHz" if psutil.cpu_freq() else "N/A",
                'current_frequency': f"{psutil.cpu_freq().current:.2f} MHz" if psutil.cpu_freq() else "N/A",
                'usage_per_core': [f"{x:.1f}%" for x in psutil.cpu_percent(percpu=True, interval=1)],
                'total_usage': f"{psutil.cpu_percent(interval=1):.1f}%"
            }
            
            # Memory Information
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            memory_info = {
                'total': self._bytes_to_gb(memory.total),
                'available': self._bytes_to_gb(memory.available),
                'used': self._bytes_to_gb(memory.used),
                'percentage': f"{memory.percent:.1f}%",
                'swap_total': self._bytes_to_gb(swap.total),
                'swap_used': self._bytes_to_gb(swap.used),
                'swap_free': self._bytes_to_gb(swap.free),
                'swap_percentage': f"{swap.percent:.1f}%"
            }
            
            # Disk Information
            disk_info = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'filesystem': partition.fstype,
                        'total': self._bytes_to_gb(usage.total),
                        'used': self._bytes_to_gb(usage.used),
                        'free': self._bytes_to_gb(usage.free),
                        'percentage': f"{(usage.used / usage.total) * 100:.1f}%"
                    })
                except PermissionError:
                    # This can happen on Windows
                    continue
            
            # GPU Information (if available)
            gpu_info = self._get_gpu_info()
            
            hardware_info = {
                'cpu': cpu_info,
                'memory': memory_info,
                'disks': disk_info,
                'gpu': gpu_info
            }
            
            self.logger.info("Hardware information collected")
            return hardware_info
            
        except Exception as e:
            self.logger.error(f"Error collecting hardware info: {str(e)}")
            return {}
    
    def get_network_info(self) -> Dict[str, Any]:
        """
        Get network configuration and statistics.
        
        Returns:
            Dict containing network information
        """
        try:
            # Network interfaces
            interfaces = []
            for interface_name, interface_addresses in psutil.net_if_addrs().items():
                interface_info = {
                    'name': interface_name,
                    'addresses': []
                }
                
                for address in interface_addresses:
                    addr_info = {
                        'family': str(address.family),
                        'address': address.address,
                        'netmask': address.netmask,
                        'broadcast': address.broadcast
                    }
                    interface_info['addresses'].append(addr_info)
                
                # Get interface statistics if available
                if interface_name in psutil.net_if_stats():
                    stats = psutil.net_if_stats()[interface_name]
                    interface_info['stats'] = {
                        'is_up': stats.isup,
                        'duplex': str(stats.duplex),
                        'speed': f"{stats.speed} Mbps" if stats.speed > 0 else "Unknown",
                        'mtu': stats.mtu
                    }
                
                interfaces.append(interface_info)
            
            # Network IO statistics
            net_io = psutil.net_io_counters()
            io_stats = {
                'bytes_sent': self._bytes_to_mb(net_io.bytes_sent),
                'bytes_received': self._bytes_to_mb(net_io.bytes_recv),
                'packets_sent': net_io.packets_sent,
                'packets_received': net_io.packets_recv,
                'errors_in': net_io.errin,
                'errors_out': net_io.errout,
                'drops_in': net_io.dropin,
                'drops_out': net_io.dropout
            }
            
            # Active connections
            connections = []
            try:
                for conn in psutil.net_connections(kind='inet'):
                    if conn.status == 'ESTABLISHED':
                        connections.append({
                            'local_address': f"{conn.laddr.ip}:{conn.laddr.port}",
                            'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                            'status': conn.status,
                            'pid': conn.pid
                        })
            except (psutil.PermissionError, psutil.AccessDenied):
                connections = ["Permission denied - run as administrator for connection details"]
            
            network_info = {
                'interfaces': interfaces,
                'io_statistics': io_stats,
                'active_connections': connections[:10],  # Limit to first 10
                'total_connections': len(connections) if isinstance(connections, list) else 0
            }
            
            self.logger.info("Network information collected")
            return network_info
            
        except Exception as e:
            self.logger.error(f"Error collecting network info: {str(e)}")
            return {}
    
    def get_process_info(self, top_n: int = 10) -> Dict[str, Any]:
        """
        Get information about running processes.
        
        Args:
            top_n: Number of top processes to include by CPU/Memory usage
            
        Returns:
            Dict containing process information
        """
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    proc_info = proc.info
                    proc_info['memory_mb'] = f"{proc.memory_info().rss / 1024 / 1024:.1f} MB"
                    processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            # Sort by CPU usage
            processes_by_cpu = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            # Sort by Memory usage
            processes_by_memory = sorted(processes, key=lambda x: x['memory_percent'] or 0, reverse=True)
            
            process_info = {
                'total_processes': len(processes),
                'top_by_cpu': processes_by_cpu[:top_n],
                'top_by_memory': processes_by_memory[:top_n],
                'process_count_by_status': {}
            }
            
            # Count processes by status
            for proc in processes:
                status = proc.get('status', 'unknown')
                process_info['process_count_by_status'][status] = process_info['process_count_by_status'].get(status, 0) + 1
            
            self.logger.info("Process information collected")
            return process_info
            
        except Exception as e:
            self.logger.error(f"Error collecting process info: {str(e)}")
            return {}
    
    def get_security_info(self) -> Dict[str, Any]:
        """
        Get security-related system information.
        
        Returns:
            Dict containing security information
        """
        try:
            security_info = {
                'users': [],
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
                'login_sessions': []
            }
            
            # Get users
            for user in psutil.users():
                security_info['users'].append({
                    'name': user.name,
                    'terminal': user.terminal,
                    'host': user.host,
                    'started': datetime.fromtimestamp(user.started).isoformat()
                })
            
            # Windows-specific security info
            if platform.system() == 'Windows':
                try:
                    # Get Windows Defender status (requires admin privileges)
                    defender_info = self._get_windows_defender_status()
                    security_info['windows_defender'] = defender_info
                except Exception as e:
                    security_info['windows_defender'] = f"Could not retrieve: {str(e)}"
            
            # Check if firewall is enabled (basic check)
            security_info['firewall_info'] = self._check_firewall_status()
            
            self.logger.info("Security information collected")
            return security_info
            
        except Exception as e:
            self.logger.error(f"Error collecting security info: {str(e)}")
            return {}
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get current performance metrics.
        
        Returns:
            Dict containing performance metrics
        """
        try:
            # Get load averages (Unix-like systems)
            load_avg = None
            try:
                if hasattr(os, 'getloadavg'):
                    load_avg = os.getloadavg()
            except (AttributeError, OSError):
                load_avg = None
            
            # Disk I/O
            disk_io = psutil.disk_io_counters()
            
            performance_info = {
                'cpu_usage': {
                    'current': f"{psutil.cpu_percent(interval=1):.1f}%",
                    'per_core': [f"{x:.1f}%" for x in psutil.cpu_percent(percpu=True, interval=1)]
                },
                'memory_usage': {
                    'virtual': f"{psutil.virtual_memory().percent:.1f}%",
                    'swap': f"{psutil.swap_memory().percent:.1f}%"
                },
                'disk_io': {
                    'read_bytes': self._bytes_to_mb(disk_io.read_bytes),
                    'write_bytes': self._bytes_to_mb(disk_io.write_bytes),
                    'read_count': disk_io.read_count,
                    'write_count': disk_io.write_count
                } if disk_io else {},
                'load_average': list(load_avg) if load_avg else "Not available on this system",
                'temperature': self._get_temperature_info()
            }
            
            self.logger.info("Performance metrics collected")
            return performance_info
            
        except Exception as e:
            self.logger.error(f"Error collecting performance metrics: {str(e)}")
            return {}
    
    def get_all_info(self) -> Dict[str, Any]:
        """
        Get comprehensive system information.
        
        Returns:
            Dict containing all available system information
        """
        self.logger.info("Collecting comprehensive system information...")
        
        all_info = {
            'collection_time': datetime.now().isoformat(),
            'basic_info': self.get_basic_info(),
            'hardware_info': self.get_hardware_info(),
            'network_info': self.get_network_info(),
            'process_info': self.get_process_info(),
            'security_info': self.get_security_info(),
            'performance_metrics': self.get_performance_metrics()
        }
        
        self.logger.info("System information collection completed")
        return all_info
    
    def export_to_json(self, data: Dict[str, Any], filename: str):
        """Export system information to JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Data exported to {filename}")
        except Exception as e:
            self.logger.error(f"Error exporting to JSON: {str(e)}")
    
    def export_to_csv(self, data: Dict[str, Any], filename: str):
        """Export flattened system information to CSV file."""
        try:
            flattened_data = self._flatten_dict(data)
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Property', 'Value'])
                for key, value in flattened_data.items():
                    writer.writerow([key, str(value)])
            
            self.logger.info(f"Data exported to {filename}")
        except Exception as e:
            self.logger.error(f"Error exporting to CSV: {str(e)}")
    
    def create_html_report(self, data: Dict[str, Any], filename: str):
        """Create an HTML report of system information."""
        try:
            html_content = self._generate_html_report(data)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"HTML report created: {filename}")
        except Exception as e:
            self.logger.error(f"Error creating HTML report: {str(e)}")
    
    # Helper methods
    def _bytes_to_gb(self, bytes_value: int) -> str:
        """Convert bytes to GB."""
        return f"{bytes_value / (1024**3):.2f} GB"
    
    def _bytes_to_mb(self, bytes_value: int) -> str:
        """Convert bytes to MB."""
        return f"{bytes_value / (1024**2):.2f} MB"
    
    def _get_uptime(self) -> str:
        """Get system uptime."""
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{days} days, {hours} hours, {minutes} minutes"
        except Exception:
            return "Unknown"
    
    def _get_gpu_info(self) -> List[Dict[str, Any]]:
        """Get GPU information (requires additional libraries for detailed info)."""
        gpu_info = []
        try:
            # Basic GPU info - this is limited without specialized libraries
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["wmic", "path", "win32_VideoController", "get", "name"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')[1:]  # Skip header
                    for line in lines:
                        if line.strip():
                            gpu_info.append({"name": line.strip()})
        except Exception:
            gpu_info = [{"name": "Unable to detect GPU information"}]
        
        return gpu_info
    
    def _get_temperature_info(self) -> Dict[str, Any]:
        """Get temperature information if available."""
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                temp_info = {}
                for name, entries in temps.items():
                    temp_info[name] = []
                    for entry in entries:
                        temp_info[name].append({
                            'label': entry.label or 'N/A',
                            'current': f"{entry.current:.1f}°C",
                            'high': f"{entry.high:.1f}°C" if entry.high else 'N/A',
                            'critical': f"{entry.critical:.1f}°C" if entry.critical else 'N/A'
                        })
                return temp_info
        except Exception:
            pass
        return {"status": "Temperature sensors not available or accessible"}
    
    def _get_windows_defender_status(self) -> Dict[str, Any]:
        """Get Windows Defender status (Windows only)."""
        try:
            result = subprocess.run([
                "powershell", "-Command",
                "Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled, IoavProtectionEnabled, BehaviorMonitorEnabled | ConvertTo-Json"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception:
            pass
        return {"status": "Unable to retrieve Windows Defender status"}
    
    def _check_firewall_status(self) -> Dict[str, Any]:
        """Check basic firewall status."""
        firewall_info = {"status": "Unknown"}
        
        try:
            if platform.system() == "Windows":
                result = subprocess.run([
                    "netsh", "advfirewall", "show", "allprofiles", "state"
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    firewall_info = {"windows_firewall_output": result.stdout}
            
            elif platform.system() == "Linux":
                # Check for common Linux firewalls
                for firewall_cmd in [["ufw", "status"], ["firewall-cmd", "--state"], ["iptables", "-L"]]:
                    try:
                        result = subprocess.run(firewall_cmd, capture_output=True, text=True, timeout=10)
                        if result.returncode == 0:
                            firewall_info[firewall_cmd[0]] = result.stdout
                            break
                    except FileNotFoundError:
                        continue
        except Exception:
            pass
        
        return firewall_info
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
        """Flatten a nested dictionary."""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(self._flatten_dict(item, f"{new_key}[{i}]", sep=sep).items())
                    else:
                        items.append((f"{new_key}[{i}]", item))
            else:
                items.append((new_key, v))
        return dict(items)
    
    def _generate_html_report(self, data: Dict[str, Any]) -> str:
        """Generate HTML report from system data."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>System Information Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; }}
                h2 {{ color: #34495e; margin-top: 30px; }}
                .info-section {{ margin-bottom: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }}
                .metric {{ margin: 5px 0; }}
                .highlight {{ background-color: #e8f5e8; padding: 2px 5px; border-radius: 3px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>System Information Report</h1>
            <p><strong>Generated:</strong> {data.get('collection_time', 'Unknown')}</p>
        """
        
        # Add sections for each info category
        for section_name, section_data in data.items():
            if section_name != 'collection_time' and isinstance(section_data, dict):
                html += f"<div class='info-section'><h2>{section_name.replace('_', ' ').title()}</h2>"
                html += self._dict_to_html(section_data)
                html += "</div>"
        
        html += """
        </body>
        </html>
        """
        return html
    
    def _dict_to_html(self, data: Dict[str, Any], level: int = 0) -> str:
        """Convert dictionary to HTML representation."""
        html = ""
        indent = "  " * level
        
        for key, value in data.items():
            if isinstance(value, dict):
                html += f"{indent}<h{min(3 + level, 6)}>{key.replace('_', ' ').title()}</h{min(3 + level, 6)}>"
                html += self._dict_to_html(value, level + 1)
            elif isinstance(value, list):
                html += f"{indent}<h{min(3 + level, 6)}>{key.replace('_', ' ').title()}</h{min(3 + level, 6)}>"
                if value and isinstance(value[0], dict):
                    html += "<table><thead><tr>"
                    if value:
                        for header in value[0].keys():
                            html += f"<th>{header.replace('_', ' ').title()}</th>"
                    html += "</tr></thead><tbody>"
                    for item in value:
                        html += "<tr>"
                        for val in item.values():
                            html += f"<td>{str(val)}</td>"
                        html += "</tr>"
                    html += "</tbody></table>"
                else:
                    html += "<ul>"
                    for item in value:
                        html += f"<li>{str(item)}</li>"
                    html += "</ul>"
            else:
                html += f"{indent}<div class='metric'><strong>{key.replace('_', ' ').title()}:</strong> <span class='highlight'>{str(value)}</span></div>"
        
        return html


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Collect comprehensive system information')
    parser.add_argument('--output', '-o', help='Output filename (without extension)')
    parser.add_argument('--format', '-f', choices=['json', 'csv', 'html', 'all'], 
                       default='json', help='Output format')
    parser.add_argument('--section', '-s', 
                       choices=['basic', 'hardware', 'network', 'process', 'security', 'performance'],
                       help='Collect specific section only')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--processes', '-p', type=int, default=10, 
                       help='Number of top processes to include (default: 10)')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        system_info = SystemInfo()
        
        # Collect information based on section argument
        if args.section:
            section_methods = {
                'basic': system_info.get_basic_info,
                'hardware': system_info.get_hardware_info,
                'network': system_info.get_network_info,
                'process': lambda: system_info.get_process_info(args.processes),
                'security': system_info.get_security_info,
                'performance': system_info.get_performance_metrics
            }
            
            data = {args.section: section_methods[args.section]()}
        else:
            data = system_info.get_all_info()
        
        # Determine output filename
        if args.output:
            base_filename = args.output
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_filename = f'system_info_{timestamp}'
        
        # Export data
        if args.format == 'json' or args.format == 'all':
            system_info.export_to_json(data, f'{base_filename}.json')
        
        if args.format == 'csv' or args.format == 'all':
            system_info.export_to_csv(data, f'{base_filename}.csv')
        
        if args.format == 'html' or args.format == 'all':
            system_info.create_html_report(data, f'{base_filename}.html')
        
        # Print summary to console
        if not args.verbose:
            print("🖥️  System Information Summary:")
            print("=" * 40)
            
            if 'basic_info' in data:
                basic = data['basic_info']
                print(f"Hostname: {basic.get('hostname', 'Unknown')}")
                print(f"OS: {basic.get('platform', 'Unknown')}")
                print(f"Uptime: {basic.get('uptime', 'Unknown')}")
            
            if 'hardware_info' in data:
                hw = data['hardware_info']
                if 'cpu' in hw:
                    print(f"CPU Cores: {hw['cpu'].get('physical_cores', 'Unknown')}")
                    print(f"CPU Usage: {hw['cpu'].get('total_usage', 'Unknown')}")
                if 'memory' in hw:
                    print(f"Memory: {hw['memory'].get('used', 'Unknown')} / {hw['memory'].get('total', 'Unknown')}")
            
            print(f"\n✅ Report generated successfully!")
            if args.format == 'all':
                print(f"Files created: {base_filename}.json, {base_filename}.csv, {base_filename}.html")
            else:
                print(f"File created: {base_filename}.{args.format}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    """
    Usage Examples:
    
    1. Get all system information (JSON format):
       python system_info.py
    
    2. Get hardware information only:
       python system_info.py --section hardware
    
    3. Export to all formats:
       python system_info.py --format all --output my_system
    
    4. Get detailed process information:
       python system_info.py --section process --processes 20
    
    5. Verbose output with HTML report:
       python system_info.py --format html --verbose
    
    6. Quick network information check:
       python system_info.py --section network --format csv
    
    The script automatically detects the operating system and adapts its
    information gathering methods accordingly. Some features may require
    administrative privileges for full functionality.
    """
    exit(main())