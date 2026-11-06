$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
try {
    $path = (Resolve-Path 'scratch/test_rebuilt_catalog_out.xlsx').Path
    $wb = $excel.Workbooks.Open($path)
    Write-Host "Workbook opened successfully!"
    
    # Check 'شستشو و نظافت'
    $ws = $wb.Sheets.Item("شستشو و نظافت")
    Write-Host "Sheet name: $($ws.Name)"
    Write-Host "Total rows in used range: $($ws.UsedRange.Rows.Count)"
    
    Write-Host "Row 100 Col 1: $($ws.Cells.Item(100, 1).Text)"
    Write-Host "Row 101 Col 1: $($ws.Cells.Item(101, 1).Text)"
    Write-Host "Row 101 Col 8: $($ws.Cells.Item(101, 8).Text)"
    Write-Host "Row 101 Col 18: $($ws.Cells.Item(101, 18).Text)"
    Write-Host "Row 101 Col 1 Interior Color (CF): $($ws.Cells.Item(101, 1).DisplayFormat.Interior.Color)"
    
    # Check Dashboard
    $wsDash = $wb.Sheets.Item("📊 خلاصه و داشبورد")
    Write-Host "Dashboard Row 5 Col 2 (Total Main): $($wsDash.Cells.Item(5, 2).Text)"
    Write-Host "Dashboard Row 5 Col 3 (Site Reg): $($wsDash.Cells.Item(5, 3).Text)"
    Write-Host "Dashboard Row 5 Col 5 (In Stock): $($wsDash.Cells.Item(5, 5).Text)"
    
    $wb.Close($false)
} finally {
    $excel.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
}
