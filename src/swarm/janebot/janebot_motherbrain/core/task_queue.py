"""
================================================================================
TASK QUEUE - PRIORITY-BASED WORK DISTRIBUTION
================================================================================
This module implements the core task management and distribution system for the
AI swarm. It ensures that work is prioritized, assigned to capable agents,
and tracked throughout its lifecycle.

Key Mechanisms:
- Priority Queue: Tasks are processed based on urgency (Critical > High > Medium, etc.).
- Capability Matching: Tasks are intelligently routed to agents possessing the required skills.
- Lifecycle Tracking: Monitors tasks from creation to completion, failure, or timeout.
- Concurrency Management: Controls how many tasks an agent or the swarm can handle.
================================================================================
"""

import asyncio
import heapq
import uuid
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
import logging

from .message_bus import MessageBus, Message, MessageType
from .agent_registry import AgentRegistry, AgentInfo

logger = logging.getLogger(__name__)


class Priority(Enum):
    """Task priority levels."""
    CRITICAL = 10
    HIGH = 8
    MEDIUM = 5
    LOW = 3
    BACKGROUND = 1


class TaskStatus(Enum):
    """Task status."""
    PENDING = auto()
    QUEUED = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()
    TIMEOUT = auto()


@dataclass
class Task:
    """A task to be executed by an agent."""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    capability: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    timeout: float = 300.0
    retry_count: int = 0
    max_retries: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __lt__(self, other: "Task") -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return self.created_at < other.created_at
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "description": self.description,
            "capability": self.capability,
            "payload": self.payload,
            "priority": self.priority.value,
            "status": self.status.name,
            "assigned_agent": self.assigned_agent,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "timeout": self.timeout,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        task = cls(**{
            k: v for k, v in data.items() 
            if k in ["task_id", "description", "capability", "payload", 
                     "timeout", "retry_count", "max_retries", "metadata"]
        })
        if "priority" in data:
            task.priority = Priority(data["priority"])
        if "status" in data:
            task.status = TaskStatus[data["status"]]
        task.assigned_agent = data.get("assigned_agent")
        task.result = data.get("result")
        task.error = data.get("error")
        task.created_at = data.get("created_at", datetime.now().timestamp())
        task.started_at = data.get("started_at")
        task.completed_at = data.get("completed_at")
        return task


