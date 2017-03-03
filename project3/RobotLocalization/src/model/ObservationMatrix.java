package model;

import java.util.LinkedList;

public class ObservationMatrix {
	private int rows, cols, nDirections;
	private double[][] observationMatrix;

	public ObservationMatrix(int rows, int cols, int nDirections) {
		this.rows = rows;
		this.cols = cols;
		this.nDirections = nDirections;
		createObservationMatrix();
	}

	private void createObservationMatrix() {
		observationMatrix = new double[rows * cols * nDirections][rows * cols * nDirections];
		for (int row = 0; row < rows; row++) {
			for (int col = 0; col < cols; col++) {
				for (int dir = 0; dir < nDirections; dir++) {
					setObservationProb(row, col, dir);
				}
			}
		}
	}

	private void setObservationProb(int row, int col, int dir) {
		State observedState = new State(row, col, dir);
		LinkedList<State> sameBox = sameBox(observedState);
		LinkedList<State> innerBox = innerBox(observedState);
		LinkedList<State> outerBox = outerBox(observedState);
		for (State s : sameBox) {
			setObserveProb(observedState, s, 0.1);
		}
		for (State s : innerBox) {
			setObserveProb(observedState, s, 0.05);
		}
		for (State s : outerBox) {
			setObserveProb(observedState, s, 0.025);
		}
	}

	private LinkedList<State> sameBox(State observedState) {
		LinkedList<State> ans = new LinkedList<State>();
		for (int dir = 0; dir < nDirections; dir++) {
			ans.add(new State(observedState.getRow(), observedState.getCol(), dir));
		}
		return ans;
	}

	private LinkedList<State> innerBox(State observedState) {
		LinkedList<State> ans = new LinkedList<State>();
		for (int row = -1; row < 2; row++) {
			for (int col = -1; col < 2; col++) {
				for (int dir = 0; dir < nDirections; dir++) {
					if (row == 0 && col == 0) {
						continue;
					}
					State s = new State(observedState.getRow() + row, observedState.getCol() + col, dir);
					if (stateOk(s)) {
						ans.add(s);
					}
				}
			}
		}
		return ans;
	}
	
	private LinkedList<State> outerBox(State observedState) {
		LinkedList<State> ans = new LinkedList<State>();
		for (int row=-2; row < 3; row++) {
			for (int col=-2; col < 3; col++) {
				for (int dir=0; dir < nDirections; dir++) {
					if ((row >= -1 && row < 2) && (col >= -1 && col < 2)) {
						continue;
					}
					State s = new State(observedState.getRow() + row, observedState.getCol() + col, dir);
					if (stateOk(s)) {
						ans.add(s);
					}
				}
			}
		}
		return ans;
	}
	
	private void setObserveProb(State observedState, State guessState, double prob) {
		int observedStateIdx = getStateIdx(observedState);
		int guessStateIdx = getStateIdx(guessState);
		observationMatrix[observedStateIdx][guessStateIdx] = prob;
	}
	
	private int getStateIdx(State s) {
		int row = s.getRow();
		int col = s.getCol();
		int dir = s.getDirection();
		return col*nDirections + dir + row*cols*nDirections;
	}
	
	private boolean stateOk(State s) {
		int row = s.getRow();
		int col = s.getCol();
		if ((row >= 0 && row < rows) && (col >= 0 && col < cols)) {
			return true;
		}
		return false;
	}
}
