import sys
from pathlib import Path
import threading
import time
import unittest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from Assignment1.blocking_queue import BlockingQueue


class TestBlockingQueue(unittest.TestCase):
    
    def test_queue_initial_state(self) -> None:
        queue = BlockingQueue[int](max_size=5)
        self.assertEqual(queue.size(), 0)
        self.assertEqual(queue.capacity(), 5)
        self.assertTrue(queue.is_empty())
        self.assertFalse(queue.is_full())
    
    def test_queue_rejects_invalid_capacity(self) -> None:
        with self.assertRaises(ValueError):
            BlockingQueue[int](max_size=0)
        with self.assertRaises(ValueError):
            BlockingQueue[int](max_size=-1)
    
    def test_queue_put_and_get_basic(self) -> None:
        queue = BlockingQueue[int](max_size=3)
        queue.put(1)
        queue.put(2)
        queue.put(3)
        
        self.assertEqual(queue.size(), 3)
        self.assertTrue(queue.is_full())
        
        self.assertEqual(queue.get(), 1)
        self.assertEqual(queue.get(), 2)
        self.assertEqual(queue.size(), 1)
        self.assertFalse(queue.is_full())
        
        queue.put(4)
        self.assertEqual(queue.size(), 2)
        self.assertEqual(queue.get(), 3)
        self.assertEqual(queue.get(), 4)
        self.assertTrue(queue.is_empty())
    
    def test_queue_blocks_get_when_empty_until_item_available(self) -> None:
        queue: BlockingQueue[int] = BlockingQueue(max_size=2)
        result: list[int] = []
        
        def consumer() -> None:
            item = queue.get()
            result.append(item)
        
        t = threading.Thread(target=consumer)
        t.start()
        
        time.sleep(0.05)
        self.assertEqual(result, [])
        
        queue.put(42)
        
        t.join(timeout=1.0)
        self.assertEqual(result, [42])
    
    def test_queue_blocks_put_when_full_until_space_available(self) -> None:
        queue: BlockingQueue[int] = BlockingQueue(max_size=1)
        queue.put(10)
        
        blocked = {"value": True}
        
        def producer() -> None:
            queue.put(20)
            blocked["value"] = False
        
        t = threading.Thread(target=producer)
        t.start()
        
        time.sleep(0.05)
        self.assertTrue(blocked["value"])
        
        self.assertEqual(queue.get(), 10)
        
        t.join(timeout=1.0)
        self.assertFalse(blocked["value"])
        self.assertEqual(queue.get(), 20)
        self.assertTrue(queue.is_empty())
    
    def test_put_timeout_raises_error(self) -> None:
        queue: BlockingQueue[int] = BlockingQueue(max_size=1)
        queue.put(1)
        
        with self.assertRaises(TimeoutError):
            queue.put(2, timeout=0.1)
    
    def test_get_timeout_raises_error(self) -> None:
        queue: BlockingQueue[int] = BlockingQueue(max_size=5)
        
        with self.assertRaises(TimeoutError):
            queue.get(timeout=0.1)
    
    def test_put_with_timeout_succeeds_when_space_available(self) -> None:
        queue: BlockingQueue[int] = BlockingQueue(max_size=1)
        queue.put(10)
        
        def consumer() -> None:
            time.sleep(0.05)
            queue.get()
        
        t = threading.Thread(target=consumer)
        t.start()
        
        queue.put(20, timeout=1.0)
        t.join()
        
        self.assertEqual(queue.get(), 20)
    
    def test_get_with_timeout_succeeds_when_item_available(self) -> None:
        queue: BlockingQueue[int] = BlockingQueue(max_size=5)
        
        def producer() -> None:
            time.sleep(0.05)
            queue.put(42)
        
        t = threading.Thread(target=producer)
        t.start()
        
        result = queue.get(timeout=1.0)
        t.join()
        
        self.assertEqual(result, 42)


if __name__ == '__main__':
    unittest.main()