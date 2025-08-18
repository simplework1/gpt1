def format_kpi_dict(kpi_dict):
    """
    Converts a dict like:
    {
        "Revenue from operations": {"FY22": "2648.55 INR", "FY23": "3666.92 INR"},
        "EBITDA": {"FY22": "1200 INR", "FY23": "1500 INR"}
    }
    into a formatted string with separators.
    """
    blocks = []
    
    for kpi_name, period_values in kpi_dict.items():
        lines = []
        
        # Take first value to show in the "Actual KPI" line
        first_val = next(iter(period_values.values()), "")
        lines.append(f"{kpi_name} : {first_val}")
        
        # Add all period-value pairs
        for period, val in period_values.items():
            lines.append(f"{period} : {val}")
        
        # Add separator
        lines.append("————————————")
        
        blocks.append("\n".join(lines))
    
    return "\n".join(blocks)