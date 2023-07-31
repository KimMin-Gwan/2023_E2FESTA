/* 컴퓨터 그래픽스
 * 1. Midpoint Line Drawing 알고리즘 구현
 * 2. 생성한 Line을 대상으로 Translation 변환 알고리즘 구현
 * 2023.05.27 완성
 * 2023.05.28 수정(1차)
 * 
 * 수정내용
 * -> midpoint line 알고리즘의 계산을 이용하지 않고 선을 그림
 * : drawMidpointLine 함수를 추가. 알고리즘을 이용하여
 *    두 점을 연결하는 선을 그리게 함.
 * -> 계산 과정 중 x,y좌표 출력해서 보고싶은데 주석 해제하면 오류 발생.
 * : Thread.sleep(1000);을 사용하여 delay시켜서 겹치지 않게함. 
 * -> translation한 선은 창의 크기를 조절해야 볼 수 있다.
 * : repaint()함수를 이용하여 JFrame을 다시 그린다.(새로고침(?))
 * -> 선 굵기 조절
 * :  Graphics2D g2 = (Graphics2D) g; ... 추가
 * 주요 과정
 * 1) 시작 좌표와 마지막 좌표를 입력받는다.
 * 2) 입력 받은 좌표를 Midpoint Line Drawing 알고리즘을 이용하여
 *    다음 좌표를 계산한다.
 * 3) 시작 좌표(계산 과정에서 갱신됨)와 다음 좌표를 잇는 선을 그린다.
 * 4) Line(파란색)이 그리는 과정이 끝난 후 이동할 크기를 입력받는다.
 * 5) 입력된 크기만큼 이동된 Line(검은색)이 생성된 것을 확인할 수 있다.
*/

import java.awt.*; // for GUI
import javax.swing.*; // for GUI
import java.util.Scanner; // for input x,y
import java.time.LocalDateTime; //for delay

public class excg extends JFrame {
    private MyPanel panel;
    private int x1, y1, x2, y2; // 시작 좌표(x1,y1), 끝 좌표(x2,y2)

    public excg(int x1, int y1, int x2, int y2){
        setTitle("Midpoint Line Drawing"); // 타이틀 바 이름 지정
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        panel = new MyPanel(x1, y1, x2, y2);
        setContentPane(panel);
        setSize(500, 500); // 창 크기 지정(500*500)
        setVisible(true);
    }

    class MyPanel extends JPanel {
        private int x1, y1, x2, y2;
        private int newX, newY;

        // 처음 line을 그릴 때 필요한 좌표
        public MyPanel(int x1, int y1, int x2, int y2) {
            this.x1 = x1;
            this.y1 = y1;
            this.x2 = x2;
            this.y2 = y2;
        }
        // 이동할 크기의 좌표
        public void setTranslation(int newX, int newY) {
            this.newX = newX;
            this.newY = newY;
        }

        // 생성한 창에 선 그린다.
        public void paintComponent(Graphics g) {
            super.paintComponent(g);
            // midpoint line 알고리즘을 이용하여 그린 선
            g.setColor(Color.BLUE);
            drawMidpointLine(g, x1, y1, x2, y2);

            // 그렸던 선을 translation한 후 생성한 선
            g.setColor(Color.BLACK);
            drawMidpointLine(g, x1+newX, y1+newY, x2+newX, y2+newY);
        }

        private void drawMidpointLine(Graphics g, int x1, int y1, int x2, int y2) {
            // midpoint line 알고리즘 구현

            // 선 굵기 조절
            Graphics2D g2 = (Graphics2D) g;
            g2.setStroke(new BasicStroke(2)); 

            int dx = x2 - x1;
            int dy = y2 - y1;
            int d = dy*2-dx;
            int incrE=dy*2;
            int incrNE=(dy-dx)*2;

            int x = x1, y = y1;

          //  System.out.print(x +"," + y + "\n");
            while (x < x2)
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
                
                g2.drawLine(x, y, x, y);
                System.out.print(x +"," + y + "\n");
                //frame.panel.repaint(); // 다시 그리기 위해 panel을 재호출한다.
            }
        }
    }

    public static void main(String[] args) {
        int x1, x2, y1, y2, newX, newY;
        Scanner sc = new Scanner(System.in);

        // x, y 좌표 입력 받기
        System.out.print("x1: ");
        x1 = sc.nextInt();
        System.out.print("y1: ");
        y1 = sc.nextInt();
        System.out.print("x2: ");
        x2 = sc.nextInt();
        System.out.print("y2: ");
        y2 = sc.nextInt();
        
        excg frame = new excg(x1, y1, x2, y2);

        try {
            //System.out.println("Sleep 1s: "  + LocalDateTime.now());
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        // 이동할 크기 입력 받기
        System.out.println("이동하고 싶은 크기: ");
        System.out.print("newX: ");
        newX = sc.nextInt();
        System.out.print("newY: ");
        newY = sc.nextInt();

        frame.panel.setTranslation(newX, newY);
        // 창 다시그리기
        frame.panel.repaint();
        sc.close();
    }
}