package mucomp.ap1;

public class voltthreadrun implements Runnable{
    String tname;
    volthread vvar;
//    volatile int rows;

    public  voltthreadrun(volthread vvar,String tname) {
                this.tname = tname;
                this.vvar = vvar;
    }

    public void run(){

        for (int i=0;i < 100000000;i++){
           synchronized (this.vvar) {
                this.vvar.rows++;
           }
        }
        System.out.println(tname + " : "+ this.vvar.rows);
    }
}
