
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

import Final_Factory_System as factory


class TestFactoryAutomationSystem(unittest.TestCase):

    # MODULE 1: SYSTEM LOGIN
    def test_successful_login(self):
        with patch("builtins.input", side_effect=["admin", "1234"]):
            with redirect_stdout(StringIO()):
                result = factory.system_login()

        self.assertTrue(result)

    def test_failed_login(self):
        with patch("builtins.input", side_effect=[
            "wrong", "wrong",
            "wrong", "wrong",
            "wrong", "wrong"
        ]):
            with redirect_stdout(StringIO()):
                result = factory.system_login()

        self.assertFalse(result)

    # MODULE 2: MACHINE MANAGEMENT
    def test_update_machine_status(self):
        test_machines = [
            {
                "machine_id": "MCH001",
                "name": "Test Machine",
                "status": "MAINTENANCE"
            }
        ]

        with patch.object(factory, "machines", test_machines):
            with patch("builtins.input", side_effect=["MCH001", "1"]):
                with redirect_stdout(StringIO()):
                    factory.update_machine_status()

        self.assertEqual(test_machines[0]["status"], "AVAILABLE")

    def test_prevent_machine_from_production_during_maintenance(self):
        test_machines = [
            {
                "machine_id": "MCH001",
                "name": "Test Machine",
                "status": "MAINTENANCE"
            }
        ]

        with patch.object(factory, "machines", test_machines):
            with patch("builtins.input", side_effect=["MCH001", "2"]):
                with redirect_stdout(StringIO()):
                    factory.update_machine_status()

        self.assertEqual(test_machines[0]["status"], "MAINTENANCE")

    # MODULE 3: PRODUCT MANAGEMENT
    def test_add_product(self):
        test_products = []

        inputs = [
            "Test Product",
            "Electronics",
            "5",
            "100",
            "200"
        ]

        with patch.object(factory, "products", test_products):
            with patch("builtins.input", side_effect=inputs):
                with redirect_stdout(StringIO()):
                    factory.add_product()

        self.assertEqual(len(test_products), 1)
        self.assertEqual(test_products[0]["name"], "Test Product")
        self.assertEqual(test_products[0]["selling_price"], 200.0)

    def test_update_product(self):
        test_products = [
            {
                "id": "PRD001",
                "name": "Old Product",
                "category": "Lighting",
                "time": 4,
                "material_cost": 100.0,
                "selling_price": 200.0
            }
        ]

        inputs = ["PRD001", "", "", "", "", "300"]

        with patch.object(factory, "products", test_products):
            with patch("builtins.input", side_effect=inputs):
                with redirect_stdout(StringIO()):
                    factory.update_product()

        self.assertEqual(test_products[0]["selling_price"], 300.0)

    # MODULE 4: OPERATOR MANAGEMENT
    def test_add_operator(self):
        test_operators = []

        inputs = [
            "John",
            "Brown",
            "123456789",
            "1",
            "CNC Machine",
            "1"
        ]

        with patch.object(factory, "operators", test_operators):
            with patch("builtins.input", side_effect=inputs):
                with redirect_stdout(StringIO()):
                    factory.add_operator()

        self.assertEqual(len(test_operators), 1)
        self.assertEqual(test_operators[0]["first_name"], "John")
        self.assertEqual(test_operators[0]["shift"], "Morning")

    # MODULE 5: MAINTENANCE
    def test_record_maintenance(self):
        test_machines = [
            {
                "machine_id": "MCH001",
                "name": "Test Machine",
                "status": "AVAILABLE"
            }
        ]

        test_records = []

        inputs = [
            "MCH001",
            "EMP1",
            "Preventive",
            "Routine maintenance",
            "50",
            "125",
            "y"
        ]

        with patch.object(factory, "machines", test_machines):
            with patch.object(factory, "maintenance_records", test_records):
                with patch.object(factory, "maint_counter", 1):
                    with patch("builtins.input", side_effect=inputs):
                        with redirect_stdout(StringIO()):
                            factory.record_maintenance_func()

        self.assertEqual(len(test_records), 1)
        self.assertEqual(test_records[0]["Cost"], 50.0)
        self.assertEqual(test_machines[0]["status"], "AVAILABLE")

    # PRODUCTION MANAGEMENT
    def test_production_order(self):
        test_machines = [
            {
                "machine_id": "MCH001",
                "name": "Test Machine",
                "status": "AVAILABLE"
            }
        ]

        test_products = [
            {
                "id": "PRD001",
                "name": "Test Product",
                "material_cost": 100.0
            }
        ]

        test_operators = [
            {
                "employee_id": "EMP1",
                "first_name": "John",
                "last_name": "Brown"
            }
        ]

        test_orders = []

        inputs = [
            "PRD001",
            "MCH001",
            "EMP1",
            "10",
            "9",
            "1"
        ]

        with patch.object(factory, "machines", test_machines):
            with patch.object(factory, "products", test_products):
                with patch.object(factory, "operators", test_operators):
                    with patch.object(factory, "production_orders", test_orders):
                        with patch.object(factory, "order_counter", 1):
                            with patch("builtins.input", side_effect=inputs):
                                with redirect_stdout(StringIO()):
                                    factory.start_production_order()

        self.assertEqual(len(test_orders), 1)
        self.assertEqual(test_orders[0]["quantity_necessary"], 10)
        self.assertEqual(test_orders[0]["acceptable_quantity"], 9)
        self.assertEqual(test_machines[0]["status"], "IN PRODUCTION")

    # MODULE 7: REPORTING
    def test_machine_report(self):
        test_machines = [
            {
                "machine_id": "MCH001",
                "name": "Test Machine",
                "machine_type": "Cutting",
                "capacity": 50,
                "operating_hours": 100,
                "status": "AVAILABLE"
            }
        ]

        output = StringIO()

        with patch.object(factory, "machines", test_machines):
            with redirect_stdout(output):
                factory.machine_report()

        self.assertIn("MCH001", output.getvalue())
        self.assertIn("Total Number of Machines: 1", output.getvalue())

    def test_product_report(self):
        test_products = [
            {
                "id": "PRD001",
                "name": "Test Product",
                "time": 5,
                "material_cost": 100.0,
                "selling_price": 200.0
            }
        ]

        output = StringIO()

        with patch.object(factory, "products", test_products):
            with redirect_stdout(output):
                factory.product_report()

        self.assertIn("Test Product", output.getvalue())
        self.assertIn("$100.00", output.getvalue())

    def test_empty_maintenance_report(self):
        output = StringIO()

        with patch.object(factory, "maintenance_records", []):
            with redirect_stdout(output):
                factory.maintenance_report()

        self.assertIn("No maintenance records available", output.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
