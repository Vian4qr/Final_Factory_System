# ==========================================
# FACTORY AUTOMATION MANAGEMENT SYSTEM
# Consolidated Master Script (Modules 1 - 7)
# ==========================================

from datetime import datetime
from enum import Enum

# --- GLOBAL DATA STRUCTURES ---
machines = [
    {"machine_id": "MCH001", "name": "CNC Milling Machine", "machine_type": "Cutting", "capacity": 50, "operating_cost": 120.0, "status": "AVAILABLE", "operating_hours": 120},
    {"machine_id": "MCH002", "name": "Assembly Robot", "machine_type": "Assembly", "capacity": 80, "operating_cost": 150.0, "status": "IN PRODUCTION", "operating_hours": 200},
    {"machine_id": "MCH003", "name": "Laser Cutter", "machine_type": "Cutting", "capacity": 30, "operating_cost": 200.0, "status": "MAINTENANCE", "operating_hours": 95}
]

products = [
    {"id": "PRD001", "name": "LED Lighting Unit", "category": "Lighting", "time": 4, "material_cost": 1500.0, "selling_price": 2800.0},
    {"id": "PRD002", "name": "Smart Power Outlet", "category": "Electrical", "time": 6, "material_cost": 2200.0, "selling_price": 4000.0},
    {"id": "PRD003", "name": "Electronic Control Module", "category": "Electronic", "time": 10, "material_cost": 3500.0, "selling_price": 6500.0},
    {"id": "PRD004", "name": "Sensor Module", "category": "Sensor", "time": 5, "material_cost": 1800.0, "selling_price": 3200.0}
]

operators = []
production_orders = []
maintenance_records = []
maint_counter = 1
order_counter = 1
machine_id_counter = 103648


# ==========================================
# MODULE 1: SYSTEM LOGIN
# ==========================================
def system_login():
    auth_personel = {"admin": "1234"}
    max_attempts = 3
    attempts = 0
    print("Restricted system, please enter username and password")

    while attempts < max_attempts:
        uname = input("Enter username: ").strip()
        pword = input("Enter password: ").strip()
        
        if uname in auth_personel and auth_personel[uname] == pword:
            print("Access Granted\n")
            return True
        else: 
            attempts += 1
            attempts_left = max_attempts - attempts
            if attempts_left > 0:
                print("Username or password incorrect please try again") 
            else: 
                print("Max attempts reached, program will now terminate")
                return False
    return False


# ==========================================
# MODULE 2: ADD MACHINE(S)
# ==========================================
def add_machine():
    global machine_id_counter
    print("\n--- ADD MACHINE ---")
    while True:
        name = input("Enter Machine Name: ").strip()
        machine_type = input("Enter Machine Type/Category: ").strip()
        if name and machine_type:
            break
        print("[ERROR] Name and type cannot be empty.")

    while True:
        try:
            capacity = int(input("Enter Production Capacity (units/hour): "))
            if capacity > 0:
                break
            print("[ERROR] Capacity must be greater than 0.")
        except ValueError:
            print("[ERROR] Enter a valid integer.")

    while True:
        try:
            operating_cost = float(input("Enter Operating Cost per hour ($): "))
            if operating_cost >= 0:
                break
            print("[ERROR] Cost cannot be negative.")
        except ValueError:
            print("[ERROR] Enter a valid number.")

    while True:
        try:
            operating_hours = int(input("Enter Total Operating Hours: "))
            if operating_hours >= 0:
                break
            print("[ERROR] Hours cannot be negative.")
        except ValueError:
            print("[ERROR] Enter a valid integer.")

    valid_statuses = ["Available", "In Production", "Maintenance", "Out of Service"]
    print("\nSelect Machine Status:")
    for idx, st in enumerate(valid_statuses, 1):
        print(f"{idx}. {st}")
    
    while True:
        try:
            choice = int(input("Enter choice (1-4): "))
            if 1 <= choice <= 4:
                status = valid_statuses[choice - 1].upper()
                break
        except ValueError:
            pass
        print("[ERROR] Invalid choice. Enter 1-4.")

    new_machine_id = f"MCH{str(machine_id_counter)[-3:]}"
    machine_id_counter += 1

    machine_dict = {
        "machine_id": new_machine_id,
        "name": name,
        "machine_type": machine_type,
        "capacity": capacity,
        "operating_cost": operating_cost,
        "status": status,
        "operating_hours": operating_hours
    }
    machines.append(machine_dict)
    print(f"[SUCCESS] Machine added successfully with ID: {new_machine_id}\n")


