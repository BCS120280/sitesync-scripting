def excelToDataSet(fileName, hasHeaders = False, sheetNum = 0, firstRow = None, lastRow = None, firstCol = None, lastCol = None):
	import org.apache.poi.ss.usermodel.WorkbookFactory as WorkbookFactory
	import org.apache.poi.ss.usermodel.DateUtil as DateUtil
	from java.io import ByteArrayInputStream
	from java.util import Date
	
	"""
	   Function to create a dataset from an Excel spreadsheet. It will try to automatically detect the boundaries of the data,
	   but helper parameters are available:
	   params:
	   		fileName   - The path to the Excel spreadsheet. (required)
	   		hasHeaders - If true, uses the first row of the spreadsheet as column names.
	   		sheetNum   - select the sheet to process. defaults to the first sheet.
	   		firstRow   - select first row to process. 
	   		lastRow    - select last row to process.
	   		firstCol   - select first column to process
	   		lastCol    - select last column toprocess
	"""
	
	fileStream = ByteArrayInputStream(fileName)

	wb = WorkbookFactory.create(fileStream)
	
	sheet = wb.getSheetAt(sheetNum)

	if firstRow is None:
		firstRow = sheet.getFirstRowNum()
	if lastRow is None:
		lastRow = sheet.getLastRowNum()

	data = []
	for i in range(firstRow , lastRow + 1):
		row = sheet.getRow(i)
		print str(i).zfill(3), list(row)
		if i == firstRow:
			if firstCol is None:
				firstCol = row.getFirstCellNum()

			if lastCol is None:
				lastCol  = row.getLastCellNum()
			else:
				# if lastCol is specified add 1 to it.
				lastCol += 1
			if hasHeaders:
				headers = list(row)[firstCol:lastCol]
			else:
				headers = ['Col'+str(cNum) for cNum in range(firstCol, lastCol)] 
		
		rowOut = []
		for j in range(firstCol, lastCol):
			if i == firstRow and hasHeaders:
				pass
			else:
				cell = row.getCell(j)
				system.perspective.print(cell)
				try:
					cellType = cell.getCellType().toString()
					if cellType == 'NUMERIC':
						if DateUtil.isCellDateFormatted(cell):
							value =  cell.dateCellValue.toString()
						else:
							value = cell.getNumericCellValue()
							if value == int(value):
								value = str(value)

						
					elif cellType == 'STRING':
						try:
							value = cell.getStringCellValue()
						except:
							value = "error loading"
					elif cellType == 'BOOLEAN':
						value = str(cell.getBooleanCellValue())
					elif cellType == 'BLANK':
						value = ""	
					elif cellType == 'FORMULA':
						formulatype=str(cell.getCachedFormulaResultType())
						if formulatype == 'NUMERIC':
							if DateUtil.isCellDateFormatted(cell):
								value =  cell.dateCellValue.toString()
							else:
								value = cell.getNumericCellValue().toString()
								
						elif formulatype == 'STRING':
							value = cell.getStringCellValue()
						elif formulatype == 'BOOLEAN':
							value = cell.getBooleanCellValue().toString()
						elif formulatype == 'BLANK':
							value = ""
					else:
						value = None	
				except Exception as e:
					system.perspective.print(e)
					
					value = ""
				rowOut.append(value)
		if len(rowOut) > 0:
			data.append(rowOut)

	
	fileStream.close()
	try:
		dataset = system.dataset.toDataSet(headers, data)
	except Exception as e:
		dataset = None

		system.perspective.print(e)
		system.perspective.print(headers)
		system.perspective.print(data)
	
	return dataset
