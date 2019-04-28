package co;


import lejos.hardware.lcd.*;
import lejos.hardware.motor.Motor;
import lejos.utility.Delay;

public class Main {

	public Main() {
		// TODO Auto-generated constructor stub
	}

	public static void main(String[] args) {
		int i = 0;
		while(i<10) {
			Motor.B.setSpeed(1000);
			//Motor.B.rotate(180);
			//Delay.msDelay(500);
			Motor.B.backward();
			LCD.drawString("Coucou les amis", 0, 4);
			i++;
		}
	
		
	}

}
