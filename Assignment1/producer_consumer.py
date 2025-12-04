import threading
from dataclasses import dataclass, field
from typing import Generic, Iterable, List, TypeVar, cast
try:
    from .blocking_queue import BlockingQueue
except ImportError:
    from blocking_queue import BlockingQueue
import time

# Generic type variable for type-safe producer-consumer
T = TypeVar("T")

# Unique sentinel object to signal end of data stream
SENTINEL = object()

@dataclass(kw_only=True, eq=False)
class Producer(threading.Thread, Generic[T]):
    """Producer thread that reads from source and pushes to queue.
    
    Continuously reads items from source iterable and places them into
    the shared blocking queue. Always sends sentinel on completion,
    even if an exception occurs.
    """
    source: Iterable[T]  # Data source to read from
    queue: BlockingQueue[object]  # Shared queue to write to
    sentinel: object = SENTINEL  # Stop signal for consumer
    name: str = "producer"  # Thread name for debugging
    
    def __post_init__(self) -> None:
        """Initialize thread after dataclass initialization."""
        threading.Thread.__init__(self, name=self.name)
    
    def run(self) -> None:
        """Main producer logic: read from source, write to queue."""
        try:
            # Iterate through source and push each item to queue
            for item in self.source:
                self.queue.put(item)  # Blocks if queue is full
        finally:
            # Always send sentinel to signal consumer to stop
            # This ensures clean shutdown even if exception occurs
            self.queue.put(self.sentinel)


@dataclass(kw_only=True, eq=False)
class Consumer(threading.Thread, Generic[T]):
    """Consumer thread that reads from queue and writes to destination.
    
    Continuously pulls items from the shared blocking queue and appends
    them to the destination list. Stops when sentinel is received.
    """
    queue: BlockingQueue[object]  # Shared queue to read from
    destination: List[T] = field(default_factory=list)  # Where to store items
    sentinel: object = SENTINEL  # Stop signal from producer
    name: str = "consumer"  # Thread name for debugging
    
    def __post_init__(self) -> None:
        """Initialize thread after dataclass initialization."""
        threading.Thread.__init__(self, name=self.name)
        
    def run(self) -> None:
        """Main consumer logic: read from queue, write to destination."""
        while True:
            # Pull item from queue (blocks if queue is empty)
            item = self.queue.get()
            
            # Check if this is the stop signal
            if item is self.sentinel:
                break  # Exit loop and terminate thread
            
            # Cast to correct type and append to destination
            value = cast(T, item)
            self.destination.append(value)


def run_pipeline(source: Iterable[T], queue_size: int=10) -> List[T]:
    """Orchestrate producer-consumer pipeline.
    
    Creates shared queue, starts producer and consumer threads,
    waits for completion, and returns collected results.
    
    Args:
        source: Iterable data source for producer
        queue_size: Maximum capacity of shared queue
        
    Returns:
        List of items transferred through pipeline
    """
    # Create shared blocking queue
    queue: BlockingQueue[object] = BlockingQueue(max_size=queue_size)
    # Create destination list for results
    destination: List[T] = []

    # Create producer and consumer threads
    producer: Producer[T] = Producer(source=source, queue=queue, sentinel=SENTINEL)
    consumer: Consumer[T] = Consumer(queue=queue, destination=destination, sentinel=SENTINEL)

    # Start both threads concurrently
    producer.start()
    consumer.start()

    # Wait for both threads to complete
    producer.join()  # Wait for producer to finish
    consumer.join()  # Wait for consumer to finish

    # Return collected results
    return destination


if __name__ == "__main__":  # pragma: no cover - to ignore main module for increased code coverage
    """Demo: Run producer-consumer pipeline with sample data."""
    source = [1, 2, 3, 4, 5]

    print("Running producer–consumer pipeline...")
    # Run pipeline with small queue to demonstrate blocking
    result = run_pipeline(source, queue_size=3)

    # Display results
    print("\n=== Pipeline Summary ===")
    print(f"Source Data:       {source}")
    print(f"Destination Data:      {result}")
    print(f"Items in:    {len(source)}")
    print(f"Items out:   {len(result)}")
    print("Status:      Completed successfully.")
