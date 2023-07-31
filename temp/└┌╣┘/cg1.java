import java.util.Scanner;
import javax.swing.*;
import java.awt.*;

public class cg1 extends JFrame {
    private MyPanel panel;

    public cg1(int X1, int Y1, int X2, int Y2){
        setTitle("midpoint Algorithm");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        panel = new MyPanel(X1, Y1, X2, Y2);
        setContentPane(panel);
        setSize(300,300);
        setVisible(true);
    }
    
    class MyPanel extends JPanel{
        private int X1, Y1, X2, Y2;

        public MyPanel(int X1, int Y1, int X2, int Y2) {
            this.X1 = X1;
            this.Y1 = Y1;
            this.X2 = X2;
            this.Y2 = Y2;
        }

        public void paintComponent(Graphics g){
            super.paintComponent(g);
            g.setColor(Color.BLUE);
            g.drawLine(X1,Y1,X2,Y2);

        }

    }

    public static void main(String [] args){            
        int X1,X2,Y1,Y2;
        Scanner sc = new Scanner(System.in);
        //x,y좌표 입력받는다
        System.out.print("x1 : ");
        X1 = sc.nextInt();
        System.out.print("Y1 : ");
        Y1 = sc.nextInt();
        System.out.print("X2 : ");
        X2 = sc.nextInt();
        System.out.print("Y2 : ");
        Y2 = sc.nextInt();

        cg1 frame = new cg1(X1, Y1, X2, Y2);

        int dx = X2 - X1;
        int dy = Y2 - Y1;
        int d = dy*2-dx;
        int incrE=dy*2;
        int incrNE=(dy-dx)*2;

        int x = X1, y = Y1;

        System.out.print(x +"," + y + "\n");

        while (x < X2)
        {
            if(d<=0){
                d+=incrE;
                x++;
            }
            else{
                d+=incrNE;
                x++;
                y++;
            }   
            System.out.print(x +"," + y + "\n");
            frame.panel.repaint(); // 다시 그리기 위해 panel을 재호출한다.
        }
        sc.close();
    }
}
