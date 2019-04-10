import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;

import actuators.Motor;
import lejos.robotics.Color;
import sensors.RGBSensor;

enum Face {
	F(0, "bleu"),
	U(1, "rouge"),
	L(2, "jaune"),
	D(3, "orange"),
	R(4, "blanc"),
	B(5, "vert");

	int value;
	String color;
	Face(int value, String color){
		this.value = value;
		this.color = color;
	}
}

enum Orient {
	NW(1, 2, -45),
	N (2, 3, -45),
	NE(3, 6, -45),
	E (6, 9, -45),
	SE(9, 8, -45),
	S (8, 7, -45),
	SW(7, 4, -44),//7,4,-44
	W (4, 5, -1),
	//W (4, 5, -45),
	C (5, 1, -45)
	;

	int value, next, angle;
	Orient(int value, int next, int angle){
		this.value = value;
		this.next = next;
		this.angle = angle;
	}

	static Orient next(Orient curr){
		int length = Orient.values().length;
		for (Orient o : Orient.values()){
			if (o.value == curr.next)
				return o;
		}
		return null;
	}
}

class Flip {
	Orient orient;
	Face face;

	public static Flip getFlipResult(Face f, Orient o){
		Flip flip = new Flip();

		switch (o){
		case N:
			switch(f){
			case F:
				flip.face = Face.U;
				flip.orient = Orient.N;
				break;
			case U:
				flip.face = Face.B;
				flip.orient = Orient.S;
				break;
			case L:
				flip.face = Face.U;
				flip.orient = Orient.E;
				break;
			case D:
				flip.face = Face.F;
				flip.orient = Orient.N;
				break;
			case B:
				flip.face = Face.U;
				flip.orient = Orient.S;
				break;
			case R:
				flip.face = Face.U;
				flip.orient = Orient.W;
				break;
			}
			break;

		case E:
			switch(f){
			case F:
				flip.face = Face.R;
				flip.orient = Orient.E;
				break;
			case U:
				flip.face = Face.R;
				flip.orient = Orient.S;
				break;
			case L:
				flip.face = Face.F;
				flip.orient = Orient.E;
				break;
			case D:
				flip.face = Face.R;
				flip.orient = Orient.N;
				break;
			case B:
				flip.face = Face.L;
				flip.orient = Orient.E;
				break;
			case R:
				flip.face = Face.B;
				flip.orient = Orient.E;
				break;
			}
			break;

		case S:
			switch(f){
			case F:
				flip.face = Face.D;
				flip.orient = Orient.S;
				break;
			case U:
				flip.face = Face.F;
				flip.orient = Orient.S;
				break;
			case L:
				flip.face = Face.D;
				flip.orient = Orient.E;
				break;
			case D:
				flip.face = Face.B;
				flip.orient = Orient.N;
				break;
			case B:
				flip.face = Face.D;
				flip.orient = Orient.N;
				break;
			case R:
				flip.face = Face.D;
				flip.orient = Orient.W;
				break;
			}
			break;

		case W:
			switch(f){
			case F:
				flip.face = Face.L;
				flip.orient = Orient.W;
				break;
			case U:
				flip.face = Face.L;
				flip.orient = Orient.S;
				break;
			case L:
				flip.face = Face.B;
				flip.orient = Orient.W;
				break;
			case D:
				flip.face = Face.L;
				flip.orient = Orient.N;
				break;
			case B:
				flip.face = Face.R;
				flip.orient = Orient.W;
				break;
			case R:
				flip.face = Face.F;
				flip.orient = Orient.W;
				break;
			}
			break;
		default:
			return null;
		}

		return flip;
	}
}

public class Main {
	public Motor motorRot = new Motor("C");
	public Motor motorFlip = new Motor("D");
	public Motor motorCol = new Motor("B");
	
	public RGBSensor colorSensor = new RGBSensor("S4");

	Face face = Face.F;
	Orient orientation = Orient.N;

	public static void main(String[] args) throws IOException {
		new Main();
	}

