from flask import Blueprint, request, jsonify
import random

benefitspecs_bp = Blueprint('benefitspecs', __name__)

@benefitspecs_bp.route('/reconcile', methods=['POST'])
def reconcile():
    try:
        data = request.get_json()
        group_name = data.get('group_name', 'Demo Group')
        period = data.get('period', '2025-07')
        
        # Mock file processing
        files_provided = []
        if data.get('benadmin_file'):
            files_provided.append('benadmin')
        if data.get('carrier_file'):
            files_provided.append('carrier')
        if data.get('payroll_file'):
            files_provided.append('payroll')
        
        num_files = len(files_provided)
        if num_files < 2:
            return jsonify({'success': False, 'error': 'Please upload at least 2 files for reconciliation'})
        
        # Mock data generation
        total_employees = 15
        errors_found = 120
        error_rate = round((errors_found / total_employees) * 100) if total_employees > 0 else 0
        
        # Generate 120 realistic reconciliation errors for comprehensive export
        # Employee names for realistic data
        first_names = ['John', 'Sarah', 'Michael', 'Jennifer', 'David', 'Lisa', 'Robert', 'Mary', 'James', 'Patricia',
                      'William', 'Linda', 'Richard', 'Barbara', 'Joseph', 'Elizabeth', 'Thomas', 'Susan', 'Christopher', 'Jessica',
                      'Charles', 'Karen', 'Daniel', 'Nancy', 'Matthew', 'Betty', 'Anthony', 'Helen', 'Mark', 'Sandra',
                      'Donald', 'Donna', 'Steven', 'Carol', 'Paul', 'Ruth', 'Andrew', 'Sharon', 'Joshua', 'Michelle']
        
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                     'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
                     'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
                     'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores']
        
        # Error types and descriptions
        error_scenarios = [
            ('Premium Mismatch', 'Carrier premium ${amount} differs from payroll deduction ${deduction}'),
            ('Missing Coverage', 'Employee has carrier coverage but no payroll deduction recorded'),
            ('Payroll Deduction Error', 'Payroll deduction ${deduction} found but no corresponding carrier coverage'),
            ('Duplicate Deduction', 'Multiple payroll deductions found for same coverage type'),
            ('Terminated Employee', 'Coverage continues for employee terminated on {date}'),
            ('New Hire Missing', 'Employee hired on {date} but coverage not yet active'),
            ('Dependent Mismatch', 'Dependent count differs between carrier ({carrier_deps}) and payroll ({payroll_deps})'),
            ('Plan Code Error', 'Plan code mismatch: Carrier shows {carrier_plan}, Payroll shows {payroll_plan}'),
            ('Effective Date Issue', 'Coverage effective date {carrier_date} differs from payroll start {payroll_date}'),
            ('Rate Discrepancy', 'Age-based rate ${carrier_rate} differs from payroll rate ${payroll_rate}')
        ]
        
        errors = []
        for i in range(120):
            # Generate realistic employee data
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            employee_name = f"{first_name} {last_name}"
            employee_id = f"EMP{1000 + i:04d}"
            
            # Select error type and generate realistic amounts/data
            error_type, description_template = random.choice(error_scenarios)
            
            # Generate realistic amounts and data based on error type
            if 'Premium Mismatch' in error_type:
                carrier_amount = round(random.uniform(150.00, 850.00), 2)
                payroll_amount = round(carrier_amount + random.uniform(-50.00, 50.00), 2)
                description = description_template.format(amount=carrier_amount, deduction=payroll_amount)
                amount = abs(carrier_amount - payroll_amount)
            elif 'Missing Coverage' in error_type:
                amount = round(random.uniform(200.00, 600.00), 2)
                description = description_template
            elif 'Payroll Deduction Error' in error_type:
                deduction_amount = round(random.uniform(180.00, 750.00), 2)
                description = description_template.format(deduction=deduction_amount)
                amount = deduction_amount
            elif 'Duplicate Deduction' in error_type:
                amount = round(random.uniform(300.00, 900.00), 2)
                description = description_template
            elif 'Terminated Employee' in error_type:
                term_dates = ['06/15/2025', '06/30/2025', '07/01/2025', '07/15/2025']
                description = description_template.format(date=random.choice(term_dates))
                amount = round(random.uniform(250.00, 700.00), 2)
            elif 'New Hire Missing' in error_type:
                hire_dates = ['07/01/2025', '07/08/2025', '07/15/2025', '07/22/2025']
                description = description_template.format(date=random.choice(hire_dates))
                amount = round(random.uniform(200.00, 650.00), 2)
            elif 'Dependent Mismatch' in error_type:
                carrier_deps = random.randint(0, 4)
                payroll_deps = random.randint(0, 4)
                while payroll_deps == carrier_deps:
                    payroll_deps = random.randint(0, 4)
                description = description_template.format(carrier_deps=carrier_deps, payroll_deps=payroll_deps)
                amount = round(random.uniform(100.00, 400.00), 2)
            elif 'Plan Code Error' in error_type:
                carrier_plans = ['MED001', 'MED002', 'DEN001', 'VIS001', 'LIFE001']
                payroll_plans = ['M01', 'M02', 'D01', 'V01', 'L01']
                description = description_template.format(
                    carrier_plan=random.choice(carrier_plans),
                    payroll_plan=random.choice(payroll_plans)
                )
                amount = round(random.uniform(50.00, 300.00), 2)
            elif 'Effective Date Issue' in error_type:
                dates = ['07/01/2025', '07/15/2025', '08/01/2025']
                carrier_date = random.choice(dates)
                payroll_date = random.choice([d for d in dates if d != carrier_date])
                description = description_template.format(carrier_date=carrier_date, payroll_date=payroll_date)
                amount = round(random.uniform(150.00, 500.00), 2)
            else:  # Rate Discrepancy
                carrier_rate = round(random.uniform(200.00, 800.00), 2)
                payroll_rate = round(carrier_rate + random.uniform(-100.00, 100.00), 2)
                description = description_template.format(carrier_rate=carrier_rate, payroll_rate=payroll_rate)
                amount = abs(carrier_rate - payroll_rate)
            
            # Assign priority based on amount
            if amount > 500:
                priority = 'High'
            elif amount > 200:
                priority = 'Medium'
            else:
                priority = 'Low'
            
            errors.append({
                'employee_id': employee_id,
                'employee_name': employee_name,
                'error_type': error_type,
                'description': description,
                'amount': amount,
                'priority': priority,
                'status': 'Pending Review'
            })
        
        # Simple hardcoded time saved for demo consistency
        time_saved = "3.75 hrs"
        
        return {
            'success': True,
            'data': {
                'group_name': group_name,
                'period': period,
                'total_employees': total_employees,
                'errors_found': errors_found,
                'error_rate': error_rate,
                'time_saved': time_saved,
                'files_processed': num_files,
                'errors': errors
            }
        }
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@benefitspecs_bp.route('/census', methods=['POST'])
def census():
    try:
        data = request.get_json()
        group_name = data.get('group_name', 'Demo Group')
        period = data.get('period', '2025-07')
        
        # Mock census data
        return {
            'success': True,
            'data': {
                'group_name': group_name,
                'period': period,
                'total_employees': 1000,
                'average_age': 42.3,
                'average_salary': 62500,
                'average_tenure': 5.2
            }
        }
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@benefitspecs_bp.route('/benefits', methods=['POST'])
def benefits():
    try:
        data = request.get_json()
        group_name = data.get('group_name', 'Demo Group')
        period = data.get('period', '2025-07')
        
        # Mock benefits data
        return {
            'success': True,
            'data': {
                'group_name': group_name,
                'period': period,
                'total_employees': 1000,
                'recommended_plans': 5,
                'estimated_participation': 78,
                'annual_premium': 450000
            }
        }
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