# ==========================================
# MODULE 3: ADD / UPDATE PRODUCT
# ==========================================
def add_product():
    print("\n--- ADD NEW PRODUCT ---")
    prod_id = f"PRD{len(products) + 1:03d}"
    print(f"Generated Product ID: {prod_id}")
    
    name = input("Enter Product Name: ").strip()
    category = input("Enter Product Category: ").strip()
    
    while True:
        try:
            time_per_unit = int(input("Enter Production Time per unit (minutes): "))
            if time_per_unit > 0:
                break
            print("[ERROR] Production time must be greater than 0.")
        except ValueError:
            print("[ERROR] Please enter a valid integer.")
            
    while True:
        try:
            material_cost = float(input("Enter Material Cost per unit ($): "))
            if material_cost >= 0:
                break
            print("[ERROR] Material cost cannot be negative.")
        except ValueError:
            print("[ERROR] Please enter a valid number.")
            
    while True:
        try:
            selling_price = float(input("Enter Selling Price per unit ($): "))
            if selling_price >= 0:
                break
            print("[ERROR] Selling price cannot be negative.")
        except ValueError:
            print("[ERROR] Please enter a valid number.")
            
    new_prod = {
        "id": prod_id,
        "name": name,
        "category": category,
        "time": time_per_unit,
        "material_cost": material_cost,
        "selling_price": selling_price
    }
    products.append(new_prod)
    print(f"[SUCCESS] Product '{name}' ({prod_id}) added successfully.\n")

def update_product():
    print("\n--- UPDATE EXISTING PRODUCT ---")
    if not products:
        print("[ERROR] No products available to update.")
        return

    print(f"{'ID':<8} | {'Product Name':<28} | {'Category':<12} | {'Price':<10}")
    print("-" * 65)
    for p in products:
        print(f"{p['id']:<8} | {p['name']:<28} | {p['category']:<12} | ${p['selling_price']:<9.2f}")

    target_id = input("\nEnter Product ID to update: ").strip().upper()
    product = next((p for p in products if p['id'] == target_id), None)

    if not product:
        print(f"[ERROR] Product ID '{target_id}' not found.")
        return

    print(f"\nUpdating Product: {product['name']} ({product['id']})")
    new_name = input(f"New Name [{product['name']}]: ").strip()
    if new_name: product['name'] = new_name

    new_cat = input(f"New Category [{product['category']}]: ").strip()
    if new_cat: product['category'] = new_cat

    new_time = input(f"New Production Time [{product['time']}]: ").strip()
    if new_time:
        try: product['time'] = int(new_time)
        except ValueError: pass

    new_mat_cost = input(f"New Material Cost [{product['material_cost']}]: ").strip()
    if new_mat_cost:
        try: product['material_cost'] = float(new_mat_cost)
        except ValueError: pass

    new_price = input(f"New Selling Price [{product['selling_price']}]: ").strip()
    if new_price:
        try: product['selling_price'] = float(new_price)
        except ValueError: pass

    print(f"[SUCCESS] Product {target_id} updated successfully.\n")


# ==========================================
# MODULE 4: ADD OPERATOR / TECHNICIAN
# ==========================================
def add_operator():
    print("\n--- ADD OPERATOR / TECHNICIAN ---")
    emp_id = f"EMP{len(operators) + 1}"
    print(f"Generated Employee ID: {emp_id}")
    
    while True:
        first_name = input("Enter First Name: ").strip()
        if first_name.isalpha(): break
        print("[ERROR] Letters only.")
        
    while True:
        last_name = input("Enter Last Name: ").strip()
        if last_name.isalpha(): break
        print("[ERROR] Letters only.")
        
    while True:
        contact = input("Enter Contact Number: ").strip()
        if contact.isdigit() and len(contact) >= 7: break
        print("[ERROR] Enter valid numeric contact (at least 7 digits).")

    roles = ["Machine Operator", "Maintenance Technician", "Electrical Technician", "Automation Technician", "Production Supervisor"]
    print("\nSelect Role:")
    for idx, role in enumerate(roles, 1): print(f"{idx}. {role}")
        
    while True:
        try:
            choice = int(input("Enter choice (1-5): "))
            if 1 <= choice <= len(roles):
                role = roles[choice - 1]
                break
        except ValueError: pass
        print("[ERROR] Invalid selection.")

    machine_spec = input("Enter Machine Specialization: ").strip()
    shifts = ["Morning", "Evening", "Night"]
    print("\nSelect Shift:")
    for idx, shift in enumerate(shifts, 1): print(f"{idx}. {shift}")
        
    while True:
        try:
            choice = int(input("Enter choice (1-3): "))
            if 1 <= choice <= len(shifts):
                shift = shifts[choice - 1]
                break
        except ValueError: pass
        print("[ERROR] Invalid selection.")

    new_operator = {
        "employee_id": emp_id,
        "first_name": first_name,
        "last_name": last_name,
        "contact": contact,
        "role": role,
        "specialization": machine_spec,
        "shift": shift
    }
    operators.append(new_operator)
    print(f"[SUCCESS] Operator {first_name} {last_name} ({emp_id}) added successfully.\n")


