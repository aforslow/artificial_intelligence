package model;

import control.EstimatorInterface;
import java.util.Random;
public class LocalizerTest implements EstimatorInterface {
		
	private int rows, cols, head, x, y, direction, nbrStates;
	private StateT[] maping;
	private double[] stateProb;
	private double[][] transMatrix;
	public static Random rand = new Random();
	private int observationCounter = 0;
	



	public LocalizerTest( int rows, int cols, int head) {
		this.rows = rows;
		this.cols = cols;
		this.head = head;
		nbrStates = rows*cols*head;
		x = rand.nextInt(rows);
		y = rand.nextInt(cols);
		direction = rand.nextInt(head) + 1;
		
		maping = new StateT[nbrStates];
		transMatrix = new double[nbrStates][nbrStates];
		stateProb = new double[nbrStates];
		
		
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
		After that we generate a number to determine which square in that
		circle we wanna get. Here is what it would look like

		1  2  3			1  2  3  4  5
		4  x  5			6  x  x  x  7
		6  7  8 		8  x  X  x  9
						10 x  x  x  11
						12 13 14 15 16
	*/

	
	public int[] getCurrentReading() {
		int[] ret = new int[2];
		int rX;
		int rY;
		int area = rand.nextInt(10) + 1;
		if (area == 1) {
			rX = x;
			rY = y;
		} else if (1 < area && area < 6) {
			int[] temp = translateNbrCircle(true);
			rX = x - temp[1];
			rY = y - temp[0];
			ret = new int[]{rX, rY};
			if (!UtilityModel.isInside(rX, rY, rows, cols)) {
				return null;
			}
		} else if (6 <= area && area < 10) {
			int[] temp = translateNbrCircle(false);
			rX = x - temp[1];
			rY = y - temp[0];
			if (!UtilityModel.isInside(rX, rY, rows, cols)) {
				return null;
			}
		} else {
			rX = -1;
			rY = -1;
			
		}
		ret[0] = rX;
		ret[1] = rY;
		
		return ret;
	}

	
	private int[] translateNbrCircle(boolean innerCircle) {
		if (innerCircle) {
			return UtilityModel.inner[rand.nextInt(8)];
		} else {
			return UtilityModel.outer[rand.nextInt(16)];
		}
	}

	public double getCurrentProb( int x, int y) {
		double ret = 0.0;
		return ret;
	}
	
	public void update() {
		int change = rand.nextInt(10);
		if (change <= 6) {
			while (!UtilityModel.validDirection(x, y, rows, cols, direction)) {
				direction = rand.nextInt(head) + 1;
			}
		} else {
			do {
				int tempDirection = rand.nextInt(head) + 1;
				while (tempDirection == direction) {
					tempDirection = rand.nextInt(head) + 1;
				}
				direction = tempDirection;
			
			} while (!UtilityModel.validDirection(x, y, rows, cols, direction));
		}
		
		switch (direction) {
		case UtilityModel.LEFT:
			x--;
			break;
		case UtilityModel.UP:
			y--;
			break;
		case UtilityModel.RIGHT:
			x++;
			break;
		case UtilityModel.DOWN:
			y++;
			break;
		}
		
		//new state
//		int[] temp = getCurrentReading();
//		observations[observationCounter++] = new State(temp[1], temp[0], direction);
		
	}
	
	
}