class TaskQueue:
    """
    Priority queue for task distribution.
    """
    
    def __init__(self, message_bus=None, agent_registry=None):
        self._message_bus = message_bus
        self._agent_registry = agent_registry
        self._queue: List[Tuple[int, Task]] = []
        self._tasks: Dict[str, Task] = {}
        self._running_tasks: Dict[str, Task] = {}
        self._lock = asyncio.Lock()
        self._running = False
        self._worker_tasks: List[asyncio.Task] = []
        self._num_workers = 10
        self._task_callbacks: Dict[str, asyncio.Queue] = {}
        
    async def start(self, num_workers: int = 10):
        self._running = True
        self._num_workers = num_workers
        for i in range(num_workers):
            worker = asyncio.create_task(self._worker(i))
            self._worker_tasks.append(worker)
        logger.info(f"TaskQueue started with {num_workers} workers")
        
    async def stop(self):
        self._running = False
        for worker in self._worker_tasks:
            worker.cancel()
        for worker in self._worker_tasks:
            try:
                await worker
            except asyncio.CancelledError:
                pass
        self._worker_tasks = []
        logger.info("TaskQueue stopped")
        
    async def enqueue(self, task: Task) -> str:
        async with self._lock:
            priority_score = self._calculate_priority_score(task)
            heapq.heappush(self._queue, (priority_score, task))
            self._tasks[task.task_id] = task
            self._task_callbacks[task.task_id] = asyncio.Queue()
            
            if self._message_bus:
                from .message_bus import Message, MessageType
                msg = Message(
                    sender="task_queue",
                    topic="task.enqueued",
                    message_type=MessageType.TASK,
                    payload={"task_id": task.task_id, "priority": task.priority.value}
                )
                await self._message_bus.publish(msg)
            return task.task_id
            
    async def enqueue_and_wait(self, task: Task, timeout: Optional[float] = None) -> Dict[str, Any]:
        task_id = await self.enqueue(task)
        try:
            result = await asyncio.wait_for(
                self._task_callbacks[task_id].get(), 
                timeout=timeout or task.timeout
            )
            return result
        except asyncio.TimeoutError:
            await self.cancel_task(task_id, reason="Timeout waiting for result")
            raise TimeoutError(f"Task {task_id} timed out")
        finally:
            self._task_callbacks.pop(task_id, None)
            
    async def _worker(self, worker_id: int):
        while self._running:
            try:
                async with self._lock:
                    if not self._queue:
                        await asyncio.sleep(0.1)
                        continue
                    _, task = heapq.heappop(self._queue)
                    if task.task_id not in self._tasks:
                        continue
                    if not self._agent_registry:
                        logger.warning("No agent registry available, skipping task")
                        continue
                    best_agent = await self._agent_registry.get_best_agent(task.capability)
                    if not best_agent or not best_agent.is_available():
                        priority_score = self._calculate_priority_score(task)
                        heapq.heappush(self._queue, (priority_score, task))
                        await asyncio.sleep(1)
                        continue
                    task.status = TaskStatus.RUNNING
                    task.assigned_agent = best_agent.agent_id
                    task.started_at = datetime.now().timestamp()
                    self._running_tasks[task.task_id] = task
                    await self._agent_registry.update_agent_status(
                        best_agent.agent_id, "busy", best_agent.current_load + 1
                    )
                try:
                    result = await self._execute_task(task, best_agent)
                    await self._complete_task(task, result)
                    await self._agent_registry.update_agent_status(
                        best_agent.agent_id, "online", best_agent.current_load - 1
                    )
                except Exception as e:
                    logger.error(f"Task {task.task_id} failed: {e}")
                    await self._fail_task(task, str(e))
                    await self._agent_registry.update_agent_status(
                        best_agent.agent_id, "online", best_agent.current_load - 1
                    )
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}")
                await asyncio.sleep(1)
                
    async def _execute_task(self, task: Task, agent: Any) -> Dict[str, Any]:
        logger.info(f"Executing task {task.task_id} on agent {agent.agent_id}")
        if not self._message_bus:
            return {"status": "completed", "result": "No message bus available"}
        msg = Message(
            message_id=task.task_id,
            sender="task_queue",
            recipient=agent.agent_id,
            topic=f"task.execute.{task.capability}",
            message_type=MessageType.TASK,
            payload={
                "task_id": task.task_id,
                "description": task.description,
                "capability": task.capability,
                "payload": task.payload,
                "timeout": task.timeout
            },
            priority=task.priority.value,
            metadata={"retry_count": task.retry_count}
        )
        await self._message_bus.publish(msg)
        try:
            result = await self._message_bus.request_response(
                Message(
                    sender="task_queue", 
                    recipient=agent.agent_id, 
                    topic=f"task.response.{task.task_id}",
                    message_type=MessageType.RESPONSE
                ),
                timeout=task.timeout
            )
            if result: return result
            raise TimeoutError(f"Agent {agent.agent_id} failed to respond to task {task.task_id}")
        except Exception as e:
            logger.error(f"Error awaiting response for task {task.task_id}: {e}")
            raise e
            
    async def _complete_task(self, task: Task, result: Dict[str, Any]):
        async with self._lock:
            task.status = TaskStatus.COMPLETED
            task.result = result
            task.completed_at = datetime.now().timestamp()
            self._running_tasks.pop(task.task_id, None)
            if task.task_id in self._task_callbacks:
                await self._task_callbacks[task.task_id].put(result)
            if self._message_bus:
                from .message_bus import Message, MessageType
                msg = Message(
                    sender="task_queue",
                    topic="task.completed",
                    message_type=MessageType.TASK,
                    payload={"task_id": task.task_id, "result": result}
                )
                await self._message_bus.publish(msg)
                
    async def _fail_task(self, task: Task, error: str):
        async with self._lock:
            task.retry_count += 1
            if task.retry_count >= task.max_retries:
                task.status = TaskStatus.FAILED
                task.error = error
                self._running_tasks.pop(task.task_id, None)
                if task.task_id in self._task_callbacks:
                    await self._task_callbacks[task.task_id].put({"status": "error", "error": error})
            else:
                task.status = TaskStatus.QUEUED
                priority_score = self._calculate_priority_score(task)
                heapq.heappush(self._queue, (priority_score, task))
                
    async def cancel_task(self, task_id: str, reason: str = "Cancelled by user"):
        async with self._lock:
            if task_id in self._running_tasks:
                task = self._running_tasks[task_id]
                task.status = TaskStatus.CANCELLED
                task.error = reason
                self._running_tasks.pop(task_id)
                if task_id in self._task_callbacks:
                    await self._task_callbacks[task_id].put({"status": "cancelled", "error": reason})
            elif task_id in self._tasks:
                task = self._tasks[task_id]
                if task.status == TaskStatus.QUEUED:
                    task.status = TaskStatus.CANCELLED
                    task.error = reason
                    if task_id in self._task_callbacks:
                        await self._task_callbacks[task_id].put({"status": "cancelled", "error": reason})
                        
    def _calculate_priority_score(self, task: Task) -> int:
        priority_value = task.priority.value
        age_factor = max(0, (datetime.now().timestamp() - task.created_at) / 100)
        retry_penalty = task.retry_count * 10
        return int(priority_value * 1000 + age_factor - retry_penalty)
        
    async def get_task(self, task_id: str) -> Optional[Task]:
        async with self._lock:
            return self._tasks.get(task_id)
            
    async def list_tasks(self, status_filter: Optional[TaskStatus] = None) -> List[Task]:
        async with self._lock:
            tasks = list(self._tasks.values())
            if status_filter:
                tasks = [t for t in tasks if t.status == status_filter]
            return sorted(tasks, key=lambda x: x.created_at, reverse=True)
            
    async def get_stats(self) -> Dict[str, Any]:
        async with self._lock:
            return {
                "total_tasks": len(self._tasks),
                "pending_tasks": sum(1 for t in self._tasks.values() if t.status == TaskStatus.PENDING),
                "queued_tasks": sum(1 for t in self._tasks.values() if t.status == TaskStatus.QUEUED),
                "running_tasks": len(self._running_tasks),
                "completed_tasks": sum(1 for t in self._tasks.values() if t.status == TaskStatus.COMPLETED),
                "failed_tasks": sum(1 for t in self._tasks.values() if t.status == TaskStatus.FAILED),
                "cancelled_tasks": sum(1 for t in self._tasks.values() if t.status == TaskStatus.CANCELLED),
                "queue_size": len(self._queue),
                "worker_count": len(self._worker_tasks)
            }
