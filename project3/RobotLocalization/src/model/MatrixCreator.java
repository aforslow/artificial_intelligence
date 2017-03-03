package model;

import java.util.LinkedList;

public class MatrixCreator {
	private int rows, cols, nDirections;
	private double[][] transitionMatrix;
	private double[] stateProb;
	private State[] stateMap;
	
	private int nbrStates;

	public MatrixCreator(int rows, int cols, int nDirections) {
		this.rows = rows;
		this.cols = cols;
		this.nDirections = nDirections;
		nbrStates = rows*cols*nDirections;
		createTransitionMatrix();
		createStateProbMatrix();
		createStateMapMatrix();
//		createObservationMatrix();
	}
	
	private void createStateMapMatrix() {
		stateMap = new State[nbrStates];
		int counter = 0;
		for (int i = 0; i<rows; i++) {
			for (int j = 0; j<cols; j++) {
				for (int n = 1; n<5; n++) {
					State temp = new State(i, j, n);
					stateMap[counter] = temp;
					counter++;
				}
			}
		}
		
		
		
	}
	
	private void createTransitionMatrix() {
		transitionMatrix = new double[rows*cols*nDirections][rows*cols*nDirections];
		for (int state = 0; state < rows * cols * nDirections; state++) {
			for (int row = 0; row < rows; row++) {
				for (int col = 0; col < cols; col++) {
					for (int direction = 0; direction < nDirections; direction++) {
						distributeProbability(row, col, direction);
					}
				}
			}
		}
	}
	
	private void createStateProbMatrix() {
		stateProb = new double[rows*cols*nDirections];
		for (int i = 0; i < rows*cols*nDirections; i++) {
			stateProb[i] = 1.0/(rows*cols*nDirections);
		}
	}
	
	public void printTransitionMatrix() {
		for (int row=0; row < rows*cols*nDirections; row++) {
			for (int col=0; col < rows*cols*nDirections; col++) {
				System.out.print(transitionMatrix[row][col] + " ");
			}
			System.out.println();
		}
	}
	
	private void distributeProbability(int row, int col, int direction) {
		State currState = new State(row, col, direction);
		State nextState = getNextState(row, col, direction);
		double pointDistribution = getLeftovers(currState, nextState);
		LinkedList<State> alternativeNextStates = getAltStates(currState);
		double nGoodTransitions = (double) alternativeNextStates.size();
		for (State s : alternativeNextStates) {
			setTransitionProb(currState, s, pointDistribution / nGoodTransitions);
		}
	}
	
	private LinkedList<State> getAltStates(State currState) {
		LinkedList<State> states = new LinkedList<State>();
		int currDirection = currState.getDirection();
		for (int dir=0; dir < nDirections; dir++) {
			State nextState = getNextState(currState.getRow(), currState.getCol(), dir);
			if (stateExists(nextState) && (dir != currDirection)) {
				states.add(nextState);
			}
		}
		return states;
	}
	
	public double[] getObsMatrix(State obState) {
		double[] obs = new double[nbrStates];
		
		obs = createObsFromObservation(obs, obState);
		return obs;
	}
	
	private double[] createObsFromObservation(double[] obs, State obState) {
		
		if (!obState.isNothing()) {
			for (int i = 0; i<nbrStates; i++) {
				double probSum = 0.1;
				probSum += 0.05*checkNeighboursOutside(stateMap[i], 1);
				probSum += 0.025*checkNeighboursOutside(stateMap[i], 2);
				obs[i] = probSum;
			}
		} else {
			for (int i = 0; i<nbrStates; i++) {
				if (obState == null) {
					System.out.println("banan");
				}
				if (obState.getRow() == stateMap[i].getRow() && obState.getCol() == stateMap[i].getCol()) {
					obs[i] = 0.1;
				} else if (closeBy(obState, i, 1)) {
					obs[i] = 0.05;
				} else if (closeBy(obState, i, 2)) {
					obs[i] = 0.025;
				} else {
					obs[i] = 0.0;
				}
			}
		}
		
		return obs;
	}
	
	private boolean closeBy(State obState, int index, int step) {
		int row = obState.getRow();
		int col = obState.getCol();
		
		int rV = stateMap[index].getRow();
		int cV = stateMap[index].getCol();
		for (int i = row - step; i<=row+step; i++) {
			for (int j = col - step; j<=col+step; j++) {
				if (i == row && j == col) {
					continue;
				}
				if (rV == row && col == cV) {
					return true;
				}
			}
		}
		return false;
	}
	
