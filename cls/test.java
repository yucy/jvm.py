package cls;

public class test{

	public static void main(String[] args){
		String a = args[0];
		String b = args[1];
		String out = "The [ "+a+" ] is %s than [ "+b+" ].\n";
		if(a.compareTo(b)>0){
			System.out.printf(out,"bigger");
		}else{
			System.out.printf(out,"smaller");
		}
	}
}