	public Main() throws IOException {
		//for (int i = 0; i < 10; i++)
		//flipCube();
		//motorCol.moveDegree(-200, 700);
		motorCol.setAbsolute();
		scan();
		//motorCol.moveDegree(0, 700);
		//motorCol.moveDegree(-600, 700);
	}

	public void scan() throws IOException {
		boolean remettre_cote = false;
		HashMap<Integer, Color> res = new HashMap<>();
		
		for (Face face : Face.values()) {
			int compteur = 0;
			for (Orient orient : Orient.values()) {
				goTo(face, orient);
				
				Color c = readColor(compteur);
				res.put(new Integer(face.value +""+ this.orientation.value), c);
				compteur++;
			}
			motorCol.moveDegree(0, 720);
			
			
			
		}
		StringBuilder donnee = new StringBuilder("");
		donnee.append("data = [");
		for (int i = 0; i < 6; i++){
			donnee.append("[");
			for (int j = 1; j < 10; j++) {
				int key = 10* i + j;
				Color c = res.get(key);
				donnee.append("[" + c.getRed() + ", " + c.getGreen() + ", " + c.getBlue() + "],");
			}
			donnee.append("\n],");
		}
		donnee.append("]");
		BufferedWriter writer = new BufferedWriter(new FileWriter("data_1004_max_S_0_3pi.txt"));
	    writer.write(donnee.toString());
	     
	    writer.close();
	    
	}
	
	// data + date + angle motor B + luminosite (L = eclairé , S = sombre,  + R = lumiere naturel) + cran du capteur (0 ,1 ,2) + angle capteur( en pi)



	public void goTo(Face face, Orient orient) {
		//System.out.println("Going to: " + face.color +" "+ orient.name());
		
		if (this.face != face){
			int i = 0;
			while (true){
				//System.out.println("Current: "+ this.face.name() +" "+ this.orientation.name());
				i++;
				Flip flp = Flip.getFlipResult(this.face, this.orientation);
				
				if (flp != null && flp.face == face){
					flipCube();
					break;
				}
				
				if (i > 9 && this.orientation.value % 2 == 0) {
					flipCube();
					i = 0;
				} else {
					rotateCW();
				}
			}
		}		

		while (this.orientation != orient){
			rotateCW();
		}
	}

	void rotateCW(){
		motorRot.moveDegree(orientation.angle*3, 720);
		this.orientation = Orient.next(this.orientation);
	}

	void blockCube(){
		motorFlip.moveDegree(-120, 100);
	}

	void releaseCube(){
		motorFlip.moveDegree(120, 100);
	}

	// 
	void flipCube(){
		motorCol.moveDegree(0, 720);
		
		Flip flp = Flip.getFlipResult(this.face, this.orientation);
		
		if (flp == null){
			System.out.println("Cannot flip");
			return;
		}
		
		motorFlip.moveDegree(-150, 200);
		motorFlip.moveDegree(150, 200);
		
		//motorFlip.moveDegree(-70, 100);
		//motorFlip.moveDegree(70, 100);
		
		motorRot.moveDegree(100, 720);
		motorRot.moveDegree(-100, 720);
		
		this.face = flp.face;
		this.orientation = flp.orient;
	
	}

	// VA ERT VIENS POUR LIRE LES 9 FACET
	Color readColor(int compt){
		//System.out.println("Reading: "+ this.face.name() +" "+ this.orientation.name());
		// cran capteur 0 , angle 3pi
		Color c = new Color(0, 0, 0);
		int angle = 0;
		
		if (compt == 0) {
			angle = 560;
		} else if (orientation.value == 5) {
			//angle = 560;
			angle = 770;
		} else if (orientation.value % 2 == 0){
			//angle = 400;
			angle = 600;
			
		} else {
			//angle = 400;
			angle = 540;
		} 

		/*
		 cran capteur 1 
		if (compt == 0) {
			angle = 570;
		} else if (orientation.value == 5) {
			//angle = 560;
			angle = 780;
		} else if (orientation.value % 2 == 0){
			//angle = 400;
			angle = 590;
			
		} else {
			//angle = 400;
			angle = 510;
		} 
		 */	
		motorCol.moveDegree(-angle, 720);
		c = colorSensor.getColor();

		return c;
	}
}