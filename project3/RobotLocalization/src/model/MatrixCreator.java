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
	}

	/*
	 * Creates a matrix that maps a state to a point
	 */
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
	
	/*
	 * Creates the transition matrix
	 */
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
	
	/*
	 * Creates a array with the probability for each state
	 */
	private void createStateProbMatrix() {
		stateProb = new double[rows*cols*nDirections];
		for (int i = 0; i < rows*cols*nDirections; i++) {
			stateProb[i] = 1.0/(rows*cols*nDirections);
		}
	}
	
	/*
	 * Used for debugging
	 */
	public void printTransitionMatrix() {
		for (int row=0; row < rows*cols*nDirections; row++) {
			for (int col=0; col < rows*cols*nDirections; col++) {
				System.out.print(transitionMatrix[row][col] + " ");
			}
			System.out.println();
		}
	}
	
	/*
	 * Help method for the transitionmatrix method
	 */
	
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
	
	/*
	 * Help method for the transitionmatrix method
	 */
	
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
	
	/*
	 * Returns the observation matrix for a observed point from the sensor
	 */
	
	public double[] getObsMatrix(State obState) {
		double[] obs = new double[nbrStates];
		
		obs = createObsFromObservation(obs, obState);
		return obs;
	}
	
	/*
	 * Private help method to create the array for the observation vector
	 */
	private double[] createObsFromObservation(double[] obs, State obState) {
		if (obState.isNothing()) {
			for (int i = 0; i<nbrStates; i++) {
				double probSum = 0.1;
				probSum += 0.05*checkNeighboursOutside(stateMap[i], 1);
				probSum += 0.025*checkNeighboursOutside(stateMap[i], 2);
				obs[i] = probSum;
			}
		} else {
			for (int i = 0; i<nbrStates; i++) {

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
	
	/*
	 * Private helpmethod to see if a state index is number "step" away from obState
	 */
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
				if (i == rV && j == cV) {
					return true;
				}
			}
		}
		return false;
	}
	
	/*
	 * Private helpmethod to see how many available nodes from a sensor output 
	 * are outside the board. Used to calculate the probability when you get
	 * a faulty state from the sensor
	 */
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
	
	/*
	 * Used by the RealLocalizerclass after each sensoroutput.
	 * It uses the sensor output as an input and use the filtering on that point
	 */
	public State localizationOfRobot(int row, int col) {
		State temp = new State(row, col, 1);
		int index = hiddenMM(temp);
		return stateMap[index];
	}
	
	/*
	 * Help method to create the new f in the matrix formula from the book.
	 * After we've created our new f we return the most likely point the robot are at.
	 */
	private int hiddenMM(State sensor) {
		double temp[] = new double[nbrStates];
		double alpha = fixTempAndAlpha(getObsMatrix(sensor), temp);
		return guessState(temp, 1/ alpha);
	}
	
	/*
	 * help method to do the formula from the book. calculates the "temp" which 
	 * is the combined matrix from the T, S and O matrices and alpha.
	 */
	private double fixTempAndAlpha(double[] obs, double[] temp) {
		double alpha = 0;
		for (int r = 0; r < nbrStates; r++) {
			temp[r] = 0;
			for (int i = 0; i<nbrStates; i++) {
				temp[r] += transitionMatrix[i][r] * stateProb[i] * obs[r];
			}
			alpha += temp[r];
		}

		return alpha;
	}
	
	/*
	 * Helpmethod to calculate the new f vector based on the tempmatrix and our alpha from the 
	 * fixTempAndAlpha method. returns the index for the most likely point.
	 *  (Easy to change the most likely state if it's interested)
	 */
	private int guessState(double[] temp, double alpha) {
		int guess = -1;
		double max = Integer.MIN_VALUE;
		for (int i = 0; i<rows; i++) {
			for (int j = 0; j<cols; j++) {
				double sum = 0;
				for (int n = 0; n<nDirections; n++) {
					int index = i*cols*4 + j*4 + n;
					stateProb[index] = temp[index]*alpha;
					sum += temp[i];
				}
				if (sum > max) {
					guess = i*cols*4 + j*4;
					max = sum;
				}
			}

		}
		
		return guess;
	}
	
	/*
	 * Help method to check if the point (row, col) is outside the board/matrix
	 */
	private boolean outsideMatrix(int row, int col) {
		return row < 0 || row >= rows || col < 0 || col >= cols;
	}
	
	/*
	 * Help method to calculate the next state from a certain state.
	 */
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
	
	/*
	 * Help method for the transitionmatrix method. Calcculates the probabilities for the
	 * transition part.
	 */
	private double getLeftovers(State currState, State nextState) {
		if (!stateExists(nextState)) {
			return 1.0;
		}
		setTransitionProb(currState, nextState, 0.7);
		return 0.3;
	}
	
	/*
	 * Help method for the transitionmatrix method. It calculates if a state is inside the
	 * board or not.
	 */
	private boolean stateExists(State state) {
		int row = state.getRow();
		int col = state.getCol();
		if ((row >= 0 && row < rows) && (col >= 0 && col < cols)) {
			return true;
		}
		return false;
	}
	
	/*
	 * Help method for the transitionmatrix method. Inserts the probability values into
	 * the transitionmatrix
	 */
	private void setTransitionProb(State currState, State nextState, double probability) {
		int currStateIdx = getStateIdx(currState);
		int nextStateIdx = getStateIdx(nextState);
		transitionMatrix[currStateIdx][nextStateIdx] = probability;
	}
	
	/*
	 * Help method to get the linear index from a certain state.
	 */
	private int getStateIdx(State state) {
		int row = state.getRow();
		int col = state.getCol();
		int dir = state.getDirection();
		return col*nDirections + dir + row*cols*nDirections;
	}
	
	/*
	 * Method to calculate the probability to go from point (row, col) -> (rRow, rCol).
	 *
	 */
	public double getTProb(int row, int col, int h, int rRow, int rCol, int rH) {
		int currStateIdx = getStateIdx(new State(row, col, h));
		int nextStateIdx = getStateIdx(new State(rRow, rCol, rH));
		return transitionMatrix[currStateIdx][nextStateIdx];
	}
	
	/*
	 * Calculates the probability that the robot is in the point (row, col)
	 */
	
	public double getStateProb(int row, int col) {
		double sum = 0;
		for (int i = 0; i < 4; i++) {
			sum += stateProb[cols*row*4 + col*4 + i];
		}
		return sum;
	}
	
	/*
	 * Mainmethod to debug the program
	 */
	public static void main(String[] args) {
		MatrixCreator mc = new MatrixCreator(3, 3, 4);
		mc.printTransitionMatrix();
	}
}
