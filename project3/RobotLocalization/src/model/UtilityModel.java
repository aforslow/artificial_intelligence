package model;

public class UtilityModel {
	
	final static int LEFT = 1;
	final static int UP = 2;
	final static int RIGHT = 3;
	final static int DOWN = 4;
	
	static boolean validDirection(int x, int y, int rows, int cols, int direction) {
		switch (direction) {
		case LEFT:
			return 0 < x - 1;
		case UP:
			return 0 < y - 1;
		case RIGHT:
			return cols > x + 1;
		case DOWN:
			return rows > y + 1;
		default:
			return false;
		}
	}
	
	static public int[][] inner = {
			{-1, -1},
			{0, -1},
			{1, -1},
			{-1, 0},
			{1, 0},
			{-1, 1},
			{0, 1},
			{1, 1}
		};
	public static int[][] outer = {
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
		};
	
	public static boolean isInside(int x, int y, int cols, int rows) {
		if (x < 0 || x >= cols || y < 0 || y >= rows) {
			return false;
		}
		return true;
	}
}
