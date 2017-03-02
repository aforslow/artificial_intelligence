package model;

public class TestUtilityModel {
	static double[][] board = new double[5][5];
	public static void main(String [] args) {
		int[] temp = UtilityModel.outer[5];
		int row = 2 + temp[1];
		int col = 2 + temp[0];
		
		board[row][col] = 1;
		
		for (int i = 0; i < 5; i++) {
			for (int j = 0; j < 5; j++) {
				System.out.print(board[i][j] + " ");
			}
			System.out.print("\n");
		}
		
		
		
		
		
	}
}
