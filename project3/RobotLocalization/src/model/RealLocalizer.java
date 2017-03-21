package model;

import control.EstimatorInterface;
import java.util.Random;
public class RealLocalizer implements EstimatorInterface {
		
	private int rows, cols, head, x, y, direction, nbrStates;
	private int rX, rY;
	private State[] observations;
	private double[][] transMatrix;
	public static Random rand = new Random();
	private int observationCounter = 0;
	
	MatrixCreator c;



	public RealLocalizer( int rows, int cols, int head) {
		this.rows = rows;
		this.cols = cols;
		this.head = head;
		nbrStates = rows*cols*head;
		x = rand.nextInt(rows);
		y = rand.nextInt(cols);
		direction = rand.nextInt(head) + 1;
		c = new MatrixCreator(rows, cols, head);
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
		//Translating the direction so it suits our structure
		h = 3 - (h + 3)%4;
		nH = 3 - (nH + 3)%4;
		
		return c.getTProb(y, x, h%4, nY, nX, (nH)%4);
	}

	public double getOrXY( int rX, int rY, int x, int y) {
		int tempCol = Math.abs(rX - x);
		int tempRow = Math.abs(rY - y);
		if (2 == tempRow  && 2 >= tempCol) {
			return 0.025;
		} else if (tempRow <= 1 && tempCol == 2) {
			return 0.025;
		} else if (tempRow == 1 && tempCol <= 1) {
			return 0.05;
		} else if (tempRow == 0 && tempCol == 1) {
			return 0.05;
		} else if (tempCol + tempRow == 0) {
			return 0.1;
		} else {
			return 0;
		}
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
		int rX = -1;
		int rY = -1;
		boolean check = false;
		int area = rand.nextInt(10) + 1;
		if (area == 1) {
			rX = x;
			rY = y;
		} else if (1 < area && area < 6) {
			int[] temp = translateNbrCircle(true);
			rX = x - temp[1];
			rY = y - temp[0];
			if (!UtilityModel.isInside(rX, rY, rows, cols)) {
				this.rX = -1;
				this.rY = -1;
				check = true;
			}
		} else if (6 <= area && area < 10) {
			int[] temp = translateNbrCircle(false);
			rX = x - temp[1];
			rY = y - temp[0];
			if (!UtilityModel.isInside(rX, rY, rows, cols)) {
				this.rX = -1;
				this.rY = -1;
				check = true;
			}
		} else {
			this.rX = -1;
			this.rY = -1;
			check = true;			
		}
		c.localizationOfRobot(rX, rY);
		return check ?  null : new int[]{rX, rY};
	}

	
	private int[] translateNbrCircle(boolean innerCircle) {
		if (innerCircle) {
			return UtilityModel.inner[rand.nextInt(8)];
		} else {
			return UtilityModel.outer[rand.nextInt(16)];
		}
	}

	public double getCurrentProb( int x, int y) {
		return c.getStateProb(x, y);
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
	}
	
	
}