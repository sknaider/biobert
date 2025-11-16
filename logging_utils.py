# coding=utf-8
# Copyright DMIS Lab. BioBERT Authors. http://dmis.korea.ac.kr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Structured logging utilities for BioBERT."""

import json
import logging
import sys
from typing import Any, Dict, Optional


class StructuredLogger:
    """Structured logger with JSON output support for enterprise logging."""

    def __init__(self, name: str, level: int = logging.INFO, json_output: bool = False):
        """Initialize structured logger.

        Args:
            name: Logger name (typically __name__)
            level: Logging level (default: INFO)
            json_output: Whether to output JSON formatted logs (default: False)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.json_output = json_output

        # Remove existing handlers to avoid duplicates
        self.logger.handlers = []

        # Create handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        # Set formatter based on output type
        if json_output:
            formatter = JsonFormatter()
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message with optional structured data."""
        if self.json_output and kwargs:
            self.logger.info(json.dumps({'message': message, **kwargs}))
        else:
            self.logger.info(message)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message with optional structured data."""
        if self.json_output and kwargs:
            self.logger.warning(json.dumps({'message': message, **kwargs}))
        else:
            self.logger.warning(message)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message with optional structured data."""
        if self.json_output and kwargs:
            self.logger.error(json.dumps({'message': message, **kwargs}))
        else:
            self.logger.error(message)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message with optional structured data."""
        if self.json_output and kwargs:
            self.logger.debug(json.dumps({'message': message, **kwargs}))
        else:
            self.logger.debug(message)


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON.

        Args:
            record: Log record to format

        Returns:
            JSON formatted log string
        """
        log_data: Dict[str, Any] = {
            'timestamp': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_data.update(record.extra_fields)

        return json.dumps(log_data)


def get_logger(
    name: str,
    level: Optional[int] = None,
    json_output: bool = False
) -> StructuredLogger:
    """Get or create a structured logger.

    Args:
        name: Logger name (typically __name__)
        level: Logging level (default: INFO)
        json_output: Whether to output JSON formatted logs

    Returns:
        Configured StructuredLogger instance
    """
    if level is None:
        level = logging.INFO

    return StructuredLogger(name, level, json_output)


def log_training_params(logger: StructuredLogger, params: Dict[str, Any]) -> None:
    """Log training parameters in a structured way.

    Args:
        logger: Logger instance
        params: Dictionary of training parameters
    """
    logger.info("Training parameters", **params)


def log_metrics(logger: StructuredLogger, metrics: Dict[str, float], step: Optional[int] = None) -> None:
    """Log metrics in a structured way.

    Args:
        logger: Logger instance
        metrics: Dictionary of metric names and values
        step: Optional training step number
    """
    log_data = {'metrics': metrics}
    if step is not None:
        log_data['step'] = step

    logger.info("Metrics", **log_data)


def log_model_info(logger: StructuredLogger, model_info: Dict[str, Any]) -> None:
    """Log model information in a structured way.

    Args:
        logger: Logger instance
        model_info: Dictionary of model information
    """
    logger.info("Model information", **model_info)
