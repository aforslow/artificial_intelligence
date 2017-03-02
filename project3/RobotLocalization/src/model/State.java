package model;

public class State {
	private int direction;
	private int row;
	private int col;
	
	public State(int row, int col, int direction) {
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
}
