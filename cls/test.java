package cls;

import java.lang.Exception;
import java.util.List;

public class test{

    private int m;
    public static int n0=45678;
    public static final int n1=12345;
    public final int n2=23456;
    public int n3=34567;
    public static final int n4="".length();
    public static char char4='z';
    public static String ss="ss_56789";
    public static String ssnull=null;
    public final static String ssfinalnull=null;
    public final static String ss0="ss_67890";
    static{
        int test_int = 6789;
        String test_str = "abcde";
    }
    public static void inc(int i,String s){  
        switch(i){
            case 2:i = 1;break;
            case 3:i = 2;break;
            case 4:i = 2;break;
            default:i = 0;
        }
    }

    public synchronized String tcc(int j,String s,List l,String[] d) throws Exception{
        int i = 10;
        return "";
    }

    public static void main(String[] args) {
    	System.out.println("11111111111111");
    	int i = 10;
    	String s = "";
        inc(12,args[0]);
    }

}