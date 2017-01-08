package cls;
/**
* 不产生类构造器（<clinit>方法）的条件。这里需要区别一下实例构造方法<init>
* 1.没有静态语句块
* 2.没有对静态变量的赋值操作
*/
public class test_extends extends test{

    private static int xxx;

    public static void main(String[] args) {
    	System.out.println("11111111111111");
    	int i = 10;
    	String s = "";
    }

}