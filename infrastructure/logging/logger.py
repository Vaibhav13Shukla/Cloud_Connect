import os
from datetime import datetime
from typing import List


class Logger:
    def __init__(self, log_directory: str = "logs"):
        self._log_directory = log_directory
        self._ensure_log_directory()
    
    def _ensure_log_directory(self) -> None:
        if not os.path.exists(self._log_directory):
            os.makedirs(self._log_directory)
    
    def log(self, resource_type: str, message: str) -> None:
        timestamp = datetime.now().strftime("%I:%M %p")
        log_entry = f"[{timestamp}] {message}"
        
        print(log_entry)
        
        log_file = os.path.join(self._log_directory, f"{resource_type.lower()}.log")
        with open(log_file, 'a') as f:
            f.write(log_entry + '\n')
    
    def get_logs(self, limit: int = 20) -> List[str]:
        logs = []
        if not os.path.exists(self._log_directory):
            return logs
        
        for filename in os.listdir(self._log_directory):
            if filename.endswith('.log'):
                filepath = os.path.join(self._log_directory, filename)
                with open(filepath, 'r') as f:
                    logs.extend(f.readlines())
        
        return logs[-limit:] if logs else []