# ==========================================
# MODULE 5: UPDATE MACHINE STATUS
# ==========================================
def update_machine_status():
    print("\n--- UPDATE MACHINE STATUS ---")
    if not machines:
        print("[INFO] No machines found.")
        return
        
    print("\nCurrent Machine List:")
    for m in machines:
        print(f"ID: {m['machine_id']} | Name: {m['name']} | Status: {m['status']}")
        
    target_id = input("\nEnter Machine ID to update: ").strip().upper()
    found_machine = next((m for m in machines if m["machine_id"] == target_id), None)
            
    if not found_machine:
        print(f"[ERROR] Machine ID '{target_id}' not found.")
        return

    print(f"Current Status for {found_machine['name']}: {found_machine['status']}")
    valid_states = ["AVAILABLE", "IN PRODUCTION", "MAINTENANCE", "OUT OF SERVICE"]
    
    print("\nSelect New Status:")
    for idx, state in enumerate(valid_states, 1): print(f"{idx}. {state}")
        
    while True:
        try:
            choice = int(input("Enter choice (1-4): "))
            if 1 <= choice <= len(valid_states):
                new_status = valid_states[choice - 1]
                break
        except ValueError: pass
        print("[ERROR] Invalid selection.")

    if new_status == "IN PRODUCTION" and found_machine["status"] in ["MAINTENANCE", "OUT OF SERVICE"]:
        print(f"[ERROR] Cannot set machine to IN PRODUCTION. Machine is currently {found_machine['status']}.")
        return

    found_machine["status"] = new_status
    print(f"[SUCCESS] Machine {target_id} status updated to {new_status}.\n")


# ==========================================
# MODULE 6: RECORD MAINTENANCE
# ==========================================
def record_maintenance_func():
    global maint_counter
    print("\n--- MODULE 6: RECORD MAINTENANCE ---")
    
    maint_id = f"MAINT-{maint_counter:03d}"
    maint_counter += 1
    
    print(f"Logging Maintenance ID: {maint_id}")
    machine_id = input("Enter Machine ID: ").strip().upper()
    tech_id = input("Enter Technician ID: ").strip().upper()
    maint_type = input("Enter Maintenance Type (Preventive / Corrective / Electrical / Mechanical / Software): ").strip()
    description = input("Enter Problem Description: ").strip()
    
    try:
        cost = float(input("Enter Maintenance Cost ($): "))
        hours = float(input("Enter Machine Operating Hours: "))
    except ValueError:
        cost = 0.0
        hours = 0.0
        print("Invalid number entered; cost and hours defaulted to 0.")

    status = "MAINTENANCE"
    print(f"-> Machine {machine_id} status set to: {status}")
    
    complete = input("Is the maintenance complete now? (y/n): ").strip().lower()
    if complete == 'y':
        status = "AVAILABLE"
        print(f"-> Machine {machine_id} status returned to: {status}")

    # Also update machine status in list if it exists
    for m in machines:
        if m["machine_id"] == machine_id:
            m["status"] = status

    record = {
        "Maintenance ID": maint_id,
        "Machine ID": machine_id,
        "Technician ID": tech_id,
        "Type": maint_type,
        "Description": description,
        "Cost": cost,
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Status": status
    }
    maintenance_records.append(record)
    print("Record saved successfully!\n")


