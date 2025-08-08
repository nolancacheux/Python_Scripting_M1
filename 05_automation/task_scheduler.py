#!/usr/bin/env python3
"""
Task Scheduler - Advanced Task Scheduling and Automation Script

This script provides comprehensive task scheduling capabilities including:
- Cron-like scheduling with human-readable syntax
- One-time and recurring tasks
- Task persistence and recovery
- Email notifications
- Task dependency management
- Web endpoint monitoring
- File system watching
- System resource monitoring

Author: Python Automation Examples
Date: 2025
"""

import schedule
import threading
import time
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Callable, Any, Optional
import subprocess
import argparse
import signal
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sqlite3
from dataclasses import dataclass, asdict
from enum import Enum


class TaskStatus(Enum):
    """Task execution status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"


@dataclass
class TaskResult:
    """Task execution result."""
    task_id: str
    status: TaskStatus
    start_time: datetime
    end_time: Optional[datetime]
    output: str
    error: Optional[str]
    execution_time: float


class Task:
    """
    Represents a schedulable task with various execution options.
    
    Attributes:
        task_id (str): Unique identifier for the task
        name (str): Human-readable task name
        command (str): Command or function to execute
        schedule_expr (str): Schedule expression (cron-like or human readable)
        enabled (bool): Whether the task is active
        max_retries (int): Maximum retry attempts on failure
        timeout (int): Task timeout in seconds
        dependencies (List[str]): List of task IDs this task depends on
        notify_on_success (bool): Send notification on successful completion
        notify_on_failure (bool): Send notification on failure
        last_run (Optional[datetime]): Last execution time
        next_run (Optional[datetime]): Next scheduled execution time
    """
    
    def __init__(self, task_id: str, name: str, command: str, schedule_expr: str,
                 enabled: bool = True, max_retries: int = 0, timeout: int = 300,
                 dependencies: List[str] = None, notify_on_success: bool = False,
                 notify_on_failure: bool = True):
        self.task_id = task_id
        self.name = name
        self.command = command
        self.schedule_expr = schedule_expr
        self.enabled = enabled
        self.max_retries = max_retries
        self.timeout = timeout
        self.dependencies = dependencies or []
        self.notify_on_success = notify_on_success
        self.notify_on_failure = notify_on_failure
        self.last_run: Optional[datetime] = None
        self.next_run: Optional[datetime] = None
        self.retry_count = 0
        self.is_running = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for serialization."""
        return {
            'task_id': self.task_id,
            'name': self.name,
            'command': self.command,
            'schedule_expr': self.schedule_expr,
            'enabled': self.enabled,
            'max_retries': self.max_retries,
            'timeout': self.timeout,
            'dependencies': self.dependencies,
            'notify_on_success': self.notify_on_success,
            'notify_on_failure': self.notify_on_failure,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create task from dictionary."""
        task = cls(
            task_id=data['task_id'],
            name=data['name'],
            command=data['command'],
            schedule_expr=data['schedule_expr'],
            enabled=data.get('enabled', True),
            max_retries=data.get('max_retries', 0),
            timeout=data.get('timeout', 300),
            dependencies=data.get('dependencies', []),
            notify_on_success=data.get('notify_on_success', False),
            notify_on_failure=data.get('notify_on_failure', True)
        )
        
        if data.get('last_run'):
            task.last_run = datetime.fromisoformat(data['last_run'])
        if data.get('next_run'):
            task.next_run = datetime.fromisoformat(data['next_run'])
        
        return task


class FileWatcher(FileSystemEventHandler):
    """File system event handler for monitoring file changes."""
    
    def __init__(self, scheduler: 'TaskScheduler', task_id: str):
        self.scheduler = scheduler
        self.task_id = task_id
        
    def on_modified(self, event):
        if not event.is_directory:
            self.scheduler.logger.info(f"File changed: {event.src_path}, triggering task {self.task_id}")
            self.scheduler.run_task_immediately(self.task_id)


class TaskScheduler:
    """
    Advanced task scheduler with persistence and monitoring capabilities.
    
    Features:
    - Cron-like and human-readable scheduling
    - Task dependencies
    - Email notifications
    - Web endpoint monitoring
    - File system monitoring
    - Task persistence
    - Resource monitoring
    """
    
    def __init__(self, config_file: str = "scheduler_config.json",
                 db_file: str = "scheduler.db"):
        """
        Initialize the TaskScheduler.
        
        Args:
            config_file: Path to configuration file
            db_file: Path to SQLite database file
        """
        self.config_file = config_file
        self.db_file = db_file
        self.tasks: Dict[str, Task] = {}
        self.running = False
        self.scheduler_thread = None
        self.file_observers = {}
        self.config = {}
        
        self._setup_logging()
        self._setup_database()
        self._load_config()
        self._load_tasks()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('task_scheduler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _setup_database(self):
        """Setup SQLite database for task history."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT,
                status TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                output TEXT,
                error TEXT,
                execution_time REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_config(self):
        """Load configuration from file."""
        if Path(self.config_file).exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                self.logger.info(f"Configuration loaded from {self.config_file}")
            except Exception as e:
                self.logger.error(f"Error loading config: {str(e)}")
                self.config = {}
        else:
            # Create default configuration
            self.config = {
                "email": {
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "username": "",
                    "password": "",
                    "use_tls": True
                },
                "monitoring": {
                    "cpu_threshold": 80,
                    "memory_threshold": 80,
                    "disk_threshold": 90
                },
                "general": {
                    "max_concurrent_tasks": 5,
                    "task_timeout": 300,
                    "cleanup_days": 30
                }
            }
            self._save_config()
    
    def _save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving config: {str(e)}")
    
    def _load_tasks(self):
        """Load tasks from configuration."""
        tasks_file = "tasks.json"
        if Path(tasks_file).exists():
            try:
                with open(tasks_file, 'r') as f:
                    tasks_data = json.load(f)
                
                for task_data in tasks_data:
                    task = Task.from_dict(task_data)
                    self.tasks[task.task_id] = task
                    self._schedule_task(task)
                
                self.logger.info(f"Loaded {len(self.tasks)} tasks")
            except Exception as e:
                self.logger.error(f"Error loading tasks: {str(e)}")
    
    def _save_tasks(self):
        """Save tasks to file."""
        try:
            tasks_data = [task.to_dict() for task in self.tasks.values()]
            with open("tasks.json", 'w') as f:
                json.dump(tasks_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving tasks: {str(e)}")
    
    def _signal_handler(self, signum, frame):
        """Handle system signals for graceful shutdown."""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.stop()
        sys.exit(0)
    
    def add_task(self, task: Task) -> bool:
        """
        Add a new task to the scheduler.
        
        Args:
            task: Task object to add
            
        Returns:
            bool: True if task was added successfully
        """
        try:
            if task.task_id in self.tasks:
                self.logger.warning(f"Task {task.task_id} already exists, updating...")
            
            self.tasks[task.task_id] = task
            self._schedule_task(task)
            self._save_tasks()
            
            self.logger.info(f"Added task: {task.name} ({task.task_id})")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding task {task.task_id}: {str(e)}")
            return False
    
    def remove_task(self, task_id: str) -> bool:
        """
        Remove a task from the scheduler.
        
        Args:
            task_id: ID of task to remove
            
        Returns:
            bool: True if task was removed successfully
        """
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                
                # Cancel scheduled job
                schedule.clear(task_id)
                
                # Stop file watcher if exists
                if task_id in self.file_observers:
                    self.file_observers[task_id].stop()
                    del self.file_observers[task_id]
                
                # Remove from tasks
                del self.tasks[task_id]
                self._save_tasks()
                
                self.logger.info(f"Removed task: {task.name} ({task_id})")
                return True
            else:
                self.logger.warning(f"Task {task_id} not found")
                return False
                
        except Exception as e:
            self.logger.error(f"Error removing task {task_id}: {str(e)}")
            return False
    
    def _schedule_task(self, task: Task):
        """Schedule a task based on its schedule expression."""
        if not task.enabled:
            return
        
        try:
            # Parse schedule expression
            expr = task.schedule_expr.lower().strip()
            
            # Handle different schedule formats
            if expr.startswith('every'):
                self._parse_every_expression(task, expr)
            elif expr.startswith('at'):
                self._parse_at_expression(task, expr)
            elif expr.startswith('cron:'):
                self._parse_cron_expression(task, expr[5:].strip())
            elif expr == 'on_file_change':
                self._setup_file_watcher(task)
            elif expr.startswith('on_url_change'):
                self._setup_url_monitor(task, expr)
            elif expr == 'on_resource_threshold':
                self._setup_resource_monitor(task)
            else:
                self.logger.warning(f"Unknown schedule expression for task {task.task_id}: {expr}")
                
        except Exception as e:
            self.logger.error(f"Error scheduling task {task.task_id}: {str(e)}")
    
    def _parse_every_expression(self, task: Task, expr: str):
        """Parse 'every' schedule expressions."""
        # Examples: "every 5 minutes", "every hour", "every day at 09:00"
        parts = expr.split()
        
        if "minute" in expr:
            if len(parts) >= 3 and parts[1].isdigit():
                interval = int(parts[1])
                schedule.every(interval).minutes.do(self._execute_task_wrapper, task).tag(task.task_id)
            else:
                schedule.every().minute.do(self._execute_task_wrapper, task).tag(task.task_id)
        
        elif "hour" in expr:
            if "at" in expr:
                time_part = expr.split("at")[1].strip()
                schedule.every().hour.at(time_part).do(self._execute_task_wrapper, task).tag(task.task_id)
            elif len(parts) >= 3 and parts[1].isdigit():
                interval = int(parts[1])
                schedule.every(interval).hours.do(self._execute_task_wrapper, task).tag(task.task_id)
            else:
                schedule.every().hour.do(self._execute_task_wrapper, task).tag(task.task_id)
        
        elif "day" in expr:
            if "at" in expr:
                time_part = expr.split("at")[1].strip()
                schedule.every().day.at(time_part).do(self._execute_task_wrapper, task).tag(task.task_id)
            else:
                schedule.every().day.do(self._execute_task_wrapper, task).tag(task.task_id)
        
        elif "week" in expr:
            if len(parts) >= 3 and parts[1].isdigit():
                interval = int(parts[1])
                schedule.every(interval).weeks.do(self._execute_task_wrapper, task).tag(task.task_id)
            else:
                schedule.every().week.do(self._execute_task_wrapper, task).tag(task.task_id)
        
        # Handle specific days
        elif "monday" in expr:
            time_part = expr.split("at")[1].strip() if "at" in expr else "09:00"
            schedule.every().monday.at(time_part).do(self._execute_task_wrapper, task).tag(task.task_id)
        elif "tuesday" in expr:
            time_part = expr.split("at")[1].strip() if "at" in expr else "09:00"
            schedule.every().tuesday.at(time_part).do(self._execute_task_wrapper, task).tag(task.task_id)
        # ... continue for other days
    
    def _parse_at_expression(self, task: Task, expr: str):
        """Parse 'at' schedule expressions."""
        # Examples: "at 09:00", "at 14:30 daily"
        time_part = expr.replace("at", "").strip()
        
        if "daily" in time_part:
            time_str = time_part.replace("daily", "").strip()
            schedule.every().day.at(time_str).do(self._execute_task_wrapper, task).tag(task.task_id)
        else:
            schedule.every().day.at(time_part).do(self._execute_task_wrapper, task).tag(task.task_id)
    
    def _parse_cron_expression(self, task: Task, cron_expr: str):
        """Parse cron expressions (basic implementation)."""
        # This is a simplified cron parser - for production use, consider using croniter
        self.logger.warning(f"Cron expressions require additional implementation for task {task.task_id}")
        # For now, schedule as daily
        schedule.every().day.do(self._execute_task_wrapper, task).tag(task.task_id)
    
    def _setup_file_watcher(self, task: Task):
        """Setup file system watcher for a task."""
        # Extract file path from task command (assuming format like "watch:/path/to/file")
        if "watch:" in task.command:
            watch_path = task.command.split("watch:")[1].strip()
            
            event_handler = FileWatcher(self, task.task_id)
            observer = Observer()
            observer.schedule(event_handler, watch_path, recursive=False)
            observer.start()
            
            self.file_observers[task.task_id] = observer
            self.logger.info(f"File watcher setup for {task.task_id} on {watch_path}")
    
    def _setup_url_monitor(self, task: Task, expr: str):
        """Setup URL monitoring for a task."""
        # Extract URL from expression
        url = expr.replace("on_url_change:", "").strip()
        
        def check_url():
            try:
                response = requests.get(url, timeout=30)
                # Simple change detection based on content hash
                content_hash = hash(response.text)
                
                # Store previous hash (simplified - should use persistent storage)
                if not hasattr(task, '_last_url_hash'):
                    task._last_url_hash = content_hash
                    return
                
                if content_hash != task._last_url_hash:
                    task._last_url_hash = content_hash
                    self.run_task_immediately(task.task_id)
                    
            except Exception as e:
                self.logger.error(f"Error checking URL {url}: {str(e)}")
        
        # Check every 5 minutes
        schedule.every(5).minutes.do(check_url).tag(f"{task.task_id}_url_monitor")
    
    def _setup_resource_monitor(self, task: Task):
        """Setup system resource monitoring for a task."""
        def check_resources():
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent
            
            config = self.config.get('monitoring', {})
            cpu_threshold = config.get('cpu_threshold', 80)
            memory_threshold = config.get('memory_threshold', 80)
            disk_threshold = config.get('disk_threshold', 90)
            
            if (cpu_percent > cpu_threshold or 
                memory_percent > memory_threshold or 
                disk_percent > disk_threshold):
                
                self.run_task_immediately(task.task_id)
        
        # Check every minute
        schedule.every().minute.do(check_resources).tag(f"{task.task_id}_resource_monitor")
    
    def _execute_task_wrapper(self, task: Task):
        """Wrapper function for task execution."""
        if task.is_running:
            self.logger.warning(f"Task {task.task_id} is already running, skipping")
            return
        
        # Check dependencies
        if not self._check_dependencies(task):
            self.logger.info(f"Dependencies not met for task {task.task_id}, skipping")
            return
        
        self._execute_task(task)
    
    def _check_dependencies(self, task: Task) -> bool:
        """Check if task dependencies are satisfied."""
        for dep_id in task.dependencies:
            if dep_id not in self.tasks:
                self.logger.error(f"Dependency {dep_id} not found for task {task.task_id}")
                return False
            
            dep_task = self.tasks[dep_id]
            
            # Check if dependency ran successfully in the last 24 hours
            if (not dep_task.last_run or 
                datetime.now() - dep_task.last_run > timedelta(hours=24)):
                return False
        
        return True
    
    def _execute_task(self, task: Task):
        """Execute a task."""
        task.is_running = True
        start_time = datetime.now()
        result = TaskResult(
            task_id=task.task_id,
            status=TaskStatus.RUNNING,
            start_time=start_time,
            end_time=None,
            output="",
            error=None,
            execution_time=0.0
        )
        
        self.logger.info(f"Executing task: {task.name} ({task.task_id})")
        
        try:
            # Execute command
            if task.command.startswith('python:'):
                # Execute Python function
                func_name = task.command[7:]
                output = self._execute_python_function(func_name)
            elif task.command.startswith('http:') or task.command.startswith('https:'):
                # Execute HTTP request
                output = self._execute_http_request(task.command)
            else:
                # Execute shell command
                process = subprocess.Popen(
                    task.command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                try:
                    output, error = process.communicate(timeout=task.timeout)
                    
                    if process.returncode == 0:
                        result.status = TaskStatus.COMPLETED
                        result.output = output
                        self.logger.info(f"Task {task.task_id} completed successfully")
                    else:
                        result.status = TaskStatus.FAILED
                        result.error = error
                        self.logger.error(f"Task {task.task_id} failed with return code {process.returncode}")
                        
                except subprocess.TimeoutExpired:
                    process.kill()
                    result.status = TaskStatus.FAILED
                    result.error = f"Task timed out after {task.timeout} seconds"
                    self.logger.error(f"Task {task.task_id} timed out")
            
            # Update task information
            task.last_run = start_time
            task.retry_count = 0
            
        except Exception as e:
            result.status = TaskStatus.FAILED
            result.error = str(e)
            self.logger.error(f"Error executing task {task.task_id}: {str(e)}")
        
        finally:
            end_time = datetime.now()
            result.end_time = end_time
            result.execution_time = (end_time - start_time).total_seconds()
            task.is_running = False
            
            # Save result to database
            self._save_task_result(result)
            
            # Send notifications
            self._send_notifications(task, result)
            
            # Handle retries
            if result.status == TaskStatus.FAILED and task.retry_count < task.max_retries:
                task.retry_count += 1
                self.logger.info(f"Retrying task {task.task_id} (attempt {task.retry_count}/{task.max_retries})")
                threading.Timer(60, self._execute_task, args=[task]).start()  # Retry after 1 minute
    
    def _execute_python_function(self, func_name: str) -> str:
        """Execute a Python function by name."""
        # This is a simplified implementation
        # In practice, you'd want to import and execute actual functions
        return f"Executed Python function: {func_name}"
    
    def _execute_http_request(self, url: str) -> str:
        """Execute an HTTP request."""
        try:
            response = requests.get(url, timeout=30)
            return f"HTTP {response.status_code}: {response.text[:200]}..."
        except Exception as e:
            raise Exception(f"HTTP request failed: {str(e)}")
    
    def _save_task_result(self, result: TaskResult):
        """Save task result to database."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO task_history 
                (task_id, status, start_time, end_time, output, error, execution_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                result.task_id,
                result.status.value,
                result.start_time.isoformat(),
                result.end_time.isoformat() if result.end_time else None,
                result.output,
                result.error,
                result.execution_time
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Error saving task result: {str(e)}")
    
    def _send_notifications(self, task: Task, result: TaskResult):
        """Send email notifications based on task settings."""
        should_notify = (
            (result.status == TaskStatus.COMPLETED and task.notify_on_success) or
            (result.status == TaskStatus.FAILED and task.notify_on_failure)
        )
        
        if not should_notify:
            return
        
        email_config = self.config.get('email', {})
        if not email_config.get('username') or not email_config.get('password'):
            return
        
        try:
            subject = f"Task {result.status.value.title()}: {task.name}"
            body = f"""
Task: {task.name} ({task.task_id})
Status: {result.status.value.title()}
Start Time: {result.start_time}
End Time: {result.end_time}
Execution Time: {result.execution_time:.2f} seconds

Output:
{result.output}

{f"Error: {result.error}" if result.error else ""}
"""
            
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = email_config['username']
            msg['To'] = email_config.get('notification_email', email_config['username'])
            
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                if email_config.get('use_tls', True):
                    server.starttls()
                server.login(email_config['username'], email_config['password'])
                server.send_message(msg)
            
            self.logger.info(f"Notification sent for task {task.task_id}")
            
        except Exception as e:
            self.logger.error(f"Error sending notification: {str(e)}")
    
    def run_task_immediately(self, task_id: str) -> bool:
        """
        Run a task immediately, bypassing the schedule.
        
        Args:
            task_id: ID of task to run
            
        Returns:
            bool: True if task was started successfully
        """
        if task_id not in self.tasks:
            self.logger.error(f"Task {task_id} not found")
            return False
        
        task = self.tasks[task_id]
        threading.Thread(target=self._execute_task, args=[task], daemon=True).start()
        return True
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get current status of a task."""
        if task_id not in self.tasks:
            return {"error": f"Task {task_id} not found"}
        
        task = self.tasks[task_id]
        
        # Get recent executions from database
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT status, start_time, end_time, execution_time
            FROM task_history
            WHERE task_id = ?
            ORDER BY start_time DESC
            LIMIT 5
        ''', (task_id,))
        
        recent_runs = cursor.fetchall()
        conn.close()
        
        return {
            "task": task.to_dict(),
            "is_running": task.is_running,
            "recent_runs": [
                {
                    "status": row[0],
                    "start_time": row[1],
                    "end_time": row[2],
                    "execution_time": row[3]
                }
                for row in recent_runs
            ]
        }
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks with their basic information."""
        return [
            {
                "task_id": task.task_id,
                "name": task.name,
                "schedule": task.schedule_expr,
                "enabled": task.enabled,
                "is_running": task.is_running,
                "last_run": task.last_run.isoformat() if task.last_run else None
            }
            for task in self.tasks.values()
        ]
    
    def start(self):
        """Start the task scheduler."""
        if self.running:
            self.logger.warning("Scheduler is already running")
            return
        
        self.running = True
        self.logger.info("Starting task scheduler...")
        
        def run_scheduler():
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        
        self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        self.logger.info(f"Task scheduler started with {len(self.tasks)} tasks")
    
    def stop(self):
        """Stop the task scheduler."""
        self.running = False
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        # Stop file observers
        for observer in self.file_observers.values():
            observer.stop()
            observer.join()
        
        self.logger.info("Task scheduler stopped")
    
    def cleanup_old_records(self, days: int = 30):
        """Clean up old task execution records."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM task_history
                WHERE start_time < ?
            ''', (cutoff_date.isoformat(),))
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            self.logger.info(f"Cleaned up {deleted_count} old task records")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up old records: {str(e)}")


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(description='Advanced Task Scheduler')
    parser.add_argument('--config', '-c', default='scheduler_config.json',
                       help='Configuration file path')
    parser.add_argument('--daemon', '-d', action='store_true',
                       help='Run as daemon (background process)')
    parser.add_argument('--add-task', help='Add a new task (JSON format)')
    parser.add_argument('--list-tasks', action='store_true',
                       help='List all tasks')
    parser.add_argument('--run-task', help='Run a specific task immediately')
    parser.add_argument('--status', help='Get status of a specific task')
    parser.add_argument('--remove-task', help='Remove a task')
    parser.add_argument('--cleanup', type=int, metavar='DAYS',
                       help='Clean up old records older than DAYS')
    
    args = parser.parse_args()
    
    try:
        scheduler = TaskScheduler(config_file=args.config)
        
        if args.add_task:
            # Parse task JSON and add
            task_data = json.loads(args.add_task)
            task = Task.from_dict(task_data)
            success = scheduler.add_task(task)
            print(f"Task {'added' if success else 'failed to add'}: {task.name}")
            return 0 if success else 1
        
        elif args.list_tasks:
            tasks = scheduler.list_tasks()
            print(f"\n📋 {len(tasks)} Tasks:")
            print("=" * 50)
            for task in tasks:
                status = "🟢 Running" if task['is_running'] else "⭕ Idle"
                enabled = "✅" if task['enabled'] else "❌"
                print(f"{enabled} {task['name']} ({task['task_id']})")
                print(f"   Schedule: {task['schedule']}")
                print(f"   Status: {status}")
                print(f"   Last Run: {task['last_run'] or 'Never'}")
                print()
            return 0
        
        elif args.run_task:
            success = scheduler.run_task_immediately(args.run_task)
            print(f"Task {'started' if success else 'failed to start'}")
            return 0 if success else 1
        
        elif args.status:
            status = scheduler.get_task_status(args.status)
            print(json.dumps(status, indent=2))
            return 0
        
        elif args.remove_task:
            success = scheduler.remove_task(args.remove_task)
            print(f"Task {'removed' if success else 'not found'}")
            return 0 if success else 1
        
        elif args.cleanup:
            scheduler.cleanup_old_records(args.cleanup)
            return 0
        
        else:
            # Start scheduler
            scheduler.start()
            
            if args.daemon:
                print("Task scheduler running in background...")
                print("Press Ctrl+C to stop")
                
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    pass
            else:
                print("Task scheduler started. Press Enter to stop...")
                input()
            
            scheduler.stop()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    """
    Usage Examples:
    
    1. Start the scheduler interactively:
       python task_scheduler.py
    
    2. Run as daemon:
       python task_scheduler.py --daemon
    
    3. Add a new task:
       python task_scheduler.py --add-task '{"task_id": "backup", "name": "Daily Backup", "command": "rsync -av /home/user/ /backup/", "schedule_expr": "every day at 02:00"}'
    
    4. List all tasks:
       python task_scheduler.py --list-tasks
    
    5. Run a task immediately:
       python task_scheduler.py --run-task backup
    
    6. Get task status:
       python task_scheduler.py --status backup
    
    7. Remove a task:
       python task_scheduler.py --remove-task backup
    
    8. Clean up old records:
       python task_scheduler.py --cleanup 30
    
    Task Schedule Expression Examples:
    - "every 5 minutes"
    - "every hour at :30"
    - "every day at 09:00"
    - "every monday at 08:00"
    - "at 14:30 daily"
    - "cron: 0 */6 * * *"
    - "on_file_change"
    - "on_url_change: https://example.com/api/status"
    - "on_resource_threshold"
    
    Task Command Examples:
    - "python /path/to/script.py"
    - "rsync -av /source/ /dest/"
    - "python: my_function"
    - "https://api.example.com/webhook"
    - "watch: /path/to/watch"
    """
    exit(main())