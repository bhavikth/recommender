package edu.umn.cs.recsys.uu;

import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

public class Excelify {
	public static void main(String[] args) throws IOException {
		InputStream is = new BufferedInputStream(new FileInputStream("data/Book1.xlsx"));
		
		XSSFWorkbook wb = new XSSFWorkbook(is);
		
		XSSFSheet matrix = wb.getSheet("Sheet1");
		XSSFSheet correl = wb.getSheet("Sheet2");
		
		Iterator<Row> rows = correl.rowIterator();
		Row headerRow = rows.next();
		
		Iterator<Cell> headerCells = headerRow.iterator();
		
		
		Map<Integer,Long> columnTitles = new HashMap<Integer,Long>();
		while (headerCells.hasNext()) {
			Cell header = headerCells.next();
			columnTitles.put(header.getColumnIndex(), (long) header.getNumericCellValue());
		}
		Map<Long,Map<Long,Float>> correlations = new HashMap<Long, Map<Long,Float>>();
		
		while(rows.hasNext()) {
			Row row = rows.next();
			Iterator<Cell> cells = row.cellIterator();
			Long rowTitle = (long) cells.next().getNumericCellValue();
			correlations.put(rowTitle, new HashMap<Long, Float>());
			while(cells.hasNext()) {
				Cell cell = cells.next();
				Long columnTitle = columnTitles.get(cell.getColumnIndex());
				correlations.get(rowTitle).put(columnTitle, (float) cell.getNumericCellValue());		
			}
		}
		
		System.out.println(correlations.get(1648L).get(5136L)+"=0.40298");
		System.out.println(correlations.get(918L).get(2824L)+"=-0.31706");
		        
		
		
		
		
	}
}