# ==========================================
# START PRODUCTION ORDER (Bonus/Brief Integration)
# ==========================================
def start_production_order():
    global order_counter
    print("\n--- START PRODUCTION ORDER ---")
    if not machines or not products or not operators:
        print("[ERROR] Ensure machines, products, and operators are added before starting production.")
        return

    order_id = f"ORD{order_counter:03d}"
    order_counter += 1

    print("\nAvailable Products:")
    for p in products: print(f"ID: {p['id']} | Name: {p['name']}")
    prod_id = input("Enter Product ID: ").strip().upper()
    product = next((p for p in products if p['id'] == prod_id), None)
    if not product:
        print("[ERROR] Product not found.")
        return

    print("\nAvailable Machines:")
    for m in machines: print(f"ID: {m['machine_id']} | Name: {m['name']} | Status: {m['status']}")
    mach_id = input("Enter Machine ID: ").strip().upper()
    machine = next((m for m in machines if m['machine_id'] == mach_id), None)
    if not machine:
        print("[ERROR] Machine not found.")
        return

    if machine['status'] != "AVAILABLE":
        print(f"[ERROR] Machine {mach_id} is '{machine['status']}' and cannot be assigned to production.")
        return

    print("\nAvailable Operators:")
    for op in operators: print(f"ID: {op['employee_id']} | Name: {op['first_name']} {op['last_name']}")
    op_id = input("Enter Operator ID: ").strip().upper()
    operator = next((o for o in operators if o['employee_id'] == op_id), None)
    if not operator:
        print("[ERROR] Operator not found.")
        return

    try:
        qty_needed = int(input("Enter quantity requested: "))
        if qty_needed <= 0: raise ValueError
    except ValueError:
        print("[ERROR] Invalid quantity.")
        return

    machine['status'] = "IN PRODUCTION"
    est_cost = qty_needed * product['material_cost'] * 0.1  # calculation estimate

    print(f"\nProduction started successfully for Order {order_id}!")
    good_qty = int(input("Enter actual acceptable quantity produced: "))
    defective_qty = int(input("Enter defective quantity: "))

    order_record = {
        "order_id": order_id,
        "product": product,
        "machine": machine,
        "operator": operator,
        "quantity_necessary": qty_needed,
        "acceptable_quantity": good_qty,
        "defective_quantity": defective_qty,
        "estimated_cost": est_cost
    }
    production_orders.append(order_record)
    print(f"[SUCCESS] Order {order_id} completed and recorded.\n")


# ==========================================
# MODULE 7: REPORTS
# ==========================================
def report_header(title):
    print("\n" + "=" * 90)
    print(f"{title:^90}")
    print("=" * 90)

def machine_report():
    report_header("MACHINE REPORT")
    if not machines:
        print("No machines available.")
        return
    print(f"{'Machine ID':<15} {'Name':<25} {'Type':<18} {'Capacity':<12} {'Hours':<12} {'Status':<18}")
    print("-" * 100)
    for m in machines:
        print(f"{m.get('machine_id', 'N/A'):<15} {m.get('name', 'N/A'):<25} {m.get('machine_type', 'N/A'):<18} {m.get('capacity', 'N/A'):<12} {m.get('operating_hours', 0):<12} {m.get('status', 'N/A'):<18}")
    print("-" * 100)
    print(f"Total Number of Machines: {len(machines)}")

def production_report():
    report_header("PRODUCTION REPORT")
    if not production_orders:
        print("No production orders available.")
        return
    print(f"{'Order ID':<12} {'Product':<22} {'Machine':<12} {'Operator':<15} {'Requested':<12} {'Good':<10} {'Defective':<12} {'Est. Cost':<12}")
    print("-" * 110)
    total_good = total_defective = total_cost = 0

    for order in production_orders:
        good = order['acceptable_quantity']
        defective = order['defective_quantity']
        total_prod = good + defective
        print(f"{order['order_id']:<12} {order['product']['name']:<22} {order['machine']['machine_id']:<12} {order['operator']['employee_id']:<15} {order['quantity_necessary']:<12} {good:<10} {defective:<12} ${order['estimated_cost']:<11.2f}")
        total_good += good
        total_defective += defective
        total_cost += order['estimated_cost']

    overall_defect_rate = (total_defective / (total_good + total_defective) * 100) if (total_good + total_defective) > 0 else 0
    print("-" * 110)
    print(f"Total Good Units: {total_good}")
    print(f"Total Defective Units: {total_defective}")
    print(f"Overall Defective Rate: {overall_defect_rate:.2f}%")
    print(f"Total Estimated Cost: ${total_cost:.2f}")

def product_report():
    report_header("PRODUCT REPORT")
    if not products:
        print("No products available.")
        return
    print(f"{'Product ID':<12} {'Product Name':<30} {'Time (mins)':<15} {'Material Cost':<18} {'Selling Price':<18} {'Est. Profit':<15}")
    print("-" * 110)
    for i in products:
        est_profit = i["selling_price"] - i["material_cost"]
        print(f"{i['id']:<12} {i['name']:<30} {i['time']:<15} ${i['material_cost']:<17.2f} ${i['selling_price']:<17.2f} ${est_profit:<14.2f}")
    print("-" * 110)
    print(f"Total Number of Products: {len(products)}")

