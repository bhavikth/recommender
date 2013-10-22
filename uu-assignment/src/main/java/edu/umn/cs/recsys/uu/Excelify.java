package edu.umn.cs.recsys.uu;

import it.unimi.dsi.fastutil.longs.LongList;
import it.unimi.dsi.fastutil.longs.LongSet;
import it.unimi.dsi.fastutil.longs.LongSortedSet;

import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.SortedSet;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.grouplens.lenskit.vectors.MutableSparseVector;
import org.grouplens.lenskit.vectors.VectorEntry;

import com.google.common.collect.Maps;

public class Excelify {
	
	private static Map<Long, MutableSparseVector> movieRatings(XSSFSheet sheet){
		Iterator<Row> rows = sheet.rowIterator();
		Row headerRow = rows.next();
		
		Iterator<Cell> headerCells = headerRow.iterator();
		
		Map<Integer,Long> columnTitles = new HashMap<Integer,Long>();
		while (headerCells.hasNext()) {
			Cell header = headerCells.next();
			columnTitles.put(header.getColumnIndex(), (long) header.getNumericCellValue());
		}
		
		Map<Long,MutableSparseVector> ratings = new HashMap<Long, MutableSparseVector>();
		
		while(rows.hasNext()) {
			Row row = rows.next();
			Iterator<Cell> cells = row.cellIterator();
			Cell movieTitleCell = cells.next(); 
			String movieTitle = movieTitleCell.getStringCellValue();
			Long movieId = Long.parseLong(movieTitle.split(":")[0]);
			ratings.put(movieId, MutableSparseVector.create(columnTitles.values()));
			
			while(cells.hasNext()) {
				Cell cell = cells.next();
				Long columnTitle = columnTitles.get(cell.getColumnIndex());
				ratings.get(movieId).set(columnTitle, (float) cell.getNumericCellValue());		
			}
		}
		return ratings;
	}
	
	private static Map<Long,MutableSparseVector> userRatings(Map<Long, MutableSparseVector> movieRatings){
//		SortedSet<Long> users = movieRatings.values().iterator().next().keySet();
		Set<Long> movies = movieRatings.keySet();
		Map<Long, MutableSparseVector> userVectors = new HashMap<Long, MutableSparseVector>();
		for (Entry<Long,MutableSparseVector> entry:movieRatings.entrySet()) {
			Long movieId = entry.getKey();
			
			for (VectorEntry rating:entry.getValue().fast()) {
				if (!userVectors.containsKey(rating.getKey())) {
					userVectors.put(rating.getKey(), MutableSparseVector.create(movies));
				}
				userVectors.get(rating.getKey()).set(movieId, rating.getValue());
			}
		}
		return userVectors;
		
	}
	public static void main(String[] args) throws IOException {
		long[] tgt_users = new long[] {3712};
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
		
		Map<Long,MutableSparseVector> correlations = new HashMap<Long, MutableSparseVector>();
		
		while(rows.hasNext()) {
			Row row = rows.next();
			Iterator<Cell> cells = row.cellIterator();
			Long rowTitle = (long) cells.next().getNumericCellValue();
			correlations.put(rowTitle, MutableSparseVector.create(columnTitles.values()));
			while(cells.hasNext()) {
				Cell cell = cells.next();
				Long columnTitle = columnTitles.get(cell.getColumnIndex());
				correlations.get(rowTitle).set(columnTitle, (float) cell.getNumericCellValue());		
			}
		}
		Map<Long,MutableSparseVector> userVectors = userRatings(movieRatings(matrix));
		
		for (long user:tgt_users) {
			MutableSparseVector userVector = userVectors.get(user);
			MutableSparseVector userNormVector = userVector.copy();
			double userMean = userVector.mean();
			
			
			MutableSparseVector correlation = correlations.get(user);
			LongList topNeighbors = correlation.keysByValue(true).subList(1, 6);
			
			Set<Long> movieSet = new HashSet<Long>(userVector.keySet());
			for (long neighbor:topNeighbors) {
				System.out.print(neighbor+" "+correlation.get(neighbor)+"\n");
				movieSet.retainAll(userVectors.get(neighbor).keySet());
			}
			
			for (long movie:userVector.keySet()) {
				double pui = 0;
	        	double sum = 0;
				for (long neighbor:topNeighbors) {
					MutableSparseVector neighborVector = userVectors.get(neighbor);
						double rv_mean = neighborVector.mean();
						
						double rvi = neighborVector.containsKey(movie)?neighborVector.get(movie):0;
						pui += correlation.get(neighbor)*(rvi);
						sum += Math.abs(correlation.get(neighbor));
						
				}
				pui = (pui/sum);
				userNormVector.set(movie,pui);
			}
			System.out.println();
			for (Long tMovie:userNormVector.keysByValue(true).subList(0, 3)) {
				System.out.println (tMovie+" "+userNormVector.get(tMovie));
			}
		}
		
		
		
		        
		
		
		
		
	}
}
