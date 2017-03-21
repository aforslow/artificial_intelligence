package model;

public class SImulateRobot {
	static int[][] board = new int[10][10];
	public static void main(String[] args) {
		LocalizerTest test = new LocalizerTest(10, 10, 4);
		
		try {
			while (true) {
				int[] vec = test.getCurrentTruePosition();
				board[vec[1]][vec[0]] = 1;
				for (int rows = 0; rows < 10; rows++) {
					for (int cols = 0; cols < 10; cols++) {
						System.out.print(board[rows][cols] + "  ");
					}
					System.out.println();
				}
				System.out.print("------------------------\n --------------------------\n");
				Thread.sleep(2500);
				test.update();
				board[vec[1]][vec[0]] = 0;
				
			}
		} catch (InterruptedException ex) {
			
		}
		 
	}
}
