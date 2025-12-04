from collections import deque
from typing import Deque, Generic, TypeVar
import threading
import time
from dataclasses import dataclass, field

T = TypeVar('T')

@dataclass(kw_only=True)
class BlockingQueue(Generic[T]):
    """Thread-safe bounded blocking queue implementation.
    
    Provides a FIFO queue with blocking put/get operations.
    Producers block when queue is full, consumers block when empty.
    """
    max_size: int = 10  # Maximum capacity of the queue
    
    # Internal queue storage (FIFO)
    _queue: Deque[T] = field(init=False, repr=False)
    # Shared lock for thread synchronization
    _lock: threading.Lock = field(init=False, repr=False)
    # Condition variable for consumers waiting on empty queue
    _not_empty: threading.Condition = field(init=False, repr=False)
    # Condition variable for producers waiting on full queue
    _not_full: threading.Condition = field(init=False, repr=False)
    
    def __post_init__(self) -> None:
        """Initialize queue with synchronization primitives."""
        # Validate capacity of the queue
        if self.max_size <= 0:
            raise ValueError("max_size must be greater than 0")
        
        # Initialize empty queue
        self._queue = deque()
        
        # Create shared lock for mutual exclusion
        self._lock = threading.Lock()
        
        # Create condition variables sharing the same lock (monitor pattern)
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)
    
    def put(self, item: T, timeout: float | None = None) -> None:
        """Add item to queue, blocking if full.
        
        Args:
            item: Item to add to queue
            timeout: Optional timeout in seconds (None = wait forever)
            
        Raises:
            TimeoutError: If timeout expires before space available
        """
        with self._not_full:  # Acquire lock
            # Calculate deadline if timeout specified
            if timeout is not None:
                end_time = time.monotonic() + timeout
            
            # Wait while queue is full (use while to handle spurious wakeups)
            while len(self._queue) >= self.max_size:
                if timeout is None:
                    # Block indefinitely until space available
                    self._not_full.wait()
                else:
                    # Calculate remaining time and wait with timeout
                    remaining = end_time - time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError("put() timed out waiting for space in the queue")
                    self._not_full.wait(timeout=remaining)
            
            # Add item to queue
            self._queue.append(item)
            
            # Wake one waiting consumer
            self._not_empty.notify()
    
    def get(self, timeout: float | None = None) -> T:
        """Remove and return item from queue, blocking if empty.
        
        Args:
            timeout: Optional timeout in seconds (None = wait forever)
            
        Returns:
            Item from front of queue
            
        Raises:
            TimeoutError: If timeout expires before item available
        """
        with self._not_empty:  # Acquire lock
            # Calculate deadline if timeout specified
            if timeout is not None:
                end_time = time.monotonic() + timeout
            
            # Wait while queue is empty (use while to handle spurious wakeups)
            while len(self._queue) == 0:
                if timeout is None:
                    # Block indefinitely until item available
                    self._not_empty.wait()
                else:
                    # Calculate remaining time and wait with timeout
                    remaining = end_time - time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError("get() timed out waiting for item")
                    self._not_empty.wait(timeout=remaining)
            
            # Remove and return item from front of queue
            item = self._queue.popleft()
            
            # Wake one waiting producer
            self._not_full.notify()
            return item

    def size(self) -> int:
        """Return current number of items in queue (thread-safe)."""
        with self._lock:
            return len(self._queue)
    
    def capacity(self) -> int:
        """Return maximum capacity of queue."""
        return self.max_size
    
    def is_empty(self) -> bool:
        """Check if queue is empty (thread-safe)."""
        with self._lock:
            return len(self._queue) == 0
    
    def is_full(self) -> bool:
        """Check if queue is full (thread-safe)."""
        with self._lock:
            return len(self._queue) >= self.max_size
