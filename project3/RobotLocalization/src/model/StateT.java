package model;

public class StateT {
	private int direction;
	private int row;
	private int col;
	
	public StateT(int row, int col, int direction) {
		this.row = row;
		this.col = col;
		this.direction = direction;
	}
	
	public int getRow() {
		return row;
	}
	
	public int getCol() {
		return col;
	}
	
	public int getDirection() {
		return direction;
	}
	
	public int nbrOfNeighbours(int rows, int cols) {
		int sum = 0;
		sum += row - 1 >= 0 ? 1 : 0;
		sum += col - 1 >= 0 ? 1 : 0;
		sum += row + 1 < rows ? 1 : 0;
		sum += col + 1 < cols ? 1 : 0;
		return sum;
	}
	
	public boolean isNeighbour(StateT other) {
		int flag = 0;
		flag += row - 1 == other.getRow() && col == other.getCol() ? 1 : 0;
		flag += col - 1 == other.getCol() && row == other.getRow() ? 1 : 0;
		flag += row + 1 == other.getRow() && col == other.getCol() ? 1 : 0;
		flag += col + 1 == other.getCol() && row == other.getRow() ? 1 : 0;
		return flag == 1;
	}
}
