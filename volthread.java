package mucomp.ap1;

import java.io.IOException;

public class volthread {

    public volatile int rows = 0;

    public static void main(String[] args) throws IOException {
        volthread v = new volthread();
        v.mycall();
        //this.rows

    }
    public void mycall() {

        volthread vvar = new volthread();
        //voltthreadrun v1 = new voltthreadrun();
        Thread t0 = new Thread(new voltthreadrun(vvar, "t1"));
        Thread t1 = new Thread(new voltthreadrun(vvar, "t2"));

        t0.start();
        t1.start();

        try {
            t0.join();
            t1.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println(vvar.rows);

    }


}