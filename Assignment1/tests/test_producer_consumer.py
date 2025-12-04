import sys
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from Assignment1.producer_consumer import Producer, Consumer, SENTINEL, run_pipeline
from Assignment1.blocking_queue import BlockingQueue


class TestProducerConsumer(unittest.TestCase):
    
    def test_producer_init(self) -> None:
        queue: BlockingQueue = BlockingQueue(max_size=5)
        producer: Producer = Producer(source=[1, 2, 3], queue=queue)
        self.assertEqual(producer.source, [1, 2, 3])
        self.assertIs(producer.sentinel, SENTINEL)
    
    def test_consumer_init(self) -> None:
        queue: BlockingQueue = BlockingQueue(max_size=5)
        consumer: Consumer = Consumer(queue=queue, destination=[])
        self.assertEqual(consumer.destination, [])
        self.assertIs(consumer.sentinel, SENTINEL)
    
    def test_producer_enqueues_items_and_sentinel(self) -> None:
        queue: BlockingQueue[object] = BlockingQueue(max_size=5)
        source = [1, 2, 3]
        
        producer: Producer[int] = Producer(source=source, queue=queue)
        producer.start()
        producer.join(timeout=1.0)
        
        self.assertEqual(queue.get(), 1)
        self.assertEqual(queue.get(), 2)
        self.assertEqual(queue.get(), 3)
        self.assertIs(queue.get(), SENTINEL)
        
        self.assertTrue(queue.is_empty())
    
    def test_consumer_stops_on_immediate_sentinel(self) -> None:
        queue: BlockingQueue[object] = BlockingQueue(max_size=10)
        destination: list[int] = []

        queue.put(SENTINEL)

        consumer: Consumer[int] = Consumer(queue=queue, destination=destination)
        consumer.start()
        consumer.join(timeout=1.0)

        self.assertEqual(destination, [])
        self.assertTrue(queue.is_empty())
    
    def test_run_pipeline_round_trip_basic(self) -> None:
        source = [1, 2, 3, 4, 5]
        result = run_pipeline(source, queue_size=2)
        self.assertEqual(result, source)
    
    def test_run_pipeline_handles_empty_source(self) -> None:
        source: list[int] = []
        result = run_pipeline(source, queue_size=3)
        self.assertEqual(result, [])
    
    def test_run_pipeline_preserves_none_values(self) -> None:
        source: list[int | None] = [1, None, 3]
        result = run_pipeline(source, queue_size=2)
        self.assertEqual(result, [1, None, 3])
    
    def test_producer_sends_sentinel_on_exception(self) -> None:
        queue: BlockingQueue[object] = BlockingQueue(max_size=5)
        
        def failing_generator():
            yield 1
            yield 2
            raise RuntimeError("Test error")
        
        producer: Producer[int] = Producer(source=failing_generator(), queue=queue)
        producer.start()
        producer.join(timeout=1.0)
        
        self.assertEqual(queue.get(), 1)
        self.assertEqual(queue.get(), 2)
        self.assertIs(queue.get(), SENTINEL)
    
    def test_run_pipeline_with_large_dataset(self) -> None:
        source = list(range(100))
        result = run_pipeline(source, queue_size=5)
        self.assertEqual(result, source)
    
    def test_consumer_with_custom_destination(self) -> None:
        queue: BlockingQueue[object] = BlockingQueue(max_size=5)
        custom_dest: list[str] = []
        
        queue.put("a")
        queue.put("b")
        queue.put(SENTINEL)
        
        consumer: Consumer[str] = Consumer(queue=queue, destination=custom_dest)
        consumer.start()
        consumer.join(timeout=1.0)
        
        self.assertEqual(custom_dest, ["a", "b"])
    
    def test_main_block_execution(self) -> None:
        import sys
        from io import StringIO
        
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Execute the main block code
            sample_data = [1, 2, 3, None, 5]
            result = run_pipeline(sample_data, queue_size=3)
            
            # Verify result
            self.assertEqual(result, [1, 2, 3, None, 5])
            self.assertEqual(len(result), 5)
        finally:
            sys.stdout = old_stdout


if __name__ == '__main__':
    unittest.main()
