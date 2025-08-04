// Helper functions for processing real data

function generateInsights(data) {
    const totalEmployees = data.total_employees || 0;
    const errorsFound = data.errors_found || 0;
    const errorRate = data.error_rate || 0;
    const errors = data.errors || [];
    
    let insights = [];
    
    // Error rate insight
    if (errorRate > 15) {
        insights.push(`<div class="insight-item"><strong>High Error Rate:</strong> ${errorRate}% error rate indicates significant discrepancies between payroll and carrier data</div>`);
    } else if (errorRate > 5) {
        insights.push(`<div class="insight-item"><strong>Moderate Error Rate:</strong> ${errorRate}% error rate shows some discrepancies that need attention</div>`);
    } else {
        insights.push(`<div class="insight-item"><strong>Low Error Rate:</strong> ${errorRate}% error rate indicates good data alignment</div>`);
    }
    
    // Error type analysis
    const errorTypes = {};
    errors.forEach(error => {
        errorTypes[error.error_type] = (errorTypes[error.error_type] || 0) + 1;
    });
    
    const mostCommonError = Object.keys(errorTypes).reduce((a, b) => errorTypes[a] > errorTypes[b] ? a : b, '');
    if (mostCommonError) {
        insights.push(`<div class="insight-item"><strong>Primary Issue:</strong> ${mostCommonError} errors are most common (${errorTypes[mostCommonError]} occurrences)</div>`);
    }
    
    // High priority errors
    const highPriorityErrors = errors.filter(error => error.priority === 'High').length;
    if (highPriorityErrors > 0) {
        insights.push(`<div class="insight-item"><strong>Urgent Attention:</strong> ${highPriorityErrors} high-priority errors require immediate review</div>`);
    }
    
    // Process efficiency
    const timeSaved = data.time_saved || '0 hrs';
    if (parseFloat(timeSaved) > 0) {
        insights.push(`<div class="insight-item"><strong>Process Efficiency:</strong> Automated reconciliation saved ${timeSaved} of manual work</div>`);
    }
    
    return insights.join('');
}

function formatErrorList(errors) {
    if (!errors || errors.length === 0) {
        return '<div style="text-align: center; color: #6b7280; padding: 20px;">No errors found in the reconciliation.</div>';
    }
    
    // Show first 3 errors in detail
    const displayErrors = errors.slice(0, 3);
    let errorHtml = '';
    
    displayErrors.forEach((error, index) => {
        const borderStyle = index < displayErrors.length - 1 ? 'border-bottom: 1px solid #f3f4f6;' : '';
        errorHtml += `
            <div style="padding: 10px 0; ${borderStyle}">
                <strong>${error.employee_name} (${error.employee_id})</strong><br>
                <span style="color: #dc2626;">${error.error_type}: $${error.amount.toFixed(2)} difference</span><br>
                <span style="color: #6b7280; font-size: 0.875rem;">${error.description}</span>
            </div>
        `;
    });
    
    // Add summary if there are more errors
    if (errors.length > 3) {
        errorHtml += `
            <div style="padding: 10px 0; text-align: center; color: #6b7280; font-style: italic;">
                ... and ${errors.length - 3} more errors (see export for complete list)
            </div>
        `;
    }
    
    return errorHtml;
}