	private int checkNeighboursOutside(State state, int size) {
		int neighbours = 0;
		
		int row = state.getRow();
		int col = state.getCol();
		
		for (int i = row - size; i<= row + size; i++) {
			for (int j = col - size; j<= col + size; j++) {
				if (Math.abs(row - i) == size || Math.abs(col - j) == size) {
					if (outsideMatrix(i, j)) {
						neighbours++;
					}
				}
			}
		}
		
		
		return neighbours;
	}
	
	public State localizationOfRobot(int row, int col) {
		State temp = new State(row, col, 1);
		int index = hiddenMM(temp);
		return stateMap[index];
	}
	
	private int hiddenMM(State sensor) {
		double temp[] = new double[nbrStates];
		double alpha = fixTempAndAlpha(getObsMatrix(sensor), temp);
//		System.out.println(alpha);
		return guessState(temp, 1/ alpha);
	}
	
	private double fixTempAndAlpha(double[] obs, double[] temp) {
//		for (int i = 0; i < nbrStates; i++) {
//			System.out.println(obs[i]);
//		}
		int counterS = 0;

		double alpha = 0;
		for (int r = 0; r < nbrStates; r++) {
			temp[r] = 0;
			for (int i = 0; i<nbrStates; i++) {
				temp[r] += transitionMatrix[i][r] * stateProb[i] * obs[i];
			}
			if (temp[r] != 0){
				System.out.println("banan   " + temp[r]);
			}
			alpha += temp[r];

//			System.out.println(temp[r]);
		
		}
		System.out.println("Gurka   " + alpha + "-----------------------------------");
		System.out.println("Gurka2   " + 1/alpha);
		for (int i = 0; i<nbrStates; i++) {
//			if (stateProb[i] == i || transitionMatrix[i][2] == 0) {
//				counterS++;
//			}
		}
		if (counterS == nbrStates*nbrStates) {
			System.out.println("Banan");
		}
		return alpha;
	}
	
	private int guessState(double[] temp, double alpha) {
		int guess = -1;
		double max = Integer.MIN_VALUE;
		System.out.println("Morot   " + alpha);
		for (int i = 0; i<nbrStates; i++) {
			stateProb[i] = temp[i]*alpha;
//			System.out.println(temp[i] + " temp  " + alpha);
			if (temp[i] > max) {
				guess = i;
				max = temp[i];
			}
		}
//		System.out.println("---------------------------");
		
		return guess;
	}
	
	private boolean outsideMatrix(int row, int col) {
		return row < 0 || row >= rows || col < 0 || col >= cols;
	}
	
	private State getNextState(int row, int col, int direction) {
		switch (direction){
			case 0:
				return new State(row, col-1, direction);
			case 1:
				return new State(row-1, col, direction);
			case 2:
				return new State(row, col+1, direction);
			case 3:
				return new State(row+1, col, direction);
			default:
				return new State(-1, -1, -1);
		}
	}
	
	private double getLeftovers(State currState, State nextState) {
		if (!stateExists(nextState)) {
			return 1.0;
		}
		setTransitionProb(currState, nextState, 0.7);
		return 0.3;
	}
	
	private boolean stateExists(State state) {
		int row = state.getRow();
		int col = state.getCol();
		if ((row >= 0 && row < rows) && (col >= 0 && col < cols)) {
			return true;
		}
		return false;
	}
	
	private void setTransitionProb(State currState, State nextState, double probability) {
		int currStateIdx = getStateIdx(currState);
		int nextStateIdx = getStateIdx(nextState);
		transitionMatrix[currStateIdx][nextStateIdx] = probability;
	}
	
	private int getStateIdx(State state) {
		int row = state.getRow();
		int col = state.getCol();
		int dir = state.getDirection();
		return col*nDirections + dir + row*cols*nDirections;
	}
	
	public double getTProb(int row, int col, int h, int rRow, int rCol, int rH) {
		int currStateIdx = getStateIdx(new State(row, col, h));

		int nextStateIdx = getStateIdx(new State(rRow, rCol, rH));
//		return transitionMatrix[0][7];
		System.out.println(row + " " + col + " " + h + "   " + rRow + " " + rCol + " " + rH + "    " + transitionMatrix[row*rows+col*cols + h][rRow*rows+rCol*cols + rH]);
		return transitionMatrix[currStateIdx][nextStateIdx];
	}
	
	public double getStateProb(int row, int col) {
		double sum = 0;
		for (int i = 0; i < 4; i++) {
			sum += stateProb[rows*row + cols*col + i];
		}
		return sum;
	}
	
	public static void main(String[] args) {
		MatrixCreator mc = new MatrixCreator(3, 3, 4);
		mc.printTransitionMatrix();
	}
}
