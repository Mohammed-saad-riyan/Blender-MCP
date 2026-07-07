import ast
import unittest
from pathlib import Path

SOURCE_PATH = Path(__file__).resolve().parents[1] / "blender_mcp.py"
SOURCE = SOURCE_PATH.read_text(encoding="utf-8")
TREE = ast.parse(SOURCE)


class BlenderMCPSourceTests(unittest.TestCase):
    def test_source_parses(self):
        self.assertIsInstance(TREE, ast.Module)

    def test_bounded_queue_is_configured(self):
        self.assertIn("MAX_QUEUE_SIZE", SOURCE)
        self.assertIn("queue.Queue(maxsize=Config.MAX_QUEUE_SIZE)", SOURCE)

    def test_requests_receive_unique_ids(self):
        self.assertIn("uuid.uuid4()", SOURCE)

    def test_main_thread_timer_drives_queue(self):
        self.assertIn("bpy.app.timers.register(self._process_queue)", SOURCE)
        self.assertIn("bpy.app.timers.is_registered(self._process_queue)", SOURCE)

    def test_timeout_path_exists(self):
        self.assertIn("Config.QUEUE_TIMEOUT", SOURCE)
        self.assertIn("raise TimeoutError", SOURCE)

    def test_queue_full_path_exists(self):
        self.assertIn("except queue.Full", SOURCE)
        self.assertIn('RuntimeError("Execution queue is full")', SOURCE)

    def test_structured_error_capture_exists(self):
        for field in ("traceback", "function", "args", "kwargs"):
            self.assertIn(f"'{field}'", SOURCE)

    def test_old_results_are_cleaned(self):
        self.assertIn("current_time - data['timestamp'] > 300", SOURCE)

    def test_visual_feedback_primitives_exist(self):
        for function_name in (
            "capture_viewport_image",
            "analyze_spatial_layout",
            "verify_last_operation",
        ):
            self.assertIn(f"def {function_name}", SOURCE)


if __name__ == "__main__":
    unittest.main()