def machine_status_report():
    report_header("MACHINE STATUS REPORT")
    statuses = {"AVAILABLE": [], "IN PRODUCTION": [], "MAINTENANCE": [], "OUT OF SERVICE": []}
    for m in machines:
        st = m.get("status", "").upper()
        if st in statuses:
            statuses[st].append(m)
    for status, machine_list in statuses.items():
        print(f"\n--- {status} MACHINES ---")
        if machine_list:
            for m in machine_list:
                print(f"ID: {m['machine_id']} | Name: {m['name']}")
        else:
            print("No machines found.")
        print(f"Total {status} Machines: {len(machine_list)}")

def maintenance_report():
    report_header("MAINTENANCE REPORT")
    if not maintenance_records:
        print("No maintenance records available.")
        print("Total Maintenance Cost: $0.00")
        return
    print(f"{'Maintenance ID':<18} {'Machine ID':<15} {'Technician ID':<17} {'Type':<18} {'Date':<15} {'Cost':<12} {'Status':<15}")
    print("-" * 115)
    total_cost = 0
    for r in maintenance_records:
        cost = r.get("Cost", 0)
        total_cost += cost
        print(f"{r.get('Maintenance ID', 'N/A'):<18} {r.get('Machine ID', 'N/A'):<15} {r.get('Technician ID', 'N/A'):<17} {r.get('Type', 'N/A'):<18} {r.get('Date', 'N/A'):<15} ${cost:<11.2f} {r.get('Status', 'N/A'):<15}")
    print("-" * 115)
    print(f"Total Records: {len(maintenance_records)} | Total Cost: ${total_cost:.2f}")

def employee_report():
    report_header("EMPLOYEE REPORT")
    if not operators:
        print("No employees available.")
        return
    print(f"{'Employee ID':<15} {'Name':<25} {'Role':<30} {'Specialization':<20} {'Shift':<12}")
    print("-" * 110)
    shift_totals = {"Morning": 0, "Evening": 0, "Night": 0}
    for i in operators:
        full_name = i["first_name"] + " " + i["last_name"]
        print(f"{i['employee_id']:<15} {full_name:<25} {i['role']:<30} {i['specialization']:<20} {i['shift']:<12}")
        if i["shift"] in shift_totals: shift_totals[i["shift"]] += 1
    print("-" * 110)
    print(f"Total Employees: {len(operators)}")
    print("\n--- SHIFT SCHEDULE ---")
    for shift, total in shift_totals.items():
        print(f"{shift} Shift: {total} Employee(s)")

def print_reports_menu():
    while True:
        report_header("REPORT MANAGEMENT MENU")
        print("1. Machine Report")
        print("2. Production Report")
        print("3. Product Report")
        print("4. Machine Status Report")
        print("5. Maintenance Report")
        print("6. Employee Report")
        print("7. Return to Main Menu")
        
        choice = input("Enter report choice (1-7): ").strip()
        if choice == '1': machine_report()
        elif choice == '2': production_report()
        elif choice == '3': product_report()
        elif choice == '4': machine_status_report()
        elif choice == '5': maintenance_report()
        elif choice == '6': employee_report()
        elif choice == '7': break
        else: print("[ERROR] Invalid choice.")


# ==========================================
# MAIN MENU LOOP
# ==========================================
def main_menu():
    print("========================================")
    print("   FACTORY AUTOMATION MANAGEMENT SYSTEM ")
    print("========================================")
    
    if not system_login():
        return

    while True:
        print("\n========================================")
        print("               MAIN MENU                ")
        print("========================================")
        print("1. Start Production Order")
        print("2. Add Machine(s)")
        print("3. Add/Update Product")
        print("4. Add Operator/Technician")
        print("5. Update Machine Status")
        print("6. Record Maintenance")
        print("7. Print Report")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            start_production_order()
        elif choice == '2':
            add_machine()
        elif choice == '3':
            sub_choice = input("Type 'add' to Add Product or 'update' to Update Product: ").strip().lower()
            if sub_choice == 'add':
                add_product()
            elif sub_choice == 'update':
                update_product()
            else:
                print("[ERROR] Invalid selection.")
        elif choice == '4':
            add_operator()
        elif choice == '5':
            update_machine_status()
        elif choice == '6':
            record_maintenance_func()
        elif choice == '7':
            print_reports_menu()
        elif choice == '8':
            print("\nExiting system. Good luck with your project presentation!")
            break
        else:
            print("\n[ERROR] Invalid choice! Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main_menu()