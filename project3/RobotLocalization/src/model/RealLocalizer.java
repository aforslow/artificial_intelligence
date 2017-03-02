package model;

import control.EstimatorInterface;
import java.util.Random;
public class RealLocalizer implements EstimatorInterface {
		
	private int rows, cols, head, x, y, direction;
	public static Random rand = new Random();



	public RealLocalizer( int rows, int cols, int head) {
		this.rows = rows;
		this.cols = cols;
		this.head = head;

		x = rand.randInt(rows);
		y = rand.randInt(cols);
		direction = rand.randInt(head) + 1;
		
	}	
	
	public int getNumRows() {
		return rows;
	}
	
	public int getNumCols() {
		return cols;
	}
	
	public int getNumHead() {
		return head;
	}
	
	public double getTProb( int x, int y, int h, int nX, int nY, int nH) {
		return 0.0;
	}

	public double getOrXY( int rX, int rY, int x, int y) {
		return 0.1;
	}


	public int[] getCurrentTruePosition() {
		
		int[] ret = new int[2];
		ret[0] = x;
		ret[1] = y;
		return ret;

	}

	/*
		First we generate which area, that is if it's the true
		location, the inner circle, outer circle or a faulty reading.
		After that we generate a number to determain whih square in that
		circle we wanna get. Here is what it would look like

		1  2  3			1  2  3  4  5
		4  x  5			6  x  x  x  7
		6  7  8 		8  x  O  x  9
						10 x  x  x  11
						12 13 14 15 16
	*/

	private int[][] inner = {
		{-1, -1},
		{0, -1},
		{1, -1},
		{-1, 0},
		{1, 0},
		{-1, 1},
		{0, 1},
		{1, 1}
	}
	private int[][] outer = {
		{-2, -2},
		{-1, -2},
		{0, -2},
		{1, -2},
		{2, -2},
		{-2, -1},
		{2, -1},
		{-2, 0},
		{2, 0},
		{-2, 1},
		{2, 1},
		{-2, 2},
		{-1, 2},
		{0, 2},
		{1, 2},
		{2, 2},
	}
	public int[] getCurrentReading() {
		int[] ret = null;
		int area = rand.nextInt(10) + 1;
		if (area == 1) {
			ret = {x, y};
		} else if (1 < area && area < 6) {
			int[] temp = translateNbrCircle(true);
			rX = x - temp[1];
			rY = y - temp[0];
			ret = {rX, rY};
			if (isInside(rX, rY)) {
				return {-1, -1};
			}
		} else if (6 <= area && area < 10) {
			int[] temp = translateNbrCircle(false);
			rX = x - temp[1];
			rY = y - temp[0];
			ret = {rX, rY};
			if (isInside(rX, rY)) {
				return {-1, -1};
			}
		} else {
			ret = {-1, -1};
		}
		return ret;
	}

	private boolean isInside(int x, int y) {
		if (x < 0 || x >= cols || y < 0 || y >= rows) {
			return false;
		}
		return true;
	}

	private int[] translateNbrCircle(boolean innerCircle, int nbr) {
		if (innerCircle) {
			return inner[rand.nextInt(8)];
		} else {
			return outer[rand.nextInt(16)];
		}
	}

	public double getCurrentProb( int x, int y) {
		double ret = 0.0;
		return ret;
	}
	
	public void update() {
		
	}
	
	
}