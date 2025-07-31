from flask import Blueprint, request, jsonify
import random
import sys
import os

# Add the src directory to the path to import file_processor
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.file_processor import FileProcessor

benefitspecs_bp = Blueprint('benefitspecs', __name__)

@benefitspecs_bp.route('/reconciliation', methods=['POST'])
def reconciliation():
    try:
        # Handle FormData from frontend
        group_name = request.form.get('group_name', 'Demo Group')
        period = request.form.get('period', '2025-07')
        
        # Check for uploaded files
        files_provided = []
        uploaded_files = {}
        
        if 'benadmin_file' in request.files and request.files['benadmin_file'].filename:
            files_provided.append('benadmin')
            uploaded_files['benadmin_file'] = request.files['benadmin_file']
            
        if 'carrier_file' in request.files and request.files['carrier_file'].filename:
            files_provided.append('carrier')
            uploaded_files['carrier_file'] = request.files['carrier_file']
            
        if 'payroll_file' in request.files and request.files['payroll_file'].filename:
            files_provided.append('payroll')
            uploaded_files['payroll_file'] = request.files['payroll_file']
        
        num_files = len(files_provided)
        if num_files < 2:
            return jsonify({'success': False, 'error': 'Please upload at least 2 files for reconciliation'})
        
        # Process actual uploaded files
        processor = FileProcessor()
        analysis_data = processor.process_files(uploaded_files)
        
        # Add metadata
        analysis_data['group_name'] = group_name
        analysis_data['period'] = period
        
        return {
            'success': True,
            'data': analysis_data
        }
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error processing files: {str(e)}'})

@benefitspecs_bp.route('/census', methods=['POST'])
def census():
    try:
        # Handle FormData from frontend
        group_name = request.form.get('group_name', 'Demo Group')
        period = request.form.get('period', '2025-07')
        
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

@benefitspecs_bp.route('/benefit-analysis', methods=['POST'])
def benefit_analysis():
    try:
        # Handle FormData from frontend
        group_name = request.form.get('group_name', 'Demo Group')
        period = request.form.get('period', '2025-07')
        
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

