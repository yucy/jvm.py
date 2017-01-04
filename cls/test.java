package cls;

public class test{

    private int m;
    public static final int n1=123456;
    public final int n2=23456;
    public int n3=34567;
    public static char char4='z';
    static{
        int test_int = 6789;
        String test_str = "abcde";
    }
    public void inc(int i){  
        switch(i){
            case 2:i = 1;break;
            case 3:i = 2;break;
            case 4:i = 2;break;
            default:i = 0;
        }
    }

    public synchronized void tcc(){
        int i = 10;
    }

    public static void main(String[] args) {
    	System.out.println("11111111111111");
    	int i = 10;
    	String s = "";
    }

}