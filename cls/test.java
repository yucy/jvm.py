package cls;

import java.lang.Exception;

public class test{

    private int m;
    public static int n0=45678;
    public static final int n1=12345;
    public final int n2=23456;
    public int n3=34567;
    public static final int n4="".length();
    public static char char4='z';
    public static String ss="ss_56789";
    public final static String ss0="ss_67890";
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

    public synchronized void tcc() throws Exception{
        int i = 10;
    }

    public static void main(String[] args) {
    	System.out.println("11111111111111");
    	int i = 10;
    	String s = "";
    }

}